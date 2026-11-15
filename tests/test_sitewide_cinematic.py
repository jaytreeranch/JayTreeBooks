import json
import re
import unittest
from pathlib import Path
from urllib.parse import urlparse
from html.parser import HTMLParser
ROOT = Path(__file__).resolve().parent.parent
CATALOG = json.loads((ROOT/'data/storefront-catalog.json').read_text(encoding='utf-8'))
PAGES = ['home-v2.html','books.html','audiobooks.html','samples.html','series-v2.html','news-v2.html','experiences-v2.html']
LEGACY = ['about.html','upcoming-books.html','mystery-books.html','reading-guides.html','case-files.html','animated-series.html','privacy.html','terms.html','psychological-mystery-books.html','kindle-unlimited-mystery-books.html']
BOOKS = [b for b in CATALOG['books'] if b['book_status']=='published']
AUDIO_PAGES = list((ROOT/'audio').glob('book-*-sample.html'))
CHAPTER_PAGES = list((ROOT/'chapters').glob('book-*-first-chapter.html'))
def text(path):return (ROOT/path).read_text(encoding='utf-8')
class HrefCollector(HTMLParser):
    def __init__(self):super().__init__();self.links=[]
    def handle_starttag(self, tag,attrs):
        if tag=='a':self.links.append(dict(attrs).get('href',''))
class SitewideTests(unittest.TestCase):
    def test_shared_nav_in_every_major_page(self):
        all_pages=PAGES+LEGACY+[b['book_page'] for b in BOOKS]+[str(p.relative_to(ROOT)).replace('\\','/') for p in AUDIO_PAGES+CHAPTER_PAGES]
        self.assertEqual(len(all_pages),len(set(all_pages)))
        for file in all_pages:
            with self.subTest(file=file):
                page=text(file)
                self.assertEqual(page.count('class="jt-header"'),1)
                self.assertIn('cinematic-site-v2.css',page)
                self.assertIn('cinematic-site-v2.js',page)
                self.assertIn('aria-label="Primary navigation"',page)
                self.assertIn('aria-label="Mobile navigation"',page)
                self.assertIn('jt-cinematic',page)
    def test_new_page_navigation_destinations_resolve(self):
        for name in PAGES:
            page=text(name)
            links=HrefCollector();links.feed(page)
            for href in links.links:
                if not href or href.startswith(('mailto:','tel:','https:','http:','#')):continue
                clean=urlparse(href).path
                if clean:
                    with self.subTest(page=name,href=href):
                        self.assertTrue((ROOT/clean).is_file(),href)
    def test_book_detail_buy_buttons_are_correct(self):
        for book in BOOKS:
            page=text(book['book_page'])
            with self.subTest(book=book['slug']):
                self.assertIn(book['amazon_url'],page)
                self.assertIn(book['payhip_url'],page)
                self.assertIn('jt-detail-buy',page)
                self.assertIn('other narrators coming soon',page.lower())
                self.assertIn(book['sample_page'],page)
                if book['edition'] != 'Novella': self.assertIn('id="read-next"',page)
    def test_legacy_critical_content_preserved(self):
        self.assertIn('jaytree-books.kit.com',text('case-files.html'))
        self.assertIn('643W5-_bLPA',text('home-v2.html'))
        self.assertIn('R-5cB9FaVOA',text('experiences-v2.html'))
        self.assertIn('where-mercy-stood',text('upcoming-books.html'))
        self.assertIn('the next three mysteries',text('series-v2.html').lower())
        for book in BOOKS:
            self.assertIn('data-track="audiobook_payhip"',text(book['book_page']))
    def test_samples_scripts_and_long_form_text_preserved(self):
        self.assertEqual(len(AUDIO_PAGES),6)
        self.assertEqual(len(CHAPTER_PAGES),5)
        for p in AUDIO_PAGES:
            self.assertIn('audiobook-experience.css',p.read_text('utf-8'))
            self.assertIn('audio-page',p.read_text('utf-8'))
        for p in CHAPTER_PAGES:
            self.assertGreater(len(p.read_text('utf-8')),12000)
    def test_seller_links_exactly_six_in_catalog(self):
        page=text('audiobooks.html')
        for book in BOOKS:
            with self.subTest(slug=book['slug']):
                self.assertIn(book['payhip_url'],page)
                self.assertIn(book['sample_page'],page)
        self.assertEqual(len(set(b['payhip_url'] for b in BOOKS)),6)
    def test_preview_isolated_and_analytics_production_gated(self):
        for page in PAGES:
            self.assertIn('name="robots" content="noindex,follow"',text(page))
        for page in ['home-v2.html','series-v2.html','news-v2.html','experiences-v2.html']:
            source=text(page)
            self.assertIn('location.hostname==="jaytreebooks.com"',source)
            self.assertIn('tracking.js',source)
            self.assertNotIn('gtag("event","purchase"',source)
    def test_rebuild_is_clean(self):
        import subprocess,sys
        p=subprocess.run([sys.executable,str(ROOT/'scripts/build_sitewide_preview.py'),'--check'],cwd=ROOT,capture_output=True,text=True,timeout=25)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
if __name__=='__main__':unittest.main()