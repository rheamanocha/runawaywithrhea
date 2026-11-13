#!/usr/bin/env python3
"""Keep the blurred "ambient" backdrop in sync with each guide page's hero photo.

Every guide page has a fixed .ambient layer behind the content (the hero photo,
blurred and darkened, so the page picks up the photo's colors). This script
points that layer at the page's real hero image (<img class="hero-img">). Pages
with no hero photo yet get the shared teal-and-amber gradient so they still have
the same sheer color wash. Run it after adding or changing a hero image
(tools/sync-tiles.py calls it for you):

    python3 tools/sync-ambient.py
"""
import glob, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLBACK = ('radial-gradient(ellipse at 25% 15%, #5FB57A 0%, transparent 55%), '
            'radial-gradient(ellipse at 80% 70%, #E08A3C 0%, transparent 55%), '
            'linear-gradient(160deg, #2f6b5a, #4a3322)')
RULE = re.compile(r'\.ambient \{ position: fixed; inset: -10%; z-index: -1; background: [^;]*; filter: blur\(70px\)')
FINAL = '.ambient { filter: blur(90px) saturate(1) brightness(0.28); }'

SKIP = {'about', 'guides', 'parks'}  # hub pages keep their own backdrop

def sync():
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, '**', 'index.html'), recursive=True)):
        if os.path.relpath(path, ROOT).split(os.sep)[0] in SKIP:
            continue
        html = open(path, encoding='utf-8').read()
        if 'class="ambient"' not in html or not RULE.search(html):
            continue
        m = re.search(r'<img class="hero-img"[^>]*?src="([^"]+)"', html)
        bg = f'#0A1317 url({m.group(1)}) center / cover no-repeat' if m else f'{FALLBACK} center / cover no-repeat #0A1317'
        new = RULE.sub(lambda _: f'.ambient {{ position: fixed; inset: -10%; z-index: -1; background: {bg}; filter: blur(70px)', html, count=1)
        if FINAL not in new:  # same calm strength everywhere
            new = re.sub(r'\.ambient \{ filter: blur\(90px\)[^}]*\}', FINAL, new, count=1)
        rel = os.path.relpath(path, ROOT)
        if new != html:
            open(path, 'w', encoding='utf-8').write(new); changed += 1
            print(f'ambient: {rel} -> {"hero " + m.group(1) if m else "fallback gradient"}')
    print(f'ambient: {changed} page(s) updated')

if __name__ == '__main__':
    sync()
