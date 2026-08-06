# JayTree Books — Website

This repository branch contains a simple static website for JayTree Books: an independent online bookstore and reading resource platform focused on a curated selection of books.

Features included:
- Responsive static front-end (HTML/CSS/JS)
- Sample curated book data (data/books.json)
- Search by title/author/tag
- Book detail modal with buy/learn-more link
- Reading resources section (placeholder content)

How to run locally:
- Quick (no install): open `index.html` in your browser. For best results run via a local server to avoid CORS issues with fetch:
  - Python 3: `python -m http.server 8000`
  - Node (http-server): `npx http-server -c-1` or `npm i -g http-server` then `http-server`

Deployment:
- Host as a static site (GitHub Pages, Netlify, Vercel) — point the deploy to the repository branch that contains the site (e.g., `site/jaytreebooks`).

Extending the project:
- Add a lightweight backend for cart/checkout and inventory.
- Replace sample JSON with a headless CMS (Sanity, Contentful) or a small API.
- Add pagination, tag filtering UI, and author pages.

License: MIT
