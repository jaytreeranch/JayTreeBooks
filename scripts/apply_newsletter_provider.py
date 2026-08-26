#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
INDEX_PATH = ROOT / "index.html"
CASE_FILES_PATH = ROOT / "case-files.html"
THANKS_PATH = ROOT / "case-files-thanks.html"
CONFIG_RE = re.compile(r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;", re.S)
FORM_RE = re.compile(r'<form class="case-files-form"[^>]*data-case-files-form[^>]*>.*?</form>', re.S)
# The active newsletter backend is controlled by newsletter.provider in config.js.


def load_config() -> dict:
    text = CONFIG_PATH.read_text(encoding="utf-8")
    match = CONFIG_RE.search(text)
    if not match:
        raise RuntimeError("Could not parse config.js")
    return json.loads(match.group(1))


def kit_block(embed_code: str, placement: str) -> str:
    return (
        f'<div class="case-files-form case-files-kit-form" data-case-files-form '
        f'data-placement="{escape(placement, quote=True)}">\n'
        f'{embed_code.strip()}\n'
        '</div>\n'
        '<p class="case-files-fineprint">By subscribing, you agree to receive JayTree Books emails. '
        'Every email includes an unsubscribe link.</p>'
    )


def replace_one(path: Path, placement: str, embed_code: str) -> None:
    text = path.read_text(encoding="utf-8")
    match = FORM_RE.search(text)
    if not match:
        raise RuntimeError(f"Could not find Case Files form in {path.name}")
    text = text[:match.start()] + kit_block(embed_code, placement) + text[match.end():]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    config = load_config()
    newsletter = config.setdefault("newsletter", {})
    provider = str(newsletter.get("provider") or "formsubmit").strip().lower()
    if provider == "formsubmit":
        print("Newsletter provider is FormSubmit; leaving current live forms unchanged.")
        return 0
    if provider != "kit":
        raise RuntimeError(f"Unsupported newsletter provider: {provider}")

    kit = newsletter.get("kit") or {}
    embed_code = str(kit.get("embedCode") or "").strip()
    if not embed_code:
        raise RuntimeError("newsletter.provider is 'kit' but newsletter.kit.embedCode is empty")
    if "kit.com" not in embed_code and "convertkit" not in embed_code:
        raise RuntimeError("Kit embed code does not appear to reference Kit")

    replace_one(INDEX_PATH, "homepage", embed_code)
    replace_one(CASE_FILES_PATH, "case-files-page", embed_code)

    # The Kit confirmation link redirects here only after the subscriber has
    # confirmed, so retain the normal "You're in" copy and just record Kit as
    # the completion source in GA4.
    thanks = THANKS_PATH.read_text(encoding="utf-8")
    thanks = thanks.replace("{source:'formsubmit'}", "{source:'kit'}")
    THANKS_PATH.write_text(thanks, encoding="utf-8")

    print("Applied Kit as the JayTree Case Files newsletter provider.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
