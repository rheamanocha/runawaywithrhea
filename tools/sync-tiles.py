#!/usr/bin/env python3
"""Keep tile images in sync with page hero images.

For every page listed in PAGES that has a real hero photo (<img id="heroImg">),
copy it to /img/<slug>.jpg and point both the Guides card and the map card
(TRIPS entry in index.html) at it. Run after changing any hero image:

    python3 tools/sync-tiles.py
"""
import os, re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# page folder -> map trip id (None if the page has no map card)
PAGES = {'udaipur': 'udaipur', 'puerto-rico': 'puertorico'}

def read(p):
    with open(os.path.join(ROOT, p), encoding='utf-8') as f: return f.read()
def write(p, t):
    with open(os.path.join(ROOT, p), 'w', encoding='utf-8') as f: f.write(t)

guides, home = read('guides/index.html'), read('index.html')
for slug, trip in PAGES.items():
    page = read(f'{slug}/index.html')
    m = re.search(r'<img class="hero-img"[^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"', page)
    if not m:
        print(f'skip {slug}: no hero photo yet'); continue
    src, alt = m.group(1), m.group(2)
    im = Image.open(os.path.join(ROOT, slug, src)).convert('RGB')
    if im.width > 1200: im = im.resize((1200, round(im.height * 1200 / im.width)))
    os.makedirs(os.path.join(ROOT, 'img'), exist_ok=True)
    im.save(os.path.join(ROOT, 'img', f'{slug}.jpg'), quality=84, optimize=True)
    tile = f'/img/{slug}.jpg'
    # Guides card
    pat = re.compile(r'(href="/%s/".*?<div class="gm">).*?(</div><div class="gb">)' % re.escape(slug), re.S)
    img = f'<img src="{tile}" alt="{alt}" loading="lazy" width="{im.width}" height="{im.height}">'
    guides, n = pat.subn(lambda mm: mm.group(1) + img + mm.group(2), guides, count=1)
    # Map card
    if trip:
        pat2 = re.compile(r"(\{ id: '%s',.*?)(?: img: '[^']*',)?( zoom:)" % trip)
        home, n2 = pat2.subn(lambda mm: mm.group(1) + f" img: '{tile.lstrip('/')}'," + mm.group(2), home, count=1)
    print(f'{slug}: tile -> {tile} (guides {n}, map {n2 if trip else "-"})')
write('guides/index.html', guides); write('index.html', home)
