'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const read = file => fs.readFileSync(path.join(__dirname, '..', file), 'utf8');
const allSix = [
  ['the-absconding', 'https://payhip.com/b/q3GfL'],
  ['the-hollow-year', 'https://payhip.com/b/Zf7tv'],
  ['second-draft', 'https://payhip.com/b/GejHn'],
  ['the-correction', 'https://payhip.com/b/OPaGw'],
  ['the-hollow-bell', 'https://payhip.com/b/0BeoF'],
  ['the-hollow-bell-novella', 'https://payhip.com/b/EWc5q'],
];

test('homepage clearly states six Vivian editions are available, alternatives only coming soon', () => {
  const html = read('index.html');
  assert.match(html, /All six complete audiobooks are available now, narrated by Vivian/);
  assert.match(html, /alternative full-length narrator editions are coming soon/i);
  assert.match(html, /Six complete Vivian audiobooks — \$1\.99 each/);
  assert.doesNotMatch(html, /(?:full|complete|novella) audiobooks?[^<.]{0,60}coming soon/i);
});

test('mystery book hub no longer claims Hollow Bell novella audiobook is unreleased', () => {
  const html = read('mystery-books.html');
  assert.match(html, /complete Vivian-narrated audiobook is available now for \$1\.99/);
  assert.match(html, /alternative narrator editions are coming soon/);
  assert.doesNotMatch(html, /Its audiobook is coming soon/);
});

for (const [slug, url] of allSix) {
  test(slug + ' book page advertises Vivian now and other complete voices later', () => {
    const html = read('books/' + slug + '.html');
    assert.match(html, /Vivian Audiobook/i);
    assert.match(html, /(?:Vivian's complete edition is available now|complete Vivian edition is available now)/i);
    assert.match(html, /alternative full-length (?:narrations|narrator editions) are coming soon/i);
    assert.match(html, /\$1\.99/);
    assert.ok(html.includes('href="' + url + '"'));
    assert.doesNotMatch(html, /(?:full|complete|novella) audiobook[^<.]{0,50}coming soon/i);
    if (slug !== 'the-hollow-bell-novella') {
      assert.doesNotMatch(html, /audiobook release news/);
      assert.match(html, /updates when alternative full-length narrators are released/);
    }
  });
}

for (let number = 1; number <= 5; number++) {
  test('narrator comparison ' + number + ' labels only alternate complete voices as coming soon', () => {
    const html = read('audio/book-' + number + '-sample.html');
    assert.match(html, /available now in Vivian Arlow's voice/);
    assert.match(html, /Alternative full-length narrator editions are coming soon/);
    assert.equal((html.match(/Alternative full-length narration coming soon/g) || []).length, 3);
    assert.match(html, /Immersive sample in development/);
    assert.doesNotMatch(html, /Audiobook editions are in production/);
    assert.doesNotMatch(html, /<span class="coming">Coming Soon<\/span>/);
    assert.equal((html.match(/data-track="audiobook_payhip"/g) || []).length, 2);
  });
}

test('dynamic book template cannot claim released audiobook is coming soon', () => {
  const js = read('app.js');
  assert.doesNotMatch(js, /Full Audiobook — Coming Soon|Audiobook Coming Soon|audiobook_coming_soon|JAYTREE_AUDIOBOOK_DIRECT_COMING_SOON/);
  assert.match(js, /Vivian Audiobook Available Now/);
  assert.match(js, /alternative full-length narrator editions are coming soon/i);
  assert.match(js, /audiobookPurchaseUrl\(b\) \? /);
  assert.match(js, /return "";\s*}\s*function track/);
});
