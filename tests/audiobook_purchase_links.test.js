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
  'the-hollow-year': 'https://payhip.com/b/Zf7tv',
  'second-draft': 'https://payhip.com/b/GejHn',
  'the-correction': 'https://payhip.com/b/OPaGw',
  'the-hollow-bell-novella': 'https://payhip.com/b/EWc5q',
  'the-hollow-bell': 'https://payhip.com/b/0BeoF'
};
const notListed = ['where-mercy-stood', 'the-fifth-copy', 'unknown-title'];

test('exactly six independently ACX-cleared editions are allowlisted for a gated release', () => {
  for (const [slug, url] of Object.entries(approved)) {
    assert.equal(purchaseUrl({ slug }), url);
    assert.match(button({ slug }), /Buy Vivian Audiobook.*\$1\.99/);
    assert.match(callout({ slug }), /Limited-Time \$1\.99/);
  }
  for (const slug of notListed) {
    assert.equal(purchaseUrl({ slug }), '');
    assert.equal(button({ slug }), '');
    assert.match(callout({ slug }), /Full Audiobook.*Coming Soon/);
  }
});

test('purchase links are allowlisted and safe for a new tab', () => {
  assert.equal((source.match(/https:\/\/payhip\.com\/b\//g) || []).length, 6);
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

test('homepage static launch banner contains exactly the six staged editions', () => {
  const index = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const payhipLinks = index.match(/https:\/\/payhip\.com\/b\/[A-Za-z0-9]+/g) || [];
  assert.deepEqual(payhipLinks, Object.values(approved));
  assert.match(index, /Limited-Time Audiobook Offer/);
  assert.match(index, /data-book="the-absconding"/);
  assert.match(index, /data-book="the-hollow-year"/);
  for (const slug of Object.keys(approved)) assert.ok(index.includes(`data-book="${slug}"`));
});

test('the separate Hollow Bell novella has a direct-sale audiobook card', () => {
  assert.match(source, /Vivian Novella Audiobook/);
  assert.match(source, /if \(b\.format === "novella"\)/);
  assert.match(source, /\$\{audiobookPurchaseButton\(b\)\}/);
  assert.doesNotMatch(source, /Novella Audiobook — Coming Soon/);
});
