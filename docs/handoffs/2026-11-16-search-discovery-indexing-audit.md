# JayTree Books: verified organic discovery and Google index audit (2026-11-16)

## Goal and sources
Primary unmodified page-one search goals:
- psychological mystery books -> https://jaytreebooks.com/psychological-mystery-books.html
- new mystery book -> https://jaytreebooks.com/mystery-books.html

Sources checked read-only via authorized, directly owned JT-GE78 Google Search Console OAuth (Search Analytics and URL Inspection API), plus first-party HTTPS checks against live JayTreeBooks.com, robots.txt and sitemap.xml. Detailed raw Google data is on PRIVATE LAN at GSC_FREE_20261115/runtime/diagnostics/2026-11-16-*.json, not in Git.

## Verified discoveries (time-specific)
- Current public site homepage responds 200, canonical correct, index/follow allowed; Google URL Inspection: PASS, Submitted and indexed; last crawl 2026-11-15.
- /psychological-mystery-books.html: HTTP 200, self canonical, index/follow; URL Inspection: PASS, Submitted and indexed; last crawl 2026-11-03. The primary term psychological mystery books is associated with this proper page in Google Search Analytics. Very low impressions mean no stable rank inference.
- /mystery-books.html: HTTP 200, self canonical, index/follow; URL Inspection: NEUTRAL, URL unknown to Google as of this query. This page has the existing "New Mystery Books" title and distinct, substantial human-facing book summaries. Do not create a duplicate second genre hub.
- /books.html: HTTP 200, index/follow and self canonical; URL Inspection currently unknown to Google.
- /audiobooks.html: HTTP 200, index/follow and self canonical; URL Inspection: Discovered, currently not indexed.
- robots.txt: User-agent * Allow / and references https://jaytreebooks.com/sitemap.xml.
- sitemap.xml: HTTP 200, 35 URL locators, includes both genre hubs. Google sitemaps API reports last downloaded 2026-11-15, zero reported errors and warnings. Sitemap data's aggregate indexed field alone is not definitive; URL Inspection explicitly proves homepage and psychological-mystery page indexed.
- Dedicated book detail pages already have Book JSON-LD and well-formed unique titles; genre hubs already include CollectionPage / ItemList and breadcrumb metadata. Do not duplicate existing structured data without validating needs.
- Current /books.html and /audiobooks.html don't visibly link to the genre hubs in their HTML at audit time; homepage does link both. More contextual linking from relevant book detail pages, guides and the books shop can strengthen discovery and reader navigation.

## Prioritized, reversible plan
P0 (index coverage): In Google Search Console manually use URL Inspection > Request indexing for /mystery-books.html, /books.html and /audiobooks.html after ensuring live indexable 200 pages. Ordinary Google Indexing API is not permitted for book pages; it only supports specified job and livestream page types. Requesting indexing is a hint, not a guarantee. Avoid repetitive quota-spamming. No index request has been submitted here.
P0 (internal discovery): On a fresh isolated website feature branch based on current production main, propose prominent descriptive contextual links from Books to Psychological Mystery Books, New Mystery Books and reading guides; from book detail pages and reading guides to the relevant genre hub; and from Audiobooks where genuinely helpful. Preserve existing branded storefront layout, sales URL redirects, author copy and easter eggs. Avoid navigation clutter and artificial keyword stuffing.
P1 (search intent/content): Keep each genre hub unique and honest. Psychological hub for readers choosing by unreliable memory, altered evidence and family secrets; New Mystery Books hub for discovering books by subgenre and premise, with accurate availability and publication status. Do not claim old books are new 2026 releases or invent endorsements, reviews or ISBNs. Add original reader value only where the page is thin or genuinely lacks useful comparisons, sample excerpts or FAQs.
P1 (real authority): Seek genuine editorial coverage, author features, reader interviews, relevant mystery-fiction communities, book podcasts/reviewers, Amazon Author Central, Goodreads and YouTube description links to the correct official book or guide pages. No paid link farms, fake awards, exchange schemes or fabricated reviews.
P2 (site experience & conversion): Check actual mobile LCP/INP/CLS with free local Lighthouse or Search Console CWV before any speculative optimization; make covers appropriately sized and lazy-load noncritical media. Check direct landing > free Chapter One > buy or audiobook CTA with privacy-preserving GA4 and owner-controlled GSC metrics.
P2 (weekly feedback): Add an index-status read-only QC to the existing self-hosted weekly Search Console tracker only after the protected farm scheduler has one verified owner; include coverage state, last crawl, clicks, impressions and query/landing page movement. Currently weekly runner NOT ACTIVE.

## Interpretation
- The biggest confirmed immediate gap is that Google has not yet reported the new-mystery hub or books shop as indexed despite live accessible pages. The latest redesign is recent; wait for genuine recrawling, don't rebuild the site solely based on transient index status.
- Tiny search samples can't establish durable position change. Missing impressions are not 'rank >50' or guaranteed deindexing.
- Site indexing is a prerequisite, not a promise of page-one results. Relevant useful content and natural third-party authority are needed long-term.

## Safety, QC, rollback, handoff
- Audit: read-only. No change to live site, GitHub Pages, Payhip, Google Site property, browser cookies, tokens, or Production Manager lease/scheduler. Google OAuth stored as before in Windows DPAPI, inaccessible to GitHub.
- Evidence: private LAN runtime/diagnostics JSON captures current Search Analytics top queries and top pages, official index inspections and sitemap status; the sanitized summary above is suitable for repository documentation.
- Rollback: none for audited live systems; this documentation can be reverted without user-facing changes.
- Next executable development: isolated source feature branch with high-value natural internal links, automated test, visual QC and explicit deploy authorization. Next owner UI action: single Google Search Console Request indexing for currently unknown/discovered key URLs, not the unsupported Google Indexing API.