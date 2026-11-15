'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const html = fs.readFileSync(
  path.join(__dirname, '..', 'books', 'the-hollow-bell-novella.html'),
  'utf8'
);

test('novella metadata promotes the available audiobook, never the old coming-soon state', () => {
  const descriptions = [
    ...html.matchAll(/<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content="([^"]+)"/g)
  ].map(match => match[1]);
  assert.equal(descriptions.length, 3);
  assert.ok(descriptions.some(text => /audiobook/i.test(text)));
  for (const text of descriptions) assert.doesNotMatch(text, /audiobook.*coming soon/i);
});

test('novella keeps exactly one direct Payhip edition and a distinct full-novel reference', () => {
  assert.deepEqual(
    [...html.matchAll(/https:\/\/payhip\.com\/b\/[A-Za-z0-9]+/g)].map(match => match[0]),
    ['https://payhip.com/b/EWc5q', 'https://payhip.com/b/EWc5q']
  );
  assert.match(html, /data-track="audiobook_payhip"\s+data-book="the-hollow-bell-novella"/);
  assert.match(html, /MP3 and chaptered M4B/);
  assert.match(html, /digitally generated JayTree Books voice/);
});

test('novella outbound links bind delegated, book-specific click analytics', () => {
  assert.match(html, /document\.addEventListener\('click', function \(event\)/);
  assert.match(html, /closest\('a\[data-track\]'\)/);
  assert.match(html, /window\.gtag\('event', link\.dataset\.track,/);
  assert.match(html, /book: link\.dataset\.book \|\| 'the-hollow-bell-novella'/);
  assert.match(html, /transport_type: 'beacon'/);
});

test('novella mobile menu closes with Escape', () => {
  assert.match(html, /event\.key === 'Escape'/);
  assert.match(html, /toggle\.setAttribute\('aria-expanded', 'false'\)/);
});

test('novella registers the PWA script only once', () => {
  assert.equal((html.match(/<script src="\/pwa\.js" defer><\/script>/g) || []).length, 1);
  assert.match(html, /<!-- JAYTREE_PWA_SCRIPT_START -->/);
});
