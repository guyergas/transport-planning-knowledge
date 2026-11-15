# transport-planning-knowledge

Fetcher + text index for the Mokosai transport-planning knowledge map.

- `requests/*.txt`: URLs to fetch (`URL [pages=1-5,9]`). Push triggers `.github/workflows/fetch.yml`.
- `results/*.jsonl`: access check per URL.
- `docs/<id>/text.md`: text per page (`=== PAGE N ===`), OCR via tessdata_best heb+eng + hunspell fix.
- `index.jsonl`: one line per document. Original PDFs: Releases `src-<host>`.
