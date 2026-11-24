import copy
import importlib.util
import json
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preview", ROOT/"scripts/preview_shopping_audiobooks.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class PreviewTests(unittest.TestCase):
    def setUp(self):
        self.c = json.loads((ROOT/"data/storefront-catalog.json").read_text(encoding="utf-8-sig"))
    def test_six_unique(self):
        rows = m.candidates(self.c)
        self.assertEqual(len(rows), 6)
        self.assertTrue(all(b["audiobook_price_usd"]=="1.99" for b in rows))
    def test_inert_previews(self):
        for b in m.candidates(self.c):
            page = m.render(b)
            self.assertIn("noindex,nofollow",page)
            self.assertIn("<button disabled>",page)
            self.assertNotIn(b["payhip_url"],page)
            self.assertNotIn("application/ld+json",page)
    def test_duplicate_checkout(self):
        self.c["books"][1]["payhip_url"] = self.c["books"][0]["payhip_url"]
        with self.assertRaises(ValueError): m.candidates(self.c)
    def test_missing_cover(self):
        self.c["books"][0]["cover"] = "nonexistent.png"
        with self.assertRaises(ValueError): m.candidates(self.c)
    def test_bad_price(self):
        self.c["books"][0]["audiobook_price_usd"] = "0"
        with self.assertRaises(ValueError): m.candidates(self.c)
