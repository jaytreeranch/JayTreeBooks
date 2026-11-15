"use strict";
const test = require("node:test");
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const root = path.resolve(__dirname, "..");
const read = (p) => fs.readFileSync(path.join(root, p), "utf8");
const site = "G-PHE2JVV5P6";

test("all 35 sitemap routes have the configured GA4 measurement ID", () => {
  const xml = read("sitemap.xml");
  const urls = [...xml.matchAll(/<loc>https:\/\/jaytreebooks\.com([^<]*)<\/loc>/g)];
  assert.equal(urls.length, 35, "update coverage when the sitemap expands");
  for (const match of urls) {
    const file = !match[1] || match[1] === "/" ? "home-v2.html" : match[1].replace(/^\//, "");
    const markup = read(file);
    assert.ok(markup.includes(site), file + " missing GA4 ID");
    assert.match(markup, /gtag\s*\(\s*['"]config['"]/, file + " missing GA4 config");
  }
});

test("all public legal pages have host-scoped analytics and campaign helper", () => {
  for (const name of ["privacy.html", "terms.html"]) {
    const markup = read(name);
    assert.ok(markup.includes(site), name);
    assert.ok(markup.includes("location.hostname"), name);
    assert.match(markup, /src="\/tracking\.js"/, name);
    assert.equal((markup.match(/gtag\('config'/g) || []).length, 1, name + " duplicate config");
  }
});

test("all six narrator sample pages capture campaign attribution and first play/complete", () => {
  for (let id = 1; id <= 6; id++) {
    const name = "audio/book-" + id + "-sample.html";
    const markup = read(name);
    assert.match(markup, /src="\/tracking\.js"/, name);
    assert.ok(markup.includes("audio_sample_play"), name + " no play event");
    assert.ok(markup.includes("audio_sample_complete"), name + " no complete event");
    assert.ok(markup.includes(site), name + " no GA4");
  }
});

test("newsletter signup intent is separate from verified signup and private auth is excluded", () => {
  assert.match(read("case-files.html"), /src="\/tracking\.js"/);
  assert.match(read("case-files.html"), /case_files_signup_submit/);
  assert.ok(!read("case-files-thanks.html").includes("'case_files_signup_complete'"));
  assert.match(read("case-files-thanks.html"), /case_files_signup_receipt_view/);
  assert.match(read("case-files-confirmed.html"), /is_verified_signup:false/);
  for (const name of ["social-poster.html", "tiktok-callback.html", "x-preview-test.html"]) {
    assert.ok(!read(name).includes(site), name + " should not send production analytics");
  }
});

test("retired generator cannot remove the shared audio helper if run later", () => {
  assert.match(read("scripts/build_audiobook_pages.py"), /src="\/tracking\.js"/);
});
