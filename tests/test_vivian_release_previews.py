"""Safety and release-consistency regression for public Vivian excerpt refresh."""
import hashlib,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
ITEMS={
 1:("second-draft","75d898f8a8e59afc1b19a4af6b18d695c71fa7113166b5510b82c246418e4a7b","GejHn"),
 2:("the-hollow-year","47d15c9c2f426e3370ee261200488130aacf3c476754f80f409bdb9b60d4a101","Zf7tv"),
 3:("the-hollow-bell","b7d0d064f8f09c3a83b6ebdeb02432f02f71ebd53ce833d2ca392f5b27598046","0BeoF"),
 4:("the-absconding","3ad58795db4a4263a8105d43a5f29ed6fca4bc807b3488de346849bc417dddcb","q3GfL"),
 5:("the-correction","fcd573acde1f8b0813a7c690c85eaa1701600abeaa9f5c8c14f9c2db34867111","OPaGw"),
 6:("the-hollow-bell-novella","3f5556cf440799ba0de6139fc84166cfdc7ecfa8dbe1c1e46b15ef02a8a4927a","EWc5q")
}
class VivianLiveSaleQC(unittest.TestCase):
 def test_six_exact_hashes(self):
  for num,(slug,expected,sku) in ITEMS.items():
   with self.subTest(slug=slug):
    p=ROOT/"audio"/"narrator-previews"/slug/"vivian-arlow.mp3"
    self.assertTrue(p.is_file())
    self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),expected)
 def test_six_public_pages(self):
  for num,(slug,expected,sku) in ITEMS.items():
   with self.subTest(slug=slug):
    text=(ROOT/"audio"/f"book-{num}-sample.html").read_text(encoding="utf-8")
    self.assertIn(f"narrator-previews/{slug}/vivian-arlow.mp3",text)
    self.assertIn("https://payhip.com/b/"+sku,text)
    self.assertIn("$1.99",text)
    self.assertIn("final edition",text.lower())
    self.assertNotIn("Every preview includes the complete opening credit",text)
    self.assertNotIn("Listen to the same Chapter One in four distinct",text)
 def test_alternates_not_sold_as_vivian(self):
  for num in range(1,6):
   t=(ROOT/"audio"/f"book-{num}-sample.html").read_text(encoding="utf-8")
   self.assertIn("other voices",t.lower())
   self.assertIn("demonstrations",t.lower())
 def test_novella_link_and_no_stale_generator(self):
  cfg=(ROOT/"config.js").read_text(encoding="utf-8")
  app=(ROOT/"app.js").read_text(encoding="utf-8")
  self.assertRegex(cfg,r'"slug": "the-hollow-bell-novella"[\s\S]*?"audio": "audio/book-6-sample.html"')
  self.assertIn("Listen to Vivian Preview",app)
  self.assertIn('Vivian Preview &amp; Other Voice Demos',app)
  self.assertIn("Preserving certified", (ROOT/"scripts"/"build_audiobook_pages.py").read_text(encoding="utf-8"))
if __name__=="__main__":unittest.main()
