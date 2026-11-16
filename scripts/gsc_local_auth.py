"""First-party JayTree Google Search Console OAuth (Windows desktop, no paid apps).

Refresh credentials are protected with per-user Windows DPAPI. OAuth only
requests Google's read-only Search Console permission.
"""
from __future__ import annotations

import argparse
import base64
import ctypes
from ctypes import wintypes
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import webbrowser

SCOPE = "https://www.googleapis.com/auth/webmasters.readonly"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
SITES_URL = "https://www.googleapis.com/webmasters/v3/sites"
VAULT_NAME = "oauth-v1.dpapi"


class AuthorizationError(RuntimeError):
    """No raw OAuth tokens or private responses in errors."""


def vault_path() -> Path:
    base = os.environ.get("LOCALAPPDATA")
    if not base:
        raise AuthorizationError("Local Windows user profile is unavailable")
    return Path(base) / "JayTree" / "GSC" / VAULT_NAME


def _dpapi(value: bytes, *, decrypt: bool) -> bytes:
    """Encrypt/decrypt with Windows per-user DPAPI, without added packages."""
    if os.name != "nt":
        raise AuthorizationError("Encrypted OAuth vault requires Windows")
    class Blob(ctypes.Structure):
        _fields_ = [("cbData", wintypes.DWORD),
                    ("pbData", ctypes.POINTER(ctypes.c_byte))]
    source = ctypes.create_string_buffer(value)
    inbound = Blob(len(value), ctypes.cast(source, ctypes.POINTER(ctypes.c_byte)))
    outbound = Blob()
    crypt = ctypes.windll.crypt32
    if decrypt:
        api = crypt.CryptUnprotectData
        api.argtypes = [ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.POINTER(Blob),
                        ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
        api.restype = wintypes.BOOL
        success = api(ctypes.byref(inbound), None, None, None, None, 1,
                      ctypes.byref(outbound))
    else:
        api = crypt.CryptProtectData
        api.argtypes = [ctypes.POINTER(Blob), wintypes.LPCWSTR, ctypes.POINTER(Blob),
                        ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
        api.restype = wintypes.BOOL
        success = api(ctypes.byref(inbound), "JayTree GSC read-only",
                      None, None, None, 1, ctypes.byref(outbound))
    if not success:
        raise AuthorizationError("Windows user-only OAuth vault unavailable")
    try:
        return ctypes.string_at(outbound.pbData, outbound.cbData)
    finally:
        local_free = ctypes.windll.kernel32.LocalFree
        local_free.argtypes = [ctypes.c_void_p]
        local_free.restype = ctypes.c_void_p
        local_free(outbound.pbData)


def save_authorization(auth: dict, path: Path | None = None) -> Path:
    target = path or vault_path()
    if not all(isinstance(auth.get(field), str) and auth[field]
               for field in ("client_id", "client_secret", "refresh_token")):
        raise AuthorizationError("Cannot store incomplete Google authorization")
    if auth.get("scope") != SCOPE:
        raise AuthorizationError("Read-only Search Console scope required")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = _dpapi(json.dumps(auth, separators=(",", ":")).encode(), decrypt=False)
    temporary = target.with_name(target.name + "." + secrets.token_hex(8) + ".tmp")
    try:
        with open(temporary, "xb") as stream:
            stream.write(payload)
        os.replace(temporary, target)
    finally:
        temporary.unlink(missing_ok=True)
    return target


def load_authorization(path: Path | None = None) -> dict:
    target = path or vault_path()
    try:
        auth = json.loads(_dpapi(target.read_bytes(), decrypt=True))
        if auth.get("scope") != SCOPE:
            raise AuthorizationError("Stored Google permission is not read-only")
        if not all(auth.get(k) for k in ("client_id", "client_secret", "refresh_token")):
            raise AuthorizationError("Stored Google consent is incomplete")
        return auth
    except FileNotFoundError:
        raise AuthorizationError("No Google consent saved for this Windows user") from None
    except (ValueError, UnicodeError):
        raise AuthorizationError("Invalid encrypted Google consent vault") from None


def parse_desktop_client(path: Path) -> dict:
    """Accept desktop OAuth credentials only, never service-account private keys."""
    try:
        client = json.loads(path.read_text(encoding="utf-8"))["installed"]
        ident = client["client_id"]
        secret = client["client_secret"]
        if not isinstance(ident, str) or not ident.endswith(".apps.googleusercontent.com"):
            raise ValueError("Invalid Google desktop client ID")
        if not isinstance(secret, str) or not secret:
            raise ValueError("Invalid Google desktop client secret")
        return {"client_id": ident, "client_secret": secret}
    except (OSError, ValueError, KeyError, TypeError):
        raise AuthorizationError("Select a Google Cloud OAuth Desktop app client JSON") from None


def _post_form(url: str, payload: dict) -> dict:
    req = urllib.request.Request(
        url, data=urllib.parse.urlencode(payload).encode("utf-8"),
        headers={"Content-Type": "application/x-www-form-urlencoded",
                 "Accept": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.load(response)
            if not isinstance(result, dict):
                raise AuthorizationError("Unexpected Google token response")
            return result
    except urllib.error.HTTPError as error:
        raise AuthorizationError("Google rejected OAuth token request (HTTP "
                                 + str(error.code) + ")") from None
    except urllib.error.URLError:
        raise AuthorizationError("Google OAuth endpoint unreachable") from None


def get_access_token(path: Path | None = None) -> str:
    auth = load_authorization(path)
    result = _post_form(TOKEN_URL, {
        "client_id": auth["client_id"], "client_secret": auth["client_secret"],
        "refresh_token": auth["refresh_token"], "grant_type": "refresh_token",
    })
    token = result.get("access_token")
    if not isinstance(token, str) or not token:
        raise AuthorizationError("Google did not return an access token; consent may have expired")
    if result.get("refresh_token") and result["refresh_token"] != auth["refresh_token"]:
        auth["refresh_token"] = result["refresh_token"]
        save_authorization(auth, path)
    return token


def validate_property(access: str, property_url: str = "sc-domain:jaytreebooks.com") -> bool:
    req = urllib.request.Request(
        SITES_URL, headers={"Authorization": "Bearer " + access,
                            "Accept": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=25) as response:
            result = json.load(response)
        return any(s.get("siteUrl") == property_url and
                   s.get("permissionLevel") not in ("siteUnverifiedUser", None)
                   for s in result.get("siteEntry", []))
    except urllib.error.HTTPError as err:
        raise AuthorizationError("Search Console permission check HTTP "
                                 + str(err.code)) from None
    except urllib.error.URLError:
        raise AuthorizationError("Search Console permission check unreachable") from None


def _oauth_parameters(client_id: str, redirect_uri: str,
                      verifier: str, state: str) -> dict:
    challenge = base64.urlsafe_b64encode(
        hashlib.sha256(verifier.encode("ascii")).digest()
    ).decode("ascii").rstrip("=")
    return {
        "client_id": client_id, "redirect_uri": redirect_uri,
        "response_type": "code", "scope": SCOPE, "access_type": "offline",
        "prompt": "consent", "state": state,
        "code_challenge": challenge, "code_challenge_method": "S256",
    }


def authorize_interactively(client_file: Path, *, timeout: int = 300) -> Path:
    """Obtain explicit owner consent in the PC's normal browser, on loopback."""
    client = parse_desktop_client(client_file)
    verifier = secrets.token_urlsafe(64)
    state = secrets.token_urlsafe(32)
    received: dict[str, str] = {}

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            return  # Never log auth codes, state, or query strings.

        def do_GET(self):
            address = urllib.parse.urlsplit(self.path)
            params = urllib.parse.parse_qs(address.query)
            supplied = params.get("state", [""])[0]
            if address.path != "/callback" or not secrets.compare_digest(supplied, state):
                self.send_error(403)
                return
            code = params.get("code", [""])[0]
            failure = params.get("error", [""])[0]
            received["code"] = code
            received["error"] = failure
            page = ("<h3>JayTree Google authorization received.</h3>"
                    "<p>Close this tab. The local program will verify access.</p>")
            self.send_response(200 if code else 400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(page.encode("utf-8"))

    with HTTPServer(("127.0.0.1", 0), Handler) as server:
        server.timeout = 1
        callback = "http://127.0.0.1:" + str(server.server_port) + "/callback"
        params = _oauth_parameters(client["client_id"], callback, verifier, state)
        url = AUTH_URL + "?" + urllib.parse.urlencode(params)
        print("Opening Google's own read-only authorization screen on this Windows computer.")
        if not webbrowser.open(url):
            raise AuthorizationError("Could not launch browser on this computer")
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline and "code" not in received:
            server.handle_request()

    if not received.get("code"):
        raise AuthorizationError("Google authorization declined or timed out")
    result = _post_form(TOKEN_URL, {
        "code": received["code"], "client_id": client["client_id"],
        "client_secret": client["client_secret"], "code_verifier": verifier,
        "redirect_uri": callback, "grant_type": "authorization_code",
    })
    if result.get("scope") and SCOPE not in result["scope"].split():
        raise AuthorizationError("Google did not grant read-only Search Console scope")
    refresh, access = result.get("refresh_token"), result.get("access_token")
    if not isinstance(refresh, str) or not refresh or not isinstance(access, str):
        raise AuthorizationError("Google consent did not return offline read-only access")
    if not validate_property(access):
        raise AuthorizationError("Google user cannot access sc-domain:jaytreebooks.com")
    return save_authorization({
        "client_id": client["client_id"], "client_secret": client["client_secret"],
        "refresh_token": refresh, "scope": SCOPE,
    })


def discover_client_files() -> list[Path]:
    """Only inspect filenames in Downloads; do not search arbitrary private assets."""
    downloads = Path.home() / "Downloads"
    if not downloads.exists():
        return []
    names = list(downloads.glob("client_secret*.json"))
    names.extend(downloads.glob("credentials*.json"))
    return sorted(set(names))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--status", action="store_true")
    modes.add_argument("--authorize", action="store_true")
    modes.add_argument("--check", action="store_true")
    parser.add_argument("--client-file", type=Path, help="Private Google OAuth Desktop client JSON")
    args = parser.parse_args(argv)
    try:
        if args.status:
            print(json.dumps({
                "host": os.environ.get("COMPUTERNAME", ""),
                "private_consent_exists": vault_path().is_file(),
                "candidate_client_filenames": [p.name for p in discover_client_files()],
                "scope": SCOPE, "paid_provider_required": False,
            }))
            return 0
        if args.authorize:
            options = [args.client_file] if args.client_file else discover_client_files()
            if len(options) != 1:
                raise AuthorizationError(
                    "Provide one Google Cloud Desktop OAuth client JSON in Downloads "
                    "or specify its private path with --client-file")
            authorize_interactively(options[0])
            print("Google Search Console read-only consent verified and encrypted locally")
            return 0
        access = get_access_token()
        if not validate_property(access):
            raise AuthorizationError("Signed-in Google account cannot read the domain property")
        print("Authorized: JayTree Books Google Search Console property accessible")
        return 0
    except (AuthorizationError, OSError) as error:
        print("BLOCKED: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
