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

  // Selecting a cover updates the featured edition in place. The source of truth
  // for purchase and sample URLs remains the corresponding static product card.
  const featured = document.querySelector("#sf-cine-featured-region");
  if (featured) {
    const featuredCover = document.querySelector("#sf-cine-featured-cover");
    const featuredDetails = document.querySelector("#sf-cine-featured-details");
    const featuredTitle = document.querySelector("#sf-cine-featured-title");
    const featuredDescription = document.querySelector("#sf-cine-featured-description");
    const featuredBuy = document.querySelector("#sf-cine-featured-buy");
    const featuredSample = document.querySelector("#sf-cine-featured-sample");
    const announcement = document.querySelector("#sf-cine-selection-status");
    const selectors = [...document.querySelectorAll(".sf-cine-select[data-select-book]")];

    selectors.forEach((selector) => {
      selector.addEventListener("click", () => {
        const card = selector.closest(".sf-cine-product");
        const thumbnail = card?.querySelector(".sf-cine-cover-link img");
        const title = card?.querySelector(".sf-cine-product-title")?.textContent.trim();
        const purchase = card?.querySelector("a.sf-cine-buy");
        const preview = card?.querySelector("a.sf-cine-sample");
        const book = card?.dataset.book;

        if (!card || !thumbnail || !title || !purchase || !preview || !book ||
            !featuredCover || !featuredDetails || !featuredTitle ||
            !featuredDescription || !featuredBuy || !featuredSample) {
          return;
        }

        featuredCover.src = thumbnail.getAttribute("src");
        featuredCover.alt = thumbnail.alt;
        featuredDetails.href = "books/" + book + ".html";
        featuredDetails.setAttribute("aria-label", title + " — featured book details");
        featuredTitle.textContent = title;
        featuredDescription.textContent = card.dataset.description || "";
        featuredBuy.href = purchase.href;
        featuredBuy.dataset.book = book;
        featuredSample.href = preview.getAttribute("href");
        featuredSample.dataset.book = book;

        selectors.forEach((item) => {
          const selected = item === selector;
          item.setAttribute("aria-pressed", String(selected));
          item.closest(".sf-cine-product")?.classList.toggle("is-selected", selected);
        });
        if (announcement) announcement.textContent = "Selected: " + title;
        if (window.matchMedia?.("(prefers-reduced-motion: reduce)").matches) {
          featured.scrollIntoView({ block: "start", behavior: "instant" });
        } else {
          featured.scrollIntoView({ block: "start", behavior: "smooth" });
        }
      });
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