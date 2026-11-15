"""Hebrew OCR with word-level re-OCR of suspicious words. Usage: python3 -I refine.py page.png out.txt [psm] [page.tsv]"""
import sys, subprocess, re, csv, io
from PIL import Image
import os; B=os.environ.get('TDB','/tmp/tdbest')
img, out = sys.argv[1], sys.argv[2]; psm = sys.argv[3] if len(sys.argv)>3 else '4'
def tess(path, lang, psm, fmt=None):
    a=['tesseract',path,'stdout','--tessdata-dir',B,'-l',lang,'--psm',str(psm)]+([fmt] if fmt else [])
    return subprocess.run(a,capture_output=True,text=True).stdout
def valid(words, d):
    if not words: return set()
    r=subprocess.run(['hunspell','-i','UTF-8','-d',d,'-G'],input='\n'.join(words),capture_output=True,text=True); return set(r.stdout.split())
src=open(sys.argv[4],encoding='utf-8').read() if len(sys.argv)>4 else tess(img,'heb+eng',psm,'tsv')
rows=list(csv.DictReader(io.StringIO(src),delimiter='\t',quoting=csv.QUOTE_NONE))
rows=[r for r in rows if r['level']=='5' and r['text'] and r['text'].strip()]
heb=re.compile(r'[א-ת]')
lines={}
for r in rows: lines.setdefault((r['block_num'],r['par_num'],r['line_num']),[]).append(r)
eng_ok=valid([re.sub(r'\W','',r['text']) for r in rows if re.fullmatch(r'[A-Za-z]+\W?',r['text'])],'en_US')
heb_ok=valid([re.sub(r'[^א-ת"]','',r['text']) for r in rows if heb.search(r['text'])],'he_IL')
im=Image.open(img); n=0; sus=[]
for k,ws in lines.items():
    hebline=sum(bool(heb.search(w['text'])) for w in ws)>=len(ws)/2
    for w in ws:
        t=w['text']; core=re.sub(r'\W','',t); conf=float(w['conf'])
        latin_junk = hebline and re.fullmatch(r'[A-Za-z]{1,6}',core or '') and core not in eng_ok and not re.fullmatch(r'[A-Z]{2,5}',core or 'x') or (hebline and core.isupper() and core not in ('HCM',))
        heb_bad = heb.search(t) and re.sub(r'[^א-ת"]','',t) not in heb_ok and conf<85
        if latin_junk or heb_bad: sus.append(w)
if sus:
    crops=[]
    for w in sus:
        x,y,ww,hh=(int(w[c]) for c in ('left','top','width','height')); pad=4
        c=im.crop((max(0,x-pad),max(0,y-pad),x+ww+pad,y+hh+pad)); crops.append(c.resize((c.width*2,c.height*2)))
    gap=40; W=max(c.width for c in crops)+2*gap; H=sum(c.height+gap for c in crops)+gap
    sheet=Image.new('L',(W,H),255); ys=[]; y=gap
    for c in crops: sheet.paste(c.convert('L'),(W-gap-c.width,y)); ys.append((y,y+c.height)); y+=c.height+gap
    sheet.save('/tmp/sheet.png')
    r2=list(csv.DictReader(io.StringIO(tess('/tmp/sheet.png','heb',6,'tsv')),delimiter='\t',quoting=csv.QUOTE_NONE))
    alts=[[] for _ in sus]
    for r in r2:
        if r.get('level')!='5' or not (r.get('text') or '').strip(): continue
        cy=int(r['top'])+int(r['height'])//2
        for i,(a,b) in enumerate(ys):
            if a-gap//2<=cy<=b+gap//2: alts[i].append((int(r['left']),r['text'])); break
    alts=[' '.join(t for _,t in sorted(a,reverse=True)) for a in alts]
    ok=valid([re.sub(r'[^א-ת"]','',a) for a in alts if a],'he_IL')
    for w,a in zip(sus,alts):
        if a and ' ' not in a and re.sub(r'[^א-ת"]','',a) in ok: w['text']=a; n+=1
txt='\n'.join(' '.join(w['text'] for w in ws) for ws in lines.values())
open(out,'w',encoding='utf-8').write(txt); print(f'refined={n}',file=sys.stderr)

