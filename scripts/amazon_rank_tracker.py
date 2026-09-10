#!/usr/bin/env python3
"""JayTree Books Amazon keyword rank tracker using the Canopy API.

The script queries Amazon search results for configured keywords and records the
organic position of the target ASIN. It is designed for GitHub Actions and keeps
API usage conservative for Canopy's Hobby plan.
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
from urllib.parse import quote
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_KEY = os.environ.get("CANOPY_API_KEY", "").strip()
TARGET_ASIN = os.environ.get("TARGET_ASIN", "B0HD52HGGZ").strip()
COUNTRY = os.environ.get("AMAZON_COUNTRY", "US").strip()
MAX_PAGES = int(os.environ.get("MAX_PAGES", "5"))

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
    """Query Canopy's REST search endpoint.

    Canopy documents a REST Search API at /api/search with query, page and domain
    parameters and API-key authentication via the Authorization header.
    """
    base = "https://rest.canopyapi.co/api/search"
    url = f"{base}?query={quote(keyword)}&page={page}&domain={COUNTRY}"
    req = Request(
        url,
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Accept": "application/json",
            "User-Agent": "JayTreeBooks-AmazonRankTracker/1.0",
        },
    )
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_results(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Handle the common result shapes used by Canopy Search API responses."""
    candidates = [
        payload.get("searchResults"),
        payload.get("results"),
        payload.get("organicResults"),
        payload.get("data", {}).get("searchResults") if isinstance(payload.get("data"), dict) else None,
        payload.get("data", {}).get("results") if isinstance(payload.get("data"), dict) else None,
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
    for key in ("sponsored", "isSponsored", "is_sponsored"):
        if key in item:
            return bool(item[key])
    return False


def title_of(item: dict[str, Any]) -> str:
    for key in ("title", "name", "productTitle"):
        value = item.get(key)
        if value:
            return str(value)
    product = item.get("product")
    if isinstance(product, dict):
        return str(product.get("title", ""))
    return ""


def rank_keyword(keyword: str) -> dict[str, Any]:
    organic_seen = 0
    sponsored_matches: list[dict[str, Any]] = []

    for page in range(1, MAX_PAGES + 1):
        payload = canopy_search(keyword, page)
        results = extract_results(payload)

        if not results:
            return {
                "keyword": keyword,
                "found": False,
                "organic_rank": None,
                "page": None,
                "sponsored_seen": bool(sponsored_matches),
                "status": "no_results_or_unrecognized_response",
            }

        for item in results:
            asin = normalize_asin(item)
            sponsored = is_sponsored(item)
            if sponsored:
                if asin.upper() == TARGET_ASIN.upper():
                    sponsored_matches.append({"page": page, "title": title_of(item)})
                continue

            organic_seen += 1
            if asin.upper() == TARGET_ASIN.upper():
                return {
                    "keyword": keyword,
                    "found": True,
                    "organic_rank": organic_seen,
                    "page": page,
                    "sponsored_seen": bool(sponsored_matches),
                    "status": "found",
                }

        time.sleep(0.35)

    return {
        "keyword": keyword,
        "found": False,
        "organic_rank": None,
        "page": None,
        "sponsored_seen": bool(sponsored_matches),
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

    keywords_env = os.environ.get("KEYWORDS", "").strip()
    keywords = [k.strip() for k in keywords_env.split("|") if k.strip()] if keywords_env else DEFAULT_KEYWORDS

    rows: list[dict[str, Any]] = []
    for keyword in keywords:
        print(f"Checking: {keyword}")
        try:
            row = rank_keyword(keyword)
        except HTTPError as exc:
            row = {
                "keyword": keyword,
                "found": False,
                "organic_rank": None,
                "page": None,
                "sponsored_seen": False,
                "status": f"http_error_{exc.code}",
            }
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
