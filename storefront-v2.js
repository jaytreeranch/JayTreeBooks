(() => {
  "use strict";
  // Product cards are real HTML: shopping, samples and navigation work without JS.
  // This script records only intent, not a completed purchase or confirmed signup.
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