#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "media" / "social"
CANVAS = (1080, 1350)  # Instagram-friendly 4:5 portrait
MAX_COVER = (860, 1210)

COVERS = [
    "second-draft",
    "the-hollow-year",
    "the-hollow-bell",
    "the-absconding",
    "the-correction",
]


def build_one(slug: str) -> None:
    source = SOURCE_DIR / f"{slug}.png"
    if not source.exists():
        raise FileNotFoundError(source)

    with Image.open(source) as opened:
        original = opened.convert("RGB")

    # Fill the 4:5 canvas with a dark blurred version of the real cover so the
    # source artwork stays recognizable without stretching or cropping it.
    background = ImageOps.fit(original, CANVAS, method=Image.Resampling.LANCZOS)
    background = background.filter(ImageFilter.GaussianBlur(radius=30))
    background = ImageEnhance.Brightness(background).enhance(0.30)

    cover = original.copy()
    cover.thumbnail(MAX_COVER, Image.Resampling.LANCZOS)

    x = (CANVAS[0] - cover.width) // 2
    y = (CANVAS[1] - cover.height) // 2

    # Add a subtle dark frame/shadow behind the cover for separation.
    framed = background.copy()
    shadow_margin = 18
    shadow = Image.new("RGB", (cover.width + shadow_margin * 2, cover.height + shadow_margin * 2), (8, 8, 8))
    framed.paste(shadow, (x - shadow_margin, y - shadow_margin))
    framed.paste(cover, (x, y))

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output = OUTPUT_DIR / f"{slug}.jpg"
    framed.save(output, "JPEG", quality=92, optimize=True, progressive=True)
    print(f"Built {output.relative_to(ROOT)}")


def main() -> int:
    for slug in COVERS:
        build_one(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
