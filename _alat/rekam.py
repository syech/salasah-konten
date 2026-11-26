import sys, base64, os, shutil, subprocess
from urllib.parse import quote
from playwright.sync_api import sync_playwright
tema, tamu, out = sys.argv[1], sys.argv[2], sys.argv[3]
scroll_px = int(sys.argv[4]) if len(sys.argv)>4 else 4200
d = "/tmp/frames"; shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
frames=[]
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome")
    ctx = b.new_context(viewport={"width":432,"height":768}, device_scale_factor=2.5, is_mobile=True, has_touch=True)
    pg = ctx.new_page()
    cdp = ctx.new_cdp_session(pg)
    def onframe(e):
        i=len(frames); fn=f"{d}/{i:05d}.jpg"
        open(fn,"wb").write(base64.b64decode(e["data"])); frames.append((fn,e["metadata"]["timestamp"]))
        cdp.send("Page.screencastFrameAck",{"sessionId":e["sessionId"]})
    cdp.on("Page.screencastFrame", onframe)
    pg.goto(f"http://localhost:8080/assets/themes/{tema}/?to={quote(tamu)}", wait_until="networkidle")
    cdp.send("Page.startScreencast",{"format":"jpeg","quality":92,"everyNthFrame":1})
    pg.wait_for_timeout(4200)
    pg.click("#openBtn"); pg.wait_for_timeout(2000)
    y=0
    while y < scroll_px:
        y+=6; pg.evaluate(f"window.scrollTo(0,{y})"); pg.wait_for_timeout(16)
    pg.wait_for_timeout(700)
    cdp.send("Page.stopScreencast"); b.close()
# concat file dengan durasi nyata
with open(f"{d}/list.txt","w") as f:
    for i,(fn,t) in enumerate(frames):
        dur = (frames[i+1][1]-t) if i+1<len(frames) else 0.04
        f.write(f"file '{fn}'\nduration {max(dur,0.001):.4f}\n")
    f.write(f"file '{frames[-1][0]}'\n")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i",f"{d}/list.txt","-vf","scale=1080:1920:flags=lanczos,fps=30","-c:v","libx264","-preset","veryfast","-crf","18","-pix_fmt","yuv420p",out],check=True)
print(len(frames),"frames")
