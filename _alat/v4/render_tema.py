import json, sys
from playwright.sync_api import sync_playwright
from urllib.parse import quote
from PIL import Image
jobs=json.loads(sys.argv[1])  # [[tema, nama], ...]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx=b.new_context(viewport={"width":432,"height":960},device_scale_factor=2.5,is_mobile=True,has_touch=True)
    for t,n in jobs:
        pg=ctx.new_page(); pg.goto(f"http://localhost:8080/assets/themes/{t}/?to={quote(n)}",wait_until="networkidle"); pg.wait_for_timeout(5500)
        pg.evaluate("""()=>{document.querySelectorAll('body *').forEach(e=>{const tx=(e.innerText||'').trim(); if(e.children.length<=2 && /^Kepada Yth/i.test(tx) && tx.length<70) e.style.visibility='hidden'}); const l=document.querySelector('.u-lang,[class*=lang]'); if(l) l.style.visibility='hidden';}""")
        btn=pg.locator('#openBtn').bounding_box()
        pg.screenshot(path=f"hero-{t}-full.png"); pg.close()
        im=Image.open(f"hero-{t}-full.png"); bottom=min(2400,int((btn['y']+btn['height'])*2.5)+70); top=max(0,bottom-1350)
        im.crop((0,top,1080,top+1350)).save(f"hero-{t}.png"); print(t,top)
    b.close()
