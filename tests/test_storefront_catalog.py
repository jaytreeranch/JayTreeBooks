"""Regression tests for adding books without hand-editing HTML pages."""
import copy
import importlib.util
import json
import pathlib
import shutil
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("storefront_generator", ROOT / "scripts" / "build_storefront_catalog.py")
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


class CatalogReleaseSafety(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((ROOT / "data" / "storefront-catalog.json").read_text(encoding="utf-8"))

    def copy_pages(self, temp):
        root = pathlib.Path(temp)
        for page in ("books.html", "audiobooks.html", "samples.html", "home-v2.html"):
            shutil.copyfile(ROOT / page, root / page)
        return root

    def test_production_six_are_explicitly_verified(self):
        entries = generator.validate(self.catalog)
        self.assertEqual(len(entries), 6)
        self.assertEqual(sum(b["audiobook_status"] == "available" for b in entries), 6)

    def test_generation_is_idempotent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = self.copy_pages(temp)
            first = generator.build(root, self.catalog)
            for filename, text in first.items():
                (root / filename).write_text(text, encoding="utf-8")
            second = generator.build(root, self.catalog)
            self.assertEqual(first, second)

    def test_new_unreleased_book_appears_without_fake_buy_button(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["books"].append({
            "slug": "new-mystery-sample",
            "title": "New Mystery Sample",
            "edition": "Novel",
            "description": "An intentionally fictional future title used only by the test.",
            "tagline": "An unpublished future edition",
            "cover": "",
            "book_page": "",
            "amazon_url": "",
            "sample_page": "",
            "chapter_page": "",
            "payhip_url": "",
            "book_status": "coming_soon",
            "audiobook_status": "coming_soon",
            "kindle_unlimited": False
        })
        with tempfile.TemporaryDirectory() as temp:
            root = self.copy_pages(temp)
            generated = generator.build(root, catalog)
            self.assertIn("New Mystery Sample", generated["books.html"])
            self.assertIn("Coming soon · Not yet for sale", generated["books.html"])
            self.assertIn("Future audiobook editions", generated["audiobooks.html"])
            self.assertNotIn("new-mystery-sample", generated["samples.html"])
            self.assertNotIn('data-book="new-mystery-sample" data-placement="audio_cinematic_shelf"', generated["audiobooks.html"])
            for k, v in generated.items():
                (root / k).write_text(v, encoding="utf-8")
            self.assertEqual(generated, generator.build(root, catalog))

    def test_invalid_release_cannot_accidentally_show_checkout(self):
        catalog = copy.deepcopy(self.catalog)
        future = copy.deepcopy(catalog["books"][0])
        future["slug"] = "not-ready"
        future["payhip_url"] = ""
        future["book_status"] = "coming_soon"
        future["audiobook_status"] = "available"
        catalog["books"].append(future)
        with self.assertRaisesRegex(ValueError, "needs published"):
            generator.validate(catalog)

    def test_new_published_audiobook_requires_only_catalog_update(self):
        catalog = copy.deepcopy(self.catalog)
        upcoming = {
            "slug": "catalog-growth-test",
            "title": "Catalog Growth Test",
            "edition": "Novel",
            "description": "A fictional seventh book used exclusively by automated tests.",
            "tagline": "A new mysterious manuscript",
            "cover": "images/optimized/catalog-growth-test.webp",
            "book_page": "books/catalog-growth-test.html",
            "amazon_url": "https://www.amazon.com/dp/TESTEXAMPLE",
            "sample_page": "audio/book-7-test-only.html",
            "chapter_page": "chapters/book-7-test-only.html",
            "payhip_url": "https://payhip.com/b/testOnlySeventh",
            "book_status": "published",
            "audiobook_status": "available",
            "audiobook_price_usd": "1.99",
            "narrator": "Vivian",
            "kindle_unlimited": False
        }
        catalog["books"].append(upcoming)
        catalog["featured_audiobook"] = upcoming["slug"]
        with tempfile.TemporaryDirectory() as temp:
            root = self.copy_pages(temp)
            generated = generator.build(root, catalog)
            self.assertEqual(generated["audiobooks.html"].count('class="sf-cine-cover-link sf-cine-select"'), 7)
            self.assertIn("https://payhip.com/b/testOnlySeventh", generated["audiobooks.html"])
            self.assertIn('id="sf-cine-featured-title">Catalog Growth Test</h2>', generated["audiobooks.html"])
            self.assertIn('id="sf-cine-featured-buy" href="https://payhip.com/b/testOnlySeventh"', generated["audiobooks.html"])
            self.assertIn('id="sf-cine-featured-sample" href="audio/book-7-test-only.html"', generated["audiobooks.html"])
            self.assertIn("Catalog Growth Test", generated["books.html"])
            self.assertIn("Catalog Growth Test", generated["samples.html"])
            self.assertIn("Seven complete Vivian-narrated editions", generated["audiobooks.html"])
            for name, source in generated.items():
                (root/name).write_text(source, encoding="utf-8")
            self.assertEqual(generated, generator.build(root, catalog))

    def test_new_price_does_not_silently_mislabel_global_sale_banner(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["books"][1]["audiobook_price_usd"] = "2.99"
        with self.assertRaisesRegex(ValueError, "Mixed audiobook prices"):
            generator.validate(catalog)

    def test_duplicate_seller_url_is_blocked(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["books"][1]["payhip_url"] = catalog["books"][0]["payhip_url"]
        with self.assertRaisesRegex(ValueError, "duplicate sale URL"):
            generator.validate(catalog)

    def test_invalid_external_seller_domain_is_blocked(self):
        catalog = copy.deepcopy(self.catalog)
        catalog["books"][1]["payhip_url"] = "https://malicious.example/checkout"
        with self.assertRaisesRegex(ValueError, "unsafe payhip_url"):
            generator.validate(catalog)


if __name__ == "__main__":
    unittest.main()
