"""Build a citation map for a document from its text.md.

Usage: python3 tools/sections.py docs/<id>            (one doc)
       python3 tools/sections.py --all               (every doc + sections.jsonl)
Writes docs/<id>/sections.json:
  front:    edition / date / publisher candidates from the first pages (verify on the cover image)
  pages:    {pdf_page: printed page label}
  sections: [{num, title, chapter, start, end, level}]  (PDF pages, inclusive)
Lookup for a citation: page -> innermost section whose [start, end] contains it.
"""
import glob, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEB = re.compile(r'[א-ת]')
PAGE = re.compile(r'^=== PAGE (\d+) ===.*$', re.M)
NUM = r'(\d{1,2}(?:\.\d{1,3}){0,4})'
# numbered heading: number at line start (logical order) or end (visual order from some layers)
HEAD_START = re.compile(rf'^\s*(?:סעיף\s+)?{NUM}\s*[.)|:\-–]?\s*[|]?\s+([^\d\s].{{1,90}}?)\s*$')
HEAD_END = re.compile(rf'^\s*([^\d\s].{{1,90}}?)\s+[|]?\s*{NUM}\s*[.)]?\s*$')
CHAPTER = re.compile(r'^\s*פרק\s+(\d{1,2}|[א-ת]{1,2}[\'׳]?)\s*[.:\-–]?\s*(.{0,90}?)\s*$')
LABEL = re.compile(r'^\s*(?:עמוד|עמ[\'׳])?\s*(\d{1,3}(?:\s*[-–]\s*\d{1,3})?|[ivxlc]{1,6})\s*$', re.I)
SENT_END = re.compile(r'[.;,:]\s*$')
MONTHS = 'ינואר|פברואר|מרץ|מרס|אפריל|מאי|יוני|יולי|אוגוסט|ספטמבר|אוקטובר|נובמבר|דצמבר'


def split_pages(text):
    parts = PAGE.split(text)
    return {int(parts[i]): parts[i + 1] for i in range(1, len(parts) - 1, 2)}


def looks_heading(title):
    t = title.strip(' |-–.')
    return (2 <= len(t) <= 70 and HEB.search(t) and not SENT_END.search(title)
            and len(t.split()) <= 8 and not re.search(r'\d{3,}|[,;]|[₪%]', t)
            and not re.search(r'(^|\s)(ראה|לעיל|להלן|בפרק|בסעיף)(\s|$)', t))


def front_matter(pages):
    first = '\n'.join(pages.get(p, '') for p in sorted(pages)[:4])
    out = {}
    m = re.findall(r'מהדורה\s+(?:מס[\'׳]?\s*)?([\w\.״"\'׳-]{1,12})', first)
    if m: out['edition'] = list(dict.fromkeys(m))[:3]
    m = re.findall(rf'(?:({MONTHS})\s*[,\-]?\s*)?((?:19|20)\d\d)', first)
    if m: out['dates'] = list(dict.fromkeys(' '.join(x for x in d if x) for d in m))[:5]
    m = re.findall(r'((?:משרד|מינהל|מנהל|הרשות|רשות|נתיבי|המועצה|אגף)\s[^\n]{2,50})', first)
    if m: out['publisher'] = list(dict.fromkeys(x.strip() for x in m))[:4]
    out['verify'] = 'candidates from text; confirm on cover page image'
    return out


def build(doc_dir):
    tf = os.path.join(doc_dir, 'text.md')
    if not os.path.exists(tf):
        return None
    pages = split_pages(open(tf, encoding='utf-8').read())
    if not pages:
        return None
    labels, heads, chapter, toc = {}, [], None, set()
    for p in sorted(pages):
        raw = re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', pages[p])
        lines = [l for l in raw.splitlines() if l.strip()]
        nums_only = sum(bool(re.fullmatch(r'\s*[\divxlcIVXLC]{1,4}\s*', l)) for l in lines)
        dotted = sum(bool(re.search(r'\.{4,}|…{2,}', l)) for l in lines)
        if re.search(r'תוכן\s*(ה)?עניינים|תוכן העניניים|רשימת (לוחות|איורים|תרשימים|טבלאות)', raw) or nums_only > 12 or dotted > 5:
            toc.add(p); continue
        for l in lines[:3] + lines[-3:]:  # printed page number: header/footer line
            m = LABEL.match(l)
            if m and not re.fullmatch(r'(19|20)\d\d', m.group(1)):
                labels[p] = re.sub(r'\s+', '', m.group(1)); break
        for l in lines:
            m = CHAPTER.match(l)
            if m and len(l.split()) <= 9 and not SENT_END.search(l) and not re.search(r'[,;()]', m.group(2)) and (not m.group(1).isdigit() or int(m.group(1)) <= 40):
                chapter = f'פרק {m.group(1)}' + (f' — {m.group(2).strip(" .|")}' if m.group(2).strip(' .|') else '')
                if not heads or heads[-1].get('chapter') != chapter or heads[-1]['num'] != m.group(1):
                    heads.append({'num': m.group(1), 'title': m.group(2).strip(' .|'), 'chapter': chapter, 'start': p, 'level': 0})
                continue
            m = HEAD_START.match(l) or HEAD_END.match(l)
            if not m:
                continue
            num, title = (m.group(1), m.group(2)) if m.re is HEAD_START else (m.group(2), m.group(1))
            if m.re is HEAD_END and '.' not in num:
                continue  # trailing single number = footnote / page ref, not a heading
            if not looks_heading(title) or int(num.split('.')[0]) > 40:
                continue
            chn = re.match(r'פרק (\d+)', chapter or '')
            if '.' in num and chn and num.split('.')[0] != chn.group(1):
                continue  # 3.2 inside chapter 16 = cross-reference or OCR noise
            if '.' not in num:
                prev = [h for h in heads if h['level'] == 1 and h['chapter'] == chapter]
                if prev and int(num) != int(prev[-1]['num']) + 1:
                    continue  # top-level numbers must run in order
            heads.append({'num': num, 'title': title.strip(' |-–.'), 'chapter': chapter, 'start': p, 'level': num.count('.') + 1})
    # drop TOC-page hits (many headings on one page) and keep the first occurrence of each number per chapter
    per_page = {}
    for h in heads: per_page[h['start']] = per_page.get(h['start'], 0) + 1
    seen, secs = set(), []
    for h in heads:
        key = (h['chapter'], h['num'], h['title'][:20])
        if per_page[h['start']] > 8 or key in seen:
            continue
        seen.add(key); secs.append(h)
    last = max(pages)
    for i, h in enumerate(secs):  # end = page before next heading of same or higher level
        nxt = next((s['start'] for s in secs[i + 1:] if s['level'] <= h['level']), last + 1)
        h['end'] = max(h['start'], nxt - 1 if nxt > h['start'] else h['start'])
    res = {'front': front_matter(pages), 'pages': labels, 'toc_pages': sorted(toc), 'sections': secs,
           'coverage': 'sections' if len(secs) >= 3 else 'page-only'}
    json.dump(res, open(os.path.join(doc_dir, 'sections.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    return res


def nearest_heading(pages, page, needle=None):
    """Scan back from the hit (or page end) for the closest numbered heading line; up to 6 pages back."""
    for p in range(page, max(0, page - 6), -1):
        lines = [l for l in re.sub(r'[\u200e\u200f\u202a-\u202e\u2066-\u2069]', '', pages.get(p, '')).splitlines() if l.strip()]
        if p == page and needle:
            idx = next((i for i, l in enumerate(lines) if needle in l), len(lines) - 1)
            lines = lines[:idx + 1]
        for l in reversed(lines):
            m = HEAD_START.match(l) or HEAD_END.match(l)
            if m:
                num, title = (m.group(1), m.group(2)) if m.re is HEAD_START else (m.group(2), m.group(1))
                if looks_heading(title) and (m.re is HEAD_START or '.' in num):
                    return {'num': num, 'title': title.strip(' |-–.'), 'page': p}
    return None


def cite(doc_dir, page, needle=None):
    """Citation for a PDF page (and optional quoted text): document, edition/date, chapter, section, pages, link, sha256."""
    meta = json.load(open(os.path.join(doc_dir, 'meta.json')))
    s = json.load(open(os.path.join(doc_dir, 'sections.json')))
    inner = [x for x in s['sections'] if x['start'] <= page <= x['end']]
    sec = max(inner, key=lambda x: (x['level'], x['start'])) if inner else None
    near = nearest_heading(split_pages(open(os.path.join(doc_dir, 'text.md'), encoding='utf-8').read()), page, needle)
    return {'doc': meta.get('title') or (meta.get('pdf_meta') or {}).get('Title'), 'url': meta['url'],
            'front': s['front'], 'chapter': sec and sec['chapter'], 'section': sec and f"{sec['num']} {sec['title']}",
            'nearest_heading': near, 'pdf_page': page, 'printed_page': s['pages'].get(str(page)) or s['pages'].get(page),
            'link': f"{meta['url'].split('#')[0]}#page={page}", 'asset': meta.get('asset'), 'sha256': meta.get('sha256')}


if __name__ == '__main__':
    if sys.argv[1:2] == ['--all']:
        with open(os.path.join(ROOT, 'sections.jsonl'), 'w', encoding='utf-8') as f:
            for d in sorted(glob.glob(os.path.join(ROOT, 'docs', '*'))):
                r = build(d)
                if r:
                    for s in r['sections']:
                        f.write(json.dumps({'id': os.path.basename(d), **s}, ensure_ascii=False) + '\n')
    elif sys.argv[1:2] == ['--cite']:
        print(json.dumps(cite(sys.argv[2], int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None), ensure_ascii=False, indent=1))
    else:
        r = build(sys.argv[1]); print(json.dumps({k: (v if k != 'sections' else v[:40]) for k, v in r.items()}, ensure_ascii=False, indent=1))
