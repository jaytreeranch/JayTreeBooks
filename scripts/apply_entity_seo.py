#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jaytreebooks.com"
PUBLISHER_ID = f"{SITE}/#publisher"
WEBSITE_ID = f"{SITE}/#website"
LOGO = f"{SITE}/icons/icon-512.png"

BOOKS = [
    {"path": "books/second-draft.html", "slug": "second-draft", "title": "Second Draft", "chapter": "chapters/book-1-first-chapter.html", "cover": "second-draft.webp"},
    {"path": "books/the-hollow-year.html", "slug": "the-hollow-year", "title": "The Hollow Year", "chapter": "chapters/book-2-first-chapter.html", "cover": "the-hollow-year.webp"},
    {"path": "books/the-hollow-bell.html", "slug": "the-hollow-bell", "title": "The Hollow Bell", "chapter": "chapters/book-3-first-chapter.html", "cover": "the-hollow-bell.webp"},
    {"path": "books/the-absconding.html", "slug": "the-absconding", "title": "The Absconding", "chapter": "chapters/book-4-first-chapter.html", "cover": "the-absconding.webp"},
    {"path": "books/the-correction.html", "slug": "the-correction", "title": "The Correction", "chapter": "chapters/book-5-first-chapter.html", "cover": "the-correction.webp"},
]

ROOT_SEO_PAGES = [
    "mystery-books.html",
    "psychological-mystery-books.html",
    "kindle-unlimited-mystery-books.html",
    "supernatural-mystery-books.html",
    "small-town-mystery-books.html",
    "cold-case-mystery-books.html",
    "case-files.html",
    "animated-series.html",
]

JSONLD_RE = re.compile(
    r'(<script\s+type=["\']application/ld\+json["\']\s*>)(.*?)(</script>)',
    re.IGNORECASE | re.DOTALL,
)

PUBLISHER = {
    "@type": "Organization",
    "@id": PUBLISHER_ID,
    "name": "JayTree Books",
    "url": SITE,
    "logo": {"@type": "ImageObject", "url": LOGO},
}


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    print(f"Updated {path.relative_to(ROOT)}")
    return True


def meta_value(text: str, name: str) -> str:
    match = re.search(
        rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)">',
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else ""


def title_value(text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, flags=re.IGNORECASE | re.DOTALL)
    return match.group(1).strip() if match else ""


def canonical_value(text: str, fallback: str) -> str:
    match = re.search(
        r'<link\s+rel="canonical"\s+href="([^"]+)">',
        text,
        flags=re.IGNORECASE,
    )
    return match.group(1) if match else fallback


def ensure_robots(text: str, video: bool = False) -> str:
    if 'name="robots"' in text:
        return text
    desc = re.search(r'<meta\s+name="description"\s+content="[^"]*">', text, re.IGNORECASE)
    if not desc:
        return text
    value = "index,follow,max-image-preview:large,max-snippet:-1"
    if video:
        value += ",max-video-preview:-1"
    return text[: desc.end()] + f'\n<meta name="robots" content="{value}">' + text[desc.end() :]


def enrich_publisher(value):
    if isinstance(value, dict):
        if value.get("@type") == "Organization" and value.get("name") == "JayTree Books":
            value["@id"] = PUBLISHER_ID
            value["url"] = SITE
            logo = value.get("logo")
            if not logo:
                value["logo"] = {"@type": "ImageObject", "url": LOGO}
            elif isinstance(logo, str):
                value["logo"] = {"@type": "ImageObject", "url": logo}
        for child in value.values():
            enrich_publisher(child)
    elif isinstance(value, list):
        for child in value:
            enrich_publisher(child)


def normalize_jsonld(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        enrich_publisher(data)
        return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    return JSONLD_RE.sub(repl, text)


def replace_marker(text: str, start: str, end: str, block: str) -> str:
    pattern = re.compile(
        re.escape(start) + r".*?" + re.escape(end),
        re.DOTALL,
    )
    wrapped = start + "\n" + block + "\n" + end
    if pattern.search(text):
        return pattern.sub(wrapped, text, count=1)
    return text.replace("</head>", "\n" + wrapped + "\n</head>")


def update_book_page(spec: dict[str, str]) -> None:
    path = ROOT / spec["path"]
    text = path.read_text(encoding="utf-8")
    text = ensure_robots(text, video=True)

    canonical = canonical_value(text, f'{SITE}/{spec["path"]}')
    page_title = title_value(text)
    description = meta_value(text, "description")

    def book_repl(match: re.Match[str]) -> str:
        raw = match.group(2).strip()
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            return match.group(0)
        if data.get("@type") != "Book":
            return match.group(0)
        data["@id"] = f"{canonical}#book"
        data["mainEntityOfPage"] = {"@id": f"{canonical}#webpage"}
        data["inLanguage"] = "en"
        data["publisher"] = PUBLISHER
        data["author"] = {"@type": "Organization", "@id": PUBLISHER_ID, "name": "JayTree Books", "url": SITE}
        data["isPartOf"] = {"@type": "WebSite", "@id": WEBSITE_ID, "name": "JayTree Books", "url": SITE}
        return match.group(1) + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + match.group(3)

    text = JSONLD_RE.sub(book_repl, text)

    video_match = re.search(
        r'data-youtube-id="([^"]+)"\s+data-title="([^"]+)"',
        text,
        flags=re.IGNORECASE,
    )
    graph = [
        {
            "@type": "WebPage",
            "@id": f"{canonical}#webpage",
            "url": canonical,
            "name": page_title,
            "description": description,
            "isPartOf": {"@id": WEBSITE_ID},
            "mainEntity": {"@id": f"{canonical}#book"},
            "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{canonical}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "JayTree Books", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": "Mystery Books", "item": f"{SITE}/mystery-books.html"},
                {"@type": "ListItem", "position": 3, "name": spec["title"], "item": canonical},
            ],
        },
    ]
    if video_match:
        video_id, video_title = video_match.groups()
        graph.append(
            {
                "@type": "VideoObject",
                "@id": f"{canonical}#trailer",
                "name": video_title,
                "description": f'Official trailer for {spec["title"]}, a JayTree Books mystery.',
                "thumbnailUrl": f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
                "embedUrl": f"https://www.youtube.com/embed/{video_id}",
                "contentUrl": f"https://www.youtube.com/watch?v={video_id}",
                "isPartOf": {"@id": f"{canonical}#book"},
            }
        )
    entity_json = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, separators=(",", ":"))
    text = replace_marker(
        text,
        "<!-- JAYTREE_ENTITY_GRAPH_START -->",
        "<!-- JAYTREE_ENTITY_GRAPH_END -->",
        f'<script type="application/ld+json">{entity_json}</script>',
    )

    if 'class="seo-breadcrumbs"' not in text:
        crumbs = (
            '<nav class="seo-breadcrumbs" aria-label="Breadcrumb">'
            '<a href="../index.html">JayTree Books</a><span aria-hidden="true">›</span>'
            '<a href="../mystery-books.html">Mystery Books</a><span aria-hidden="true">›</span>'
            f'<span aria-current="page">{spec["title"]}</span></nav>'
        )
        text = re.sub(r"<main>\s*", "<main>\n" + crumbs + "\n", text, count=1, flags=re.IGNORECASE)

    write_if_changed(path, text)


def update_chapter_page(spec: dict[str, str]) -> None:
    path = ROOT / spec["chapter"]
    text = path.read_text(encoding="utf-8")
    text = ensure_robots(text)
    canonical = canonical_value(text, f'{SITE}/{spec["chapter"]}')
    book_url = f'{SITE}/books/{spec["slug"]}.html'
    page_title = title_value(text)
    description = meta_value(text, "description")

    if 'property="og:title"' not in text:
        social = "\n".join(
            [
                '<meta property="og:type" content="article">',
                f'<meta property="og:url" content="{canonical}">',
                f'<meta property="og:title" content="{page_title}">',
                f'<meta property="og:description" content="{description}">',
                f'<meta property="og:image" content="{SITE}/images/optimized/{spec["cover"]}">',
                f'<meta property="og:image:alt" content="{spec["title"]} book cover">',
                '<meta name="twitter:card" content="summary_large_image">',
                f'<meta name="twitter:title" content="{page_title}">',
                f'<meta name="twitter:description" content="{description}">',
                f'<meta name="twitter:image" content="{SITE}/images/optimized/{spec["cover"]}">',
            ]
        )
        canonical_tag = re.search(r'<link\s+rel="canonical"\s+href="[^"]+">', text, re.IGNORECASE)
        if canonical_tag:
            text = text[: canonical_tag.end()] + "\n" + social + text[canonical_tag.end() :]

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": page_title,
                "description": description,
                "isPartOf": {"@id": WEBSITE_ID},
                "about": {"@id": f"{book_url}#book"},
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
                "mainEntity": {"@id": f"{canonical}#preview"},
            },
            {
                "@type": "CreativeWork",
                "@id": f"{canonical}#preview",
                "name": f'{spec["title"]} — First Chapter Preview',
                "isPartOf": {"@type": "Book", "@id": f"{book_url}#book", "name": spec["title"], "url": book_url},
                "inLanguage": "en",
                "publisher": {"@id": PUBLISHER_ID},
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "JayTree Books", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": spec["title"], "item": book_url},
                    {"@type": "ListItem", "position": 3, "name": "First Chapter", "item": canonical},
                ],
            },
        ],
    }
    schema_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    text = replace_marker(
        text,
        "<!-- JAYTREE_CHAPTER_SCHEMA_START -->",
        "<!-- JAYTREE_CHAPTER_SCHEMA_END -->",
        f'<script type="application/ld+json">{schema_json}</script>',
    )

    if 'class="reader-breadcrumbs"' not in text:
        crumbs = (
            '<nav class="reader-breadcrumbs" aria-label="Breadcrumb">'
            '<a href="../index.html">JayTree Books</a><span aria-hidden="true">›</span>'
            f'<a href="../books/{spec["slug"]}.html">{spec["title"]}</a><span aria-hidden="true">›</span>'
            '<span aria-current="page">First Chapter</span></nav>'
        )
        context = (
            f'<p class="chapter-context">Reading preview for <a href="../books/{spec["slug"]}.html">{spec["title"]}</a> '
            '— view the book page for the trailer, audio sample, Kindle Unlimited link, and related mysteries.</p>'
        )
        text = re.sub(r"<main>\s*", "<main>\n" + crumbs + "\n" + context + "\n", text, count=1, flags=re.IGNORECASE)

    if "JAYTREE_CHAPTER_SEO_STYLES" not in text:
        css = (
            "\n/* JAYTREE_CHAPTER_SEO_STYLES */\n"
            ".reader-breadcrumbs{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 18px;font-family:Arial,Helvetica,sans-serif;font-size:.82rem;color:#aaa9a3}"
            ".reader-breadcrumbs a{color:#c8a15a;text-decoration:none}.reader-breadcrumbs a:hover{text-decoration:underline}"
            ".chapter-context{margin:0 0 28px;padding:14px 16px;border-left:3px solid #c8a15a;background:#101920;color:#c8c2b5;font-family:Arial,Helvetica,sans-serif;font-size:.92rem;line-height:1.55}"
            ".chapter-context a{color:#e8dfcc}\n"
        )
        text = text.replace("</style>", css + "</style>", 1)

    write_if_changed(path, text)


def update_index() -> None:
    path = ROOT / "index.html"
    text = path.read_text(encoding="utf-8")
    text = ensure_robots(text, video=True)
    text = normalize_jsonld(text)

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "WebSite", "@id": WEBSITE_ID, "url": f"{SITE}/", "name": "JayTree Books", "publisher": {"@id": PUBLISHER_ID}, "inLanguage": "en"},
            {"@type": "WebPage", "@id": f"{SITE}/#webpage", "url": f"{SITE}/", "name": "JayTree Books | Mystery & Psychological Thrillers", "isPartOf": {"@id": WEBSITE_ID}, "about": {"@id": PUBLISHER_ID}},
        ],
    }
    schema_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    text = replace_marker(
        text,
        "<!-- JAYTREE_WEBSITE_SCHEMA_START -->",
        "<!-- JAYTREE_WEBSITE_SCHEMA_END -->",
        f'<script type="application/ld+json">{schema_json}</script>',
    )
    text = text.replace('href="#about">About</a>', 'href="about.html">About</a>')
    if 'href="about.html" data-track="about_page"' not in text:
        text = text.replace(
            '<a class="cta" href="mystery-books.html">Find Your Next Mystery →</a>',
            '<div class="hero-actions"><a class="cta" href="mystery-books.html">Find Your Next Mystery →</a>'
            '<a class="cta" href="about.html" data-track="about_page">About JayTree Books →</a></div>',
        )
    if '<div class="footer-links"><a href="about.html">' not in text:
        text = text.replace(
            '<div class="footer-links"><a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></div>',
            '<div class="footer-links"><a href="about.html">About</a> · <a href="privacy.html">Privacy</a> · <a href="terms.html">Terms</a></div>',
        )
    write_if_changed(path, text)


def update_root_pages() -> None:
    for rel in ROOT_SEO_PAGES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        text = ensure_robots(text, video=True)
        text = normalize_jsonld(text)
        text = text.replace('href="index.html#about"', 'href="about.html"')
        write_if_changed(path, text)


def update_styles() -> None:
    path = ROOT / "styles.css"
    text = path.read_text(encoding="utf-8")
    if "JAYTREE_SEO_BREADCRUMBS" not in text:
        text += (
            "\n\n/* JAYTREE_SEO_BREADCRUMBS */\n"
            ".seo-breadcrumbs{max-width:1180px;margin:0 auto;padding:20px 24px 0;display:flex;flex-wrap:wrap;gap:8px;align-items:center;color:var(--muted);font-size:.82rem;letter-spacing:.02em}"
            ".seo-breadcrumbs a{color:var(--gold);text-decoration:none}.seo-breadcrumbs a:hover{text-decoration:underline}"
            '.seo-breadcrumbs span[aria-current="page"]{color:#c9c5bb}\n'
        )
    write_if_changed(path, text)


def validate() -> None:
    problems: list[str] = []
    for spec in BOOKS:
        book = (ROOT / spec["path"]).read_text(encoding="utf-8")
        chapter = (ROOT / spec["chapter"]).read_text(encoding="utf-8")
        for raw in JSONLD_RE.findall(book):
            try:
                json.loads(raw[1].strip())
            except json.JSONDecodeError as exc:
                problems.append(f'{spec["path"]}: invalid JSON-LD: {exc}')
        if f'{SITE}/books/{spec["slug"]}.html#book' not in book:
            problems.append(f'{spec["path"]}: Book @id missing')
        if '"author":{"@type":"Organization","@id":"https://jaytreebooks.com/#publisher","name":"JayTree Books"' not in book:
            problems.append(f'{spec["path"]}: Book author entity missing')
        if "JAYTREE_ENTITY_GRAPH_START" not in book or '"@type":"VideoObject"' not in book:
            problems.append(f'{spec["path"]}: entity graph/video missing')
        if 'class="seo-breadcrumbs"' not in book:
            problems.append(f'{spec["path"]}: visible breadcrumbs missing')
        if "JAYTREE_CHAPTER_SCHEMA_START" not in chapter:
            problems.append(f'{spec["chapter"]}: chapter schema missing')
        if 'class="reader-breadcrumbs"' not in chapter or 'class="chapter-context"' not in chapter:
            problems.append(f'{spec["chapter"]}: chapter/book relationship UI missing')

    about = (ROOT / "about.html").read_text(encoding="utf-8")
    if '"@type":"ProfilePage"' not in about or PUBLISHER_ID not in about:
        problems.append("about.html: publisher profile schema missing")
    index = (ROOT / "index.html").read_text(encoding="utf-8")
    if "JAYTREE_WEBSITE_SCHEMA_START" not in index or 'href="about.html"' not in index:
        problems.append("index.html: website schema/about link missing")
    if "JAYTREE_SEO_BREADCRUMBS" not in (ROOT / "styles.css").read_text(encoding="utf-8"):
        problems.append("styles.css: breadcrumb styles missing")

    if problems:
        raise SystemExit("Entity SEO validation failed:\n- " + "\n- ".join(problems))
    print("Entity SEO validation passed.")


def main() -> int:
    update_index()
    update_root_pages()
    update_styles()
    for spec in BOOKS:
        update_book_page(spec)
        update_chapter_page(spec)
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
