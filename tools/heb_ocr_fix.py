"""Fix common Hebrew OCR slips with hunspell he_IL + document self-learning.
Usage: python3 -I heb_ocr_fix.py in.txt out.txt [extra_words.txt]"""
import re, sys, subprocess, collections
SWAP = {'ס':'ם','ם':'ס','ז':'ו','ו':'ז','ה':'ח','ח':'ה','ד':'ר','ר':'ד','ב':'כ','כ':'ב','ן':'ו','ט':'מ','ע':'צ','צ':'ע'}
FIN = {'כ':'ך','מ':'ם','נ':'ן','פ':'ף','צ':'ץ'}; UNFIN = {v:k for k,v in FIN.items()}
KEEP = set('ולהיפך להיפך לעיתים'.split())
ACR = set('ק"מ קמ"ש מ"ר מ"ק ס"מ מ"מ ק"ג בארה"ב וכו\' ע"י עפ"י לפ"מ רח"ק ת"א נת"צ'.split())
def good(words):
    if not words: return set()
    r = subprocess.run(['hunspell','-i','UTF-8','-d','he_IL','-G'], input='\n'.join(words), capture_output=True, text=True)
    return set(r.stdout.split()) | (set(words) & ACR)
def norm(w):
    w = ''.join(UNFIN.get(c,c) for c in w[:-1]) + w[-1]
    return w[:-1] + FIN.get(w[-1], w[-1])
def cands(w):
    out = [w[:-1]+'ם'] if w.endswith('ס') else []
    if w.endswith('ו') and len(w) >= 3: out.append(w[:-1]+'ן')   # final nun read as vav
    for m in re.finditer('יי', w):
        a = w[:m.start()]+'"'+w[m.end():]; out += [a, a[:-1]+UNFIN.get(a[-1],a[-1])]   # gershayim read as yy; acronyms end non-final
    if len(w) < 4: return list(dict.fromkeys(out))   # short words: too ambiguous for letter swaps
    for i,c in enumerate(w):
        if c in SWAP: out.append(norm(w[:i]+SWAP[c]+w[i+1:]))
    return list(dict.fromkeys(out))
t = open(sys.argv[1], encoding='utf-8').read().replace('עלפי', 'על פי')
cnt = collections.Counter(re.findall(r'[א-ת]{2,}', t))
extra = set(open(sys.argv[3], encoding='utf-8').read().split()) if len(sys.argv) > 3 else set()
ok = good(sorted(cnt)) | extra | KEEP
bad = [w for w in cnt if w not in ok]
allc = {w: cands(w) for w in bad}
okc = good(sorted({c for cs in allc.values() for c in cs}))
fix = {}
for w, cs in allc.items():
    safe = {w[:-1]+'ם', w[:-1]+'ן'} | {c for c in cs if '"' in c}   # high-precision rules: dictionary is enough
    hits = [c for c in cs if (c in safe and (c in okc or cnt.get(c, 0) >= 2)) or (c not in safe and cnt.get(c, 0) >= max(2, 3 * cnt[w]) and (c in okc or cnt.get(c, 0) >= 3))]
    if not hits: continue
    # a frequent unknown word is probably a real domain term: only fix it if the candidate is far more common
    if cnt[w] >= 3 and cnt.get(hits[0], 0) < 5 * cnt[w] and hits[0] not in ACR and '"' not in hits[0]: continue
    if len(hits) == 1 or hits[0] in safe: fix[w] = hits[0]
out = re.sub(r'[א-ת]{2,}', lambda m: fix.get(m.group(), m.group()), t)
open(sys.argv[2], 'w', encoding='utf-8').write(out)
print(f'words={len(cnt)} unknown={len(bad)} fixed={len(fix)}', file=sys.stderr)
for a, b in sorted(fix.items(), key=lambda x: -cnt[x[0]]): print(f'  {a} -> {b}  x{cnt[a]}', file=sys.stderr)

