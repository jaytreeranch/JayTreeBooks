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
    if (u.hostname.includes("youtu.be")) return u.pathname.split("/").filter(Boolean)[0] || "";
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
  if (!id) return "";
  return `<iframe src="https://www.youtube-nocookie.com/embed/${id}?rel=0" title="${title}" frameborder="0" referrerpolicy="strict-origin-when-cross-origin" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>`;
}

function externalButton(url, label, eventName, bookSlug, extraClass = "") {
  if (!url) return "";
  return `<a class="cta${extraClass ? ` ${extraClass}` : ""}" href="${url}" target="_blank" rel="noopener" data-track="${eventName}" data-book="${bookSlug}">${label}</a>`;
}

function kindleUnlimitedBadge(b) {
  return b.kindleUnlimited ? `<div class="ku-badge">Kindle Unlimited</div>` : "";
}

function kindleUnlimitedCallout(b) {
  if (!b.kindleUnlimited || !b.amazonUrl) return "";
  return `<div class="ku-callout">
    <div>
      <span class="ku-kicker">Kindle Unlimited</span>
      <strong>Read FREE with Kindle Unlimited</strong>
      <small>Kindle Unlimited members can read this title at no additional cost.</small>
    </div>
    <a class="cta solid ku-button" href="${b.amazonUrl}" target="_blank" rel="noopener" data-track="kindle_unlimited" data-book="${b.slug}">Read on Kindle Unlimited</a>
  </div>`;
}

function bookCard(b) {
  return `<article class="card">
    <a class="cover" href="books/${b.slug}.html" aria-label="Explore ${b.title}"><img src="${b.cover}" alt="${b.title} book cover" loading="lazy" decoding="async"></a>
    <div class="card-body">
      ${kindleUnlimitedBadge(b)}
      <div class="genre">${b.genre}</div><h3>${b.title}</h3><p>${b.description}</p>
      <div class="card-actions">
        <a class="read-sample" href="${b.chapter}" data-track="chapter" data-book="${b.slug}">Read First Chapter</a>
        <a class="buy" href="books/${b.slug}.html" data-track="book_page" data-book="${b.slug}">Explore Book</a>
      </div>
    </div>
  </article>`;
}

function audioCard(b) {
  return `<article class="audio-card">
    <div class="audio-icon">◉</div><div class="format">Audiobook</div><h3>${b.title}</h3><p>${b.description}</p>
    <div class="card-actions">
      <a class="read-sample" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">Audio Sample</a>
      <a class="audible" href="books/${b.slug}.html#listen" data-track="book_audio" data-book="${b.slug}">Full Audiobook — Coming Soon</a>
    </div>
  </article>`;
}

function bindTracking() {
  document.querySelectorAll("[data-track]").forEach(el => {
    el.addEventListener("click", () => track(el.dataset.track, { book: el.dataset.book || "" }));
  });
  document.querySelectorAll("[data-social]").forEach(el => {
    el.addEventListener("click", () => track("social_visit", { platform: el.dataset.social || "" }));
  });
  document.querySelectorAll("[data-case-files-form]").forEach(form => {
    form.addEventListener("submit", () => track("case_files_signup_submit", { placement: form.dataset.placement || "unknown" }));
  });
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
  const toggle = document.querySelector(".menu-toggle");
  if (toggle) toggle.addEventListener("click", () => document.querySelector(".nav")?.classList.toggle("open"));
}

let campaignConfigPromise = null;

function dateKeyInTimeZone(timeZone) {
  const parts = new Intl.DateTimeFormat("en-US", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit"
  }).formatToParts(new Date());
  const values = Object.fromEntries(parts.map(part => [part.type, part.value]));
  return `${values.year}-${values.month}-${values.day}`;
}

function utcDayNumber(dateKey) {
  const [year, month, day] = String(dateKey).split("-").map(Number);
  if (!year || !month || !day) throw new Error(`Invalid campaign date: ${dateKey}`);
  return Math.floor(Date.UTC(year, month - 1, day) / 86400000);
}

function mondayDayNumber(dayNumber) {
  const weekday = new Date(dayNumber * 86400000).getUTCDay();
  return dayNumber - ((weekday + 6) % 7);
}

function featuredSlugFromCampaign(campaign) {
  if (!campaign || !Array.isArray(campaign.rotation) || !campaign.rotation.length) {
    throw new Error("Campaign rotation is missing or empty");
  }
  const timeZone = campaign.timezone || "America/Chicago";
  const today = utcDayNumber(dateKeyInTimeZone(timeZone));
  const anchor = utcDayNumber(campaign.rotation_anchor);
  const weeks = Math.floor((mondayDayNumber(today) - mondayDayNumber(anchor)) / 7);
  const index = ((weeks % campaign.rotation.length) + campaign.rotation.length) % campaign.rotation.length;
  return campaign.rotation[index];
}

async function loadCampaignConfig() {
  if (!campaignConfigPromise) {
    const url = JT.campaignConfigUrl || "data/campaign.json";
    campaignConfigPromise = fetch(url, { cache: "no-store" }).then(async response => {
      if (!response.ok) throw new Error(`Campaign config returned HTTP ${response.status}`);
      return response.json();
    });
  }
  return campaignConfigPromise;
}

async function featuredBook() {
  let slug = JT.featuredBook;
  try {
    const campaign = await loadCampaignConfig();
    const campaignSlug = featuredSlugFromCampaign(campaign);
    if (JT.books.some(book => book.slug === campaignSlug)) slug = campaignSlug;
  } catch (error) {
    console.warn("Using fallback featured book because campaign sync was unavailable.", error);
  }
  return JT.books.find(book => book.slug === slug) || JT.books[0];
}

async function renderIndex() {
  const bookGrid = document.getElementById("book-grid");
  const audioGrid = document.getElementById("audio-grid");
  if (bookGrid) bookGrid.innerHTML = JT.books.map(bookCard).join("");
  if (audioGrid) audioGrid.innerHTML = JT.books.map(audioCard).join("");

  const featured = await featuredBook();
  const heroImage = document.querySelector(".hero-feature img");
  const heroLabel = document.querySelector(".hero-feature span");
  const heroTitle = document.querySelector(".hero-feature strong");
  const heroSmall = document.querySelector(".hero-feature small");
  if (heroImage) { heroImage.src = featured.cover; heroImage.alt = featured.title + " book cover"; }
  if (heroLabel) heroLabel.textContent = "THIS WEEK'S FEATURED MYSTERY";
  if (heroTitle) heroTitle.textContent = featured.title;
  if (heroSmall) heroSmall.textContent = featured.description;

  const heroActions = document.querySelector(".hero-actions");
  if (heroActions && featured) {
    heroActions.innerHTML = `
      <a class="cta solid" href="${featured.chapter}" data-track="featured_chapter" data-book="${featured.slug}">Read Chapter One</a>
      ${featured.kindleUnlimited ? externalButton(featured.amazonUrl, "Read FREE with Kindle Unlimited", "featured_kindle_unlimited", featured.slug) : ""}
      ${featured.trailerUrl ? `<a class="cta" href="#youtube" data-track="featured_trailer" data-book="${featured.slug}">Watch Trailer</a>` : ""}
      <a class="cta" href="book.html?book=${featured.slug}" data-track="featured_book" data-book="${featured.slug}">Explore ${featured.title}</a>`;
  }

  const youtubeCard = document.querySelector(".youtube-card");
  if (youtubeCard && featured.trailerUrl) {
    youtubeCard.classList.add("homepage-video");
    youtubeCard.innerHTML = youtubeEmbed(featured.trailerUrl, `${featured.title} official book trailer`);
  }

  bindTracking();
}

function relatedCards(book) {
  return JT.books.filter(x => x.slug !== book.slug).slice(0, 3).map(bookCard).join("");
}

async function renderBook() {
  const requestedSlug = new URLSearchParams(location.search).get("book");
  const b = requestedSlug
    ? (JT.books.find(x => x.slug === requestedSlug) || JT.books[0])
    : await featuredBook();
  const page = document.getElementById("book-page");
  if (!page) return;
  document.title = `${b.title} | JayTree Books`;

  const trailerSection = b.trailerUrl ? `
    <section class="book-section" id="trailer">
      <div class="eyebrow">Book Trailer</div><h2>Watch the story come alive.</h2>
      <p class="section-copy">Watch the official trailer directly on JayTreeBooks.com.</p>
      <div class="book-video">${youtubeEmbed(b.trailerUrl, `${b.title} book trailer`)}</div>
      <div class="video-actions">${externalButton(b.trailerUrl, "Watch on YouTube", "trailer_youtube", b.slug)}</div>
    </section>` : "";

  const shortSection = b.shortUrl ? `
    <section class="book-section" id="short">
      <div class="eyebrow">YouTube Short</div><h2>A quick taste of the mystery.</h2>
      <p class="section-copy">Watch a cinematic teaser tied to the story.</p>
      <div class="short-wrap"><div class="book-video short-video">${youtubeEmbed(b.shortUrl, `${b.title} YouTube Short`)}</div></div>
      <div class="video-actions centered">${externalButton(b.shortUrl, "Watch Short on YouTube", "short_youtube", b.slug)}</div>
    </section>` : "";

  const audiobookVideo = b.audiobookYoutubeUrl ? `
      <div class="book-video">${youtubeEmbed(b.audiobookYoutubeUrl, `${b.title} audiobook reading`)}</div>` : "";

  page.innerHTML = `
    <section class="book-hero">
      <div class="book-cover-large"><img src="${b.cover}" alt="${b.title} book cover"></div>
      <div>
        <div class="book-meta">${b.genre}</div><h1>${b.title}</h1><p class="book-hook">${b.description}</p>
        ${kindleUnlimitedCallout(b)}
        <div class="book-actions">
          <a class="cta solid" href="${b.chapter}" data-track="chapter" data-book="${b.slug}">Read Chapter One</a>
          <a class="cta" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">Play Audio Sample</a>
          ${externalButton(b.amazonUrl, "Buy on Amazon", "amazon", b.slug)}
        </div>
        <p><a class="back" href="index.html#books">← Back to the collection</a></p>
      </div>
    </section>
    ${trailerSection}
    ${shortSection}
    <section class="book-section" id="audiobook">
      <div class="eyebrow">Audiobook / Reading</div><h2>Listen to the story.</h2>
      <p class="section-copy">Play the website audio sample${b.audiobookYoutubeUrl ? " or watch the YouTube chapter reading" : ""}.</p>
      ${audiobookVideo}
      <!-- JAYTREE_AUDIOBOOK_DIRECT_COMING_SOON -->
      <div class="ku-callout audiobook-coming-soon" aria-label="Full audiobook coming soon">
        <div>
          <span class="ku-kicker">Direct from JayTree Books</span>
          <strong>Full Audiobook — Coming Soon</strong>
          <small>Full audiobook editions will be available to purchase directly from JayTreeBooks.com.</small>
        </div>
      </div>
      <div class="book-actions">
        <a class="cta solid" href="${b.audio}" data-track="audio_preview" data-book="${b.slug}">Play Website Audio Sample</a>
        ${externalButton(b.audiobookYoutubeUrl, "Open Reading on YouTube", "audiobook_youtube", b.slug)}
      </div>
    </section>
    <section class="book-section"><div class="eyebrow">Keep Reading</div><h2>More from JayTree Books.</h2><div class="grid">${relatedCards(b)}</div></section>`;

  bindTracking();
}

if (document.getElementById("book-grid")) renderIndex().catch(error => console.error("Homepage render failed", error));
if (document.getElementById("book-page")) renderBook().catch(error => console.error("Book page render failed", error));
