"""One command for a Claude session: search + full citation for each hit.

Usage: python3 tools/ask.py "רוחב נתיב מינימלי" [-n 8] [--doc <id>] [--json]
Per hit: document (sheet title), sheet record, edition status, chapter / section / nearest heading,
printed page, PDF page, link URL#page=N, where the hit is (text / table / figure), OCR confidence, snippet.
Uses tools/get_index.sh, so the index is always in sync with docs/.
"""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import search_index, sections  # noqa: E402


def index_rows():
    rows = {}
    f = os.path.join(ROOT, 'index.jsonl')
    if os.path.exists(f):
        for l in open(f, encoding='utf-8'):
            r = json.loads(l); rows[r['id']] = r
    return rows


def main(a):
    q = a[0]
    n = int(a[a.index('-n') + 1]) if '-n' in a else 8
    doc = a[a.index('--doc') + 1] if '--doc' in a else None
    db = os.environ.get('SEARCH_DB') or subprocess.run(['sh', os.path.join(ROOT, 'tools', 'get_index.sh')], capture_output=True, text=True).stdout.strip()
    idx = index_rows()
    out = []
    for h in search_index.query(db, q, n, doc):
        d = os.path.join(ROOT, 'docs', h['id'])
        r = idx.get(h['id'], {})
        try:
            word = next((w for w in q.split() if len(w) > 2), None)
            c = sections.cite(d, h['page'], word)
        except Exception:
            c = {}
        conf = re.search(r'conf=(\d+)', h['method'] or '')
        out.append({
            'doc': r.get('title') or c.get('doc'), 'id': h['id'],
            'sheet': [f"{x['id']} — {x['title']}" for x in r.get('sheet_records', [])],
            'edition_status': r.get('edition_status'), 'newer_in_record': r.get('newer_in_record'),
            'front': c.get('front'), 'chapter': c.get('chapter'), 'section': c.get('section'),
            'nearest_heading': c.get('nearest_heading'), 'printed_page': c.get('printed_page'),
            'pdf_page': h['page'], 'link': h['link'], 'where': h['where'], 'method': h['method'],
            'ocr_conf': int(conf.group(1)) if conf else None, 'snippet': h['snippet'],
            'asset': r.get('asset'), 'sha256': r.get('sha256')})
    if '--json' in a:
        print(json.dumps(out, ensure_ascii=False, indent=1)); return
    for i, o in enumerate(out, 1):
        sec = ' · '.join(x for x in [o['chapter'], o['section']] if x) or (o['nearest_heading'] or {}).get('title') or 'עמוד בלבד'
        warn = []
        if o['where'] != 'text': warn.append(o['where'])
        if o['ocr_conf'] is not None and o['ocr_conf'] < 75: warn.append(f"OCR conf {o['ocr_conf']}: read the page image")
        if o['edition_status'] == 'older': warn.append('older edition per sheet')
        if o['newer_in_record']: warn.append(f"newer doc in record: {o['newer_in_record']}")
        print(f"{i}. {o['doc']}  [{o['id']}]")
        if o['sheet']: print(f"   sheet: {'; '.join(o['sheet'])}")
        print(f"   {sec} | עמ׳ {o['printed_page'] or '-'} (PDF {o['pdf_page']}) | {o['link']}")
        if warn: print(f"   ! {' | '.join(warn)}")
        print(f"   {o['snippet']}")


if __name__ == '__main__':
    main(sys.argv[1:]) if sys.argv[1:] else print(__doc__)
