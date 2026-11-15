'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const books = Object.freeze({
  'the-absconding': 'https://payhip.com/b/q3GfL',
  'the-hollow-year': 'https://payhip.com/b/Zf7tv',
  'second-draft': 'https://payhip.com/b/GejHn',
  'the-correction': 'https://payhip.com/b/OPaGw',
  'the-hollow-bell': 'https://payhip.com/b/0BeoF',
  'the-hollow-bell-novella': 'https://payhip.com/b/EWc5q'
});

for (const [slug, url] of Object.entries(books)) {
  test('static book detail '+slug+' advertises only its certified Payhip audiobook', () => {
    const html = fs.readFileSync(path.join(__dirname, '..', 'books', slug+'.html'), 'utf8');
    const links = html.match(/https:\/\/payhip\.com\/b\/[A-Za-z0-9]+/g) || [];
    assert.equal(links.length, 2, 'the featured purchase bar and original audiobook callout must both point to the correct edition');
    assert.deepEqual([...new Set(links)], [url], 'no other Payhip SKU is allowed');
    assert.match(html, /\$1\.99/);
    assert.match(html, /data-track="audiobook_payhip"/);
    assert.match(html, /target="_blank" rel="noopener noreferrer"/);
    assert.doesNotMatch(html, /Full Audiobook — Coming Soon/);
    assert.doesNotMatch(html, /The novella audiobook is coming soon/);
    assert.doesNotMatch(html, /Audiobook • In Final Preparation/);
    assert.match(html, /MP3 and chaptered M4B/);
    assert.match(html, /digitally generated JayTree Books voice/);
    // The limited-time offer must not impose an automatic or advertised end date.
    assert.doesNotMatch(html, /Audiobook[^<]{0,150}(?:expires|ends on|until November|7 days from)/i);
  });
}

test('all six detail pages use distinct checkout URLs', () => {
  assert.equal(new Set(Object.values(books)).size, 6);
});
