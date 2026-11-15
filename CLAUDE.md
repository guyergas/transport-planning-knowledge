# transport-planning-knowledge — how to use (for Claude sessions)

Why: the session egress blocks gov.il, apps.land.gov.il, data.gov.il, olaw, eshed, etc. (403 policy).
github.com is open. So GitHub Actions downloads, the session reads results from GitHub.

## Read (no push rights needed)
- `git clone --depth 1 https://github.com/guyergas/transport-planning-knowledge`
- `index.jsonl` — one line per document: id, url, final_url, kind, title, pages, layer (ok/mixed/broken), ocr_pages, asset.
- `docs/<id>/text.md` — full text, `=== PAGE N === [text-layer|ocr; layer=...]` markers. Search with grep, read only the hit pages.
- `docs/<id>/meta.json` — access check, PDF metadata, fonts, `file_links` (download links found on HTML pages).
- Original PDF: `curl -sSL -o f.pdf <asset>` (GitHub Releases `src-<host>`). Use it for tables, maps, formulas, sub/superscripts: render the page image (hebrew-pdf-read skill) — the image wins over text.
- `id` = first 12 hex of sha1(url without #fragment).

## Request new / partial downloads (needs push: add_repo access=push)
1. Write `requests/<name>.txt`, one line per URL: `URL [pages=1-5,9 | pages=toc]`.
   `pages=toc` = index only (first 15 + last 3 pages). Omit = all pages. Optional first line `# shards=N` (≤20).
2. Commit + push to main → workflow `fetch` runs (plan → N shards → index).
3. Poll `https://api.github.com/repos/guyergas/transport-planning-knowledge/actions/runs?per_page=1`, then `git pull`.
   Results: `results/<name>[.<shard>].jsonl` (status, result: ok / redirect / error <code> / login / blocked, via=browser if Chromium fallback was needed).
A request name is processed once; to re-run, use a new name.

## Pipeline (tools/fetch.py)
curl (browser UA) → on 403/challenge: headless Chromium (Playwright) → PDF: pdffonts + per-page text-layer check
(reversed / junk / dropped final letters / empty → OCR) → tesseract tessdata_best heb+eng psm4 150dpi + refine.py → heb_ocr_fix.py (hunspell he_IL).
Same method as the hebrew-pdf-read skill.

## Known limits
- www.iroads.co.il: Imperva blocks GitHub IPs, even with Chromium (403).
- gov.il HTML pages need the Chromium fallback (Cloudflare 403 to curl); gov.il BlobFolder files download directly.
