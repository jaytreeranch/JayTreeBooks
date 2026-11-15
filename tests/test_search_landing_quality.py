"""Regression gates for the two primary search-intent landing pages."""
import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HUBS = ("mystery-books.html", "psychological-mystery-books.html")

class SearchLandingQuality(unittest.TestCase):
    def test_canonical_titles_and_indexable_search_pages(self):
        for page in HUBS:
            with self.subTest(page=page):
                html = (ROOT / page).read_text(encoding="utf-8")
                self.assertRegex(html, r'<link rel="canonical" href="https://jaytreebooks.com/' + page)
                self.assertEqual(len(re.findall(r'<h1\b', html)), 1)
                self.assertNotRegex(html, r'<meta[^>]*robots[^>]*noindex')
                self.assertIn("G-PHE2JVV5P6", html)
                self.assertIn('href="samples.html"', html)
                self.assertIn('href="audiobooks.html"', html)
                self.assertIn('class="discovery-listen"', html)
                self.assertIn('class="jt-skip"', html)
                self.assertRegex(html, r'<main\b[^>]*\bid="main"')
                for tag in re.findall('<img [^>]*src="images/optimized/[^"]+"[^>]*>', html):
                    self.assertIn('width="240"', tag)
                    self.assertIn('height="360"', tag)

    def test_structured_data_represents_actual_books_and_breadcrumbs(self):
        for page in HUBS:
            html = (ROOT / page).read_text(encoding="utf-8")
            blocks = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            self.assertTrue(blocks)
            graphs = [obj for b in blocks for obj in json.loads(b).get("@graph", [])]
            kinds = [obj.get("@type") for obj in graphs]
            self.assertIn("CollectionPage", kinds)
            self.assertIn("BreadcrumbList", kinds)
            self.assertIn("ItemList", kinds)
            book_list = next(x for x in graphs if x.get("@type") == "ItemList")
            self.assertGreaterEqual(book_list.get("numberOfItems", 0), 3)
            for entry in book_list["itemListElement"]:
                self.assertTrue((ROOT / entry["item"]["url"].split("jaytreebooks.com/")[1]).exists())

    def test_internal_links_and_preloaded_hero(self):
        home=(ROOT / "home-v2.html").read_text(encoding="utf-8")
        self.assertIn('rel="preload" as="image" href="images/optimized/second-draft.webp"', home)
        for page in HUBS:
            self.assertIn('href="' + page + '"', home)
        self.assertIn('mystery-books.html', (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn('psychological-mystery-books.html', (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()
