#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
APP_PATH = ROOT / "app.js"
LEGACY_BOOK_PATH = ROOT / "book.html"
BOOKS_DIR = ROOT / "books"
SITE = "https://www.JayTreeBooks.com"

CONFIG_RE = re.compile(
    r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;",
    re.DOTALL,
)


def load_config() -> dict:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    match = CONFIG_RE.search(text)
    if not match:
        raise RuntimeError("Could not parse config.js")
    return json.loads(match.group(1))


def patch_app() -> None:
    text = APP_PATH.read_text(encoding="utf-8")
    text = text.replace(
        'href="book.html?book=${b.slug}#audiobook"',
        'href="books/${b.slug}.html#listen"',
    )
    marker = 'document.querySelectorAll("[data-social]")'
    if marker not in text:
        needle = '''  document.querySelectorAll("[data-track]").forEach(el => {
    el.addEventListener("click", () => track(el.dataset.track, { book: el.dataset.book || "" }));
  });
'''
        addition = needle + '''  document.querySelectorAll("[data-social]").forEach(el => {
    el.addEventListener("click", () => track("social_visit", { platform: el.dataset.social || "" }));
  });
'''
        if needle not in text:
            raise RuntimeError("Could not find bindTracking data-track block in app.js")
        text = text.replace(needle, addition, 1)
    APP_PATH.write_text(text, encoding="utf-8")


def patch_legacy_book_page() -> None:
    text = LEGACY_BOOK_PATH.read_text(encoding="utf-8")
    if 'name="robots" content="noindex,follow"' not in text:
        text = text.replace(
            '<meta name="description" content="Explore a JayTree Books mystery.">',
            '<meta name="description" content="Explore a JayTree Books mystery.">\n  <meta name="robots" content="noindex,follow">',
            1,
        )
    LEGACY_BOOK_PATH.write_text(text, encoding="utf-8")


def patch_static_book_pages(config: dict) -> None:
    for book in config.get("books", []):
        path = BOOKS_DIR / f"{book['slug']}.html"
        text = path.read_text(encoding="utf-8")
        optimized = f"{SITE}/{book['cover']}"
        original_rel = book.get("coverOriginal") or book["cover"]
        social_image = f"{SITE}/{original_rel}"
        text = text.replace(
            f'<meta property="og:image" content="{optimized}">',
            f'<meta property="og:image" content="{social_image}">',
        )
        text = text.replace(
            f'<meta name="twitter:image" content="{optimized}">',
            f'<meta name="twitter:image" content="{social_image}">',
        )
        text = text.replace(
            '<section class="book-section"><div class="eyebrow">Listen</div>',
            '<section class="book-section" id="listen"><div class="eyebrow">Listen</div>',
        )
        path.write_text(text, encoding="utf-8")


def main() -> int:
    config = load_config()
    patch_app()
    patch_legacy_book_page()
    patch_static_book_pages(config)
    print("Reader-growth final polish complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
