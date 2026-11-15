#!/usr/bin/env python3
"""Produce branded 1200x630 page-specific JayTree social artwork.
Run on authorized JayTree computer: PYTHONPATH=<isolated Pillow directory> python scripts/build_social_art.py
Assets use existing approved artwork and book covers. No external network or AI dependency.
"""
from __future__ import annotations
from pathlib import Path
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "images" / "social" / "previews"
OUT.mkdir(parents=True, exist_ok=True)
W, H = 1200, 630
CREAM = (246, 228, 193)
GOLD = (235, 186, 97)
NAVY = (4, 12, 19)

FONT_DIR = Path("C:/Windows/Fonts")
SERIF = str(FONT_DIR / "georgia.ttf")
SERIF_BOLD = str(FONT_DIR / "georgiab.ttf")
SANS = str(FONT_DIR / "arial.ttf")
SANS_BOLD = str(FONT_DIR / "arialbd.ttf")

def font(path, size):
    return ImageFont.truetype(path, size)

def src(path):
    f = ROOT / path
    if not f.is_file():
        raise FileNotFoundError(path)
    return Image.open(f).convert("RGBA")

def add_backdrop(art, path, focus=(0.53, 0.46), dim=0):
    photo = ImageOps.fit(src(path), (W, H), method=Image.Resampling.LANCZOS, centering=focus).convert("RGBA")
    if dim:
        photo = Image.alpha_composite(photo, Image.new("RGBA", (W,H),(0,0,0,dim)))
    if path.startswith("images/upcoming/"):
        photo = photo.filter(ImageFilter.GaussianBlur(18))
    art.alpha_composite(photo)

def atmospheric_overlay(art, strength=1):
    overlay = Image.new("RGBA", (W,H))
    pix = overlay.load()
    for x in range(W):
        # Stronger on editorial left, atmospheric blue on right. Text remains legible.
        left = 226 * (1 - min(1,x/825))**1.75 + 18
        right = max(0, (x-950)/250) * 52
        for y in range(H):
            vignette = int(38*(abs(y-H/2)/(H/2))**2)
            pix[x,y] = (1, 9, 15, int(min(242,(left+right+vignette)*strength)))
    art.alpha_composite(overlay)

def drop_shadow(image, x, y, blur=20, opacity=210):
    silhouette = Image.new("RGBA", image.size)
    silhouette.paste((0,0,0,opacity), (0,0,*image.size), image.getchannel("A"))
    shadow = silhouette.filter(ImageFilter.GaussianBlur(blur))
    art.alpha_composite(shadow,(x+10,y+17))

def compose_cover(art, path, x, y, height, rotation=0):
    im = src(path)
    neww = int(height * im.width / im.height)
    im = im.resize((neww,height), Image.Resampling.LANCZOS)
    if rotation:
        im = im.rotate(rotation,expand=True,resample=Image.Resampling.BICUBIC)
    # Fine gold trim around the published artwork.
    canvas = Image.new("RGBA", (im.width+7,im.height+7),(219,173,89,255))
    canvas.alpha_composite(im,(3,3))
    drop_shadow(canvas,x,y,15,235)
    art.alpha_composite(canvas,(x,y))
    return canvas.width,canvas.height

def text_shadow(d, xy, content, f, fill, stroke_width=0):
    x,y=xy
    d.text((x+2,y+3),content,font=f,fill=(0,0,0,190),stroke_width=stroke_width,stroke_fill=(0,0,0,155))
    d.text((x,y),content,font=f,fill=fill,stroke_width=stroke_width,stroke_fill=(0,0,0,100))

def ribbon(d, xy, text):
    x,y=xy
    f=font(SANS_BOLD,18)
    tw=int(d.textlength(text,font=f))
    d.rounded_rectangle((x,y,x+tw+30,y+37),radius=6,fill=(217,164,74),outline=(255,221,148),width=1)
    d.text((x+15,y+8),text,font=f,fill=(11,15,17))

def letterspaced(d,text,xy,f,spacing=4,fill=GOLD):
    x,y=xy
    for c in text:
        d.text((x,y),c,font=f,fill=fill,stroke_width=0)
        x+=d.textlength(c,font=f)+spacing

def title_block(art, main, sub, eyebrow="JAYTREE BOOKS", ribbons=()):
    d=ImageDraw.Draw(art)
    d.line((74,85,191,85),fill=(206,161,82),width=2)
    letterspaced(d,eyebrow,(74,110),font(SANS_BOLD,17),3)
    lines=main.split("\n")
    size=76 if max(map(len,lines))<=16 else (64 if max(map(len,lines))<=19 else 54)
    f=font(SERIF_BOLD,size)
    y=169
    for line in lines:
        text_shadow(d,(70,y),line,f,CREAM)
        y+=size+8
    y+=10
    d.line((75,y,405,y),fill=GOLD,width=2)
    y+=20
    sf=font(SERIF,25)
    for line in sub.split("\n"):
        text_shadow(d,(75,y),line,sf,(230,220,196))
        y+=36
    if ribbons:
        ry=min(515,max(448,y+9))
        for i,r in enumerate(ribbons):
            ribbon(d,(76+205*i,ry),r)
    # Bottom branding identity independent of page image.
    d.line((76,582,494,582),fill=(209,170,92,160),width=1)
    d.text((76,590),"JAYTREEBOOKS.COM",font=font(SANS_BOLD,15),fill=GOLD)

def save(art, name):
    file=OUT / (name+".jpg")
    art.convert("RGB").save(file,"JPEG",quality=88,subsampling=0,optimize=True)
    with Image.open(file) as verify:
        if verify.size!=(1200,630): raise RuntimeError("Invalid OG dimensions")
    print(f"OG {file.relative_to(ROOT)} {file.stat().st_size}")
    return file

SCENES = {
"home":("images/optimized/moonlit-manor.webp","MYSTERIES THAT\nSTAY WITH YOU","Novels, audiobooks and\nstories worth investigating.",["second-draft","the-hollow-bell","the-correction"]),
"books":("images/optimized/moonlit-manor.webp","MYSTERY\nBOOKS","Five novels. One novella.\nEvery story leaves a trace.",["the-hollow-year","the-hollow-bell","the-hollow-bell-novella","the-absconding"]),
"samples":("images/optimized/reading-guides-desk.webp","FIRST\nIMPRESSIONS","Read a chapter.\nHear a mystery.",["second-draft","the-hollow-year"]),
"series":("images/upcoming/the-sixth-town-1600.webp","THE MYSTERY\nUNIVERSE","Distinct stories.\nUnexpected connections.",[]),
"news":("images/upcoming/where-mercy-stood-1600.webp","NEWS &\nUPDATES","New mysteries, trailers\nand stories on the horizon.",[]),
"experiences":("images/interactive/JayTree_Interactive_Mystery_Background.webp","MYSTERY\nEXPERIENCES","Watch. Question. Solve.",[]),
"about":("images/optimized/reading-guides-desk.webp","ABOUT\nJAYTREE BOOKS","Independent storytelling.\nUnforgettable questions.",[]),
"upcoming-books":("images/upcoming/the-sixth-town-1600.webp","UPCOMING\nNOVELS","Where Mercy Stood.\nThe Fifth Copy. The Sixth Town.",[]),
"reading-guides":("images/optimized/reading-guides-desk.webp","READING\nGUIDES","Look closer at the clues.",[]),
"case-files":("images/optimized/moonlit-manor.webp","JOIN THE\nCASE FILES","Be the first to see\nwhat's coming next.",[]),
"animated-series":("images/optimized/hollow-bell-series-trailer.webp","ON SCREEN","Animated mysteries\nand cinematic stories.",[]),
"mystery-books":("images/optimized/moonlit-manor.webp","MYSTERY\nNOVELS","Discover the collection.",[]),
"psychological-mystery-books":("images/optimized/reading-guides-desk.webp","PSYCHOLOGICAL\nMYSTERIES","Truth is rarely the\nwhole story.",[]),
"kindle-unlimited-mystery-books":("images/optimized/moonlit-manor.webp","READ MORE\nMYSTERIES","Explore Kindle Unlimited\nJayTree editions.",[]),
 "small-town-mystery-books":("images/optimized/moonlit-manor.webp","SMALL TOWN\nSECRETS","Ordinary streets.\nImpossible discoveries.",[]),
 "cold-case-mystery-books":("images/optimized/moonlit-manor.webp","COLD CASE\nMYSTERIES","Some answers surface\nlong after they should.",["the-hollow-bell"]),
 "supernatural-mystery-books":("images/interactive/JayTree_Interactive_Mystery_Background.webp","UNSETTLING\nMYSTERIES","The unexplained starts\nwith a question.",[]),
}
catalog=json.loads((ROOT/"data/storefront-catalog.json").read_text(encoding="utf-8"))
books={b["slug"]:b for b in catalog["books"]}
for slug,(bg,main,subtitle,showbooks) in SCENES.items():
    art=Image.new("RGBA",(W,H),NAVY)
    add_backdrop(art,bg, focus=(.58,.45))
    atmospheric_overlay(art,1)
    if showbooks:
        # A cohesive display of multiple genuine official covers
        count=len(showbooks)
        heights={1:[410],2:[350,305],3:[344,400,324],4:[260,333,300,270]}[count]
        xs={1:[820],2:[740,936],3:[695,829,1021],4:[705,833,955,1070]}[count]
        ys={1:[122],2:[150,186],3:[177,114,195],4:[230,150,183,218]}[count]
        for i,bookslug in enumerate(showbooks):
            compose_cover(art,books[bookslug]["cover"],xs[i],ys[i],heights[i])
    elif slug in ("series","upcoming-books"):
        for i,bg2 in enumerate(("images/upcoming/where-mercy-stood-800.webp","images/upcoming/the-fifth-copy-800.webp","images/upcoming/the-sixth-town-800.webp")):
            tile=src(bg2)
            tile=ImageOps.fit(tile,(172,330),centering=(.5,.5))
            x=625+i*184
            drop_shadow(tile,x,167,13,205)
            art.alpha_composite(tile,(x,167))
    elif slug=="case-files":
        compose_cover(art,books["the-hollow-bell"]["cover"],880,155,325)
    elif slug=="about":
        compose_cover(art,books["the-correction"]["cover"],915,143,363)
    elif slug=="reading-guides":
        compose_cover(art,books["the-hollow-year"]["cover"],883,160,355)
    elif slug=="animated-series":
        # Preserve cinematic trailer still as the strongest focal feature
        pass
    title_block(art,main,subtitle)
    save(art,slug)

# Match the actual approved page hero: house + gold headphones embracing a real cover.
art=Image.new("RGBA",(W,H),NAVY)
add_backdrop(art,"images/optimized/moonlit-manor.webp",focus=(.58,.5))
atmospheric_overlay(art,1.02)
cover=src(books["second-draft"]["cover"]).resize((184,278),Image.Resampling.LANCZOS)
drop_shadow(cover,848,195,17,225)
art.alpha_composite(cover,(848,195))
headphones=src("images/optimized/bronze-headphones.webp")
headphones=headphones.resize((570,570),Image.Resampling.LANCZOS)
art.alpha_composite(headphones,(661,20))
title_block(art,"AUDIOBOOKS","Six complete Vivian editions.\nListen first or buy direct.",ribbons=("$1.99 EACH",))
save(art,"audiobooks")

# Every published book has its own landscape, not a repeated site-wide Challenge card.
for slug,book in books.items():
    if slug in ("the-hollow-bell","the-hollow-bell-novella"):
        backdrop="images/optimized/moonlit-manor.webp"
    elif slug in ("the-correction","second-draft"):
        backdrop="images/optimized/reading-guides-desk.webp"
    else:
        backdrop="images/optimized/moonlit-manor.webp"
    art=Image.new("RGBA",(W,H),NAVY)
    add_backdrop(art,backdrop,focus=(.67,.48))
    atmospheric_overlay(art,1.06)
    compose_cover(art,book["cover"],810,100,415)
    name=book["title"].upper()
    if name=="THE HOLLOW BELL":name="THE HOLLOW\nBELL"
    elif name=="THE HOLLOW YEAR":name="THE HOLLOW\nYEAR"
    elif name=="THE ABSCONDING":name="THE\nABSCONDING"
    title_block(art,name,book["tagline"],ribbons=("NOVELLA",) if book["edition"]=="Novella" else (("FULL NOVEL",) if book["edition"]=="Full novel" else ()))
    save(art,"book-"+slug)

print("TOTAL",len(list(OUT.glob("*.jpg"))))
