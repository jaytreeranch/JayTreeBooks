"""Offline QC for free Google Search Console history (no API credentials)."""
import datetime as dt
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gsc_weekly_tracker as gsc


class SearchHistoryTests(unittest.TestCase):
    def test_fixed_page_one_goals(self):
        self.assertEqual(gsc.KEYWORDS[:2], (
            "psychological mystery books", "new mystery book"))

    def test_two_complete_28_day_windows(self):
        now, old = gsc.windows(dt.date(2026, 11, 15))
        self.assertEqual(now, {"startDate": "2026-10-16", "endDate": "2026-11-12"})
        self.assertEqual(old, {"startDate": "2026-09-18", "endDate": "2026-10-15"})

    def test_request_exact_us_device_read_only(self):
        data = gsc.payload("new mystery book", "MOBILE",
                           {"startDate": "2026-10-16", "endDate": "2026-11-12"})
        self.assertEqual(data["type"], "web")
        self.assertEqual(data["dataState"], "final")
        self.assertEqual(data["rowLimit"], 10)
        filters = data["dimensionFilterGroups"][0]["filters"]
        self.assertEqual([(f["dimension"], f["expression"]) for f in filters],
                         [("query", "new mystery book"), ("country", "usa"),
                          ("device", "MOBILE")])

    def test_no_impressions_is_not_rank_50(self):
        result = gsc.metrics({"rows": []}, "psychological mystery books")
        self.assertEqual(result["status"], "no_reported_data")
        self.assertIsNone(result["position"])

    def test_rank_direction_and_missing_baseline(self):
        def fetched(keyword, device, period):
            if keyword == gsc.KEYWORDS[0] and device == "MOBILE":
                pos = 18 if period["startDate"] == "2026-10-16" else 25
                return {"rows": [{
                    "keys": [keyword], "clicks": 2, "impressions": 100,
                    "ctr": 0.02, "position": pos}]}
            return {"rows": []}
        snap = gsc.collect(dt.date(2026, 11, 15), fetched)
        self.assertEqual(snap["rows"][0]["improvement"], 7)
        self.assertEqual(snap["rows"][0]["trend"], "up")
        self.assertEqual(snap["rows"][1]["trend"], "not_comparable")
        self.assertIsNone(snap["rows"][1]["current"]["position"])

    def test_idempotent_history_and_no_fake_production_output(self):
        snap = gsc.collect(dt.date(2026, 11, 15),
                           lambda kw, dev, period: {"rows": []},
                           source="fixture_test")
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            gsc.save(snap, folder)
            gsc.save(snap, folder)
            lines = (folder / "fixture-history.csv").read_text().splitlines()
            self.assertEqual(len(lines), 1 + len(gsc.KEYWORDS) * len(gsc.DEVICES))
            self.assertFalse((folder / "history.csv").exists())
            self.assertFalse((folder / "snapshots").exists())
            self.assertIn("NOT a SERP", snap["warning"])

    def test_credentials_absent_fail_closed(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(gsc.GscError):
                gsc.token()

    def test_validate_property_requires_permission(self):
        with patch.object(gsc, "google", return_value={
            "siteEntry": [{"siteUrl": gsc.PROPERTY, "permissionLevel": "siteUnverifiedUser"}]
        }):
            with self.assertRaises(gsc.GscError):
                gsc.check_property("fake")

    def test_api_failure_does_not_create_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch.dict(os.environ, {}, clear=True):
                self.assertEqual(gsc.main(["--out", tmp, "--as-of", "2026-11-15"]), 2)
                self.assertFalse((Path(tmp) / "snapshots").exists())


    def test_legacy_archive_preserves_source_not_target_rank(self):
        original = {
            "generated_at": "2026-09-24",
            "search_console": {
                "property": gsc.PROPERTY,
                "period": {"from": "2026-08-25", "to": "2026-09-21"},
                "totals": {"clicks": 16, "impressions": 80, "average_position": 5.475}
            }
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            inp = root / "baseline.json"
            inp.write_text(json.dumps(original), encoding="utf-8")
            output = gsc.import_legacy(inp, root / "output")
            data = json.loads(Path(output).read_text())
            self.assertEqual(data["totals"]["clicks"], 16)
            self.assertIn("not the rank", data["warning"])
            self.assertFalse((root / "output" / "history.csv").exists())
if __name__ == "__main__":
    unittest.main()
