#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"
CASE_START = "<!-- JAYTREE_CASE_FILES_START -->"
CASE_END = "<!-- JAYTREE_CASE_FILES_END -->"

CASE_BLOCK_RE = re.compile(
    r'(?:\s*<!-- JAYTREE_CASE_FILES_START -->)?\s*'
    r'(?P<section><section class="case-files" id="case-files">.*?</section>)\s*'
    r'(?:<!-- JAYTREE_CASE_FILES_END -->\s*)?',
    re.DOTALL,
)


def normalize_case_files(text: str) -> str:
    main_match = re.search(r'<main>(?P<body>.*?)</main>', text, flags=re.DOTALL)
    if not main_match:
        raise RuntimeError("Homepage <main> block not found")

    body = main_match.group("body")
    matches = list(CASE_BLOCK_RE.finditer(body))
    if not matches:
        raise RuntimeError("Homepage Case Files section not found")

    # The provider/finalizer may insert a new copy while an older unmarked copy
    # still exists. Keep the last rendered section, remove every copy, then
    # insert exactly one canonical marked block after the Mystery Challenge.
    case_section = matches[-1].group("section").strip()
    body = CASE_BLOCK_RE.sub("\n", body)
    body = body.replace(CASE_START, "").replace(CASE_END, "")

    challenge = re.search(
        r'<section class="challenge challenge-launch" id="challenge">.*?</section>',
        body,
        flags=re.DOTALL,
    )
    if not challenge:
        raise RuntimeError("Homepage Mystery Challenge section not found")

    canonical = f"\n\n{CASE_START}\n{case_section}\n{CASE_END}"
    body = body[: challenge.end()] + canonical + body[challenge.end() :]
    body = re.sub(r'\n{4,}', '\n\n\n', body)

    return text[: main_match.start("body")] + body + text[main_match.end("body") :]


def verify(text: str) -> None:
    assert text.count('id="case-files"') == 1, "Case Files must appear exactly once"
    assert text.count(CASE_START) == 1 and text.count(CASE_END) == 1

    tokens = [
        'class="hero"',
        'id="kindle-unlimited"',
        'id="books"',
        'class="intro"',
        'id="challenge"',
        'id="case-files"',
        'id="audiobooks"',
        'id="youtube"',
        'id="follow"',
        'id="about"',
    ]
    positions = [text.index(token) for token in tokens]
    assert positions == sorted(positions), "Homepage conversion sections are out of order"


def main() -> int:
    text = INDEX.read_text(encoding="utf-8")
    text = normalize_case_files(text)
    verify(text)
    INDEX.write_text(text, encoding="utf-8")
    print("Homepage Case Files deduplicated and conversion order verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
