# JayTree Books — Page-specific social image workflow

Every major site page has its own 1200x630 JPEG located in images/social/previews. Both the original homepage and home-v2 intentionally share home.jpg. Audiobooks uses moonlit manor, bronze headphones, the official Second Draft cover and the $1.99 offer. Six individual book editions have their own 1200x630 title-specific social cards, including distinct full novel and novella images.

scripts/apply_social_previews.py is the authoritative standard-library image/metadata updater. scripts/build_social_art.py is a manual asset-composition script that uses Pillow on JT-DESKTOP; Pillow is not needed on GitHub Pages or in CI. The images are composed from existing owned JayTree artwork and official cover files. No font files were distributed.

To update after future books or pages are added, create the new cover and corresponding named image under images/social/previews and update the mapping in apply_social_previews.py. Run:
    python scripts/apply_social_previews.py --write
    python scripts/apply_social_previews.py --check
    python scripts/build_sitewide_preview.py --check
    python scripts/build_storefront_catalog.py --check
    python -m unittest discover -s tests -p test_social_previews.py
The updater refuses to add a published page whose image does not exist. Both the sitewide generator and SEO maintenance workflow restore the intended OG metadata so nightly or manual site builds do not overwrite previews.

Facebook and X render social metadata from initial HTML. The old /#audiobooks URL sends real visitors to the Audiobooks shop, but a fragment cannot select an independent social card. Share https://jaytreebooks.com/audiobooks.html to get the audiobook-specific image.

After deploy, verify the bot-facing page has one og:image and twitter:image, absolute HTTPS URLs, og:image:width=1200, og:image:height=630 and an image/jpeg response. Meta/Facebook caches may need a fresh scrape using https://developers.facebook.com/tools/debug/ and the Scrape Again action. Never claim a provider cache refresh without a provider receipt. Existing Payhip products, book content and approved audio remain unchanged.
