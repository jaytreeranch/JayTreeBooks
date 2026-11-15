"""Test the extracted portable review using the local Chrome on JT-DESKTOP."""
from pathlib import Path
from time import monotonic, sleep
import base64, json, os, subprocess, sys, tempfile
import requests, websocket
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
root = Path(sys.argv[1]).resolve()
out = Path(sys.argv[2]).resolve()
out.mkdir(parents=True, exist_ok=True)
base_url = sys.argv[3] if len(sys.argv) > 3 else None
books = json.loads((root / 'data/storefront-catalog.json').read_text('utf-8'))['books']
pages = ['index.html', 'books.html', 'audiobooks.html', 'samples.html', 'series-v2.html', 'about.html', 'news-v2.html', 'experiences-v2.html', 'case-files.html', 'chapters/book-1-first-chapter.html', 'upcoming-books.html'] + [book[key] for book in books for key in ('book_page', 'sample_page')]
receipts = []
fail = []
checks = {}

def record(kind, detail, ok):
    checks[kind] = checks.get(kind, 0) + 1
    if not ok:
        fail.append([kind, detail])
with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as profile:
    chrome = Path(os.environ['ProgramFiles']) / 'Google/Chrome/Application/chrome.exe'
    proc = subprocess.Popen([str(chrome), '--headless=new', '--disable-gpu', '--no-first-run', '--disable-extensions', '--remote-debugging-address=127.0.0.1', '--remote-debugging-port=0', '--user-data-dir=' + profile, '--autoplay-policy=no-user-gesture-required', 'about:blank'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for i in range(150):
            portfile = Path(profile) / 'DevToolsActivePort'
            if portfile.is_file():
                break
            sleep(0.1)
        port = portfile.read_text().splitlines()[0]
        tab = next((t for t in requests.get('http://127.0.0.1:' + port + '/json', timeout=3).json() if t['type'] == 'page'))
        ws = websocket.create_connection(tab['webSocketDebuggerUrl'], timeout=12, suppress_origin=True)
        sequence = 0

        def cmd(method, params=None):
            global sequence
            sequence += 1
            ws.send(json.dumps(dict(id=sequence, method=method, params=params or {})))
            while True:
                msg = json.loads(ws.recv())
                if msg.get('id') == sequence:
                    if 'error' in msg:
                        raise RuntimeError(msg['error'])
                    return msg['result']

        def ev(js):
            res = cmd('Runtime.evaluate', dict(expression=js, returnByValue=True, awaitPromise=True))
            if 'exceptionDetails' in res:
                raise RuntimeError(str(res)[:800])
            return res['result'].get('value')

        def visit(path):
            url = urljoin(base_url, path) if base_url else (root / path).as_uri()
            cmd('Page.navigate', {'url': url})
            for i in range(70):
                if ev('location.href===' + json.dumps(url) + ' && document.readyState!=="loading"'):
                    return
                sleep(0.05)
            raise RuntimeError(path)
        cmd('Page.enable')
        cmd('Page.bringToFront')
        cmd('Emulation.setFocusEmulationEnabled', {'enabled': True})
        cmd('Network.enable')
        cmd('Network.setBlockedURLs', {'urls': ['*googletagmanager.com*', '*youtube.com/embed/*', '*youtube-nocookie.com/embed/*', '*fonts.googleapis.com*']})
        cmd('Emulation.setEmulatedMedia', {'features': [{'name': 'prefers-reduced-motion', 'value': 'reduce'}]})
        for w, h in [(1440, 900), (768, 980), (390, 844), (320, 740)]:
            cmd('Emulation.setDeviceMetricsOverride', dict(width=w, height=h, deviceScaleFactor=1, mobile=False))
            for p in pages:
                visit(p)
                layout = ev('({width:document.documentElement.scrollWidth,main:!!document.querySelector("main"),title:document.title})')
                record('layout', [p, w, layout], layout['width'] <= w + 1 and layout['main'])
                if p in ['index.html', 'audiobooks.html', 'books.html', 'samples.html', 'books/second-draft.html', 'audio/book-1-sample.html', 'about.html', 'news-v2.html', 'case-files.html']:
                    data = cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 76})['data']
                    (out / (p.replace('/', '_') + str(w) + '.jpg')).write_bytes(base64.b64decode(data))
            visit('samples.html')
            covers = ev("""(async () => {
              const images = [...document.querySelectorAll('.sf-sample-cover img')];
              for (const img of images) { img.loading = 'eager'; await img.decode(); }
              return images.map(img => {
                const bounds = img.getBoundingClientRect();
                return img.naturalWidth > 0 && bounds.width > 0 &&
                  Math.abs(bounds.height - bounds.width * img.naturalHeight / img.naturalWidth) < 1;
              });
            })()""")
            record('sample_covers', w, len(covers) == len(books) and all(covers))
            visit('news-v2.html')
            news_art = ev("""(async () => {
              const images = [...document.querySelectorAll('.jt-media-tile img')];
              for (const img of images) { img.loading = 'eager'; await img.decode(); }
              return images.map(img => [img.getAttribute('src'), img.closest('a').getAttribute('href')]);
            })()""")
            record('news_art', w, news_art[1:] == [
                ['images/optimized/hollow-bell-series-trailer.webp', 'animated-series.html'],
                ['images/optimized/reading-guides-desk.webp', 'reading-guides.html']])
            for route, selector in [('news-v2.html', '.jt-media-grid'), ('samples.html', '.sf-sample-grid'), ('series-v2.html', '.jt-section h2')]:
                visit(route)
                ev('document.querySelector(' + json.dumps(selector) + ').scrollIntoView({block:"start",behavior:"instant"})')
                ev('window.scrollBy(0,-96)')
                ev('new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)))')
                photo = cmd('Page.captureScreenshot', {'format': 'jpeg', 'quality': 82})['data']
                (out / (route + '-section-' + str(w) + '.jpg')).write_bytes(base64.b64decode(photo))
            visit('audiobooks.html')
            search = ev('(()=>{document.querySelector(".jt-search summary").click();const s=document.querySelector("#jt-search-input");s.value="Hollow Bell";s.dispatchEvent(new Event("input"));return [...document.querySelectorAll(".jt-search-results a")].map(a=>a.getAttribute("href"))})()')
            record('search', [w, search], all((b['book_page'] in search for b in books if 'hollow-bell' in b['slug'])))
            ev('document.querySelector(".jt-search summary").click()')
            if w <= 768:
                record('menu', w, ev('(()=>{document.querySelector(".jt-mobile summary").click();return document.querySelector(".jt-mobile nav a").getBoundingClientRect().width>0})()'))
                ev('document.querySelector(".jt-mobile summary").click()')
            for b in books:
                slug = b['slug']
                ev('document.querySelector(\'[data-select-book="' + slug + '"]\').focus()')
                cmd('Input.dispatchKeyEvent', dict(type='keyDown', key='Enter', code='Enter', text='\r', windowsVirtualKeyCode=13))
                cmd('Input.dispatchKeyEvent', dict(type='keyUp', key='Enter', code='Enter', windowsVirtualKeyCode=13))
                picked = ev('(()=>{const el=s=>document.getElementById("sf-cine-featured-"+s);return [el("cover").getAttribute("src"),el("buy").getAttribute("href"),el("sample").getAttribute("href"),el("details").getAttribute("href"),el("description").textContent, document.querySelector(".sf-cine-select[aria-pressed=true]").dataset.selectBook]})()')
                record('select', [slug, w, picked], picked == [b['audio_hero'], b['payhip_url'], b['sample_page'], b['book_page'], b['description'], slug])
        for b in books:
            visit(b['sample_page'])
            states = ev('(async()=>{let rows=[];for(const a of document.querySelectorAll("audio")){a.muted=true;await a.play();await new Promise(r=>setTimeout(r,140));a.pause();rows.push([a.currentTime,a.duration])}return rows})()')
            for item in states:
                record('audio', [b['slug'], item], 0 < item[0] < item[1])
        for b in books:
            visit('audiobooks.html')
            link = ev('(() => {const a=document.querySelector(".sf-cine-select[data-select-book=' + b['slug'] + ']");a.scrollIntoView({block:"center"});const r=a.getBoundingClientRect();return [r.x+r.width/2,r.y+r.height/2]})()')
            for phase in ['mousePressed', 'mouseReleased']:
                cmd('Input.dispatchMouseEvent', dict(type=phase, x=link[0], y=link[1], button='left', clickCount=1))
            record('pointer', b['slug'], ev('document.querySelector("#sf-cine-featured-buy").href') == b['payhip_url'])
        def wait_for_page(name):
            for _ in range(80):
                if ev('location.pathname.endsWith(' + json.dumps('/' + name) + ') && document.readyState !== "loading"'):
                    return True
                sleep(.05)
            return False

        if base_url:
            visit_url = urljoin(base_url, '?utm_source=release-qc#audiobooks')
            cmd('Page.navigate', {'url': visit_url})
            for _ in range(120):
                if ev('location.href === ' + json.dumps(visit_url) + ' && !!document.querySelector("#audiobooks a")'):
                    break
                sleep(.05)
            record('campaign', visit_url, ev('document.querySelector("#audiobooks a")?.getAttribute("href")') == 'audiobooks.html')
        visit('index.html')
        ev('document.querySelector("[data-secret-path]").focus()')
        cmd('Input.dispatchKeyEvent', dict(type='keyDown', key='Enter', code='Enter', text='\r', windowsVirtualKeyCode=13))
        cmd('Input.dispatchKeyEvent', dict(type='keyUp', key='Enter', code='Enter', windowsVirtualKeyCode=13))
        record('footer_easter_egg', 'Enter', wait_for_page('interactive.html'))
        for gesture in ('shift-click', 'long-press'):
            visit('interactive.html')
            coords = ev("""(() => {
              const mark = document.querySelector('[data-second-secret]');
              mark.scrollIntoView({block:'center',behavior:'instant'});
              const rect = mark.getBoundingClientRect();
              return {x:rect.x+rect.width/2, y:rect.y+rect.height/2};
            })()""")
            if gesture == 'long-press':
                cmd('Input.dispatchTouchEvent', {'type':'touchStart', 'touchPoints':[coords]})
                sleep(1.4)
                cmd('Input.dispatchTouchEvent', {'type':'touchEnd', 'touchPoints':[]})
            else:
                for phase in ('mousePressed', 'mouseReleased'):
                    cmd('Input.dispatchMouseEvent', dict(type=phase, modifiers=8, button='left', clickCount=1, **coords))
            record('archive_easter_egg', gesture, wait_for_page('echo-archive.html'))
        ws.close()
    finally:
        proc.terminate()
        proc.wait(12)

def product(b):
    try:
        r = requests.get(b['payhip_url'], timeout=12)
        return [b['slug'], r.status_code, b['title'].lower() in r.text.lower()]
    except requests.RequestException as e:
        return [b['slug'], str(e), False]
with ThreadPoolExecutor(max_workers=3) as pool:
    receipts = list(pool.map(product, books))
report = dict(checks=checks, failures=fail, product_pages=receipts)
(out / 'browser-qc.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
print(json.dumps(report))
raise SystemExit(1 if fail else 0)
