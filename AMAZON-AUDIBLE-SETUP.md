# Amazon / Audible setup

The original site supplied for this redesign uses the Amazon and Audible homepages for its external purchase links. The final site preserves those destinations rather than guessing individual product pages.

To make each CTA go directly to a book:
1. Open `config.js`.
2. Find the book record.
3. Replace `amazonUrl` with the exact Amazon product URL.
4. Replace `audibleUrl` with the exact Audible product URL.

For YouTube, put the video ID only in `trailerVideoId`.
For example, `https://www.youtube.com/watch?v=ABC123` becomes `ABC123`.
