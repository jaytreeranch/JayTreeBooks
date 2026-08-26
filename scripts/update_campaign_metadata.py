#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
from datetime import date, datetime, timedelta
from pathlib import Path
from urllib.parse import urljoin
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
CAMPAIGN_PATH = ROOT / "data" / "campaign.json"
CONFIG_PATH = ROOT / "config.js"
INDEX_PATH = ROOT / "index.html"
SITE_URL = "https://www.JayTreeBooks.com/"


def _load_campaign() -> dict:
    return json.loads(CAMPAIGN_PATH.read_text(encoding="utf-8"))


def _load_site_config() -> dict:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    prefix = "window.JT = "
    suffix = ";\nwindow.JAYTREE_CONFIG"
    start = text.find(prefix)
    end = text.find(suffix)
    if start < 0 or end < 0:
        raise SystemExit("Could not parse config.js window.JT payload.")
    payload = text[start + len(prefix):end]
    return json.loads(payload)


def _monday(day: date) -> date:
    return day - timedelta(days=day.weekday())


def _featured_slug(campaign: dict, reference_day: date) -> str:
    rotation = campaign.get("rotation") or []
    if not rotation:
        raise SystemExit("data/campaign.json has an empty rotation.")
    anchor = date.fromisoformat(str(campaign["rotation_anchor"]))
    weeks = (_monday(reference_day) - _monday(anchor)).days // 7
    return str(rotation[weeks % len(rotation)])


def _replace_or_insert_meta(text: str, *, attr: str, key: str, content: str) -> str:
    escaped = html.escape(content, quote=True)
    pattern = re.compile(
        rf'<meta\s+{re.escape(attr)}="{re.escape(key)}"\s+content="[^"]*"\s*/?>',
        re.IGNORECASE,
    )
    tag = f'<meta {attr}="{key}" content="{escaped}">'
    if pattern.search(text):
        return pattern.sub(tag, text, count=1)
    marker = '<meta name="referrer" content="strict-origin-when-cross-origin">'
    if marker in text:
        return text.replace(marker, marker + "\n" + tag, 1)
    return text.replace("<head>", "<head>\n" + tag, 1)


def _replace_title(text: str, title: str) -> str:
    escaped = html.escape(title, quote=False)
    return re.sub(r"<title>.*?</title>", f"<title>{escaped}</title>", text, count=1, flags=re.I | re.S)


def _replace_hero_fallback(text: str, book: dict) -> str:
    title = str(book["title"])
    description = str(book["description"])
    cover = str(book["cover"])
    text = re.sub(
        r'(<div class="hero-feature">\s*<img\s+src=")[^"]+("\s+alt=")[^"]+("\s*>)',
        lambda m: f'{m.group(1)}{html.escape(cover, quote=True)}{m.group(2)}{html.escape(title + " book cover", quote=True)}{m.group(3)}',
        text,
        count=1,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'(<div class="hero-feature">.*?<span>).*?(</span>)',
        lambda m: m.group(1) + "THIS WEEK'S FEATURED MYSTERY" + m.group(2),
        text,
        count=1,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'(<div class="hero-feature">.*?<strong>).*?(</strong>)',
        lambda m: m.group(1) + html.escape(title) + m.group(2),
        text,
        count=1,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'(<div class="hero-feature">.*?<small>).*?(</small>)',
        lambda m: m.group(1) + html.escape(description) + m.group(2),
        text,
        count=1,
        flags=re.I | re.S,
    )
    return text


def _update_featured_fallback(slug: str) -> bool:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    updated = re.sub(
        r'("featuredBook"\s*:\s*")[^"]+("")?',
        lambda m: f'{m.group(1)}{slug}"',
        text,
        count=1,
    )
    if updated == text:
        # Safer explicit fallback for the exact JSON property shape.
        updated = re.sub(
            r'("featuredBook"\s*:\s*")[^"]+("\s*,)',
            lambda m: f'{m.group(1)}{slug}{m.group(2)}',
            text,
            count=1,
        )
    if updated == text:
        raise SystemExit("Could not update featuredBook fallback in config.js.")
    CONFIG_PATH.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize homepage SEO/share metadata to the weekly featured book")
    parser.add_argument("--date", help="America/Chicago date in YYYY-MM-DD; defaults to today")
    args = parser.parse_args()

    campaign = _load_campaign()
    tz_name = str(campaign.get("timezone") or "America/Chicago")
    tz = ZoneInfo(tz_name)
    reference_day = date.fromisoformat(args.date) if args.date else datetime.now(tz).date()
    slug = _featured_slug(campaign, reference_day)

    site_config = _load_site_config()
    book = next((item for item in site_config.get("books", []) if item.get("slug") == slug), None)
    if not book:
        raise SystemExit(f"Featured slug {slug!r} is missing from config.js.")

    title = str(book["title"])
    description = str(book["description"])
    share_title = f"{title} — Read FREE with Kindle Unlimited | JayTree Books"
    share_description = (
        f"{description} Read FREE with Kindle Unlimited. "
        "Read Chapter One and watch the official trailer at JayTreeBooks.com."
    )
    share_image = urljoin(SITE_URL, str(book["cover"]))

    index = INDEX_PATH.read_text(encoding="utf-8")
    index = _replace_title(index, share_title)
    index = _replace_or_insert_meta(index, attr="name", key="description", content=share_description)
    index = _replace_or_insert_meta(index, attr="property", key="og:title", content=share_title)
    index = _replace_or_insert_meta(index, attr="property", key="og:description", content=share_description)
    index = _replace_or_insert_meta(index, attr="property", key="og:type", content="website")
    index = _replace_or_insert_meta(index, attr="property", key="og:url", content=SITE_URL)
    index = _replace_or_insert_meta(index, attr="property", key="og:image", content=share_image)
    index = _replace_or_insert_meta(index, attr="property", key="og:image:alt", content=f"{title} book cover")
    index = _replace_or_insert_meta(index, attr="name", key="twitter:card", content="summary_large_image")
    index = _replace_or_insert_meta(index, attr="name", key="twitter:title", content=share_title)
    index = _replace_or_insert_meta(index, attr="name", key="twitter:description", content=share_description)
    index = _replace_or_insert_meta(index, attr="name", key="twitter:image", content=share_image)
    index = _replace_hero_fallback(index, book)
    INDEX_PATH.write_text(index, encoding="utf-8")

    _update_featured_fallback(slug)

    print(f"Campaign metadata synchronized for week of {_monday(reference_day).isoformat()}")
    print(f"Featured book: {title} ({slug})")
    print(f"Share title: {share_title}")
    print(f"Share image: {share_image}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
