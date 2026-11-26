import json, sys
from playwright.sync_api import sync_playwright
plan=json.load(open('/home/claude/salasah-konten/rencana/rencana-3-pekan.json'))
# warna selang-seling kronologis: post terbit sebelumnya = intro L, harga L, nov N, adab L; 27a disisipkan N
seq=['L']  # intro
order=sorted(plan,key=lambda p:p['waktu'])
# susun kronologi penuh
existing={'2026-11-27T19:30':'harga','2026-11-28T19:30':'nov','2026-11-29T19:30':'adab'}
allp=[(p['waktu'],p) for p in plan]+[(k,{'id':v,'existing':True}) for k,v in existing.items()]
allp.sort(key=lambda x:x[0])
c='N'
for w,p in allp:
    p['warna']=c; c='L' if c=='N' else 'N'
json.dump(plan,open('/home/claude/salasah-konten/rencana/rencana-3-pekan.json','w'),ensure_ascii=False,indent=1)
def phones(t,dk):
    bg='#0B1226' if dk else '#10131C'
    if not t: return ''
    if len(t)==1:
        return f'<div class="phone" style="width:330px;left:375px;top:760px"><img src="tema/{t[0]}.webp"></div>'
    if len(t)==3:
        return ''.join([f'<div class="phone" style="width:280px;left:{x}px;top:{y}px;transform:rotate({r}deg)"><img src="tema/{n}.webp"></div>' for n,(x,y,r) in zip(t,[(110,830,-7),(400,780,0),(690,830,7)])])
    if len(t)==4:
        return ''.join([f'<div class="phone" style="width:210px;left:{x}px;top:{y}px"><img src="tema/{n}.webp"></div>' for n,(x,y) in zip(t,[(88,760),(328,820),(568,760),(808,820)])])
    return ''
html=['<html><head><meta charset="utf-8"><link rel="stylesheet" href="base.css"><style>.dots{display:flex;gap:14px}.dots i{width:16px;height:16px;border-radius:50%;background:var(--goldb);display:block}.frame{position:absolute;inset:40px;border:2px solid var(--line);border-radius:30px}.dk .frame{border-color:rgba(255,255,255,.12)}</style></head><body>']
for p in plan:
    dk=p['warna']=='N'
    t=p['tema']
    body=f'<div class="wrap"><div class="eyebrow">{p["ey"]}</div><h1 style="font-size:{104 if t else 118}px">{p["judul"]}</h1></div>'
    if not t:
        body=f'<div class="frame"></div><div class="wrap" style="top:auto;bottom:250px"><div class="dots" style="margin-bottom:56px"><i></i><i></i><i></i></div><div class="eyebrow">{p["ey"]}</div><h1 style="font-size:122px">{p["judul"]}</h1></div><div class="foot"><span>Geser</span><span>&rarr;</span></div>'
    html.append(f'<div class="s{" dk" if dk else ""}" id="c{p["id"]}"><div class="logo">Salasah<i></i></div><div class="num">01 / 05</div>{body}{phones(t,dk)}</div>')
html.append('</body></html>')
open('covers.html','w').write('\n'.join(html))
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/google-chrome")
    pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file:///home/claude/feed/covers.html"); pg.wait_for_timeout(1200)
    for p in plan: pg.locator(f'#c{p["id"]}').screenshot(path=f'/home/claude/feed/cover-{p["id"]}.png')
    b.close()
print('ok')
