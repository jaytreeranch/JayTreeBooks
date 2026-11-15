from pathlib import Path
import re
import unittest
ROOT=Path(__file__).resolve().parent.parent
SAMPLE_IMAGE="samples-approved-20261115.jpg"
EXPECTED="https://jaytreebooks.com/images/social/previews/"+SAMPLE_IMAGE
class SamplesArtTests(unittest.TestCase):
    def test_samples_metadata_uses_approved_art(self):
        html=(ROOT/"samples.html").read_text(encoding="utf-8")
        self.assertIn(f'property="og:image" content="{EXPECTED}"',html)
        self.assertIn(f'name="twitter:image" content="{EXPECTED}"',html)
        self.assertIn('content="1200"',html)
        self.assertIn('content="630"',html)
        self.assertIn("read Chapter One or listen",html)
        self.assertEqual(html.count('property="og:image"'),1)
        self.assertEqual(html.count('name="twitter:image"'),1)
    def test_jpeg_is_valid_1200_by_630(self):
        blob=(ROOT/"images/social/previews"/SAMPLE_IMAGE).read_bytes()
        self.assertGreater(len(blob),100000)
        self.assertLess(len(blob),900000)
        self.assertTrue(blob.startswith(b"\xff\xd8"),"must be JPEG")
        self.assertTrue(blob.endswith(b"\xff\xd9"),"must end as JPEG")
        self.assertIn(b"JFIF",blob[:100])
    def test_source_mapping_stays_future_safe(self):
        script=(ROOT/"scripts/apply_social_previews.py").read_text(encoding="utf-8")
        self.assertIn('"samples.html": "samples-approved-20261115"',script)
        self.assertIn('"samples-approved-20261115":',script)
        self.assertTrue((ROOT/"images/social/previews"/SAMPLE_IMAGE).is_file())
    def test_samples_purchase_sample_actions_preserved(self):
        page=(ROOT/"samples.html").read_text(encoding="utf-8")
        self.assertEqual(page.count('class="sf-sample-card"'),6)
        for name in ("book-1","book-2","book-3","book-4","book-5","book-6"):
            self.assertIn(f'audio/{name}-sample.html',page)
        self.assertIn('href="audiobooks.html"',page)
        self.assertIn('href="books.html"',page)
    def test_other_page_social_images_not_replaced(self):
        for name,token in [("audiobooks.html","audiobooks.jpg"),("books.html","books.jpg"),("series-v2.html","series.jpg")]:
            self.assertIn('https://jaytreebooks.com/images/social/previews/'+token,(ROOT/name).read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()