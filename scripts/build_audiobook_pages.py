from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
books=[
 dict(page="book-1-sample.html",slug="second-draft",title="Second Draft",genre="A Psychological Mystery Thriller",description="Nora helps people rehearse impossible conversations—until the rehearsals begin changing reality.",cover="second-draft.webp",book="../books/second-draft.html",chapter="../chapters/book-1-first-chapter.html",amazon="https://www.amazon.com/dp/B0HFYQ9KGV"),
 dict(page="book-2-sample.html",slug="the-hollow-year",title="The Hollow Year",genre="A Psychological Mystery Thriller",description="In Amity Hollow, one person is erased from every living memory each October.",cover="the-hollow-year.webp",book="../books/the-hollow-year.html",chapter="../chapters/book-2-first-chapter.html",amazon="https://www.amazon.com/dp/B0HFXF8MTP"),
 dict(page="book-3-sample.html",slug="the-hollow-bell",title="The Hollow Bell",genre="A Psychological Mystery Thriller • Supernatural",description="Twenty years after Marnie Renner vanished, her remains surface beneath the ice—and a bell tied to old drownings starts ringing again.",cover="the-hollow-bell.webp",book="../books/the-hollow-bell.html",chapter="../chapters/book-3-first-chapter.html",amazon="https://www.amazon.com/dp/B0HD52HGGZ"),
 dict(page="book-4-sample.html",slug="the-absconding",title="The Absconding",genre="A Psychological Mystery Thriller",description="Del returns after her mother dies beside the family beehives. The hives fall silent, and an old family ritual says the story is wrong.",cover="the-absconding.webp",book="../books/the-absconding.html",chapter="../chapters/book-4-first-chapter.html",amazon="https://www.amazon.com/dp/B0HDWRVSXQ"),
 dict(page="book-5-sample.html",slug="the-correction",title="The Correction",genre="A Psychological Mystery Thriller",description="A correction slip changes more than the official record—it changes what Averill Falls remembers.",cover="the-correction.webp",book="../books/the-correction.html",chapter="../chapters/book-5-first-chapter.html",amazon="https://www.amazon.com/dp/B0HFV8KCVL"),
]
narrators=[
 ("vivian-arlow","Vivian Arlow","Dark Velvet Female","Dark, intimate, and cinematic. The JayTree default voice for psychological suspense.",True),
 ("helena-corven","Helena Corven","Mature Female","Measured and atmospheric, with a mature storytelling presence.",False),
 ("grant-orlin","Grant Orlin","Gentle Gravel Male","Warm gravel and grounded suspense with a restrained dramatic edge.",False),
 ("edwin-lorren","Edwin Lorren","Mature Male","Steady, resonant, and deliberate for a classic mystery feel.",False),
]

for b in books:
    audio_objects=[]
    for ns,name,style,desc,rec in narrators:
        audio_objects.append({"@type":"AudioObject","name":f"{b['title']} — {name} Chapter One preview","contentUrl":f"https://jaytreebooks.com/audio/narrator-previews/{b['slug']}/{ns}.mp3","encodingFormat":"audio/mpeg","inLanguage":"en"})
    schema=json.dumps({"@context":"https://schema.org","@graph":[{"@type":"WebPage","url":f"https://jaytreebooks.com/audio/{b['page']}","name":f"{b['title']} — Choose Your Narrator | JayTree Books","description":f"Listen to Chapter One of {b['title']} with four JayTree narrator choices."},*audio_objects]},ensure_ascii=False,separators=(",",":"))
    cards=[]
    for ns,name,style,desc,rec in narrators:
        badge='<span class="narrator-badge">Recommended Narrator</span>' if rec else ''
        cards.append(f'''<article class="narrator-card{" recommended" if rec else ""}">
          {badge}
          <div class="voice-type">{style}</div>
          <h3>{name}</h3>
          <p>{desc}</p>
          <audio data-narrator="{name}" controls preload="metadata" aria-label="{b['title']} narrated by {name}">
            <source src="narrator-previews/{b['slug']}/{ns}.mp3" type="audio/mpeg">
            Your browser does not support audio playback.
          </audio>
          <small class="preview-note">Opening credits • Chapter One • Closing credits</small>
        </article>''')
    html=f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="referrer" content="strict-origin-when-cross-origin">
<title>{b['title']} — Choose Your Narrator | JayTree Books</title>
<meta name="description" content="Listen to Chapter One of {b['title']} with four narrator choices from JayTree Books. Compare voices before choosing your audiobook edition.">
<link rel="canonical" href="https://jaytreebooks.com/audio/{b['page']}">
<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">
<meta property="og:type" content="website"><meta property="og:title" content="{b['title']} — Choose Your Narrator"><meta property="og:description" content="Four narrator choices. Listen to Chapter One before you choose."><meta property="og:image" content="https://jaytreebooks.com/images/optimized/{b['cover']}">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="manifest" href="/manifest.webmanifest"><link rel="stylesheet" href="/pwa.css"><link rel="stylesheet" href="audiobook-experience.css">
<meta name="theme-color" content="#070b0f">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag('js',new Date());gtag('config','G-PHE2JVV5P6');</script>
<script type="application/ld+json">{schema}</script>
</head>
<body data-book="{b['slug']}" style="--book-cover:url('../images/optimized/{b['cover']}')">
<header class="audio-nav"><a class="brand" href="../index.html">JAYTREE BOOKS</a><a class="nav-back" href="{b['book']}" data-track="audio_book_page">Back to the Book</a></header>
<main class="audio-page">
  <section class="audio-hero">
    <img class="audio-cover" src="../images/optimized/{b['cover']}" alt="{b['title']} book cover">
    <div>
      <div class="eyebrow">Choose Your Narrator</div>
      <h1>{b['title']}</h1>
      <div class="voice-type">{b['genre']}</div>
      <p class="lede">{b['description']} Listen to the same Chapter One in four distinct JayTree voices, then choose the narrator you want for the Classic audiobook edition.</p>
      <div class="sequence">Opening credits • Chapter One • Closing credits</div>
    </div>
  </section>
  <section aria-labelledby="choose-title">
    <div class="chooser-head">
      <div><div class="eyebrow">Classic Edition</div><h2 id="choose-title">Four voices. One story. Your choice.</h2></div>
      <p>Every preview includes the complete opening credit, Chapter One, and closing credit in the selected narrator's voice. Vivian Arlow is the JayTree recommended default.</p>
    </div>
    <div class="narrator-grid">{''.join(cards)}</div>
  </section>
  <section class="immersive" aria-labelledby="immersive-title">
    <div class="immersive-copy">
      <span class="coming">Coming Soon</span>
      <div class="eyebrow" style="margin-top:18px">Premium Listening Option</div>
      <h2 id="immersive-title">JayTree Immersive Experience</h2>
      <p>A more cinematic audiobook experience built around Vivian Arlow's narration, with selective approved character voices, sparse story-driven sound effects, and short score moments—without burying the words under constant music.</p>
    </div>
    <div class="immersive-list"><span>Vivian Arlow core narration</span><span>Selective character performances</span><span>Sparse cinematic SFX & score</span><span>Immersive sample coming soon</span></div>
  </section>
  <div class="actions"><a class="cta primary" href="{b['book']}" data-track="audio_book_page">Explore the Book</a><a class="cta" href="{b['chapter']}" data-track="audio_chapter">Read Chapter One</a><a class="cta" href="{b['amazon']}" target="_blank" rel="noopener" data-track="audio_kindle_unlimited">Continue on Amazon</a></div>
  <p class="site-note"><strong>Audiobook editions are in production.</strong> These listening previews let you compare narrator choices before the full Classic and Immersive editions are released.</p>
</main>
<script src="audiobook-experience.js"></script><script src="/pwa.js" defer></script>
</body></html>'''
    html = "\n".join(line.rstrip() for line in html.splitlines()) + "\n"
    (ROOT/"audio"/b["page"]).write_text(html,encoding="utf-8")
print("BUILT",len(books),"audiobook pages")
