#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
APP_PATH = ROOT / "app.js"
INDEX_PATH = ROOT / "index.html"
STYLES_PATH = ROOT / "styles.css"
BOOKS_DIR = ROOT / "books"
OPTIMIZED_DIR = ROOT / "images" / "optimized"
SITE = "https://www.JayTreeBooks.com"

CONFIG_RE = re.compile(
    r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;",
    re.DOTALL,
)

KNOWN_SOCIALS = {
    "youtube": "https://www.youtube.com/@JayTreeBooks",
    "x": "https://x.com/JayTreeBooks",
    "tiktok": "https://www.tiktok.com/@jaytreebooks",
    "instagram": "",
    "facebook": "",
}

CHAPTER_STYLE_MARKER = "/* JAYTREE_READER_CONVERSION */"
CHAPTER_CTA_START = "<!-- JAYTREE_READER_CONVERSION_START -->"
CHAPTER_CTA_END = "<!-- JAYTREE_READER_CONVERSION_END -->"
CHAPTER_ANALYTICS_START = "<!-- JAYTREE_CHAPTER_ANALYTICS_START -->"
CHAPTER_ANALYTICS_END = "<!-- JAYTREE_CHAPTER_ANALYTICS_END -->"
INDEX_SCHEMA_START = "<!-- JAYTREE_ORG_SCHEMA_START -->"
INDEX_SCHEMA_END = "<!-- JAYTREE_ORG_SCHEMA_END -->"
INDEX_SOCIAL_START = "<!-- JAYTREE_SOCIAL_FOLLOW_START -->"
INDEX_SOCIAL_END = "<!-- JAYTREE_SOCIAL_FOLLOW_END -->"
SITE_STYLE_MARKER = "/* JAYTREE_READER_GROWTH */"


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


def youtube_id(value: str) -> str:
    value = str(value or "").strip().replace("\\&", "&")
    if not value:
        return ""
    parsed = urlparse(value)
    host = parsed.netloc.lower()
    if "youtu.be" in host:
        return parsed.path.strip("/").split("/")[0]
    if "youtube.com" in host:
        if parsed.path.startswith("/watch"):
            from urllib.parse import parse_qs
            return (parse_qs(parsed.query).get("v") or [""])[0]
        parts = [part for part in parsed.path.split("/") if part]
        for marker in ("shorts", "embed"):
            if marker in parts:
                index = parts.index(marker)
                if index + 1 < len(parts):
                    return parts[index + 1]
    return ""


def optimize_covers(config: dict) -> None:
    OPTIMIZED_DIR.mkdir(parents=True, exist_ok=True)
    for book in config.get("books", []):
        original = str(book.get("coverOriginal") or book.get("cover") or "").strip()
        if original.startswith("images/optimized/"):
            candidate = ROOT / "images" / f"{book['slug']}.png"
            if candidate.exists():
                original = str(candidate.relative_to(ROOT)).replace("\\", "/")
            else:
                raise FileNotFoundError(f"Original cover is unknown for {book['title']}")
        source = ROOT / original
        if not source.exists():
            raise FileNotFoundError(f"Cover not found for {book['title']}: {source}")
        destination = OPTIMIZED_DIR / f"{book['slug']}.webp"
        with Image.open(source) as image:
            image.load()
            if image.width > 900:
                height = max(1, round(image.height * (900 / image.width)))
                image = image.resize((900, height), Image.Resampling.LANCZOS)
            if image.mode not in {"RGB", "RGBA"}:
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
            image.save(destination, "WEBP", quality=84, method=6)
        book["coverOriginal"] = original
        book["cover"] = str(destination.relative_to(ROOT)).replace("\\", "/")
        print(f"Optimized {book['title']}: {source.name} -> {destination.name} ({destination.stat().st_size:,} bytes)")


def ensure_socials(config: dict) -> None:
    socials = config.setdefault("socials", {})
    for key, value in KNOWN_SOCIALS.items():
        if key not in socials:
            socials[key] = value


def social_links(config: dict, *, prefix: str = "") -> str:
    labels = {
        "youtube": "YouTube",
        "instagram": "Instagram",
        "facebook": "Facebook",
        "tiktok": "TikTok",
        "x": "X",
    }
    links = []
    for key in ("youtube", "instagram", "facebook", "tiktok", "x"):
        url = str((config.get("socials") or {}).get(key) or "").strip()
        if url:
            links.append(
                f'<a class="social-pill" href="{escape(url, quote=True)}" target="_blank" rel="noopener" '
                f'data-social="{key}">{labels[key]}</a>'
            )
    return "".join(links)


def replace_marker_block(text: str, start: str, end: str, content: str) -> str:
    block = f"{start}\n{content.rstrip()}\n{end}"
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.DOTALL)
    if pattern.search(text):
        return pattern.sub(lambda _: block, text)
    return text


def patch_app_js() -> None:
    text = APP_PATH.read_text(encoding="utf-8")
    text = text.replace(
        '<a class="cover" href="book.html?book=${b.slug}" aria-label="Explore ${b.title}"><img src="${b.cover}" alt="${b.title} book cover"></a>',
        '<a class="cover" href="books/${b.slug}.html" aria-label="Explore ${b.title}"><img src="${b.cover}" alt="${b.title} book cover" loading="lazy" decoding="async"></a>',
    )
    text = text.replace(
        '<a class="buy" href="book.html?book=${b.slug}" data-track="book_page" data-book="${b.slug}">Explore Book</a>',
        '<a class="buy" href="books/${b.slug}.html" data-track="book_page" data-book="${b.slug}">Explore Book</a>',
    )
    APP_PATH.write_text(text, encoding="utf-8")


def chapter_analytics(config: dict) -> str:
    ga4 = escape(str(config.get("ga4") or ""), quote=True)
    if not ga4:
        return ""
    return f"""{CHAPTER_ANALYTICS_START}
<script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
<script>
window.dataLayer=window.dataLayer||[];
function gtag(){{dataLayer.push(arguments)}}
gtag('js',new Date());
gtag('config','{ga4}');
</script>
{CHAPTER_ANALYTICS_END}"""


def chapter_cta(book: dict) -> str:
    slug = escape(book["slug"], quote=True)
    title = escape(book["title"])
    amazon = escape(book["amazonUrl"], quote=True)
    trailer = escape(book.get("trailerUrl") or "", quote=True)
    trailer_button = ""
    if trailer:
        trailer_button = (
            f'<a class="chapter-conversion-button" href="{trailer}" target="_blank" rel="noopener" '
            f'data-conversion="chapter_trailer">Watch the Trailer</a>'
        )
    return f"""{CHAPTER_CTA_START}
<section class="chapter-conversion" aria-label="Continue reading {title}">
  <div class="chapter-conversion-kicker">Ready for Chapter Two?</div>
  <h2>Keep reading <em>{title}</em>.</h2>
  <p>Kindle Unlimited members can continue the full story at no additional cost.</p>
  <div class="chapter-conversion-actions">
    <a class="chapter-conversion-button primary" href="{amazon}" target="_blank" rel="noopener" data-conversion="chapter_kindle_unlimited">Continue FREE with Kindle Unlimited</a>
    <a class="chapter-conversion-button" href="../books/{slug}.html" data-conversion="chapter_book_page">Explore the Book</a>
    {trailer_button}
  </div>
  <small>Not a Kindle Unlimited member? The Amazon page also shows available purchase formats.</small>
</section>
<script>
document.querySelectorAll('[data-conversion]').forEach(function(el){{
  el.addEventListener('click',function(){{
    if(typeof gtag==='function') gtag('event',el.dataset.conversion,{{book:'{slug}'}});
  }});
}});
</script>
{CHAPTER_CTA_END}"""


def patch_chapters(config: dict) -> None:
    style = f"""
{CHAPTER_STYLE_MARKER}
.chapter-conversion{{margin:54px 0 10px;padding:30px;border:1px solid #c8a15a;background:linear-gradient(145deg,#111d25,#0b1218);box-shadow:0 24px 55px rgba(0,0,0,.28)}}
.chapter-conversion-kicker{{color:#c8a15a;letter-spacing:.2em;text-transform:uppercase;font-size:.72rem}}
.chapter-conversion h2{{margin:10px 0 12px;font-size:2rem;font-weight:400;line-height:1.15}}
.chapter-conversion p{{color:#c8c2b5}}
.chapter-conversion small{{display:block;margin-top:16px;color:#8d918f}}
.chapter-conversion-actions{{display:flex;gap:10px;flex-wrap:wrap;margin-top:20px}}
.chapter-conversion-button{{display:inline-block;padding:12px 16px;border:1px solid #c8a15a;text-decoration:none;text-transform:uppercase;letter-spacing:.09em;font-size:.7rem;color:#e8dfcc}}
.chapter-conversion-button.primary,.chapter-conversion-button:hover{{background:#c8a15a;color:#080d12}}
@media(max-width:650px){{.chapter-conversion{{padding:22px}}.chapter-conversion-actions{{display:grid}}.chapter-conversion-button{{text-align:center}}}}
""".strip()

    analytics = chapter_analytics(config)
    for book in config.get("books", []):
        path = ROOT / book["chapter"]
        text = path.read_text(encoding="utf-8")

        if CHAPTER_STYLE_MARKER not in text:
            if "</style>" in text:
                text = text.replace("</style>", style + "\n</style>", 1)
            else:
                text = text.replace("</head>", f"<style>\n{style}\n</style>\n</head>", 1)

        description = escape(
            f"Read Chapter One of {book['title']} by JayTree Books, then continue the full mystery with Kindle Unlimited.",
            quote=True,
        )
        canonical = f"{SITE}/{book['chapter']}"
        meta_block = (
            f'<meta name="description" content="{description}">\n'
            f'<link rel="canonical" href="{canonical}">'
        )
        if 'name="description"' not in text:
            text = text.replace("<title>", meta_block + "\n<title>", 1)
        if analytics and CHAPTER_ANALYTICS_START not in text:
            text = text.replace("</head>", analytics + "\n</head>", 1)

        cta = chapter_cta(book)
        if CHAPTER_CTA_START in text:
            text = replace_marker_block(text, CHAPTER_CTA_START, CHAPTER_CTA_END, cta[len(CHAPTER_CTA_START):].split(CHAPTER_CTA_END)[0].strip())
        else:
            text = text.replace("</main>", cta + "\n</main>", 1)

        path.write_text(text, encoding="utf-8")
        print(f"Enhanced chapter conversion: {path.relative_to(ROOT)}")


def book_schema(book: dict) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Book",
        "name": book["title"],
        "description": book["description"],
        "genre": book["genre"],
        "image": f"{SITE}/{book['cover']}",
        "url": f"{SITE}/books/{book['slug']}.html",
        "publisher": {
            "@type": "Organization",
            "name": "JayTree Books",
            "url": SITE,
        },
        "offers": {
            "@type": "Offer",
            "url": book["amazonUrl"],
            "availability": "https://schema.org/InStock",
        },
        "sameAs": [book["amazonUrl"]] + ([book["trailerUrl"]] if book.get("trailerUrl") else []),
    }


def video_embed(url: str, title: str, *, short: bool = False) -> str:
    video_id = youtube_id(url)
    if not video_id:
        return ""
    cls = "book-video short-video" if short else "book-video"
    return (
        f'<div class="{cls}"><iframe src="https://www.youtube-nocookie.com/embed/{video_id}?rel=0" '
        f'title="{escape(title, quote=True)}" loading="lazy" referrerpolicy="strict-origin-when-cross-origin" '
        'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
        'allowfullscreen></iframe></div>'
    )


def generate_book_page(book: dict, config: dict) -> str:
    title = escape(book["title"])
    slug = escape(book["slug"], quote=True)
    description = escape(book["description"])
    meta_description = escape(
        f"{book['description']} Read Chapter One, watch the official trailer, and read FREE with Kindle Unlimited.",
        quote=True,
    )
    canonical = f"{SITE}/books/{book['slug']}.html"
    image = f"{SITE}/{book['cover']}"
    schema = json.dumps(book_schema(book), ensure_ascii=False, separators=(",", ":"))
    ga4 = escape(str(config.get("ga4") or ""), quote=True)
    analytics = ""
    if ga4:
        analytics = f"""<script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{ga4}');</script>"""

    trailer = video_embed(book.get("trailerUrl") or "", f"{book['title']} official book trailer")
    short = video_embed(book.get("shortUrl") or "", f"{book['title']} YouTube Short", short=True)
    audiobook = video_embed(book.get("audiobookYoutubeUrl") or "", f"{book['title']} audiobook reading")

    media_sections = []
    if trailer:
        media_sections.append(f"""<section class="book-section"><div class="eyebrow">Official Book Trailer</div><h2>Watch the mystery begin.</h2><p class="section-copy">Get a cinematic introduction to {title}.</p>{trailer}</section>""")
    if short:
        media_sections.append(f"""<section class="book-section"><div class="eyebrow">YouTube Short</div><h2>A quick taste of the story.</h2><div class="short-wrap">{short}</div></section>""")
    if audiobook:
        media_sections.append(f"""<section class="book-section"><div class="eyebrow">Listen</div><h2>Hear the story.</h2><p class="section-copy">Preview the atmosphere with the JayTree Books reading.</p>{audiobook}</section>""")

    related = []
    for other in config.get("books", []):
        if other["slug"] == book["slug"]:
            continue
        related.append(
            f'<a class="related-book-link" href="{escape(other["slug"], quote=True)}.html">'
            f'<img src="../{escape(other["cover"], quote=True)}" alt="{escape(other["title"], quote=True)} book cover" loading="lazy" decoding="async">'
            f'<span>{escape(other["title"])}</span></a>'
        )
    related_html = "".join(related[:4])

    social_html = social_links(config)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{title} — Mystery Thriller | JayTree Books</title>
<meta name="description" content="{meta_description}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="book">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="{title} — Read FREE with Kindle Unlimited | JayTree Books">
<meta property="og:description" content="{meta_description}">
<meta property="og:image" content="{image}">
<meta property="og:image:alt" content="{title} book cover">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title} — Read FREE with Kindle Unlimited | JayTree Books">
<meta name="twitter:description" content="{meta_description}">
<meta name="twitter:image" content="{image}">
<script type="application/ld+json">{schema}</script>
{analytics}
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<header class="nav"><div class="nav-inner"><a class="brand" href="../index.html">JAYTREE BOOKS</a><button class="menu-toggle" aria-label="Open menu">☰</button><nav class="nav-links"><a href="../index.html#books">Books</a><a href="../index.html#challenge">Challenge</a><a href="#follow">Follow</a><a href="{escape(config.get('youtube') or KNOWN_SOCIALS['youtube'], quote=True)}" target="_blank" rel="noopener">YouTube</a></nav></div></header>
<main>
<section class="book-hero seo-book-hero">
  <div class="book-cover-large"><img src="../{escape(book['cover'], quote=True)}" alt="{title} book cover" decoding="async" fetchpriority="high"></div>
  <div>
    <div class="book-meta">{escape(book['genre'])}</div>
    <h1>{title}</h1>
    <p class="book-hook">{description}</p>
    <div class="ku-callout"><div><span class="ku-kicker">Kindle Unlimited</span><strong>Read FREE with Kindle Unlimited</strong><small>Kindle Unlimited members can read this title at no additional cost.</small></div><a class="cta solid ku-button" href="{escape(book['amazonUrl'], quote=True)}" target="_blank" rel="noopener" data-track="kindle_unlimited">Read on Kindle Unlimited</a></div>
    <div class="book-actions">
      <a class="cta solid" href="../{escape(book['chapter'], quote=True)}" data-track="chapter">Read Chapter One</a>
      <a class="cta" href="../{escape(book['audio'], quote=True)}" data-track="audio_preview">Play Audio Sample</a>
      <a class="cta" href="{escape(book['amazonUrl'], quote=True)}" target="_blank" rel="noopener" data-track="amazon">Amazon</a>
      {f'<a class="cta" href="{escape(book.get("trailerUrl") or "", quote=True)}" target="_blank" rel="noopener" data-track="trailer_youtube">Watch on YouTube</a>' if book.get('trailerUrl') else ''}
    </div>
  </div>
</section>
{''.join(media_sections)}
<section class="book-section"><div class="eyebrow">More JayTree Mysteries</div><h2>Choose your next case.</h2><div class="related-books">{related_html}</div></section>
<section class="social-follow" id="follow"><div class="wrap narrow"><div class="eyebrow">Follow JayTree Books</div><h2>Stay inside the mystery.</h2><p>Follow for cinematic trailers, mystery challenges, audiobook previews, clues, polls, and new releases.</p><div class="social-pills">{social_html}</div></div></section>
</main>
<footer><div class="footer-brand">JAYTREE BOOKS</div><p>Stories That Stay.</p><div class="footer-links"><a href="../index.html#books">Books</a> · <a href="../index.html#challenge">Challenge</a></div><small>© <span id="year"></span> JayTree Books. All rights reserved.</small></footer>
<script>
document.getElementById('year').textContent=new Date().getFullYear();
document.querySelector('.menu-toggle')?.addEventListener('click',function(){{document.querySelector('.nav')?.classList.toggle('open')}});
document.querySelectorAll('[data-track]').forEach(function(el){{el.addEventListener('click',function(){{if(typeof gtag==='function')gtag('event',el.dataset.track,{{book:'{slug}'}})}})}});
document.querySelectorAll('[data-social]').forEach(function(el){{el.addEventListener('click',function(){{if(typeof gtag==='function')gtag('event','social_visit',{{platform:el.dataset.social,book:'{slug}'}})}})}});
</script>
</body>
</html>
"""


def generate_book_pages(config: dict) -> None:
    BOOKS_DIR.mkdir(parents=True, exist_ok=True)
    for book in config.get("books", []):
        path = BOOKS_DIR / f"{book['slug']}.html"
        path.write_text(generate_book_page(book, config), encoding="utf-8")
        print(f"Generated SEO book page: {path.relative_to(ROOT)}")


def org_schema(config: dict) -> str:
    same_as = [url for url in (config.get("socials") or {}).values() if url]
    if config.get("amazon"):
        same_as.append(config["amazon"])
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "JayTree Books",
        "url": SITE,
        "sameAs": same_as,
    }
    return f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(",", ":"))}</script>'


def patch_index(config: dict) -> None:
    text = INDEX_PATH.read_text(encoding="utf-8")
    schema_content = org_schema(config)
    schema_block = f"{INDEX_SCHEMA_START}\n{schema_content}\n{INDEX_SCHEMA_END}"
    schema_pattern = re.compile(re.escape(INDEX_SCHEMA_START) + r".*?" + re.escape(INDEX_SCHEMA_END), re.DOTALL)
    if schema_pattern.search(text):
        text = schema_pattern.sub(schema_block, text)
    else:
        text = text.replace("</head>", schema_block + "\n</head>", 1)

    socials = social_links(config)
    social_section = f"""{INDEX_SOCIAL_START}
<section class="social-follow" id="follow">
  <div class="wrap narrow">
    <div class="eyebrow">Follow JayTree Books</div>
    <h2>Stay inside the mystery.</h2>
    <p>Follow for cinematic trailers, Mystery Challenge clues, polls, audiobook previews, book news, and new releases.</p>
    <div class="social-pills">{socials}</div>
  </div>
</section>
{INDEX_SOCIAL_END}"""
    social_pattern = re.compile(re.escape(INDEX_SOCIAL_START) + r".*?" + re.escape(INDEX_SOCIAL_END), re.DOTALL)
    if social_pattern.search(text):
        text = social_pattern.sub(social_section, text)
    else:
        text = text.replace('<section class="about" id="about">', social_section + '\n\n\t\t<section class="about" id="about">', 1)

    featured = next((b for b in config.get("books", []) if b["slug"] == config.get("featuredBook")), None)
    if featured:
        text = re.sub(
            r'(<div class="hero-feature">\s*<img src=")[^"]+(" alt="[^"]*book cover")',
            lambda m: m.group(1) + featured["cover"] + m.group(2),
            text,
            count=1,
        )
        text = text.replace(
            f'<img src="{featured["cover"]}" alt="{featured["title"]} book cover">',
            f'<img src="{featured["cover"]}" alt="{featured["title"]} book cover" decoding="async" fetchpriority="high">',
            1,
        )
    text = text.replace(
        '<img src="images/mystery-challenge-case-001.webp"\n\t\t\t\t\t\t\talt="Mystery Challenge Case File 001 — Who Was Lying?">',
        '<img src="images/mystery-challenge-case-001.webp"\n\t\t\t\t\t\t\talt="Mystery Challenge Case File 001 — Who Was Lying?" loading="lazy" decoding="async">',
    )
    INDEX_PATH.write_text(text, encoding="utf-8")


def patch_styles() -> None:
    text = STYLES_PATH.read_text(encoding="utf-8")
    if SITE_STYLE_MARKER in text:
        return
    additions = r'''
/* JAYTREE_READER_GROWTH */
.social-follow{background:radial-gradient(circle at 50% 10%,rgba(200,161,90,.10),transparent 36%),#0a1116;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.social-follow p{color:var(--muted);max-width:720px;margin:0 auto 24px}.social-pills{display:flex;gap:12px;justify-content:center;flex-wrap:wrap}.social-pill{min-width:120px;padding:12px 18px;border:1px solid var(--gold);color:var(--cream);text-decoration:none;text-transform:uppercase;letter-spacing:.12em;font-size:.7rem}.social-pill:hover{background:var(--gold);color:var(--ink)}
.seo-book-hero h1{font-size:clamp(3rem,7vw,6rem)}.related-books{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.related-book-link{display:flex;flex-direction:column;gap:10px;text-decoration:none;color:var(--cream);font-size:1rem}.related-book-link img{width:100%;aspect-ratio:2/3;object-fit:cover;display:block;border:1px solid rgba(232,223,204,.12)}.related-book-link span{color:var(--gold)}
@media(max-width:800px){.related-books{grid-template-columns:repeat(2,1fr)}.social-pill{flex:1 1 135px}.seo-book-hero h1{font-size:clamp(2.7rem,15vw,4.5rem)}}
'''
    STYLES_PATH.write_text(text.rstrip() + "\n" + additions.strip() + "\n", encoding="utf-8")


def generate_sitemap(config: dict) -> None:
    urls = [f"{SITE}/"]
    for book in config.get("books", []):
        urls.append(f"{SITE}/books/{book['slug']}.html")
    for book in config.get("books", []):
        urls.append(f"{SITE}/{book['chapter']}")
    entries = "\n".join(f"  <url><loc>{escape(url)}</loc></url>" for url in urls)
    sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
'''
    (ROOT / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    (ROOT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n",
        encoding="utf-8",
    )


def main() -> int:
    config = load_config()
    ensure_socials(config)
    optimize_covers(config)
    save_config(config)
    patch_app_js()
    patch_chapters(config)
    generate_book_pages(config)
    patch_index(config)
    patch_styles()
    generate_sitemap(config)
    print(f"Reader-growth site build complete for {len(config.get('books', []))} books on {date.today().isoformat()}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
