#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config.js"
CONFIG_RE = re.compile(r"window\.JT\s*=\s*(\{.*?\});\s*window\.JAYTREE_CONFIG\s*=\s*window\.JT;", re.S)


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Switch JayTree Case Files to a Kit form embed.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--embed-code", help="Kit JavaScript/HTML form embed code")
    group.add_argument("--embed-file", help="Text file containing the Kit form embed code")
    args = parser.parse_args()

    embed_code = args.embed_code
    if args.embed_file:
        embed_code = Path(args.embed_file).read_text(encoding="utf-8")
    embed_code = str(embed_code or "").strip()
    if not embed_code:
        raise RuntimeError("Kit embed code is empty")
    if "kit.com" not in embed_code and "convertkit" not in embed_code:
        raise RuntimeError("Embed code does not appear to be from Kit")

    config = load_config()
    newsletter = config.setdefault("newsletter", {})
    newsletter.setdefault("name", "JayTree Case Files")
    newsletter.setdefault("formAction", "https://formsubmit.co/jaytreebooks@gmail.com")
    newsletter.setdefault("thankYouUrl", "https://www.JayTreeBooks.com/case-files-thanks.html")
    newsletter["provider"] = "kit"
    newsletter["kit"] = {
        "formName": "JayTree Case Files",
        "sequenceName": "JayTree Case Files Welcome",
        "embedCode": embed_code,
        "confirmationRedirect": "https://www.JayTreeBooks.com/case-files-thanks.html",
    }
    save_config(config)
    print("Configured Kit for JayTree Case Files. Run the website build workflow to deploy it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
