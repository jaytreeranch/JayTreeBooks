#!/usr/bin/env python3
"""JayTree Books six-title Amazon keyword rank tracker using Canopy GraphQL.

One Canopy request is sent per keyword. Each response is scanned once for all
six JayTree Kindle ASINs, so portfolio tracking does not multiply API usage by
book count. The report also records Canopy rate-limit headers when available so
we can verify the exact credit cost of each run.
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
COUNTRY = os.environ.get("AMAZON_COUNTRY", "US").strip()
MAX_PAGES = int(os.environ.get("MAX_PAGES", "5"))
PAGE_SIZE = 40
GRAPHQL_URL = "https://graphql.canopyapi.co/"

BOOKS = [
    {"name": "The Hollow Bell — Full Novel", "asin": "B0HD52HGGZ"},
    {"name": "Second Draft", "asin": "B0HFYQ9KGV"},
    {"name": "The Hollow Year", "asin": "B0HFXF8MTP"},
    {"name": "The Absconding", "asin": "B0HDWRVSXQ"},
    {"name": "The Correction", "asin": "B0HFV8KCVL"},
    {"name": "The Hollow Bell — Novella", "asin": "B0HD2H8586"},
]
BOOK_BY_ASIN = {book["asin"].upper(): book for book in BOOKS}

# 22 phrases: broad enough to compare the catalog, but focused enough to be
# actionable for KDP metadata and Amazon Ads. One phrase = one Canopy request.
DEFAULT_KEYWORDS = [
    "small town mystery",
    "psychological mystery",
    "supernatural mystery",
    "atmospheric mystery",
    "family secrets mystery",
    "cold case mystery",
    "small town cold case mystery",
    "missing sister mystery",
    "missing person mystery",
    "police procedural mystery",
    "women sleuth mystery",
    "winter mystery",
    "memory mystery",
    "reality bending mystery",
    "supernatural disappearance mystery",
    "rural mystery",
    "homecoming mystery",
    "archive mystery",
    "conspiracy mystery",
    "altered records mystery",
    "mystery novella",
    "supernatural mystery novella",
]

# Phrases we consider strategically relevant to each book. All six ASINs are
# still checked against every phrase, so unexpected rankings are also captured.
RELEVANT_KEYWORDS = {
    "B0HD52HGGZ": {
        "small town mystery", "supernatural mystery", "atmospheric mystery",
        "cold case mystery", "small town cold case mystery", "missing sister mystery",
        "missing person mystery", "police procedural mystery", "women sleuth mystery",
        "winter mystery",
    },
    "B0HFYQ9KGV": {
        "psychological mystery", "atmospheric mystery", "memory mystery",
        "reality bending mystery",
    },
    "B0HFXF8MTP": {
        "small town mystery", "psychological mystery", "supernatural mystery",
        "atmospheric mystery", "memory mystery", "reality bending mystery",
        "supernatural disappearance mystery",
    },
    "B0HDWRVSXQ": {
        "psychological mystery", "atmospheric mystery", "family secrets mystery",
        "rural mystery", "homecoming mystery",
    },
    "B0HFV8KCVL": {
        "small town mystery", "psychological mystery", "atmospheric mystery",
        "archive mystery", "conspiracy mystery", "altered records mystery",
    },
    "B0HD2H8586": {
        "small town mystery", "supernatural mystery", "atmospheric mystery",
        "mystery novella", "supernatural mystery novella",
    },
}

REQUEST_COUNT = 0
RATE_LIMIT_REMAINING: list[int] = []
RATE_LIMIT_LIMIT: list[int] = []


class CanopyGraphQLError(RuntimeError):
    pass


def _header_int(headers: Any, name: str) -> int | None:
    value = headers.get(name)
    if value is None:
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


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
    return f'''query PortfolioKeywordRank($input: AmazonProductSearchResultsInput!) {{
      amazonProductSearchResults(input: $input) {{
        {pages}
      }}
    }}'''


def canopy_search(keyword: str) -> dict[str, Any]:
    global REQUEST_COUNT
    payload = {
        "query": build_query(),
        "variables": {"input": {"searchTerm": keyword, "domain": COUNTRY}},
    }
    req = Request(
        GRAPHQL_URL,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "API-KEY": API_KEY,
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": "JayTreeBooks-AmazonPortfolioRankTracker/3.0",
        },
    )
    REQUEST_COUNT += 1
    with urlopen(req, timeout=90) as resp:
        remaining = _header_int(resp.headers, "X-RateLimit-Remaining")
        limit = _header_int(resp.headers, "X-RateLimit-Limit")
        if remaining is not None:
            RATE_LIMIT_REMAINING.append(remaining)
        if limit is not None:
            RATE_LIMIT_LIMIT.append(limit)
        data = json.loads(resp.read().decode("utf-8"))
    if data.get("errors"):
        msg = "; ".join(str(e.get("message", e)) for e in data["errors"][:3])
        raise CanopyGraphQLError(msg)
    return data


def scan_keyword(keyword: str) -> list[dict[str, Any]]:
    payload = canopy_search(keyword)
    search = payload.get("data", {}).get("amazonProductSearchResults")
    if not isinstance(search, dict):
        raise CanopyGraphQLError("Missing data.amazonProductSearchResults")

    found: dict[str, dict[str, Any]] = {}
    sponsored_seen = {asin: False for asin in BOOK_BY_ASIN}
    organic_seen = 0
    pages_scanned = 0

    for page in range(1, MAX_PAGES + 1):
        block = search.get(f"page{page}")
        if not isinstance(block, dict):
            break
        results = block.get("results") or []
        if not isinstance(results, list) or not results:
            break
        pages_scanned += 1

        for item in results:
            if not isinstance(item, dict):
                continue
            asin = str(item.get("asin") or "").strip().upper()
            sponsored = bool(item.get("sponsored", False))
            if sponsored:
                if asin in sponsored_seen:
                    sponsored_seen[asin] = True
                continue

            organic_seen += 1
            if asin in BOOK_BY_ASIN and asin not in found:
                found[asin] = {
                    "organic_rank": organic_seen,
                    "page": page,
                }

        page_info = block.get("pageInfo") or {}
        if isinstance(page_info, dict) and page_info.get("hasNextPage") is False:
            break

    rows = []
    for book in BOOKS:
        asin = book["asin"].upper()
        hit = found.get(asin)
        rows.append({
            "book": book["name"],
            "asin": asin,
            "keyword": keyword,
            "relevant": keyword in RELEVANT_KEYWORDS.get(asin, set()),
            "found": hit is not None,
            "organic_rank": hit["organic_rank"] if hit else None,
            "page": hit["page"] if hit else None,
            "sponsored_seen": sponsored_seen[asin],
            "results_scanned": organic_seen,
            "status": "found" if hit else f"not_found_after_{pages_scanned}_pages_{organic_seen}_organic_results",
        })
    return rows


def failure_rows(keyword: str, status: str) -> list[dict[str, Any]]:
    return [{
        "book": book["name"],
        "asin": book["asin"],
        "keyword": keyword,
        "relevant": keyword in RELEVANT_KEYWORDS.get(book["asin"], set()),
        "found": False,
        "organic_rank": None,
        "page": None,
        "sponsored_seen": False,
        "results_scanned": 0,
        "status": status,
    } for book in BOOKS]


def usage_summary() -> dict[str, Any]:
    # Canopy documents each API call as one request/credit. Where the API
    # returns X-RateLimit-Remaining, use the header delta as an independent
    # cross-check of the run's exact cost.
    header_start = RATE_LIMIT_REMAINING[0] + 1 if RATE_LIMIT_REMAINING else None
    header_end = RATE_LIMIT_REMAINING[-1] if RATE_LIMIT_REMAINING else None
    header_used = (header_start - header_end) if header_start is not None and header_end is not None else None
    return {
        "requests_sent": REQUEST_COUNT,
        "header_limit": RATE_LIMIT_LIMIT[-1] if RATE_LIMIT_LIMIT else None,
        "header_start": header_start,
        "header_end": header_end,
        "header_used": header_used,
    }


def write_outputs(rows: list[dict[str, Any]], keywords: list[str]) -> None:
    out_dir = Path("reports/amazon-rank")
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now = datetime.now(timezone.utc).isoformat()
    usage = usage_summary()

    csv_path = out_dir / f"amazon-portfolio-rank-{stamp}.csv"
    fields = [
        "book", "asin", "keyword", "relevant", "found", "organic_rank", "page",
        "sponsored_seen", "results_scanned", "status",
    ]
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    md_path = out_dir / "latest.md"
    lines = [
        "# JayTree Books Amazon Search Portfolio Baseline",
        "",
        f"- Marketplace: `{COUNTRY}`",
        "- API: `Canopy GraphQL`",
        f"- Checked: `{now}`",
        f"- Books checked: `{len(BOOKS)}`",
        f"- Unique keywords checked: `{len(keywords)}`",
        f"- Maximum pages requested per keyword: `{MAX_PAGES}`",
        f"- Page size requested: `{PAGE_SIZE}`",
        f"- Canopy API requests sent this run: `{usage['requests_sent']}`",
    ]
    if usage["header_end"] is not None:
        lines.append(f"- Canopy credits remaining after run: `{usage['header_end']}`")
    if usage["header_used"] is not None:
        lines.append(f"- Canopy credits consumed this run (rate-limit header delta): `{usage['header_used']}`")
    lines.extend(["", "## Portfolio summary", "", "| Book | ASIN | Best Organic Rank Found | Best Keyword | Relevant Phrases Found |", "|---|---|---:|---|---:|"])

    for book in BOOKS:
        book_rows = [r for r in rows if r["asin"] == book["asin"] and r["status"] == "found"]
        relevant_found = [r for r in book_rows if r["relevant"]]
        best = min(book_rows, key=lambda r: r["organic_rank"]) if book_rows else None
        lines.append(
            f"| {book['name']} | `{book['asin']}` | "
            f"{best['organic_rank'] if best else '—'} | {best['keyword'] if best else '—'} | {len(relevant_found)} |"
        )

    for book in BOOKS:
        asin = book["asin"]
        lines.extend(["", f"## {book['name']}", "", "| Keyword | Organic Rank | Page | Results Scanned | Sponsored | Status |", "|---|---:|---:|---:|:---:|---|"])
        book_rows = [r for r in rows if r["asin"] == asin and r["relevant"]]
        for row in book_rows:
            rank = row["organic_rank"] if row["organic_rank"] is not None else "—"
            page = row["page"] if row["page"] is not None else "—"
            lines.append(
                f"| {row['keyword']} | {rank} | {page} | {row['results_scanned']} | "
                f"{'Yes' if row['sponsored_seen'] else 'No'} | {row['status']} |"
            )

    unexpected = [r for r in rows if r["found"] and not r["relevant"]]
    lines.extend(["", "## Unexpected cross-title rankings", ""])
    if unexpected:
        lines.extend(["| Book | Keyword | Organic Rank | Page |", "|---|---|---:|---:|"])
        for row in sorted(unexpected, key=lambda r: (r["organic_rank"], r["book"])):
            lines.append(f"| {row['book']} | {row['keyword']} | {row['organic_rank']} | {row['page']} |")
    else:
        lines.append("None found in this baseline.")

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    usage_path = out_dir / "usage-latest.json"
    usage_path.write_text(json.dumps({"checked": now, "keywords": len(keywords), **usage}, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    if not API_KEY:
        print("ERROR: CANOPY_API_KEY is not set", file=sys.stderr)
        return 2
    if MAX_PAGES < 1 or MAX_PAGES > 5:
        print("ERROR: MAX_PAGES must be between 1 and 5", file=sys.stderr)
        return 2

    keywords_env = os.environ.get("KEYWORDS", "").strip()
    keywords = [k.strip() for k in keywords_env.split("|") if k.strip()] if keywords_env else DEFAULT_KEYWORDS

    print(f"JayTree titles: {len(BOOKS)}")
    print(f"Marketplace: {COUNTRY}")
    print(f"Unique keywords: {len(keywords)}")
    print(f"Pages requested per keyword: {MAX_PAGES} x {PAGE_SIZE}")
    print(f"Maximum Canopy API requests this run: {len(keywords)}")

    if len(keywords) > 25:
        print("ERROR: Refusing a run with more than 25 keyword/API requests.", file=sys.stderr)
        return 2

    rows: list[dict[str, Any]] = []
    failed_keywords = 0
    for keyword in keywords:
        print(f"Checking portfolio keyword: {keyword}")
        try:
            keyword_rows = scan_keyword(keyword)
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")[:500]
            print(f"HTTP {exc.code}: {body}", file=sys.stderr)
            keyword_rows = failure_rows(keyword, f"http_error_{exc.code}")
            failed_keywords += 1
        except CanopyGraphQLError as exc:
            print(f"GraphQL error: {exc}", file=sys.stderr)
            keyword_rows = failure_rows(keyword, "graphql_error")
            failed_keywords += 1
        except (URLError, TimeoutError, json.JSONDecodeError) as exc:
            print(f"Request error: {exc}", file=sys.stderr)
            keyword_rows = failure_rows(keyword, f"error_{type(exc).__name__}")
            failed_keywords += 1
        rows.extend(keyword_rows)

        hits = [r for r in keyword_rows if r["found"]]
        if hits:
            print("  Found: " + ", ".join(f"{r['book']} #{r['organic_rank']}" for r in hits))
        else:
            scanned = max((r["results_scanned"] for r in keyword_rows), default=0)
            print(f"  No JayTree ASIN found; organic results scanned: {scanned}")

    usage = usage_summary()
    print(f"Canopy API requests sent: {usage['requests_sent']}")
    if usage["header_end"] is not None:
        print(f"Canopy credits remaining after run: {usage['header_end']}")
    if usage["header_used"] is not None:
        print(f"Canopy credits consumed this run by header delta: {usage['header_used']}")

    write_outputs(rows, keywords)
    if failed_keywords == len(keywords):
        print("ERROR: All keyword checks failed; report is diagnostic only.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
