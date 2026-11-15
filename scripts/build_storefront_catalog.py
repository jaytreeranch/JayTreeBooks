#!/usr/bin/env python3
"""Generate static Books, Audiobooks, and Samples cards from one catalog.
python scripts/build_storefront_catalog.py --write
python scripts/build_storefront_catalog.py --check
"""
import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
MARKERS = {"books.html": "BOOKS", "audiobooks.html": "AUDIOBOOKS", "samples.html": "SAMPLES"}
CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="9" cy="20" r="1.3"/><circle cx="19" cy="20" r="1.3"/><path d="M2 3h3l2.5 12h12l2-9H6"/></svg>'
PLAY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M10 7.7v8.6l6.6-4.3z" fill="currentColor" stroke="none"/></svg>'
NUMBER = ("zero","one","two","three","four","five","six","seven","eight","nine","ten",
          "eleven","twelve","thirteen","fourteen","fifteen","sixteen","seventeen","eighteen","nineteen","twenty")

def e(value):
    return html.escape(str(value), quote=True)

def words(n):
    return NUMBER[n] if n < len(NUMBER) else str(n)

def validate(catalog):
    if catalog.get("schema_version") != 1 or not isinstance(catalog.get("books"), list):
        raise ValueError("catalog must have schema_version=1 and books array")
    seen, sales = set(), set()
    for book in catalog["books"]:
        slug = book.get("slug", "")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug) or slug in seen:
            raise ValueError("invalid or duplicate slug: " + slug)
        seen.add(slug)
        for required in ("title","edition","tagline","description"):
            if not isinstance(book.get(required), str) or not book[required].strip():
                raise ValueError(slug + ": missing " + required)
        if book.get("book_status") not in ("published", "coming_soon"):
            raise ValueError(slug + ": bad book status")
        if book.get("audiobook_status") not in ("available","coming_soon","not_planned"):
            raise ValueError(slug + ": bad audiobook status")
        for field in ("cover","audio_cover","audio_hero","book_page","sample_page","chapter_page"):
            value = book.get(field, "")
            if value and (not isinstance(value, str) or
                          not re.fullmatch(r"[A-Za-z0-9_./-]+", value) or
                          ".." in value.split("/") or value.startswith("/")):
                raise ValueError(slug + ": unsafe " + field)
        for field, domain in (("amazon_url", "www.amazon.com"), ("payhip_url", "payhip.com")):
            value = book.get(field, "")
            if value:
                u = urlparse(value)
                if u.scheme != "https" or u.netloc != domain or not u.path.startswith("/"):
                    raise ValueError(slug + ": unsafe " + field)
        if book["book_status"] == "published" and not all(book.get(k) for k in ("cover","book_page","amazon_url")):
            raise ValueError(slug + ": published book needs cover, book page and Amazon URL")
        if book["audiobook_status"] == "available":
            if book["book_status"] != "published" or not all(book.get(k) for k in
                 ("cover","sample_page","payhip_url","narrator","audiobook_price_usd")):
                raise ValueError(slug + ": audiobook needs published status and actual sale/sample details")
            try:
                if float(book["audiobook_price_usd"]) <= 0: raise ValueError()
            except (TypeError, ValueError):
                raise ValueError(slug + ": invalid audiobook price")
            if book["payhip_url"] in sales: raise ValueError(slug + ": duplicate sale URL")
            sales.add(book["payhip_url"])
        elif book.get("payhip_url"):
            raise ValueError(slug + ": unreleased audiobook must not have a Payhip sale URL")
        if book.get("kindle_unlimited") not in (None, True, False):
            raise ValueError(slug + ": invalid KU setting")
    if catalog.get("featured_audiobook") not in [x["slug"] for x in catalog["books"] if x["audiobook_status"] == "available"]:
        raise ValueError("featured_audiobook must be currently available")
    live_prices = {str(x["audiobook_price_usd"]) for x in catalog["books"] if x["audiobook_status"] == "available"}
    if len(live_prices) > 1:
        raise ValueError("Mixed audiobook prices require review of sitewide sale-price banners")
    live_narrators = {x["narrator"] for x in catalog["books"] if x["audiobook_status"] == "available"}
    if live_narrators != {"Vivian"}:
        raise ValueError("This storefront currently advertises Vivian only; review narrator messaging before release")
    return catalog["books"]

def cover(book, audio=False):
    if not book.get("cover"):
        return '<span class="sf-coming-cover-placeholder">Artwork coming soon</span>'
    artwork = book.get("audio_cover") if audio else None
    label = " audiobook artwork" if artwork else " official book cover"
    return '<img src="' + e(artwork or book["cover"]) + '" width="300" height="450" loading="lazy" decoding="async" alt="' + e(book["title"] + " " + book["edition"] + label) + '">'

def audio_card(book, selected):
    slug,title,edition = e(book["slug"]),e(book["title"]),e(book["edition"])
    full_title = title + ((" (" + edition + ")") if book["edition"] != "Novel" else "")
    badge = '<span class="sf-cine-edition-badge">' + edition + '</span>' if book["edition"] != "Novel" else ""
    price = "$" + format(float(book["audiobook_price_usd"]), ".2f")
    return f'''<article class="sf-cine-product{' is-selected' if selected else ''}" data-title="{e((book["title"]+" "+book["edition"]).lower())}" data-book="{slug}" data-featured-art="{e(book.get('audio_hero') or book['cover'])}" data-book-page="{e(book['book_page'])}" data-description="{e(book["description"])}">
<button type="button" class="sf-cine-cover-link sf-cine-select" data-select-book="{slug}" aria-label="Feature {full_title} and update Buy and Listen buttons" aria-controls="sf-cine-featured-region" aria-pressed="{'true' if selected else 'false'}">
{cover(book, audio=True)}{badge}<span class="sf-cine-narrated">Narrated by {e(book["narrator"])}</span></button>
<h3 class="sf-cine-product-title">{full_title}</h3>
<a class="sf-cine-buy sf-cine-card-action" href="{e(book["payhip_url"])}" target="_blank" rel="noopener noreferrer" data-track="audiobook_payhip" data-book="{slug}" data-placement="audio_cinematic_shelf">{CART}<span>Buy Audiobook — {price}</span></a>
<a class="sf-cine-sample sf-cine-card-action" href="{e(book["sample_page"])}" data-track="audio_preview" data-book="{slug}" data-placement="audio_cinematic_shelf">{PLAY}<span>Listen to Sample</span></a></article>'''

def books_card(book):
    slug = e(book["slug"])
    published = book["book_status"] == "published"
    kind = e(book["edition"])
    title = e(book["title"]) + ((' <span class="sf-title-kind">('+kind+')</span>') if book["edition"] != "Novel" else "")
    label = ("Kindle Unlimited · Novel" if book.get("kindle_unlimited") else "Separate edition") if published else "Coming soon · Not yet for sale"
    cover_html = ('<a class="sf-cover" href="'+e(book["book_page"])+'">'+cover(book)+'</a>') if published else ('<div class="sf-cover">'+cover(book)+'</div>')
    actions = '<div class="sf-coming-status">In development · No purchase link until released</div>'
    if published:
        actions = f'''<div class="sf-card-row">
<a class="sf-btn sf-btn-gold" href="{e(book["amazon_url"])}" target="_blank" rel="noopener noreferrer" data-track="amazon" data-book="{slug}" data-placement="book_grid">Shop on Amazon</a>
<a class="sf-btn sf-btn-outline" href="{e(book["book_page"])}" data-track="book_page" data-book="{slug}" data-placement="book_grid">Book details</a></div>'''
        if book.get("chapter_page"):
            actions += f'<a class="sf-secondary-link" href="{e(book["chapter_page"])}" data-track="chapter" data-book="{slug}" data-placement="book_grid">Read the first chapter ↗</a>'
        elif book.get("sample_page"):
            actions += f'<a class="sf-secondary-link" href="{e(book["sample_page"])}" data-track="audio_preview" data-book="{slug}" data-placement="book_grid">Listen to preview ↗</a>'
    return f'''<article class="sf-book-card{' sf-book-coming-soon' if not published else ''}">
{cover_html}<div class="sf-card-copy"><span class="sf-label">{label}</span><h3>{title}</h3>
<p class="sf-tag">{e(book["tagline"])}</p><p class="sf-card-hook">{e(book["description"])}</p>{actions}</div></article>'''

def sample_card(book):
    slug,kind=e(book["slug"]),e(book["edition"])
    title = e(book["title"]) + ((" (" + kind + ")") if book["edition"] != "Novel" else "")
    actions = []
    if book.get("sample_page"):
        actions.append(f'<a class="sf-btn sf-btn-gold" href="{e(book["sample_page"])}" data-track="audio_preview" data-book="{slug}" data-placement="samples_page">Hear narrator previews</a>')
    if book.get("chapter_page"):
        actions.append(f'<a class="sf-btn sf-btn-outline" href="{e(book["chapter_page"])}" data-track="chapter" data-book="{slug}" data-placement="samples_page">Read Chapter One</a>')
    if not actions:
        actions.append(f'<a class="sf-btn sf-btn-outline" href="{e(book["book_page"])}">Book details</a>')
    return f'''<article class="sf-sample-card"><div class="sf-sample-cover">{cover(book)}</div><div>
<span class="sf-label">{kind}</span><h3>{title}</h3><p>{e(book["tagline"])}</p>
<div class="sf-sample-actions">{''.join(actions)}</div></div></article>'''

def render_section(text, name, content):
    start,end = "<!-- STOREFRONT_"+name+"_START -->", "<!-- STOREFRONT_"+name+"_END -->"
    if text.count(start) != 1 or text.count(end) != 1:
        raise ValueError(name + ": expected exactly one generated section")
    return text.split(start)[0] + start + "\n" + content + "\n" + end + text.split(end)[1]

def count_copy(text, name, books):
    audio = sum(b["audiobook_status"] == "available" for b in books)
    pub = sum(b["book_status"] == "published" for b in books)
    novels = sum(b["book_status"] == "published" and b["edition"] != "Novella" for b in books)
    novella = sum(b["book_status"] == "published" and b["edition"] == "Novella" for b in books)
    def replace(pattern, value):
        nonlocal text
        text = re.sub(pattern,lambda _:value,text,flags=re.I)
    if name == "home-v2.html":
        replace(r"\b\d+ novels \+ \d+ novella", f"{novels} novels + {novella} novella")
        replace(r"\b\d+ complete Vivian audiobooks", f"{audio} complete Vivian audiobooks")
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) complete audiobooks", f"{words(audio).capitalize()} complete audiobooks")
    if name == "audiobooks.html":
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) complete Vivian audiobooks", f"{words(audio).capitalize()} complete Vivian audiobooks")
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) complete audiobooks", f"{words(audio).capitalize()} complete audiobooks")
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) complete Vivian-narrated editions", f"{words(audio).capitalize()} complete Vivian-narrated editions")
        replace(r"Search (?:six|seven|eight|nine|ten|\d+) audiobooks", f"Search {words(audio)} audiobooks")
        replace(r"Filter the (?:six|seven|eight|nine|ten|\d+) currently available Vivian editions", f"Filter the {words(audio)} currently available Vivian editions")
    if name == "books.html":
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) published books", f"{pub} published books")
        replace(r"\b(?:five|six|seven|eight|nine|ten|\d+) full novels", f"{words(novels)} full novels")
    if name == "samples.html":
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) published editions", f"{pub} published editions")
        replace(r"Vivian's (?:six|seven|eight|nine|ten|\d+) complete audiobooks", f"Vivian's {words(audio)} complete audiobooks")
    if name == "home-v2.html":
        replace(r"\b(?:six|seven|eight|nine|ten|\d+) Vivian audiobooks", f"{words(audio)} Vivian audiobooks")
    if name == "books.html":
        replace(r"\b(?:five|six|seven|eight|nine|ten|\d+) psychological mystery novels", f"{words(novels)} psychological mystery novels")
    return text


def sync_featured(text, book):
    """Update initial featured product when featured_audiobook changes in JSON."""
    slug = e(book["slug"])
    full_title = e(book["title"]) + ((" (" + e(book["edition"]) + ")") if book["edition"] != "Novel" else "")
    def update_tag(tag, identifier, updates):
        nonlocal text
        pattern = r"<" + tag + r"\b[^>]*\bid=\"" + re.escape(identifier) + r"\"[^>]*>"
        def apply(match):
            element = match.group(0)
            for attr, value in updates.items():
                element, count = re.subn(r"\b" + attr + r'="[^"]*"', attr + '="' + e(value) + '"', element, count=1)
                if count != 1:
                    raise ValueError("Featured " + identifier + " missing " + attr)
            return element
        text, count = re.subn(pattern, apply, text, count=1)
        if count != 1:
            raise ValueError("Missing unique featured element " + identifier)
    update_tag("a", "sf-cine-featured-details", {
        "href": book["book_page"], "aria-label": full_title + " — featured book details"})
    update_tag("img", "sf-cine-featured-cover", {
        "src": book.get("audio_hero") or book["cover"], "alt": full_title + " audiobook artwork"})
    update_tag("a", "sf-cine-featured-buy", {
        "href": book["payhip_url"], "data-book": book["slug"]})
    update_tag("a", "sf-cine-featured-sample", {
        "href": book["sample_page"], "data-book": book["slug"]})
    for identifier, value in (("sf-cine-featured-title", full_title),
                              ("sf-cine-featured-description", book["description"])):
        pattern = r'(<(?:h2|p)\b[^>]*id="' + identifier + r'"[^>]*>).*?(</(?:h2|p)>)'
        text, count = re.subn(pattern, lambda m: m.group(1) + e(value) + m.group(2), text, count=1, flags=re.S)
        if count != 1: raise ValueError("Missing featured content " + identifier)
    pattern = r'(<span\b[^>]*id="sf-cine-selection-status"[^>]*>).*?(</span>)'
    text, count = re.subn(pattern, lambda m: m.group(1) + "Selected: " + full_title + m.group(2), text, count=1, flags=re.S)
    if count != 1: raise ValueError("Missing selected status")
    return text

def build(root, catalog):
    books = validate(catalog)
    selected = catalog["featured_audiobook"]
    audio = [b for b in books if b["audiobook_status"] == "available"]
    upcoming_audio = [b for b in books if b["audiobook_status"] == "coming_soon"]
    future = ""
    if upcoming_audio:
        labels = ", ".join(e(b["title"]) + ((" (" + e(b["edition"]) + ")") if b["edition"] != "Novel" else "") for b in upcoming_audio)
        future = f'<section class="sf-cine-upcoming-audio"><h3>Future audiobook editions</h3><p>{labels} — not yet available to buy.</p></section>'
    parts = {
       "audiobooks.html": "\n".join(audio_card(b,b["slug"]==selected) for b in audio) + ("\n"+future if future else ""),
       "books.html": "\n".join(books_card(b) for b in books),
       "samples.html": "\n".join(sample_card(b) for b in books if b["book_status"] == "published"),
    }
    updates = {}
    for name,marker in MARKERS.items():
        source = (root/name).read_text(encoding="utf-8")
        rendered = count_copy(render_section(source,marker,parts[name]),name,books)
        if name == "audiobooks.html":
            rendered = sync_featured(rendered, next(b for b in books if b["slug"] == selected))
        updates[name] = rendered
    updates["home-v2.html"] = count_copy((root/"home-v2.html").read_text(encoding="utf-8"),"home-v2.html",books)
    return updates

def main():
    parser=argparse.ArgumentParser()
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--check",action="store_true")
    action.add_argument("--write",action="store_true")
    parser.add_argument("--root",type=Path,default=ROOT)
    args=parser.parse_args()
    root=args.root.resolve()
    catalog=json.loads((root/"data/storefront-catalog.json").read_text(encoding="utf-8"))
    result=build(root,catalog)
    changed=[]
    for name,text in result.items():
        path=root/name
        if text != path.read_text(encoding="utf-8"):
            changed.append(name)
            if args.write: path.write_text(text,encoding="utf-8")
    print("Catalog:",len(catalog["books"]),"titles |",sum(b["audiobook_status"]=="available" for b in catalog["books"]),"available audiobooks")
    print(("Updated: " if args.write else "OUT-OF-SYNC: ") + ", ".join(changed) if changed else "Generated pages in sync")
    return 1 if args.check and changed else 0

if __name__=="__main__":
    try: sys.exit(main())
    except (ValueError,OSError,json.JSONDecodeError) as exc:
        print("CATALOG ERROR:",exc,file=sys.stderr)
        sys.exit(2)
