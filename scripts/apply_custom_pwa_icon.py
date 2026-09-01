#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import re
from io import BytesIO
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ICONS = ROOT / "icons"
CHUNK_FILES = [ICONS / f"app-icon-source.b64.{index}" for index in range(4)]
MASKABLE_SOURCE = ICONS / "icon-maskable-512.b64"
EXPECTED_SOURCE_BYTES = 7488
EXPECTED_SOURCE_SHA256 = "479419fa1dd597799d44eba21cc0efba7986080b625a64a4f8425ef6ac74e042"
EXPECTED_MASKABLE_BYTES = 10008
EXPECTED_MASKABLE_SHA256 = "c5761d01d7da880a5a027e9f93ac1d60f189f0a1d28976cf56449f5b5276afff"
ICON_VERSION = "publisher-logo-3"
CACHE_NAME = "jaytree-pwa-v4"


def decode_image(encoded: str, expected_bytes: int, expected_sha256: str, label: str) -> Image.Image:
    raw = base64.b64decode(encoded, validate=True)
    if len(raw) != expected_bytes:
        raise ValueError(f"Unexpected {label} source size: {len(raw)} bytes")
    digest = hashlib.sha256(raw).hexdigest()
    if digest != expected_sha256:
        raise ValueError(f"Unexpected {label} source SHA256: {digest}")

    with Image.open(BytesIO(raw)) as source_image:
        source_image.load()
        return source_image.convert("RGB")


def load_source() -> Image.Image:
    missing = [path for path in CHUNK_FILES if not path.exists()]
    if missing:
        raise FileNotFoundError(", ".join(str(path) for path in missing))

    encoded = "".join(path.read_text(encoding="ascii").strip() for path in CHUNK_FILES)
    return decode_image(encoded, EXPECTED_SOURCE_BYTES, EXPECTED_SOURCE_SHA256, "standard icon")


def load_maskable_source() -> Image.Image:
    if not MASKABLE_SOURCE.exists():
        raise FileNotFoundError(str(MASKABLE_SOURCE))
    encoded = MASKABLE_SOURCE.read_text(encoding="ascii").strip()
    return decode_image(encoded, EXPECTED_MASKABLE_BYTES, EXPECTED_MASKABLE_SHA256, "maskable icon")


def write_icons() -> None:
    source = load_source()
    icon512 = source.resize((512, 512), Image.Resampling.LANCZOS)
    icon512.save(ICONS / "icon-512.png", "PNG", optimize=True)
    source.resize((192, 192), Image.Resampling.LANCZOS).save(
        ICONS / "icon-192.png", "PNG", optimize=True
    )
    source.resize((180, 180), Image.Resampling.LANCZOS).save(
        ICONS / "apple-touch-icon.png", "PNG", optimize=True
    )

    maskable = load_maskable_source().resize((512, 512), Image.Resampling.LANCZOS)
    maskable.save(ICONS / "icon-maskable-512.png", "PNG", optimize=True)


def patch_manifest() -> None:
    path = ROOT / "manifest.webmanifest"
    manifest = json.loads(path.read_text(encoding="utf-8"))
    for icon in manifest.get("icons", []):
        sizes = icon.get("sizes")
        purposes = set(str(icon.get("purpose", "any")).split())
        if "maskable" in purposes:
            icon["src"] = f"/icons/icon-maskable-512.png?v={ICON_VERSION}"
            icon["sizes"] = "512x512"
            icon["type"] = "image/png"
            icon["purpose"] = "maskable"
        elif sizes == "192x192":
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
    text = re.sub(
        r'"/icons/icon-maskable-512\.png(?:\?v=[^"]+)?"',
        f'"/icons/icon-maskable-512.png?v={ICON_VERSION}"',
        text,
    )

    maskable_entry = f'  "/icons/icon-maskable-512.png?v={ICON_VERSION}"'
    if "/icons/icon-maskable-512.png" not in text:
        marker = f'  "/icons/icon-512.png?v={ICON_VERSION}"'
        if marker in text:
            text = text.replace(marker, marker + ",\n" + maskable_entry, 1)

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
        f"Applied JayTree standard icons plus dedicated Android maskable icon; "
        f"updated {html_changed} Apple icon reference(s)."
    )


if __name__ == "__main__":
    main()
