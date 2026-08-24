from pathlib import Path
import re, sys
# The nine Future Compounder skills live directly under this root.
ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    'future-compounder': ['SKILL.md','references/pipeline-contract.md'],
    'business-identity-scope': ['SKILL.md','references/methodology-map.md','references/market-scope-classification.md'],
    'market-growth-intelligence': ['SKILL.md','references/methodology-router.md','references/research-foundations.md','references/growth-decomposition.md'],
    'business-economic-engine': ['SKILL.md','references/economic-unit-guide.md','references/evidence-ledger.md','references/life-cycle-stage.md'],
    'reinvestment-runway': ['SKILL.md','references/reinvestment-methods.md','references/runway-methods.md','references/emerging-compounder.md'],
    'compounder-grill': ['SKILL.md','references/falsification-tests.md','references/potential-rubric.md','references/confidence-rubric.md','references/hurdle-rates.md','references/reverse-reality-check.md'],
    'compounder-bf-report': ['SKILL.md','references/report-template.md','references/citation-standard.md','references/design_system.md','references/logos.md','references/report_template.html'],
    'compounder-stage-chart': ['SKILL.md','references/stage-classification.md','references/stage-business-alignment.md','references/chart-capture.md'],
    'compounder-accumulation-plan': ['SKILL.md','references/gate.md','references/price-implied-expectations.md','references/expected-return-math.md','references/accumulation-plan.md','references/research-foundations.md'],
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
        'base_rate_context','evidence_ladder','reverse_reality_check','review_schedule'
    ]:
        if field not in ct:
            errors.append(f'pipeline-contract: missing V2 field {field}')


# V3 report contract: the report is an article for one reader, and every verdict
# carries a review date. Both are enforced as terms so a rewrite cannot drop them.
v3_checks = {
 'compounder-bf-report/SKILL.md':[
    'plain words','review schedule','question','appendix'
 ],
 'compounder-bf-report/references/report-template.md':[
    'question','appendix','plain words','review schedule','as_of','next_review',
    'expires_on','watch_triggers','self-check'
 ],
 'compounder-bf-report/references/citation-standard.md':[
    'marker','Appendix A'
 ],
 'compounder-grill/SKILL.md':[
    'review_schedule','next_review','watch_triggers','expires_on','binding leg'
 ],
 'future-compounder/SKILL.md':[
    'review schedule'
 ],
}
for rel, terms in v3_checks.items():
    pp=ROOT/rel
    if pp.exists():
        tt=pp.read_text(encoding='utf-8')
        for term in terms:
            if term.lower() not in tt.lower():
                errors.append(f'{rel}: missing V3 report/review term {term}')
    else:
        errors.append(f'MISSING {rel}')

# The inline bracketed evidence tag is banned in body text from v3; the template
# and the citation standard may only name it to forbid it.
tmpl=ROOT/'compounder-bf-report/references/report-template.md'
if tmpl.exists():
    tt=tmpl.read_text(encoding='utf-8')
    if 'never in the body' not in tt.lower():
        errors.append('report-template: evidence markers must be banned from body text')


# V4 contract: price is admitted only after the verdict, the chart read is crossed with
# the business life cycle, the plan is gated, and the report is an article with a real
# HTML house style. Enforced as terms so a rewrite cannot quietly drop any of them.
v4_checks = {
 'compounder-stage-chart/SKILL.md':[
    'stage_pack','Stage Alignment','life-cycle','monthly','weekly','Weinstein',
    'no target price','STOP'
 ],
 'compounder-stage-chart/references/stage-classification.md':[
    'Stage 1','Stage 2','Stage 3','Stage 4','30-week','unclosed','stage_since'
 ],
 'compounder-stage-chart/references/stage-business-alignment.md':[
    'MARKET_HAS_NOT_PRICED_IT','MOVING_TOGETHER','LATE_AND_EXTENDED',
    'MARKET_SEES_DAMAGE_FIRST','life_cycle_stage'
 ],
 'compounder-stage-chart/references/chart-capture.md':[
    'TRADINGVIEW_MCP','RENDERED_SVG','base64','fallback'
 ],
 'compounder-accumulation-plan/SKILL.md':[
    'accumulation_pack','Expectation Gap','plan_archetype','conditional',
    'no target price','STOP'
 ],
 'compounder-accumulation-plan/references/gate.md':[
    'proven-compounder','emerging-starter','narrow-runway','BLOCKED','Not a Compounder'
 ],
 'compounder-accumulation-plan/references/price-implied-expectations.md':[
    'required return','sensitivity','durable_growth','Expectation Gap','UNRESOLVED'
 ],
 'compounder-accumulation-plan/references/expected-return-math.md':[
    'shareholder yield','multiple','scenario','per share'
 ],
 'compounder-accumulation-plan/references/accumulation-plan.md':[
    'Accumulation Band','kill_conditions','conditional plan','staging'
 ],
 'compounder-bf-report/SKILL.md':[
    'report_template.html','design_system.md','logo','mobile','article'
 ],
 'compounder-bf-report/references/report-template.md':[
    'article','stage','accumulation','gate'
 ],
 'compounder-bf-report/references/design_system.md':[
    '--accent','print','sticky','dark','article summary','verdict panel'
 ],
 'compounder-bf-report/references/logos.md':[
    'base64','fallback','monogram'
 ],
 'future-compounder/SKILL.md':[
    'compounder-stage-chart','compounder-accumulation-plan','gate'
 ],
 'future-compounder/references/pipeline-contract.md':[
    'stage_pack','accumulation_pack','plan_archetype','post-verdict'
 ],
}
for rel, terms in v4_checks.items():
    pp=ROOT/rel
    if pp.exists():
        tt=pp.read_text(encoding='utf-8')
        for term in terms:
            if term.lower() not in tt.lower():
                errors.append(f'{rel}: missing V4 term {term}')
    else:
        errors.append(f'MISSING {rel}')

# The report template is a real, fillable HTML scaffold — not prose about one. The
# mobile TOC script is the part that has broken before, so its shape is pinned here.
tpl=ROOT/'compounder-bf-report/references/report_template.html'
if tpl.exists():
    ht=tpl.read_text(encoding='utf-8')
    for term in ['<style','DOMContentLoaded','toc-toggle','@media print','prefers-color-scheme','data-theme']:
        if term.lower() not in ht.lower():
            errors.append(f'report_template.html: missing {term}')
    if 'src="http' in ht:
        errors.append('report_template.html: remote asset reference — the report must be self-contained')

# Provenance columns are required of every research-foundations file, not just the report's.
for rel in ['compounder-bf-report/references/research-foundations.md',
            'compounder-accumulation-plan/references/research-foundations.md']:
    fp=ROOT/rel
    if fp.exists():
        ft=fp.read_text(encoding='utf-8')
        for term in ['https://','Concept used','Limitation','Publication date','Source role']:
            if term.lower() not in ft.lower():
                errors.append(f'{rel}: missing provenance term {term}')

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
