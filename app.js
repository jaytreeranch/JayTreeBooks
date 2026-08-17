const JT = window.JT;

function track(name, params = {}) {
  if (typeof gtag === "function") gtag("event", name, params);
}

function youtubeIdFromUrl(value) {
  if (!value) return "";
  value = String(value).trim().replace(/\\&/g, "&");

  if (/^[A-Za-z0-9_-]{6,}$/.test(value) && !value.includes("http")) return value;

  try {
    const u = new URL(value);

    if (u.hostname.includes("youtu.be")) {
      return u.pathname.split("/").filter(Boolean)[0] || "";
    }

    const watchId = u.searchParams.get("v");
    if (watchId) return watchId;

    const parts = u.pathname.split("/").filter(Boolean);

    const shortsIndex = parts.indexOf("shorts");
    if (shortsIndex >= 0 && parts[shortsIndex + 1]) return parts[shortsIndex + 1];

    const embedIndex = parts.indexOf("embed");
    if (embedIndex >= 0 && parts[embedIndex + 1]) return parts[embedIndex + 1];
  } catch (e) {}

  return "";
}

function youtubeEmbed(url, title) {
  const id = youtubeIdFromUrl(url);

  if (!id) {
    return `<div class="video-placeholder">
      <div class="youtube-mark">▶</div>
      <strong>No video added yet</strong>
      <small>Add the YouTube URL for this book in config.js.</small>
    </div>`;
  }

  return `<iframe
    src="https://www.youtube-nocookie.com/embed/${id}?rel=0"
    title="${title}"
    frameborder="0"
    referrerpolicy="strict-origin-when-cross-origin"
    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
    allowfullscreen>
  </iframe>`;
}

function externalButton(url, label, eventName, bookSlug) {
  if (!url) return "";
  return `<a class="cta" href="${url}" target="_blank" rel="noopener"
    data-track="${eventName}" data-book="${bookSlug}">${label}</a>`;
}

function bookCard(b) {
  return `<article class="card">
    <a class="cover" href="book.html?book=${b.slug}" aria-label="Explore ${b.title}">
      <img src="${b.cover}" alt="${b.title} book cover">
    </a>
    <div class="card-body">
      <div class="genre">${b.genre}</div>
      <h3>${b.title}</h3>
      <p>${b.description}</p>
      <div class="card-actions">
        <a class="read-sample" href="${b.chapter}" data-track="chapter" data-book="${b.slug}">
          Read First Chapter
        </a>
        <a class="buy" href="book.html?book=${b.slug}" data-track="book_page" data-book="${b.slug}">
          Explore Book
        </a>
      </div>
    </div>
  </article>`;
}

function audioCard(b) {
  return `<article class="audio-card">
    <div class="audio-icon">◉</div>
    <div class="format">Audiobook</div>
    <h3>${b.title}</h3>
    <p>${b.description}</p>
    <div class="card-actions">
      <a class="read-sample" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">
        Audio Sample
      </a>
      <a class="audible" href="book.html?book=${b.slug}#audiobook" data-track="book_audio" data-book="${b.slug}">
        Listen / Watch
      </a>
    </div>
  </article>`;
}

function bindTracking() {
  document.querySelectorAll("[data-track]").forEach(el => {
    el.addEventListener("click", () => {
      track(el.dataset.track, { book: el.dataset.book || "" });
    });
  });

  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();

  const toggle = document.querySelector(".menu-toggle");
  if (toggle) {
    toggle.addEventListener("click", () => {
      document.querySelector(".nav")?.classList.toggle("open");
    });
  }
}

function renderIndex() {
  const bookGrid = document.getElementById("book-grid");
  const audioGrid = document.getElementById("audio-grid");

  if (bookGrid) bookGrid.innerHTML = JT.books.map(bookCard).join("");
  if (audioGrid) audioGrid.innerHTML = JT.books.map(audioCard).join("");

  const featured = JT.books.find(b => b.slug === JT.featuredBook) || JT.books[0];
  const heroImage = document.querySelector(".hero-feature img");
  const heroTitle = document.querySelector(".hero-feature strong");
  const heroSmall = document.querySelector(".hero-feature small");

  if (heroImage) {
    heroImage.src = featured.cover;
    heroImage.alt = featured.title + " book cover";
  }
  if (heroTitle) heroTitle.textContent = featured.title;
  if (heroSmall) heroSmall.textContent = featured.description;

  bindTracking();
}

function relatedCards(book) {
  return JT.books
    .filter(x => x.slug !== book.slug)
    .slice(0, 3)
    .map(bookCard)
    .join("");
}

function renderBook() {
  const slug = new URLSearchParams(location.search).get("book") || JT.featuredBook;
  const b = JT.books.find(x => x.slug === slug) || JT.books[0];
  const page = document.getElementById("book-page");

  if (!page) return;

  document.title = `${b.title} | JayTree Books`;

  const trailerBlock = b.trailerUrl
    ? youtubeEmbed(b.trailerUrl, `${b.title} book trailer`)
    : `<div class="video-placeholder">
        <div class="youtube-mark">▶</div>
        <strong>Book trailer coming here</strong>
        <small>Add trailerUrl for ${b.title} in config.js.</small>
      </div>`;

  const shortBlock = b.shortUrl
    ? youtubeEmbed(b.shortUrl, `${b.title} YouTube Short`)
    : `<div class="video-placeholder">
        <div class="youtube-mark">▶</div>
        <strong>YouTube Short coming here</strong>
        <small>Add shortUrl for ${b.title} in config.js.</small>
      </div>`;

  const audiobookBlock = b.audiobookYoutubeUrl
    ? youtubeEmbed(b.audiobookYoutubeUrl, `${b.title} audiobook reading`)
    : `<div class="video-placeholder">
        <div class="youtube-mark">▶</div>
        <strong>YouTube reading coming here</strong>
        <small>Add audiobookYoutubeUrl for ${b.title} in config.js.</small>
      </div>`;

  page.innerHTML = `
    <section class="book-hero">
      <div class="book-cover-large">
        <img src="${b.cover}" alt="${b.title} book cover">
      </div>

      <div>
        <div class="book-meta">${b.genre}</div>
        <h1>${b.title}</h1>
        <p class="book-hook">${b.description}</p>

        <div class="book-actions">
          <a class="cta solid" href="${b.chapter}" data-track="chapter" data-book="${b.slug}">
            Read Chapter One
          </a>
          <a class="cta" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">
            Play Audio Sample
          </a>
          ${externalButton(b.amazonUrl, "Buy on Amazon", "amazon", b.slug)}
          ${externalButton(b.audibleUrl, "Listen on Audible", "audible", b.slug)}
        </div>

        <p><a class="back" href="index.html#books">← Back to the collection</a></p>
      </div>
    </section>

    <section class="book-section" id="trailer">
      <div class="eyebrow">Book Trailer</div>
      <h2>Watch the story come alive.</h2>
      <p class="section-copy">The trailer plays here without sending readers away from JayTreeBooks.com.</p>
      <div class="book-video">${trailerBlock}</div>
      <div class="video-actions">
        ${externalButton(b.trailerUrl, "Watch on YouTube", "trailer_youtube", b.slug)}
      </div>
    </section>

    <section class="book-section" id="short">
      <div class="eyebrow">YouTube Short</div>
      <h2>A quick taste of the mystery.</h2>
      <p class="section-copy">Use this for a teaser, cinematic Short, clue, or 60-second mystery tied to the book.</p>
      <div class="short-wrap">
        <div class="book-video short-video">${shortBlock}</div>
      </div>
      <div class="video-actions centered">
        ${externalButton(b.shortUrl, "Watch Short on YouTube", "short_youtube", b.slug)}
      </div>
    </section>

    <section class="book-section" id="audiobook">
      <div class="eyebrow">Audiobook / Reading</div>
      <h2>Listen to the story.</h2>
      <p class="section-copy">Readers can play your YouTube chapter reading or audiobook preview directly on the site.</p>
      <div class="book-video">${audiobookBlock}</div>

      <div class="book-actions">
        <a class="cta solid" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">
          Play Website Audio Sample
        </a>
        ${externalButton(b.audiobookYoutubeUrl, "Open Reading on YouTube", "audiobook_youtube", b.slug)}
        ${externalButton(b.audibleUrl, "Full Audiobook on Audible", "audible", b.slug)}
      </div>
    </section>

    <section class="book-section">
      <div class="eyebrow">Keep Reading</div>
      <h2>More from JayTree Books.</h2>
      <div class="grid">${relatedCards(b)}</div>
    </section>
  `;

  bindTracking();
}

if (document.getElementById("book-grid")) renderIndex();
if (document.getElementById("book-page")) renderBook();
