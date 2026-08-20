from pathlib import Path
import re, sys
# The seven Future Compounder skills live directly under this root.
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'future-compounder': ['SKILL.md','references/pipeline-contract.md'],
    'business-identity-scope': ['SKILL.md','references/methodology-map.md','references/market-scope-classification.md'],
    'market-growth-intelligence': ['SKILL.md','references/methodology-router.md','references/research-foundations.md','references/growth-decomposition.md'],
    'business-economic-engine': ['SKILL.md','references/economic-unit-guide.md','references/evidence-ledger.md'],
    'reinvestment-runway': ['SKILL.md','references/reinvestment-methods.md','references/runway-methods.md','references/emerging-compounder.md'],
    'compounder-grill': ['SKILL.md','references/falsification-tests.md'],
    'compounder-bf-report': ['SKILL.md','references/report-template.md','references/citation-standard.md'],
}
errors=[]
for skill, files in EXPECTED.items():
    for rel in files:
        p=ROOT/skill/rel
        if not p.exists(): errors.append(f'MISSING {p.relative_to(ROOT)}')
    skillmd=ROOT/skill/'SKILL.md'
    if skillmd.exists():
        txt=skillmd.read_text(encoding='utf-8')
        if not txt.startswith('---\n'): errors.append(f'{skill}: missing YAML frontmatter')
        if not re.search(r'^name:\s*[a-z0-9-]+\s*$',txt,re.M): errors.append(f'{skill}: invalid/missing name')
        m=re.search(r'^description:\s*(.+)$',txt,re.M)
        if not m or not m.group(1).startswith('Use when'): errors.append(f'{skill}: description must start Use when')
        # SDO: descriptions should not disclose workflow sequencing.
        if m and any(w in m.group(1).lower() for w in ['then ', 'pipeline', 'first ', 'next ', 'workflow']):
            errors.append(f'{skill}: description leaks workflow')


# Directory/frontmatter name consistency
for skill in EXPECTED:
    p=ROOT/skill/'SKILL.md'
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        m=re.search(r'^name:\s*([a-z0-9-]+)\s*$',txt,re.M)
        if m and m.group(1) != skill:
            errors.append(f'{skill}: frontmatter name {m.group(1)} does not match directory')

# No placeholder language in deployable skill files
for p in (ROOT).rglob('*.md') if (ROOT).exists() else []:
    txt=p.read_text(encoding='utf-8')
    for marker in ['TBD','TODO','implement later','fill in details']:
        if marker.lower() in txt.lower(): errors.append(f'{p.relative_to(ROOT)}: placeholder {marker}')

# Contract-specific expectations once files exist
checks = {
 'business-identity-scope/SKILL.md':['business_identity_pack','PROVEN','EMERGING','OPTION','NARRATIVE','STOP'],
 'market-growth-intelligence/SKILL.md':['market_growth_pack','Metric Comparability','Growth Decomposition','incrementality','SCOPE_CHALLENGE','STOP'],
 'business-economic-engine/SKILL.md':['economic_engine_pack','Economic Unit','Micro','Corporate','STOP'],
 'reinvestment-runway/SKILL.md':['reinvestment_runway_pack','Incremental','Duration','Evidence Maturity','STOP'],
 'compounder-grill/SKILL.md':['Compounding Potential','Evidence Maturity','Confidence','Counter','STOP'],
 'compounder-bf-report/SKILL.md':['FACT','DERIVED','MANAGEMENT_CLAIM','Data Gaps','STOP'],
 'future-compounder/SKILL.md':['business-economic-engine','reinvestment-runway','compounder-grill','compounder-bf-report','DoD'],
}
for rel, terms in checks.items():
    p=ROOT/rel
    if p.exists():
        txt=p.read_text(encoding='utf-8')
        for term in terms:
            if term.lower() not in txt.lower(): errors.append(f'{rel}: missing contract term {term}')

# No major scoring as primary output
for p in (ROOT).glob('*/SKILL.md') if (ROOT).exists() else []:
    txt=p.read_text(encoding='utf-8').lower()
    if 'score 87/100' in txt or '100-point score' in txt:
        errors.append(f'{p.relative_to(ROOT)}: forbidden primary 100-point scoring')



# V2 Core contract requirements (TDD: expected to fail against v1 before production edits)
v2_checks = {
 'business-economic-engine/SKILL.md':[
    'Growth Architecture','per-share','intangible','scale economics'
 ],
 'reinvestment-runway/SKILL.md':[
    'capital allocation','acquisition','buyback','funding','financial resilience'
 ],
 'compounder-grill/SKILL.md':[
    'base rate','Evidence Ladder','reverse','per-share','scale economics'
 ],
 'future-compounder/SKILL.md':[
    'base rate','per-share','reverse','financial resilience'
 ],
 'compounder-bf-report/SKILL.md':[
    'Growth Architecture','per-share','Capital Allocation','base rate','Evidence Ladder','Reverse Reality'
 ],
}
for rel, terms in v2_checks.items():
    pp=ROOT/rel
    if pp.exists():
        tt=pp.read_text(encoding='utf-8')
        for term in terms:
            if term.lower() not in tt.lower():
                errors.append(f'{rel}: missing V2 core term {term}')


foundations=ROOT/'compounder-bf-report/references/research-foundations.md'
if foundations.exists():
    ft=foundations.read_text(encoding='utf-8')
    for term in ['https://','Concept used','Limitation','Publication date','Source role']:
        if term.lower() not in ft.lower():
            errors.append(f'research-foundations: missing provenance term {term}')

contract=ROOT/'future-compounder/references/pipeline-contract.md'
if contract.exists():
    ct=contract.read_text(encoding='utf-8')
    for field in [
        'business_identity_pack','market_growth_pack','metric_comparability','growth_decomposition',
        'growth_architecture','per_share_economics','intangible_capital',
        'scale_economics','capital_allocation','financial_resilience',
        'base_rate_context','evidence_ladder','reverse_reality_check'
    ]:
        if field not in ct:
            errors.append(f'pipeline-contract: missing V2 field {field}')


# Repo rule (AGENTS.md): every skill touching investing carries the standing disclaimer.
DISCLAIMER = 'Research and educational output only. Not financial advice.'
for skill in EXPECTED:
    p = ROOT/skill/'SKILL.md'
    if p.exists() and DISCLAIMER not in p.read_text(encoding='utf-8'):
        errors.append(f'{skill}: missing mandatory disclaimer')

if errors:
    print('FAIL')
    print('\n'.join(errors))
    sys.exit(1)
print(f'PASS: {len(EXPECTED)} Future Compounder skills validated')
