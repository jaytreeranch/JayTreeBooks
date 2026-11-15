"""Build a portable browser review from the public web assets in this checkout."""
import argparse
import re
import zipfile
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKIP_PAGES = {"storefront-home.html", "x-preview-test.html", "tiktok-callback.html"}
SECTIONS = {"books": "books.html", "audiobooks": "audiobooks.html", "challenge": "experiences-v2.html",
            "about": "about.html", "case-files": "case-files.html", "youtube": "experiences-v2.html",
            "upcoming-novels": "upcoming-books.html"}
# Other historical campaign anchors retain their original homepage content.
def portable_html(source, name, catalog):
    source = re.sub(r"\A---\n.*?\n---\n", "", source, count=1, flags=re.S)
    root = "../" * (len(PurePosixPath(name).parts) - 1)
    source = re.sub(r'<script\b[^>]*\bsrc=["\']https://www\.googletagmanager\.com/[^>]*></script>', '', source)
    source = re.sub(r'<script\b[^>]*\bsrc="[^"]*pwa\.js[^"]*"[^>]*></script>', '', source)
    source = re.sub(r'<link\b[^>]*\brel="manifest"[^>]*>', '', source)

    def adjust(match):
        attr, quote, value = match.groups()
        if value.startswith("/") and not value.startswith("//"):
            value = root + (value.lstrip("/") or "index.html")
        if attr == "href" and value == "./":
            value = "index.html"
        if attr == "href":
            link = urlsplit(value)
            if not link.scheme and not link.netloc and link.path.endswith("index.html") and link.fragment:
                value = root + SECTIONS.get(link.fragment, "classic.html#" + link.fragment)
        return attr + "=" + quote + value + quote
    source = re.sub(r'''\b(href|src|poster)=(["'])(.*?)\2''', adjust, source)
    if 'class="jt-header"' in source:
        inline = '<script id="jt-portable-catalog" type="application/json">' + catalog + '</script>'
        source = source.replace('</head>', inline + '</head>', 1)
    return source

def build(output):
    catalog = (ROOT / "data/storefront-catalog.json").read_text(encoding="utf-8").replace("<",r"\u003c")
    selected = set()
    for ext in ("html", "css", "js", "png", "ico"):
        selected.update(p for p in ROOT.glob("*." + ext) if p.name not in SKIP_PAGES)
    for folder in ("books", "chapters", "audio", "guides", "images", "icons", "cards"):
        selected.update(p for p in (ROOT / folder).rglob("*") if p.is_file() and p.suffix.lower()
                        in {".html",".css",".js",".webp",".jpg",".jpeg",".png",".svg",".mp3",".ico"})
    selected.difference_update((ROOT / "audio").glob("book-*-sample.mp3"))
    selected.update((ROOT / "data").glob("*.json"))
    for p in list(selected):
        if p.suffix == ".html":
            for media in re.findall(r'["\'](media/[^"\'<>]+)["\']', p.read_text(encoding="utf-8")):
                file = ROOT / media.split("?")[0]
                if file.is_file():
                    selected.add(file)
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, "w") as archive:
        def add(name, data):
            # Fixed metadata makes the LAN and downloadable builds comparable.
            info = zipfile.ZipInfo(name)
            info.create_system = 0
            archive.writestr(info, data, compress_type=zipfile.ZIP_STORED)
        for p in sorted(selected, key=lambda path:path.relative_to(ROOT).as_posix()):
            name = p.relative_to(ROOT).as_posix()
            if p.suffix == ".html":
                html = portable_html(p.read_text(encoding="utf-8"),name,catalog)
                add("classic.html" if name == "index.html" else name, html.encode("utf-8"))
                if name == "home-v2.html":
                    add("index.html", html.encode("utf-8"))
            elif p.suffix in {".css",".js",".json",".svg",".vtt"}:
                add(name, p.read_text(encoding="utf-8").encode("utf-8"))
            else:
                add(name, p.read_bytes())
        add("START-HERE.txt", b"Extract the entire ZIP. Double-click index.html to start.\r\nOpen audiobooks.html for the listening shelf. Search, book pages and audio previews work locally.\r\nPurchases, newsletter signup and hosted videos use the internet.\r\n")
    print(output, output.stat().st_size, "bytes")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    build(parser.parse_args().output)
