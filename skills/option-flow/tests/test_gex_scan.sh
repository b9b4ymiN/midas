#!/usr/bin/env bash
# test_gex_scan.sh -- known-answer regression + gate + masking test.
# No network. Run from the repo root or from this skill's folder.
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL="$(dirname "$HERE")"
FIX="$HERE/fixture_vlo_20260818.json"
PASS=0; FAIL=0

ok(){ printf '  PASS  %s\n' "$1"; PASS=$((PASS+1)); }
no(){ printf '  FAIL  %s\n' "$1"; FAIL=$((FAIL+1)); }
chk(){ if [ "$2" = "$3" ]; then ok "$1"; else no "$1 (want $3, got $2)"; fi; }

echo "== option-flow tests =="

# ---- 1. known-answer regression against the real VLO chain ----
OUT="$(python3 "$SKILL/scripts/gex_scan.py" --snapshot "$FIX" --json 2>/dev/null)"
[ -n "$OUT" ] || { echo "  FAIL  scanner produced no output"; exit 1; }

read -r REGIME WALL NET TIER DTE <<EOF
$(printf '%s' "$OUT" | python3 -c '
import json,sys
d=json.load(sys.stdin); r=list(d.values())[0]
print(r["regime"], r["call_wall"], round(r["net_gex"]), r["tier"], r["dte_nearest"])')
EOF

chk "regime is STICKY"            "$REGIME" "STICKY"
chk "call wall at 350"            "$WALL"   "350.0"
chk "nearest expiry 3 DTE"        "$DTE"    "3"
chk "tier MED (stale prices)"     "$TIER"   "MED"

# net GEX within 2% of the hand-computed 7,054,414
python3 - "$NET" <<'PY'
import sys
got=float(sys.argv[1]); want=7_054_414
d=abs(got-want)/want
print(f"  {'PASS' if d<0.02 else 'FAIL'}  net GEX within 2% of hand-computed "
      f"({got:,.0f} vs {want:,} = {d:.3%})")
sys.exit(0 if d<0.02 else 1)
PY
[ $? -eq 0 ] && PASS=$((PASS+1)) || FAIL=$((FAIL+1))

# ---- 2. the risk-geometry check must fire on a stop inside the noise band ----
python3 "$SKILL/scripts/gex_scan.py" --snapshot "$FIX" --stop 337.50 2>/dev/null \
  | grep -q "SITS INSIDE" \
  && ok "stop inside noise band is flagged" \
  || no "stop inside noise band NOT flagged"

# ---- 2b. --spot pins the price used for regime math, chain still from --snapshot ----
# (writes to a temp file rather than piping straight into grep -q: on this
#  platform grep's early exit on match can race a large JSON write mid-flush)
SPOT_OUT="$(mktemp)"
python3 "$SKILL/scripts/gex_scan.py" --snapshot "$FIX" --spot 345 --json > "$SPOT_OUT" 2>/dev/null
grep -q '"spot": 345.0' "$SPOT_OUT" \
  && ok "--spot overrides the snapshot's own spot price" \
  || no "--spot did NOT override spot price"
grep -q '"gate": "PASS"' "$SPOT_OUT" \
  && ok "--spot override still clears the liquidity gate" \
  || no "--spot override unexpectedly failed the gate"
rm -f "$SPOT_OUT"

# ---- 3. masking test: sign must be isolated ----
if python3 "$SKILL/scripts/verify_sign.py" --fixture "$FIX" >/dev/null 2>&1; then
  ok "masking test (sign negates exactly, flip invariant)"
else
  no "masking test FAILED -- implementation bug, do not use output"
fi

# ---- 4. the gate must REFUSE a thin chain, not soften it ----
THIN="$(mktemp)"
python3 - "$THIN" <<'PY'
import json,sys
json.dump({"ticker":"THIN","spot":100.0,"chain":[
 {"strike":100,"T":0.05,"right":"call","open_interest":40,"implied_volatility":0.4},
 {"strike":105,"T":0.05,"right":"put","open_interest":30,"implied_volatility":0.4}]},
 open(sys.argv[1],"w"))
PY
TOUT="$(python3 "$SKILL/scripts/gex_scan.py" --snapshot "$THIN" 2>/dev/null)"
printf '%s' "$TOUT" | grep -q "UNRELIABLE" \
  && ok "thin chain returns UNRELIABLE" || no "thin chain NOT refused"
# assert on VALUES, not words -- the refusal text itself says "No regime, no walls"
printf '%s' "$TOUT" | grep -qE '\$[0-9]|per 1% move|STICKY|SLIPPERY' \
  && no "thin chain leaked a computed value (must emit refusal only)" \
  || ok "thin chain leaks no computed values"
rm -f "$THIN"

# ---- 5. disclaimer must be present in output and in SKILL.md ----
printf '%s' "$(python3 "$SKILL/scripts/gex_scan.py" --snapshot "$FIX" 2>/dev/null)" \
  | grep -q "Not financial advice" \
  && ok "disclaimer in runtime output" || no "disclaimer missing from output"
grep -q "Not financial advice" "$SKILL/SKILL.md" \
  && ok "disclaimer in SKILL.md" || no "disclaimer missing from SKILL.md"

echo
echo "  $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ] || exit 1
