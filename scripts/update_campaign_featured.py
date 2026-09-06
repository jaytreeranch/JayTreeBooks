#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import date, datetime, timedelta
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_PATH = ROOT / "data" / "campaign.json"
CONFIG_PATH = ROOT / "config.js"
INDEX_PATH = ROOT / "index.html"

CONFIG_RE = re.compile(
    r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;",
    re.DOTALL,
)


def load_config() -> dict:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    match = CONFIG_RE.search(text)
    if not match:
        raise RuntimeError("Could not parse window.JT from config.js")
    return json.loads(match.group(1))


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(
        "window.JT = " + json.dumps(config, indent=2, ensure_ascii=False) + ";\n"
        "window.JAYTREE_CONFIG = window.JT;\n",
        encoding="utf-8",
    )


def monday(day: date) -> date:
    return day - timedelta(days=day.weekday())


def featured_slug(campaign: dict, reference_day: date) -> str:
    rotation = campaign.get("rotation") or []
    if not rotation:
        raise RuntimeError("Campaign rotation is empty")
    anchor = date.fromisoformat(str(campaign["rotation_anchor"]))
    weeks = (monday(reference_day) - monday(anchor)).days // 7
    return str(rotation[weeks % len(rotation)])


def patch_hero(index: str, book: dict) -> str:
    hero = re.search(r'<div class="hero-feature">.*?</div>', index, flags=re.DOTALL)
    if not hero:
        raise RuntimeError("Homepage hero feature block was not found")

    block = hero.group(0)
    image = re.search(r'<img\b[^>]*>', block)
    if image:
        tag = image.group(0)
        tag = re.sub(
            r'\bsrc="[^"]*"',
            f'src="{escape(str(book["cover"]), quote=True)}"',
            tag,
            count=1,
        )
        if re.search(r'\balt="[^"]*"', tag):
            tag = re.sub(
                r'\balt="[^"]*"',
                f'alt="{escape(str(book["title"]) + " book cover", quote=True)}"',
                tag,
                count=1,
            )
        block = block[: image.start()] + tag + block[image.end() :]

    block = re.sub(
        r'(<strong>).*?(</strong>)',
        lambda m: m.group(1) + escape(str(book["title"])) + m.group(2),
        block,
        count=1,
        flags=re.DOTALL,
    )
    block = re.sub(
        r'(<small>).*?(</small>)',
        lambda m: m.group(1) + escape(str(book["description"])) + m.group(2),
        block,
        count=1,
        flags=re.DOTALL,
    )
    return index[: hero.start()] + block + index[hero.end() :]


def main() -> int:
    campaign = json.loads(CAMPAIGN_PATH.read_text(encoding="utf-8"))
    tz = ZoneInfo(str(campaign.get("timezone") or "America/Chicago"))

    import argparse
    parser = argparse.ArgumentParser(description="Update only the weekly featured-book fallback")
    parser.add_argument("--date", help="America/Chicago date in YYYY-MM-DD")
    args = parser.parse_args()

    reference_day = date.fromisoformat(args.date) if args.date else datetime.now(tz).date()
    slug = featured_slug(campaign, reference_day)

    config = load_config()
    book = next((b for b in config.get("books", []) if b.get("slug") == slug), None)
    if not book:
        raise RuntimeError(f"Featured book {slug!r} is not present in config.js")

    config["featuredBook"] = slug
    save_config(config)

    index = INDEX_PATH.read_text(encoding="utf-8")
    index = patch_hero(index, book)
    INDEX_PATH.write_text(index, encoding="utf-8")

    print(f"Featured fallback updated for week of {monday(reference_day).isoformat()}: {book['title']}")
    print("Homepage SEO title and social metadata were intentionally left publisher-focused.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
