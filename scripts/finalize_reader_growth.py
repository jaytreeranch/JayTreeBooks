#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
APP_PATH = ROOT / "app.js"
INDEX_PATH = ROOT / "index.html"
STYLES_PATH = ROOT / "styles.css"
SITEMAP_PATH = ROOT / "sitemap.xml"
LEGACY_BOOK_PATH = ROOT / "book.html"
BOOKS_DIR = ROOT / "books"
CASE_FILES_PATH = ROOT / "case-files.html"
CASE_FILES_THANKS_PATH = ROOT / "case-files-thanks.html"
SITE = "https://www.JayTreeBooks.com"

CONFIG_RE = re.compile(
    r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;",
    re.DOTALL,
)

CASE_FILES_START = "<!-- JAYTREE_CASE_FILES_START -->"
CASE_FILES_END = "<!-- JAYTREE_CASE_FILES_END -->"
CASE_FILES_STYLE_MARKER = "/* JAYTREE_CASE_FILES */"


def load_config() -> dict:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    match = CONFIG_RE.search(text)
    if not match:
        raise RuntimeError("Could not parse config.js")
    return json.loads(match.group(1))


def save_config(config: dict) -> None:
    CONFIG_PATH.write_text(
        "window.JT = " + json.dumps(config, indent=2, ensure_ascii=False) + ";\n"
        "window.JAYTREE_CONFIG = window.JT;\n",
        encoding="utf-8",
    )


def ensure_newsletter_config(config: dict) -> None:
    newsletter = config.setdefault("newsletter", {})
    newsletter.setdefault("name", "JayTree Case Files")
    newsletter.setdefault("formAction", "https://formsubmit.co/jaytreebooks@gmail.com")
    newsletter.setdefault("thankYouUrl", f"{SITE}/case-files-thanks.html")


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

    if 'data-case-files-form' not in text:
        needle = '''  document.querySelectorAll("[data-social]").forEach(el => {
    el.addEventListener("click", () => track("social_visit", { platform: el.dataset.social || "" }));
  });
'''
        addition = needle + '''  document.querySelectorAll("[data-case-files-form]").forEach(form => {
    form.addEventListener("submit", () => track("case_files_signup_submit", { placement: form.dataset.placement || "unknown" }));
  });
'''
        if needle not in text:
            raise RuntimeError("Could not find social tracking block in app.js")
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


def case_files_form(config: dict, placement: str) -> str:
    newsletter = config["newsletter"]
    action = escape(newsletter["formAction"], quote=True)
    next_url = escape(newsletter["thankYouUrl"], quote=True)
    placement_value = escape(placement, quote=True)
    return f'''<form class="case-files-form" action="{action}" method="POST" data-case-files-form data-placement="{placement_value}">
  <input type="hidden" name="_subject" value="New JayTree Case Files signup">
  <input type="hidden" name="_next" value="{next_url}">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_url" value="{SITE}/case-files.html">
  <input type="hidden" name="list" value="JayTree Case Files">
  <input type="hidden" name="source" value="{placement_value}">
  <input type="hidden" name="_autoresponse" value="You're in the JayTree Case Files. Watch your inbox for new Mystery Challenge cases, clues, trailers, first-chapter reads, book news, and Kindle Unlimited promotions from JayTree Books. Visit JayTreeBooks.com anytime to enter the mystery.">
  <input class="case-files-honey" type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true">
  <div class="case-files-input-row">
    <label class="sr-only" for="case-files-email-{placement_value}">Email address</label>
    <input id="case-files-email-{placement_value}" type="email" name="email" autocomplete="email" inputmode="email" placeholder="Your email address" required>
    <button type="submit">Open the Case Files</button>
  </div>
  <label class="case-files-consent"><input type="checkbox" name="consent" value="Yes — JayTree Case Files email updates" required><span>Yes, send me JayTree Books emails about mystery challenges, books, trailers, first chapters, and promotions.</span></label>
  <p class="case-files-fineprint">No spam. You can unsubscribe at any time.</p>
</form>'''


def case_files_section(config: dict) -> str:
    return f'''{CASE_FILES_START}
<section class="case-files" id="case-files">
  <div class="wrap case-files-layout">
    <div class="case-files-copy">
      <div class="eyebrow">JayTree Case Files</div>
      <h2>Get the next mystery before the reveal.</h2>
      <p class="case-files-lead">Join the JayTree Books reader list for new Mystery Challenge cases, clue alerts, trailer premieres, first-chapter releases, book news, and Kindle Unlimited promotions.</p>
      <div class="case-files-benefits">
        <span>New case alerts</span><span>Clues & reveals</span><span>Book + KU updates</span>
      </div>
      <a class="case-files-detail-link" href="case-files.html">What are the JayTree Case Files? →</a>
    </div>
    <div class="case-files-panel">
      <div class="case-files-stamp">READER ACCESS</div>
      <h3>Enter your email. Join the case.</h3>
      <p>Be first in line when a new mystery, chapter, trailer, or reader promotion drops.</p>
      {case_files_form(config, "homepage")}
    </div>
  </div>
</section>
{CASE_FILES_END}'''


def patch_index(config: dict) -> None:
    text = INDEX_PATH.read_text(encoding="utf-8")
    section = case_files_section(config)
    pattern = re.compile(re.escape(CASE_FILES_START) + r".*?" + re.escape(CASE_FILES_END), re.DOTALL)
    if pattern.search(text):
        text = pattern.sub(lambda _: section, text)
    else:
        needle = '<section class="books" id="books">'
        if needle not in text:
            raise RuntimeError("Could not find books section in index.html")
        text = text.replace(needle, section + "\n\n\t\t" + needle, 1)

    if 'href="#case-files">Case Files</a>' not in text:
        text = re.sub(
            r'(<a\s+href="#challenge">Challenge</a>)',
            r'\1<a href="#case-files">Case Files</a>',
            text,
            count=1,
        )
    INDEX_PATH.write_text(text, encoding="utf-8")


def patch_styles() -> None:
    text = STYLES_PATH.read_text(encoding="utf-8")
    if CASE_FILES_STYLE_MARKER in text:
        return
    additions = r'''
/* JAYTREE_CASE_FILES */
.case-files{position:relative;overflow:hidden;background:linear-gradient(145deg,#0b1218,#101b23);border-top:1px solid var(--line);border-bottom:1px solid var(--line)}.case-files:before{content:"";position:absolute;inset:-30% 50% auto -15%;height:420px;background:radial-gradient(circle,rgba(200,161,90,.12),transparent 68%);pointer-events:none}.case-files-layout{position:relative;display:grid;grid-template-columns:1.05fr .95fr;gap:60px;align-items:center}.case-files-copy h2{font-size:clamp(2.7rem,5vw,4.8rem);margin:10px 0 18px;max-width:760px}.case-files-lead{max-width:690px;color:var(--muted);font-size:1.06rem}.case-files-benefits{display:flex;flex-wrap:wrap;gap:10px;margin:24px 0}.case-files-benefits span{padding:9px 12px;border:1px solid rgba(200,161,90,.35);font-size:.68rem;letter-spacing:.11em;text-transform:uppercase;color:var(--cream)}.case-files-detail-link{color:var(--gold);text-decoration:none;font-size:.83rem}.case-files-panel{padding:34px;border:1px solid rgba(200,161,90,.55);background:rgba(5,9,12,.62);box-shadow:0 28px 70px rgba(0,0,0,.34)}.case-files-stamp{display:inline-block;padding:7px 10px;border:1px solid var(--gold);color:var(--gold);font-size:.64rem;letter-spacing:.2em;transform:rotate(-1deg)}.case-files-panel h3{font-size:clamp(1.7rem,3vw,2.35rem);margin:18px 0 8px}.case-files-panel>p{color:var(--muted)}.case-files-form{margin-top:22px}.case-files-input-row{display:grid;grid-template-columns:1fr auto;gap:10px}.case-files-input-row input[type=email]{width:100%;min-width:0;padding:14px 16px;border:1px solid rgba(232,223,204,.28);background:#071016;color:var(--cream);font:inherit;outline:none}.case-files-input-row input[type=email]:focus{border-color:var(--gold)}.case-files-input-row button{padding:14px 18px;border:1px solid var(--gold);background:var(--gold);color:var(--ink);font:inherit;font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;cursor:pointer}.case-files-input-row button:hover{filter:brightness(1.08)}.case-files-consent{display:flex;gap:9px;align-items:flex-start;margin-top:14px;color:var(--muted);font-size:.72rem;line-height:1.45}.case-files-consent input{margin-top:3px;accent-color:#c8a15a}.case-files-fineprint{margin:8px 0 0;color:#7f8788;font-size:.68rem}.case-files-honey{position:absolute!important;left:-9999px!important;width:1px!important;height:1px!important;opacity:0!important}.sr-only{position:absolute!important;width:1px!important;height:1px!important;padding:0!important;margin:-1px!important;overflow:hidden!important;clip:rect(0,0,0,0)!important;white-space:nowrap!important;border:0!important}.case-files-page{min-height:75vh;padding-top:120px}.case-files-page .case-files-layout{align-items:start}.case-files-page-art{position:relative}.case-files-page-art img{width:100%;display:block;border:1px solid rgba(200,161,90,.35);box-shadow:0 30px 75px rgba(0,0,0,.4)}.case-files-page-art:after{content:"CASE FILE ACCESS";position:absolute;right:20px;bottom:20px;padding:9px 12px;border:2px solid rgba(200,161,90,.82);color:var(--gold);font-size:.68rem;letter-spacing:.18em;background:rgba(5,9,12,.78);transform:rotate(-2deg)}.case-files-points{display:grid;gap:12px;margin:26px 0}.case-files-point{padding:14px 16px;border-left:2px solid var(--gold);background:rgba(255,255,255,.025)}.case-files-point strong{display:block;color:var(--cream);margin-bottom:3px}.case-files-point span{color:var(--muted);font-size:.88rem}.case-files-thanks{text-align:center;max-width:760px;margin:0 auto}.case-files-thanks .case-files-stamp{margin-bottom:20px}.case-files-thanks h1{font-size:clamp(3.1rem,7vw,6rem);margin:0 0 18px}.case-files-thanks p{color:var(--muted);font-size:1.05rem}.case-files-thanks .hero-actions{justify-content:center;margin-top:28px}
@media(max-width:850px){.case-files-layout{grid-template-columns:1fr;gap:34px}.case-files-panel{padding:24px}.case-files-input-row{grid-template-columns:1fr}.case-files-input-row button{width:100%}.case-files-page{padding-top:90px}}
'''
    STYLES_PATH.write_text(text.rstrip() + "\n" + additions.strip() + "\n", encoding="utf-8")


def analytics_head(config: dict) -> str:
    ga4 = escape(str(config.get("ga4") or ""), quote=True)
    if not ga4:
        return ""
    return f'''<script async src="https://www.googletagmanager.com/gtag/js?id={ga4}"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','{ga4}');</script>'''


def generate_case_files_page(config: dict) -> None:
    canonical = f"{SITE}/case-files.html"
    description = "Join the JayTree Case Files reader list for Mystery Challenge case alerts, clues, book trailers, first chapters, new releases, and Kindle Unlimited promotions."
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>JayTree Case Files — Reader Email List | JayTree Books</title>
<meta name="description" content="{escape(description, quote=True)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<meta property="og:title" content="JayTree Case Files — Get the Next Mystery">
<meta property="og:description" content="{escape(description, quote=True)}">
<meta property="og:image" content="{SITE}/images/mystery-challenge-case-001.webp">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="JayTree Case Files — Get the Next Mystery">
<meta name="twitter:description" content="{escape(description, quote=True)}">
<meta name="twitter:image" content="{SITE}/images/mystery-challenge-case-001.webp">
{analytics_head(config)}
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="nav"><div class="nav-inner"><a class="brand" href="index.html">JAYTREE BOOKS</a><button class="menu-toggle" aria-label="Open menu">☰</button><nav class="nav-links"><a href="index.html#books">Books</a><a href="index.html#challenge">Challenge</a><a href="case-files.html">Case Files</a><a href="index.html#follow">Follow</a></nav></div></header>
<main class="case-files-page">
<section class="case-files">
  <div class="wrap case-files-layout">
    <div class="case-files-copy">
      <div class="eyebrow">JayTree Case Files</div>
      <h1>Get the next mystery before the reveal.</h1>
      <p class="case-files-lead">Join the JayTree Books reader list and get a direct line to new mystery content—without depending on an algorithm to show it to you.</p>
      <div class="case-files-points">
        <div class="case-files-point"><strong>Mystery Challenge case alerts</strong><span>Know when a new case, clue, poll, or reveal goes live.</span></div>
        <div class="case-files-point"><strong>First chapters & cinematic trailers</strong><span>See new reading samples, book trailers, and audiobook previews.</span></div>
        <div class="case-files-point"><strong>Book and Kindle Unlimited news</strong><span>Get release updates and reader promotions from JayTree Books.</span></div>
      </div>
      <div class="case-files-panel">
        <div class="case-files-stamp">READER ACCESS</div>
        <h3>Enter the Case Files.</h3>
        <p>One email address. No unnecessary profile questions.</p>
        {case_files_form(config, "case-files-page")}
      </div>
    </div>
    <div class="case-files-page-art"><img src="images/mystery-challenge-case-001.webp" alt="JayTree Books Mystery Challenge Case File 001" decoding="async" fetchpriority="high"></div>
  </div>
</section>
</main>
<footer><div class="footer-brand">JAYTREE BOOKS</div><p>Stories That Stay.</p><div><a href="index.html#books">Books</a> · <a href="index.html#challenge">Challenge</a> · <a href="case-files.html">Case Files</a></div><small>© <span id="year"></span> JayTree Books. All rights reserved.</small></footer>
<script>
document.getElementById('year').textContent=new Date().getFullYear();
document.querySelector('.menu-toggle')?.addEventListener('click',function(){{document.querySelector('.nav')?.classList.toggle('open')}});
document.querySelectorAll('[data-case-files-form]').forEach(function(form){{form.addEventListener('submit',function(){{if(typeof gtag==='function')gtag('event','case_files_signup_submit',{{placement:form.dataset.placement||'case-files-page'}})}})}});
if(typeof gtag==='function')gtag('event','case_files_signup_view',{{placement:'case-files-page'}});
</script>
</body>
</html>
'''
    CASE_FILES_PATH.write_text(html, encoding="utf-8")


def generate_thanks_page(config: dict) -> None:
    html = f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow">
<title>You're in the Case Files | JayTree Books</title>
<meta name="description" content="Thanks for joining the JayTree Case Files reader email list.">
{analytics_head(config)}
<link rel="stylesheet" href="styles.css">
</head>
<body>
<header class="nav"><div class="nav-inner"><a class="brand" href="index.html">JAYTREE BOOKS</a></div></header>
<main class="case-files-page"><section class="intro"><div class="wrap case-files-thanks"><div class="case-files-stamp">ACCESS REQUEST RECEIVED</div><h1>You're in the Case Files.</h1><p>Your signup was submitted. Watch your inbox for JayTree Books mysteries, clues, first chapters, trailers, book news, and reader promotions.</p><div class="hero-actions"><a class="cta solid" href="index.html#challenge">Enter the Mystery Challenge</a><a class="cta" href="index.html#books">Explore the Books</a></div></div></section></main>
<footer><div class="footer-brand">JAYTREE BOOKS</div><p>Stories That Stay.</p><small>© <span id="year"></span> JayTree Books. All rights reserved.</small></footer>
<script>document.getElementById('year').textContent=new Date().getFullYear();if(typeof gtag==='function')gtag('event','case_files_signup_complete',{{source:'formsubmit'}});</script>
</body>
</html>
'''
    CASE_FILES_THANKS_PATH.write_text(html, encoding="utf-8")


def patch_sitemap() -> None:
    text = SITEMAP_PATH.read_text(encoding="utf-8")
    case_files_url = f"{SITE}/case-files.html"
    if case_files_url in text:
        return
    entry = f"  <url><loc>{case_files_url}</loc></url>\n"
    text = text.replace("</urlset>", entry + "</urlset>")
    SITEMAP_PATH.write_text(text, encoding="utf-8")


def main() -> int:
    config = load_config()
    ensure_newsletter_config(config)
    save_config(config)
    patch_app()
    patch_legacy_book_page()
    patch_static_book_pages(config)
    patch_index(config)
    patch_styles()
    generate_case_files_page(config)
    generate_thanks_page(config)
    patch_sitemap()
    print("Reader-growth final polish and JayTree Case Files signup complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
