#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "images"
OUTPUT_DIR = ROOT / "media" / "social" / "variety"
CANVAS = (1080, 1350)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

CREAM = (241, 232, 211)
GOLD = (198, 155, 79)
WHITE = (240, 235, 222)

BOOKS = {
    "the-hollow-bell": "SOME BELLS NEVER\nSTOP RINGING",
    "the-correction": "WHAT IF THE RECORD\nWAS WRONG?",
    "second-draft": "NOBODY TELLS THE TRUTH\nTHE FIRST TIME",
    "the-absconding": "SOME HIVES\nNEVER FORGET",
    "the-hollow-year": "WHAT IF EVERYONE\nFORGOT YOU EXISTED?",
}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def fit_font(text: str, max_width: int, start: int, minimum: int = 28) -> ImageFont.FreeTypeFont:
    probe = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    size = start
    while size >= minimum:
        candidate = font(SERIF_BOLD, size)
        if all(probe.textbbox((0, 0), line, font=candidate)[2] <= max_width for line in text.splitlines()):
            return candidate
        size -= 2
    return font(SERIF_BOLD, minimum)


def center_text(draw: ImageDraw.ImageDraw, y: int, text: str, text_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int], *, spacing: int = 6) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=text_font, align="center", spacing=spacing)
    width = box[2] - box[0]
    draw.multiline_text(((CANVAS[0] - width) / 2, y), text, font=text_font, fill=fill, align="center", spacing=spacing)


def panel_text(draw: ImageDraw.ImageDraw, panel_x: int, y: int, text: str, text_font: ImageFont.FreeTypeFont, fill: tuple[int, int, int], *, spacing: int = 6) -> None:
    box = draw.multiline_textbbox((0, 0), text, font=text_font, align="center", spacing=spacing)
    width = box[2] - box[0]
    draw.multiline_text((panel_x + (440 - width) / 2, y), text, font=text_font, fill=fill, align="center", spacing=spacing)


def background(original: Image.Image, brightness: float, blur: int) -> Image.Image:
    bg = ImageOps.fit(original, CANVAS, method=Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(bg).enhance(brightness)


def scaled_cover(original: Image.Image, maximum: tuple[int, int]) -> Image.Image:
    cover = original.copy()
    cover.thumbnail(maximum, Image.Resampling.LANCZOS)
    return cover


def add_cover_with_shadow(canvas: Image.Image, cover: Image.Image, x: int, y: int, margin: int = 16) -> Image.Image:
    canvas = canvas.convert("RGBA")
    shadow = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rectangle((x - margin, y - margin, x + cover.width + margin, y + cover.height + margin), fill=(0, 0, 0, 215))
    shadow = shadow.filter(ImageFilter.GaussianBlur(14))
    canvas = Image.alpha_composite(canvas, shadow)
    canvas.alpha_composite(cover.convert("RGBA"), (x, y))
    return canvas


def build_hook(slug: str, original: Image.Image) -> Image.Image:
    canvas = background(original, 0.38, 18).convert("RGBA")
    overlay = Image.new("RGBA", CANVAS, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 1080, 400), fill=(0, 0, 0, 165))
    canvas = Image.alpha_composite(canvas, overlay)

    cover = scaled_cover(original, (730, 880))
    x = (CANVAS[0] - cover.width) // 2
    y = 415
    canvas = add_cover_with_shadow(canvas, cover, x, y)

    draw = ImageDraw.Draw(canvas)
    hook = BOOKS[slug]
    center_text(draw, 65, hook, fit_font(hook, 930, 72), CREAM, spacing=10)
    center_text(draw, 330, "JAYTREE BOOKS • STORY HOOK", font(SERIF, 30), GOLD)
    return canvas


def build_spotlight(original: Image.Image) -> Image.Image:
    canvas = background(original, 0.24, 30).convert("RGBA")
    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 0, 1080, 215), fill=(0, 0, 0, 185))
    headline = "THIS WEEK'S\nFEATURED MYSTERY"
    center_text(draw, 35, headline, fit_font(headline, 950, 62), GOLD, spacing=4)

    cover = scaled_cover(original, (720, 1020))
    x = (CANVAS[0] - cover.width) // 2
    y = 245
    canvas = add_cover_with_shadow(canvas, cover, x, y, 18)

    draw = ImageDraw.Draw(canvas)
    draw.rectangle((0, 1270, 1080, 1350), fill=(0, 0, 0, 195))
    center_text(draw, 1288, "WATCH THE TRAILER • JAYTREEBOOKS.COM", font(SERIF_BOLD, 31), WHITE)
    return canvas


def build_cta(original: Image.Image) -> Image.Image:
    canvas = background(original, 0.22, 30).convert("RGBA")
    cover = scaled_cover(original, (520, 990))
    x = 45
    y = (CANVAS[1] - cover.height) // 2 - 20
    canvas = add_cover_with_shadow(canvas, cover, x, y, 12)

    draw = ImageDraw.Draw(canvas)
    panel_x = 590
    draw.rounded_rectangle((panel_x, 145, 1030, 1185), radius=28, fill=(0, 0, 0, 210), outline=(190, 145, 66, 180), width=2)
    panel_text(draw, panel_x, 220, "READ WITH", fit_font("READ WITH", 390, 48), WHITE)
    panel_text(draw, panel_x, 300, "KINDLE\nUNLIMITED", fit_font("KINDLE\nUNLIMITED", 390, 58), GOLD)
    draw.line((650, 520, 970, 520), fill=GOLD, width=2)
    panel_text(draw, panel_x, 610, "START THE\nMYSTERY TODAY", fit_font("START THE\nMYSTERY TODAY", 365, 44), WHITE)
    panel_text(draw, panel_x, 800, "Available to read with\nKindle Unlimited.", font(SERIF, 28), (220, 214, 200))
    panel_text(draw, panel_x, 1015, "JAYTREEBOOKS.COM", fit_font("JAYTREEBOOKS.COM", 380, 30), GOLD)
    draw.rectangle((0, 1265, 1080, 1350), fill=(0, 0, 0, 200))
    center_text(draw, 1285, "JAYTREE BOOKS", font(SERIF_BOLD, 34), WHITE)
    return canvas


def build_book(slug: str) -> None:
    source = SOURCE_DIR / f"{slug}.png"
    if not source.exists():
        raise FileNotFoundError(source)

    with Image.open(source) as opened:
        original = opened.convert("RGB")

    builders = {
        "hook": lambda: build_hook(slug, original),
        "spotlight": lambda: build_spotlight(original),
        "cta": lambda: build_cta(original),
    }

    destination = OUTPUT_DIR / slug
    destination.mkdir(parents=True, exist_ok=True)
    for slot, builder in builders.items():
        output = destination / f"{slot}.jpg"
        builder().convert("RGB").save(output, "JPEG", quality=90, optimize=True, progressive=True)
        print(f"Built {output.relative_to(ROOT)}")


def main() -> int:
    for slug in BOOKS:
        build_book(slug)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
