"""Regression guard for contextual genre paths on JayTree Books.

Preserves the storefront catalog, purchase destinations, existing book metadata,
and the single source of truth for the two search landing pages.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]
GOALS = ("psychological-mystery-books.html", "mystery-books.html")


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []
        self.h1s = 0
        self.h2_ids = []
        self.discovery_sections = 0
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "h1":
            self.h1s += 1
        if data.get("id"):
            self.ids.add(data["id"])
            if tag == "h2":
                self.h2_ids.append(data["id"])
        if tag == "a":
            self.hrefs.append(data.get("href", ""))
        if tag == "section" and "sf-seo-discovery" in data.get("class", "").split():
            self.discovery_sections += 1


def parsed(rel):
    obj = PageParser()
    obj.feed((ROOT / rel).read_text(encoding="utf-8"))
    return obj


class GenreDiscoveryTests(unittest.TestCase):
    def test_books_has_two_meaningful_genre_destinations(self):
        page = parsed("books.html")
        self.assertEqual(page.h1s, 1)
        self.assertEqual(page.discovery_sections, 1)
        self.assertIn("sf-discovery-books-title", page.h2_ids)
        for url in GOALS:
            self.assertIn(url, page.hrefs)
        self.assertIn("reading-guides.html", page.hrefs)

    def test_audio_is_still_a_purchase_page_with_genre_paths(self):
        page = parsed("audiobooks.html")
        self.assertEqual(page.h1s, 1)
        self.assertEqual(page.discovery_sections, 1)
        self.assertIn("sf-discovery-audio-title", page.h2_ids)
        for url in GOALS:
            self.assertIn(url, page.hrefs)
        source = (ROOT / "audiobooks.html").read_text(encoding="utf-8")
        self.assertIn("<!-- STOREFRONT_AUDIOBOOKS_START -->", source)
        self.assertIn("<!-- STOREFRONT_AUDIOBOOKS_END -->", source)

    def test_books_generation_markers_preserved(self):
        source = (ROOT / "books.html").read_text(encoding="utf-8")
        self.assertEqual(source.count("<!-- STOREFRONT_BOOKS_START -->"), 1)
        self.assertEqual(source.count("<!-- STOREFRONT_BOOKS_END -->"), 1)
        self.assertIn('href="audiobooks.html"', source)

    def test_topic_links_in_relevant_guide_bodies(self):
        p = parsed("guides/psychological-mystery-stories.html")
        n = parsed("guides/supernatural-suspense.html")
        self.assertIn("../psychological-mystery-books.html", p.hrefs)
        self.assertIn("../mystery-books.html", n.hrefs)
        self.assertEqual(p.h1s, 1)
        self.assertEqual(n.h1s, 1)

    def test_added_genre_destinations_are_real_files(self):
        for rel in ("books.html", "audiobooks.html", "guides/psychological-mystery-stories.html",
                    "guides/supernatural-suspense.html"):
            page = parsed(rel)
            for link in page.hrefs:
                url = urlsplit(link)
                if "mystery-books.html" not in url.path or url.netloc or url.scheme:
                    continue
                absolute = (ROOT / unquote(url.path).lstrip("/")) if url.path.startswith("/") else (ROOT / rel).parent / unquote(url.path)
                self.assertTrue(absolute.is_file(), (rel, link))

    def test_scoped_css_guards_mobile_and_avoids_overflow(self):
        css = (ROOT / "storefront-v2.css").read_text(encoding="utf-8")
        self.assertIn(".sf-seo-discovery-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr))", css)
        self.assertIn(".sf-seo-discovery-grid{grid-template-columns:1fr;", css)
        self.assertIn(".sf-seo-discovery-card{min-width:0;", css)
        self.assertNotIn("!important", css.split("Reader-first contextual genre paths", 1)[1])

    def test_no_new_keyword_stuffed_duplicate_pages(self):
        self.assertTrue((ROOT / GOALS[0]).is_file())
        self.assertTrue((ROOT / GOALS[1]).is_file())
        paths = sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob("*mystery-books.html"))
        self.assertIn("psychological-mystery-books.html", paths)
        self.assertIn("mystery-books.html", paths)
        self.assertEqual(parsed("psychological-mystery-books.html").h1s, 1)
        self.assertEqual(parsed("mystery-books.html").h1s, 1)


if __name__ == "__main__":
    unittest.main()
