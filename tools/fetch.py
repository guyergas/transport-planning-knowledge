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
    try:
        h = open(hdr, encoding='latin-1').read().lower()
        rec['server'] = (re.findall(r'^server:\s*(.+)$', h, re.M) or [''])[-1].strip()
    except OSError:
        pass
    return rec


class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.out = []; self.skip = 0; self.title = ''; self._t = False
    def handle_starttag(self, tag, a):
        if tag in ('script', 'style', 'noscript'): self.skip += 1
        if tag == 'title': self._t = True
        if tag in ('p', 'br', 'div', 'li', 'h1', 'h2', 'h3', 'h4', 'tr'): self.out.append('\n')
    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'): self.skip = max(0, self.skip - 1)
        if tag == 'title': self._t = False
    def handle_data(self, d):
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


def ensure_release(tag):
    if sh(['gh', 'release', 'view', tag, '-R', REPO]).returncode:
        sh(['gh', 'release', 'create', tag, '-R', REPO, '-t', tag, '-n', 'Original source files (see index.jsonl)'])


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
        st = check_layer(t)
        if uni_no and st == 'ok' and len(re.findall(r'[א-ת]', t)) < 50:
            st = 'garbled'  # uni=no fonts: trust the layer only where real Hebrew came out
        layer[p] = (st, t)
        if st != 'ok':
            need.append(p)
    ocr = ocr_pages(path, need, work) if need else {}
    out = []
    for p in pages:
        st, t = layer[p]
        if p in ocr:
            out.append(f'=== PAGE {p} === [ocr; layer={st}]\n{ocr[p].strip()}\n')
        else:
            out.append(f'=== PAGE {p} === [text-layer]\n{t.strip()}\n')
    raw = '\n'.join(out)
    if ocr:
        tmp_in, tmp_out = os.path.join(work, 'all_raw.txt'), os.path.join(work, 'all_fixed.txt')
        open(tmp_in, 'w', encoding='utf-8').write(raw)
        r = sh(['python3', '-I', os.path.join(TOOLS, 'heb_ocr_fix.py'), tmp_in, tmp_out])
        if os.path.exists(tmp_out):
            raw = open(tmp_out, encoding='utf-8').read()
        rec['fix_log'] = r.stderr.splitlines()[:1]
    rec.update(text_pages=len(pages), ocr_pages=len(ocr), layer=('broken' if len(need) == len(pages) else 'mixed') if need else 'ok')
    return raw


def main():
    os.makedirs(os.path.join(ROOT, 'results'), exist_ok=True)
    for req in sorted(glob.glob(os.path.join(ROOT, 'requests', '*.txt'))):
        name = os.path.splitext(os.path.basename(req))[0]
        res = os.path.join(ROOT, 'results', name + '.jsonl')
        if os.path.exists(res):
            continue
        recs = []
        for line in open(req, encoding='utf-8'):
            line = line.strip()
            if not line or line.startswith('#'):
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
                    if rec['kind'] == 'pdf' and rec.get('status') == 200:
                        text = process_pdf(rec, path, opts.get('pages'), did)
                except Exception as e:  # keep going on one bad file
                    rec['process_error'] = repr(e)[:300]
                if text:
                    os.makedirs(d, exist_ok=True)
                    open(os.path.join(d, 'text.md'), 'w', encoding='utf-8').write(text)
                if rec['kind'] in ('pdf', 'html', 'zip') and rec.get('status') == 200:
                    os.makedirs(d, exist_ok=True)
                    json.dump(rec, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
            recs.append(rec)
        with open(res, 'w', encoding='utf-8') as f:
            for r in recs:
                f.write(json.dumps(r, ensure_ascii=False) + '\n')
    # rebuild index
    with open(os.path.join(ROOT, 'index.jsonl'), 'w', encoding='utf-8') as f:
        for m in sorted(glob.glob(os.path.join(ROOT, 'docs', '*', 'meta.json'))):
            r = json.load(open(m))
            keep = {k: r.get(k) for k in ('id', 'url', 'final_url', 'kind', 'title', 'pages', 'layer', 'text_pages', 'ocr_pages', 'asset', 'sha256', 'checked')}
            keep['pdf_title'] = (r.get('pdf_meta') or {}).get('Title')
            f.write(json.dumps(keep, ensure_ascii=False) + '\n')


if __name__ == '__main__':
    main()
