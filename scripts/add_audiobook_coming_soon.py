#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOKS_DIR = ROOT / "books"
APP_PATH = ROOT / "app.js"

MARKER = "JAYTREE_AUDIOBOOK_DIRECT_COMING_SOON"
CALLOUT = f'''<!-- {MARKER} -->
<div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">
  <div>
    <span class="ku-kicker">Direct from JayTree Books</span>
    <strong>Full Audiobook — Coming Soon</strong>
    <small>Join JayTree Case Files and we’ll let you know when full audiobook editions are available to purchase directly from JayTreeBooks.com.</small>
  </div>
  <a class="cta solid ku-button" href="../case-files.html" data-track="audiobook_case_files">Join JayTree Case Files</a>
</div>'''

LEGACY_CALLOUT = f'''      <!-- {MARKER} -->
      <div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">
        <div>
          <span class="ku-kicker">Direct from JayTree Books</span>
          <strong>Full Audiobook — Coming Soon</strong>
          <small>Join JayTree Case Files and we’ll let you know when full audiobook editions are available to purchase directly from JayTreeBooks.com.</small>
        </div>
        <a class="cta solid ku-button" href="case-files.html" data-track="audiobook_case_files" data-book="${{b.slug}}">Join JayTree Case Files</a>
      </div>'''

OLD_LEGACY_CALLOUT = f'''      <!-- {MARKER} -->
      <div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">
        <div>
          <span class="ku-kicker">Direct from JayTree Books</span>
          <strong>Full Audiobook — Coming Soon</strong>
          <small>Full audiobook editions will be available to purchase directly from JayTreeBooks.com.</small>
        </div>
      </div>'''


def patch_book_page(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
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
            print(f"Added direct audiobook coming-soon Case Files callout: {path.relative_to(ROOT)}")
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

    if OLD_LEGACY_CALLOUT in text:
        text = text.replace(OLD_LEGACY_CALLOUT, LEGACY_CALLOUT, 1)
    elif MARKER not in text:
        needle = '''      <p class="section-copy">Play the website audio sample${b.audiobookYoutubeUrl ? " or watch the YouTube chapter reading" : ""}.</p>\n      ${audiobookVideo}'''
        replacement = needle + "\n" + LEGACY_CALLOUT
        if needle not in text:
            raise RuntimeError("Could not find legacy audiobook section in app.js")
        text = text.replace(needle, replacement, 1)

    APP_PATH.write_text(text, encoding="utf-8")
    print("Updated legacy audiobook page with Case Files signup CTA in app.js")


def main() -> None:
    pages = sorted(BOOKS_DIR.glob("*.html"))
    if not pages:
        raise RuntimeError("No generated book pages found")
    for page in pages:
        patch_book_page(page)
    patch_app_js()


if __name__ == "__main__":
    main()
