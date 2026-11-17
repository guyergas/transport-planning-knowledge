"""National datasets (not documents): data/sources.jsonl -> GitHub Release 'data-<name>' + data/<name>/meta.json.
Line fields: name, title, page, and either url (one file) or ckan (data.gov.il package name; every resource whose
name/url matches 'match' regex is downloaded). Optional: refresh_days (re-download when older), force (true = now).
No OCR, no index. Projects download the assets and clip them locally."""
import hashlib, json, os, re, subprocess, time, zipfile, urllib.parse
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get('GITHUB_REPOSITORY', 'guyergas/transport-planning-knowledge')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
CKAN = 'https://data.gov.il/api/3/action/'


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def download(url, dest):
    """-> (http status, error). A login/HTML page instead of the file counts as failure."""
    url = url.replace('://e.data.gov.il/', '://data.gov.il/')  # e. host redirects to Google sign-in
    code, err = '0', ''
    for wait in (0, 90, 240):  # same pacing idea as fetch.py
        time.sleep(wait)
        r = sh(['curl', '-sSL', '--retry', '2', '-A', UA, '-o', dest, '-w', '%{http_code}', url])
        code, err = r.stdout.strip() or '0', r.stderr.strip()[-200:]
        if code == '200' and os.path.exists(dest) and open(dest, 'rb').read(64).lstrip()[:1] == b'<' and not url.endswith(('.html', '.htm')):
            code, err = '200', 'got an HTML page instead of the file (login/challenge)'
        if code == '200' and not err or err.startswith('got an HTML'):
            break
    return int(code), err


def datastore_csv(rid, dest):
    """CKAN datastore resources: page through datastore_search (the file link may need a login)."""
    import csv
    off, n, w = 0, 0, None
    with open(dest, 'w', newline='', encoding='utf-8') as f:
        while True:
            d = ckan('datastore_search', resource_id=rid, limit=32000, offset=off)
            if not d.get('success'):
                return 0
            recs = d['result']['records']
            if not recs:
                break
            if w is None:
                w = csv.DictWriter(f, fieldnames=[k for k in recs[0] if k != '_id'], extrasaction='ignore')
                w.writeheader()
            w.writerows(recs)
            n += len(recs)
            off += len(recs)
            time.sleep(1.5)
    return n


def ckan(action, **q):
    r = sh(['curl', '-sSL', '-A', UA, CKAN + action + '?' + urllib.parse.urlencode(q)])
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {'success': False, 'raw': r.stdout[:300]}


def due(meta, s):
    if s.get('force') or not meta or meta.get('status') != 200:
        return True
    days = s.get('refresh_days')
    if not days:
        return False
    age = time.time() - time.mktime(time.strptime(meta['checked'], '%Y-%m-%dT%H:%M:%SZ'))
    return age > days * 86400


def one_file(url, tag, name_hint=None, rid=None, mirrors=()):
    fn = re.sub(r'[^\w.\-]+', '_', name_hint or os.path.basename(url.split('?')[0])) or 'file'
    dest = os.path.join('/tmp', fn)
    rec = {'url': url, 'file': fn}
    for u in (url, *mirrors):
        rec['status'], err = download(u, dest)
        if rec['status'] == 200 and not err:
            rec['via'] = u
            break
        rec.setdefault('errors', []).append(f'{u}: {rec["status"]} {err}')
    else:
        rec['status'] = 0
        if rid:  # datastore fallback
            dest = os.path.splitext(dest)[0] + '.csv'; fn = os.path.basename(dest)
            n = datastore_csv(rid, dest)
            if n:
                rec.update(status=200, via='datastore_search', rows=n, file=fn)
    if rec['status'] == 200:
        rec.update(bytes=os.path.getsize(dest), sha256=hashlib.sha256(open(dest, 'rb').read()).hexdigest())
        if zipfile.is_zipfile(dest):
            rec['files'] = [{'name': i.filename, 'bytes': i.file_size} for i in zipfile.ZipFile(dest).infolist()]
        up = sh(['gh', 'release', 'upload', tag, dest, '--clobber', '-R', REPO])
        if up.returncode:
            rec['release_error'] = up.stderr.strip()[-300:]
        else:
            rec['asset'] = f'https://github.com/{REPO}/releases/download/{tag}/{fn}'
        os.remove(dest)
    return rec


def main():
    for line in open(os.path.join(ROOT, 'data', 'sources.jsonl'), encoding='utf-8'):
        if not line.strip():
            continue
        s = json.loads(line)
        d = os.path.join(ROOT, 'data', s['name'])
        mf = os.path.join(d, 'meta.json')
        old = json.load(open(mf)) if os.path.exists(mf) else None
        if not due(old, s):
            continue
        os.makedirs(d, exist_ok=True)
        tag = 'data-' + s['name']
        if s.get('force'):  # start clean: drop old assets
            sh(['gh', 'release', 'delete', tag, '-y', '-R', REPO])
        sh(['gh', 'release', 'create', tag, '-R', REPO, '-t', tag, '-n', s.get('title', s['name'])])
        meta = {**s, 'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        if 'url' in s:
            meta.update(one_file(s['url'], tag, mirrors=s.get('mirrors', ())))
        else:
            p = ckan('package_show', id=s['ckan'])
            if not p.get('success'):
                hits = ckan('package_search', q=s.get('search', s['ckan']), rows=15)
                meta.update(status=404, candidates=[(x['name'], x.get('title')) for x in hits.get('result', {}).get('results', [])])
            else:
                res = p['result']
                meta['metadata_modified'] = res.get('metadata_modified')
                meta['resources'] = []
                for r in res['resources']:
                    if re.search(s.get('match', '.'), (r.get('name') or '') + ' ' + (r.get('url') or ''), re.I):
                        ext = os.path.splitext(r['url'].split('?')[0])[1] or '.' + (r.get('format') or 'bin').lower()
                        meta['resources'].append({'name': r.get('name'), **one_file(r['url'], tag, r['id'][:8] + '_' + (r.get('name') or 'res') + ext, rid=r['id'] if r.get('datastore_active') else None)})
                meta['status'] = 200 if meta['resources'] and all(x['status'] == 200 for x in meta['resources']) else 207
        json.dump(meta, open(mf, 'w'), ensure_ascii=False, indent=1)
        print(meta.get('status'), s['name'], meta.get('bytes') or len(meta.get('resources', [])))


if __name__ == '__main__':
    main()
