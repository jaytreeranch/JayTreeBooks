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
  assert.match(home, /five dark mystery novels and a separate novella/);
});
test('novella page links verified purchase formats and gates audiobook', () => {
  const p = read('books/the-hollow-bell-novella.html');
  assert.match(p, /B0HD2H8586/);
  assert.match(p, /B0HD2KL44Q/);
  assert.match(p, /B0HFT5VDRL/);
  assert.match(p, /The novella audiobook is coming soon/);
  assert.doesNotMatch(p, /href="[^"]*(\.mp3|\.m4b|checkout|payhip)/i);
  assert.match(p, /href="the-hollow-bell.html"/);
  const match = p.match(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/);
  assert.ok(match);
  const obj = JSON.parse(match[1]);
  assert.equal(obj['@type'], 'Book');
  assert.equal(obj.offers.url, 'https://www.amazon.com/dp/B0HD2H8586');
});
test('dynamic catalog does not advertise a novella chapter or audio preview', () => {
  const config = read('config.js');
  assert.match(config, /"slug": "the-hollow-bell-novella"/);
  assert.match(config, /"kindleUnlimited": false/);
  const app = read('app.js');
  assert.match(app, /b\.format === "novella"/);
  assert.match(app, /b\.chapter \?/);
  assert.match(app, /b\.audio \?/);
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
