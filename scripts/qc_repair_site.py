#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
INDEX_PATH = ROOT / "index.html"
APP_PATH = ROOT / "app.js"
SITEMAP_PATH = ROOT / "sitemap.xml"
SITE = "https://www.JayTreeBooks.com"

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


def youtube_id(value: str) -> str:
    value = str(value or "").strip()
    if not value:
        return ""
    parsed = urlparse(value)
    if "youtu.be" in parsed.netloc.lower():
        return parsed.path.strip("/").split("/")[0]
    if "youtube.com" in parsed.netloc.lower():
        if parsed.path.startswith("/watch"):
            return (parse_qs(parsed.query).get("v") or [""])[0]
        parts = [part for part in parsed.path.split("/") if part]
        for marker in ("shorts", "embed"):
            if marker in parts:
                i = parts.index(marker)
                if i + 1 < len(parts):
                    return parts[i + 1]
    return ""


def patch_app(config: dict) -> None:
    text = APP_PATH.read_text(encoding="utf-8")
    original = text

    text = text.replace(
        "8-Episode Mini-Series • Coming Soon",
        "8-Episode Mini-Series • Official Trailer Live",
    )
    text = text.replace(
        "Production is underway now, with sneak peeks and a 2+ minute cinematic trailer on the way.",
        "Production is underway now, and the official cinematic trailer is live.",
    )
    text = text.replace(
        '''<a class="cta solid" href="animated-series.html" data-track="animated_series_home">Explore the Mini-Series</a>
            <a class="cta" href="https://www.youtube.com/@JayTreeBooks" target="_blank" rel="noopener" data-track="animated_series_youtube">Follow on YouTube</a>''',
        '''<a class="cta solid" href="animated-series.html#trailer" data-track="animated_series_trailer">Watch Official Trailer</a>
            <a class="cta" href="animated-series.html" data-track="animated_series_home">Explore the Mini-Series</a>''',
    )
    text = text.replace(
        "The official cinematic trailer will be embedded on JayTreeBooks.com after its YouTube premiere.",
        "The official cinematic trailer is live now on JayTreeBooks.com.",
    )

    if text != original:
        APP_PATH.write_text(text, encoding="utf-8")
        print("QC: updated homepage mini-series messaging in app.js")


def patch_index(config: dict) -> None:
    text = INDEX_PATH.read_text(encoding="utf-8")
    original = text

    nav_match = re.search(r'<nav class="nav-links">.*?</nav>', text, flags=re.DOTALL)
    if nav_match and 'href="#animated-series"' not in nav_match.group(0):
        nav = nav_match.group(0).replace(
            '<a href="#books">Books</a>',
            '<a href="#books">Books</a>\n                <a href="#animated-series">Mini-Series</a>',
            1,
        )
        text = text[: nav_match.start()] + nav + text[nav_match.end() :]

    featured_slug = str(config.get("featuredBook") or "")
    featured = next((b for b in config.get("books", []) if b.get("slug") == featured_slug), None)
    if featured:
        hero = re.search(r'(<div class="hero-feature">\s*)(<img\b[^>]*>)(.*?</div>)', text, flags=re.DOTALL)
        if hero:
            tag = hero.group(2)
            tag = re.sub(
                r'\bsrc="[^"]*"',
                f'src="{escape(str(featured["cover"]), quote=True)}"',
                tag,
                count=1,
            )
            if re.search(r'\balt="[^"]*"', tag):
                tag = re.sub(
                    r'\balt="[^"]*"',
                    f'alt="{escape(str(featured["title"]) + " book cover", quote=True)}"',
                    tag,
                    count=1,
                )
            text = text[: hero.start(2)] + tag + text[hero.end(2) :]

            hero_block = re.search(r'<div class="hero-feature">.*?</div>', text, flags=re.DOTALL)
            if hero_block:
                block = hero_block.group(0)
                block = re.sub(
                    r'(<strong>).*?(</strong>)',
                    lambda m: m.group(1) + escape(str(featured["title"])) + m.group(2),
                    block,
                    count=1,
                    flags=re.DOTALL,
                )
                block = re.sub(
                    r'(<small>).*?(</small>)',
                    lambda m: m.group(1) + escape(str(featured["description"])) + m.group(2),
                    block,
                    count=1,
                    flags=re.DOTALL,
                )
                text = text[: hero_block.start()] + block + text[hero_block.end() :]

    if text != original:
        INDEX_PATH.write_text(text, encoding="utf-8")
        print("QC: normalized homepage navigation and featured fallback")


def patch_book_pages(config: dict) -> None:
    for book in config.get("books", []):
        path = ROOT / "books" / f'{book["slug"]}.html'
        text = path.read_text(encoding="utf-8")
        original = text

        nav_match = re.search(r'<nav class="nav-links">.*?</nav>', text, flags=re.DOTALL)
        if nav_match and '../animated-series.html' not in nav_match.group(0):
            nav = nav_match.group(0).replace(
                '<a href="../index.html#books">Books</a>',
                '<a href="../index.html#books">Books</a><a href="../animated-series.html">Mini-Series</a>',
                1,
            )
            text = text[: nav_match.start()] + nav + text[nav_match.end() :]

        if book.get("slug") == "the-hollow-bell" and "JAYTREE_HOLLOW_BELL_SERIES_PROMO_START" not in text:
            promo = '''<!-- JAYTREE_HOLLOW_BELL_SERIES_PROMO_START -->
<section class="book-section" id="animated-mini-series">
  <div class="eyebrow">Animated Mini-Series</div>
  <h2>The Hollow Bell is coming to life.</h2>
  <p class="section-copy">The novel is being adapted into an 8-episode animated mystery mini-series. Watch the official cinematic trailer and follow production from Millbrook Falls.</p>
  <div class="hero-actions">
    <a class="cta solid" href="../animated-series.html#trailer" data-track="animated_series_trailer">Watch the Animated Trailer</a>
    <a class="cta" href="../animated-series.html" data-track="animated_series_page">Explore the Mini-Series</a>
  </div>
</section>
<!-- JAYTREE_HOLLOW_BELL_SERIES_PROMO_END -->
'''
            hero = re.search(r'<section class="book-hero seo-book-hero">.*?</section>', text, flags=re.DOTALL)
            if hero:
                text = text[: hero.end()] + "\n" + promo + text[hero.end() :]

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"QC: repaired {path.relative_to(ROOT)}")


def patch_chapters(config: dict) -> None:
    for book in config.get("books", []):
        path = ROOT / str(book["chapter"])
        text = path.read_text(encoding="utf-8")
        original = text

        title = str(book["title"])
        text = re.sub(
            r"<title>.*?</title>",
            f"<title>{escape(title)} — First Chapter | JayTree Books</title>",
            text,
            count=1,
            flags=re.DOTALL,
        )

        marker = '<div class="note">'
        if marker in text:
            head, tail = text.split(marker, 1)
            tail = re.sub(r"<h1(\b[^>]*)>", r"<h2\1>", tail)
            tail = tail.replace("</h1>", "</h2>")
            text = head + marker + tail

        if text != original:
            path.write_text(text, encoding="utf-8")
            print(f"QC: normalized chapter semantics for {path.relative_to(ROOT)}")


def write_sitemap(config: dict) -> None:
    urls = [
        f"{SITE}/",
        f"{SITE}/animated-series.html",
        f"{SITE}/case-files.html",
    ]
    urls.extend(f'{SITE}/books/{b["slug"]}.html' for b in config.get("books", []))
    urls.extend(f'{SITE}/{b["chapter"]}' for b in config.get("books", []))
    entries = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{entries}\n"
        "</urlset>\n"
    )
    SITEMAP_PATH.write_text(sitemap, encoding="utf-8")
    print(f"QC: sitemap contains {len(urls)} public URLs")


def validate(config: dict) -> None:
    index = INDEX_PATH.read_text(encoding="utf-8")
    assert 'href="#animated-series">Mini-Series</a>' in index
    app = APP_PATH.read_text(encoding="utf-8")
    assert "cinematic trailer on the way" not in app
    assert "will be embedded on JayTreeBooks.com after its YouTube premiere" not in app

    expected = {
        "the-hollow-bell": "VRp1zXJ6ja4",
        "the-correction": "tRlHA4UKNGk",
    }
    for slug, video_id in expected.items():
        book = next(b for b in config["books"] if b["slug"] == slug)
        assert youtube_id(book["trailerUrl"]) == video_id, (slug, book["trailerUrl"])
        page = (ROOT / "books" / f"{slug}.html").read_text(encoding="utf-8")
        assert video_id in page, (slug, video_id)
        assert '../animated-series.html' in page

    hollow = (ROOT / "books" / "the-hollow-bell.html").read_text(encoding="utf-8")
    assert "JAYTREE_HOLLOW_BELL_SERIES_PROMO_START" in hollow
    assert "../animated-series.html#trailer" in hollow

    for book in config["books"]:
        chapter = (ROOT / book["chapter"]).read_text(encoding="utf-8")
        assert f'{book["title"]} — First Chapter | JayTree Books' in chapter
        after_note = chapter.split('<div class="note">', 1)[-1]
        assert "<h1" not in after_note

    sitemap = SITEMAP_PATH.read_text(encoding="utf-8")
    assert f"{SITE}/animated-series.html" in sitemap
    assert f"{SITE}/case-files.html" in sitemap
    assert sitemap.count("<url>") == 13
    print("QC repair validation passed.")


def validate_static_pages(config: dict) -> None:
    animated = (ROOT / "animated-series.html").read_text(encoding="utf-8")
    assert animated.count('<link rel="manifest" href="/manifest.webmanifest">') == 1
    assert animated.count('<script src="/pwa.js" defer></script>') == 1
    assert 'data-youtube-id="PmGQoyjYTDs"' in animated
    assert '<link rel="canonical" href="https://www.JayTreeBooks.com/animated-series.html">' in animated

    for book in config["books"]:
        audio = (ROOT / book["audio"]).read_text(encoding="utf-8")
        assert "Jaytree Books" not in audio
        assert f'{SITE}/{book["audio"]}' in audio
        assert f'../books/{book["slug"]}.html' in audio
        assert f'../{book["chapter"]}' in audio
        assert book["amazonUrl"] in audio
        assert f'../{book["cover"]}' in audio
        assert 'G-PHE2JVV5P6' in audio

    privacy = (ROOT / "privacy.html").read_text(encoding="utf-8")
    for required in ("Google Analytics", "Kit", "YouTube", "service worker", "Google API Services User Data Policy"):
        assert required in privacy, required

    terms = (ROOT / "terms.html").read_text(encoding="utf-8")
    for required in ("JayTreeBooks.com", "Kindle Unlimited", "newsletter", "JayTree Social Poster"):
        assert required in terms, required

    preview = (ROOT / "x-preview-test.html").read_text(encoding="utf-8")
    assert 'name="robots" content="noindex,nofollow"' in preview

    callback = (ROOT / "tiktok-callback.html").read_text(encoding="utf-8")
    assert 'name="referrer" content="no-referrer"' in callback
    assert 'name="robots" content="noindex,nofollow"' in callback
    print("QC static-page validation passed.")


def main() -> int:
    config = load_config()
    patch_app(config)
    patch_index(config)
    patch_book_pages(config)
    patch_chapters(config)
    write_sitemap(config)
    validate(config)
    validate_static_pages(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
