(() => {
  document.addEventListener("click", event => {
    const toggle = event.target.closest(".menu-toggle");
    if (toggle) {
      requestAnimationFrame(() => {
        const nav = toggle.closest(".nav");
        toggle.setAttribute("aria-expanded", nav?.classList.contains("open") ? "true" : "false");
      });
    }

    const button = event.target.closest(".video-lite");
    if (!button) return;
    const id = button.dataset.youtubeId;
    if (!id) return;

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
