"""Generate non-publishable, offline product previews from the site catalog."""
import argparse
import html
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def candidates(catalog):
    rows = [b for b in catalog["books"] if b.get("audiobook_status") == "available"]
    if len(rows) != 6 or len({b["slug"] for b in rows}) != 6 or len({b["payhip_url"] for b in rows}) != 6:
        raise ValueError("Expected six distinct releases")
    for b in rows:
        if b["narrator"] != "Vivian" or not re.fullmatch(r"[a-z0-9-]+", b["slug"]):
            raise ValueError("Unexpected release")
        if not re.fullmatch(r"[1-9][0-9]*\.[0-9]{2}", b["audiobook_price_usd"]):
            raise ValueError("Invalid advertised price")
        if not re.fullmatch(r"https://payhip.com/b/[A-Za-z0-9]+", b["payhip_url"]):
            raise ValueError("Invalid checkout")
        for field in ("cover", "sample_page", "book_page"):
            path = (ROOT / b[field]).resolve()
            if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
                raise ValueError("Missing catalog asset")
    return rows

def render(b):
    e = html.escape
    title = e(b["title"] + " - " + b["edition"] + " - Audiobook")
    def url(key):
        return e("https://jaytreebooks.com/" + b[key], quote=True)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow">
<title>{title} | Preview</title><style>body{{background:#191919;color:#f4eede;font:18px/1.6 system-ui;margin:0}}main{{max-width:780px;margin:auto;padding:24px}}img{{max-width:280px;width:100%;height:auto}}a{{color:#e8ca90}}aside{{border:1px solid #bda570;padding:12px}}button{{padding:12px;font:inherit}}</style></head><body><main>
<aside>OFFLINE DEVELOPMENT PREVIEW. Advertised price only. Checkout not verified; not for publication or Shopping submission.</aside>
<p>JayTree Books / Audiobooks</p><h1>{title}</h1><img src="{url('cover')}" alt="{title} cover">
<p>Narrated by Vivian Arlow</p><p>{e(b['description'])}</p><p>USD {e(b['audiobook_price_usd'])} (advertised)</p>
<p><a href="{url('sample_page')}">Listen to sample</a></p><button disabled>Checkout pending verification</button>
<p><a href="{url('book_page')}">Existing book page</a></p></main></body></html>"""

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    out = parser.parse_args().output.resolve()
    if out.is_relative_to(ROOT.resolve()):
        parser.error("Output must be outside the website repository")
    rows = candidates(json.loads((ROOT/"data/storefront-catalog.json").read_text(encoding="utf-8-sig")))
    out.mkdir(parents=True, exist_ok=False)
    for b in rows:
        (out/(b["slug"]+"-vivian.html")).write_text(render(b), encoding="utf-8")
    print("Six offline previews written")
if __name__ == "__main__":
    main()
