'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const books = [
  ['second-draft', 1, 'https://payhip.com/b/GejHn'],
  ['the-hollow-year', 2, 'https://payhip.com/b/Zf7tv'],
  ['the-hollow-bell', 3, 'https://payhip.com/b/0BeoF'],
  ['the-absconding', 4, 'https://payhip.com/b/q3GfL'],
  ['the-correction', 5, 'https://payhip.com/b/OPaGw'],
];

for (const [slug, number, payhip] of books) {
  test(`audio sample ${slug} promotes live Vivian audiobook without misrepresenting others`, () => {
    const html = fs.readFileSync(path.join(__dirname, '..', 'audio', `book-${number}-sample.html`), 'utf8');
    assert.equal((html.match(/data-track="audiobook_payhip"/g) || []).length, 2);
    assert.equal((html.match(new RegExp(payhip, 'g')) || []).length, 2);
    assert.match(html, /complete audiobook is available now in Vivian Arlow's voice/i);
    assert.match(html, /Alternative full-length narrator editions are coming soon/);
    assert.equal((html.match(/Alternative full-length narration coming soon/g) || []).length, 3, 'only the three alternative narrators should have coming-soon badges');
    assert.match(html, /MP3 and chaptered M4B/);
    assert.doesNotMatch(html, /Audiobook editions are in production/);
    assert.doesNotMatch(html, /before the full Classic and Immersive editions are released/);
    assert.doesNotMatch(html, /document.querySelectorAll\('\[data-track\]'\).forEach/);
    assert.match(html, /audiobook-experience.js/);
    assert.match(html, /Immersive Experience/);
  });
}

test('narrator preview events and outbound actions have one authoritative binding', () => {
  const script = fs.readFileSync(path.join(__dirname, '..', 'audio', 'audiobook-experience.js'), 'utf8');
  assert.match(script, /audiobook_narrator_preview_play/);
  assert.match(script, /audiobook_narrator_preview_complete/);
  assert.match(script, /\[data-track\]/);
});

test('install option does not overlay mobile sales or reader actions', () => {
  const js = fs.readFileSync(path.join(__dirname, '..', 'pwa.js'), 'utf8');
  const css = fs.readFileSync(path.join(__dirname, '..', 'pwa.css'), 'utf8');
  assert.match(js, /querySelector\("footer"\) \|\| document.body/);
  assert.match(css, /\.pwa-install-button\{\s*position:static/);
  assert.doesNotMatch(css, /\.pwa-install-button\{[^}]*position:fixed/);
});

test('authoritative PWA generator matches shipped assets, preventing workflow regressions', () => {
  const generator = fs.readFileSync(path.join(__dirname, '..', 'scripts', 'apply_pwa.py'), 'utf8');
  const generatedJs = generator.split('PWA_JS = r"""')[1]?.split('"""')[0];
  const generatedCss = generator.split('PWA_CSS = r"""')[1]?.split('"""')[0]?.trim() + '\n';
  assert.ok(generatedJs, 'generated PWA JS is discoverable');
  const normalizeNewlines = value => value.replace(/\r\n?/g, '\n');
  assert.equal(normalizeNewlines(generatedJs), normalizeNewlines(fs.readFileSync(path.join(__dirname, '..', 'pwa.js'), 'utf8')));
  assert.equal(normalizeNewlines(generatedCss), normalizeNewlines(fs.readFileSync(path.join(__dirname, '..', 'pwa.css'), 'utf8')));
  assert.match(generator, /querySelector\("footer"\) \|\| document.body/);
});

test('authoritative audio SEO generator never rebinds narrator purchase clicks', () => {
  const generator = fs.readFileSync(path.join(__dirname, '..', 'scripts', 'apply_audio_seo.py'), 'utf8');
  assert.match(generator, /Outbound click events are registered once by audiobook-experience\.js/);
  assert.doesNotMatch(generator, /document\.querySelectorAll\('\[data-track\]'\)\.forEach/);
});
