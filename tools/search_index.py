"""Full-text search index over docs/*/text.md (SQLite FTS5, one row per page).

build:  python3 tools/search_index.py build [out.db]      -> search.db + search.json (manifest)
query:  python3 tools/search_index.py q "חניה תקן" [-n 20] [--doc <id>]
Hebrew handling: niqqud/bidi removed, final letters folded (ך->כ ...), gershayim unified,
and each word is also indexed without its prefix letters (ו ה ב כ ל מ ש), so "חניה" finds "והחניה".
"""
import glob, hashlib, json, os, re, sqlite3, subprocess, sys, time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = re.compile(r'^=== PAGE (\d+) === ?(\[[^\]]*\])?.*$', re.M)
FOLD = str.maketrans({'ך': 'כ', 'ם': 'מ', 'ן': 'נ', 'ף': 'פ', 'ץ': 'צ', '״': '"', '׳': "'", '–': '-', '־': '-'})
PREFIX = 'והבכלמש'


def norm(t):
    t = re.sub(r'[֑-ׇ‎‏‪-‮⁦-⁩]', '', t)
    return t.translate(FOLD).lower()


def expand(t):
    """word -> word + prefix-stripped variants (Hebrew only)."""
    out = []
    for w in re.findall(r'[\w"\'.-]+', t):
        w = w.strip('.-\'')
        if not w:
            continue
        out.append(w)
        if re.match(r'[א-ת]', w):
            v = w
            for _ in range(3):
                if len(v) > 3 and v[0] in PREFIX:
                    v = v[1:]; out.append(v)
                else:
                    break
            if '"' in w:
                out.append(w.replace('"', ''))
    return ' '.join(out)


def link_base(url, asset, did):
    """Manual uploads (Drive, attachments) link to the repo copy in Releases; fetched documents link to the official URL."""
    m = os.path.join(ROOT, 'docs', did, 'meta.json') if 'ROOT' in globals() else None
    manual = False
    if m and os.path.exists(m):
        manual = json.load(open(m)).get('source') == 'manual upload'
    return (asset if manual and asset else (url or '')).split('#')[0]


def build(db):
    if os.path.exists(db):
        os.remove(db)
    con = sqlite3.connect(db)
    con.execute("CREATE VIRTUAL TABLE fts USING fts5(terms, id UNINDEXED, page UNINDEXED, method UNINDEXED, tokenize='unicode61 remove_diacritics 2')")
    con.execute('CREATE TABLE text(id TEXT, page INT, body TEXT, PRIMARY KEY(id, page))')
    con.execute('CREATE TABLE docs(id TEXT PRIMARY KEY, url TEXT, title TEXT, pages INT, sha256 TEXT, asset TEXT)')
    n_docs = n_pages = 0
    for d in sorted(glob.glob(os.path.join(ROOT, 'docs', '*'))):
        did = os.path.basename(d)
        tf, mf = os.path.join(d, 'text.md'), os.path.join(d, 'meta.json')
        if not os.path.exists(tf):
            continue
        m = json.load(open(mf)) if os.path.exists(mf) else {}
        if m.get('duplicate_of'):
            continue
        con.execute('INSERT INTO docs VALUES (?,?,?,?,?,?)', (did, m.get('url'), m.get('title') or (m.get('pdf_meta') or {}).get('Title'), m.get('pages'), m.get('sha256'), m.get('asset')))
        t = open(tf, encoding='utf-8').read()
        parts = PAGE.split(t)
        if len(parts) == 1:  # HTML page: single "page"
            parts = ['', '1', '[html]', t]
        for i in range(1, len(parts) - 2, 3):
            p, method, body = int(parts[i]), (parts[i + 1] or '').strip('[]'), parts[i + 2]
            con.execute('INSERT INTO fts VALUES (?,?,?,?)', (expand(norm(body)), did, p, method))
            con.execute('INSERT OR REPLACE INTO text VALUES (?,?,?)', (did, p, body.strip()))
            n_pages += 1
        n_docs += 1
    con.commit(); con.execute("INSERT INTO fts(fts) VALUES('optimize')"); con.commit(); con.execute('VACUUM'); con.close()
    commit = subprocess.run(['git', '-C', ROOT, 'rev-parse', 'HEAD'], capture_output=True, text=True).stdout.strip()
    man = {'built': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'docs': n_docs, 'pages': n_pages,
           'source_commit': commit, 'docs_hash': docs_hash(), 'bytes': os.path.getsize(db),
           'sha256': hashlib.sha256(open(db, 'rb').read()).hexdigest()}
    json.dump(man, open(os.path.join(ROOT, 'search.json'), 'w'), indent=1)
    print(json.dumps(man))


def docs_hash():
    """Hash of all text.md files: equal hash = index in sync with docs/."""
    h = hashlib.sha256()
    for f in sorted(glob.glob(os.path.join(ROOT, 'docs', '*', 'text.md'))):
        h.update(os.path.relpath(f, ROOT).encode()); h.update(hashlib.sha256(open(f, 'rb').read()).digest())
    return h.hexdigest()


def query(db, q, n=20, doc=None):
    terms = [w for w in expand(norm(q)).split() if len(w) > 1]
    # each user word must match (word or its prefix-stripped form); FTS phrase-quote every term
    groups = []
    for w in norm(q).split():
        vs = [v for v in expand(w).split() if len(v) > 1]
        if vs:
            groups.append('(' + ' OR '.join('"%s"' % v.replace('"', '""') for v in dict.fromkeys(vs)) + ')')
    if not groups:
        return []
    con = sqlite3.connect(db)
    sql = 'SELECT fts.id, fts.page, fts.method, bm25(fts) s, d.title, d.url, d.asset FROM fts JOIN docs d ON d.id = fts.id WHERE fts MATCH ?'
    args = [' AND '.join(groups)]
    if doc:
        sql += ' AND fts.id = ?'; args.append(doc)
    rows = con.execute(sql + ' ORDER BY s LIMIT ?', args + [n]).fetchall()
    out = []
    for did, page, method, score, title, url, asset in rows:
        body = con.execute('SELECT body FROM text WHERE id=? AND page=?', (did, page)).fetchone()[0]
        nb = norm(body)
        key = next((v for w in norm(q).split() for v in [w] + expand(w).split()[1:] if v in nb), None)
        i = nb.find(key) if key else 0
        snip = re.sub(r'\s+', ' ', body[max(0, i - 120): i + 200])
        cut = min([x for x in (nb.find('--- figure-ocr'), nb.find('--- table-ocr')) if x >= 0] or [len(nb)])
        where = 'figure/table: read the page image' if i >= cut else ('table page: verify values on the image' if 'table' in method else 'text')
        out.append({'id': did, 'page': page, 'method': method, 'title': title, 'link': f"{link_base(url, asset, did)}#page={page}", 'source': url, 'snippet': snip, 'where': where})
    return out


if __name__ == '__main__':
    a = sys.argv[1:]
    if a[:1] == ['build']:
        build(a[1] if len(a) > 1 else os.path.join(ROOT, 'search.db'))
    elif a[:1] == ['q']:
        n = int(a[a.index('-n') + 1]) if '-n' in a else 20
        doc = a[a.index('--doc') + 1] if '--doc' in a else None
        db = os.environ.get('SEARCH_DB', os.path.join(ROOT, 'search.db'))
        for r in query(db, a[1], n, doc):
            print(f"{r['id']} p{r['page']} [{r['method']}] ({r['where']}) {(r['title'] or '')[:50]}\n  {r['snippet']}\n  {r['link']}")
    else:
        print(__doc__)
