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
    code = '0'
    for wait in (0, 90, 240):  # same pacing idea as fetch.py
        time.sleep(wait)
        code = sh(['curl', '-sSL', '-A', UA, '-o', dest, '-w', '%{http_code}', url]).stdout.strip() or '0'
        if code == '200':
            break
    return int(code)


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


def one_file(url, tag, name_hint=None):
    fn = re.sub(r'[^\w.\-]+', '_', name_hint or os.path.basename(url.split('?')[0])) or 'file'
    dest = os.path.join('/tmp', fn)
    rec = {'url': url, 'file': fn, 'status': download(url, dest)}
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
        sh(['gh', 'release', 'create', tag, '-R', REPO, '-t', tag, '-n', s.get('title', s['name'])])
        meta = {**s, 'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}
        if 'url' in s:
            meta.update(one_file(s['url'], tag))
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
                        meta['resources'].append({'name': r.get('name'), **one_file(r['url'], tag, r['id'][:8] + '_' + (r.get('name') or 'res') + ext)})
                meta['status'] = 200 if meta['resources'] and all(x['status'] == 200 for x in meta['resources']) else 207
        json.dump(meta, open(mf, 'w'), ensure_ascii=False, indent=1)
        print(meta.get('status'), s['name'], meta.get('bytes') or len(meta.get('resources', [])))


if __name__ == '__main__':
    main()
