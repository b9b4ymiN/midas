#!/usr/bin/env bash
set -u

# Resolve the skill root from this script's own location, so it runs from
# anywhere — the repo root, the skill folder, or an absolute path. Relying on
# the caller's cwd meant every relative path broke the moment someone ran it
# the obvious way.
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)" || exit 1
S=scripts/sensitivity.py; pass=0; fail=0
chk(){ if echo "$2" | grep -q -- "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }

TU=$(python3 $S --driver tuna --cost-share 0.55 --margin 0.0487 --move 0.10 \
     --pass-through 0.6 --revenue 135439918000 --lag-months 3 --currency THB 2>&1)
chk "p=0 drop equals cost-share x move (5.50pp)" "$TU" "5.50pp"
chk "stated 60% pass-through gives -2.29pp"      "$TU" "2.29pp"
chk "breakeven at zero pass-through is +9%"      "$TU" "passing on nothing:      +9%"
chk "breakeven at stated pass-through is +22%"   "$TU" "60% pass-through: +22%"
chk "lag is reported"                            "$TU" "3 month(s) out"
chk "currency impact shown"                      "$TU" "3,095"

# p=1: cost fully recovered, margin dilutes only
P1=$(python3 $S --driver x --cost-share 0.50 --margin 0.10 --move 0.10 --pass-through 1.0 2>&1)
chk "full pass-through barely moves margin"      "$P1" "9.52%"

# sanity guards
BAD=$(python3 $S --driver x --cost-share 1.5 --margin 0.1 --move 0.1 2>&1)
chk "cost share >1 warns"                        "$BAD" "outside (0, 1]"
R=$(python3 $S --driver x --cost-share 0.5 --margin 0.1 --move 0.1 --pass-through 2 2>&1); rc=$?
[ $rc -eq 2 ] && { echo "  PASS pass-through out of range exits 2"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"; exit $([ $fail -eq 0 ] && echo 0 || echo 1)
