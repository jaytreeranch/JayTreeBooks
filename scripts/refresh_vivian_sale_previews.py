#!/usr/bin/env python3
"""Hash-verified website replacement with exact public Payhip Vivian excerpts.
Only certified, already-public-sale excerpts. Do not copy full masters or private receipts.
"""
import argparse,hashlib,json,re,shutil
from pathlib import Path
ED={
"The Absconding":("the-absconding",4),
"The Hollow Year":("the-hollow-year",2),
"Second Draft":("second-draft",1),
"The Correction":("the-correction",5),
"The Hollow Bell (Novella)":("the-hollow-bell-novella",6),
"The Hollow Bell: A Millbrook Falls Mystery (Full Novel)":("the-hollow-bell",3),
}
def sha(p):
 h=hashlib.sha256()
 with open(p,"rb") as f:
  for x in iter(lambda:f.read(1048576),b""):h.update(x)
 return h.hexdigest()
def replace1(s,pattern,repl,slug,flags=0):
 new,num=re.subn(pattern,repl,s,count=1,flags=flags)
 if num!=1:raise RuntimeError("Expected markup missing in "+slug+": "+pattern[:40])
 return new
def run(site,manifest,staging):
 site=Path(site);j=json.loads(Path(manifest).read_text(encoding="utf-8-sig"));staging=Path(staging)
 assert len(j["editions"])==6
 jobs=[]
 for item in j["editions"]:
  title=item["title"];slug,ix=ED[title];data=item["files"]["preview"]
  rel=Path(data["relative_staging_path"])
  if rel.is_absolute() or ".." in rel.parts:raise RuntimeError("Unsafe path")
  source=staging/rel;target=site/"audio"/"narrator-previews"/slug/"vivian-arlow.mp3"
  if sha(source)!=data["sha256"].lower():raise RuntimeError("Incorrect release SHA "+slug)
  jobs.append((source,target,data["sha256"].lower(),slug,ix))
 for source,target,expected,slug,ix in jobs:
  target.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(source,target)
  assert sha(target)==expected
  print("AUDIO_PASS",slug,target.stat().st_size,expected)
 for source,target,expected,slug,ix in jobs:
  if ix==6:continue
  page=site/"audio"/f"book-{ix}-sample.html"
  t=page.read_text(encoding="utf-8-sig")
  t=replace1(t,r"Listen to the same Chapter One in four distinct JayTree voices, then hear how Vivian Arlow narrates the complete audiobook, available now for a limited-time \$1\.99\. Alternative full-length narrator editions are coming soon; other voices are available as previews now\.",
    "Listen to the exact Vivian preview from the finished audiobook available for $1.99. The other voices below are earlier demonstrations only; the sold complete edition uses Vivian.",slug)
  t=replace1(t,r'<div class="sequence">.*?</div>',
    '<div class="sequence">Final Vivian audiobook excerpt | Alternate narrator demos</div>',slug)
  t=replace1(t,r"Every preview includes the complete opening credit, Chapter One, and closing credit in the selected narrator.s voice\. The complete audiobook is available now in Vivian Arlow.s voice\. Alternative full-length narrator editions are coming soon; their Chapter One previews can already be played here\.",
    "Vivian's player contains the exact approved excerpt from the currently sold final edition. The complete audiobook is available now in Vivian Arlow's voice. Alternative full-length narrator editions are coming soon; the other voices are archived Chapter One narrator demonstrations, not currently purchasable as complete audiobooks.",slug)
  t=replace1(t,r'(<article class="narrator-card recommended">\s*)<span class="narrator-badge">Recommended Narrator</span>',r'\1<span class="narrator-badge">Available audiobook: Vivian — $1.99</span>',slug)
  t=replace1(t,r'(<audio data-narrator="Vivian Arlow".*?</audio>\s*<small class="preview-note">).*?(</small>)',r'\1Exact Vivian release preview from approved final edition\2',slug,re.S)
  t=replace1(t,rf'(<source src="narrator-previews/{slug}/vivian-arlow\.mp3)(" type="audio/mpeg">)',r'\1?v=vivian-20261114\2',slug)
  t=t.replace("Vivian Arlow Chapter One preview","Vivian Arlow final-edition audiobook excerpt")
  t=t.replace(f"https://jaytreebooks.com/audio/book-{ix}-sample.mp3",f"https://jaytreebooks.com/audio/narrator-previews/{slug}/vivian-arlow.mp3")
  page.write_text(t,encoding="utf-8")
 # New novella preview page, deliberately standalone (no stale four-voice generator).
 novella=site/"audio"/"book-6-sample.html"
 novella.write_text("""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Hollow Bell Novella — Vivian Audiobook Preview | JayTree Books</title>
<meta name="description" content="Listen to the approved final-edition Vivian preview for The Hollow Bell novella. Complete MP3/M4B audiobook $1.99 for a limited time.">
<link rel="canonical" href="https://jaytreebooks.com/audio/book-6-sample.html">
<link rel="stylesheet" href="audiobook-experience.css">
<meta property="og:title" content="The Hollow Bell Novella — Vivian Audiobook Preview">
<meta property="og:image" content="https://jaytreebooks.com/images/optimized/the-hollow-bell-novella.webp">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"AudioObject","name":"The Hollow Bell novella — final Vivian audiobook excerpt","contentUrl":"https://jaytreebooks.com/audio/narrator-previews/the-hollow-bell-novella/vivian-arlow.mp3","encodingFormat":"audio/mpeg","inLanguage":"en"}</script>
</head><body data-book="the-hollow-bell-novella" style="--book-cover:url('../images/optimized/the-hollow-bell-novella.webp')">
<header class="audio-nav"><a class="brand" href="../index.html">JAYTREE BOOKS</a><a class="nav-back" href="../books/the-hollow-bell-novella.html">Back to Novella</a></header>
<main class="audio-page"><section class="audio-hero">
<img class="audio-cover" src="../images/optimized/the-hollow-bell-novella.webp" alt="The Hollow Bell novella cover">
<div><div class="eyebrow">Available Now — Vivian Audiobook</div><h1>The Hollow Bell (Novella)</h1>
<p class="lede">Hear the exact approved Vivian excerpt from the complete novella audiobook. Limited-time sale: $1.99 each.</p>
<div class="sequence">Final Vivian audiobook excerpt</div>
<div class="actions"><a class="cta primary" data-track="audiobook_payhip" data-book="the-hollow-bell-novella" href="https://payhip.com/b/EWc5q" target="_blank" rel="noopener noreferrer">Buy Vivian Audiobook — $1.99</a></div></div></section>
<section aria-labelledby="listen-vivian"><div class="chooser-head"><div><div class="eyebrow">Hear the mystery</div><h2 id="listen-vivian">Listen to Vivian</h2></div>
<p>The exact preview from the final audiobook. The complete purchase includes MP3 and chaptered M4B; narrated using a digitally generated JayTree Books voice.</p></div>
<article class="narrator-card recommended"><span class="narrator-badge">Available audiobook: Vivian — $1.99</span>
<h3>Vivian Arlow</h3><audio controls preload="metadata" data-audio-sample aria-label="The Hollow Bell novella final Vivian audiobook preview">
<source src="narrator-previews/the-hollow-bell-novella/vivian-arlow.mp3" type="audio/mpeg">Your browser does not support audio playback.</audio>
<small class="preview-note">Exact Vivian release preview from approved final edition</small></article></section>
<div class="actions"><a class="cta primary" data-track="audiobook_payhip" data-book="the-hollow-bell-novella" href="https://payhip.com/b/EWc5q" target="_blank" rel="noopener noreferrer">Buy Complete Audiobook — $1.99</a>
<a class="cta" href="../books/the-hollow-bell-novella.html">Explore the Novella</a></div></main>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}gtag('js',new Date());gtag('config','G-PHE2JVV5P6');document.querySelectorAll('[data-track]').forEach(function(a){a.addEventListener('click',function(){if(typeof gtag==='function')gtag('event',a.dataset.track,{book:'the-hollow-bell-novella'})})})</script>
</body></html>""",encoding="utf-8")
 cfg=site/"config.js";text=cfg.read_text(encoding="utf-8-sig")
 text=replace1(text,r'("slug": "the-hollow-bell-novella".*?"cover": "images/optimized/the-hollow-bell-novella\.webp",)',r'\1\n      "audio": "audio/book-6-sample.html",',"config",re.S)
 cfg.write_text(text,encoding="utf-8")
 app=site/"app.js";text=app.read_text(encoding="utf-8-sig")
 link='<a class="read-sample" href="'+chr(36)+'{b.audio}" data-track="audio_preview" data-book="'+chr(36)+'{b.slug}">Listen to Vivian Preview</a>'
 text=replace1(text,r'(if \(b\.format === "novella"\).*?\$\{audiobookPurchaseButton\(b\)\})(</div>)',lambda m:m.group(1)+" "+link+m.group(2),"app",re.S)
 if "Preview 4 Narrators" not in text:raise RuntimeError("expected prior preview label")
 text=text.replace("Preview 4 Narrators","Vivian Preview &amp; Other Voice Demos",1)
 app.write_text(text,encoding="utf-8")
 print("PAGE_PASS 6 previews; current Vivian + preserved alternate demos, purchase links")
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("--site-root",required=True);p.add_argument("--manifest",required=True);p.add_argument("--release-root",required=True);a=p.parse_args()
 run(a.site_root,a.manifest,a.release_root)
