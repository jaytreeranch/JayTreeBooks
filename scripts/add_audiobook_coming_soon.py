#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "books"
APP_PATH = ROOT / "app.js"
STYLES_PATH = ROOT / "styles.css"

MARKER = "JAYTREE_AUDIOBOOK_DIRECT_COMING_SOON"
HEADLINE_STYLE_MARKER = "JAYTREE_CASE_FILES_HEADLINE_SIZE"
CALLOUT = f'''<!-- {MARKER} -->
<div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">
  <div>
    <span class="ku-kicker">Direct from JayTree Books</span>
    <strong>Full Audiobook — Coming Soon</strong>
    <small>Join JayTree Case Files and we’ll let you know when full audiobook editions are available to purchase directly from JayTreeBooks.com.</small>
  </div>
  <a class="cta solid ku-button" href="../case-files.html" data-track="audiobook_case_files">Join JayTree Case Files</a>
</div>'''

HEADLINE_STYLE = f'''/* {HEADLINE_STYLE_MARKER} */
.case-files-page .case-files-copy h1{{
  font-size:clamp(2.2rem,2.8vw,3rem);
  line-height:1.02;
  letter-spacing:.01em;
  text-transform:none;
  max-width:650px;
  margin:10px 0 22px;
}}
@media(max-width:850px){{
  .case-files-page .case-files-copy h1{{
    font-size:clamp(2rem,8vw,2.6rem);
    line-height:1.04;
  }}
}}'''


def patch_book_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        pattern = re.compile(
            rf'<!-- {MARKER} -->\s*<div class="ku-callout audiobook-coming-soon".*?</div>\s*</div>',
            re.S,
        )
        if pattern.search(text):
            text = pattern.sub(CALLOUT, text, count=1)
            path.write_text(text, encoding="utf-8")
        return

    patterns = [
        re.compile(r'(<section class="book-section" id="listen">.*?)(</section>)', re.S),
        re.compile(r'(<section class="book-section"[^>]*>\s*<div class="eyebrow">Listen</div>.*?)(</section>)', re.S),
    ]

    for pattern in patterns:
        match = pattern.search(text)
        if match:
            replacement = match.group(1).rstrip() + "\n" + CALLOUT + "\n" + match.group(2)
            path.write_text(text[:match.start()] + replacement + text[match.end():], encoding="utf-8")
            print(f"Added direct audiobook coming-soon callout: {path.relative_to(ROOT)}")
            return

    raise RuntimeError(f"Could not find audiobook/listen section in {path.relative_to(ROOT)}")


def patch_app_js() -> None:
    text = APP_PATH.read_text(encoding="utf-8")

    text = text.replace(
        '>Audiobook & Reading</a>',
        '>Full Audiobook — Coming Soon</a>',
    )

    text = re.sub(
        r'\n\s*\$\{externalButton\(b\.audibleUrl,\s*"Listen on Audible",\s*"audible",\s*b\.slug\)\}',
        '',
        text,
    )
    text = re.sub(
        r'\n\s*\$\{externalButton\(b\.audibleUrl,\s*"Full Audiobook on Audible",\s*"audible",\s*b\.slug\)\}',
        '',
        text,
    )

    callout_js = f'''      <!-- {MARKER} -->\n      <div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">\n        <div>\n          <span class="ku-kicker">Direct from JayTree Books</span>\n          <strong>Full Audiobook — Coming Soon</strong>\n          <small>Join JayTree Case Files and we’ll let you know when full audiobook editions are available to purchase directly from JayTreeBooks.com.</small>\n        </div>\n        <a class="cta solid ku-button" href="case-files.html" data-track="audiobook_case_files" data-book="${{b.slug}}">Join JayTree Case Files</a>\n      </div>'''

    if MARKER in text:
        pattern = re.compile(
            rf'\s*<!-- {MARKER} -->\s*<div class="ku-callout audiobook-coming-soon".*?</div>\s*</div>',
            re.S,
        )
        if pattern.search(text):
            text = pattern.sub("\n" + callout_js, text, count=1)
    else:
        needle = '''      <p class="section-copy">Play the website audio sample${b.audiobookYoutubeUrl ? " or watch the YouTube chapter reading" : ""}.</p>\n      ${audiobookVideo}'''
        replacement = needle + "\n" + callout_js
        if needle not in text:
            raise RuntimeError("Could not find legacy audiobook section in app.js")
        text = text.replace(needle, replacement, 1)

    APP_PATH.write_text(text, encoding="utf-8")
    print("Updated legacy audiobook page messaging in app.js")


def patch_case_files_headline_styles() -> None:
    text = STYLES_PATH.read_text(encoding="utf-8")
    block_pattern = re.compile(
        rf'/\* {HEADLINE_STYLE_MARKER} \*/.*?(?=/\*|\Z)',
        re.S,
    )
    if block_pattern.search(text):
        text = block_pattern.sub(HEADLINE_STYLE + "\n", text, count=1)
    else:
        text = text.rstrip() + "\n\n" + HEADLINE_STYLE + "\n"
    STYLES_PATH.write_text(text, encoding="utf-8")
    print("Reduced Case Files page headline size")


def main() -> None:
    pages = sorted(BOOKS_DIR.glob("*.html"))
    if not pages:
        raise RuntimeError("No generated book pages found")
    for page in pages:
        patch_book_page(page)
    patch_app_js()
    patch_case_files_headline_styles()


if __name__ == "__main__":
    main()
