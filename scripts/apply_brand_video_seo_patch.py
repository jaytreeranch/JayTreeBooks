#!/usr/bin/env python3
"""Apply narrowly scoped JayTree Books brand/video SEO fixes, never deploy."""
from pathlib import Path
import json
import re
import sys

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
SITE = "https://jaytreebooks.com"
VIDEO_FILE = "https://github.com/jaytreeranch/JayTreeBooks/releases/download/upcoming-novels-teaser-20261109/JayTree_Upcoming_Novels_Cinematic_Teaser_v1.mp4"
WATCH = SITE + "/upcoming-novels-teaser.html"
THUMB = SITE + "/images/social/previews/upcoming-books.jpg"
SCHEMA = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S | re.I)

def update(path, text):
    p = ROOT / path
    old = p.read_text(encoding="utf-8") if p.exists() else None
    if old != text:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        print("UPDATED", path)

def change_schema(path, predicate, change):
    src = (ROOT / path).read_text(encoding="utf-8")
    n = 0
    def patch(m):
        nonlocal n
        obj = json.loads(m.group(2))
        if predicate(obj):
            change(obj)
            n += 1
        return m.group(1) + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + m.group(3)
    out = SCHEMA.sub(patch, src)
    if n != 1:
        raise RuntimeError(f"{path}: expected 1 matching schema, found {n}")
    update(path, out)

def brand(obj):
    return isinstance(obj, dict) and obj.get("@type") == "Organization" and obj.get("name") == "JayTree Books"
def fix_brand(obj):
    obj["alternateName"] = "JayTreeBooks"
    obj.setdefault("description", "Independent publisher of psychological mysteries, suspense novels and audiobooks.")

for target in ("index.html", "home-v2.html"):
    change_schema(target, brand, fix_brand)

def is_trailer(obj):
    return obj.get("@type") == "VideoObject" and "Hollow Bell" in obj.get("name", "")
def fix_trailer(obj):
    # A YouTube watch page is NOT a contentUrl to video bytes.
    obj.pop("contentUrl", None)
    obj["embedUrl"] = "https://www.youtube-nocookie.com/embed/PmGQoyjYTDs"
    obj["creator"] = {"@id": SITE + "/#publisher"}
    obj["mainEntityOfPage"] = SITE + "/animated-series.html"
    obj["@id"] = SITE + "/animated-series.html#official-trailer"

change_schema("animated-series.html", is_trailer, fix_trailer)

publisher = {"@type": "Organization", "@id": SITE + "/#publisher", "name": "JayTree Books", "url": SITE + "/"}
video_json = {
    "@context": "https://schema.org",
    "@type": "VideoObject",
    "@id": WATCH + "#video",
    "name": "Three Upcoming JayTree Mysteries | Official Cinematic Teaser",
    "description": "A 27-second cinematic first look at Where Mercy Stood, The Fifth Copy and The Sixth Town from JayTree Books.",
    "thumbnailUrl": THUMB,
    "uploadDate": "2026-11-09",
    "duration": "PT27.2S",
    "contentUrl": VIDEO_FILE,
    "creator": publisher,
    "publisher": publisher,
    "mainEntityOfPage": WATCH,
}
schema_json = json.dumps(video_json, ensure_ascii=False, separators=(",", ":"))
page = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Three Upcoming Mystery Novels | Official Cinematic Teaser | JayTree Books</title>
<meta name="description" content="Watch the official 27-second JayTree Books cinematic teaser for Where Mercy Stood, The Fifth Copy and The Sixth Town.">
<meta name="robots" content="index,follow,max-image-preview:large,max-video-preview:-1">
<link rel="canonical" href="{WATCH}">
<meta property="og:type" content="video.other">
<meta property="og:url" content="{WATCH}">
<meta property="og:title" content="Upcoming JayTree Mysteries | Official Cinematic Teaser">
<meta property="og:description" content="Three new mysteries. One unsettling first look. Watch the approved cinematic teaser.">
<meta property="og:image" content="{THUMB}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{THUMB}">
<link rel="icon" href="/favicon.png">
<link rel="stylesheet" href="/cinematic-site-v2.css">
<script type="application/ld+json">{schema_json}</script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-PHE2JVV5P6');</script>
<script src="/tracking.js" defer></script>
<style>
body{{margin:0;background:#070d12;color:#f2ede5;font-family:system-ui,Arial,sans-serif}}
main{{max-width:1000px;margin:0 auto;padding:55px 20px 85px}}
a{{color:#e6c789}}a:focus-visible,video:focus-visible{{outline:3px solid #edc86f;outline-offset:5px}}
nav{{padding:24px max(20px,calc((100% - 1000px)/2));border-bottom:1px solid #493e2e}}
nav a{{margin-right:22px}}h1{{font-size:clamp(2rem,5vw,3.6rem);line-height:1.14}}
p{{line-height:1.7;color:#d7cfc3}}.eyebrow{{color:#c6a768;letter-spacing:.15em;text-transform:uppercase;font-size:.8rem}}
video{{width:100%;height:auto;aspect-ratio:16/9;background:#000;border:1px solid #5b4b30}}
.actions{{display:flex;gap:20px;flex-wrap:wrap;margin-top:24px}}footer{{padding:28px;text-align:center;border-top:1px solid #493e2e}}
</style>
</head>
<body>
<nav aria-label="Primary"><a href="/">JayTree Books</a><a href="/upcoming-books.html">Upcoming Novels</a><a href="/books.html">Books</a><a href="/samples.html">Samples</a></nav>
<main id="main">
<p class="eyebrow">Official JayTree Books video · 27 seconds</p>
<h1>Three mysteries. One unsettling first look.</h1>
<p>Watch the approved JayTree Books cinematic teaser introducing <em>Where Mercy Stood</em>, <em>The Fifth Copy</em> and <em>The Sixth Town</em>.</p>
<video controls playsinline preload="metadata" poster="/images/social/previews/upcoming-books.jpg" aria-label="Official JayTree Books upcoming novels cinematic teaser">
<source src="{VIDEO_FILE}" type="video/mp4">
<track kind="captions" src="/media/upcoming/teaser-en.vtt" srclang="en" label="English captions">
Your browser cannot play this video. <a href="{VIDEO_FILE}">View the teaser file</a>.
</video>
<div class="actions"><a href="/upcoming-books.html">Explore all three upcoming novels</a><a href="{VIDEO_FILE}">Open original video</a></div>
</main>
<footer>© 2026 JayTree Books · Independent mystery fiction</footer>
</body></html>
'''
# Preserve production-only analytics while reusing the approved teaser listener.
page = page.replace('<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6"></script>', '')
page = page.replace(
    "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-PHE2JVV5P6');</script>",
    '<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}if(location.hostname==="jaytreebooks.com"||location.hostname==="www.jaytreebooks.com"){const s=document.createElement("script");s.async=true;s.src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6";document.head.appendChild(s);gtag("js",new Date());gtag("config","G-PHE2JVV5P6");}</script>'
)
page = page.replace('<script src="/tracking.js" defer></script>', '<script src="/tracking.js" defer></script>\n<script src="/upcoming.js" defer></script>')
page = page.replace('<main id="main">', '<main id="main" data-upcoming-surface="landing">')
page = page.replace('<video controls', '<video data-upcoming-video="upcoming_novels_teaser_v1" controls')
for asset in ("images/social/previews/upcoming-books.jpg", "media/upcoming/teaser-en.vtt"):
    if not (ROOT / asset).is_file():
        raise RuntimeError("Missing approved site asset " + asset)
update("upcoming-novels-teaser.html", page)

upcoming_path = ROOT / "upcoming-books.html"
upcoming = upcoming_path.read_text(encoding="utf-8")
marker = '<section class="upcoming-teaser"'
if marker not in upcoming:
    raise RuntimeError("upcoming teaser section not found")
if 'href="upcoming-novels-teaser.html"' not in upcoming:
    section_start = upcoming.index(marker)
    section_end = upcoming.index("</section>", section_start)
    upcoming = upcoming[:section_end] + '<p class="upcoming-fineprint"><a href="upcoming-novels-teaser.html">Watch on the dedicated video page</a></p>\n  ' + upcoming[section_end:]
    update("upcoming-books.html", upcoming)

sitemap_path = ROOT / "sitemap.xml"
sitemap = sitemap_path.read_text(encoding="utf-8")
sitemap_item = '<url><loc>' + WATCH + '</loc><lastmod>2026-11-15</lastmod></url>'
if WATCH not in sitemap:
    insertion = '<url><loc>' + SITE + '/upcoming-books.html</loc><lastmod>2026-11-15</lastmod></url>'
    if insertion not in sitemap:
        raise RuntimeError("Could not locate teaser sitemap insertion point")
    sitemap = sitemap.replace(insertion, insertion + '\n  ' + sitemap_item, 1)
    update("sitemap.xml", sitemap)

generator_path = ROOT / "scripts/seo_content_cleanup.py"
generator = generator_path.read_text(encoding="utf-8")
source_item = '    ("upcoming-books.html", "upcoming-books.html"),'
new_item = '    ("upcoming-novels-teaser.html", "upcoming-novels-teaser.html"),'
if new_item not in generator:
    if source_item not in generator:
        raise RuntimeError("SEO sitemap generator layout changed")
    generator = generator.replace(source_item, source_item + '\n' + new_item, 1)
    update("scripts/seo_content_cleanup.py", generator)

entity_path = ROOT / "scripts/apply_entity_seo.py"
entity = entity_path.read_text(encoding="utf-8")
needle = '            value["@id"] = PUBLISHER_ID\n'
if 'value.setdefault("alternateName", "JayTreeBooks")' not in entity:
    if needle not in entity:
        raise RuntimeError("entity generator layout changed")
    entity = entity.replace(needle, needle + '            value.setdefault("alternateName", "JayTreeBooks")\n', 1)
    update("scripts/apply_entity_seo.py", entity)
print("BRAND_VIDEO_SEO_PATCH_COMPLETED")
