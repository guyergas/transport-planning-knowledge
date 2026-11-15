"""Markdown report for one request's results (used for the weekly GitHub Issue).

Usage: python3 tools/report.py <request-name>  > report.md
Sections: totals, not accessible (id, url, reason), changed documents, new files found on pages, low-confidence OCR.
"""
import glob, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    recs = []
    for f in sorted(glob.glob(os.path.join(ROOT, 'results', name + '*.jsonl'))):
        recs += [json.loads(l) for l in open(f, encoding='utf-8')]
    return recs


def main(name):
    recs = load(name)
    bad = [r for r in recs if not str(r.get('result', '')).startswith(('ok', 'redirect'))]
    arch = [r for r in recs if r.get('via') == 'wayback']
    changed = [r for r in recs if r.get('change') == 'changed']
    new = [(r, x) for r in recs for x in r.get('unknown_file_links', [])]
    low = [r for r in recs if r.get('lowconf_pages')]
    out = [f'# Knowledge-map check: {name}', '',
           f'- checked: {len(recs)}', f'- accessible: {len(recs) - len(bad)}', f'- not accessible: {len(bad)}',
           f'- from Internet Archive copy (official site blocked): {len(arch)}', f'- changed documents: {len(changed)}', f'- new files found on pages: {len(new)}', '']
    if bad:
        out += ['## Not accessible', '', '| id | url | reason |', '|---|---|---|']
        out += [f"| {r.get('id')} | {r['url']} | {r.get('result')} {r.get('server', '')}; browser: {(r.get('browser') or {}).get('status', '-') if isinstance(r.get('browser'), dict) else '-'}; archive: {r.get('wayback', '-')}; candidates on page: {len(r.get('candidates') or [])} |" for r in bad]
        out.append('')
    if arch:
        out += ['## Read from Internet Archive (official URL blocked from GitHub)', '']
        out += [f"- {r.get('id')} {r['url']} — snapshot {r.get('archive_snapshot')}" for r in arch]
        out.append('')
    if changed:
        out += ['## Changed (new bytes, re-OCRed)', '']
        out += [f"- {r.get('id')} {r['url']}" for r in changed]
        out.append('')
    if new:
        out += ['## New files on pages (not in the sheet/requests)', '']
        out += [f"- [{x.get('text') or 'file'}]({x['url']}) — on {r['url']}" for r, x in new]
        out.append('')
    if low:
        out += ['## Low OCR confidence (read these pages from the image)', '']
        out += [f"- {r.get('id')} pages {r['lowconf_pages'][:30]} — {r['url']}" for r in low]
    out += ['', '## Waiting for Guy', f"See pending.md: https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'guyergas/transport-planning-knowledge')}/blob/main/pending.md"]
    print('\n'.join(out))


if __name__ == '__main__':
    main(sys.argv[1])
