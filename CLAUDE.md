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

## The map (no Google Sheet any more)
The Google Sheet Transport_Planning_Records_Index and the guide doc Transport_Planning_Knowledge_Index were retired on 16.11.2026 (Guy).
This file is the only guide; the repo is the only source of truth. The project spec (Google Doc 1sLjsTAN_ESW3tVmxxfpehCXMSwnOcADuAySq8wXlW4Q,
sections 1 and 8) points here. When repo logic changes, update this file in the same commit.
- `sheet/records.jsonl` — 224 records: id ("שורה N" / "מקור נוסף NNN"), title, section, status (+ `status_note`, `status_checked` when reviewed against the repo).
- `sheet/links.jsonl` — every link of every record (record, desc, url; `replaced` = old URL + decision). Edit THIS file to add/fix links.
- `sheet/replacements.jsonl` — log of Guy's replacement decisions (old → new, kind, who/when).
- index.jsonl per doc joins these: `sheet_records`, `sheet_desc`, `edition_status`, `newer_in_record`; titles fall back to the record title; when several documents of one record would share it, the document's own link description is appended (`<record title> – <desc>`).
(`tools/sheet_import.py` is kept only for re-importing an old export.)

## Reference files (not documents)
- `reference/Eshed_Document_Audit.tsv` — audit of the Eshed catalog (id, type, title, publisher, date, edition, filters, record target, open result, pages). Moved from Drive (folder הנחיות תכנון, deleted 18.11.2026).

## Quality flags
- OCR pages: `conf=NN` in the page header (mean tesseract word confidence); `lowconf` if <75 → read from the page image.
  meta.json: `ocr_conf_mean`, `lowconf_pages`.
- Text-layer pages are bidi-repaired (`. word`, `(abc)`, `80 שניות`).
- HTML pages: `new_file_links` (vs last check) and `unknown_file_links` (not in sheet/requests) = possible new editions.
- Weekly run (and any request with `# report`) opens a GitHub Issue: not accessible / changed / new files / low confidence.

## Access status (rebuilt every run)
- `status.jsonl`: latest check per URL (result, http status, via=browser|wayback, server, sheet record + rows, checked date).
- `pending.md`: everything waiting for Guy (unresolved sheet links + reason + ranked candidates; decided ones marked "הוחלט — ממתין לעדכון הגיליון"). Guy answers in chat "שורה N → link".
- `inaccessible.jsonl`: map URLs (in sheet/links.jsonl) still not readable and with no stored copy, with the reason chain: curl → Chromium (`browser`) → Internet Archive (`archive`).
- Pacing: ≥6 s between gov.il hits per runner (others 1.5 s). On 403/429/503: retry after ~90 s, then ~240 s; then 60–90 s cool-down → Chromium. Waits never block a shard: the queue (run_queue) works on other hosts / OCR meanwhile → newest Wayback snapshot (`via: wayback`, result `ok (archive copy YYYYMMDD)` —
  cite it as an archive copy and prefer an official URL when one is found).
- 404/410 → gov.il language mirrors (`/he/`↔`/ar/`↔`/en/`↔`/ru/` in BlobFolder paths; result `ok (alternate /ar/)`, `alt_url`)
  → Internet Archive. 403 after Chromium → same mirrors → archive.
  Still nothing → `candidates`: files currently listed on the publication page gov.il/he/pages/<slug> (text + url);
  a session matches them to the sheet title and proposes the replacement to Guy (never auto-replaced).
- Sheet links split at "(" by the export (`name_\(part\` + rest in the next cell) are rejoined by `tools/sheet_import.py`.
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
- Link: fetched documents → official `url#page=N`; manual uploads (`source: manual upload`, e.g. Drive files) → the repo copy (Release asset) `#page=N`, original kept as `source`.
- Edition/date from text are candidates: confirm on the cover page image before stating them. Read the heading on the page itself when map and nearest heading disagree.

## National datasets (not documents)
Rule (Guy, 17.11.2026): every national dataset (not project-specific) lives here, never fetched by a project task directly.
Big data files (CSV/ZIP/PBF/XLSX) that projects clip locally — no OCR, no index, not in the map.
- Files behind a login (e.data.gov.il → Google sign-in) are detected; CKAN datastore resources fall back to `datastore_search` paging (CSV). `"mirrors"` = alternative URLs. Remove `"force"` after the run.
- Add: append a line to `data/sources.jsonl`: `{"name","title","page"}` + `"url"` (one file) or `"ckan"` (data.gov.il package; `"match"` regex on resource name/url; `"search"` words used if the package name is wrong → `candidates` in meta). Optional `"refresh_days"`, `"force": true`.
- Workflow `data`: on push of that file + weekly (Monday) for sources whose `refresh_days` passed.
- Result: Release `data-<name>` (latest file, same name each time) + `data/<name>/meta.json` (status, checked, bytes, sha256, zip file list, asset URL; for ckan: per resource).
- Project fetch tasks (spec section 15) download the asset and clip to the study area; never store national files in project folders. Record `checked` + `sha256` from meta.json as the source version. In reports, cite the ORIGINAL source (publisher, dataset, `url`/`page`, retrieval date, version), never the repo; links appear as short descriptive clickable text (Word hyperlink), never as a raw URL.
- Query services stay in the project task (area query, no national file): Open Bus Stride API, iplan ArcGIS, GovMap, street-imagery APIs (KartaView/Mapillary), Tiltan boardings, Civil Administration plans (J&S), orthophoto. Decided by Guy 18.11.2026: these are pulled per project, not stored here. Split of responsibility: this repo only fetches and refreshes national files; component A (the project fetch task) does everything else — clipping national files to the study area, area-query services, processing, saving to the project folder, report.
- Current: `tripscelular_1819` (cellular OD 2018–19 v1.3), `gtfs`, `cbs_accidents_puf`, `cbs_localities`, `osm_israel`, bicycle: `bike_infra_plan`, `bike_infra_exist`, `bike_ofneidan`, `bike_metrofan`, `bike_net_tlv`. Data dictionaries/reports (PDF) go through the normal document pipeline (requests/).

## Maintain the repo (needs push: add_repo owner=guyergas repo=transport-planning-knowledge access=push)
Every push below triggers workflow `fetch`; it ends with the `index` job (dedupe, sheet join, sections, search, Issue).
Poll `https://api.github.com/repos/guyergas/transport-planning-knowledge/actions/runs?per_page=1`, then `git pull`.

| Task | What to push |
|---|---|
| Add documents by URL | `requests/<new-name>.txt`, one line per URL: `URL [pages=1-5,9 \| pages=toc]` (toc = index only: first 15 + last 3 pages; omit = all). Header lines: `# shards=N` (≤20), `# force`, `# report`. Per line `render=1` = open in Chromium (JS-built pages, e.g. eshed document library). |
| Add a file you have (blocked site, login, attachment) | `inbox/<name>.pdf` + optional `inbox/<name>.url` (original URL or source note; the doc keeps that URL as its id and is never re-fetched weekly). Guy can drag it in on github.com (≤25MB). Stored in Release `src-inbox`, removed from inbox/. |
| Update / re-read a document | `requests/<new-name>.txt` with its URL and `# force` (otherwise unchanged bytes are skipped). Changed bytes are re-OCRed automatically, also weekly. |
| Replace a broken URL with a new one | edit the row in `sheet/links.jsonl` (new url + `replaced`), log it in `sheet/replacements.jsonl`, add the old URL to `removed.txt`. |
| Remove a document | add its URL or id to `removed.txt` (one per line, `#` comments). Docs + Release asset are deleted; never fetched again. |
| Add a record | append to `sheet/records.jsonl` (next free id) and its links to `sheet/links.jsonl`. |
| Re-check everything | automatic weekly (Sunday 01:17 UTC): every URL in `sheet/links.jsonl` minus `removed.txt` → `weekly-YYYY-MM-DD` + GitHub Issue. `sheet/links.jsonl` is the source of truth. |

Results: `results/<name>[.<shard>].jsonl` (status; result ok / redirect / error <code> / login / blocked; via=browser; change).
A request name is processed once; to re-run, use a new name. Never edit derived files (index.jsonl, sections, search.json).

## Pipeline (tools/fetch.py)
Excel workbooks (.xlsx) → one page per sheet, rows as `a | b | c` (openpyxl), original in Releases as `<id>.xlsx`; cell hyperlinks → `file_links` (same discovery as HTML pages).
A cut-off transfer (curl error with HTTP 200) counts as transient and is retried; a PDF with 0 pages never replaces the stored copy (`error (unreadable pdf)`).
curl (browser UA) → on 403/challenge: headless Chromium (Playwright) → PDF: pdffonts + per-page text-layer check
(reversed / junk / dropped final letters / empty → OCR) → tesseract tessdata_best heb+eng psm4 150dpi + refine.py → heb_ocr_fix.py (hunspell he_IL).
Same method as the hebrew-pdf-read skill.

## Known limits
- www.iroads.co.il: Imperva blocks GitHub IPs, even with Chromium (403).
- gov.il HTML pages need the Chromium fallback (Cloudflare 403 to curl); gov.il BlobFolder files download directly.
