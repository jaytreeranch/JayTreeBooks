'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const root = path.join(__dirname, '..');
const html = name => fs.readFileSync(path.join(root, name), 'utf8');
const pages = ['home-v2.html', 'books.html', 'audiobooks.html', 'samples.html'];
const offers = [
  ['second-draft', 'GejHn', 'audio/book-1-sample.html', 'B0HFYQ9KGV'],
  ['the-hollow-year', 'Zf7tv', 'audio/book-2-sample.html', 'B0HFXF8MTP'],
  ['the-hollow-bell', '0BeoF', 'audio/book-3-sample.html', 'B0HD52HGGZ'],
  ['the-hollow-bell-novella', 'EWc5q', 'audio/book-6-sample.html', 'B0HD2H8586'],
  ['the-absconding', 'q3GfL', 'audio/book-4-sample.html', 'B0HDWRVSXQ'],
  ['the-correction', 'OPaGw', 'audio/book-5-sample.html', 'B0HFV8KCVL']
];

for (const file of pages) {
  test(`${file} has crawlable static content, accessible landmarks, and preview guard`, () => {
    const page = html(file);
    assert.match(page, /<html lang="en">/);
    assert.match(page, /<main id="main">/);
    assert.match(page, /<a class="sf-skip" href="#main">/);
    assert.match(page, /<nav[^>]+aria-label="Primary navigation"/);
    assert.match(page, /<nav aria-label="Mobile navigation">/);
    assert.match(page, /<meta name="robots" content="noindex,follow">/);
    assert.match(page, /<h1>[^]*?<\/h1>/);
    assert.match(page, /<img src="icons\/icon-192\.png" alt=""/);
    assert.match(page, /href="storefront-v2\.css"/);
    assert.match(page, /src="storefront-v2\.js"/);
    assert.match(page, /Preview hosts never send QA clicks or visits/);
    assert.match(page, /window\.location\.hostname/);
    assert.match(page, /document\.head\.appendChild\(jtAnalytics\)/);
    assert.doesNotMatch(page, /<script[^>]*src="app\.js"/);
    assert.doesNotMatch(page, /Full Audiobook — Coming Soon|Audiobook editions are in production/);
  });
}

test('all six Vivian offers are purchasable, separate, and edition-specific on the audiobook catalog', () => {
  const page = html('audiobooks.html');
  assert.equal((page.match(/data-track="audiobook_payhip"/g) || []).length, offers.length + 1, "six shelf links and one featured link");
  assert.equal((page.match(/class="sf-cine-product(?: is-selected)?"/g) || []).length, offers.length);
  assert.equal((page.match(/class="sf-cine-cover-link sf-cine-select"/g) || []).length, offers.length);
  for (const [slug, sku, sample] of offers) {
    assert.match(page, new RegExp(`href="https://payhip\\.com/b/${sku}"[^>]*data-track="audiobook_payhip" data-book="${slug}"`));
    assert.ok(page.includes(`href="${sample}"`), `missing ${slug} sample`);
  }
  assert.match(page, /Alternative narrator editions coming soon/);
  assert.match(page, /id="sf-cine-featured-cover"/);
  assert.match(page, /id="sf-cine-featured-buy"/);
  assert.match(page, /Vivian is the only complete narrator edition available to buy today/);
  assert.match(page, /MP3 \+ chaptered M4B/);
  assert.match(page, /Six complete audiobooks — available now/);
});

test('books catalog is directly accessible without JS and all six Amazon links remain original', () => {
  const page = html('books.html');
  assert.equal((page.match(/class="sf-book-card"/g) || []).length, 6);
  for (const [slug, sku, sample, asin] of offers) {
    assert.ok(page.includes(`href="https://www.amazon.com/dp/${asin}"`), slug);
    assert.ok(page.includes(`href="books/${slug}.html"`), slug);
  }
  assert.match(page, /five full novels/);
  assert.match(page, /separate Amazon edition/);
});

test('six samples resolve to existing audio preview HTML routes; novella is separate', () => {
  const page = html('samples.html');
  for (const [slug, , sample] of offers) {
    assert.ok(page.includes(`href="${sample}"`), slug);
  }
  assert.match(page, /Vivian's six complete audiobooks are available for purchase now/);
  assert.match(page, /full-length narrations are coming soon/);
});

test('shortened homepage sends visitors to books, audiobooks, or samples immediately', () => {
  const page = html('home-v2.html');
  assert.match(page, /data-placement="home_hero">Explore books/);
  assert.match(page, /data-placement="home_hero">Shop audiobooks/);
  assert.match(page, /href="samples\.html" data-track="storefront_samples" data-placement="home_path"/);
  assert.match(page, /Explore free samples/);
  assert.match(page, /Six complete Vivian audiobooks/);
  assert.match(page, /Alternative full-length narrator editions are coming soon/);
});

test('all new pages use real book covers and avoid invented mockup image assets', () => {
  for (const file of pages) {
    const page = html(file);
    for (const match of page.matchAll(/<img[^>]+src="([^"]+)"/g)) {
      assert.ok(/^images\/optimized\/[a-z-]+\.webp$/.test(match[1]) || match[1] === 'icons/icon-192.png', match[1]);
    }
  }
});

test('tracking records intent without claiming a sale or intercepting purchase navigation', () => {
  const script = html('storefront-v2.js');
  assert.match(script, /document.addEventListener\("click"/);
  assert.match(script, /closest\("a\[data-track\]"\)/);
  assert.match(script, /window.gtag\("event", link.dataset.track/);
  assert.doesNotMatch(script, /preventDefault\(|gtag\(['"]event['"],\s*['"]purchase|gtag\(['"]event['"],\s*['"]sign_up/);
});

test('CSS supports mobile layouts, motion preferences and visible keyboard focus', () => {
  const css = html('storefront-v2.css');
  assert.match(css, /@media\(max-width:430px\)/);
  assert.match(css, /@media\(max-width:700px\)/);
  assert.match(css, /prefers-reduced-motion:reduce/);
  assert.match(css, /:focus-visible/);
  assert.match(css, /\.sf-product-grid\{display:grid/);
});

test('cinematic featured book selector uses real card data and never invents purchase URLs', () => {
  const page = html('audiobooks.html');
  const script = html('storefront-v2.js');
  for (const [slug, sku, sample] of offers) {
    assert.match(page, new RegExp('data-select-book="' + slug + '"'));
    assert.match(page, new RegExp('data-book="' + slug + '"'));
    assert.ok(page.includes('https://payhip.com/b/' + sku));
    assert.ok(page.includes('href="' + sample + '"'));
  }
  assert.match(script, /featuredBuy\.href = purchase\.href/);
  assert.match(script, /featuredSample\.href = preview\.getAttribute/);
  assert.match(script, /featuredCover\.src = thumbnail\.getAttribute/);
  assert.match(script, /featuredDescription\.textContent = card\.dataset\.description/);
  assert.match(script, /scrollIntoView/);
  assert.match(script, /aria-pressed/);
});

test('catalog uses a single JSON source and static generator to make future books easy to add', () => {
  const catalog = JSON.parse(html('data/storefront-catalog.json'));
  assert.equal(catalog.schema_version, 1);
  assert.equal(catalog.books.length, offers.length);
  assert.equal(catalog.books.filter(x => x.audiobook_status === 'available').length, offers.length);
  for (const [slug, sku] of offers) {
    const row = catalog.books.find(x => x.slug === slug);
    assert.equal(row.payhip_url, 'https://payhip.com/b/' + sku);
    assert.equal(row.book_status, 'published');
    assert.equal(row.audiobook_status, 'available');
  }
  const generator = html('scripts/build_storefront_catalog.py');
  assert.match(generator, /book_status/);
  assert.match(generator, /audiobook_status/);
  assert.match(generator, /--check/);
});
