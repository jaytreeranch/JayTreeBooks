#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "index.html"

CASE_START = "<!-- JAYTREE_CASE_FILES_START -->"
CASE_END = "<!-- JAYTREE_CASE_FILES_END -->"
SOCIAL_START = "<!-- JAYTREE_SOCIAL_FOLLOW_START -->"
SOCIAL_END = "<!-- JAYTREE_SOCIAL_FOLLOW_END -->"

CASE_SECTION_RE = re.compile(r'<section class="case-files" id="case-files">.*?</section>', re.DOTALL)
SOCIAL_SECTION_RE = re.compile(r'<section class="social-follow" id="follow">.*?</section>', re.DOTALL)
CASE_MARKED_RE = re.compile(re.escape(CASE_START) + r".*?" + re.escape(CASE_END), re.DOTALL)
SOCIAL_MARKED_RE = re.compile(re.escape(SOCIAL_START) + r".*?" + re.escape(SOCIAL_END), re.DOTALL)
CHALLENGE_RE = re.compile(r'<section class="challenge[^>]*id="challenge"[^>]*>.*?</section>', re.DOTALL)
ABOUT_RE = re.compile(r'<section class="about" id="about">', re.DOTALL)


def extract_section(text: str, marked_re: re.Pattern[str], section_re: re.Pattern[str], start: str, end: str) -> str:
    marked = marked_re.search(text)
    if marked:
        section = section_re.search(marked.group(0))
        if section:
            return f"{start}\n{section.group(0)}\n{end}"
    section = section_re.search(text)
    if not section:
        raise RuntimeError(f"Could not find homepage section for {start}")
    return f"{start}\n{section.group(0)}\n{end}"


def remove_all(text: str, marked_re: re.Pattern[str], section_re: re.Pattern[str]) -> str:
    text = marked_re.sub("", text)
    text = section_re.sub("", text)
    return text


def compact_spacing(text: str) -> str:
    return re.sub(r"\n{4,}", "\n\n\n", text)


def normalize() -> None:
    text = INDEX.read_text(encoding="utf-8")

    case_block = extract_section(text, CASE_MARKED_RE, CASE_SECTION_RE, CASE_START, CASE_END)
    social_block = extract_section(text, SOCIAL_MARKED_RE, SOCIAL_SECTION_RE, SOCIAL_START, SOCIAL_END)

    text = remove_all(text, CASE_MARKED_RE, CASE_SECTION_RE)
    text = remove_all(text, SOCIAL_MARKED_RE, SOCIAL_SECTION_RE)
    text = compact_spacing(text)

    challenge = CHALLENGE_RE.search(text)
    if not challenge:
        raise RuntimeError("Could not find Mystery Challenge section")
    text = text[: challenge.end()] + "\n\n" + case_block + text[challenge.end() :]

    about = ABOUT_RE.search(text)
    if not about:
        raise RuntimeError("Could not find About section")
    text = text[: about.start()] + social_block + "\n\n" + text[about.start() :]
    text = compact_spacing(text)

    checks = {
        'id="case-files"': 1,
        'id="follow"': 1,
        CASE_START: 1,
        CASE_END: 1,
        SOCIAL_START: 1,
        SOCIAL_END: 1,
    }
    for token, expected in checks.items():
        actual = text.count(token)
        if actual != expected:
            raise RuntimeError(f"Expected {expected} occurrence of {token!r}, found {actual}")

    positions = [
        text.index('id="kindle-unlimited"'),
        text.index('id="books"'),
        text.index('id="challenge"'),
        text.index('id="case-files"'),
        text.index('id="audiobooks"'),
        text.index('id="youtube"'),
        text.index('id="follow"'),
        text.index('id="about"'),
    ]
    if positions != sorted(positions):
        raise RuntimeError("Homepage sections are not in the intended order")

    INDEX.write_text(text, encoding="utf-8")
    print("Homepage normalized: one Case Files section, one social section, correct section order.")


if __name__ == "__main__":
    normalize()
