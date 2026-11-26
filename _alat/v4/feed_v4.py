import json, html as H
from playwright.sync_api import sync_playwright
# id, waktu, pola, data
F=[
("26-intro","2026-11-26T20:53","lama",{"img":"/home/claude/feed/salasah-01-1.png"}),
("27a","2026-11-27T12:00","big",{"v":"n","t":"Tamumu punya nama.","s":"Bukan \"Bapak/Ibu/Saudara/i\". Undangan Salasah menyapa setiap tamu dengan namanya sendiri."}),
("27b","2026-11-27T19:30","big",{"v":"c","t":"Undangan 300 tamu, habis berapa?","s":"Kami hitung harga aslinya: cetak dibanding digital."}),
("28a","2026-11-28T19:30","hero",{"tema":"melayu-deli","label":"Tema Melayu Deli","band":"Kondangan lagi? November memang bulan nikah."}),
("29a","2026-11-29T19:30","edu",{"seri":"Adab & Doa","t":"Diundang nikah, tapi malas datang?","orn":"orn-oman-i-rosette.webp","v":"n"}),
("30a","2026-11-30T12:00","hero",{"tema":"melayu-deli","label":"Tema Melayu Deli","band":"Orang Medan kenal undangan ini dari payungnya."}),
("30b","2026-11-30T19:30","big",{"v":"c","t":"300 terkirim. 40 dibuka.","s":"Sisanya ke mana? Ini cara tahu siapa yang belum membuka undanganmu."}),
("01a","2026-12-01T19:30","edu",{"seri":"Salasah Edu","t":"Cara mengundang atasan lewat WA tanpa canggung.","orn":"orn-melayu-deli-i-tepak.webp","v":"w"}),
("02a","2026-12-02T12:00","hero",{"tema":"seoul-pastel","label":"Kuis 10 detik","band":"Pilih satu tema. Kami tebak gaya nikahmu."}),
("03a","2026-12-03T19:30","edu",{"seri":"Salasah Edu","t":"Rp79 ribu atau Rp149 ribu? Ini bedanya.","orn":"orn-persian-garden-i-mawar.webp","v":"w"}),
("04a","2026-12-04T12:00","edu",{"seri":"Adab & Doa","t":"Diundang itu hak yang perlu dipenuhi.","orn":"orn-jawa-keraton-i-kawung.webp","v":"n"}),
("04b","2026-12-04T19:30","hero",{"tema":"antique-rose","label":"Promo perkenalan","band":"Paket Plus Rp100.000 untuk 20 pembeli pertama."}),
("05a","2026-12-05T19:30","big",{"v":"n","t":"Ngaku: kamu buka undangan cuma cari parkir.","s":""}),
("06a","2026-12-06T19:30","edu",{"seri":"Adab & Doa","t":"Ayat yang paling sering ada di undangan, dan artinya.","orn":"orn-melayu-deli-i-melati.webp","v":"n"}),
("07a","2026-12-07T12:00","hero",{"tema":"batak","label":"Tema Batak","band":"Horas! Undangan pakai ulos, bukan template polos."}),
("07b","2026-12-07T19:30","edu",{"seri":"Salasah Edu","t":"Sebelum pesan undangan, siapkan 6 hal ini.","orn":"orn-oman-i-dallah.webp","v":"w"}),
("08a","2026-12-08T19:30","banding",{"t":"Mama mau cetak, kamu mau digital.","l":"Cetak","r":"Digital","s":"Dua-duanya bisa menang."}),
("09a","2026-12-09T12:00","hero",{"tema":"green-jasmine","label":"Tema Green Jasmine","band":"Cara menerima amplop tanpa terdengar meminta."}),
("10a","2026-12-10T19:30","big",{"v":"c","t":"500 tamu. Rp149 ribu. Per orangnya?","s":"Hitungan jujur biaya undangan per tamu."}),
("11a","2026-12-11T12:00","edu",{"seri":"Cerita Salasah","t":"Salasah artinya tiga. Ini ceritanya.","orn":"orn-tionghoa-classic-i-teratai.webp","v":"w"}),
("11b","2026-12-11T19:30","hero",{"tema":"persian-garden","label":"Promo perkenalan","band":"Plus Rp100.000 masih ada. Ini isinya."}),
("12a","2026-12-12T19:30","edu",{"seri":"Salasah Edu","t":"\"Parkirnya di mana?\" Jawab sebelum tamu bertanya.","orn":"orn-persian-garden-i-sulur.webp","v":"w"}),
("13a","2026-12-13T19:30","edu",{"seri":"Adab & Doa","t":"Kamu menikahinya karena apa? Rasulullah menjawabnya.","orn":"orn-oman-i-rosette.webp","v":"n"}),
("14a","2026-12-14T12:00","hero",{"tema":"jawa-keraton","label":"Tema Jawa Keraton","band":"Jawa, Sunda, atau Betawi? Pilih yang mirip rumah nenekmu."}),
("14b","2026-12-14T19:30","big",{"v":"n","t":"Dilempar ke grup, tamu merasa diundang setengah hati.","s":""}),
("15a","2026-12-15T19:30","edu",{"seri":"Salasah Edu","t":"Selain \"selamat ya\", ini 8 ucapan yang bikin pengantin terharu.","orn":"orn-melayu-deli-i-melati.webp","v":"w"}),
("16a","2026-12-16T12:00","hero",{"tema":"love-in-paris","label":"Tema Love in Paris","band":"Tidak pakai adat? Tiga tema ini untuk yang suka simpel."}),
("17a","2026-12-17T19:30","edu",{"seri":"Salasah Edu","t":"Dari chat pertama sampai link siap dibagikan.","orn":"orn-jawa-keraton-i-kawung.webp","v":"w"}),
("18a","2026-12-18T12:00","edu",{"seri":"Adab & Doa","t":"Walimah tidak harus mewah. Ini dalilnya.","orn":"orn-jawa-keraton-i-gunungan.webp","v":"n"}),
("18b","2026-12-18T19:30","hero",{"tema":"tuscan","label":"Promo perkenalan","band":"Satu link untuk semua tamu. Rp100.000 untuk 20 orang pertama."}),
("19a","2026-12-19T19:30","big",{"v":"n","t":"Nikah 2027? Mulai dari sini, sekarang.","s":"Timeline 12 bulan, simpan dulu."}),
("20a","2026-12-20T19:30","edu",{"seri":"Adab & Doa","t":"Ayat untuk yang ragu menikah karena belum mapan.","orn":"orn-persian-garden-i-mawar.webp","v":"n"}),
]
css='''@font-face{font-family:CG;font-weight:600;src:url(fonts/cormorant-garamond-latin-600-normal.woff2)}
@font-face{font-family:PJ;font-weight:400;src:url(fonts/plus-jakarta-sans-latin-400-normal.woff2)}
@font-face{font-family:PJ;font-weight:600;src:url(fonts/plus-jakarta-sans-latin-600-normal.woff2)}
:root{--w:#F6F4EF;--c:#E9DCC4;--n:#1E2F5C;--g:#A8823F;--gl:#D8B15E;--mu:#5B6478}
*{margin:0;padding:0;box-sizing:border-box}.s{width:1080px;height:1350px;position:relative;overflow:hidden;font-family:PJ;color:var(--n)}
.h{font-family:CG;font-weight:600;letter-spacing:-.015em;line-height:1}.wm{font-family:CG;font-weight:600;font-size:38px}.wm b{color:var(--g)}
.pill{position:absolute;left:44px;top:40px;background:rgba(246,244,239,.95);border-radius:999px;padding:12px 26px;font-size:24px;font-weight:600;display:flex;gap:16px;align-items:baseline}
.band{position:absolute;left:0;right:0;bottom:0;background:var(--n);color:#F6F4EF;padding:44px 60px 52px}'''
def cell(i,p,d):
    if p=='hero':
        return f'<div class="s" id="c{i}"><img src="hero-{d["tema"]}.png" style="position:absolute;inset:0;width:1080px;height:1350px"><div class="pill"><span class="wm" style="font-size:28px">Salasah<b>.</b></span><span>{H.escape(d["label"])}</span></div><div class="band"><div class="h" style="font-size:72px">{H.escape(d["band"])}</div></div></div>'
    if p=='big':
        bg,fg,sub=('var(--n)','#F6F4EF','#C9CFDD') if d['v']=='n' else ('var(--c)','var(--n)','var(--mu)')
        n=len(d['t']); fs=210 if n<22 else 170 if n<34 else 140
        return f'<div class="s" id="c{i}" style="background:{bg}"><div class="h" style="position:absolute;left:60px;top:130px;width:980px;font-size:{fs}px;line-height:.92;color:{fg}">{H.escape(d["t"])}</div><p style="position:absolute;left:64px;bottom:120px;width:720px;font-size:32px;line-height:1.45;color:{sub}">{H.escape(d["s"])}</p><div class="wm" style="position:absolute;right:60px;bottom:56px;color:{fg}">Salasah<b style="color:var(--gl)">.</b></div></div>'
    if p=='edu':
        nav=d['v']=='n'; body='var(--n)' if nav else 'var(--w)'; fg='#F6F4EF' if nav else 'var(--n)'; top='var(--c)' if nav else 'var(--n)'; topfg='var(--n)' if nav else '#F6F4EF'
        return f'<div class="s" id="c{i}" style="background:{body}"><div style="position:absolute;left:0;right:0;top:0;height:96px;background:{top};color:{topfg};display:flex;align-items:center;justify-content:space-between;padding:0 56px"><span class="wm" style="font-size:36px">Salasah<b>.</b></span><span style="font-size:24px;font-weight:600">{H.escape(d["seri"])}</span></div><div class="h" style="position:absolute;left:70px;top:190px;width:900px;font-size:104px;color:{fg}">{H.escape(d["t"])}</div><img src="{d["orn"]}" style="position:absolute;right:-40px;bottom:30px;width:430px"><div style="position:absolute;left:70px;bottom:70px;font-size:24px;font-weight:600;color:{fg};opacity:.8">Geser untuk membaca</div></div>'
    if p=='banding':
        return f'<div class="s" id="c{i}"><div style="position:absolute;left:0;top:0;width:540px;height:1350px;background:var(--c)"></div><div style="position:absolute;left:540px;top:0;width:540px;height:1350px;background:var(--n)"></div><div class="h" style="position:absolute;left:60px;top:120px;width:960px;font-size:120px;color:var(--n);mix-blend-mode:normal"><span>{H.escape(d["t"])}</span></div><div class="h" style="position:absolute;left:60px;bottom:110px;font-size:96px;color:var(--n)">{d["l"]}</div><div class="h" style="position:absolute;left:600px;bottom:110px;font-size:96px;color:#F6F4EF">{d["r"]}</div><div style="position:absolute;left:600px;bottom:60px;font-size:26px;color:#C9CFDD">{H.escape(d["s"])}</div></div>'
    return ''
out='<html><head><meta charset="utf-8"><style>'+css+'</style></head><body>'+''.join(cell(i,p,d) for i,(k,w,p,d) in enumerate(F) if p!='lama')+'</body></html>'
open('feed_v4.html','w').write(out)
with sync_playwright() as pw:
    b=pw.chromium.launch(executable_path="/usr/bin/google-chrome"); pg=b.new_page(viewport={"width":1080,"height":1350})
    pg.goto("file:///home/claude/pola/feed_v4.html"); pg.wait_for_timeout(1200)
    for i,(k,w,p,d) in enumerate(F):
        if p!='lama': pg.locator(f'#c{i}').screenshot(path=f'v4-{k}.png')
    b.close()
json.dump([(k,w,p) for k,w,p,d in F],open('feed_v4.json','w'))
print('ok')
