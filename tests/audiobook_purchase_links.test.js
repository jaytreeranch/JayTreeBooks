'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const source = fs.readFileSync(path.join(__dirname, '..', 'app.js'), 'utf8');
const start = source.indexOf('const JT_AUDIOBOOK_PAYHIP');
const end = source.indexOf('function track(', start);
assert.ok(start >= 0 && end > start, 'purchase helper source exists');
const { purchaseUrl, button, callout } = new Function(
  source.slice(start, end) +
  '\nreturn {purchaseUrl:audiobookPurchaseUrl,button:audiobookPurchaseButton,callout:audiobookDirectCallout};'
)();
const approved = {
  'the-absconding': 'https://payhip.com/b/q3GfL',
  'the-hollow-year': 'https://payhip.com/b/Zf7tv'
};
const held = ['second-draft', 'the-correction', 'the-hollow-bell', 'the-hollow-bell-novella'];

test('only the two cleared titles have direct purchase URLs', () => {
  for (const [slug, url] of Object.entries(approved)) {
    assert.equal(purchaseUrl({ slug }), url);
    assert.match(button({ slug }), /Buy Vivian Audiobook.*\$1\.99/);
    assert.match(callout({ slug }), /Limited-Time \$1\.99/);
  }
  for (const slug of held) {
    assert.equal(purchaseUrl({ slug }), '');
    assert.equal(button({ slug }), '');
    assert.match(callout({ slug }), /Full Audiobook.*Coming Soon/);
  }
});

test('purchase links are allowlisted and safe for a new tab', () => {
  assert.equal((source.match(/https:\/\/payhip\.com\/b\//g) || []).length, 2);
  for (const slug of Object.keys(approved)) {
    const html = button({ slug });
    assert.match(html, /rel="noopener noreferrer"/);
    assert.match(html, /data-track="audiobook_payhip"/);
  }
});

test('index cards and book pages both include purchase CTA', () => {
  assert.match(source, /\$\{audiobookPurchaseButton\(b\)\}/);
  assert.match(source, /\$\{audiobookDirectCallout\(b\)\}/);
  assert.match(source, /JAYTREE_AUDIOBOOK_DIRECT_COMING_SOON/);
});
