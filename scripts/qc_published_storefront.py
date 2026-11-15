"""Verify the rendered Pages output, including legacy bookmarks and catalog assets."""
import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from xml.etree import ElementTree

root = Path(sys.argv[1])
origin = "https://jaytreebooks.com/"
pages = ["index.html", "books.html", "audiobooks.html", "samples.html",
         "series-v2.html", "news-v2.html", "experiences-v2.html"]

class References(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        for key in ("src", "href", "poster"):
            if key in attr:
                self.targets.append(attr[key])

sitemap = {el.text for el in ElementTree.parse(root / "sitemap.xml").findall(".//{*}loc")}
for page in pages:
    source = (root / page).read_text(encoding="utf-8")
    assert source.lower().count("<!doctype html>") == 1, page
    canonical = origin + ("" if page == "index.html" else page)
    assert f'<link rel="canonical" href="{canonical}">' in source and canonical in sitemap, page
    assert 'name="robots" content="index,follow"' in source, page
    assert "Development design preview" not in source and "Interactive design preview" not in source
    parser = References()
    parser.feed(source)
    for ref in parser.targets:
        url = urlsplit(ref)
        if url.scheme or url.netloc or not url.path:
            continue
        assert (root / url.path.lstrip("/")).is_file(), (page, ref)
home = (root / "index.html").read_text(encoding="utf-8")
assert home.strip() == (root / "home-v2.html").read_text(encoding="utf-8").strip()
assert 'id="audiobooks"' in home and 'href="audiobooks.html"' in home
legacy = (root / "home-links.js").read_text(encoding="utf-8")
assert "audiobooks: 'audiobooks.html'" in legacy and "anchor !== 'audiobooks'" in legacy
assert "target.search = location.search" in legacy, "Must preserve social campaign UTM parameters"
book_shop = (root / "books.html").read_text(encoding="utf-8")
assert book_shop.count('class="sf-book-edition-badge"') == 2
for label in ("Full Novel", "Novella"):
    assert ('class="sf-book-edition-badge" aria-hidden="true">' + label) in book_shop
assert home.count('class="jt-home-edition-badge"') == 2
assert 'data-secret-path' in home and 'data-second-secret' in (root / "interactive.html").read_text(encoding="utf-8")
classic = (root / "classic.html").read_text(encoding="utf-8")
assert 'id="follow"' in classic and 'id="youtube"' in classic
catalog = json.loads((root / "data/storefront-catalog.json").read_text(encoding="utf-8"))
shop = (root / "audiobooks.html").read_text(encoding="utf-8")
for book in catalog["books"]:
    if book["audiobook_status"] == "available":
        assert book["payhip_url"] in shop and book["sample_page"] in shop
        assert (root / book["sample_page"]).is_file()
print("Rendered homepage, campaign anchor, six catalog offers, sitemap, hidden routes and storefront references passed.")
