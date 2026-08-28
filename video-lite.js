(() => {
  document.addEventListener("click", event => {
    const toggle = event.target.closest(".menu-toggle");
    if (toggle) {
      requestAnimationFrame(() => {
        const nav = toggle.closest(".nav");
        toggle.setAttribute("aria-expanded", nav?.classList.contains("open") ? "true" : "false");
      });
    }

    const navLink = event.target.closest(".nav-links a");
    if (navLink) {
      const nav = navLink.closest(".nav");
      nav?.classList.remove("open");
      nav?.querySelector(".menu-toggle")?.setAttribute("aria-expanded", "false");
    }

    const fallback = event.target.closest(".video-lite-fallback");
    if (fallback && typeof gtag === "function") {
      gtag("event", "video_youtube_fallback", { youtube_url: fallback.href });
    }

    const button = event.target.closest(".video-lite");
    if (!button) return;
    const id = button.dataset.youtubeId;
    if (!id) return;
    if (typeof gtag === "function") {
      gtag("event", "video_play", { youtube_id: id, video_title: button.dataset.title || "" });
    }

    const iframe = document.createElement("iframe");
    iframe.src = `https://www.youtube-nocookie.com/embed/${id}?rel=0&playsinline=1&autoplay=1`;
    iframe.title = button.dataset.title || "YouTube video";
    iframe.loading = "lazy";
    iframe.referrerPolicy = "strict-origin-when-cross-origin";
    iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share";
    iframe.allowFullscreen = true;
    iframe.setAttribute("frameborder", "0");
    button.replaceWith(iframe);
  });
})();
