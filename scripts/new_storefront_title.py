#!/usr/bin/env python3
"""Stage a new JayTree title in the v2 catalog without publishing it.

Example:
  python scripts/new_storefront_title.py --title "A New Mystery" \
    --tagline "A hidden truth" --description "Short reader-facing hook." --write

The default is a dry run; --write appends an unpublished entry only.
"""
import argparse
import json
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "data" / "storefront-catalog.json"

def slugify(value):
    value = unicodedata.normalize("NFKD", value).encode("ascii","ignore").decode()
    value = re.sub(r"[^a-z0-9]+","-",value.lower()).strip("-")
    if not value: raise ValueError("title must contain letters or numbers")
    return value

def stage(data, title, edition, description, tagline, audio_planned=False):
    slug = slugify(title)
    if any(book["slug"] == slug for book in data["books"]):
        raise ValueError(f"Title slug already exists: {slug}")
    entry = {
        "slug":slug, "title":title, "edition":edition,
        "description":description, "tagline":tagline,
        "cover":"", "book_page":"", "amazon_url":"",
        "sample_page":"", "chapter_page":"", "payhip_url":"",
        "book_status":"coming_soon",
        "audiobook_status":"coming_soon" if audio_planned else "not_planned",
        "kindle_unlimited":False
    }
    data["books"].append(entry)
    return entry

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--title",required=True)
    p.add_argument("--edition",default="Novel",choices=["Novel","Novella","Full novel"])
    p.add_argument("--description",required=True)
    p.add_argument("--tagline",required=True)
    p.add_argument("--audiobook-coming-soon",action="store_true")
    p.add_argument("--write",action="store_true",help="Actually append draft to catalog")
    args=p.parse_args()
    data=json.loads(MANIFEST.read_text(encoding="utf-8"))
    entry=stage(data,args.title,args.edition,args.description,args.tagline,args.audiobook_coming_soon)
    print(json.dumps(entry,indent=2,ensure_ascii=False))
    if args.write:
        MANIFEST.write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
        print("Staged only: not published, no checkout links. Regenerate the pages before review.")
    else:
        print("Dry run: nothing changed. Pass --write to stage it.")
if __name__=="__main__":
    main()
