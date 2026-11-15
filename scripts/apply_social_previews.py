#!/usr/bin/env python3
"""Synchronize page-specific Open Graph and X/Twitter social preview metadata.

No dependencies. Preserves existing titles, descriptions, canonicals, schema, and tracking.
Examples:
  python scripts/apply_social_previews.py --write
  python scripts/apply_social_previews.py --check
"""
from __future__ import annotations
import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://jaytreebooks.com/"
SOCIAL_BASE = "images/social/previews/"
PAGE_ART = {
    "index.html": "home",
    "home-v2.html": "home",
    "books.html": "books",
    "audiobooks.html": "audiobooks",
    "samples.html": "samples-approved-20261115",
    "series-v2.html": "series",
    "news-v2.html": "news",
    "experiences-v2.html": "experiences",
    "about.html": "about",
    "upcoming-books.html": "upcoming-books",
    "reading-guides.html": "reading-guides",
    "case-files.html": "case-files",
    "animated-series.html": "animated-series",
    "mystery-books.html": "mystery-books",
    "psychological-mystery-books.html": "psychological-mystery-books",
    "kindle-unlimited-mystery-books.html": "kindle-unlimited-mystery-books",
    "small-town-mystery-books.html": "small-town-mystery-books",
    "cold-case-mystery-books.html": "cold-case-mystery-books",
    "supernatural-mystery-books.html": "supernatural-mystery-books",
}
PAGE_ALT = {
    "home": "JayTree Books cinematic mystery lake and published thriller covers",
    "books": "JayTree Books psychological mystery book collection with official novel covers",
    "audiobooks": "JayTree Books audiobooks with gold and black headphones, featured Second Draft and $1.99 offer",
    "samples": "JayTree Books first chapter and audiobook samples with an open book and official covers",
    "samples-approved-20261115": "JayTree Books Samples: Try the story first, read Chapter One or listen to an audiobook sample, illustrated with a glowing open book, lantern and headphones by a moonlit lake",
    "series": "JayTree Books connected mystery universe and three upcoming novels",
    "news": "JayTree Books news and upcoming mystery novels artwork",
    "experiences": "JayTree mystery experiences with a haunting red moon over dark water",
    "about": "JayTree Books independent mystery publisher and vintage reading desk",
    "upcoming-books": "JayTree Books upcoming novels Where Mercy Stood, The Fifth Copy and The Sixth Town",
    "reading-guides": "JayTree Books reading guides, open book and The Hollow Year official cover",
    "case-files": "Join the JayTree Case Files and discover mystery news",
    "animated-series": "JayTree Books on-screen cinematic and animated mystery artwork",
    "mystery-books": "JayTree Books mystery novel collection artwork",
    "psychological-mystery-books": "JayTree Books psychological mystery reading desk artwork",
    "kindle-unlimited-mystery-books": "JayTree Books Kindle Unlimited mystery editions",
    "small-town-mystery-books": "JayTree Books small-town mysteries under moonlit skies",
    "cold-case-mystery-books": "JayTree Books cold-case mysteries with The Hollow Bell",
    "supernatural-mystery-books": "JayTree Books eerie mysteries under a crimson moon",
}
META_RE = re.compile(r"<meta\b[^>]*>",re.I|re.S)
ATTR_RE = re.compile(r"([a-zA-Z:_-]+)\s*=\s*([\"'])(.*?)\2",re.S)
HEAD_RE = re.compile(r"(?i)</head\s*>")
TARGETS = {
    ("property","og:image"),("property","og:image:secure_url"),
    ("property","og:image:url"),("property","og:image:type"),
    ("property","og:image:width"),("property","og:image:height"),
    ("property","og:image:alt"),("name","twitter:card"),
    ("name","twitter:image"),("name","twitter:image:alt"),
    ("name","twitter:title"),("name","twitter:description"),
}

def _attrs(tag):
    return {a.lower():v for a,q,v in ATTR_RE.findall(tag)}

def _find_meta(source, typ, key):
    for tag in META_RE.findall(source):
        m=_attrs(tag)
        if m.get(typ,"").lower()==key.lower():
            return html.unescape(m.get("content",""))
    return None

def _page_title(source):
    return html.unescape(re.search(r"<title[^>]*>(.*?)</title>",source,re.I|re.S).group(1)).strip()

def _canonical(source, path):
    m = re.search(r'<link\b(?=[^>]*rel=["\']canonical["\'])[^>]*>',source,re.I|re.S)
    if m:
        href = _attrs(m.group(0)).get("href")
        if href and href.startswith(ORIGIN):
            return href
    return ORIGIN + ("" if path in ("index.html","home-v2.html") else path)

def _page_name(path):
    if path in PAGE_ART:
        return PAGE_ART[path]
    if path.startswith("books/") and path.endswith(".html"):
        slug = Path(path).stem
        if re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*",slug):
            return "book-"+slug
    return None

def _alt(name):
    if name.startswith("book-"):
        suffix=name[5:].replace("-"," ").title()
        return f"{suffix} official JayTree Books cover in its cinematic mystery setting"
    return PAGE_ALT[name]

def apply_to_markup(path, markup):
    """Return modified markup for a known page or original bytes for unrelated pages."""
    name=_page_name(path)
    if not name:
        return markup
    if not (ROOT / SOCIAL_BASE / (name+".jpg")).is_file():
        raise FileNotFoundError(f"No source image for {path}: {name}.jpg")
    head_match=HEAD_RE.search(markup)
    if not head_match:
        raise ValueError(f"Missing </head>: {path}")
    prior=markup[:head_match.start()]
    tail=markup[head_match.start():]
    title=_find_meta(prior,"property","og:title") or _page_title(prior)
    desc=_find_meta(prior,"property","og:description") or _find_meta(prior,"name","description") or ""
    # Filter only social-image and Twitter card tags; keep all other critical tags.
    def remove_tag(match):
        a=_attrs(match.group(0))
        if (("property",a.get("property","").lower()) in TARGETS or
            ("name",a.get("name","").lower()) in TARGETS):
            return ""
        return match.group(0)
    prior=META_RE.sub(remove_tag,prior)
    url=ORIGIN+SOCIAL_BASE+name+".jpg"
    esc=lambda value: html.escape(str(value),quote=True)
    social="\n".join([
        "<!-- JAYTREE_PAGE_SOCIAL_PREVIEW_START -->",
        f'<meta property="og:image" content="{esc(url)}">',
        f'<meta property="og:image:secure_url" content="{esc(url)}">',
        '<meta property="og:image:type" content="image/jpeg">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:image:alt" content="{esc(_alt(name))}">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{esc(title)}">',
        f'<meta name="twitter:description" content="{esc(desc)}">',
        f'<meta name="twitter:image" content="{esc(url)}">',
        f'<meta name="twitter:image:alt" content="{esc(_alt(name))}">',
        "<!-- JAYTREE_PAGE_SOCIAL_PREVIEW_END -->",
    ])
    # Replace previously emitted block to guarantee byte-for-byte idempotence.
    prior=re.sub(r"(?s)\n?<!-- JAYTREE_PAGE_SOCIAL_PREVIEW_START -->.*?<!-- JAYTREE_PAGE_SOCIAL_PREVIEW_END -->\n?","",prior)
    return prior.rstrip()+"\n"+social+"\n"+tail

def files_to_update():
    files=list(PAGE_ART)
    catalog=json.loads((ROOT/"data/storefront-catalog.json").read_text(encoding="utf-8"))
    for book in catalog["books"]:
        if book["book_status"]=="published":
            files.append(book["book_page"])
    return files

def main():
    parser=argparse.ArgumentParser()
    modes=parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--check",action="store_true")
    modes.add_argument("--write",action="store_true")
    args=parser.parse_args()
    changed=[]
    for path in files_to_update():
        file=ROOT/path
        if not file.is_file():
            raise FileNotFoundError(f"Expected published page: {path}")
        old=file.read_text(encoding="utf-8")
        new=apply_to_markup(path,old)
        if new!=old:
            changed.append(path)
            if args.write:file.write_text(new,encoding="utf-8")
    print(f"Social previews: {len(files_to_update())} pages, {len(changed)} {'updated' if args.write else 'out of sync'}")
    if changed:print("Files:",", ".join(changed))
    return 1 if args.check and changed else 0

if __name__=="__main__":
    try:
        sys.exit(main())
    except (OSError,ValueError,KeyError) as exc:
        print("SOCIAL PREVIEW ERROR",exc,file=sys.stderr)
        sys.exit(2)
