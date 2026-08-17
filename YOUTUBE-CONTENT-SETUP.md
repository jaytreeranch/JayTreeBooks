# Add YouTube videos to JayTree Books

Open `config.js`. Each book has three editable YouTube fields:

- `trailerUrl` — full book trailer
- `shortUrl` — YouTube Short / teaser
- `audiobookYoutubeUrl` — YouTube reading, chapter, or audiobook preview

Example:

```js
"trailerUrl": "https://www.youtube.com/watch?v=ABC123",
"shortUrl": "https://www.youtube.com/shorts/XYZ789",
"audiobookYoutubeUrl": "https://www.youtube.com/watch?v=READ456"
```

Paste the complete YouTube URL. The website converts it into an embedded player automatically.

The original chapter pages and audio sample pages remain connected. Amazon and Audible links can also be changed per book in the same `config.js` file.
