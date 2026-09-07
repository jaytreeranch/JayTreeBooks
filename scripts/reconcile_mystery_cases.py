#!/usr/bin/env python3
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import sync_youtube_uploads as sync

ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "data" / "youtube-sync.json"


def main() -> int:
    channel_id = sync._resolve_channel_id()
    entries = sync._feed_entries(channel_id)
    registry = sync._load_registry(channel_id)
    cases = registry.setdefault("mystery_cases", {})

    for entry in reversed([e for e in entries if sync._is_after_cutoff(e, registry)]):
        number = sync._case_number(entry["title"])
        if not number:
            continue

        title = entry["title"]
        lowered = title.casefold()
        duration = sync._duration_seconds(entry["video_id"])
        video = dict(entry)
        video["duration_seconds"] = duration
        record = cases.setdefault(number, {})

        if "reveal" in lowered or "solution" in lowered or "solved" in lowered:
            record["reveal"] = video
            continue

        explicit_short = any(term in lowered for term in ("#shorts", "shorts", "teaser"))
        explicit_case = any(term in lowered for term in ("full case", "can you solve", "mystery case"))

        if explicit_short:
            record["teaser"] = video
        elif explicit_case or duration >= 180:
            record["case"] = video
        elif duration < 120:
            record["teaser"] = video

    latest_number = None
    latest_stamp = ""
    for number, record in cases.items():
        stamp = max(
            [str((record.get(kind) or {}).get("published") or "") for kind in ("case", "reveal", "teaser")]
            or [""]
        )
        if stamp > latest_stamp:
            latest_stamp = stamp
            latest_number = number

    if latest_number:
        record = cases[latest_number]
        registry["latest_mystery_case"] = {
            "case_number": latest_number,
            "case": record.get("case"),
            "reveal": record.get("reveal"),
            "teaser": record.get("teaser"),
        }

    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    registry["last_checked"] = now
    registry["last_synced"] = now
    REGISTRY_PATH.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sync._update_index(registry)

    latest = registry.get("latest_mystery_case") or {}
    case = latest.get("case") or {}
    print(f"Mystery Case reconcile complete: case #{latest.get('case_number') or 'none'} -> {case.get('url') or 'no full case found'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
