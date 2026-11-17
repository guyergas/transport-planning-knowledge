"""National datasets (not documents): data/sources.jsonl -> GitHub Release 'data-<name>' + data/<name>/meta.json.
A dataset is downloaded only if it has no meta.json yet, or its line has "force": true. No OCR, no index."""
import hashlib, json, os, subprocess, sys, time, zipfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.environ.get('GITHUB_REPOSITORY', 'guyergas/transport-planning-knowledge')
UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def download(url, dest):
    for wait in (0, 90, 240):  # same pacing idea as fetch.py
        time.sleep(wait)
        r = sh(['curl', '-sSL', '-A', UA, '-o', dest, '-w', '%{http_code}', url])
        if r.stdout.strip() == '200':
            return 200
    return int(r.stdout.strip() or 0)


def main():
    for line in open(os.path.join(ROOT, 'data', 'sources.jsonl'), encoding='utf-8'):
        s = json.loads(line)
        d = os.path.join(ROOT, 'data', s['name'])
        if os.path.exists(os.path.join(d, 'meta.json')) and not s.get('force'):
            continue
        os.makedirs(d, exist_ok=True)
        fn = os.path.basename(s['url'].split('?')[0])
        dest = os.path.join('/tmp', fn)
        code = download(s['url'], dest)
        meta = {**s, 'checked': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'status': code}
        if code == 200:
            meta.update(bytes=os.path.getsize(dest), sha256=hashlib.sha256(open(dest, 'rb').read()).hexdigest())
            if zipfile.is_zipfile(dest):
                meta['files'] = [{'name': i.filename, 'bytes': i.file_size} for i in zipfile.ZipFile(dest).infolist()]
            tag = 'data-' + s['name']
            sh(['gh', 'release', 'create', tag, '-R', REPO, '-t', tag, '-n', s.get('title', s['name'])])
            up = sh(['gh', 'release', 'upload', tag, dest, '--clobber', '-R', REPO])
            if up.returncode:
                meta['release_error'] = up.stderr.strip()[-300:]
            else:
                meta['asset'] = f'https://github.com/{REPO}/releases/download/{tag}/{fn}'
        json.dump(meta, open(os.path.join(d, 'meta.json'), 'w'), ensure_ascii=False, indent=1)
        print(code, s['name'], meta.get('bytes'), meta.get('asset') or meta.get('release_error'))


if __name__ == '__main__':
    main()
