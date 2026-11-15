#!/bin/sh
# Session setup: fetch search.db from the Release and verify it matches this checkout.
# Usage: sh tools/get_index.sh   -> prints the db path. Rebuilds locally if out of sync.
set -e
R=$(cd "$(dirname "$0")/.." && pwd)
DB=/tmp/tpk-search.db
want=$(python3 -c "import json;print(json.load(open('$R/search.json'))['sha256'])")
docs=$(python3 -c "import json;print(json.load(open('$R/search.json'))['docs_hash'])")
[ -s $DB ] && [ "$(sha256sum $DB | cut -d' ' -f1)" = "$want" ] || \
  curl -sSL -o $DB https://github.com/guyergas/transport-planning-knowledge/releases/download/search-index/search.db
have=$(python3 -c "import sys;sys.path.insert(0,'$R/tools');import search_index as s;print(s.docs_hash())")
if [ "$(sha256sum $DB | cut -d' ' -f1)" != "$want" ] || [ "$have" != "$docs" ]; then
  echo "search.db out of sync with docs/ -> rebuilding locally" >&2
  python3 "$R/tools/search_index.py" build $DB >/dev/null
  git -C "$R" checkout -q search.json 2>/dev/null || true   # keep repo manifest untouched
fi
echo $DB
