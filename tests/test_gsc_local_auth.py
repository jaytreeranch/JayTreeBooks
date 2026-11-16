"""Security and functionality tests for self-owned Google Search Console OAuth.

No real Google accounts, login windows, browser sessions or API charges.
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gsc_local_auth as auth
import gsc_local_dashboard as dashboard
import gsc_weekly_tracker as gsc


class LocalOAuthTests(unittest.TestCase):
    def fixture_authorization(self):
        return {
            "client_id": "demo.apps.googleusercontent.com",
            "client_secret": "TEST_PRIVATE_CLIENT_SECRET",
            "refresh_token": "TEST_REFRESH_TOKEN",
            "scope": auth.SCOPE,
        }

    def test_read_only_scope(self):
        self.assertEqual(auth.SCOPE, "https://www.googleapis.com/auth/webmasters.readonly")
        self.assertNotIn(auth.SCOPE, ("https://www.googleapis.com/auth/webmasters",))

    def test_no_google_desktop_client(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "service_account.json"
            path.write_text(json.dumps({"type": "service_account",
                                        "private_key": "DO_NOT_USE"}))
            with self.assertRaises(auth.AuthorizationError):
                auth.parse_desktop_client(path)

    def test_desktop_client_is_validated(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "client_secret.json"
            payload = {"installed": {"client_id": "demo.apps.googleusercontent.com",
                                     "client_secret": "test_dummy"}}
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertEqual(auth.parse_desktop_client(path)["client_id"], payload["installed"]["client_id"])
            payload["installed"]["client_id"] = "invalid-google-client"
            path.write_text(json.dumps(payload), encoding="utf-8")
            with self.assertRaises(auth.AuthorizationError):
                auth.parse_desktop_client(path)

    def test_windows_dpapi_encrypted_token_not_plaintext(self):
        if os.name != "nt":
            self.skipTest("Windows DPAPI only")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test-token.dpapi"
            source = self.fixture_authorization()
            auth.save_authorization(source, path)
            data = path.read_bytes()
            self.assertNotIn(b"TEST_REFRESH_TOKEN", data)
            self.assertNotIn(b"TEST_PRIVATE_CLIENT_SECRET", data)
            self.assertEqual(auth.load_authorization(path), source)

    def test_missing_consent_fails_without_google_request(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.dpapi"
            with self.assertRaises(auth.AuthorizationError):
                auth.load_authorization(path)

    def test_wrong_scope_cannot_be_saved(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "no-admin.dpapi"
            record = self.fixture_authorization()
            record["scope"] = "https://www.googleapis.com/auth/webmasters"
            with self.assertRaises(auth.AuthorizationError):
                auth.save_authorization(record, path)
            self.assertFalse(path.exists())

    def test_google_authorization_uses_pkce_and_random_state(self):
        params = auth._oauth_parameters("demo.apps.googleusercontent.com",
                                        "http://127.0.0.1:49100/callback",
                                        "example-verifier-secret", "random-state-secret")
        expected = base64.urlsafe_b64encode(
            hashlib.sha256(b"example-verifier-secret").digest()).decode("ascii").rstrip("=")
        self.assertEqual(params["code_challenge"], expected)
        self.assertEqual(params["code_challenge_method"], "S256")
        self.assertEqual(params["scope"], auth.SCOPE)
        self.assertEqual(params["response_type"], "code")
        self.assertEqual(params["access_type"], "offline")

    def test_refresh_uses_encrypted_vault_without_persisting_access_token(self):
        if os.name != "nt":
            self.skipTest("Windows DPAPI only")
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test-token.dpapi"
            auth.save_authorization(self.fixture_authorization(), path)
            before = path.read_bytes()
            with patch.object(auth, "_post_form", return_value={"access_token": "TEMP_GOOGLE_ACCESS_TOKEN"}) as call:
                access = auth.get_access_token(path)
            self.assertEqual(access, "TEMP_GOOGLE_ACCESS_TOKEN")
            self.assertEqual(call.call_args.args[0], auth.TOKEN_URL)
            self.assertEqual(call.call_args.args[1]["grant_type"], "refresh_token")
            self.assertEqual(before, path.read_bytes())
            self.assertNotIn(b"TEMP_GOOGLE_ACCESS_TOKEN", path.read_bytes())

    def test_provider_error_never_leaks_private_body(self):
        import io
        import urllib.error
        error = urllib.error.HTTPError(
            "https://oauth2.googleapis.com/token", 400, "bad request", {},
            io.BytesIO(b"refresh_token=HIGHLY_PRIVATE"))
        with patch.object(auth.urllib.request, "urlopen", side_effect=error):
            with self.assertRaises(auth.AuthorizationError) as caught:
                auth._post_form(auth.TOKEN_URL, {"foo": "bar"})
        self.assertNotIn("HIGHLY_PRIVATE", str(caught.exception))

    def test_collector_can_use_local_secure_refresh(self):
        with patch.dict(os.environ, {}, clear=True):
            with patch.object(auth, "get_access_token", return_value="FAKE_READ_ONLY_TOKEN"):
                self.assertEqual(gsc.token(), "FAKE_READ_ONLY_TOKEN")

    def test_local_consent_status_does_not_require_google_network(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch.dict(os.environ, {"LOCALAPPDATA": folder}):
                self.assertFalse(gsc.local_consent_ready())

    def test_privately_saved_permission_not_accidentally_admin(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "missing.dpapi"
            with self.assertRaises(auth.AuthorizationError):
                auth.get_access_token(path)


    def test_offline_dashboard_escapes_untrusted_strings(self):
        import csv
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "history.csv"
            with path.open("w", newline="", encoding="utf-8") as stream:
                writer = csv.DictWriter(stream, fieldnames=[
                    "as_of", "source", "keyword", "device", "impressions",
                    "clicks", "avg_position", "prior_avg_position",
                    "position_improvement", "trend"])
                writer.writeheader()
                writer.writerow({
                    "as_of": "2026-11-16", "source": "fixture_test",
                    "keyword": "<script>alert('x')</script>", "device": "MOBILE",
                    "impressions": "10", "clicks": "2",
                    "avg_position": "18", "prior_avg_position": "25",
                    "position_improvement": "7", "trend": "up"})
            output = dashboard.render(path, fixture=True)
            self.assertNotIn("<script>alert(", output)
            self.assertIn("&lt;script&gt;", output)
            self.assertIn("TEST DATA ONLY", output)
            self.assertIn("<svg", output)
            self.assertNotIn('src="https://', output)
            self.assertNotIn('href="https://', output)
            with self.assertRaises(ValueError):
                dashboard.render(path, fixture=False)

    def test_collector_fixture_emits_only_fixture_dashboard(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)
            snap = gsc.collect(__import__("datetime").date(2026, 11, 16),
                               lambda query, device, period: {"rows": []},
                               source="fixture_test")
            gsc.save(snap, path)
            self.assertTrue((path / "fixture-dashboard.html").is_file())
            self.assertFalse((path / "dashboard.html").exists())
            self.assertFalse((path / "history.csv").exists())
    def test_google_permission_error_discloses_only_safe_reason(self):
        import io
        import urllib.error
        response = io.BytesIO(json.dumps({
            "error": {
                "status": "PERMISSION_DENIED",
                "message": "PRIVATE Google project or user identity",
                "errors": [{"reason": "accessNotConfigured"}],
            },
        }).encode("utf-8"))
        exc = urllib.error.HTTPError(
            "https://www.googleapis.com/webmasters/v3/sites",
            403, "Forbidden", {}, response)
        with patch.object(auth.urllib.request, "urlopen", side_effect=exc):
            with self.assertRaises(auth.AuthorizationError) as caught:
                auth.validate_property("FAKE_ACCESS_TOKEN")
        self.assertIn("accessNotConfigured", str(caught.exception))
        self.assertNotIn("PRIVATE", str(caught.exception))
        self.assertNotIn("FAKE_ACCESS_TOKEN", str(caught.exception))
if __name__ == "__main__":
    unittest.main()
