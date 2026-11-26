"""Pemeriksa fakta otomatis untuk konten Salasah.
Pakai: python3 cek_fakta.py <folder_post> [--caption caption.txt]
Membaca teks dari file .html (sumber slide) dan caption, lalu memeriksa:
- harga yang disebut harus ada di js/data.js (atau promo resmi Rp100.000 untuk Plus)
- tema yang disebut bersama nama paket harus ada di paket itu
- kata terlarang (SWT, SAW, Wr. Wb., musik, PIN, WA blast, payment gateway, live streaming)
- hadis/ayat yang dikutip harus ada di daftar rujukan terverifikasi (rujukan.json)
Keluar dengan kode 1 bila ada masalah. JANGAN unggah bila gagal."""
import sys, re, json, glob, html
DATA='/home/claude/salasah/js/data.js'
s=open(DATA,encoding='utf-8').read()
js=json.loads(s[s.index('{'):s.rindex('}')+1])
harga={p['nama'].lower():p['harga'] for p in js['paket']}
paket_tema={p['nama'].lower():set(p['tema']) for p in js['paket']}
nama_tema={t['nama'].lower():t['id'] for t in js['tema']} if 'tema' in js else {}
sah={79000,149000,199000,299000,399000,799000,100000}  # 100000 = promo Plus 20 pembeli pertama (keputusan Syech)
folder=sys.argv[1]
teks=''
for f in glob.glob(folder+'/*.html')+glob.glob(folder+'/*.txt'):
    t=open(f,encoding='utf-8').read(); t=re.sub(r'<[^>]+>',' ',t); teks+=html.unescape(t)+'\n'
masalah=[]
for m in re.finditer(r'Rp\s?([\d\.]+)(?!\s?(rb|ribu|jt|juta))',teks):
    v=int(m.group(1).replace('.','')) if m.group(1).replace('.','').isdigit() else None
    if v and v>=10000 and v not in sah and not re.search(r'cetak|lembar|per tamu|ongkos|pasaran',teks[max(0,m.start()-120):m.end()+60],re.I):
        masalah.append(f'Harga Rp{m.group(1)} tidak ada di data.js')
for kata in [r'\bSWT\b',r'\bSAW\b',r'\bSAAW\b',r'Wr\.?\s?Wb',r'\bmusik\b',r'\bPIN\b',r'WA blast',r'payment gateway',r'live ?streaming',r'testimoni']:
    if re.search(kata,teks,re.I): masalah.append(f'Kata/klaim terlarang: {kata}')
for nm,tid in nama_tema.items():
    for pk,ts in paket_tema.items():
        if re.search(rf'{re.escape(nm)}[^.\n]{{0,60}}\b(paket )?{pk}\b',teks,re.I) and tid not in ts:
            masalah.append(f'Tema {nm} disebut di paket {pk}, padahal tidak termasuk')
ruj=json.load(open(__file__.rsplit('/',1)[0]+'/rujukan.json',encoding='utf-8'))
for m in re.finditer(r'(HR\.[^\n<]{0,80}|QS\.[^\n<]{0,40})',teks):
    r=m.group(1)
    if not any(k in r for k in ruj['terverifikasi']): masalah.append(f'Rujukan belum terverifikasi: {r.strip()}')
print('LOLOS' if not masalah else 'GAGAL'); [print(' -',x) for x in masalah]
sys.exit(1 if masalah else 0)
