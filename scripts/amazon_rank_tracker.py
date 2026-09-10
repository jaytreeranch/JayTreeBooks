#!/usr/bin/env python3
"""JayTree Books Amazon keyword rank tracker using Canopy GraphQL.

The tracker follows Canopy's documented keyword-rank query shape. Each keyword
uses one GraphQL request while retrieving several Amazon result pages through
GraphQL aliases, which keeps usage low on the Canopy Hobby plan.
"""

from __future__ import annotations

import csv
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

API_KEY = os.environ.get("CANOPY_API_KEY", "").strip()
TARGET_ASIN = os.environ.get("TARGET_ASIN", "B0HD52HGGZ").strip()
COUNTRY = os.environ.get("AMAZON_COUNTRY", "US").strip()
MAX_PAGES = int(os.environ.get("MAX_PAGES", "5"))
PAGE_SIZE = 40
GRAPHQL_URL = "https://graphql.canopyapi.co/"

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


class CanopyGraphQLError(RuntimeError):
    pass


def build_query() -> str:
    page_fields = []
    for page in range(1, MAX_PAGES + 1):
        page_fields.append(
            f'''page{page}: productResults(input: {{ page: {page}, limit: {PAGE_SIZE}, sort: FEATURED }}) {{
              results {{ asin title sponsored }}
              pageInfo {{ currentPage hasNextPage }}
            }}'''
        )
    pages = "\n".join(page_fields)
    return f'''query KeywordRank($input: AmazonProductSearchResultsInput!) {{
      amazonProductSearchResults(input: $input) {{
        {pages}
      }}
    }}'''


def canopy_search(keyword: str) -> dict[str, Any]:
    payload = {
        "query": build_query(),
        "variables": {"input": {"searchTerm": keyword, "domain": COUNTRY}},
    }
    body = json.dumps(payload).encode("utf-8")
    req = Request(
        GRAPHQL_URL,
        data=body,
        method="POST",
        headers={
            "API-KEY": API_KEY,
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "JayTreeBooks-AmazonRankTracker/2.0",
        },
    )
    with urlopen(req, timeout=90) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("errors"):
        msg = "; ".join(str(e.get("message", e)) for e in data["errors"][:3])
        raise CanopyGraphQLError(msg)
    return data


def rank_keyword(keyword: str) -> dict[str, Any]:
    payload = canopy_search(keyword)
    search = payload.get("data", {}).get("amazonProductSearchResults")
    if not isinstance(search, dict):
        raise CanopyGraphQLError("Missing data.amazonProductSearchResults")

    organic_seen = 0
    sponsored_seen = False
    pages_scanned = 0

    for page in range(1, MAX_PAGES + 1):
        block = search.get(f"page{page}")
        if not isinstance(block, dict):
            break
        results = block.get("results") or []
        if not isinstance(results, list):
            break
        if not results:
            break
        pages_scanned += 1

        for item in results:
            if not isinstance(item, dict):
                continue
            asin = str(item.get("asin") or "").strip().upper()
            sponsored = bool(item.get("sponsored", False))
            if sponsored:
                if asin == TARGET_ASIN.upper():
                    sponsored_seen = True
                continue

            organic_seen += 1
            if asin == TARGET_ASIN.upper():
                return {
                    "keyword": keyword,
                    "found": True,
                    "organic_rank": organic_seen,
                    "page": page,
                    "sponsored_seen": sponsored_seen,
                    "results_scanned": organic_seen,
                    "status": "found",
                }

        page_info = block.get("pageInfo") or {}
        if isinstance(page_info, dict) and page_info.get("hasNextPage") is False:
            break

    return {
        "keyword": keyword,
        "found": False,
        "organic_rank": None,
        "page": None,
        "sponsored_seen": sponsored_seen,
        "results_scanned": organic_seen,
        "status": f"not_found_after_{pages_scanned}_pages_{organic_seen}_organic_results",
    }


def write_outputs(rows: list[dict[str, Any]]) -> None:
    out_dir = Path("reports/amazon-rank")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    csv_path = out_dir / f"amazon-rank-{stamp}.csv"
    fields = ["keyword", "found", "organic_rank", "page", "sponsored_seen", "results_scanned", "status"]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    md_path = out_dir / "latest.md"
    lines = [
        "# Amazon Keyword Rank Report",
        "",
        f"- ASIN: `{TARGET_ASIN}`",
        f"- Marketplace: `{COUNTRY}`",
        "- API: `Canopy GraphQL`",
        f"- Checked: `{datetime.now(timezone.utc).isoformat()}`",
        f"- Maximum pages requested per keyword: `{MAX_PAGES}`",
        f"- Page size requested: `{PAGE_SIZE}`",
        "",
        "| Keyword | Organic Rank | Page | Organic Results Scanned | Sponsored Seen | Status |",
        "|---|---:|---:|---:|:---:|---|",
    ]
    for row in rows:
        rank = row["organic_rank"] if row["organic_rank"] is not None else "—"
        page = row["page"] if row["page"] is not None else "—"
        lines.append(
            f"| {row['keyword']} | {rank} | {page} | {row['results_scanned']} | "
            f"{'Yes' if row['sponsored_seen'] else 'No'} | {row['status']} |"
        )
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def failure_row(keyword: str, status: str) -> dict[str, Any]:
    return {
        "keyword": keyword,
        "found": False,
        "organic_rank": None,
        "page": None,
        "sponsored_seen": False,
        "results_scanned": 0,
        "status": status,
    }


def main() -> int:
    if not API_KEY:
        print("ERROR: CANOPY_API_KEY is not set", file=sys.stderr)
        return 2
    if MAX_PAGES < 1 or MAX_PAGES > 5:
        print("ERROR: MAX_PAGES must be between 1 and 5", file=sys.stderr)
        return 2

    keywords_env = os.environ.get("KEYWORDS", "").strip()
    keywords = [k.strip() for k in keywords_env.split("|") if k.strip()] if keywords_env else DEFAULT_KEYWORDS

    estimated_requests = len(keywords)
    print(f"Target ASIN: {TARGET_ASIN}")
    print(f"Marketplace: {COUNTRY}")
    print(f"Keywords: {len(keywords)}")
    print(f"Pages requested per keyword: {MAX_PAGES} x {PAGE_SIZE}")
    print(f"Maximum Canopy API requests this run: {estimated_requests}")

    if estimated_requests > 25:
        print("ERROR: Refusing a run with more than 25 keyword/API requests.", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    for keyword in keywords:
        print(f"Checking: {keyword}")
        try:
            row = rank_keyword(keyword)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            print(f"HTTP {exc.code}: {body}", file=sys.stderr)
            row = failure_row(keyword, f"http_error_{exc.code}")
        except CanopyGraphQLError as exc:
            print(f"GraphQL error: {exc}", file=sys.stderr)
            row = failure_row(keyword, "graphql_error")
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"Request error: {exc}", file=sys.stderr)
            row = failure_row(keyword, f"error_{type(exc).__name__}")
        rows.append(row)
        print(row)

    write_outputs(rows)
    failed = sum(row["status"].startswith(("http_error_", "graphql_error", "error_")) for row in rows)
    if failed == len(rows):
        print("ERROR: All keyword checks failed; report is diagnostic only.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
