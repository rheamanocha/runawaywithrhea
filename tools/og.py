#!/usr/bin/env python3
"""Build 1200x630 share images (img/og/*.jpg) and write Open Graph / Twitter meta tags into each page.
Run from the repo root: python3 tools/og.py"""
import re, os
from PIL import Image, ImageDraw, ImageFont
SITE='https://runawaywithrhea.com'
# page file -> (share image name, source photo, vertical focus 0-1, description)
PAGES={
 'index.html':('home','peru/img/p00.jpg',0.5,"Adventure travel guides, itineraries, and honest tips from Rhea. Explore the map to find your next trip.",'/'),
 'about/index.html':('about','about/rhea-machu-picchu.jpg',0.62,"Hi, I'm Rhea, a travel content creator sharing adventure travel stories, itineraries, and tips.",'/about/'),
 'guides/index.html':('guides','puerto-rico/img/p00.jpg',0.62,"All of my travel guides in one place: Peru, Puerto Rico, Udaipur, and more on the way.",'/guides/'),
 'ojai/index.html':('ojai','ojai/img/p00.jpg',0.5,"Ojai, California: a charming small town full of hidden gems, from Bart's Books to a trail ride, plus where we stayed and ate.",'/ojai/'),
 'parks/index.html':('parks','peru/img/p00.jpg',0.5,"My national parks tracker: the parks I've visited and the ones still on the list.",'/parks/'),
 'peru/index.html':('peru','peru/img/p00.jpg',0.5,"Two weeks in Peru: the Amazon, Cusco, Ausangate on horseback, and the Inca Trail to Machu Picchu, with tips for each stop.",'/peru/'),
 'puerto-rico/index.html':('puerto-rico','puerto-rico/img/p00.jpg',0.62,"Six days in Puerto Rico with friends: Old San Juan, Culebra, El Yunque, a zipline, and a bioluminescent kayak, plus where we ate.",'/puerto-rico/'),
 'udaipur/index.html':('udaipur','udaipur/img/p00.jpg',0.5,"A first-timer's guide to Udaipur: City Palace, a boat ride on Lake Pichola, where to eat, and where to stay.",'/udaipur/'),
}
W,H=1200,630
def card(src,focus,name):
    im=Image.open(src).convert('RGB'); s=W/im.width
    if im.height*s<H: s=H/im.height
    im=im.resize((round(im.width*s),round(im.height*s)),Image.LANCZOS)
    x=(im.width-W)//2; y=int((im.height-H)*focus); im=im.crop((x,y,x+W,y+H))
    if name=='home':   # branded card for the home page
        ov=Image.new('RGB',(W,H),(10,19,23)); im=Image.blend(im,ov,0.62)
        d=ImageDraw.Draw(im)
        f1=ImageFont.truetype('/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf',92)
        f2=ImageFont.truetype('/usr/share/fonts/opentype/inter/Inter-Regular.otf',38)
        d.text((80,H//2-86),'run away with rhea',font=f1,fill=(238,243,244))
        d.text((84,H//2+36),'Adventure travel guides and itineraries',font=f2,fill=(124,224,195))
    return im
for page,(name,src,focus,desc,path) in PAGES.items():
    out=f'img/og/{name}.jpg'
    if name!='home': card(src,focus,name).save(out,quality=84,optimize=True)  # home.jpg is a hand-built map card (live map + title); keep it
    t=open(page).read()
    t=re.sub(r'\n?<!-- og:start -->.*?<!-- og:end -->','',t,flags=re.S)
    title=re.search(r'<title>(.*?)</title>',t,re.S).group(1)
    v='?v=2' if name=='home' else ''
    d=desc.replace("'","&#39;")
    tags=f'''<!-- og:start -->
<meta name="description" content="{d}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="run away with rhea">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{SITE}/{out}{v}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/{out}{v}">
<!-- og:end -->'''
    t=t.replace('</title>','</title>\n'+tags,1)
    open(page,'w').write(t); print(page,os.path.getsize(out)//1024,'KB')
