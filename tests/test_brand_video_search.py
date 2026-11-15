#!/usr/bin/env python3
"""Regression tests for JayTree brand identity, video markup and Search Console CSV reporting."""
import importlib.util
import json
from pathlib import Path
import re
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "report_search_visibility.py"
spec = importlib.util.spec_from_file_location("jaytree_search_visibility", SCRIPT)
tracker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tracker)

def jsonld(page):
    html = (ROOT / page).read_text(encoding="utf-8")
    values = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S | re.I)
    return [json.loads(v) for v in values]

class BrandVideoSearchTests(unittest.TestCase):
    def test_publisher_links_preserved_and_alias(self):
        orgs = [x for x in jsonld("home-v2.html") if x.get("@type") == "Organization"]
        self.assertEqual(len(orgs), 1)
        org = orgs[0]
        self.assertEqual(org["@id"], "https://jaytreebooks.com/#publisher")
        self.assertEqual(org["alternateName"], "JayTreeBooks")
        for url in ("https://www.youtube.com/@JayTreeBooks", "https://www.instagram.com/jaytreebooks/",
                    "https://www.facebook.com/profile.php?id=61593984832182"):
            self.assertIn(url, org["sameAs"])

    def test_youtube_trailer_markup_uses_embed_not_watch_content_url(self):
        video = next(x for x in jsonld("animated-series.html") if x.get("@type") == "VideoObject")
        self.assertNotIn("contentUrl", video)
        self.assertEqual(video["embedUrl"], "https://www.youtube-nocookie.com/embed/PmGQoyjYTDs")
        self.assertTrue((ROOT / "media/social/images/the-hollow-bell/official-trailer-thumbnail.jpg").exists())

    def test_original_mp4_watch_page_and_links(self):
        video = next(x for x in jsonld("upcoming-novels-teaser.html") if x.get("@type") == "VideoObject")
        self.assertEqual(video["mainEntityOfPage"], "https://jaytreebooks.com/upcoming-novels-teaser.html")
        self.assertTrue(video["contentUrl"].endswith(".mp4"))
        self.assertEqual(video["uploadDate"], "2026-11-09")
        self.assertTrue((ROOT / "images/social/previews/upcoming-books.jpg").exists())
        page = (ROOT / "upcoming-novels-teaser.html").read_text(encoding="utf-8")
        self.assertIn(video["contentUrl"], page)
        self.assertIn('src="/media/upcoming/teaser-en.vtt"', page)
        self.assertIn("G-PHE2JVV5P6", page)
        self.assertIn('href="upcoming-novels-teaser.html"', (ROOT / "upcoming-books.html").read_text(encoding="utf-8"))

    def test_sitemap_and_durable_generator(self):
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        generator = (ROOT / "scripts/seo_content_cleanup.py").read_text(encoding="utf-8")
        self.assertEqual(sitemap.count("https://jaytreebooks.com/upcoming-novels-teaser.html"), 1)
        self.assertIn('("upcoming-novels-teaser.html", "upcoming-novels-teaser.html")', generator)

    def test_query_classification(self):
        self.assertEqual(tracker.bucket("JayTreeBooks.com"), "branded")
        self.assertEqual(tracker.bucket("JayTree Books review"), "branded")
        self.assertEqual(tracker.bucket("psychological mystery books"), "genre")
        self.assertEqual(tracker.bucket("best new mystery books"), "genre")
        self.assertEqual(tracker.bucket("JayTree bookstore scandal"), "other")

    def test_weighted_position_and_unobserved(self):
        rows = [{"query": "JayTree Books", "clicks": 2, "impressions": 10, "position": 2.0, "bucket": "branded"},
                {"query": "JayTree Books", "clicks": 1, "impressions": 30, "position": 10.0, "bucket": "branded"}]
        result = tracker.build_report(rows, period="test")
        self.assertEqual(result["current"]["groups"]["branded"]["avg_position"], 8.0)
        self.assertIsNone(result["current"]["tracked_queries"]["new mystery book"]["avg_position"])
        self.assertFalse(result["current"]["tracked_queries"]["new mystery book"]["observed"])

    def test_search_console_export_parse(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "gsc.csv"
            p.write_text("Top queries,Clicks,Impressions,CTR,Position\nJayTreeBooks,3,100,3%,8.5\npsychological mystery books,1,20,5%,49\n", encoding="utf-8")
            rows = tracker.parse_gsc_csv(p)
            self.assertEqual(len(rows), 2)
            self.assertEqual(rows[0]["bucket"], "branded")
            self.assertEqual(rows[1]["bucket"], "genre")
            self.assertEqual(tracker.build_report(rows)["current"]["tracked_queries"]["psychological mystery books"]["avg_position"], 49.0)

if __name__ == "__main__":
    unittest.main()
