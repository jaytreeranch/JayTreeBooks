from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

index=ROOT/"index.html"
text=index.read_text(encoding="utf-8")
text=text.replace('<div class="eyebrow">Listen to the Stories</div>\n\t\t\t\t\t\t<h2>Hear the mystery.</h2>','<div class="eyebrow">Choose Your Narrator</div>\n\t\t\t\t\t\t<h2>Hear Chapter One your way.</h2>')
text=text.replace('<p>Hear a sample or watch a chapter reading. Full audiobook editions are coming soon.</p>','<p>Compare four Classic narrators for every title. Each preview includes opening credits, Chapter One, and closing credits. The JayTree Immersive Experience is coming soon.</p>')
index.write_text(text,encoding="utf-8")

app=ROOT/"app.js"
text=app.read_text(encoding="utf-8")
old='''function audioCard(b) {
  return `<article class="audio-card">
    <div class="audio-icon">◉</div><div class="format">Audiobook</div><h3>${b.title}</h3><p>${b.description}</p>
    <div class="card-actions">
      <a class="read-sample" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">Audio Sample</a>
      <a class="audible" href="books/${b.slug}.html#listen" data-track="book_audio" data-book="${b.slug}">Full Audiobook — Coming Soon</a>
    </div>
  </article>`;
}
'''
new='''function audioCard(b) {
  return `<article class="audio-card">
    <div class="audio-icon">◉</div><div class="format">Choose Your Narrator</div><h3>${b.title}</h3><p>${b.description}</p>
    <div class="card-actions">
      <a class="read-sample" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">Compare 4 Narrators</a>
      <a class="audible" href="${b.audio}#immersive-title" data-track="book_audio" data-book="${b.slug}">Immersive — Coming Soon</a>
    </div>
  </article>`;
}
'''
if old not in text:
    raise SystemExit("audioCard block not found")
text=text.replace(old,new)
text=text.replace(">Play Audio Sample</a>",">Choose Narrator & Listen</a>")
app.write_text(text,encoding="utf-8")

for name in ["second-draft.html","the-hollow-year.html","the-hollow-bell.html","the-absconding.html","the-correction.html"]:
    p=ROOT/"books"/name
    text=p.read_text(encoding="utf-8").replace(">Play Audio Sample</a>",">Choose Narrator & Listen</a>")
    p.write_text(text,encoding="utf-8")

book=ROOT/"book.html"
book.write_text(book.read_text(encoding="utf-8").replace(">Play Audio Sample</a>",">Choose Narrator & Listen</a>"),encoding="utf-8")
print("WIRED_SITE")
