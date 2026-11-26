from playwright.sync_api import sync_playwright
from urllib.parse import quote
S=[("jawa-keraton","Bu Sari"),("tionghoa-classic","Kak Rina"),("oman","Bang Ucok"),("persian-garden","Tante Lia")]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx=b.new_context(viewport={"width":432,"height":768},device_scale_factor=2.5,is_mobile=True,has_touch=True)
    for t,n in S:
        pg=ctx.new_page(); pg.goto(f"http://localhost:8080/assets/themes/{t}/?to={quote(n)}",wait_until="networkidle"); pg.wait_for_timeout(5500)
        pg.screenshot(path=f"shot-{t}.png"); pg.close()
    b.close()
