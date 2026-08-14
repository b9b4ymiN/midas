#!/usr/bin/env bash
set -u
S=scripts/growth_decomp.py; pass=0; fail=0
chk(){ if echo "$2" | grep -q -- "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }

A=$(python3 $S --revenue 112000,100000 --years 2025,2024 --volume-growth -0.03 \
    --price-growth 0.09 --fx-growth 0.02 --acquisition-revenue 3000 2>&1)
chk "price-up-volume-down flagged as pass-through" "$A" "cost pass-through, not pricing power"
chk "fx contribution called out"                   "$A" "not earned"
chk "acquisition graded as bought"                 "$A" "bought"
chk "unexplained residual reported"                "$A" "unexplained"
chk "durable share computed"                       "$A" "durable share"

B=$(python3 $S --revenue 132718,138433,136153,155586,141048 --years 2025,2024,2023,2022,2021 2>&1)
chk "no components -> refuses to project"          "$B" "cannot be projected forward"
chk "erratic history warned"                       "$B" "growth is not established"
chk "CAGR reported"                                "$B" "CAGR"

C=$(python3 $S --revenue 100 2>&1); rc=$?
[ $rc -eq 1 ] && { echo "  PASS single period exits 1"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }
D=$(python3 $S --revenue abc 2>&1); rc=$?
[ $rc -eq 2 ] && { echo "  PASS unparseable exits 2"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"; exit $([ $fail -eq 0 ] && echo 0 || echo 1)
