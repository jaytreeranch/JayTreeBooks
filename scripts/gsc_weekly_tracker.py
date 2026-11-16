"""JayTree Books: free Google Search Console weekly keyword history.
Read-only, stdlib only, no passwords or tokens stored in the repository.
"""
import argparse
import csv
import datetime as dt
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import urllib.error
import urllib.parse
import urllib.request
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

PROPERTY = "sc-domain:jaytreebooks.com"
KEYWORDS = (
    "psychological mystery books",
    "new mystery book",
    "psychological thriller books",
    "mystery books",
    "jaytree books",
    "the hollow bell",
)
DEVICES = ("MOBILE", "DESKTOP")
SITES_URL = "https://www.googleapis.com/webmasters/v3/sites"
TOKEN_URL = "https://oauth2.googleapis.com/token"

class GscError(Exception):
    pass

def token():
    if os.environ.get("JT_GSC_ACCESS_TOKEN"):
        return os.environ["JT_GSC_ACCESS_TOKEN"]
    keys = ("JT_GSC_OAUTH_CLIENT_ID", "JT_GSC_OAUTH_CLIENT_SECRET", "JT_GSC_OAUTH_REFRESH_TOKEN")
    values = [os.environ.get(k) for k in keys]
    if not all(values):
        try:
            from gsc_local_auth import AuthorizationError, get_access_token
            return get_access_token()
        except AuthorizationError:
            raise GscError(
                "Google Search Console not yet authorized for this Windows user; "
                "run gsc_local_auth.py --status and complete read-only consent"
            ) from None
    payload = urllib.parse.urlencode(dict(
        client_id=values[0], client_secret=values[1], refresh_token=values[2],
        grant_type="refresh_token")).encode()
    req = urllib.request.Request(TOKEN_URL, data=payload,
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            result = json.load(response)
        return result["access_token"]
    except (urllib.error.HTTPError, urllib.error.URLError, KeyError):
        raise GscError("Google OAuth refresh failed; credentials and responses withheld") from None

def google(url, access, payload=None):
    headers = {"Authorization": "Bearer " + access, "Accept": "application/json"}
    if payload is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, headers=headers,
                                 data=json.dumps(payload).encode() if payload is not None else None)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        raise GscError("Google Search Console API HTTP " + str(exc.code)) from None
    except urllib.error.URLError:
        raise GscError("Google Search Console API network unavailable") from None

def check_property(access, site=PROPERTY):
    data = google(SITES_URL, access)
    if not any(x.get("siteUrl") == site and x.get("permissionLevel") not in
               (None, "siteUnverifiedUser") for x in data.get("siteEntry", [])):
        raise GscError("Google account has no read permission for " + site)

def windows(as_of):
    end = as_of - dt.timedelta(days=3)
    start = end - dt.timedelta(days=27)
    prior_end = start - dt.timedelta(days=1)
    return (
        {"startDate": str(start), "endDate": str(end)},
        {"startDate": str(prior_end - dt.timedelta(days=27)), "endDate": str(prior_end)},
    )

def payload(keyword, device, period):
    filters = [
        {"dimension": "query", "operator": "equals", "expression": keyword},
        {"dimension": "country", "operator": "equals", "expression": "usa"},
        {"dimension": "device", "operator": "equals", "expression": device},
    ]
    return dict(period, type="web", dataState="final", dimensions=["query"],
                aggregationType="byProperty", rowLimit=10,
                dimensionFilterGroups=[{"groupType": "and", "filters": filters}])

def metrics(data, keyword):
    for row in data.get("rows", []):
        if row.get("keys") and row["keys"][0].casefold() == keyword.casefold():
            impressions = int(row.get("impressions", 0))
            return {
                "clicks": int(row.get("clicks", 0)), "impressions": impressions,
                "ctr": round(float(row["ctr"]), 5) if impressions else None,
                "position": round(float(row["position"]), 3) if impressions else None,
                "status": "reported" if impressions else "no_reported_data",
            }
    return {"clicks": 0, "impressions": 0, "ctr": None, "position": None,
            "status": "no_reported_data"}

def collect(as_of, fetch, site=PROPERTY, source="gsc_api"):
    current_window, previous_window = windows(as_of)
    rows = []
    for keyword in KEYWORDS:
        for device in DEVICES:
            now = metrics(fetch(keyword, device, current_window), keyword)
            before = metrics(fetch(keyword, device, previous_window), keyword)
            improvement = (round(before["position"] - now["position"], 3)
                           if now["position"] is not None and before["position"] is not None
                           else None)
            movement = ("not_comparable" if improvement is None else
                        "up" if improvement > 0 else "down" if improvement < 0 else "unchanged")
            rows.append(dict(keyword=keyword, device=device, current=now,
                             previous=before, improvement=improvement, trend=movement))
    return dict(schema=1, source=source, site=site, country="USA",
                as_of=str(as_of), collected_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                current_window=current_window, previous_window=previous_window, rows=rows,
                warning="No reportable impressions is NOT a SERP rank, >50 ranking, or deindexing proof.")

def atomic(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", newline="",
                                         delete=False, dir=path.parent) as handle:
            name = handle.name
            handle.write(text)
        os.replace(name, path)
    finally:
        if name and os.path.exists(name):
            os.unlink(name)

def report(snapshot):
    cur = snapshot["current_window"]
    prev = snapshot["previous_window"]
    lines = [
        "# JayTree Books — Weekly Google Search Performance",
        "",
        "Source: " + snapshot["source"] + "; country USA; Google web; US English target phrases",
        "Snapshot: " + snapshot["as_of"],
        "Current 28 days: " + cur["startDate"] + " — " + cur["endDate"],
        "Previous 28 days: " + prev["startDate"] + " — " + prev["endDate"],
        "",
        "| Keyword | Device | Impressions | Clicks | Avg position | Prior position | Trend |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in snapshot["rows"]:
        now, before = row["current"], row["previous"]
        fmt = lambda v: "-" if v is None else str(v)
        lines.append("| {} | {} | {} | {} | {} | {} | {} |".format(
            row["keyword"], row["device"], now["impressions"], now["clicks"],
            fmt(now["position"]), fmt(before["position"]), row["trend"]))
    lines += [
        "",
        "Lower average position is better: moving from 25 to 18 is an improvement.",
        "An unreported keyword is NOT below #50; Search Console omits some low-volume queries.",
        "Our fixed page-one goals are **psychological mystery books** and **new mystery book**.",
        "",
    ]
    return "\n".join(lines)

def save(snapshot, output):
    # Fixture data NEVER appears in the real Google report or history file.
    is_test = snapshot["source"] != "gsc_api"
    folder = output / ("fixture_snapshots" if is_test else "snapshots")
    atomic(folder / (snapshot["as_of"] + ".json"), json.dumps(snapshot, indent=2) + "\n")
    buffer = io.StringIO(newline="")
    writer = csv.writer(buffer)
    writer.writerow(["as_of", "source", "keyword", "device", "impressions", "clicks",
                     "avg_position", "prior_avg_position", "position_improvement", "trend"])
    for p in sorted(folder.glob("????-??-??.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        for row in data["rows"]:
            writer.writerow([
                data["as_of"], data["source"], row["keyword"], row["device"],
                row["current"]["impressions"], row["current"]["clicks"],
                row["current"]["position"], row["previous"]["position"],
                row["improvement"], row["trend"],
            ])
    atomic(output / ("fixture-history.csv" if is_test else "history.csv"), buffer.getvalue())
    latest = output / ("fixture-latest.md" if is_test else "latest.md")
    atomic(latest, report(snapshot))
    from gsc_local_dashboard import save_dashboard
    filename = "fixture-dashboard.html" if is_test else "dashboard.html"
    save_dashboard(output / ("fixture-history.csv" if is_test else "history.csv"),
                   output / filename, fixture=is_test)
    return str(latest)

def pacific_today():
    """Windows Python may omit IANA zone data; keep the fallback conservative."""
    try:
        return dt.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    except ZoneInfoNotFoundError:
        # At normal daytime weekly runs the date agrees with Pacific year-round.
        return dt.datetime.now(dt.timezone(dt.timedelta(hours=-8))).date()

def import_legacy(path, output):
    """Archive old first-party evidence separately, never as a live keyword rank."""
    data = json.loads(path.read_text(encoding="utf-8"))
    sc = data["search_console"]
    if sc.get("property") != PROPERTY or not isinstance(sc.get("totals"), dict):
        raise GscError("Legacy data is not for the JayTree Search Console domain property")
    captured = data.get("generated_at", "undated")
    archive = {
        "source": "historical_2026_repo_snapshot_not_live",
        "collected_at": captured,
        "property": sc["property"],
        "period": sc.get("period"),
        "totals": sc["totals"],
        "visible_queries": sc.get("visible_queries", []),
        "priority_pages": sc.get("priority_pages", []),
        "warning": "Site average position is not the rank of our two target phrases.",
    }
    folder = output / "legacy"
    atomic(folder / (captured + ".json"), json.dumps(archive, indent=2) + "\n")
    lines = [
        "# Historical JayTree Search Console baseline (not current)",
        "",
        "Source: repository data/seo-search-baseline.json collected " + captured,
        "Window: " + sc["period"]["from"] + " to " + sc["period"]["to"],
        "Property: " + sc["property"],
        "Total clicks: " + str(sc["totals"].get("clicks")),
        "Total impressions: " + str(sc["totals"].get("impressions")),
        "Average position across all shown queries: " + str(sc["totals"].get("average_position")),
        "",
        "Do not interpret this as a current rank for psychological mystery books or new mystery book.",
        "No real current keyword report can be produced until Google read-only OAuth is authorized.",
    ]
    atomic(folder / "README.md", "\n".join(lines) + "\n")
    return str(folder / (captured + ".json"))

def local_consent_ready():
    try:
        from gsc_local_auth import vault_path
        return vault_path().is_file()
    except Exception:
        return False

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--site", default=PROPERTY)
    parser.add_argument("--as-of", type=dt.date.fromisoformat,
                        default=pacific_today())
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--import-legacy", type=Path, help="archive existing September GSC baseline")
    parser.add_argument("--fixture", type=Path, help="TEST ONLY: simulate API response rows")
    args = parser.parse_args(argv)
    if args.status:
        print(json.dumps({"property": args.site, "oauth_present":
                          bool(os.getenv("JT_GSC_ACCESS_TOKEN")) or
                          all(os.getenv(k) for k in ("JT_GSC_OAUTH_CLIENT_ID",
                              "JT_GSC_OAUTH_CLIENT_SECRET", "JT_GSC_OAUTH_REFRESH_TOKEN")),
                          "self_hosted_consent_exists": local_consent_ready(),
                          "historical_snapshots": len(list((args.out / "snapshots").glob("*.json")))
                          if args.out else 0, "paid_plugin": False}))
        return 0
    if not args.out:
        parser.error("--out required for collection")
    try:
        if args.import_legacy:
            print(json.dumps({"result": "PASS", "legacy_file": import_legacy(args.import_legacy, args.out)}))
            return 0
        if args.fixture:
            fixture = json.loads(args.fixture.read_text(encoding="utf-8"))
            def fetch(keyword, device, period):
                segment = "current" if period == windows(args.as_of)[0] else "previous"
                values = fixture.get(device, {}).get(keyword, {}).get(segment)
                return {"rows": [{"keys": [keyword], **values}]} if values else {"rows": []}
            source = "fixture_test"
        else:
            access = token()
            check_property(access, args.site)
            url = SITES_URL + "/" + urllib.parse.quote(args.site, safe="") + "/searchAnalytics/query"
            def fetch(keyword, device, period):
                return google(url, access, payload(keyword, device, period))
            source = "gsc_api"
        snap = collect(args.as_of, fetch, args.site, source)
        print(json.dumps({"result": "PASS", "report": save(snap, args.out), "source": source}))
        return 0
    except (GscError, ValueError, OSError, KeyError) as exc:
        print("BLOCKED: " + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    sys.exit(main())
