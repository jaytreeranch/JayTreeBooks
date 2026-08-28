#!/usr/bin/env python3
from __future__ import annotations

import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
APP = ROOT / "app.js"
STYLES = ROOT / "styles.css"
VIDEO_JS = ROOT / "video-lite.js"

TITLE = "JayTree Books | Mystery Thrillers, Kindle Unlimited & Mystery Challenges"
DESCRIPTION = (
    "Discover JayTree Books mysteries and psychological thrillers. Read first chapters, "
    "watch trailers, solve Mystery Challenges, and find Kindle Unlimited reads."
)
SHARE_IMAGE = "https://www.JayTreeBooks.com/images/jaytree-books-challenge.png"
POLISH_MARKER = "/* JAYTREE_2026_CONVERSION_POLISH */"
CHAPTER_MARKER = "/* JAYTREE_2026_READER_ACCESSIBILITY */"
CASE_START = "<!-- JAYTREE_CASE_FILES_START -->"
CASE_END = "<!-- JAYTREE_CASE_FILES_END -->"
SOCIAL_START = "<!-- JAYTREE_SOCIAL_FOLLOW_START -->"
SOCIAL_END = "<!-- JAYTREE_SOCIAL_FOLLOW_END -->"


def replace_first(text: str, pattern: str, replacement: str, *, flags: int = 0) -> str:
    new, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    return new if count else text


def lite_markup(video_id: str, title: str) -> str:
    safe = escape(title, quote=True)
    return (
        '<div class="video-lite-inner">'
        f'<button class="video-lite" type="button" data-youtube-id="{video_id}" '
        f'data-title="{safe}" aria-label="Play {safe}">'
        f'<img src="https://i.ytimg.com/vi/{video_id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">'
        '<span class="video-lite-play" aria-hidden="true">▶</span>'
        '<span class="video-lite-label">Play video</span>'
        '</button>'
        f'<a class="video-lite-fallback" href="https://www.youtube.com/watch?v={video_id}" '
        'target="_blank" rel="noopener">Open on YouTube ↗</a>'
        '</div>'
    )


IFRAME_RE = re.compile(
    r'<iframe(?=[^>]*\bsrc="https://www\.youtube-nocookie\.com/embed/([^"?]+)[^"]*")'
    r'(?=[^>]*\btitle="([^"]+)")[^>]*>\s*</iframe>',
    re.IGNORECASE,
)


def replace_youtube_iframes(text: str) -> str:
    return IFRAME_RE.sub(lambda m: lite_markup(m.group(1), m.group(2)), text)


def add_legal_footer(text: str, prefix: str = "") -> str:
    match = re.search(r'<footer>.*?</footer>', text, flags=re.DOTALL)
    if not match:
        return text
    footer = match.group(0)
    if f'{prefix}privacy.html' in footer and f'{prefix}terms.html' in footer:
        return text
    legal = f'<a href="{prefix}privacy.html">Privacy</a> · <a href="{prefix}terms.html">Terms</a>'
    if 'class="footer-links"' in footer:
        footer = re.sub(
            r'(<div class="footer-links">.*?)(</div>)',
            rf'\1 · {legal}\2',
            footer,
            count=1,
            flags=re.DOTALL,
        )
    elif re.search(r'<div>.*?</div><small>', footer, flags=re.DOTALL):
        footer = re.sub(
            r'(<div>.*?)(</div><small>)',
            rf'\1 · {legal}\2',
            footer,
            count=1,
            flags=re.DOTALL,
        )
    else:
        footer = footer.replace('</footer>', f'<div class="footer-links">{legal}</div></footer>')
    return text[: match.start()] + footer + text[match.end() :]


def wrap_section(text: str, section_re: str, start: str, end: str) -> str:
    if start in text:
        return text
    match = re.search(section_re, text, flags=re.DOTALL)
    if not match:
        return text
    block = f"{start}\n{match.group(0)}\n{end}"
    return text[: match.start()] + block + text[match.end() :]


def patch_index() -> None:
    text = INDEX.read_text(encoding="utf-8")
    text = replace_first(text, r'<title>.*?</title>', f'<title>{TITLE}</title>', flags=re.DOTALL)
    text = replace_first(
        text,
        r'<meta name="description" content="[^"]*">',
        f'<meta name="description" content="{DESCRIPTION}">',
    )
    if '<link rel="canonical" href="https://www.JayTreeBooks.com/">' not in text:
        text = text.replace(
            f'<meta name="description" content="{DESCRIPTION}">',
            f'<meta name="description" content="{DESCRIPTION}">\n<link rel="canonical" href="https://www.JayTreeBooks.com/">',
            1,
        )
    text = replace_first(text, r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{TITLE}">')
    text = replace_first(text, r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{DESCRIPTION}">')
    text = replace_first(text, r'<meta property="og:image" content="[^"]*">', f'<meta property="og:image" content="{SHARE_IMAGE}">')
    text = replace_first(text, r'<meta property="og:image:alt" content="[^"]*">', '<meta property="og:image:alt" content="JayTree Books mystery challenge artwork">')
    text = replace_first(text, r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{TITLE}">')
    text = replace_first(text, r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{DESCRIPTION}">')
    text = replace_first(text, r'<meta name="twitter:image" content="[^"]*">', f'<meta name="twitter:image" content="{SHARE_IMAGE}">')
    if '<meta name="twitter:image:alt"' not in text:
        text = text.replace(
            f'<meta name="twitter:image" content="{SHARE_IMAGE}">',
            f'<meta name="twitter:image" content="{SHARE_IMAGE}">\n<meta name="twitter:image:alt" content="JayTree Books mystery challenge artwork">',
            1,
        )
    if '<meta property="og:site_name"' not in text:
        text = text.replace(
            '<meta property="og:type" content="website">',
            '<meta property="og:type" content="website">\n<meta property="og:site_name" content="JayTree Books">',
            1,
        )

    nav = '''<nav class="nav-links">
                <a href="#books">Books</a>
                <a href="#challenge">Challenge</a>
                <a href="#case-files">Case Files</a>
                <a href="#audiobooks">Audiobooks</a>
                <a href="#youtube">YouTube</a>
                <a href="#about">About</a>
                <a class="nav-cta" href="#books">Start Reading</a>
            </nav>'''
    text = replace_first(text, r'<nav class="nav-links">.*?</nav>', nav, flags=re.DOTALL)
    text = text.replace('Preview the atmosphere, then continue the story on Audible.', 'Hear a sample or watch a chapter reading. Full audiobook editions are coming soon.')
    text = text.replace('Read the first chapter. Hear the audiobook. Watch the story', 'Read the first chapter. Hear a sample. Watch the story')

    if 'id="kindle-unlimited"' not in text:
        hero = re.search(r'<section class="hero">.*?</section>', text, flags=re.DOTALL)
        if hero:
            banner = '''

<section class="ku-home-banner" id="kindle-unlimited">
  <div class="wrap ku-home-inner">
    <div>
      <div class="eyebrow">Kindle Unlimited</div>
      <h2>Five mysteries. Read them all with Kindle Unlimited.</h2>
      <p>Every current JayTree Books title is available to Kindle Unlimited members at no additional cost. Choose a mystery, read Chapter One here, then continue on Kindle.</p>
    </div>
    <div class="ku-home-actions">
      <a class="cta solid" href="#books" data-track="ku_home_choose">Choose Your Mystery</a>
      <a class="cta" href="https://www.amazon.com/stores/JayTree-Books/author/B0HG41STKM" target="_blank" rel="noopener" data-track="ku_home_amazon">Browse JayTree Books on Amazon</a>
    </div>
  </div>
</section>'''
            text = text[: hero.end()] + banner + text[hero.end() :]

    text = replace_youtube_iframes(text)
    text = add_legal_footer(text)
    text = text.replace('<button class="menu-toggle" aria-label="Menu">', '<button class="menu-toggle" aria-label="Menu" aria-expanded="false">')
    text = text.replace('<button class="menu-toggle" aria-label="Open menu">', '<button class="menu-toggle" aria-label="Open menu" aria-expanded="false">')
    text = wrap_section(text, r'<section class="case-files" id="case-files">.*?</section>', CASE_START, CASE_END)
    text = wrap_section(text, r'<section class="social-follow" id="follow">.*?</section>', SOCIAL_START, SOCIAL_END)
    if '<script src="video-lite.js"></script>' not in text:
        text = text.replace('<script src="config.js"></script>', '<script src="video-lite.js"></script>\n\t<script src="config.js"></script>', 1)
    INDEX.write_text(text, encoding="utf-8")


def patch_app() -> None:
    text = APP.read_text(encoding="utf-8")
    if 'class="video-lite-inner"' not in text.split('function externalButton', 1)[0]:
        function = '''function youtubeEmbed(url, title) {
  const id = youtubeIdFromUrl(url);
  if (!id) return "";
  const safeTitle = String(title || "YouTube video")
    .replace(/&/g, "&amp;")
    .replace(/"/g, "&quot;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
  return `<div class="video-lite-inner">
    <button class="video-lite" type="button" data-youtube-id="${id}" data-title="${safeTitle}" aria-label="Play ${safeTitle}">
      <img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">
      <span class="video-lite-play" aria-hidden="true">▶</span>
      <span class="video-lite-label">Play video</span>
    </button>
    <a class="video-lite-fallback" href="https://www.youtube.com/watch?v=${id}" target="_blank" rel="noopener">Open on YouTube ↗</a>
  </div>`;
}'''
        text = replace_first(text, r'function youtubeEmbed\(url, title\) \{.*?\n\}', function, flags=re.DOTALL)
    text = text.replace('href="book.html?book=${featured.slug}"', 'href="books/${featured.slug}.html"')
    if '[data-event]' not in text:
        social = re.search(
            r'(\s*document\.querySelectorAll\("\[data-social\]"\)\.forEach\(el => \{\s*el\.addEventListener\("click", \(\) => track\("social_visit", \{ platform: el\.dataset\.social \|\| "" \}\)\);\s*\}\);)',
            text,
        )
        if social:
            event_block = '''
  document.querySelectorAll("[data-event]").forEach(el => {
    el.addEventListener("click", () => track(el.dataset.event, { book: el.dataset.book || "" }));
  });'''
            text = text[: social.end()] + event_block + text[social.end() :]
    APP.write_text(text, encoding="utf-8")


def write_video_loader() -> None:
    VIDEO_JS.write_text('''(() => {
  document.addEventListener("click", event => {
    const toggle = event.target.closest(".menu-toggle");
    if (toggle) {
      requestAnimationFrame(() => {
        const nav = toggle.closest(".nav");
        toggle.setAttribute("aria-expanded", nav?.classList.contains("open") ? "true" : "false");
      });
    }

    const navLink = event.target.closest(".nav-links a");
    if (navLink) {
      const nav = navLink.closest(".nav");
      nav?.classList.remove("open");
      nav?.querySelector(".menu-toggle")?.setAttribute("aria-expanded", "false");
    }

    const fallback = event.target.closest(".video-lite-fallback");
    if (fallback && typeof gtag === "function") {
      gtag("event", "video_youtube_fallback", { youtube_url: fallback.href });
    }

    const button = event.target.closest(".video-lite");
    if (!button) return;
    const id = button.dataset.youtubeId;
    if (!id) return;
    if (typeof gtag === "function") {
      gtag("event", "video_play", { youtube_id: id, video_title: button.dataset.title || "" });
    }

    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?rel=0&playsinline=1&autoplay=1`;
    iframe.title = button.dataset.title || "YouTube video";
    iframe.loading = "lazy";
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    iframe.setAttribute("frameborder", "0");
    button.replaceWith(iframe);
  });
})();
''', encoding="utf-8")


def patch_styles() -> None:
    text = STYLES.read_text(encoding="utf-8")
    if POLISH_MARKER in text:
        return
    additions = r'''
/* JAYTREE_2026_CONVERSION_POLISH */
.ku-home-banner{padding:42px 24px;background:linear-gradient(90deg,rgba(200,161,90,.13),rgba(12,20,26,.98),rgba(200,161,90,.08));border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.ku-home-inner{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:42px;align-items:center}.ku-home-banner h2{font-size:clamp(2rem,4vw,3.35rem);margin:8px 0 12px}.ku-home-banner p{max-width:760px;margin:0;color:var(--muted)}.ku-home-actions{display:flex;gap:10px;flex-wrap:wrap;justify-content:flex-end;max-width:390px}
.video-lite-inner{position:relative;width:100%;height:100%;min-height:inherit;background:#05080a;overflow:hidden}.video-lite-inner>iframe{width:100%;height:100%;display:block;border:0}.video-lite{position:absolute;inset:0;width:100%;height:100%;padding:0;border:0;background:#05080a;color:var(--cream);cursor:pointer;overflow:hidden;font:inherit}.video-lite img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block;opacity:.8;transition:transform .3s ease,opacity .3s ease}.video-lite:before{content:"";position:absolute;inset:0;z-index:1;background:linear-gradient(180deg,rgba(0,0,0,.04),rgba(0,0,0,.48))}.video-lite:hover img{transform:scale(1.025);opacity:.92}.video-lite-play{position:absolute;z-index:2;left:50%;top:50%;transform:translate(-50%,-50%);display:grid;place-items:center;width:72px;height:72px;border:1px solid rgba(232,223,204,.72);border-radius:50%;background:rgba(8,13,18,.82);color:var(--gold);font-family:Arial,sans-serif;font-size:1.8rem;box-shadow:0 12px 38px rgba(0,0,0,.45)}.video-lite-label{position:absolute;z-index:2;left:16px;bottom:15px;text-transform:uppercase;letter-spacing:.13em;font-size:.67rem;color:#f1eadc;text-shadow:0 2px 8px #000}.video-lite-fallback{position:absolute;z-index:3;right:12px;bottom:10px;padding:7px 9px;background:rgba(8,13,18,.88);border:1px solid rgba(200,161,90,.48);color:var(--gold)!important;text-decoration:none;text-transform:uppercase;letter-spacing:.08em;font-size:.58rem!important}
a:focus-visible,button:focus-visible{outline:2px solid var(--gold);outline-offset:4px}.cover:focus-visible,.related-book-link:focus-visible{outline-offset:6px}
@media(max-width:800px){.ku-home-inner{grid-template-columns:1fr;text-align:center;gap:24px}.ku-home-banner p{margin-left:auto;margin-right:auto}.ku-home-actions{justify-content:center;max-width:none}.video-lite-play{width:62px;height:62px;font-size:1.5rem}.video-lite-fallback{font-size:.53rem!important}}
'''
    STYLES.write_text(text.rstrip() + "\n\n" + additions.strip() + "\n", encoding="utf-8")


def patch_generated_pages() -> None:
    for path in sorted((ROOT / "books").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        text = replace_youtube_iframes(text)
        text = add_legal_footer(text, "../")
        text = text.replace('<button class="menu-toggle" aria-label="Open menu">', '<button class="menu-toggle" aria-label="Open menu" aria-expanded="false">')
        if '<script src="../video-lite.js"></script>' not in text:
            text = text.replace('</footer>', '</footer>\n<script src="../video-lite.js"></script>', 1)
        path.write_text(text, encoding="utf-8")

    generic = ROOT / "book.html"
    if generic.exists():
        text = generic.read_text(encoding="utf-8")
        text = add_legal_footer(text)
        text = text.replace('<button class="menu-toggle" aria-label="Open menu">', '<button class="menu-toggle" aria-label="Open menu" aria-expanded="false">')
        if '<script src="video-lite.js"></script>' not in text:
            text = text.replace('<script src="config.js"></script>', '<script src="video-lite.js"></script>\n  <script src="config.js"></script>', 1)
        generic.write_text(text, encoding="utf-8")

    for filename in ("case-files.html", "case-files-thanks.html"):
        path = ROOT / filename
        if not path.exists():
            continue
        text = add_legal_footer(path.read_text(encoding="utf-8"))
        text = text.replace('<button class="menu-toggle" aria-label="Open menu">', '<button class="menu-toggle" aria-label="Open menu" aria-expanded="false">')
        path.write_text(text, encoding="utf-8")


def patch_chapters() -> None:
    extra = '''
/* JAYTREE_2026_READER_ACCESSIBILITY */
p:first-of-type::first-letter,.drop-cap::first-letter{color:#c8a15a}
a:focus-visible{outline:2px solid #c8a15a;outline-offset:4px}
'''
    for path in sorted((ROOT / "chapters").glob("book-*-first-chapter.html")):
        text = path.read_text(encoding="utf-8").replace("Jaytree Books", "JayTree Books")
        if CHAPTER_MARKER not in text:
            text = text.replace('</style>', extra + '\n</style>', 1)
        path.write_text(text, encoding="utf-8")


def verify() -> None:
    index = INDEX.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    assert TITLE in index
    assert '<link rel="canonical" href="https://www.JayTreeBooks.com/">' in index
    assert 'Five mysteries. Read them all with Kindle Unlimited.' in index
    assert index.index('id="kindle-unlimited"') < index.index('id="books"')
    assert 'continue the story on Audible' not in index
    assert '<script src="video-lite.js"></script>' in index
    assert 'privacy.html' in index and 'terms.html' in index
    assert CASE_START in index and SOCIAL_START in index
    assert 'href="books/${featured.slug}.html"' in app
    assert '[data-event]' in app
    assert 'video-lite-inner' in app
    assert VIDEO_JS.exists()
    for path in sorted((ROOT / "books").glob("*.html")):
        text = path.read_text(encoding="utf-8")
        assert 'src="https://www.youtube-nocookie.com/embed/' not in text
        assert 'video-lite' in text and '../video-lite.js' in text
        assert '../privacy.html' in text and '../terms.html' in text
    for path in sorted((ROOT / "chapters").glob("book-*-first-chapter.html")):
        text = path.read_text(encoding="utf-8")
        assert 'Jaytree Books' not in text
        assert CHAPTER_MARKER in text


def main() -> int:
    patch_index()
    patch_app()
    write_video_loader()
    patch_styles()
    patch_generated_pages()
    patch_chapters()
    verify()
    print("Applied durable JayTreeBooks conversion, SEO, video, legal, and accessibility improvements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
