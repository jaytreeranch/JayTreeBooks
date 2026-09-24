#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://jaytreebooks.com"
PUBLISHER_ID = f"{SITE}/#publisher"
WEBSITE_ID = f"{SITE}/#website"

BOOKS = [
    {"index": 1, "slug": "second-draft", "title": "Second Draft", "chapter": 1, "cover": "second-draft.png", "amazon": "https://www.amazon.com/dp/B0HFYQ9KGV"},
    {"index": 2, "slug": "the-hollow-year", "title": "The Hollow Year", "chapter": 2, "cover": "the-hollow-year.png", "amazon": "https://www.amazon.com/dp/B0HFXF8MTP"},
    {"index": 3, "slug": "the-hollow-bell", "title": "The Hollow Bell", "chapter": 3, "cover": "the-hollow-bell.png", "amazon": "https://www.amazon.com/dp/B0HD52HGGZ"},
    {"index": 4, "slug": "the-absconding", "title": "The Absconding", "chapter": 4, "cover": "the-absconding.png", "amazon": "https://www.amazon.com/dp/B0HDWRVSXQ"},
    {"index": 5, "slug": "the-correction", "title": "The Correction", "chapter": 5, "cover": "the-correction.png", "amazon": "https://www.amazon.com/dp/B0HFV8KCVL"},
]

CONFIG_RE = re.compile(
    r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;",
    re.DOTALL,
)

SCHEMA_START = "<!-- JAYTREE_AUDIO_SCHEMA_START -->"
SCHEMA_END = "<!-- JAYTREE_AUDIO_SCHEMA_END -->"
TRACKING_START = "<!-- JAYTREE_AUDIO_TRACKING_START -->"
TRACKING_END = "<!-- JAYTREE_AUDIO_TRACKING_END -->"


def load_descriptions() -> dict[str, str]:
    text = (ROOT / "config.js").read_text(encoding="utf-8")
    match = CONFIG_RE.search(text)
    if not match:
        raise RuntimeError("Could not parse config.js")
    data = json.loads(match.group(1))
    return {book["slug"]: book["description"] for book in data["books"]}


def marker_replace(text: str, start: str, end: str, block: str, before: str) -> str:
    wrapped = f"{start}\n{block}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(wrapped, text, count=1)
    return text.replace(before, wrapped + "\n" + before, 1)


def set_or_insert_meta(text: str, attr: str, key: str, value: str) -> str:
    pattern = re.compile(
        rf'<meta\s+{attr}="{re.escape(key)}"\s+content="[^"]*">',
        re.IGNORECASE,
    )
    tag = f'<meta {attr}="{key}" content="{value}">'
    if pattern.search(text):
        return pattern.sub(tag, text, count=1)
    canonical = re.search(r'<link\s+rel="canonical"\s+href="[^"]+">', text, re.IGNORECASE)
    if canonical:
        return text[: canonical.end()] + "\n" + tag + text[canonical.end() :]
    return text.replace("</head>", tag + "\n</head>", 1)


def patch_page(spec: dict, description: str) -> None:
    idx = spec["index"]
    path = ROOT / "audio" / f"book-{idx}-sample.html"
    text = path.read_text(encoding="utf-8")
    canonical = f"{SITE}/audio/book-{idx}-sample.html"
    book_url = f"{SITE}/books/{spec['slug']}.html"
    audio_url = f"{SITE}/audio/book-{idx}-sample.mp3"
    chapter_url = f"{SITE}/chapters/book-{spec['chapter']}-first-chapter.html"
    title = f"{spec['title']} — Audio Sample | JayTree Books"
    meta_description = f"Listen to an audio sample of {spec['title']} by JayTree Books, then explore the book, read Chapter One, or continue with Kindle Unlimited."

    text = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", text, count=1, flags=re.DOTALL)
    text = set_or_insert_meta(text, "name", "description", meta_description)
    text = set_or_insert_meta(text, "name", "robots", "index,follow,max-image-preview:large,max-snippet:-1")
    text = set_or_insert_meta(text, "property", "og:title", title)
    text = set_or_insert_meta(text, "property", "og:description", description)
    text = set_or_insert_meta(text, "property", "og:image:alt", f"{spec['title']} book cover")
    text = set_or_insert_meta(text, "name", "twitter:title", title)
    text = set_or_insert_meta(text, "name", "twitter:description", description)

    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"{canonical}#webpage",
                "url": canonical,
                "name": title,
                "description": meta_description,
                "isPartOf": {"@id": WEBSITE_ID},
                "about": {"@id": f"{book_url}#book"},
                "mainEntity": {"@id": f"{canonical}#audio"},
                "breadcrumb": {"@id": f"{canonical}#breadcrumb"},
            },
            {
                "@type": "AudioObject",
                "@id": f"{canonical}#audio",
                "name": f"{spec['title']} audio sample",
                "description": description,
                "contentUrl": audio_url,
                "encodingFormat": "audio/mpeg",
                "inLanguage": "en",
                "isPartOf": {"@type": "Book", "@id": f"{book_url}#book", "name": spec["title"], "url": book_url},
                "author": {"@type": "Organization", "@id": PUBLISHER_ID, "name": "JayTree Books", "url": SITE},
                "publisher": {"@id": PUBLISHER_ID},
                "thumbnailUrl": f"{SITE}/images/{spec['cover']}",
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "JayTree Books", "item": f"{SITE}/"},
                    {"@type": "ListItem", "position": 2, "name": spec["title"], "item": book_url},
                    {"@type": "ListItem", "position": 3, "name": "Audio Sample", "item": canonical},
                ],
            },
        ],
    }
    schema = '<script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False, separators=(",", ":")) + "</script>"
    text = marker_replace(text, SCHEMA_START, SCHEMA_END, schema, "</head>")

    text = re.sub(
        r'<p class="description">.*?</p>',
        f'<p class="description">{description}</p>',
        text,
        count=1,
        flags=re.DOTALL,
    )

    if 'class="audio-breadcrumbs"' not in text:
        crumbs = (
            '<nav class="audio-breadcrumbs" aria-label="Breadcrumb">'
            '<a href="../index.html">JayTree Books</a><span aria-hidden="true">›</span>'
            f'<a href="../books/{spec["slug"]}.html">{spec["title"]}</a><span aria-hidden="true">›</span>'
            '<span aria-current="page">Audio Sample</span></nav>'
        )
        text = re.sub(
            r'(<section class="audio-card"[^>]*>)',
            r'\1' + crumbs,
            text,
            count=1,
            flags=re.IGNORECASE,
        )

    if "JAYTREE_AUDIO_SEO_STYLES" not in text:
        css = (
            "/* JAYTREE_AUDIO_SEO_STYLES */"
            ".audio-breadcrumbs{display:flex;flex-wrap:wrap;justify-content:center;gap:8px;align-items:center;margin:0 0 24px;color:#aaa9a3;font:400 .76rem/1.4 Arial,sans-serif}"
            ".audio-breadcrumbs a{color:#c8a15a;text-decoration:none}.audio-breadcrumbs a:hover{text-decoration:underline}"
        )
        text = text.replace("</style>", css + "</style>", 1)

    text = re.sub(r"<audio\s+controls", '<audio data-audio-sample controls', text, count=1, flags=re.IGNORECASE)
    text = text.replace(
        f'href="../books/{spec["slug"]}.html"',
        f'href="../books/{spec["slug"]}.html" data-track="audio_book_page"',
        1,
    )
    text = text.replace(
        f'href="../chapters/book-{spec["chapter"]}-first-chapter.html"',
        f'href="../chapters/book-{spec["chapter"]}-first-chapter.html" data-track="audio_chapter"',
        1,
    )
    text = text.replace(
        f'href="{spec["amazon"]}"',
        f'href="{spec["amazon"]}" data-track="audio_kindle_unlimited"',
        1,
    )

    tracking = f"""<script>
(function(){{
  var audio=document.querySelector('[data-audio-sample]');
  var started=false, completed=false;
  function send(name, extra){{
    if(typeof gtag==='function') gtag('event',name,Object.assign({{book:'{spec["slug"]}',placement:'audio_sample_page'}},extra||{{}}));
  }}
  if(audio){{
    audio.addEventListener('play',function(){{if(!started){{started=true;send('audio_sample_play')}}}});
    audio.addEventListener('ended',function(){{if(!completed){{completed=true;send('audio_sample_complete')}}}});
  }}
  document.querySelectorAll('[data-track]').forEach(function(el){{
    el.addEventListener('click',function(){{send(el.dataset.track)}});
  }});
}})();
</script>"""
    text = marker_replace(text, TRACKING_START, TRACKING_END, tracking, "</body>")

    path.write_text(text, encoding="utf-8")
    print(f"Upgraded audio SEO: {path.relative_to(ROOT)}")


def validate() -> None:
    problems = []
    for spec in BOOKS:
        idx = spec["index"]
        text = (ROOT / "audio" / f"book-{idx}-sample.html").read_text(encoding="utf-8")
        required = [
            '"@type":"AudioObject"',
            f'{SITE}/audio/book-{idx}-sample.mp3',
            f'{SITE}/books/{spec["slug"]}.html#book',
            '"author":{"@type":"Organization","@id":"https://jaytreebooks.com/#publisher"',
            'class="audio-breadcrumbs"',
            'name="robots" content="index,follow,max-image-preview:large,max-snippet:-1"',
            'data-audio-sample',
            "audio_sample_play",
            "audio_sample_complete",
        ]
        for needle in required:
            if needle not in text:
                problems.append(f"audio/book-{idx}-sample.html missing {needle}")
        match = re.search(rf"{re.escape(SCHEMA_START)}\s*<script type=\"application/ld\+json\">(.*?)</script>", text, re.DOTALL)
        if not match:
            problems.append(f"audio/book-{idx}-sample.html missing JSON-LD block")
        else:
            try:
                json.loads(match.group(1))
            except json.JSONDecodeError as exc:
                problems.append(f"audio/book-{idx}-sample.html invalid JSON-LD: {exc}")
    if problems:
        raise SystemExit("Audio SEO validation failed:\n- " + "\n- ".join(problems))
    print("Audio SEO validation passed.")


def main() -> int:
    descriptions = load_descriptions()
    for spec in BOOKS:
        patch_page(spec, descriptions[spec["slug"]])
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
