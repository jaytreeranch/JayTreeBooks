const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const read = p => fs.readFileSync(path.join(root, p), 'utf8');
test('novella is the sixth distinct book and has its own Amazon ASIN', () => {
  const books = JSON.parse(read('data/books.json'));
  assert.equal(books.length, 6);
  assert.equal(new Set(books.map(book => book.slug)).size, 6);
  const novella = books.find(book => book.slug === 'the-hollow-bell-novella');
  const novel = books.find(book => book.slug === 'the-hollow-bell');
  assert.equal(novella.amazonUrl, 'https://www.amazon.com/dp/B0HD2H8586');
  assert.equal(novel.amazonUrl, undefined); // static data catalog does not store novel purchase links
  assert.equal(novella.format, 'novella');
  assert.equal(novella.kindleUnlimited, false);
});
test('homepage renders six crawlable cards and distinct novella purchase link', () => {
  const home = read('index.html');
  assert.equal((home.match(/data-book-card="/g) || []).length, 6);
  assert.match(home, /data-book-card="the-hollow-bell-novella"/);
  assert.match(home, /https:\/\/www\.amazon\.com\/dp\/B0HD2H8586/);
  assert.match(home, /five JayTree mystery novels and The Hollow Bell novella/i);
  assert.match(home, /Five novels on Kindle Unlimited\. Plus a novella on Amazon\./);
  assert.doesNotMatch(home, /Every current JayTree Books title is available/);
});
test('novella page links verified formats and the live Vivian $1.99 audiobook', () => {
  const p = read('books/the-hollow-bell-novella.html');
  assert.match(p, /B0HD2H8586/);
  assert.match(p, /B0HD2KL44Q/);
  assert.match(p, /B0HFT5VDRL/);
  assert.match(p, /https:\/\/payhip\.com\/b\/EWc5q/);
  assert.match(p, /\$1\.99/);
  assert.doesNotMatch(p, /The novella audiobook is coming soon/i);
  assert.match(p, /href="the-hollow-bell.html"/);
  const match = p.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  assert.ok(match);
  const obj = JSON.parse(match[1]);
  assert.equal(obj['@type'], 'Book');
  assert.equal(obj.offers.url, 'https://www.amazon.com/dp/B0HD2H8586');
});
test('dynamic catalog presents the released novella Vivian audio preview', () => {
  const config = read('config.js');
  assert.match(config, /"slug": "the-hollow-bell-novella"/);
  assert.match(config, /"kindleUnlimited": false/);
  assert.match(config, /"audio": "audio\/book-6-sample.html"/);
  const app = read('app.js');
  assert.match(app, /b\.format === "novella"/);
  assert.match(app, /b\.chapter \?/);
  assert.match(app, /b\.audio \?/);
  assert.match(app, /Listen to Vivian Preview/);
});
test('novel, mystery hub and sitemap link to the novella', () => {
  assert.match(read('books/the-hollow-bell.html'), /href="the-hollow-bell-novella.html"/);
  assert.match(read('mystery-books.html'), /href="books\/the-hollow-bell-novella.html"/);
  assert.match(read('sitemap.xml'), /books\/the-hollow-bell-novella\.html/);
});

test('legacy site generator preserves editorial pages and skips unavailable novella samples', () => {
  const generator = read('scripts/build_reader_growth_site.py');
  assert.match(generator, /if not book\.get\("chapter"\)/);
  assert.match(generator, /Preserved existing book page/);
  assert.match(generator, /Retain the editorial sitemap/);
  const audioSeo = read('scripts/apply_audio_seo.py');
  assert.match(audioSeo, /Modern narrator pages use/);
});

test('published novella remains distinct across legacy build automation', () => {
  const workflow = read('.github/workflows/build-reader-growth-site.yml');
  assert.match(workflow, /build_storefront_catalog\.py --write/);
  const offers = JSON.parse(read('data/storefront-catalog.json')).books;
  const editions = offers.filter(book => book.slug.startsWith('the-hollow-bell'));
  assert.equal(editions.length, 2);
  assert.equal(new Set(editions.map(book => book.amazon_url)).size, 2);
  assert.equal(new Set(editions.map(book => book.payhip_url)).size, 2);
  const seo = read('scripts/seo_content_cleanup.py');
  assert.match(seo, /books\/the-hollow-bell-novella\.html/);
  assert.match(read('scripts/add_audiobook_coming_soon.py'), /Preserved novella audiobook release gate/);
  assert.match(read('scripts/qc_repair_site.py'), /if not book\.get\("audio"\)/);
  const sitemap = read('sitemap.xml');
  for (const book of editions) {
    assert.ok(sitemap.includes('/' + book.book_page + '</loc>'));
    assert.ok(sitemap.includes('/' + book.sample_page + '</loc>'));
  }
});

test('the current audiobook anchors resolve in both editions', () => {
  assert.match(read('app.js'), /books\/\$\{b\.slug\}\.html#audiobook/);
  for (const edition of ['the-hollow-bell', 'the-hollow-bell-novella']) {
    assert.match(read('books/' + edition + '.html'), /id="audiobook"/);
  }
});

test('automation does not promise the novella participates in Kindle Unlimited', () => {
  assert.match(read('scripts/apply_site_improvements.py'), /Five novels on Kindle Unlimited\. Plus a novella on Amazon/);
  assert.match(read('scripts/seo_content_cleanup.py'), /Discover five JayTree mystery novels and The Hollow Bell novella/);
  for (const entry of ['index.html', 'home-v2.html', 'books.html']) {
    assert.doesNotMatch(read(entry), /Every current JayTree Books title is available/);
  }
});
