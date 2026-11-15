"""Share-preview regression suite. Uses Python stdlib; safe in GitHub Actions."""
import html
import re
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/"scripts"))
from apply_social_previews import PAGE_ART, apply_to_markup, files_to_update

IMAGE_ROOT="https://jaytreebooks.com/images/social/previews/"
IMG_DIR=ROOT/"images/social/previews"

def meta(markup, attr, key):
    for m in re.finditer(r"<meta\b[^>]*>", markup, re.I|re.S):
        tag=m.group(0)
        a=dict((k.lower(),v) for k,_,v in re.findall(r"([a-zA-Z:_-]+)=([\"'])(.*?)\2",tag))
        if a.get(attr)==key:
            return html.unescape(a.get("content",""))
    return None

def jpeg_size(path):
    data=path.read_bytes()
    if not data.startswith(b"\xff\xd8"):raise ValueError("Not a JPEG")
    pos=2
    while pos<len(data):
        if data[pos]!=255:
            pos+=1;continue
        while pos<len(data) and data[pos]==255:pos+=1
        if pos>=len(data):break
        kind=data[pos];pos+=1
        if kind in (0xD9,0xDA):break
        if pos+2>=len(data):break
        length=int.from_bytes(data[pos:pos+2],"big")
        if length<2:break
        if kind in (0xC0,0xC1,0xC2,0xC3,0xC5,0xC6,0xC7,0xC9,0xCA,0xCB,0xCD,0xCE,0xCF):
            return int.from_bytes(data[pos+5:pos+7],"big"),int.from_bytes(data[pos+3:pos+5],"big")
        pos+=length
    raise ValueError("JPEG dimension marker missing")

class TestSocialPreviewMetadata(unittest.TestCase):
    def test_every_target_page_has_unique_correct_public_image(self):
        pages=files_to_update()
        self.assertGreaterEqual(len(pages),22)
        for page in pages:
            with self.subTest(page=page):
                text=(ROOT/page).read_text(encoding="utf-8")
                raw=meta(text,"property","og:image")
                self.assertIsNotNone(raw)
                self.assertTrue(raw.startswith(IMAGE_ROOT),raw)
                self.assertNotIn("challenge.png",raw)
                self.assertEqual(raw,meta(text,"name","twitter:image"))
                self.assertEqual(raw,meta(text,"property","og:image:secure_url"))
                self.assertEqual(meta(text,"property","og:image:type"),"image/jpeg")
                self.assertEqual(meta(text,"property","og:image:width"),"1200")
                self.assertEqual(meta(text,"property","og:image:height"),"630")
                self.assertEqual(meta(text,"name","twitter:card"),"summary_large_image")
                self.assertTrue(meta(text,"property","og:image:alt"))
                self.assertTrue(meta(text,"name","twitter:image:alt"))
                self.assertTrue(meta(text,"name","twitter:title"))
                self.assertTrue(meta(text,"name","twitter:description"))
                self.assertEqual(text.count('property="og:image"'),1)
                self.assertEqual(text.count('name="twitter:image"'),1)
                self.assertEqual(text.count("JAYTREE_PAGE_SOCIAL_PREVIEW_START"),1)
                self.assertEqual(apply_to_markup(page,text),text)

    def test_all_images_are_high_quality_standard_jpeg_dimensions(self):
        files=list(IMG_DIR.glob("*.jpg"))
        self.assertGreaterEqual(len(files),21)
        for file in files:
            with self.subTest(image=file.name):
                self.assertEqual(jpeg_size(file),(1200,630))
                self.assertGreater(file.stat().st_size,40000)
                self.assertLess(file.stat().st_size,1_500_000)

    def test_no_unintended_duplicate_images_between_unique_pages(self):
        metas={}
        for page in files_to_update():
            metas[page]=meta((ROOT/page).read_text("utf-8"),"property","og:image")
        self.assertEqual(metas["index.html"],metas["home-v2.html"])
        self.assertNotEqual(metas["audiobooks.html"],metas["index.html"])
        self.assertNotEqual(metas["books.html"],metas["audiobooks.html"])
        self.assertNotEqual(metas["samples.html"],metas["audiobooks.html"])
        self.assertEqual(len({metas[p] for p in metas if p!="home-v2.html"}),len(metas)-1)

    def test_book_edition_previews_remain_distinct(self):
        novel=meta((ROOT/"books/the-hollow-bell.html").read_text("utf-8"),"property","og:image")
        novella=meta((ROOT/"books/the-hollow-bell-novella.html").read_text("utf-8"),"property","og:image")
        self.assertNotEqual(novel,novella)
        self.assertTrue(novel.endswith("/book-the-hollow-bell.jpg"))
        self.assertTrue(novella.endswith("/book-the-hollow-bell-novella.jpg"))

    def test_original_buyers_and_analytics_are_preserved(self):
        catalog=__import__("json").loads((ROOT/"data/storefront-catalog.json").read_text("utf-8"))
        for book in catalog["books"]:
            text=(ROOT/book["book_page"]).read_text(encoding="utf-8")
            self.assertIn(book["payhip_url"],text)
            self.assertIn(book["sample_page"],text)
            self.assertIn(book["amazon_url"],text)
        home=(ROOT/"index.html").read_text("utf-8")
        self.assertIn('id="audiobooks"',home)
        self.assertIn("G-PHE2JVV5P6",home)

    def test_seo_workflow_preserves_the_images(self):
        flow=(ROOT/".github/workflows/seo-content-cleanup.yml").read_text(encoding="utf-8")
        self.assertIn("python scripts/apply_social_previews.py --write",flow)
        self.assertIn("python scripts/apply_social_previews.py --check",flow)
        build=(ROOT/"scripts/build_sitewide_preview.py").read_text(encoding="utf-8")
        self.assertIn("from apply_social_previews import apply_to_markup",build)

if __name__=="__main__":
    unittest.main()
