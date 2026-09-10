#!/usr/bin/env python3
"""JayTree Books Amazon keyword rank tracker using the Canopy API.

Queries Canopy's Amazon Search API and records where a target ASIN appears for
selected shopper searches. The defaults are intentionally conservative so the
workflow stays well within Canopy Hobby's 100-request monthly allowance.
"""

from __future__ import annotations

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_KEY = os.environ.get("CANOPY_API_KEY", "").strip()
TARGET_ASIN = os.environ.get("TARGET_ASIN", "B0HD52HGGZ").strip()
COUNTRY = os.environ.get("AMAZON_COUNTRY", "US").strip()
SEARCH_INDEX = os.environ.get("AMAZON_SEARCH_INDEX", "KindleStore").strip()
MAX_PAGES = int(os.environ.get("MAX_PAGES", "1"))

DEFAULT_KEYWORDS = [
    "cold case mystery",
    "small town mystery",
    "small town cold case mystery",
    "missing sister mystery",
    "missing person mystery",
    "police procedural mystery",
    "women sleuth mystery",
    "atmospheric mystery",
    "supernatural mystery",
    "family secrets mystery",
]


def canopy_search(keyword: str, page: int) -> dict[str, Any]:
    """Query Canopy's current REST Amazon Search endpoint."""
    params = {
        "searchTerm": keyword,
        "domain": COUNTRY,
        "page": str(page),
    }
    if SEARCH_INDEX:
        params["searchIndex"] = SEARCH_INDEX

    url = "https://rest.canopyapi.co/v1/amazon/search?" + urlencode(params)
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json",
            "User-Agent": "JayTreeBooks-AmazonRankTracker/1.1",
        },
    )
    with urlopen(req, timeout=45) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle known and legacy Canopy search response shapes."""
    data = payload.get("data") if isinstance(payload.get("data"), dict) else {}
    candidates = [
        payload.get("searchResults"),
        payload.get("results"),
        payload.get("organicResults"),
        data.get("searchResults"),
        data.get("results"),
    ]
    for value in candidates:
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def normalize_asin(item: dict[str, Any]) -> str:
    for key in ("asin", "ASIN", "productAsin", "product_asin"):
        value = item.get(key)
        if value:
            return str(value).strip()
    product = item.get("product")
    if isinstance(product, dict):
        for key in ("asin", "ASIN"):
            if product.get(key):
                return str(product[key]).strip()
    return ""


def is_sponsored(item: dict[str, Any]) -> bool:
    for key in ("sponsored", "isSponsored", "is_sponsored", "sponsoredAd", "isAd"):
        if key in item:
            value = item[key]
            if isinstance(value, str):
                return value.lower() in {"true", "1", "yes", "sponsored"}
            return bool(value)
    return False


def rank_keyword(keyword: str) -> dict[str, Any]:
    organic_seen = 0
    sponsored_seen = False

    for page in range(1, MAX_PAGES + 1):
        payload = canopy_search(keyword, page)
        results = extract_results(payload)

        if not results:
            return {
                "keyword": keyword,
                "found": False,
                "organic_rank": None,
                "page": None,
                "sponsored_seen": sponsored_seen,
                "status": "no_results_or_unrecognized_response",
            }

        for item in results:
            asin = normalize_asin(item)
            sponsored = is_sponsored(item)
            if sponsored:
                if asin.upper() == TARGET_ASIN.upper():
                    sponsored_seen = True
                continue

            organic_seen += 1
            if asin.upper() == TARGET_ASIN.upper():
                return {
                    "keyword": keyword,
                    "found": True,
                    "organic_rank": organic_seen,
                    "page": page,
                    "sponsored_seen": sponsored_seen,
                    "status": "found",
                }

        time.sleep(0.35)

    return {
        "keyword": keyword,
        "found": False,
        "organic_rank": None,
        "page": None,
        "sponsored_seen": sponsored_seen,
        "status": f"not_found_first_{MAX_PAGES}_pages",
    }


def write_outputs(rows: list[dict[str, Any]]) -> None:
    out_dir = Path("reports/amazon-rank")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    csv_path = out_dir / f"amazon-rank-{stamp}.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["keyword", "found", "organic_rank", "page", "sponsored_seen", "status"],
        )
        writer.writeheader()
        writer.writerows(rows)

    md_path = out_dir / "latest.md"
    lines = [
        "# Amazon Keyword Rank Report",
        "",
        f"- ASIN: `{TARGET_ASIN}`",
        f"- Marketplace: `{COUNTRY}`",
        f"- Search index: `{SEARCH_INDEX or 'All'}`",
        f"- Checked: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Max pages per keyword: `{MAX_PAGES}`",
        "",
        "| Keyword | Organic Rank | Page | Sponsored Seen | Status |",
        "|---|---:|---:|:---:|---|",
    ]
    for row in rows:
        rank = row["organic_rank"] if row["organic_rank"] is not None else "—"
        page = row["page"] if row["page"] is not None else "—"
        lines.append(
            f"| {row['keyword']} | {rank} | {page} | {'Yes' if row['sponsored_seen'] else 'No'} | {row['status']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if not API_KEY:
        print("ERROR: CANOPY_API_KEY is not set", file=sys.stderr)
        return 2

    if MAX_PAGES < 1 or MAX_PAGES > 10:
        print("ERROR: MAX_PAGES must be between 1 and 10", file=sys.stderr)
        return 2

    keywords_env = os.environ.get("KEYWORDS", "").strip()
    keywords = [k.strip() for k in keywords_env.split("|") if k.strip()] if keywords_env else DEFAULT_KEYWORDS

    estimated_requests = len(keywords) * MAX_PAGES
    print(f"Target ASIN: {TARGET_ASIN}")
    print(f"Search index: {SEARCH_INDEX}")
    print(f"Keywords: {len(keywords)}")
    print(f"Maximum possible API requests this run: {estimated_requests}")

    if estimated_requests > 50:
        print("ERROR: Refusing a run that could consume more than 50 Canopy requests.", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    for keyword in keywords:
        print(f"Checking: {keyword}")
        try:
            row = rank_keyword(keyword)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            print(f"HTTP {exc.code}: {body}", file=sys.stderr)
            row = {
                "keyword": keyword,
                "found": False,
                "organic_rank": None,
                "page": None,
                "sponsored_seen": False,
                "status": f"http_error_{exc.code}",
            }
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"Request error: {exc}", file=sys.stderr)
            row = {
                "keyword": keyword,
                "found": False,
                "organic_rank": None,
                "page": None,
                "sponsored_seen": False,
                "status": f"error_{type(exc).__name__}",
            }
        rows.append(row)
        print(row)

    write_outputs(rows)

    if all(row["status"].startswith(("http_error_", "error_", "no_results")) for row in rows):
        print("ERROR: All keyword checks failed; inspect the API response before trusting the report.", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
