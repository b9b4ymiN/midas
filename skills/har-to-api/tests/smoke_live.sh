#!/usr/bin/env bash
# Run this on a machine with real outbound network to validate the
# stockanalysis profile before relying on it.
set -u

# Resolve the skill root from this script's own location, so it runs from
# anywhere — the repo root, the skill folder, or an absolute path. Relying on
# the caller's cwd meant every relative path broke the moment someone ran it
# the obvious way.
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)" || exit 1
SYM="${1:-TU}"; MKT="${2:-bkk}"
URL="https://stockanalysis.com/quote/${MKT}/${SYM}/financials/__data.json?x-sveltekit-trailing-slash=1"
echo "== 1. route reachable and returns JSON =="
python3 scripts/discover.py --url "$URL" --save "/tmp/${SYM}_raw.json" | head -40
echo
echo "== 2. same route WITHOUT the required query param (should NOT be JSON) =="
python3 scripts/discover.py --url "https://stockanalysis.com/quote/${MKT}/${SYM}/financials/__data.json" 2>&1 | head -4
echo
echo "== 3. now paste the suggested facts into profiles/stockanalysis.json, then: =="
echo "   python3 scripts/fetch.py ${SYM}.BK --market ${MKT} --profiles ./profiles"
echo "   python3 scripts/fetch.py ${SYM}.BK --use-snapshot \$(date +%F)   # must match exactly"
