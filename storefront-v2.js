(() => {
  "use strict";
  // Product cards are real HTML: shopping, samples and navigation work without JS.
  // This script records only intent, not a completed purchase or confirmed signup.
  // The cinematic audiobook search filters only the six visible product cards.
  // Cards and purchase links remain fully usable when JavaScript is unavailable.
  const titleSearch = document.querySelector("#sf-cine-title-search");
  if (titleSearch) {
    const cards = [...document.querySelectorAll(".sf-cine-product")];
    const noResults = document.querySelector(".sf-cine-no-results");
    titleSearch.addEventListener("input", () => {
      const query = titleSearch.value.trim().toLocaleLowerCase();
      let visible = 0;
      cards.forEach((card) => {
        const match = !query || (card.dataset.title || "").includes(query);
        card.hidden = !match;
        if (match) visible++;
      });
      if (noResults) noResults.hidden = visible !== 0;
    });
  }

  document.addEventListener("click", (event) => {
    const link = event.target.closest("a[data-track]");
    if (!link || typeof window.gtag !== "function") return;
    window.gtag("event", link.dataset.track, {
      book: link.dataset.book || "",
      placement: link.dataset.placement || "storefront_v2",
      transport_type: "beacon"
    });
  });
})();