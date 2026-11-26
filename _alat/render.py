import sys
from playwright.sync_api import sync_playwright
src,prefix,n=sys.argv[1],sys.argv[2],int(sys.argv[3])
with sync_playwright() as p:
    b=p.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.goto(f"file:///home/claude/feed/{src}"); pg.wait_for_timeout(800)
    for i in range(1,n+1):
        pg.locator(f"#s{i}").screenshot(path=f"/home/claude/feed/{prefix}-{i}.png")
    b.close()
