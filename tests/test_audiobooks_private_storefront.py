"""Ensure the five-book audiobook storefront stays a private, non-selling preview."""
from pathlib import Path
from html.parser import HTMLParser
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "audiobooks" / "index.html"
BOOKS = {
    "second-draft": ("../images/optimized/second-draft.webp", "../audio/book-1-sample.html"),
    "the-correction": ("../images/optimized/the-correction.webp", "../audio/book-5-sample.html"),
    "the-hollow-year": ("../images/optimized/the-hollow-year.webp", "../audio/book-2-sample.html"),
    "the-absconding": ("../images/optimized/the-absconding.webp", "../audio/book-4-sample.html"),
    "the-hollow-bell": ("../images/optimized/the-hollow-bell.webp", "../audio/book-3-sample.html"),
}

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.articles=0
        self.links=[]
        self.images=[]
        self.meta=[]
        self.buttons=0
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=="article" and "product" in attrs.get("class","").split():self.articles+=1
        if tag=="a":self.links.append(attrs.get("href",""))
        if tag=="img":self.images.append(attrs)
        if tag=="meta":self.meta.append(attrs)
        if tag=="button":self.buttons+=1

class StorefrontReleaseGate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf-8")
        cls.page=Audit()
        cls.page.feed(cls.html)
    def test_exactly_five_novel_cards(self):
        self.assertEqual(self.page.articles,5)
    def test_original_cover_and_samples(self):
        for cover,audio in BOOKS.values():
            self.assertIn(cover,[x.get("src") for x in self.page.images])
            self.assertIn(audio,self.page.links)
    def test_image_accessibility(self):
        self.assertEqual(len([i for i in self.page.images if i.get("alt")]),5)
    def test_no_checkout_or_download(self):
        self.assertEqual(self.page.buttons,0)
        for link in self.page.links:
            self.assertNotIn("payhip",link.lower())
            self.assertNotIn("checkout",link.lower())
            self.assertNotIn("download",link.lower())
            self.assertNotIn(".mp3",link.lower())
            self.assertNotIn(".m4b",link.lower())
    def test_noindex_before_release(self):
        self.assertTrue(any(x.get("name")=="robots" and "noindex" in x.get("content","") for x in self.page.meta))
    def test_only_correct_titles(self):
        for name in ("Second Draft","The Correction","The Hollow Year","The Absconding","The Hollow Bell"):
            self.assertIn("<h3>"+name+"</h3>",self.html)
        self.assertNotIn("<h3>The Hollow Bell — Novella</h3>",self.html)
    def test_selling_is_not_misrepresented(self):
        self.assertIn("purchases are not available",self.html.lower())
        self.assertIn("No payment buttons or download links are enabled",self.html)
if __name__=="__main__":unittest.main()
