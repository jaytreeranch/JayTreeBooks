"""Regression checks for Hollow Bell edition badges and legacy audiobook social campaign links."""
import json
import re
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

class CampaignLinkAndBadges(unittest.TestCase):
 def test_books_have_distinct_corner_badges(self):
  text=(ROOT/"books.html").read_text("utf-8")
  self.assertEqual(text.count('class="sf-book-edition-badge"'),2)
  for slug,label in (("the-hollow-bell","Full Novel"),("the-hollow-bell-novella","Novella")):
   m=re.search(r'<a class="sf-cover" href="books/'+slug+r'\.html">(.+?)</a>',text,re.S)
   self.assertIsNotNone(m,slug)
   self.assertIn('class="sf-book-edition-badge"',m.group(1))
   self.assertIn(">"+label+"</span>",m.group(1))
  self.assertIn("the-hollow-bell-novella.webp",text)
  self.assertIn("the-hollow-bell.webp",text)

 def test_home_tiles_show_same_two_badges(self):
  text=(ROOT/"home-v2.html").read_text("utf-8")
  self.assertEqual(text.count('class="jt-home-edition-badge"'),2)
  self.assertIn('jt-home-edition-badge" aria-hidden="true">Full Novel',text)
  self.assertIn('jt-home-edition-badge" aria-hidden="true">Novella',text)

 def test_legacy_social_link_is_redirected_not_replaced(self):
  home=(ROOT/"home-v2.html").read_text("utf-8")
  source=(ROOT/"home-links.js").read_text("utf-8")
  self.assertIn('id="audiobooks"',home) # no fallback lost
  self.assertIn('src="home-links.js"',home)
  self.assertIn("audiobooks: 'audiobooks.html'",source)
  self.assertIn("anchor !== 'audiobooks'",source)
  self.assertIn("target.search = location.search",source)
  self.assertIn("location.replace(target.href)",source)
  self.assertIn("window.addEventListener('hashchange', openBookmark)",source)
  self.assertIn("about: 'about.html'",source)

 def test_specific_offer_and_narrator_copy_unchanged(self):
  catalog=json.loads((ROOT/"data/storefront-catalog.json").read_text("utf-8"))
  entries={x["slug"]:x for x in catalog["books"]}
  self.assertEqual(len(entries),6)
  self.assertEqual(entries["the-hollow-bell"]["payhip_url"],"https://payhip.com/b/0BeoF")
  self.assertEqual(entries["the-hollow-bell-novella"]["payhip_url"],"https://payhip.com/b/EWc5q")
  for entry in entries.values():
   self.assertEqual(entry["audiobook_status"],"available")
   self.assertEqual(entry["narrator"],"Vivian")
   self.assertEqual(entry["audiobook_price_usd"],"1.99")
  shop=(ROOT/"audiobooks.html").read_text("utf-8")
  for entry in entries.values():
   self.assertIn(entry["payhip_url"],shop)
   self.assertIn(entry["sample_page"],shop)

 def test_css_has_positioned_badges_and_responsive_sizing(self):
  css=(ROOT/"cinematic-site-v2.css").read_text("utf-8")
  self.assertIn(".sf-book-edition-badge",css)
  self.assertIn(".jt-home-edition-badge",css)
  self.assertIn("position:absolute",css)
  self.assertIn("@media(max-width:430px)",css)

if __name__=="__main__":
 unittest.main()