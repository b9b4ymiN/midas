#!/usr/bin/env bash
# Regression tests for read_report.py. Run from the skill root.
set -u

# Resolve the skill root from this script's own location, so it runs from
# anywhere — the repo root, the skill folder, or an absolute path. Relying on
# the caller's cwd meant every relative path broke the moment someone ran it
# the obvious way.
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)" || exit 1
S=scripts/read_report.py; pass=0; fail=0
chk(){ if echo "$2" | grep -q "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }
nchk(){ if echo "$2" | grep -q "$3"; then echo "  FAIL $1 (false positive)"; fail=$((fail+1)); else echo "  PASS $1"; pass=$((pass+1)); fi }

C=$(python3 $S tests/fixture_clean.html 2>&1); rcC=$?
chk  "clean: reports no inconsistency"      "$C" "No internal inconsistencies"
nchk "clean: no price disagreement"         "$C" "PRICE_DISAGREE"
nchk "clean: no probability finding"        "$C" "PROB_"
nchk "clean: return % not read as a target" "$C" "TARGET_UNANCHORED"
[ $rcC -eq 0 ] && { echo "  PASS clean: exit 0"; pass=$((pass+1)); } || { echo "  FAIL clean exit=$rcC"; fail=$((fail+1)); }

B=$(python3 $S tests/fixture_broken.html 2>&1); rcB=$?
chk "broken: price disagreement across sections" "$B" "PRICE_DISAGREE"
chk "broken: probabilities do not sum to 100"    "$B" "PROB_SUM"
chk "broken: no scenario carries a majority"     "$B" "PROB_NO_VIEW"
chk "broken: target unanchored to fair value"    "$B" "TARGET_UNANCHORED"
chk "broken: target found from a TABLE cell"     "$B" "31.00"
chk "broken: dangling cross-reference"           "$B" "LINK_BROKEN"
chk "broken: missing sources"                    "$B" "NO_SOURCES"
chk "broken: missing as-of date"                 "$B" "NO_ASOF"
chk "broken: missing disclaimer"                 "$B" "NO_DISCLAIMER"
[ $rcB -eq 1 ] && { echo "  PASS broken: exit 1"; pass=$((pass+1)); } || { echo "  FAIL broken exit=$rcB"; fail=$((fail+1)); }

E=$(python3 $S tests/fixture_clean.html --extract 2>&1)
chk "extract: all 7 sections found"    "$E" '"s7"'
chk "extract: stat cards parsed"       "$E" '"label"'
chk "extract: table rows captured"     "$E" '"rows"'

M=$(python3 $S /nonexistent.html 2>&1); rcM=$?
[ $rcM -eq 2 ] && { echo "  PASS missing file: exit 2"; pass=$((pass+1)); } || { echo "  FAIL missing file exit=$rcM"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"
exit $([ $fail -eq 0 ] && echo 0 || echo 1)
