#!/usr/bin/env bash
# Regression tests for normalize.py. Run from the skill root.
set -u
S=scripts/normalize.py
pass=0; fail=0
chk(){ if echo "$2" | grep -q "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }

TU=$(python3 $S --ticker TU.BK --currency THB --years 2025,2024,2023,2022,2021 \
 --revenue 132718579000,138433059000,136152713000,155586350000,141047695000 \
 --op-margin 0.04595,0.05177,0.05018,0.05098,0.05828 \
 --net-margin 0.03473,0.03384,-0.10454,0.04395,0.05468 \
 --op-income 6098791000,7166649000,6831477000,7931680000,8219836000 \
 --net-income 4609416000,4684072000,-14233205000,6838003000,7712996000 \
 --current-revenue 135439918000 --current-op-income 6601235000 2>&1)
chk "TU: below-the-line distortion detected"  "$TU" "damage sat BELOW the operating line"
chk "TU: normalised op income ~6,966m"        "$TU" "6,966"
chk "TU: net-based base is far lower"         "$TU" "1,697"
chk "TU: growth gates fail"                   "$TU" "0/3"
chk "TU: readable unit is millions"           "$TU" "THB (millions)"

SC=$(python3 $S --ticker G --years a,b,c,d,e --revenue 300,240,180,130,100 \
 --op-margin .2,.19,.18,.17,.15 --current-revenue 320 2>&1)
chk "scale change disables method 1"          "$SC" "applicable: NO"

SH=$(python3 $S --ticker S --years a,b,c --revenue 100,105,98 --op-margin .1,.11,.09 --current-revenue 102 2>&1)
chk "short history warns"                     "$SH" "cover a full cycle"

DV=$(python3 $S --ticker D --years a,b,c,d,e --revenue 1000,1100,1050,900,950 \
 --op-income 100,121,105,72,95 --current-revenue 1050 2>&1)
chk "margins derived from absolutes"          "$DV" "9.80%"

BAD=$(python3 $S --ticker B --revenue 100,200 2>&1); rc=$?
chk "insufficient data errors out"            "$BAD" "need at least a revenue series"
[ $rc -eq 1 ] && { echo "  PASS exit code 1"; pass=$((pass+1)); } || { echo "  FAIL exit code"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"
exit $([ $fail -eq 0 ] && echo 0 || echo 1)
