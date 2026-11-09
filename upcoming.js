(() => {
  "use strict";
  const local = /^(localhost|127\.0\.0\.1|\[::1\])$/.test(window.location.hostname);
  const testTraffic = new URLSearchParams(window.location.search).get("promo_test") === "1";
  function send(name, params = {}) {
    if (local || typeof window.gtag !== "function") return;
    window.gtag("event", name, Object.assign({
      promo_id: "upcoming_novels_202611",
      promo_path: window.location.pathname,
      transport_type: "beacon"
    }, testTraffic ? {debug_mode: true, promo_test: true} : {}, params));
  }
  function ready() {
    const surfaces = Array.from(document.querySelectorAll("[data-upcoming-surface]"));
    if (!surfaces.length) return;
    const placement = surfaces[0].dataset.upcomingSurface;
    const counted = new Set();
    function impression(target) {
      if (counted.has(target) || document.visibilityState === "hidden") return;
      counted.add(target);
      const book = target.dataset.upcomingBook;
      send(book ? "upcoming_book_view" : "upcoming_promo_view",
        Object.assign({placement}, book ? {book} : {}));
    }
    const landingSurfaces = surfaces.filter(el => el.dataset.upcomingSurface === "landing");
    const countLanding = () => landingSurfaces.forEach(impression);
    countLanding();
    document.addEventListener("visibilitychange", () => {
      if (document.visibilityState !== "hidden") countLanding();
    });
    if (window.IntersectionObserver) {
      const observer = new window.IntersectionObserver(entries => {
        entries.forEach(entry => {
          if (!entry.isIntersecting || entry.intersectionRatio < 0.35 ||
              document.visibilityState === "hidden") return;
          impression(entry.target);
          observer.unobserve(entry.target);
        });
      }, {threshold: [0.35]});
      surfaces.filter(el => el.dataset.upcomingSurface !== "landing").forEach(el => observer.observe(el));
      document.querySelectorAll("[data-upcoming-book]").forEach(el => observer.observe(el));
    }
    const actions = {
      open: "upcoming_promo_click", notify: "upcoming_notify_click",
      collection: "upcoming_collection_click", chapter: "upcoming_chapter_click",
      book: "upcoming_existing_book_click"
    };
    document.addEventListener("click", event => {
      const el = event.target.closest?.("[data-promo-action]");
      if (!el || !actions[el.dataset.promoAction]) return;
      const params = {placement, book: el.dataset.book || "", link_url: el.getAttribute("href") || ""};
      send(actions[el.dataset.promoAction], params);
      if (el.dataset.promoAction === "chapter") send("chapter", params);
      if (el.dataset.promoAction === "book") send("book_page", params);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready, {once:true});
  else ready();
})();
