# YouTube Error 153 fix

This build:
- uses `youtube-nocookie.com` for embedded YouTube players
- sends `referrerpolicy="strict-origin-when-cross-origin"`
- adds a matching referrer meta tag to HTML pages
- strips escaped `\&` from pasted YouTube URLs
- ignores extra tracking parameters such as `source_ve_path`

Important:
If you test by double-clicking `index.html` and the browser address begins with `file:///`, YouTube may still show Error 153 because the page has no normal website origin/referrer.

Test after uploading to `https://www.jaytreebooks.com`, or use a local web server such as:

`python -m http.server 8000`

Then open:

`http://localhost:8000`
