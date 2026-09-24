#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jaytreebooks.com"
LOGO = f"{SITE}/icons/icon-512.png"

SEO = {
    "index.html": {
        "title": "JayTree Books | Mystery & Psychological Thrillers",
        "description": "Discover JayTree Books mysteries and psychological thrillers. Read first chapters, watch trailers, solve Mystery Challenges, and find Kindle Unlimited reads.",
        "video_alt": "JayTree Books Mystery Challenge video thumbnail",
    },
    "books/second-draft.html": {
        "title": "Second Draft | Psychological Mystery | JayTree Books",
        "description": "Nora helps people rehearse impossible conversations—until the rehearsals start changing reality. Read Chapter One and continue with Kindle Unlimited.",
        "video_alt": "Second Draft video preview thumbnail",
    },
    "books/the-hollow-year.html": {
        "title": "The Hollow Year | Supernatural Mystery | JayTree Books",
        "description": "In Amity Hollow, one person is erased from every living memory each October—and one woman still remembers. Read Chapter One and continue with Kindle Unlimited.",
        "video_alt": "The Hollow Year video preview thumbnail",
    },
    "books/the-hollow-bell.html": {
        "title": "The Hollow Bell | Cold-Case Mystery | JayTree Books",
        "description": "Twenty years after Marnie Renner vanished, her remains surface beneath the ice in Millbrook Falls. Read Chapter One and continue with Kindle Unlimited.",
        "video_alt": "The Hollow Bell video preview thumbnail",
    },
    "books/the-absconding.html": {
        "title": "The Absconding | Family Secrets Mystery | JayTree Books",
        "description": "After Del's mother dies beside the family beehives, the hives fall silent—and an old family ritual suggests the story she's been told is wrong. Read Chapter One and continue with Kindle Unlimited.",
        "video_alt": "The Absconding video preview thumbnail",
    },
    "books/the-correction.html": {
        "title": "The Correction | Archive Conspiracy Mystery | JayTree Books",
        "description": "A correction slip changes more than the official record—it changes what Averill Falls remembers. Read Chapter One and continue with Kindle Unlimited.",
        "video_alt": "The Correction video preview thumbnail",
    },
    "about.html": {
        "title": "About JayTree Books | Independent Mystery Publisher",
        "description": "About JayTree Books, an independent mystery publisher creating psychological thrillers, supernatural mysteries, cold cases, first-chapter previews, trailers, and Mystery Challenges.",
        "video_alt": "JayTree Books publisher artwork",
    },
    "mystery-books.html": {
        "title": "New Mystery Books & Psychological Thrillers | JayTree Books",
        "description": "Discover new mystery books from JayTree Books: psychological thrillers, supernatural mysteries, cold cases, family secrets, and Kindle Unlimited reads.",
        "video_alt": "JayTree Books mystery video thumbnail",
    },
}

JSONLD_RE = re.compile(
    r'(<script\s+type=["\']application/ld\+json["\']\s*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)
SITEMAP_PATHS = [
    ("", "index.html"),
    ("about.html", "about.html"),
    ("animated-series.html", "animated-series.html"),
    ("case-files.html", "case-files.html"),
    ("books/second-draft.html", "books/second-draft.html"),
    ("books/the-hollow-year.html", "books/the-hollow-year.html"),
    ("books/the-hollow-bell.html", "books/the-hollow-bell.html"),
    ("books/the-absconding.html", "books/the-absconding.html"),
    ("books/the-correction.html", "books/the-correction.html"),
    ("chapters/book-1-first-chapter.html", "chapters/book-1-first-chapter.html"),
    ("chapters/book-2-first-chapter.html", "chapters/book-2-first-chapter.html"),
    ("chapters/book-3-first-chapter.html", "chapters/book-3-first-chapter.html"),
    ("chapters/book-4-first-chapter.html", "chapters/book-4-first-chapter.html"),
    ("chapters/book-5-first-chapter.html", "chapters/book-5-first-chapter.html"),
    ("mystery-books.html", "mystery-books.html"),
    ("psychological-mystery-books.html", "psychological-mystery-books.html"),
    ("kindle-unlimited-mystery-books.html", "kindle-unlimited-mystery-books.html"),
    ("supernatural-mystery-books.html", "supernatural-mystery-books.html"),
    ("small-town-mystery-books.html", "small-town-mystery-books.html"),
    ("cold-case-mystery-books.html", "cold-case-mystery-books.html"),
]

YT_EMPTY_ALT_RE = re.compile(
    r'(<img\s+src="https://i\.ytimg\.com/vi/[^\"]+/hqdefault\.jpg")\s+alt=""',
    re.IGNORECASE,
)


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.relative_to(ROOT)}")
    return True


def add_org_logo(value):
    if isinstance(value, dict):
        if value.get("@type") == "Organization" and value.get("name") == "JayTree Books":
            value["@id"] = f"{SITE}/#publisher"
            value["url"] = SITE
            logo = value.get("logo")
            if not logo:
                value["logo"] = {"@type": "ImageObject", "url": LOGO}
            elif isinstance(logo, str):
                value["logo"] = {"@type": "ImageObject", "url": logo}
            same_as = value.get("sameAs")
            if isinstance(same_as, list):
                value["sameAs"] = list(dict.fromkeys(same_as))
        for child in value.values():
            add_org_logo(child)
    elif isinstance(value, list):
        for child in value:
            add_org_logo(child)


def patch_jsonld(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        add_org_logo(data)
        return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    return JSONLD_RE.sub(repl, text)


def patch_page(rel: str, spec: dict[str, str]) -> None:
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")

    text = re.sub(r'<title>.*?</title>', f'<title>{spec["title"]}</title>', text, count=1, flags=re.DOTALL)
    text = re.sub(
        r'<meta\s+name="description"\s+content="[^"]*">',
        f'<meta name="description" content="{spec["description"]}">',
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    # Keep social titles/descriptions aligned with the cleaned search metadata.
    text = re.sub(
        r'<meta\s+property="og:title"\s+content="[^"]*">',
        f'<meta property="og:title" content="{spec["title"]}">',
        text,
        count=1,
        flags=re.IGNORECASE,
    )
    text = re.sub(
        r'<meta\s+name="twitter:title"\s+content="[^"]*">',
        f'<meta name="twitter:title" content="{spec["title"]}">',
        text,
        count=1,
        flags=re.IGNORECASE,
    )

    text = patch_jsonld(text)
    text = YT_EMPTY_ALT_RE.sub(rf'\1 alt="{spec["video_alt"]}"', text)

    if '<link rel="icon"' not in text:
        canonical = re.search(r'<link\s+rel="canonical"\s+href="[^"]+">', text, flags=re.IGNORECASE)
        if canonical:
            text = text[:canonical.end()] + '\n<link rel="icon" type="image/png" sizes="192x192" href="/favicon.png">' + text[canonical.end():]

    write_if_changed(path, text)


def patch_all_html_schema_and_video_alt() -> None:
    for path in ROOT.rglob("*.html"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        updated = patch_jsonld(text)
        updated = YT_EMPTY_ALT_RE.sub(r'\1 alt="Video preview thumbnail"', updated)
        write_if_changed(path, updated)


def patch_durable_sources() -> None:
    # Workflow definitions are deliberately out of scope. This cleanup may update
    # source generators under scripts/, but it must never edit .github/workflows/.
    base = ROOT / "scripts"
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".yml", ".yaml"}:
            continue
        if path.name == "seo_content_cleanup.py":
            continue
        text = path.read_text(encoding="utf-8")
        text = text.replace("https://www.JayTreeBooks.com", SITE)
        text = text.replace(
            "JayTree Books | Mystery Thrillers, Kindle Unlimited & Mystery Challenges",
            SEO["index.html"]["title"],
        )
        write_if_changed(path, text)

    builder = ROOT / "scripts" / "build_reader_growth_site.py"
    text = builder.read_text(encoding="utf-8")
    text = text.replace(
        '            "url": SITE,\n        },\n        "offers": {',
        '            "url": SITE,\n            "logo": f"{SITE}/icons/icon-512.png",\n        },\n        "offers": {',
    )
    text = text.replace(
        '        "url": SITE,\n        "sameAs": same_as,',
        '        "url": SITE,\n        "logo": f"{SITE}/icons/icon-512.png",\n        "sameAs": list(dict.fromkeys(same_as)),',
    )
    write_if_changed(builder, text)

    improvements = ROOT / "scripts" / "apply_site_improvements.py"
    text = improvements.read_text(encoding="utf-8")
    text = text.replace(
        'f\'<img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">\'',
        'f\'<img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="{safe} thumbnail" loading="lazy" decoding="async">\'',
    )
    text = text.replace(
        '<img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">',
        '<img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="${safeTitle} thumbnail" loading="lazy" decoding="async">',
    )
    write_if_changed(improvements, text)

    app = ROOT / "app.js"
    if app.exists():
        text = app.read_text(encoding="utf-8")
        text = text.replace(
            '<img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">',
            '<img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="${safeTitle} thumbnail" loading="lazy" decoding="async">',
        )
        write_if_changed(app, text)



def _git_output(*args: str) -> str:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=True,
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return ""


def _lastmod(rel: str) -> str:
    # If the cleanup itself changed the file, today's date is the accurate
    # last-modified date for the commit this workflow is about to create.
    if _git_output("status", "--porcelain", "--", rel):
        return date.today().isoformat()
    committed = _git_output("log", "-1", "--format=%cs", "--", rel)
    return committed or date.today().isoformat()


def refresh_sitemap() -> None:
    rows = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url_path, file_path in SITEMAP_PATHS:
        loc = f"{SITE}/" + url_path
        rows.append(f"  <url><loc>{loc}</loc><lastmod>{_lastmod(file_path)}</lastmod></url>")
    rows.append("</urlset>")
    rows.append("")
    write_if_changed(ROOT / "sitemap.xml", "\n".join(rows))

def validate() -> None:
    problems: list[str] = []

    for rel, spec in SEO.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        title = re.search(r'<title>(.*?)</title>', text, flags=re.DOTALL)
        desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)">', text, flags=re.IGNORECASE)
        canonical = re.search(r'<link\s+rel="canonical"\s+href="([^"]+)">', text, flags=re.IGNORECASE)
        if not title or title.group(1) != spec["title"]:
            problems.append(f"{rel}: title mismatch")
        elif len(title.group(1)) > 60:
            problems.append(f"{rel}: title too long ({len(title.group(1))})")
        if not desc or desc.group(1) != spec["description"]:
            problems.append(f"{rel}: meta description mismatch")
        elif len(desc.group(1)) > 160:
            problems.append(f"{rel}: meta description too long ({len(desc.group(1))})")
        if not canonical or not canonical.group(1).startswith(SITE):
            problems.append(f"{rel}: canonical is not on {SITE}")
        if YT_EMPTY_ALT_RE.search(text):
            problems.append(f"{rel}: YouTube thumbnail still has empty alt")
        if '"@type":"Organization"' in text and LOGO not in text:
            problems.append(f"{rel}: Organization schema logo missing")

    sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    if "https://www.JayTreeBooks.com" in sitemap:
        problems.append("sitemap.xml: WWW host remains")
    if sitemap.count("<url>") != len(SITEMAP_PATHS):
        problems.append(
            f"sitemap.xml: expected {len(SITEMAP_PATHS)} URLs, found {sitemap.count('<url>')}"
        )
    if sitemap.count("<lastmod>") != sitemap.count("<url>"):
        problems.append("sitemap.xml: every URL must have lastmod")
    if f"{SITE}/about.html" not in sitemap:
        problems.append("sitemap.xml: about.html missing")

    # Durable SEO-source checks are limited to scripts/. Workflow definitions are
    # intentionally read-only for this job and are guarded separately by Actions.
    base = ROOT / "scripts"
    for path in base.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".py", ".yml", ".yaml"}:
            continue
        if path.name == "seo_content_cleanup.py":
            continue
        if "https://www.JayTreeBooks.com" in path.read_text(encoding="utf-8"):
            problems.append(f"{path.relative_to(ROOT)}: legacy WWW host remains")

    builder = (ROOT / "scripts" / "build_reader_growth_site.py").read_text(encoding="utf-8")
    if builder.count('"logo": f"{SITE}/icons/icon-512.png"') < 2:
        problems.append("build_reader_growth_site.py: durable Organization logos not installed")

    if problems:
        raise SystemExit("SEO validation failed:\n- " + "\n- ".join(problems))
    print("SEO cleanup validation passed.")


def main() -> int:
    patch_durable_sources()
    patch_all_html_schema_and_video_alt()
    for rel, spec in SEO.items():
        patch_page(rel, spec)
    refresh_sitemap()
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
