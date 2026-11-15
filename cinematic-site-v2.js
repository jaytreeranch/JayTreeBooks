/* JayTree sitewide cinematic navigation: no network dependency, no fake purchase events. */
(() => {
  "use strict";
  const body = document.body;
  const root = body?.dataset?.jtRoot || "";
  const entries = [
    ["Home", "home-v2.html", "Begin with JayTree Books"],
    ["Books", "books.html", "Mystery novels and Hollow Bell novella"],
    ["Audiobooks", "audiobooks.html", "Six Vivian complete audiobooks"],
    ["Samples", "samples.html", "Read first chapters and hear narrators"],
    ["The Series", "series-v2.html", "Upcoming trilogy and connected mysteries"],
    ["About", "about.html", "About the author and independent publisher"],
    ["News", "news-v2.html", "Trailers and upcoming mystery announcements"],
    ["Case Files", "case-files.html", "Subscribe to JayTree Case Files"],
    ["Reading Guides", "reading-guides.html", "Guides to psychological mysteries"],
    ["Video & Mystery Challenge", "experiences-v2.html", "Watch trailers and solve cases"]
  ];
  const header = body.querySelector(".jt-header");
  if (!header) return;
  const input = header.querySelector(".jt-search-box input");
  const results = header.querySelector(".jt-search-results");
  if (input && results) {
    let bookEntries = [];
    const draw = () => {
      const q = input.value.toLocaleLowerCase().trim();
      const all = entries.concat(bookEntries);
      const shown = all.filter(item => !q || item.join(" ").toLocaleLowerCase().includes(q)).slice(0,10);
      results.replaceChildren();
      for (const [label, path, desc] of shown) {
        const a = document.createElement("a");
        a.href = root + path;
        a.textContent = label + " · " + desc;
        results.appendChild(a);
      }
      if (!shown.length) {
        const item = document.createElement("span");
        item.textContent = "No matching title or page";
        results.appendChild(item);
      }
    };
    input.addEventListener("input", draw);
    header.querySelector(".jt-search")?.addEventListener("toggle", ev => {
      if (ev.target.open) { draw(); input.focus(); }
    });
    header.addEventListener("keydown", ev => {
      if (ev.key === "Escape") header.querySelector(".jt-search")?.removeAttribute("open");
    });
    const useBooks = data => {
      bookEntries = data.books.filter(book => book.book_status === "published")
        .map(book => [book.title + (book.edition === "Novella" ? " (Novella)" : ""), book.book_page, book.tagline || "Book details"]);
      draw();
    };
    const embedded = document.getElementById("jt-portable-catalog");
    if (embedded) {
      useBooks(JSON.parse(embedded.textContent));
    } else if (/^https?:$/.test(location.protocol)) {
      results.setAttribute("aria-busy", "true");
      fetch(root + "data/storefront-catalog.json", {cache:"force-cache"})
        .then(r => r.ok ? r.json() : Promise.reject(Error("No catalog")))
        .then(useBooks).catch(() => { /* Navigation search still works offline. */ })
        .finally(() => results.removeAttribute("aria-busy"));
    }
  }
  // Preview pages don't claim payments, signups, or completions. Existing attribution remains owned by tracking.js.
})();
