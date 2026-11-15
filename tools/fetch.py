"""Process request files: check access, store PDFs in Releases, extract/OCR Hebrew text.

Request line: URL [pages=1-8,20] [ocr=auto|none]
  pages: limit text extraction to these PDF pages (default: all pages)
Outputs:
  results/<req>.jsonl          one access-check record per URL
  docs/<docid>/meta.json       document metadata (+ release asset URL)
  docs/<docid>/text.md         text with '=== PAGE N ===' markers and per-page method
  index.jsonl                  one line per document (rebuilt)
"""
import hashlib, html, json, os, re, subprocess, sys, tempfile, time, glob, urllib.parse
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


def browser_fetch(url, dest):
    """Fallback for bot-protected sites: real headless Chromium (Playwright)."""
    r = sh(['python3', os.path.join(TOOLS, 'browser_fetch.py'), url, dest], timeout=300)
    try:
        return json.loads(r.stdout.strip().splitlines()[-1])
    except Exception:
        return {'status': 0, 'error': (r.stderr or r.stdout)[-300:]}


def classify(rec, path):
    """Accessible / error / redirect / login-required, plus kind."""
    head = open(path, 'rb').read(2048) if os.path.exists(path) else b''
    rec['kind'] = 'pdf' if head.startswith(b'%PDF') else 'zip' if head.startswith(b'PK') else 'html' if b'<' in head[:200] else 'other'
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
            if u.startswith('http') and u not in seen and re.search(r'\.(pdf|zip|docx?|xlsx?|kmz|shp)(\?|#|$)|BlobFolder|/download|/media/', u, re.I):
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


def process_pdf(rec, path, pages_spec, did):
    info = sh(['pdfinfo', path]).stdout
    n = int((re.findall(r'^Pages:\s+(\d+)', info, re.M) or ['0'])[0])
    meta = {k: (re.findall(rf'^{k}:\s+(.+)$', info, re.M) or [''])[0].strip() for k in ('Title', 'Producer', 'Creator', 'CreationDate', 'ModDate')}
    fonts = sh(['pdffonts', path]).stdout
    uni_no = sum(1 for l in fonts.splitlines()[2:] if re.search(r'\s(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$', l) and l.split()[-3] == 'no')
    rec.update(pages=n, pdf_meta=meta, fonts_uni_no=uni_no, sha256=hashlib.sha256(open(path, 'rb').read()).hexdigest())
    # Release asset (originals; repo itself keeps only text)
    host = re.sub(r'[^a-z0-9]+', '-', urllib.parse.urlsplit(rec['url']).netloc.lower()).strip('-')
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
    out = []
    for p in pages:
        st, t = layer[p]
        flags = ''.join(f'; {f}' for f, on in (('image', p in imgs), ('table', p in tables)) if on)
        if p in ocr:
            body = f'=== PAGE {p} === [ocr; layer={st}{flags}]\n{ocr[p].strip()}\n'
        else:
            body = f'=== PAGE {p} === [text-layer{flags}]\n{t.strip()}\n'
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
    """Scheduled re-check: every URL ever requested, one request file, 20 shards."""
    urls = []
    for req in sorted(glob.glob(os.path.join(ROOT, 'requests', '*.txt'))):
        for l in open(req, encoding='utf-8'):
            if l.strip() and not l.startswith('#'):
                urls.append(l.split()[0])
    urls = list(dict.fromkeys(urls))
    name = time.strftime('weekly-%Y-%m-%d', time.gmtime())
    open(os.path.join(ROOT, 'requests', name + '.txt'), 'w').write('# shards=20\n' + '\n'.join(urls) + '\n')
    print(name)


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


def build_index():
    with open(os.path.join(ROOT, 'index.jsonl'), 'w', encoding='utf-8') as f:
        for m in sorted(glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json'))):
            r = json.load(open(m))
            keep = {k: r.get(k) for k in ('id', 'url', 'final_url', 'kind', 'title', 'pages', 'layer', 'text_pages', 'ocr_pages', 'image_pages', 'table_pages', 'asset', 'sha256', 'checked')}
            keep['pdf_title'] = (r.get('pdf_meta') or {}).get('Title')
            f.write(json.dumps(keep, ensure_ascii=False) + '\n')


def main():
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    if sys.argv[1:2] == ['matrix']:  # used by the workflow to size the job matrix
        n = max([s for _, _, s in pending()] or [1])
        print(json.dumps({'shard': list(range(n))}))
        return
    if sys.argv[1:2] == ['weekly']:
        weekly()
        return
    if sys.argv[1:2] == ['index']:
        dedupe()
        build_index()
        return
    shard = int(os.environ.get('SHARD', '0'))
    for name, req, nshard in pending():
        if shard >= nshard:
            continue
        res = os.path.join(ROOT, 'results', f'{name}.{shard}.jsonl' if nshard > 1 else f'{name}.jsonl')
        recs = []
        lines = [l.strip() for l in open(req, encoding='utf-8') if l.strip() and not l.startswith('#')]
        for i, line in enumerate(lines):
            if i % nshard != shard:
                continue
            parts = line.split()
            url, opts = parts[0], dict(p.split('=', 1) for p in parts[1:] if '=' in p)
            did = docid(url)
            with tempfile.TemporaryDirectory() as td:
                path = os.path.join(td, 'f')
                rec = fetch(url, path)
                rec['id'] = did
                text = classify(rec, path)
                if rec['result'].startswith(('error 403', 'blocked', 'error 0')):
                    b = browser_fetch(url, path)
                    if b.get('status') == 200:
                        first = {k: rec.get(k) for k in ('status', 'result', 'server')}
                        rec.update(b, via='browser', first_try=first)
                        text = classify(rec, path)
                    else:
                        rec['browser'] = b
                print(f"{rec.get('status')} {rec['result']:<10} {rec['kind']:<5} {url[:110]}", flush=True)
                d = os.path.join(ROOT, 'docs', did)
                try:
                    old = None if force(req) or rec['kind'] != 'pdf' or rec.get('status') != 200 else unchanged(path, did)
                    if old:
                        rec.update({k: old.get(k) for k in ('pages', 'pdf_meta', 'fonts_uni_no', 'sha256', 'asset', 'text_pages', 'ocr_pages', 'layer', 'image_pages', 'table_pages', 'figure_ocr_pages', 'table_ocr_pages')}, change='unchanged')
                        text = None  # keep existing text.md / sections.json
                    elif rec['kind'] == 'pdf' and rec.get('status') == 200:
                        if os.path.exists(os.path.join(d, 'meta.json')):
                            rec['change'] = 'changed'
                        text = process_pdf(rec, path, opts.get('pages'), did)
                except Exception as e:  # keep going on one bad file
                    rec['process_error'] = repr(e)[:300]
                if text:
                    os.makedirs(d, exist_ok=True)
                    open(os.path.join(d, 'text.md'), 'w', encoding='utf-8').write(text)
                    try:
                        sections.build(d)
                    except Exception as e:
                        rec['sections_error'] = repr(e)[:200]
                if rec['kind'] in ('pdf', 'html', 'zip') and rec.get('status') == 200:
                    os.makedirs(d, exist_ok=True)
                    json.dump(rec, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
            recs.append(rec)
        with open(res, 'w', encoding='utf-8') as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
