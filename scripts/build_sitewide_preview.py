#!/usr/bin/env python3
"""Build the JayTree Books cinematic multi-page review site from approved source.
Does not publish, merge, or edit original audiobook sample files.
Run: python scripts/build_sitewide_preview.py --write | --check
"""
import argparse
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "data/storefront-catalog.json"
NAV = [
 ("Home", "home-v2.html", "home"),
 ("Books", "books.html", "books"),
 ("Audiobooks", "audiobooks.html", "audio"),
 ("The Series", "series-v2.html", "series"),
 ("Samples", "samples.html", "samples"),
 ("About", "about.html", "about"),
 ("News", "news-v2.html", "news")
]
LEGACY = [
 "about.html", "upcoming-books.html", "mystery-books.html",
 "psychological-mystery-books.html", "kindle-unlimited-mystery-books.html",
 "reading-guides.html", "case-files.html", "animated-series.html",
 "privacy.html", "terms.html"
]

def e(x):
    return html.escape(str(x),quote=True)

def header(page="",root=""):
    links = "".join(f'<a href="{root}{href}"'+(' aria-current="page"' if tag==page else "")+f'>{name}</a>' for name,href,tag in NAV)
    return f'''<header class="jt-header"><div class="jt-head-inner">
<a class="jt-brand" href="{root}home-v2.html" aria-label="JayTree Books home">
<img src="{root}icons/icon-192.png" width="61" height="60" alt=""><span>JAYTREE BOOKS</span></a>
<nav class="jt-nav" aria-label="Primary navigation">{links}</nav>
<details class="jt-search"><summary aria-label="Search books and pages" title="Search">⌕</summary>
<div class="jt-search-box"><label for="jt-search-input">Search JayTree Books</label>
<input id="jt-search-input" type="search" placeholder="Book title or page" autocomplete="off">
<div class="jt-search-results" aria-live="polite"></div></div></details>
<details class="jt-mobile"><summary aria-label="Open navigation">MENU ☰</summary>
<nav aria-label="Mobile navigation">{links}</nav></details>
</div></header>'''

def footer(root=""):
    links=[
        ("Books","books.html"),("Audiobooks","audiobooks.html"),("Free samples","samples.html"),
        ("Series","series-v2.html"),("Reading guides","reading-guides.html"),
        ("Videos & challenge","experiences-v2.html"),("Case Files","case-files.html"),
        ("About","about.html"),("Privacy","privacy.html"),("Terms","terms.html")
    ]
    return f'''<footer class="jt-footer"><div class="jt-wrap"><div class="jt-footer-inner">
<div><div class="jt-footer-brand">JAYTREE BOOKS</div><p>Stories that stay with you.</p><small>© 2026 JayTree Books · Independent mystery fiction</small></div>
<nav aria-label="Footer navigation">{''.join(f'<a href="{root}{href}">{label}</a>' for label,href in links)}</nav>
</div><small>Development design preview. No changes to the public JayTreeBooks.com website or Payhip listings.</small></div></footer>'''

ANALYTICS = '<script>\n// Analytics is only loaded on production host, never local preview.\nwindow.dataLayer=window.dataLayer||[];\nfunction gtag(){dataLayer.push(arguments)}\nif (location.hostname==="jaytreebooks.com" || location.hostname==="www.jaytreebooks.com"){\n const jtTag=document.createElement("script");jtTag.async=true;\n jtTag.src="https://www.googletagmanager.com/gtag/js?id=G-PHE2JVV5P6";\n document.head.appendChild(jtTag);\n gtag("js",new Date());gtag("config","G-PHE2JVV5P6");\n}\n</script>'

def head(title,desc,extra=""):
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,follow"><meta name="theme-color" content="#061116">
<meta name="description" content="{e(desc)}"><title>{e(title)} | JayTree Books Preview</title>
<link rel="icon" href="favicon.png"><link rel="stylesheet" href="storefront-v2.css">
<link rel="stylesheet" href="cinematic-site-v2.css">{extra}
{ANALYTICS}
<script src="tracking.js" defer></script>
<script src="cinematic-site-v2.js" defer></script><script src="storefront-v2.js" defer></script>
</head>'''

def body(page,title,desc,main):
    return head(title,desc)+f'<body class="jt-cinematic jt-page-{page}" data-jt-root=""><a class="sf-skip" href="#main">Skip to content</a>'+header(page)+f'<main id="main">{main}</main>'+footer()+'</body></html>'

def newsletter():
    return '''<section class="jt-newsletter" id="case-files"><div class="jt-wrap"><span class="jt-overline">Behind the next clue</span>
<h2>Join the JayTree Case Files.</h2><p>Get announcements, case reveals, previews and mystery news.
No guessing which narrator edition is available: all six complete Vivian audiobooks are already on sale.</p>
<a class="jt-btn primary" href="case-files.html" data-track="case_files" data-placement="cinematic_site">Join the Case Files</a>
</div></section>'''

def media_card(url,img,label,title,desc):
    return f'<a class="jt-media-tile" href="{e(url)}"><img src="{e(img)}" alt="{e(title)} artwork" loading="lazy" decoding="async"><div><small>{e(label)}</small><h3>{e(title)}</h3><p>{e(desc)}</p><span>Explore →</span></div></a>'

def home(catalog):
    books=[x for x in catalog["books"] if x["book_status"]=="published"]
    tiles="".join(f'''<a class="jt-home-book" href="{e(b['book_page'])}">
<img src="{e(b['cover'])}" alt="{e(b['title'])} {e(b['edition'])} official cover" width="240" height="360" loading="lazy">
<span>{e(b["title"])}{ " · Novella" if b["edition"]=="Novella" else ""}</span></a>''' for b in books)
    routes=[
      ("01","Read a mystery","Five novels and a separate Hollow Bell novella. Find the story mechanism that catches your imagination.","books.html","Shop the Books"),
      ("02","Hear a mystery","Six complete Vivian audiobooks available now at the limited-time $1.99 price.","audiobooks.html","Shop Audiobooks"),
      ("03","Try a first chapter","Read a chapter or hear the narrator demos before you decide.","samples.html","Explore Free Samples")
    ]
    paths="".join(f'<a class="jt-path" href="{url}"><small>{num} / JAYTREE</small><h3>{title}</h3><p>{copy}</p><strong>{action} →</strong></a>' for num,title,copy,url,action in routes)
    media=media_card("upcoming-books.html","images/upcoming/where-mercy-stood-1600.webp","Upcoming mystery","Where Mercy Stood","A town stood here. The records tell another story.")+media_card("experiences-v2.html","images/interactive/JayTree_Interactive_Hidden_Page_Hero.webp","Enter the experience","Mystery Challenges & Videos","Watch a case unfold, search for clues, then see the reveal.")+media_card("reading-guides.html","images/upcoming/the-fifth-copy-1600.webp","Go deeper","The Reader Guides","Explore the unique mysteries of memory, evidence, records and silence.")
    return body("home","Psychological Mysteries, Books & Audiobooks","Discover suspense novels, first chapter samples and Vivian audiobooks direct from JayTree Books.",
f'''<section class="jt-hero" id="top"><div class="jt-wrap jt-hero-grid">
<div><div class="jt-overline">Psychological mysteries · Stories that stay</div><h1>Every story<br><em>leaves a trace.</em></h1>
<p>Impossible rehearsals. Forgotten people. Cold cases beneath the ice.
At JayTree Books, each mystery begins with a question you can name—and an answer that refuses to stay simple.</p>
<div class="jt-actions"><a class="jt-btn primary" href="books.html" data-track="storefront_books">Explore the Books</a>
<a class="jt-btn secondary" href="audiobooks.html" data-track="storefront_audio">Shop Audiobooks</a></div>
</div><div class="jt-hero-art"><a href="books/second-draft.html" aria-label="Discover Second Draft">
<img src="images/optimized/second-draft.webp" width="300" height="450" alt="Second Draft official published book cover" fetchpriority="high"></a>
<span>Featured mystery · Second Draft</span></div></div></section>
<section class="jt-section" id="start-here"><div class="jt-wrap"><div class="jt-overline">Choose your doorway</div>
<h2>Enter the mystery your way.</h2><div class="jt-path-grid">{paths}</div></div></section>
<section class="jt-section jt-dark" id="books"><div class="jt-wrap"><div class="jt-overline">The collection</div>
<h2>Six books. Six different secrets.</h2><p>Five full novels and a shorter, separate <em>Hollow Bell</em> novella.</p>
<div class="jt-home-books">{tiles}</div><div class="jt-actions" style="margin-top:25px"><a class="jt-btn secondary" href="books.html">Explore all book editions</a></div>
</div></section>
<section class="jt-section jt-home-audio" id="audiobooks"><div class="jt-wrap jt-hero-grid">
<div><div class="jt-overline">Available now · $1.99 each</div><h2>Hear the story<br><em>after dark.</em></h2>
<p>All six complete audiobooks are available now with Vivian narration. Enjoy direct MP3 and chaptered M4B downloads.</p>
<p>Alternative full-length narrator editions are coming soon. Preview the voices today.</p>
<div class="jt-actions"><a class="jt-btn primary" href="audiobooks.html" data-track="storefront_audio">Shop all six audiobooks</a>
<a class="jt-btn secondary" href="samples.html" data-track="storefront_samples">Hear samples</a></div></div>
<div class="jt-hero-art"><a href="audiobooks.html"><img src="images/optimized/the-hollow-bell.webp" alt="The Hollow Bell full novel official cover" loading="lazy"></a><span>Six complete Vivian editions</span></div>
</div></section>
<section class="jt-section" id="upcoming-novels"><div class="jt-wrap"><div class="jt-overline">On the horizon</div>
<h2>The stories are still unfolding.</h2><div class="jt-media-grid">{media}</div></div></section>
<section class="jt-section jt-dark" id="challenge"><div class="jt-wrap"><div class="jt-overline">The mystery doesn't end at the page</div>
<h2>Watch. Question. Solve.</h2><p>The first Mystery Challenge reveal is live, along with cinematic previews and further investigations.</p>
<div class="jt-actions"><a class="jt-btn primary" href="experiences-v2.html">Enter the Experiences</a>
<a class="jt-btn secondary" href="https://www.youtube.com/watch?v=643W5-_bLPA" target="_blank" rel="noopener noreferrer">Watch Case #001</a></div>
<div id="youtube"></div></div></section>'''+newsletter()+'''<div id="follow"></div><div id="about"></div>''')

def series():
    cards=[
      ("Where Mercy Stood","images/upcoming/where-mercy-stood-1600.webp","A town stood here. The records tell another story.","where-mercy-stood"),
      ("The Fifth Copy","images/upcoming/the-fifth-copy-1600.webp","Five copies. One missing original. Whose version would you trust?","the-fifth-copy"),
      ("The Sixth Town","images/upcoming/the-sixth-town-1600.webp","The road is familiar. The history isn't.","the-sixth-town")
    ]
    art="".join(media_card("upcoming-books.html#"+slug,img,"Upcoming · working title",title,hook) for title,img,hook,slug in cards)
    return body("series","The JayTree Mystery Universe & Upcoming Novels","Follow the mystery universe and preview Where Mercy Stood, The Fifth Copy and The Sixth Town.",
    '''<section class="jt-subhero"><div class="jt-wrap"><span class="jt-overline">One universe · distinct mysteries</span>
<h1>Every secret leads <em>somewhere.</em></h1><p>Discover the published novels, then follow three upcoming mysteries built around disputed records, missing originals and histories that refuse to agree. All release dates are to be announced.</p>
<div class="jt-actions"><a class="jt-btn primary" href="books.html">Read the published books</a><a class="jt-btn secondary" href="upcoming-books.html">Read the full previews</a></div></div></section>
<section class="jt-section"><div class="jt-wrap"><span class="jt-overline">Coming chapters</span><h2>The next three mysteries.</h2><div class="jt-media-grid">'''+art+'''</div><p style="margin-top:20px">Working titles and promotional concept art. No preorders or release dates are implied.</p></div></section>
<section class="jt-section jt-dark"><div class="jt-wrap"><span class="jt-overline">Start anywhere</span><h2>The stories before them.</h2><p>The five published novels and Hollow Bell novella stand on their own, with threads readers may recognize across the wider mystery universe.</p><div class="jt-actions"><a class="jt-btn primary" href="books.html">Browse published books</a><a class="jt-btn secondary" href="samples.html">Read a free first chapter</a></div></div></section>'''+newsletter())

def news():
    arts=[
      ("upcoming-books.html","images/upcoming/where-mercy-stood-1600.webp","Manuscript updates","Three upcoming novels","Discover the next stories taking shape."),
      ("animated-series.html","images/interactive/JayTree_Interactive_Hidden_Page_Hero.webp","On screen","Mystery stories in motion","Explore the cinematic and animated mystery experiences."),
      ("reading-guides.html","images/upcoming/the-fifth-copy-1600.webp","Reader notes","Explore the story mechanisms","Reading guides for cold cases, unreliable memories and psychological suspense."),
    ]
    tiles="".join(media_card(*p) for p in arts)
    return body("news","News & Upcoming Mysteries","Follow upcoming JayTree novels, cinematic trailers and mystery-reader updates.",
    '''<section class="jt-subhero"><div class="jt-wrap"><span class="jt-overline">Behind the pages</span><h1>Something new is <em>taking shape.</em></h1>
<p>New mysteries, trailers, reader guides, and case-file reveals—organized so you can explore without hunting through the homepage.</p></div></section>
<section class="jt-section"><div class="jt-wrap"><span class="jt-overline">Explore the latest project areas</span><h2>Follow your favorite story.</h2><div class="jt-media-grid">'''+tiles+'''</div></div></section>
<section class="jt-section jt-dark"><div class="jt-wrap"><span class="jt-overline">More from JayTree</span><h2>Take the mystery with you.</h2><p>Watch original video work or find us on social channels for short-form clues and atmosphere.</p><div class="jt-actions"><a class="jt-btn primary" href="https://www.youtube.com/@JayTreeBooks" target="_blank" rel="noopener noreferrer">JayTree Books on YouTube</a><a class="jt-btn secondary" href="experiences-v2.html">Videos & Challenges</a></div></div></section>'''+newsletter())

def experiences():
    return body("experiences","Mystery Challenges, Videos & Reading Experiences","Watch mystery case reveals, cinematic book trailers and JayTree video experiences.",
    '''<section class="jt-subhero"><div class="jt-wrap"><span class="jt-overline">Watch · Question · Solve</span><h1>Don't just read<br><em>the mystery.</em></h1>
<p>Discover cinematic book trailers, mini-series work, and interactive mysteries that carry the suspense beyond the page.</p></div></section>
<section class="jt-section"><div class="jt-wrap"><span class="jt-overline">Case #001 · Reveal live</span><h2>Can you solve it before the reveal?</h2><p>Watch the mystery case, decide which clues mattered, then see the official reveal.</p>
<div class="jt-actions"><a class="jt-btn primary" href="https://www.youtube.com/watch?v=643W5-_bLPA" target="_blank" rel="noopener noreferrer">Watch full case</a>
<a class="jt-btn secondary" href="https://www.youtube.com/watch?v=R-5cB9FaVOA" target="_blank" rel="noopener noreferrer">Watch the reveal</a></div></div></section>
<section class="jt-section jt-dark"><div class="jt-wrap"><span class="jt-overline">Watch more</span><h2>Choose another mystery.</h2>
<div class="jt-media-grid">'''+media_card("animated-series.html","images/interactive/JayTree_Interactive_Hidden_Page_Hero.webp","Cinematic storytelling","Animated mini-series","Explore the developing Hollow Bell screen experience.")+media_card("upcoming-books.html#cinematic-teaser","images/upcoming/where-mercy-stood-1600.webp","Next in the universe","Upcoming novels teaser","A 27-second glimpse of the next JayTree mysteries.")+media_card("reading-guides.html","images/upcoming/the-fifth-copy-1600.webp","Read deeper","Reader guides","Explore how each story builds its own mystery mechanism.")+'''</div></div></section>'''+newsletter())

def ensure_buy_panel(source,book,path):
    if book and 'jt-detail-buy' not in source:
        actions=[]
        slug=e(book["slug"])
        if book.get("amazon_url"):
            actions.append('<a class="jt-btn secondary" href="'+e(book["amazon_url"])+'" target="_blank" rel="noopener noreferrer" data-track="amazon" data-book="'+slug+'">Buy the Book</a>')
        if book.get("chapter_page"):
            actions.append('<a class="jt-btn secondary" href="../'+e(book["chapter_page"])+'" data-track="chapter" data-book="'+slug+'">Read Chapter One</a>')
        if book.get("sample_page"):
            actions.append('<a class="jt-btn secondary" href="../'+e(book["sample_page"])+'" data-track="audio_preview" data-book="'+slug+'">Hear a Sample</a>')
        if book.get("audiobook_status") == "available":
            actions.insert(0,'<a class="jt-btn primary" href="'+e(book["payhip_url"])+'" target="_blank" rel="noopener noreferrer" data-track="audiobook_payhip" data-book="'+slug+'">Buy Vivian Audiobook · $'+e(book["audiobook_price_usd"])+'</a>')
        label=e(book["title"])+(" (Novella)" if book["edition"]=="Novella" else "")
        strip='<aside class="jt-detail-buy" aria-label="Choose format for '+label+'"><p>Choose your edition · Vivian audiobook available now; other narrators coming soon.</p><div class="jt-actions">'+''.join(actions)+'</div></aside>'
        m=re.search(r'<section class="book-hero[^"]*".*?</section>',source,flags=re.S)
        if not m:
            raise ValueError(str(path)+" missing existing book hero")
        source=source[:m.end()]+'\n'+strip+source[m.end():]
    return source

def customize(path,root="",page="",book=None):
    source=path.read_text(encoding="utf-8")
    if 'jt-cinematic jt-modernized' in source:
        return ensure_buy_panel(source,book,path)
    # Preserve canonical URLs, structured data, existing main/story sections,
    # action hooks, lazy video playback, PWA, Kit and GA4.
    style=f'<link rel="stylesheet" href="{root}cinematic-site-v2.css">\n'
    script=f'<script src="{root}cinematic-site-v2.js" defer></script>\n'
    if '</head>' not in source:
        raise ValueError(str(path)+" has no closing head")
    source=source.replace('</head>',style+'</head>',1)
    source,count=re.subn(r'<body\b([^>]*)>',lambda m:'<body'+m.group(1).replace('class="','class="jt-cinematic jt-modernized ',1) + (' class="jt-cinematic jt-modernized"' if 'class="' not in m.group(1) else '')+f' data-jt-root="{root}">',source,count=1,flags=re.I)
    if count!=1: raise ValueError(str(path)+" missing body")
    idx=source.index('>',source.index('<body'))+1
    source=source[:idx]+'\n'+header(page,root)+'\n'+source[idx:]
    if '</body>' not in source:raise ValueError(str(path)+" missing end body")
    source=source.replace('</body>',script+'</body>',1)
    source=ensure_buy_panel(source,book,path)
    return source


def modernize_catalog(page, key):
    """Shared navigation for the three generated storefronts without altering static cards."""
    source=(ROOT/page).read_text(encoding="utf-8")
    if '<header class="jt-header">' in source:
        return source
    old=re.search(r'<header class="sf-(?:header|cine-header)"[^>]*>.*?</header>',source,flags=re.S)
    if not old:
        raise ValueError(page+" missing old header")
    source=source[:old.start()]+header(key)+source[old.end():]
    if '<body class="sf-site ' not in source:
        raise ValueError(page+" missing body class")
    source=source.replace('<body class="sf-site ','<body class="jt-cinematic sf-site ',1)
    source=source.replace('</head>','<link rel="stylesheet" href="cinematic-site-v2.css">\n</head>',1)
    source=source.replace('</body>','<script src="cinematic-site-v2.js" defer></script>\n</body>',1)
    return source


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    action=parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write",action="store_true")
    action.add_argument("--check",action="store_true")
    args=parser.parse_args()
    catalog=json.loads(CATALOG.read_text(encoding="utf-8"))
    pages={
      "home-v2.html":home(catalog),
      "series-v2.html":series(),
      "news-v2.html":news(),
      "experiences-v2.html":experiences()
    }
    # The catalog cards remain generated by build_storefront_catalog.py.
    for page,key in (("books.html","books"),("samples.html","samples"),("audiobooks.html","audio")):
        pages[page]=modernize_catalog(page,key)
    # Preserve complete listening player scripts and chapter text; add only common chrome.
    for folder,pattern in (("audio","book-*-sample.html"),("chapters","book-*-first-chapter.html")):
        for f in sorted((ROOT/folder).glob(pattern)):
            pages[str(f.relative_to(ROOT)).replace("\\","/")]=customize(f,root="../")
    # Modernize, without replacing, original evergreen and commerce editorial pages.
    for path in LEGACY:
        f=ROOT/path
        if f.exists():pages[path]=customize(f, page="about" if path=="about.html" else "")
    for b in catalog["books"]:
        f=ROOT/b["book_page"]
        if f.exists() and b["book_status"]=="published":
            pages[b["book_page"]]=customize(f,root="../",book=b)
    changed=[]
    for path,html_doc in pages.items():
        f=ROOT/path
        if not f.exists() or f.read_text(encoding="utf-8")!=html_doc:
            changed.append(path)
            if args.write:
                f.parent.mkdir(parents=True,exist_ok=True)
                f.write_text(html_doc,encoding="utf-8")
    if args.check and changed:
        print("Out of sync:",", ".join(changed))
        return 1
    print(("Built" if args.write else "Validated"),len(pages),"full-site pages; updated",len(changed))
    if changed:print("Changed:",", ".join(changed))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
