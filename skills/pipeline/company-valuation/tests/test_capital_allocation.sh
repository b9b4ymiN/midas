#!/usr/bin/env bash
set -u
S=scripts/capital_allocation.py; pass=0; fail=0
chk(){ if echo "$2" | grep -q -- "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }
nchk(){ if echo "$2" | grep -q -- "$3"; then echo "  FAIL $1 (false positive)"; fail=$((fail+1)); else echo "  PASS $1"; pass=$((pass+1)); fi }

A=$(python3 $S --shares 4128,4110,4098,3980,3720 --years 2025,2024,2023,2022,2021 \
   --goodwill 12400,12500,4100,4050,4000 --total-assets 210000,205000,190000,188000,180000 \
   --roic 0.081,0.079,0.112,0.118,0.121 --related-party-purchases 8200 --cogs 109000 2>&1)
chk "dilution rate computed"           "$A" "2.64% a year"
chk "acquisition year detected"        "$A" "goodwill jumped 205% in 2024"
chk "ROIC fall flagged high"           "$A" "3.7 points"
chk "related party flagged"            "$A" "8% of cost of goods"

B=$(python3 $S --shares 3600,3700,3800,3900,4000 --years 2025,2024,2023,2022,2021 2>&1)
chk "buybacks reported as info"        "$B" "buybacks are"
nchk "buybacks not flagged as dilution" "$B" "being diluted"
chk "missing inputs listed"            "$B" "NOT ASSESSED"
chk "related party gap explains where to look" "$B" "notes to the financial statements"

C=$(python3 $S --shares 5000,4000,3500,3000,2500 2>&1)
chk "heavy dilution flagged high"      "$C" "HIGH"

D=$(python3 $S --goodwill 100,90 --total-assets 200 2>&1); rc=$?
[ $rc -eq 2 ] && { echo "  PASS mismatched series exits 2"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }
# related-party alone IS computable — it is one of the three metrics
E=$(python3 $S --related-party-purchases 100 --cogs 1000 2>&1); rc=$?
[ $rc -eq 0 ] && { echo "  PASS related-party alone is computable (exit 0)"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }
chk "and the other two are listed as not assessed" "$E" "share count series"
# genuinely nothing supplied
F=$(python3 $S 2>&1); rc=$?
[ $rc -eq 1 ] && { echo "  PASS no inputs at all exits 1"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"; exit $([ $fail -eq 0 ] && echo 0 || echo 1)
