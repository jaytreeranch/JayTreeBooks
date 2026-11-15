// Preserve bookmarks and campaign parameters from the original single-page site.
(() => {
  const destinations = {
    about: 'about.html', 'audio-grid': 'audiobooks.html', 'book-grid': 'books.html',
    'animated-series': 'animated-series.html', 'upcoming-novels': 'upcoming-books.html',
    'reading-guides': 'reading-guides.html', 'kindle-unlimited': 'kindle-unlimited-mystery-books.html',
    'case-001-video': 'classic.html#case-001-video', follow: 'classic.html#follow', youtube: 'classic.html#youtube'
  };
  function openBookmark() {
    const anchor = location.hash.slice(1);
    if (document.getElementById(anchor) || !Object.hasOwn(destinations, anchor)) return;
    const target = new URL(destinations[anchor], location.href);
    target.search = location.search;
    location.replace(target.href);
  }
  openBookmark();
  window.addEventListener('hashchange', openBookmark);
})();
