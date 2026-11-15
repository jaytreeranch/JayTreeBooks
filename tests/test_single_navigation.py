from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "about.html", "animated-series.html", "case-files.html", "privacy.html",
    "terms.html", "reading-guides.html", "kindle-unlimited-mystery-books.html",
    "mystery-books.html", "psychological-mystery-books.html",
    "books/second-draft.html", "books/the-absconding.html",
    "books/the-correction.html", "books/the-hollow-bell-novella.html",
    "books/the-hollow-bell.html", "books/the-hollow-year.html"
)

class NavigationTests(unittest.TestCase):
    def test_one_header_per_migrated_public_page(self):
        for rel in PAGES:
            with self.subTest(page=rel):
                html = (ROOT / rel).read_text(encoding="utf-8")
                self.assertEqual(html.count('<header class="jt-header">'), 1)
                self.assertNotRegex(html, r'<header\s+class="nav"')
                self.assertIn('aria-label="Primary navigation"', html)
                self.assertIn('class="jt-mobile"', html)
                self.assertIn('class="jt-skip"', html)
                self.assertRegex(html, r'<main\b[^>]*\bid="main"')

    def test_generator_contains_permanent_header_deduplication(self):
        code = (ROOT / "scripts/build_sitewide_preview.py").read_text(encoding="utf-8")
        self.assertIn("def remove_duplicate_legacy_header(", code)
        self.assertIn("remove_duplicate_legacy_header(ensure_buy_panel", code)

    def test_discovery_paths_have_inbound_links_and_stable_image_dimensions(self):
        home = (ROOT / "home-v2.html").read_text(encoding="utf-8")
        for page in ("psychological-mystery-books.html", "mystery-books.html"):
            self.assertIn('href="' + page + '"', home)
            html = (ROOT / page).read_text(encoding="utf-8")
            for tag in re.findall(r'<img\b[^>]*\bsrc="images/optimized/[^"]+"[^>]*>', html):
                self.assertIn('width="240"', tag)
                self.assertIn('height="360"', tag)
            self.assertIn('overflow-wrap:anywhere', html)
            self.assertIn('@media(max-width:480px)', html)

    def test_conversion_and_hidden_paths_remain(self):
        for rel in ("books/second-draft.html", "books/the-hollow-bell-novella.html"):
            content = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("audiobook_payhip", content)
            self.assertIn("tracking.js", content)
        assert (ROOT / "interactive.html").exists()
        assert (ROOT / "echo-archive.html").exists()

if __name__ == "__main__":
    unittest.main()
