#!/usr/bin/env bash
set -u

# Resolve the skill root from this script's own location, so it runs from
# anywhere — the repo root, the skill folder, or an absolute path. Relying on
# the caller's cwd meant every relative path broke the moment someone ran it
# the obvious way.
cd "$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)" || exit 1
S=scripts/peer_impact.py; F=tests/fixture_peers.json; pass=0; fail=0
chk(){ if echo "$2" | grep -q -- "$3"; then echo "  PASS $1"; pass=$((pass+1)); else echo "  FAIL $1"; fail=$((fail+1)); fi }
nchk(){ if echo "$2" | grep -q -- "$3"; then echo "  FAIL $1 (false positive)"; fail=$((fail+1)); else echo "  PASS $1"; pass=$((pass+1)); fi }

A=$(python3 $S --candidates $F --margin 0.0487 --cost-share 0.55 --pass-through 0.6 --input-move 0.10 2>&1)
chk  "three-channel peer ranks first"          "$A" "1  Global tuna processor A"
chk  "vertical neighbour kept on supply alone" "$A" "Pet-food maker using marine protein E"
chk  "exposure weights by segment share"       "$A" "47.2%"
chk  "dropped list is printed"                 "$A" "CONSIDERED AND DROPPED"
chk  "drop reason carried through"             "$A" "same GICS sector and same country only"
chk  "missing drop reason warned"              "$A" "dropped with no reason recorded"
chk  "margin chain matches sensitivity.py"     "$A" "2.29pp"
chk  "attribution names supply peers only"     "$A" "supply-channel peers: Global tuna processor A, Pet-food maker"
chk  "valuation peer set disclaimed"           "$A" "NOT A VALUATION PEER SET"
nchk "no-channel candidates not kept"          "$A" "1  Domestic snack maker"

# no segment mix -> warns that ranking is meaningless
python3 - <<'PY'
import json
d=json.load(open('tests/fixture_peers.json')); d.pop('segments')
json.dump(d,open('/tmp/noseg.json','w'))
PY
B=$(python3 $S --candidates /tmp/noseg.json 2>&1)
chk "missing segment mix warned" "$B" "no segment mix supplied"

# margin math with no supply peer -> attribution warning
python3 - <<'PY'
import json
d=json.load(open('tests/fixture_peers.json'))
for c in d['candidates']:
    c['channels']=[x for x in c.get('channels',[]) if x!='supply']
json.dump(d,open('/tmp/nosupply.json','w'))
PY
C=$(python3 $S --candidates /tmp/nosupply.json --margin 0.05 --cost-share 0.5 --input-move 0.1 2>&1)
chk "margin without supply peer warns" "$C" "no candidate scored on the supply"

# nothing survives -> exit 1
python3 - <<'PY'
import json
d=json.load(open('tests/fixture_peers.json'))
for c in d['candidates']: c['channels']=[]
json.dump(d,open('/tmp/none.json','w'))
PY
D=$(python3 $S --candidates /tmp/none.json 2>&1); rc=$?
[ $rc -eq 1 ] && { echo "  PASS nothing survives exits 1"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }
chk "and says so rather than printing an empty table" "$D" "competitor whose actions reach its margin"

E=$(python3 $S --candidates /nonexistent.json 2>&1); rc=$?
[ $rc -eq 2 ] && { echo "  PASS missing file exits 2"; pass=$((pass+1)); } || { echo "  FAIL exit=$rc"; fail=$((fail+1)); }

echo; echo "passed $pass, failed $fail"; exit $([ $fail -eq 0 ] && echo 0 || echo 1)
