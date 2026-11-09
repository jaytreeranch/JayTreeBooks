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
    document.querySelectorAll("[data-upcoming-video]").forEach(video => {
      let started = false;
      const milestones = new Set();
      let complete = false;
      const details = () => ({placement, video_id: video.dataset.upcomingVideo,
        video_title: "Upcoming novels cinematic teaser",
        video_duration: Number.isFinite(video.duration) ? video.duration : 0});
      function percentWatched() {
        if (!Number.isFinite(video.duration) || video.duration <= 0) return 0;
        const ranges = video.played;
        let watched = 0;
        for (let i = 0; i < ranges.length; i++) watched += ranges.end(i) - ranges.start(i);
        return Math.min(100, watched / video.duration * 100);
      }
      function progress() {
        const percent = percentWatched();
        [25, 50, 75].forEach(milestone => {
          if (percent >= milestone && !milestones.has(milestone)) {
            milestones.add(milestone);
            send("upcoming_video_progress", Object.assign(details(), {video_percent: milestone}));
          }
        });
      }
      video.addEventListener("play", () => {
        if (started) return;
        started = true;
        send("upcoming_video_start", details());
      });
      video.addEventListener("timeupdate", progress);
      video.addEventListener("ended", () => {
        progress();
        if (!complete && percentWatched() >= 90) {
          complete = true;
          send("upcoming_video_complete", Object.assign(details(), {video_percent: Math.round(percentWatched())}));
        }
      });
      video.addEventListener("error", () => send("upcoming_video_error",
        Object.assign(details(), {media_error_code: video.error?.code || 0})));
    });
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
