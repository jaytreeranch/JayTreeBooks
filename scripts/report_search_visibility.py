#!/usr/bin/env python3
"""Compare JayTree Books branded and genre queries from first-party GSC CSV exports.

This does not scrape Google or claim a universal Google rank. Search Console average
position is impression-weighted and may differ by country, device, date and SERP.
Examples:
  python scripts/report_search_visibility.py current.csv --period 2026-11 --out C:/private/report.json
  python scripts/report_search_visibility.py current.csv --previous prior.csv --period 2026-11 --out C:/private/report.json
"""
import argparse
import csv
import json
import re
from pathlib import Path

BRAND_RE = re.compile(r'\bjay\s*tree\s*books?(?:\.com)?\b', re.IGNORECASE)
GENRE_TERMS = (
    "psychological mystery books",
    "psychological mystery book",
    "psychological mystery thriller",
    "new mystery book",
    "new mystery books",
    "mystery thriller books",
)
TRACKED = (
    "jaytree books",
    "jaytreebooks",
    "jaytreebooks.com",
    "psychological mystery books",
    "new mystery book",
    "new mystery books",
)
BUCKETS = ("branded", "genre", "other")

def normalize(query):
    return " ".join(query.lower().split())

def bucket(query):
    value = normalize(query)
    if BRAND_RE.search(value):
        return "branded"
    if any(term in value for term in GENRE_TERMS):
        return "genre"
    return "other"

def category_for_header(name):
    simplified = re.sub(r'[^a-z]', '', name.lower())
    if simplified in ("query", "queries", "topqueries"):
        return "query"
    if simplified in ("clicks", "impressions", "position", "averageposition", "avgposition"):
        return "position" if "position" in simplified else simplified
    return None

def parse_gsc_csv(path):
    rows = []
    with Path(path).open(encoding="utf-8-sig", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None:
            raise ValueError("Empty GSC query CSV")
        cols = {category_for_header(c): c for c in reader.fieldnames if category_for_header(c)}
        required = {"query", "clicks", "impressions", "position"}
        if not required.issubset(cols):
            raise ValueError("Expected Search Console CSV columns: Top queries/Query, Clicks, Impressions, Position")
        for record in reader:
            query = (record[cols["query"]] or "").strip()
            if not query:
                continue
            impressions = int(str(record[cols["impressions"]]).replace(",", ""))
            clicks = int(str(record[cols["clicks"]]).replace(",", ""))
            position = float(str(record[cols["position"]]).replace(",", ""))
            if impressions < 0 or clicks < 0 or position < 0:
                raise ValueError("Invalid negative GSC metric")
            rows.append({"query": query, "clicks": clicks, "impressions": impressions, "position": position, "bucket": bucket(query)})
    return rows

def summarise(rows):
    selected = {}
    for k in BUCKETS:
        filtered = [r for r in rows if r["bucket"] == k]
        impr = sum(r["impressions"] for r in filtered)
        clicks = sum(r["clicks"] for r in filtered)
        weighted = sum(r["position"] * r["impressions"] for r in filtered)
        selected[k] = {"queries_with_data": len(filtered), "clicks": clicks, "impressions": impr,
                       "ctr_percent": round(clicks / impr * 100, 2) if impr else None,
                       "avg_position": round(weighted / impr, 2) if impr else None}
    details = {}
    for needle in TRACKED:
        matches = [r for r in rows if normalize(r["query"]) == needle]
        impr = sum(r["impressions"] for r in matches)
        details[needle] = {
            "observed": bool(impr),
            "clicks": sum(r["clicks"] for r in matches),
            "impressions": impr,
            "avg_position": round(sum(r["position"] * r["impressions"] for r in matches) / impr, 2) if impr else None
        }
    return {"groups": selected, "tracked_queries": details}

def compare(cur, prev):
    if prev is None:
        return None
    diff = {}
    for label in TRACKED:
        a = cur["tracked_queries"][label]["avg_position"]
        b = prev["tracked_queries"][label]["avg_position"]
        diff[label] = round(b - a, 2) if a is not None and b is not None else None
    return diff

def build_report(current_rows, previous_rows=None, period=None):
    cur = summarise(current_rows)
    prev = summarise(previous_rows) if previous_rows is not None else None
    return {
        "site": "https://jaytreebooks.com/",
        "period": period,
        "source": "Owner-exported Google Search Console Performance > Search results > Queries CSV",
        "not_live_api_data": True,
        "caution": "Search Console position is average impression position, not a fixed search-result rank; queries with no impressions are unobserved, not position zero.",
        "current": cur,
        "previous": prev,
        "position_gain_positive_is_better": compare(cur, prev),
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("current", help="CSV exported from Search Console queries")
    parser.add_argument("--previous", help="Earlier CSV for identical country/device/search type and period length")
    parser.add_argument("--period", required=True, help="Explicit date range label, e.g. 2026-11-01..2026-11-14")
    parser.add_argument("--out", required=True, help="Private LAN or local JSON output path (do not commit private GSC data)")
    args = parser.parse_args()
    current = parse_gsc_csv(args.current)
    previous = parse_gsc_csv(args.previous) if args.previous else None
    report = build_report(current, previous, args.period)
    target = Path(args.out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Saved {target}; branded={report['current']['groups']['branded']['impressions']} impressions; genre={report['current']['groups']['genre']['impressions']} impressions")
    print("Any target with no Search Console impressions is UNOBSERVED, not Google page 1 or page 50.")

if __name__ == "__main__":
    main()
