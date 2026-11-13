#!/usr/bin/env python3
"""Give every secondary page the mobile Menu button (the home page has its own). Idempotent. Run from repo root."""
import re
PAGES=['about','guides','parks','peru','puerto-rico','udaipur']
CSS='''<style id="menu-css">
.menu-btn{display:none}
.menu-panel{display:contents}
@media(max-width:820px){
 .bar.home-bar{flex-wrap:nowrap!important;justify-content:space-between!important;position:relative;padding:4px 12px!important;gap:8px!important}
 .home-bar .logo{font-size:17px;padding:6px 2px}
 .menu-btn{display:inline-flex;align-items:center;gap:8px;min-height:44px;padding:0 14px;background:transparent;border:1px solid #2B424B;color:#E8EEF0;font:500 14px "Space Grotesk",system-ui,sans-serif;cursor:pointer}
 .menu-ico{width:14px;height:10px;background:linear-gradient(currentColor 0 0) top/100% 2px no-repeat,linear-gradient(currentColor 0 0) center/100% 2px no-repeat,linear-gradient(currentColor 0 0) bottom/100% 2px no-repeat}
 .menu-btn[aria-expanded="true"]{background:#7CE0C3;color:#0E1A1F;border-color:#7CE0C3}
 .menu-btn:focus-visible{outline:3px solid #F2B94B;outline-offset:2px}
 .menu-panel{display:none;position:absolute;left:0;right:0;top:100%;flex-direction:column;gap:16px;padding:12px 12px 18px;background:#0E1A1F;border-bottom:1px solid #2B424B;box-shadow:0 18px 30px rgba(0,0,0,.45);z-index:60}
 .bar.open .menu-panel{display:flex}
 .home-bar .nav{flex-direction:column;width:100%!important;margin:0!important;order:0;gap:0;border-top:1px solid #2B424B;overflow:visible}
 .home-bar .nav a{padding:0 4px;font-size:16px;border-bottom:1px solid #2B424B}
 .home-bar .hsearch{margin:0;width:100%}
 .home-bar .hsearch input{flex:1;width:auto}
}
</style>'''
JS='''<script id="menu-js">(function(){var b=document.querySelector('.bar'),m=document.getElementById('menuBtn');if(!b||!m)return;function s(o){b.classList.toggle('open',o);m.setAttribute('aria-expanded',o?'true':'false')}m.addEventListener('click',function(){s(!b.classList.contains('open'))});document.addEventListener('keydown',function(e){if(e.key==='Escape')s(false)});document.addEventListener('click',function(e){if(!b.contains(e.target))s(false)});window.addEventListener('resize',function(){if(innerWidth>820)s(false)})})();</script>'''
for p in PAGES:
    f=f'{p}/index.html'; t=open(f).read()
    if 'id="menuBtn"' in t: print(p,'already'); continue
    old=re.search(r'(<header class="bar home-bar"><a class="logo" href="/">run away with rhea</a>)(<nav.*?</form>)(</header>)',t,re.S)
    assert old,p
    new=old.group(1)+'<button type="button" class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="menuPanel"><span class="menu-ico" aria-hidden="true"></span>Menu</button><div class="menu-panel" id="menuPanel">'+old.group(2)+'</div>'+old.group(3)
    t=t.replace(old.group(0),new,1)
    t=t.replace('</head>',CSS+'</head>',1).replace('</body>',JS+'</body>',1)
    open(f,'w').write(t); print(p,'ok')
