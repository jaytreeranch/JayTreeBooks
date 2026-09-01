#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"
SOURCE = ICONS / "app-icon-source.jpg"
ICON_VERSION = "publisher-logo-2"
CACHE_NAME = "jaytree-pwa-v3"


def write_icons() -> None:
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    with Image.open(SOURCE) as source_image:
        source = source_image.convert("RGB")
        icon512 = source.resize((512, 512), Image.Resampling.LANCZOS)
        icon512.save(ICONS / "icon-512.png", "PNG", optimize=True)
        icon512.resize((192, 192), Image.Resampling.LANCZOS).save(
            ICONS / "icon-192.png", "PNG", optimize=True
        )
        icon512.resize((180, 180), Image.Resampling.LANCZOS).save(
            ICONS / "apple-touch-icon.png", "PNG", optimize=True
        )


def patch_manifest() -> None:
    path = ROOT / "manifest.webmanifest"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for icon in manifest.get("icons", []):
        sizes = icon.get("sizes")
        if sizes == "192x192":
            icon["src"] = f"/icons/icon-192.png?v={ICON_VERSION}"
        elif sizes == "512x512":
            icon["src"] = f"/icons/icon-512.png?v={ICON_VERSION}"
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def patch_service_worker() -> None:
    path = ROOT / "service-worker.js"
    text = path.read_text(encoding="utf-8")
    text = re.sub(
        r'const CACHE_NAME = "jaytree-pwa-v\d+";',
        f'const CACHE_NAME = "{CACHE_NAME}";',
        text,
    )
    text = re.sub(
        r'"/icons/icon-192\.png(?:\?v=[^"]+)?"',
        f'"/icons/icon-192.png?v={ICON_VERSION}"',
        text,
    )
    text = re.sub(
        r'"/icons/icon-512\.png(?:\?v=[^"]+)?"',
        f'"/icons/icon-512.png?v={ICON_VERSION}"',
        text,
    )
    path.write_text(text, encoding="utf-8")


def patch_html() -> int:
    targets = set(ROOT.glob("*.html"))
    for folder in ("books", "chapters", "audio"):
        directory = ROOT / folder
        if directory.exists():
            targets.update(directory.glob("*.html"))

    changed = 0
    for path in targets:
        html = path.read_text(encoding="utf-8")
        updated = re.sub(
            r'href="/icons/apple-touch-icon\.png(?:\?v=[^"]+)?"',
            f'href="/icons/apple-touch-icon.png?v={ICON_VERSION}"',
            html,
        )
        if updated != html:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    write_icons()
    patch_manifest()
    patch_service_worker()
    html_changed = patch_html()
    print(
        f"Applied optimized JayTree publisher logo as the PWA app icon; "
        f"updated {html_changed} Apple icon reference(s)."
    )


if __name__ == "__main__":
    main()
