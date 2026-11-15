"""Refresh sheet/records.jsonl + sheet/links.jsonl from the Google Sheet (run in a Claude session).

1. Google Sheets connector: get_spreadsheet(spreadsheetId=1ubQpGziTL6LNoqL6jo2JtkdN-w7MQmd8jc3Siuw75Qk,
   includeGridData=true, ranges=["רשומות!A1:F400","קישורים!A1:D2000"],
   fields=["sheets.properties.title","sheets.data.rowData.values.formattedValue"])
2. python3 tools/sheet_import.py <saved tool-result json>
3. commit sheet/ (the next run's index job joins it into index.jsonl)
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
d = json.load(open(sys.argv[1]))
d = d.get('content', d)
sh = {s['properties']['title']: [[c.get('formattedValue', '') for c in r.get('values', [])] for r in s['data'][0].get('rowData', [])] for s in d['sheets']}
os.makedirs(os.path.join(ROOT, 'sheet'), exist_ok=True)
with open(os.path.join(ROOT, 'sheet', 'records.jsonl'), 'w', encoding='utf-8') as f:
    for r in sh['רשומות'][1:]:
        if r and r[0]:
            r += [''] * (6 - len(r))
            f.write(json.dumps(dict(zip(['id', 'kind', 'number', 'title', 'section', 'status'], r)), ensure_ascii=False) + '\n')
with open(os.path.join(ROOT, 'sheet', 'links.jsonl'), 'w', encoding='utf-8') as f:
    for i, r in enumerate(sh['קישורים'][1:], start=2):
        if len(r) > 2 and r[2].startswith('http'):
            url = r[2]
            if '\\' in url:  # link with '(' split by the export: 'name_\\(part\\' | next cell 'rest.pdf) · notes'
                d = r[3] if len(r) > 3 else ''
                m = re.match(r'^\s*(\S*?\.(?:pdf|docx?|xlsx?))\)', d) or re.search(r'\s(\S*?\.(?:pdf|docx?|xlsx?))\)\s*$', d)
                url = url.replace('\\(', '(').replace('\\', '') + (')' + m.group(1) if m else '')
            f.write(json.dumps({'row': i, 'record': r[0], 'desc': r[1], 'url': url}, ensure_ascii=False) + '\n')
print('ok')
