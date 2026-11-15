# transport-planning-knowledge — how to use (for Claude sessions)

Why: the session egress blocks gov.il, apps.land.gov.il, data.gov.il, olaw, eshed, etc. (403 policy).
github.com is open. So GitHub Actions downloads, the session reads results from GitHub.

## Start here: one command
`python3 tools/ask.py "<question words>" [-n 8] [--doc <id>] [--json]` → per hit: document (sheet title) · sheet record ·
chapter · section · printed page · PDF page · `URL#page=N` · warnings (table/figure → image, low OCR conf, older edition,
newer doc in record) · snippet. Then read the hit pages (and the page image when warned) and answer with the citation.

## Read (no push rights needed)
- `git clone --depth 1 https://github.com/guyergas/transport-planning-knowledge`
- `index.jsonl` — one line per document: id, url, final_url, kind, title, pages, layer (ok/mixed/broken), ocr_pages, asset.
- `docs/<id>/text.md` — full text, `=== PAGE N === [text-layer|ocr; layer=...]` markers. Search with grep, read only the hit pages.
- `docs/<id>/meta.json` — access check, PDF metadata, fonts, `file_links` (download links found on HTML pages).
- Original PDF: `curl -sSL -o f.pdf <asset>` (GitHub Releases `src-<host>`). Use it for tables, maps, formulas, sub/superscripts: render the page image (hebrew-pdf-read skill) — the image wins over text.
- `id` = first 12 hex of sha1(url without #fragment).

## Search (fast full-text, Hebrew-aware)
`DB=$(sh tools/get_index.sh)` then `SEARCH_DB=$DB python3 tools/search_index.py q "עיכוב בקרה" [-n 20] [--doc <id>]`
→ hits: id, PDF page, method (text-layer/ocr), title, snippet, `URL#page=N`. Then cite (below).
- search.db = SQLite FTS5, one row per page; Release `search-index`. `search.json` = manifest (sha256, docs_hash, source_commit).
- get_index.sh verifies sha256 + docs_hash against this checkout; on mismatch rebuilds locally (never uses a stale index).
- Page flags in `=== PAGE N === [...; image; table]`. Text-layer pages with pictures get an extra
  `--- figure-ocr ---` block (labels inside images, dictionary-filtered); OCR pages with tables get `--- table-ocr psm6 ---`.
  A hit there is marked "figure/table: read the page image" — values/labels must be confirmed on the image.
- Words match without prefix letters (ו ה ב כ ל מ ש) and with final letters folded.

## Link to the Google Sheet (Transport_Planning_Records_Index)
`sheet/records.jsonl` + `sheet/links.jsonl` = export of tabs רשומות / קישורים (refresh: `tools/sheet_import.py`, steps inside).
index.jsonl per doc: `sheet_records` (id, title, section, status), `sheet_desc`, `sheet_rows` (row numbers in קישורים), `year`,
`edition_status` (newer/older ONLY when the sheet text says so; null = not stated), `newer_in_record`. Titles fall back to the sheet title.

## Quality flags
- OCR pages: `conf=NN` in the page header (mean tesseract word confidence); `lowconf` if <75 → read from the page image.
  meta.json: `ocr_conf_mean`, `lowconf_pages`.
- Text-layer pages are bidi-repaired (`. word`, `(abc)`, `80 שניות`).
- HTML pages: `new_file_links` (vs last check) and `unknown_file_links` (not in sheet/requests) = possible new editions.
- Weekly run (and any request with `# report`) opens a GitHub Issue: not accessible / changed / new files / low confidence.

## Access status (rebuilt every run)
- `status.jsonl`: latest check per URL (result, http status, via=browser|wayback, server, sheet record + rows, checked date).
- `inaccessible.jsonl`: URLs still not readable, with the reason chain: curl → Chromium (`browser`) → Internet Archive (`archive`).
- Pacing: ≥6 s between gov.il hits per runner (others 1.5 s). On 403/429/503: retry after ~90 s, then ~240 s; then 60–90 s cool-down → Chromium → newest Wayback snapshot (`via: wayback`, result `ok (archive copy YYYYMMDD)` —
  cite it as an archive copy and prefer an official URL when one is found).
- Still blocked → in a session: WebSearch the document title for another official/mirror copy → add it as a request;
  else ask Guy for the file → `inbox/`.

## No duplicates
One document = one id. The index job folds ids with the same sha256 (or, for HTML, the same final URL) into the
smallest id: the others keep only meta.json with `duplicate_of`, their URLs go to the canonical `aliases`,
their Release asset is deleted, and they are skipped by index.jsonl / sections / search.
Different editions (different bytes) are separate documents on purpose.

## Sync rule
All derived data (index.jsonl, docs/*/sections.json, sections.jsonl, search.db + search.json) is rebuilt from docs/ by the
`index` job at the end of EVERY run, in one commit. Never edit derived files by hand.

## Citations (every guideline you quote must carry one)
`python3 tools/sections.py --cite docs/<id> <pdf_page> "<quoted words>"` →
document · front (edition/date/publisher candidates) · chapter · section (map + nearest heading above the quote) · printed page · PDF page · link `URL#page=N` · asset · sha256.
- `docs/<id>/sections.json`: section map (heuristic; `coverage: page-only` when no reliable numbering). `sections.jsonl`: all docs.
- Edition/date from text are candidates: confirm on the cover page image before stating them. Read the heading on the page itself when map and nearest heading disagree.

## Maintain the repo (needs push: add_repo owner=guyergas repo=transport-planning-knowledge access=push)
Every push below triggers workflow `fetch`; it ends with the `index` job (dedupe, sheet join, sections, search, Issue).
Poll `https://api.github.com/repos/guyergas/transport-planning-knowledge/actions/runs?per_page=1`, then `git pull`.

| Task | What to push |
|---|---|
| Add documents by URL | `requests/<new-name>.txt`, one line per URL: `URL [pages=1-5,9 \| pages=toc]` (toc = index only: first 15 + last 3 pages; omit = all). Header lines: `# shards=N` (≤20), `# force`, `# report`. Per line `render=1` = open in Chromium (JS-built pages, e.g. eshed document library). |
| Add a file you have (blocked site, login, attachment) | `inbox/<name>.pdf` + optional `inbox/<name>.url` (original URL or source note). Guy can drag it in on github.com (≤25MB). Stored in Release `src-inbox`, removed from inbox/. |
| Update / re-read a document | `requests/<new-name>.txt` with its URL and `# force` (otherwise unchanged bytes are skipped). Changed bytes are re-OCRed automatically, also weekly. |
| Replace a broken URL with a new one | add the new URL (request), add the old URL to `removed.txt`, update the sheet, then refresh `sheet/` (below). |
| Remove a document | add its URL or id to `removed.txt` (one per line, `#` comments). Docs + Release asset are deleted; never fetched again. |
| Refresh the sheet link | `tools/sheet_import.py` (steps inside) → commit `sheet/`. |
| Re-check everything | automatic weekly (Sunday 01:17 UTC) → `weekly-YYYY-MM-DD` + GitHub Issue report. |

Results: `results/<name>[.<shard>].jsonl` (status; result ok / redirect / error <code> / login / blocked; via=browser; change).
A request name is processed once; to re-run, use a new name. Never edit derived files (index.jsonl, sections, search.json).

## Pipeline (tools/fetch.py)
curl (browser UA) → on 403/challenge: headless Chromium (Playwright) → PDF: pdffonts + per-page text-layer check
(reversed / junk / dropped final letters / empty → OCR) → tesseract tessdata_best heb+eng psm4 150dpi + refine.py → heb_ocr_fix.py (hunspell he_IL).
Same method as the hebrew-pdf-read skill.

## Known limits
- www.iroads.co.il: Imperva blocks GitHub IPs, even with Chromium (403).
- gov.il HTML pages need the Chromium fallback (Cloudflare 403 to curl); gov.il BlobFolder files download directly.
