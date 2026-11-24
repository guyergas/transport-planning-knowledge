"""Process request files: check access, store PDFs in Releases, extract/OCR Hebrew text.

Request line: URL [pages=1-8,20] [ocr=auto|none]
  pages: limit text extraction to these PDF pages (default: all pages)
Outputs:
  results/<req>.jsonl          one access-check record per URL
  docs/<docid>/meta.json       document metadata (+ release asset URL)
  docs/<docid>/text.md         text with '=== PAGE N ===' markers and per-page method
  index.jsonl                  one line per document (rebuilt)
"""
import collections
import hashlib, html, json, os, random, re, shutil, subprocess, sys, tempfile, time, glob, urllib.parse
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, 'tools')
TDB = os.environ.get('TDB', '/tmp/tdbest')
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36'
REPO = os.environ.get('GITHUB_REPOSITORY', '')


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def docid(url):
    return hashlib.sha1(url.encode()).hexdigest()[:12]


def parse_pages(spec, n):
    if not spec:
        return list(range(1, n + 1))
    if spec == 'toc':  # index-only: front matter + last pages
        return sorted(set(range(1, min(n, 15) + 1)) | set(range(max(1, n - 2), n + 1)))
    out = []
    for part in spec.split(','):
        a, _, b = part.partition('-')
        out += range(int(a), int(b or a) + 1)
    return [p for p in out if 1 <= p <= n]


def fetch(url, dest):
    hdr = dest + '.hdr'
    r = sh(['curl', '-sS', '-L', '--max-redirs', '10', '-m', '600', '--retry', '2', '-A', UA,
            '-H', 'Accept-Language: he-IL,he;q=0.9,en;q=0.8', '-D', hdr, '-o', dest,
            '-w', '%{http_code}\t%{url_effective}\t%{content_type}\t%{num_redirects}\t%{size_download}\t%{time_total}', url])
    rec = {'url': url, 'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
    if r.returncode and not r.stdout:
        rec.update(status=0, error=r.stderr.strip()[-300:])
        return rec
    code, final, ctype, nred, size, t = r.stdout.split('\t')
    rec.update(status=int(code), final_url=final, content_type=ctype, redirects=int(nred), bytes=int(float(size)), secs=float(t))
    if r.returncode:
        rec['error'] = r.stderr.strip()[-300:]
        if rec['status'] < 400:  # transfer cut off mid-file (e.g. curl 18/56): treat as transient, never as a good file
            rec['http_status'], rec['status'] = rec['status'], 0
    if rec['status'] >= 400 and os.path.exists(dest):
        rec['body_head'] = re.sub(r'\s+', ' ', open(dest, 'rb').read(3000).decode('utf-8', 'replace'))[:400]
    try:
        h = open(hdr, encoding='latin-1').read().lower()
        rec['server'] = (re.findall(r'^server:\s*(.+)$', h, re.M) or [''])[-1].strip()
    except OSError:
        pass
    return rec


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0; self.title = ''; self._t = False; self.links = []; self._a = None
    def handle_starttag(self, tag, a):
        if tag == 'a' and dict(a).get('href'): self._a = [dict(a)['href'], '']
        if tag in ('script', 'style', 'noscript'): self.skip += 1
        if tag == 'title': self._t = True
        if tag in ('p', 'br', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'tr'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'): self.skip = max(0, self.skip - 1)
        if tag == 'title': self._t = False
        if tag == 'a' and self._a: self.links.append(self._a); self._a = None
    def handle_data(self, d):
        if self._a is not None: self._a[1] += d
        if self._t: self.title += d
        if not self.skip: self.out.append(d)


LAST_HIT = {}
PACE = {'www.gov.il': 6, 'gov.il': 6}  # min seconds between requests to one host from one runner


def browser_fetch(url, dest):
    """Fallback for bot-protected sites: real headless Chromium (Playwright)."""
    r = sh(['python3', os.path.join(TOOLS, 'browser_fetch.py'), url, dest], timeout=300)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {'status': 0, 'error': (r.stderr or r.stdout)[-300:]}


def wayback_fetch(url, dest):
    """Last resort: newest Internet Archive snapshot (raw bytes via id_). Marked as an archive copy."""
    r = sh(['curl', '-sS', '-m', '60', 'https://archive.org/wayback/available?url=' + urllib.parse.quote(url, safe='')])
    try:
        snap = json.loads(r.stdout)['archived_snapshots']['closest']
    except Exception:
        return {'status': 0, 'error': 'no snapshot'}
    if not snap.get('available'):
        return {'status': 0, 'error': 'no snapshot'}
    raw = re.sub(r'/web/(\d+)/', r'/web/\1id_/', snap['url'])
    rec = fetch(raw, dest)
    rec.update(archive_snapshot=snap['timestamp'], archive_url=snap['url'])
    return rec


def classify(rec, path):
    """Accessible / error / redirect / login-required, plus kind."""
    head = open(path, 'rb').read(2048) if os.path.exists(path) else b''
    rec['kind'] = 'pdf' if head.startswith(b'%PDF') else 'zip' if head.startswith(b'PK') else 'html' if b'<' in head[:200] else 'other'
    if rec['kind'] == 'zip':
        try:
            import zipfile
            if 'xl/workbook.xml' in zipfile.ZipFile(path).namelist():
                rec['kind'] = 'xlsx'
        except Exception:
            pass
    s = rec.get('status', 0)
    final = rec.get('final_url', '')
    moved = final and urllib.parse.urlsplit(final).path != urllib.parse.urlsplit(rec['url']).path
    if s in (401, 407) or (moved and re.search(r'/(login|signin|sign-in|logon|sso|oauth2?|account/login)\b', final, re.I)):
        rec['result'] = 'login'
    elif s >= 400 or s == 0:
        rec['result'] = f'error {s}'
    elif rec.get('redirects') and urllib.parse.urlsplit(final)._replace(fragment='') != urllib.parse.urlsplit(rec['url'])._replace(fragment=''):
        rec['result'] = 'redirect'
    else:
        rec['result'] = 'ok'
    if rec['kind'] == 'html' and s == 200:
        t = open(path, encoding='utf-8', errors='replace').read()
        if len(t) < 60000 and re.search(r'cf-chl|challenge-platform|Request unsuccessful|Incapsula incident|<title>(Access Denied|Just a moment)', t, re.I):
            rec['result'] = 'blocked (bot challenge)'
        p = Text(); p.feed(t)
        rec['title'] = re.sub(r'\s+', ' ', p.title).strip()[:200]
        base = rec.get('final_url') or rec['url']
        seen, links = set(), []
        for h, txt in p.links:
            u = urllib.parse.urljoin(base, h.strip())
            if u.startswith('http') and u not in seen and (re.search(r'לצפי[יה]|להורדה|לחצו כאן|הורדה|download', txt, re.I) and '#' not in u or re.search(r'\.(pdf|zip|docx?|xlsx?|kmz|shp)(\?|#|$)|BlobFolder|/download|/media/|/uploads/|/documents/\d+/view', u, re.I)):
                seen.add(u); links.append({'url': u, 'text': re.sub(r'\s+', ' ', txt).strip()[:150]})
        rec['file_links'] = links
        rec['all_links'] = len(p.links)
        return re.sub(r'\n\s*\n+', '\n\n', ''.join(p.out)).strip()
    return None


def check_layer(txt):
    words = re.findall(r'[א-ת]{2,}', txt)
    fin = 'ךםןףץ'
    start = sum(w[0] in fin for w in words); end = sum(w[-1] in fin for w in words)
    bad = len(re.findall(r'[�\u0080-\u009f]', txt)); heb = sum(len(w) for w in words)
    junk = len(re.findall(r'[\$\+]{2,}|[ÀÁÂÃÄÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖØÙÚÛÜÝÞßàáâãäåæçèéêëìíîïðñòóôõöøùúûüýþ]', txt))
    if len(txt.strip()) < 30:
        return 'empty'
    if len(words) >= 30 and end / len(words) < 0.05:
        return 'garbled'  # final letters dropped (broken font map)
    if (start > end and start >= 3) or bad > 20 or junk > 15 or (heb < 50 and len(txt.strip()) > 200 and not re.search(r'[A-Za-z]{4,}\s+[A-Za-z]{4,}', txt)):
        return 'garbled'
    return 'ok'


def fix_bidi(t):
    """Repair visual-order artifacts in Hebrew text layers: '.word' -> '. word', ')abc(' -> '(abc)', '80שניות' -> '80 שניות'."""
    out = []
    for l in t.splitlines():
        if re.search(r'[א-ת]', l):
            m = re.match(r'^(\s*)([.,;:])(?=[א-ת"])', l)
            if m and out:
                out[-1] = out[-1].rstrip() + m.group(2)
                l = m.group(1) + l[m.end():]
            l = re.sub(r'\s([.,;:!?])(?=[א-ת"(])', r'\1 ', l)
            l = re.sub(r'\)([א-ת"\'׳״/\- ]{1,60})\(', r'(\1)', l)
            l = re.sub(r'(\d)([א-ת][א-ת"]{2,})', r'\1 \2', l)
        out.append(l)
    return '\n'.join(out)


def ocr_pages(pdf, pages, work):
    os.makedirs(work, exist_ok=True)
    jobs = os.path.join(work, 'jobs.sh')
    with open(jobs, 'w') as f:
        for p in pages:
            b = os.path.join(work, f'p{p}')
            f.write(f'[ -s {b}.txt ] || (pdftoppm -r 150 -gray -png -f {p} -l {p} -singlefile "{pdf}" {b} && '
                    f'OMP_THREAD_LIMIT=1 tesseract {b}.png {b} --tessdata-dir {TDB} -l heb+eng --psm 4 --dpi 150 tsv 2>/dev/null && '
                    f'TDB={TDB} python3 -I {TOOLS}/refine.py {b}.png {b}.txt 4 {b}.tsv 2>/dev/null; rm -f {b}.png)\n')
    subprocess.run(f'xargs -P {os.cpu_count() or 2} -I CMD sh -c CMD < {jobs}', shell=True)
    return {p: open(os.path.join(work, f'p{p}.txt'), encoding='utf-8').read() if os.path.exists(os.path.join(work, f'p{p}.txt')) else '' for p in pages}


def ocr_conf(work, p):
    """Mean tesseract word confidence (0-100) for an OCR page, from its TSV; None if missing."""
    f = os.path.join(work, f'p{p}.tsv')
    if not os.path.exists(f):
        return None
    c = [float(r[10]) for r in (l.split('\t') for l in open(f, encoding='utf-8').read().splitlines()[1:])
         if len(r) > 11 and r[0] == '5' and r[11].strip() and float(r[10]) >= 0]
    return round(sum(c) / len(c)) if c else None


def ocr_extra(pdf, pages, work, psm, tag):
    """Plain OCR pass (no refine) for figure labels (psm 11 sparse) or tables (psm 6 block)."""
    if not pages:
        return {}
    jobs = os.path.join(work, f'jobs_{tag}.sh')
    with open(jobs, 'w') as f:
        for p in pages:
            b = os.path.join(work, f'{tag}{p}')
            f.write(f'pdftoppm -r 150 -gray -png -f {p} -l {p} -singlefile "{pdf}" {b} && '
                    f'OMP_THREAD_LIMIT=1 tesseract {b}.png {b} --tessdata-dir {TDB} -l heb+eng --psm {psm} --dpi 150 2>/dev/null; rm -f {b}.png\n')
    subprocess.run(f'xargs -P {os.cpu_count() or 2} -I CMD sh -c CMD < {jobs}', shell=True)
    out = {}
    for p in pages:
        f = os.path.join(work, f'{tag}{p}.txt')
        out[p] = open(f, encoding='utf-8').read() if os.path.exists(f) else ''
    return out


def image_pages(path):
    """PDF pages holding a real picture (>=200x150 px raster, not a mask)."""
    pg = set()
    for l in sh(['pdfimages', '-list', path]).stdout.splitlines()[2:]:
        c = l.split()
        if len(c) > 4 and c[2] == 'image' and c[3].isdigit() and int(c[3]) >= 200 and int(c[4]) >= 150:
            pg.add(int(c[0]))
    return pg


def table_like(t):
    """Many lines with 3+ number cells, or ruled/aligned columns -> treat as table page."""
    rows = [l for l in t.splitlines() if len(re.findall(r'(?<![\w.])\d[\d.,/%-]*(?![\w.])', l)) >= 3]
    gaps = [l for l in t.splitlines() if len(re.findall(r'\S\s{3,}\S', l)) >= 3]
    return len(rows) >= 4 or len(gaps) >= 6


def new_words(extra, base):
    """Keep only OCR lines that add real words missing from the page text (figure labels).
    A line survives if it has a dictionary word (hunspell he_IL / en_US, >=3 letters) not already in the page text."""
    have = set(re.findall(r'[\w"]{2,}', base))
    cand = [l.strip() for l in extra.splitlines() if re.search(r'[א-תA-Za-z]{3}', l)]
    words = sorted({w for l in cand for w in re.findall(r'[א-ת"]{3,}|[A-Za-z]{3,}', l) if w not in have})
    ok = set()
    for d, rx in (('he_IL', r'[א-ת]'), ('en_US', r'[A-Za-z]')):
        ws = [w for w in words if re.match(rx, w)]
        if ws:
            r = sh(['hunspell', '-i', 'UTF-8', '-d', d, '-G'], input='\n'.join(ws))
            ok |= set(r.stdout.split())
    keep = [l for l in cand if any(w in ok for w in re.findall(r'[א-ת"]{3,}|[A-Za-z]{3,}', l))]
    return '\n'.join(keep)


def ensure_release(tag):
    if sh(['gh', 'release', 'view', tag, '-R', REPO]).returncode:
        sh(['gh', 'release', 'create', tag, '-R', REPO, '-t', tag, '-n', 'Original source files (see index.jsonl)'])


def unchanged(path, did):
    """Same bytes as last time and text already built -> no need to re-OCR."""
    mf = os.path.join(ROOT, 'docs', did, 'meta.json')
    if not (os.path.exists(mf) and os.path.exists(os.path.join(ROOT, 'docs', did, 'text.md'))):
        return None
    old = json.load(open(mf))
    new = hashlib.sha256(open(path, 'rb').read()).hexdigest()
    return old if old.get('sha256') == new else None


def upload_asset(rec, path, did, ext):
    """Original file -> Release src-<host> as <docid>.<ext>."""
    host = re.sub(r'[^a-z0-9]+', '-', urllib.parse.urlsplit(rec['url']).netloc.lower()).strip('-') or 'inbox'
    tag = f'src-{host}'
    ensure_release(tag)
    named = os.path.join(os.path.dirname(path), f'{did}.{ext}')
    if not os.path.exists(named):
        os.link(path, named)
    up = sh(['gh', 'release', 'upload', tag, named, '--clobber', '-R', REPO])
    if up.returncode:
        rec['release_error'] = up.stderr.strip()[-200:]
    else:
        rec['asset'] = f'https://github.com/{REPO}/releases/download/{tag}/{did}.{ext}'


def process_xlsx(rec, path, did):
    """Excel workbook -> one page per sheet, rows as ' | '-joined cells (text only; no OCR needed)."""
    import openpyxl
    wb = openpyxl.load_workbook(open(path, 'rb'), read_only=True, data_only=True)  # file object: temp path has no .xlsx extension
    pages = []
    for i, ws in enumerate(wb.worksheets, 1):
        lines = []
        for row in ws.iter_rows(values_only=True):
            cells = [re.sub(r'\s+', ' ', str(c)).strip() for c in row if c is not None and str(c).strip()]
            if cells:
                lines.append(' | '.join(cells))
        pages.append(f'=== PAGE {i} === [text-layer; sheet={ws.title}]\n' + '\n'.join(lines) + '\n')
    rec.update(pages=len(pages), sheets=[ws.title for ws in wb.worksheets], text_pages=len(pages), ocr_pages=0, layer='ok',
               sha256=hashlib.sha256(open(path, 'rb').read()).hexdigest())
    upload_asset(rec, path, did, 'xlsx')
    return '\n'.join(pages)


def process_pdf(rec, path, pages_spec, did):
    info = sh(['pdfinfo', path]).stdout
    n = int((re.findall(r'^Pages:\s+(\d+)', info, re.M) or ['0'])[0])
    meta = {k: (re.findall(rf'^{k}:\s+(.+)$', info, re.M) or [''])[0].strip() for k in ('Title', 'Producer', 'Creator', 'CreationDate', 'ModDate')}
    fonts = sh(['pdffonts', path]).stdout
    uni_no = sum(1 for l in fonts.splitlines()[2:] if re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', l) and l.split()[-3] == 'no')
    if n == 0:  # truncated or broken file: stop before it replaces the stored copy
        raise ValueError('unreadable PDF (pdfinfo: 0 pages): ' + sh(['pdfinfo', path]).stderr.strip()[-120:])
    rec.update(pages=n, pdf_meta=meta, fonts_uni_no=uni_no, sha256=hashlib.sha256(open(path, 'rb').read()).hexdigest())
    # Release asset (originals; repo itself keeps only text)
    host = re.sub(r'[^a-z0-9]+', '-', urllib.parse.urlsplit(rec['url']).netloc.lower()).strip('-') or 'inbox'
    tag = f'src-{host}'
    ensure_release(tag)
    named = os.path.join(os.path.dirname(path), did + '.pdf')
    os.link(path, named)
    up = sh(['gh', 'release', 'upload', tag, named, '--clobber', '-R', REPO])
    asset = f'https://github.com/{REPO}/releases/download/{tag}/{did}.pdf'
    if up.returncode:
        rec['release_error'] = up.stderr.strip()[-200:]
    else:
        rec['asset'] = asset
    pages = parse_pages(pages_spec, n)
    work = tempfile.mkdtemp()
    layer, need = {}, []
    for p in pages:
        t = sh(['pdftotext', '-layout', '-f', str(p), '-l', str(p), path, '-']).stdout
        t = re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', t)  # bidi controls
        st = check_layer(t)
        if uni_no and st == 'ok' and len(re.findall(r'[א-ת]', t)) < 50:
            st = 'garbled'  # uni=no fonts: trust the layer only where real Hebrew came out
        layer[p] = (st, t)
        if st != 'ok':
            need.append(p)
    ocr = ocr_pages(path, need, work) if need else {}
    imgs = image_pages(path) & set(pages)
    tables = {p for p in pages if table_like(ocr.get(p) or layer[p][1])}
    fig = ocr_extra(path, sorted(p for p in imgs if p not in ocr), work, 11, 'fig')  # labels inside pictures on text-layer pages
    tab = ocr_extra(path, sorted(p for p in tables if p in ocr), work, 6, 'tab')     # scanned tables: row-preserving pass
    out, confs = [], {}
    for p in pages:
        st, t = layer[p]
        flags = ''.join(f'; {f}' for f, on in (('image', p in imgs), ('table', p in tables)) if on)
        if p in ocr:
            cf = ocr_conf(work, p)
            confs[p] = cf
            if cf is not None:
                flags += f'; conf={cf}' + ('; lowconf' if cf < 75 else '')
            body = f'=== PAGE {p} === [ocr; layer={st}{flags}]\n{ocr[p].strip()}\n'
        else:
            body = f'=== PAGE {p} === [text-layer{flags}]\n{fix_bidi(t).strip()}\n'
        fw = new_words(fig.get(p, ''), t) if p in fig else ''
        if fw:
            body += f'--- figure-ocr (text inside images; verify on page image) ---\n{fw}\n'
        if tab.get(p, '').strip():
            body += f'--- table-ocr psm6 (row order; verify values on page image) ---\n{tab[p].strip()}\n'
        out.append(body)
    raw = '\n'.join(out)
    if ocr:
        tmp_in, tmp_out = os.path.join(work, 'all_raw.txt'), os.path.join(work, 'all_fixed.txt')
        open(tmp_in, 'w', encoding='utf-8').write(raw)
        r = sh(['python3', '-I', os.path.join(TOOLS, 'heb_ocr_fix.py'), tmp_in, tmp_out])
        if os.path.exists(tmp_out):
            raw = open(tmp_out, encoding='utf-8').read()
        rec['fix_log'] = r.stderr.splitlines()[:1]
    rec.update(image_pages=len(imgs), table_pages=len(tables), figure_ocr_pages=len(fig), table_ocr_pages=len(tab))
    cv = [c for c in confs.values() if c is not None]
    rec.update(ocr_conf_mean=round(sum(cv) / len(cv)) if cv else None, lowconf_pages=sorted(p for p, c in confs.items() if c is not None and c < 75))
    rec.update(text_pages=len(pages), ocr_pages=len(ocr), layer=('broken' if len(need) == len(pages) else 'mixed') if need else 'ok')
    return raw


def pending():
    """Request files with no results yet, and their shard count ('# shards=N' line, default 1)."""
    out = []
    for req in sorted(glob.glob(os.path.join(ROOT, 'requests', '*.txt'))):
        name = os.path.splitext(os.path.basename(req))[0]
        if glob.glob(os.path.join(ROOT, 'results', name + '*.jsonl')):
            continue
        m = re.search(r'^#\s*shards=(\d+)', open(req, encoding='utf-8').read(), re.M)
        out.append((name, req, min(int(m.group(1)), 20) if m else 1))
    return out


def force(req):
    return bool(re.search(r'^#\s*force\b', open(req, encoding='utf-8').read(), re.M))


def weekly():
    """Scheduled re-check. Source of truth = the sheet export (sheet/links.jsonl) minus removed.txt,
    plus inbox/manual docs' original URLs are not re-fetched. One request file, 20 shards."""
    lf = os.path.join(ROOT, 'sheet', 'links.jsonl')
    urls = [json.loads(l)['url'].split('#')[0] for l in open(lf, encoding='utf-8')] if os.path.exists(lf) else []
    rm = removed_set() | set(settled_replacements())
    for m in glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json')):  # files Guy uploaded: never re-fetched from the blocked source
        r = json.load(open(m))
        if r.get('source') == 'manual upload':
            rm.add(r['url'].split('#')[0])
    for x in (json.loads(l) for l in open(os.path.join(ROOT, 'sheet', 'replacements.jsonl'), encoding='utf-8')) if os.path.exists(os.path.join(ROOT, 'sheet', 'replacements.jsonl')) else []:
        urls.append(x['new'].split('#')[0])  # the replacement is checked even before the sheet itself is updated
    urls = [u for u in dict.fromkeys(urls) if u.startswith('http') and u not in rm and docid(u) not in rm]
    name = time.strftime('weekly-%Y-%m-%d', time.gmtime())
    open(os.path.join(ROOT, 'requests', name + '.txt'), 'w').write('# shards=20\n# report\n' + '\n'.join(urls) + '\n')
    print(name, len(urls))


def removed_set():
    """removed.txt: one URL or doc id per line (# comments ok). Those docs are deleted and never fetched again."""
    f = os.path.join(ROOT, 'removed.txt')
    if not os.path.exists(f):
        return set()
    return {l.split('#')[0].strip() for l in open(f, encoding='utf-8') if l.split('#')[0].strip()}


def apply_removed():
    rm = removed_set()
    n = 0
    for m in glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json')):
        r = json.load(open(m)); did = os.path.basename(os.path.dirname(m))
        if did in rm or r['url'].split('#')[0] in rm:
            if r.get('asset') and REPO and not r.get('duplicate_of'):
                tag = r['asset'].split('/download/')[1].split('/')[0]
                sh(['gh', 'release', 'delete-asset', tag, did + '.pdf', '-y', '-R', REPO])
            shutil.rmtree(os.path.dirname(m)); n += 1
    print(f'removed: {n} docs', file=sys.stderr)


def dedupe():
    """One document = one copy. Same bytes (sha256) or, for HTML, same final URL -> keep one canonical id
    (the smallest id), turn the others into aliases: no text/sections/search rows, no second Release asset.
    Runs in the index job after all shards, so it is race-free and deterministic."""
    groups = {}
    for m in sorted(glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json'))):
        r = json.load(open(m))
        key = r.get('sha256') or (r.get('kind') == 'html' and (r.get('final_url') or '').lower().split('#')[0])
        if key:
            groups.setdefault(key, []).append((os.path.basename(os.path.dirname(m)), r))
    n = 0
    for key, docs in groups.items():
        ids = sorted({d for d, _ in docs})
        if len(ids) < 2:
            continue
        canon = ids[0]
        cm = os.path.join(ROOT, 'docs', canon, 'meta.json')
        c = json.load(open(cm))
        aliases = set(c.get('aliases', []))
        for did, r in docs:
            if did == canon:
                continue
            aliases.add(r['url'])
            d = os.path.join(ROOT, 'docs', did)
            for f in ('text.md', 'sections.json'):
                if os.path.exists(os.path.join(d, f)):
                    os.remove(os.path.join(d, f))
            if r.get('asset') and r['asset'] != c.get('asset') and REPO:
                tag = r['asset'].split('/download/')[1].split('/')[0]
                sh(['gh', 'release', 'delete-asset', tag, did + '.pdf', '-y', '-R', REPO])
            r.update(duplicate_of=canon, asset=c.get('asset'))
            json.dump(r, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
            n += 1
        c['aliases'] = sorted(aliases - {c['url']})
        json.dump(c, open(cm, 'w'), ensure_ascii=False, indent=1)
    print(f'dedupe: {n} duplicate ids folded', file=sys.stderr)


def sheet_maps():
    """sheet/links.jsonl + sheet/records.jsonl (exported from the Google Sheet by a session) -> url -> rows."""
    recs, by_url = {}, {}
    rf, lf = os.path.join(ROOT, 'sheet', 'records.jsonl'), os.path.join(ROOT, 'sheet', 'links.jsonl')
    if os.path.exists(rf):
        for l in open(rf, encoding='utf-8'):
            r = json.loads(l); recs[r['id']] = r
    if os.path.exists(lf):
        for l in open(lf, encoding='utf-8'):
            r = json.loads(l)
            by_url.setdefault(r['url'].split('#')[0], []).append(r)
    return recs, by_url


YEAR = re.compile(r'(?<!\d)(19[5-9]\d|20[0-4]\d)(?!\d)')


def build_status():
    """status.jsonl: latest check per URL (all results); inaccessible.jsonl: the ones still not readable, with the reasons."""
    recs, by_url = sheet_maps()
    last = {}
    for f in sorted(glob.glob(os.path.join(ROOT, 'results', '*.jsonl'))):
        for l in open(f, encoding='utf-8'):
            r = json.loads(l)
            u = r['url'].split('#')[0]
            if u not in last or (r.get('checked') or '') >= (last[u].get('checked') or ''):
                last[u] = r
    rm = removed_set() | set(settled_replacements(last))
    have = stored_urls()
    with open(os.path.join(ROOT, 'status.jsonl'), 'w', encoding='utf-8') as fs, open(os.path.join(ROOT, 'inaccessible.jsonl'), 'w', encoding='utf-8') as fi:
        for u in sorted(last):
            if u in rm:
                continue
            r = last[u]
            row = {'url': u, 'id': r.get('id'), 'result': r.get('result'), 'status': r.get('status'), 'via': r.get('via'),
                   'server': r.get('server'), 'browser': (r.get('browser') or {}).get('status') if isinstance(r.get('browser'), dict) else None,
                   'archive': r.get('wayback') or r.get('archive_snapshot'), 'checked': r.get('checked'),
                   'sheet': sorted({x['record'] for x in by_url.get(u, [])}), 'sheet_rows': sorted({x['row'] for x in by_url.get(u, []) if x.get('row') is not None})}
            fs.write(json.dumps(row, ensure_ascii=False) + '\n')
            # inaccessible = still unreadable, still in the map, and no stored copy (manual upload / mirror)
            if not str(row['result'] or '').startswith(('ok', 'redirect')) and u in by_url and urllib.parse.unquote(u) not in have:
                fi.write(json.dumps(row, ensure_ascii=False) + '\n')


def latest_results():
    last = {}
    for f in glob.glob(os.path.join(ROOT, 'results', '*.jsonl')):
        for l in open(f, encoding='utf-8'):
            r = json.loads(l); u = r['url'].split('#')[0]
            if (r.get('checked') or '') >= (last.get(u, {}).get('checked') or ''):
                last[u] = r
    return last


def stored_urls():
    """Unquoted URLs that already have a stored document (fetched or uploaded by hand)."""
    have = set()
    for m in glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json')):
        r = json.load(open(m))
        if r.get('pages') or r.get('asset') or r.get('source'):
            have |= {urllib.parse.unquote(v.split('#')[0]) for v in [r.get('url'), r.get('final_url')] + r.get('aliases', []) if v}
    return have


def settled_replacements(last=None):
    """Old URLs Guy already replaced AND whose new URL now opens: never re-check or re-report them."""
    rp = os.path.join(ROOT, 'sheet', 'replacements.jsonl')
    if not os.path.exists(rp):
        return {}
    last = last if last is not None else latest_results()
    have = stored_urls()
    out = {}
    for l in open(rp, encoding='utf-8'):
        x = json.loads(l)
        if x.get('deferred'):
            continue
        n = x['new'].split('#')[0]
        if str(last.get(n, {}).get('result', '')).startswith(('ok', 'redirect')) or urllib.parse.unquote(n) in have:
            out[x['old'].split('#')[0]] = x  # new URL opens, or a copy is already stored (manual upload)
    return out


def build_pending():
    """pending.md: everything that waits for Guy's decision, newest check first.
    Per unresolved link: sheet record + title, reason chain, and replacement candidates ranked by title-word overlap."""
    recs, by_url = sheet_maps()
    words = lambda t: {w for w in re.findall(r'[א-תA-Za-z0-9.]{3,}', t or '')}
    rows = [json.loads(l) for l in open(os.path.join(ROOT, 'inaccessible.jsonl'), encoding='utf-8')] if os.path.exists(os.path.join(ROOT, 'inaccessible.jsonl')) else []
    last = {}
    for f in glob.glob(os.path.join(ROOT, 'results', '*.jsonl')):
        for l in open(f, encoding='utf-8'):
            r = json.loads(l); u = r['url'].split('#')[0]
            if (r.get('checked') or '') >= (last.get(u, {}).get('checked') or ''):
                last[u] = r
    rp = os.path.join(ROOT, 'sheet', 'replacements.jsonl')
    decided = {json.loads(l)['old']: json.loads(l) for l in open(rp, encoding='utf-8')} if os.path.exists(rp) else {}
    settled = settled_replacements()
    have = stored_urls()
    out = ['# ממתין להחלטה', '', 'נבנה אוטומטית בסוף כל ריצה. לכל קישור שלא נפתח: הרשומה, הסיבה, והצעות לתחליף (אם נמצאו).',
           'כדי להחליט: כתוב בשיחה "שורה N → קישור" (או "להסיר" / "ידני"), ואני אעדכן את הריפו.', '']
    for row in sorted(rows, key=lambda r: (r.get('sheet') or ['~'])[0]):
        u = row['url']; r = last.get(u, {})
        if u not in by_url:
            continue  # probes / old forms no longer in the sheet
        if u in settled or urllib.parse.unquote(u) in have:
            continue  # decided and the replacement works, or a copy is stored: nothing to ask
        title = '; '.join(f"{i} — {recs.get(i, {}).get('title', '')}" for i in row.get('sheet') or []) or '(לא ברשומות)'
        out.append(f"## {title}")
        out.append(f"- קישור: [{urllib.parse.unquote(u)[-80:]}]({u})")
        if decided.get(u, {}).get('deferred'):
            out.append(f"- נדחה לבינתיים: {decided[u]['kind']}"); out.append('')
            continue
        if u in decided:
            out.append(f"- הוחלט ({decided[u].get('by', '')}): {decided[u].get('kind', '')} → [{urllib.parse.unquote(decided[u]['new']).split('/')[-1][:70]}]({decided[u]['new']}) — התחליף עוד לא נפתח, צריך החלטה חדשה")
            out.append('')
            continue
        out.append(f"- סיבה: {row.get('result')} · שרת {row.get('server') or '-'} · דפדפן {row.get('browser') or '-'} · ארכיון {row.get('archive') or '-'} · נבדק {row.get('checked', '')[:10]}")
        tw = words(' '.join(recs.get(i, {}).get('title', '') for i in row.get('sheet') or []))
        cands = sorted(r.get('candidates') or [], key=lambda c: -len(words(c.get('text', '') + ' ' + urllib.parse.unquote(c.get('url', ''))) & tw))
        for c in cands[:5]:
            if c.get('url'):
                out.append(f"  - הצעה: [{(c.get('text') or '').strip()[:70] or urllib.parse.unquote(c['url']).split('/')[-1][:70]}]({c['url']})")
        if not cands:
            out.append('  - אין הצעה אוטומטית')
        out.append('')
    open(os.path.join(ROOT, 'pending.md'), 'w', encoding='utf-8').write('\n'.join(out))


def build_index():
    recs, by_url = sheet_maps()
    rows = []
    for m in sorted(glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json'))):
        r = json.load(open(m))
        if r.get('duplicate_of'):
            continue
        urls = {u.split('#')[0] for u in [r['url'], r.get('final_url') or ''] + r.get('aliases', []) if u}
        links = [x for u in urls for x in by_url.get(u, [])]
        ids = sorted({x['record'] for x in links}, key=lambda i: (len(i), i))
        sj = os.path.join(os.path.dirname(m), 'sections.json')
        front = json.load(open(sj)).get('front', {}) if os.path.exists(sj) else {}
        years = sorted({int(y) for t in [x['desc'] for x in links] + front.get('dates', []) for y in YEAR.findall(t)})
        r['_sheet'] = {'records': [{k: recs.get(i, {}).get(k) for k in ('id', 'title', 'section', 'status')} for i in ids],
                       'desc': sorted({x['desc'] for x in links}), 'rows': sorted({x['row'] for x in links if x.get('row') is not None})}
        r['_year'] = years[-1] if years else None
        rows.append(r)
    # edition status: only what the sheet text says explicitly (no guessing across different documents of one record)
    GENERIC_DESC = re.compile(r'דף הפרסום|הפניה מקורית|הפניה באקסל|^קישור')
    NEWER = re.compile(r'מהדורה (רשמית )?מאוחרת|מהדורה עדכנית|מחליפ|עדכון (מס[\'׳]?\s*)?\d|מהדורה אחרונה')
    OLDER = re.compile(r'(עותק|נוסח|מקור|כרך) היסטורי|מהדורה קודמת|הוחלפ|בוטל')
    newest = {}
    for r in rows:
        if any(NEWER.search(d) for d in r['_sheet']['desc']):
            for rec in r['_sheet']['records']:
                newest.setdefault(rec['id'], []).append(r['id'])
    base_titles = collections.Counter(r['_sheet']['records'][0]['title'] for r in rows
                                      if r['_sheet']['records'] and not r.get('title'))
    with open(os.path.join(ROOT, 'index.jsonl'), 'w', encoding='utf-8') as f:
        for r in rows:
            keep = {k: r.get(k) for k in ('id', 'url', 'final_url', 'kind', 'title', 'pages', 'layer', 'text_pages', 'ocr_pages', 'image_pages', 'table_pages', 'asset', 'sha256', 'checked')}
            keep['pdf_title'] = (r.get('pdf_meta') or {}).get('Title')
            sheet = r['_sheet']
            keep.update(sheet_records=sheet['records'], sheet_desc=sheet['desc'], sheet_rows=sheet['rows'], year=r['_year'])
            if sheet['records'] and not keep.get('title'):
                rt = sheet['records'][0]['title']
                # a record with several documents: add this document's own link description, so each title is distinct
                d = [x for x in sheet['desc'] if not GENERIC_DESC.search(x)]
                clash = base_titles.get(rt, 0) > 1  # several documents would otherwise show the same title
                keep['title'] = f"{rt} – {d[0]}" if clash and len(d) == 1 and d[0] not in rt else rt
            if r.get('kind') == 'pdf':
                desc = sheet['desc']
                keep['edition_status'] = ('newer' if any(NEWER.search(d) for d in desc) else
                                          'older' if any(OLDER.search(d) for d in desc) else None)
                keep['newer_in_record'] = sorted({i for rec in sheet['records'] for i in newest.get(rec['id'], []) if i != r['id']})
                keep['edition_check'] = 'from sheet wording only; null = not stated. Confirm edition/date on the cover image'
            f.write(json.dumps(keep, ensure_ascii=False) + '\n')


def known_urls():
    """Every URL already in a request file or in the sheet export."""
    k = set()
    for req in glob.glob(os.path.join(ROOT, 'requests', '*.txt')):
        k |= {l.split()[0].split('#')[0] for l in open(req, encoding='utf-8') if l.strip() and not l.startswith('#')}
    lf = os.path.join(ROOT, 'sheet', 'links.jsonl')
    if os.path.exists(lf):
        k |= {json.loads(l)['url'].split('#')[0] for l in open(lf, encoding='utf-8')}
    return k


KNOWN = set()


def process_inbox():
    """Manual uploads: inbox/<name>.pdf (+ optional inbox/<name>.url = original URL / source note).
    Processed like a download (same OCR, sections, Release asset), then removed from inbox/."""
    out = []
    for pdf in sorted(glob.glob(os.path.join(ROOT, 'inbox', '*.pdf'))):
        base = os.path.splitext(pdf)[0]
        src = open(base + '.url', encoding='utf-8').read().strip() if os.path.exists(base + '.url') else ''
        url = src.split()[0] if src.startswith('http') else 'inbox:' + os.path.basename(pdf)
        did = docid(url)
        rec = {'url': url, 'id': did, 'source': 'manual upload', 'note': src, 'status': 200, 'kind': 'pdf', 'result': 'ok',
               'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        with tempfile.TemporaryDirectory() as td:
            path = os.path.join(td, 'f'); shutil.copy(pdf, path)
            d = os.path.join(ROOT, 'docs', did); os.makedirs(d, exist_ok=True)
            try:
                text = process_pdf(rec, path, None, did)
                open(os.path.join(d, 'text.md'), 'w', encoding='utf-8').write(text)
                sections.build(d)
            except Exception as e:
                rec['process_error'] = repr(e)[:300]
            json.dump(rec, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
        if 'asset' in rec:  # stored in Releases -> drop the repo copy
            os.remove(pdf)
            if os.path.exists(base + '.url'): os.remove(base + '.url')
        out.append(rec)
        print(f"inbox {rec.get('result')} {url}", flush=True)
    if out:
        with open(os.path.join(ROOT, 'results', time.strftime('inbox-%Y%m%d-%H%M%S.jsonl', time.gmtime())), 'w', encoding='utf-8') as f:
            for r in out: f.write(json.dumps(r, ensure_ascii=False) + '\n')


def alternates(url):
    """Known mirror patterns. gov.il BlobFolder keeps the same file under several language folders
    (/he/ /ar/ /en/ /ru/): when one returns 404/403, the others often still serve it."""
    out = []
    m = re.match(r'(https?://www\.gov\.il/BlobFolder/[^/]+/[^/]+/)(he|ar|en|ru|am)(/.*)$', url)
    if m:
        out += [m.group(1) + lang + m.group(3) for lang in ('he', 'ar', 'en', 'ru') if lang != m.group(2)]
    return out


def try_alternates(rec, url, path):
    """Try mirror URLs, then the Internet Archive. Returns page text / True when a copy was found (rec updated), else None."""
    first = {k: rec.get(k) for k in ('status', 'result', 'server')}
    for alt in alternates(url):
        time.sleep(PACE.get(urllib.parse.urlsplit(alt).netloc.lower(), 1.5))
        a = fetch(alt, path)
        if a.get('status') == 200 and open(path, 'rb').read(5) == b'%PDF-':
            rec.update({k: a[k] for k in ('status', 'final_url', 'content_type', 'bytes') if k in a}, via='alternate', alt_url=alt, first_try=first)
            text = classify(rec, path)
            rec['result'] = 'ok (alternate ' + re.search(r'/(he|ar|en|ru)/', alt).group(0) + ')'
            return text or True
    wb = wayback_fetch(url, path)
    if wb.get('status') == 200:
        rec.update({k: wb[k] for k in ('status', 'final_url', 'content_type', 'bytes', 'archive_snapshot', 'archive_url') if k in wb}, via='wayback', first_try=first)
        text = classify(rec, path)
        rec['result'] = 'ok (archive copy ' + rec['archive_snapshot'][:8] + ')'
        return text or True
    rec['wayback'] = wb.get('error') or wb.get('status')
    rec['alternates_tried'] = alternates(url)
    rec['candidates'] = parent_candidates(url)
    return None


def parent_candidates(url):
    """gov.il BlobFolder/<type>/<slug>/<lang>/file -> the publication page gov.il/he/pages/<slug> lists the files
    published now. Return them (text + url) as replacement candidates for a human / session to confirm."""
    m = re.match(r'https?://www\.gov\.il/BlobFolder/[^/]+/([^/]+)/', url)
    if not m:
        return []
    page = f'https://www.gov.il/he/pages/{m.group(1)}'
    with tempfile.TemporaryDirectory() as td:
        f = os.path.join(td, 'p')
        time.sleep(PACE['www.gov.il'])
        b = browser_fetch(page, f)
        if b.get('status') != 200 or not os.path.exists(f):
            return [{'page': page, 'error': b.get('status')}]
        r = {'url': page, 'status': 200, 'final_url': b.get('final_url', page)}
        classify(r, f)
        return [{'page': page, 'text': x['text'], 'url': x['url']} for x in r.get('file_links', []) if 'BlobFolder' in x['url']][:40]


TRANSIENT = (403, 429, 503, 0)
BACKOFF = (90, 240)  # seconds before curl attempt 2 and 3 (plus jitter)


def host_next(url):
    host = urllib.parse.urlsplit(url).netloc.lower()
    return LAST_HIT.get(host, 0) + PACE.get(host, 1.5)


def mark(url):
    LAST_HIT[urllib.parse.urlsplit(url).netloc.lower()] = time.time()


def run_queue(lines, req):
    """Process URLs as a time-aware queue: a URL waiting for its gov.il back-off (or host pacing)
    does not block the shard - other URLs (other hosts, or OCR work) run in the meantime."""
    work = []
    for line in lines:
        parts = line.split()
        url, opts = parts[0], dict(p.split('=', 1) for p in parts[1:] if '=' in p)
        td = tempfile.mkdtemp()
        work.append({'url': url, 'opts': opts, 'did': docid(url), 'td': td, 'path': os.path.join(td, 'f'),
                     'stage': 'render' if opts.get('render') else 'curl', 'tries': [], 'nb': 0.0, 'rec': None})
    recs = []
    while work:
        now = time.time()
        ready = [w for w in work if w['nb'] <= now and host_next(w['url']) <= now]
        if not ready:
            t = min(max(w['nb'], host_next(w['url'])) for w in work)
            time.sleep(max(0.2, min(t - now, 30)))
            continue
        w = ready[0]
        url, path = w['url'], w['path']
        mark(url)
        if w['stage'] == 'curl':
            rec = fetch(url, path)
            w['tries'].append(rec.get('status'))
            if rec.get('status') in TRANSIENT and len(w['tries']) <= len(BACKOFF):
                w['nb'] = time.time() + BACKOFF[len(w['tries']) - 1] + random.random() * 30
                print(f"   wait {url[:90]} after {rec.get('status')} (try {len(w['tries'])})", flush=True)
                continue
            rec['tries'], rec['id'] = w['tries'], w['did']
            text = classify(rec, path)
            if rec['result'].startswith(('error 403', 'blocked', 'error 0')):
                w.update(stage='browser', rec=rec, nb=time.time() + 60 + random.random() * 30)
                continue
            if rec['result'].startswith(('error 404', 'error 410')):
                t = try_alternates(rec, url, path)
                text = t if isinstance(t, str) else None
        elif w['stage'] == 'browser':
            rec = w['rec']
            b = browser_fetch(url, path)
            if b.get('status') == 200:
                first = {k: rec.get(k) for k in ('status', 'result', 'server')}
                rec.update(b, via='browser', first_try=first)
                text = classify(rec, path)
            else:
                rec['browser'] = b
                t = try_alternates(rec, url, path)
                text = t if isinstance(t, str) else None
        else:  # render: JS-built page, straight to Chromium
            b = browser_fetch(url, path)
            rec = {'url': url, 'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), **b, 'via': 'browser (render)'}
            rec.setdefault('redirects', 0)
            rec['id'] = w['did']
            text = classify(rec, path)
        work.remove(w)
        finalize(rec, path, w['opts'], w['did'], req, text)
        shutil.rmtree(w['td'], ignore_errors=True)
        recs.append(rec)
    return recs


def finalize(rec, path, opts, did, req, text):
    url = rec['url']
    print(f"{rec.get('status')} {rec['result']:<10} {rec['kind']:<5} {url[:110]}", flush=True)
    d = os.path.join(ROOT, 'docs', did)
    try:
        old = None if force(req) or rec['kind'] != 'pdf' or rec.get('status') != 200 else unchanged(path, did)
        if old:
            rec.update({k: old.get(k) for k in ('pages', 'pdf_meta', 'fonts_uni_no', 'sha256', 'asset', 'text_pages', 'ocr_pages', 'layer', 'image_pages', 'table_pages', 'figure_ocr_pages', 'table_ocr_pages', 'ocr_conf_mean', 'lowconf_pages')}, change='unchanged')
            text = None  # keep existing text.md / sections.json
        elif rec['kind'] == 'xlsx' and rec.get('status') == 200:
            text = process_xlsx(rec, path, did)
        elif rec['kind'] == 'pdf' and rec.get('status') == 200:
            prev = json.load(open(os.path.join(d, 'meta.json'))).get('sha256') if os.path.exists(os.path.join(d, 'meta.json')) else None
            text = process_pdf(rec, path, opts.get('pages'), did)
            if prev:
                rec['change'] = 'changed' if prev != rec.get('sha256') else 'reprocessed'
    except Exception as e:  # keep going on one bad file
        rec['process_error'] = repr(e)[:300]
    if text:
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, 'text.md'), 'w', encoding='utf-8').write(text)
        try:
            sections.build(d)
        except Exception as e:
            rec['sections_error'] = repr(e)[:200]
    if rec.get('file_links') is not None:  # discovery: files on the page that we did not know before
        old = os.path.join(d, 'meta.json')
        prev = {x['url'] for x in json.load(open(old)).get('file_links', [])} if os.path.exists(old) else None
        if prev is not None:
            rec['new_file_links'] = [x for x in rec['file_links'] if x['url'] not in prev]
        rec['unknown_file_links'] = [x for x in rec['file_links'] if x['url'].split('#')[0] not in KNOWN]
    if rec.get('process_error') and rec['kind'] in ('pdf', 'xlsx'):
        rec['result'] = f"error (unreadable {rec['kind']})"  # keep the previous meta.json / text.md / asset untouched
    elif rec['kind'] in ('pdf', 'xlsx', 'html', 'zip') and rec.get('status') == 200:
        os.makedirs(d, exist_ok=True)
        json.dump(rec, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)


def main():
    global KNOWN
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    KNOWN = known_urls()
    if sys.argv[1:2] == ['matrix']:  # used by the workflow to size the job matrix
        n = max([s for _, _, s in pending()] or [1])
        print(json.dumps({'shard': list(range(n))}))
        return
    if sys.argv[1:2] == ['weekly']:
        weekly()
        return
    if sys.argv[1:2] == ['index']:
        apply_removed()
        dedupe()
        build_index()
        build_status()
        build_pending()
        return
    shard = int(os.environ.get('SHARD', '0'))
    if shard == 0:
        process_inbox()
    for name, req, nshard in pending():
        if shard >= nshard:
            continue
        res = os.path.join(ROOT, 'results', f'{name}.{shard}.jsonl' if nshard > 1 else f'{name}.jsonl')
        lines = [l.strip() for l in open(req, encoding='utf-8') if l.strip() and not l.startswith('#')]
        rm = removed_set()
        mine = [l for i, l in enumerate(lines) if i % nshard == shard and l.split()[0].split('#')[0] not in rm and docid(l.split()[0]) not in rm]
        recs = run_queue(mine, req)
        with open(res, 'w', encoding='utf-8') as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
