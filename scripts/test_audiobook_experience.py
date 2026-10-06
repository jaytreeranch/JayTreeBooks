from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BOOKS = {
    "book-1-sample.html": "second-draft",
    "book-2-sample.html": "the-hollow-year",
    "book-3-sample.html": "the-hollow-bell",
    "book-4-sample.html": "the-absconding",
    "book-5-sample.html": "the-correction",
}
NARRATORS = {
    "vivian-arlow": "Vivian Arlow",
    "helena-corven": "Helena Corven",
    "grant-orlin": "Grant Orlin",
    "edwin-lorren": "Edwin Lorren",
}

errors = []

for page_name, slug in BOOKS.items():
    page = (ROOT / "audio" / page_name)
    if not page.exists():
        errors.append(f"missing page: {page}")
        continue
    text = page.read_text(encoding="utf-8")
    for name in NARRATORS.values():
        if name not in text:
            errors.append(f"{page_name}: missing narrator {name}")
    if "Recommended Narrator" not in text:
        errors.append(f"{page_name}: missing Recommended Narrator badge")
    if "Immersive Experience" not in text or "Coming Soon" not in text:
        errors.append(f"{page_name}: missing Immersive Experience coming-soon card")
    if text.count('<script src="/pwa.js" defer></script>') != 1:
        errors.append(f"{page_name}: expected exactly one pwa.js script")
    if text.count("JAYTREE_PWA_HEAD_START") != 1 or text.count("JAYTREE_PWA_SCRIPT_START") != 1:
        errors.append(f"{page_name}: missing or duplicated standard PWA markers")
    if "Opening credits • Chapter One • Closing credits" not in text:
        errors.append(f"{page_name}: missing preview sequence disclosure")

    for narrator_slug in NARRATORS:
        audio = ROOT / "audio" / "narrator-previews" / slug / f"{narrator_slug}.mp3"
        if not audio.exists() or audio.stat().st_size < 100_000:
            errors.append(f"missing/too-small preview: {audio.relative_to(ROOT)}")

home = (ROOT / "index.html").read_text(encoding="utf-8")
if "Choose Your Narrator" not in home:
    errors.append("index.html: missing Choose Your Narrator messaging")
if "Immersive Experience" not in home:
    errors.append("index.html: missing Immersive Experience messaging")

css = ROOT / "audio" / "audiobook-experience.css"
if not css.exists():
    errors.append("missing audiobook-experience.css")
else:
    css_text = css.read_text(encoding="utf-8")
    if "width:min(calc(100% - 28px),1180px)" not in css_text:
        errors.append("audiobook-experience.css: mobile page width must use valid calc()")
    if ".narrator-card audio{width:100%;max-width:100%;min-width:0" not in css_text:
        errors.append("audiobook-experience.css: native audio controls must not force horizontal overflow")
    if "grid-template-columns:1fr;gap:22px;align-items:start;text-align:center" not in css_text:
        errors.append("audiobook-experience.css: mobile hero must stack to avoid narrow-column overflow")
    if "flex-wrap:wrap;justify-content:center" not in css_text:
        errors.append("audiobook-experience.css: preview sequence must wrap on mobile")
js = ROOT / "audio" / "audiobook-experience.js"
if not js.exists():
    errors.append("missing audiobook-experience.js")

if errors:
    print("AUDIOBOOK_EXPERIENCE_FAIL")
    for error in errors:
        print(" -", error)
    sys.exit(1)

print("AUDIOBOOK_EXPERIENCE_PASS")
print("5 pages; 4 narrators each; 20 preview files; recommended + immersive UI present")
