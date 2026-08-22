# BF Citation and Claim Standard

## Where the claim label goes

Every material claim carries its certainty class. In v2 the class was written
inline, in brackets, inside the sentence. That kept traceability and cost
readability: a Thai paragraph with three bracketed tags in it is unreadable at
the speed anyone actually reads.

From v3 the class travels as a **marker**, and the evidence itself lives in
Appendix A.

**In the body** — a superscript class letter plus the entry id:

- `รายได้โต 18% เทียบปีก่อน` `F031`
- `ระยะเวลาคืนทุนของสาขาที่เปิดเต็มปีแล้วอยู่ราว 2.6 ปี` `D017`
- `ผู้บริหารตั้งเป้าเปิดเพิ่ม 300 สาขาใน 2 ปี` `M009`

Class letters: **F** fact · **D** derived · **M** management claim ·
**E** estimate or assumption · **I** inference · **X** market expectation ·
**U** unverified. Each class gets a colour that reads in both light and dark
themes, and the masthead carries the legend.

**In Appendix A** — the entry the marker points to:

| id | class | claim | source | locator | date | inputs / calculation |
|---|---|---|---|---|---|---|
| F031 | FACT | Revenue +18% YoY | FY2026 annual filing | p.42 | 2026-03-28 | — |
| D017 | DERIVED | Mature-store payback ≈ 2.6 years | store capex + mature store EBITDA | E-017, E-021 | 2026-08-21 | 4.1m ÷ 1.58m |
| M009 | MANAGEMENT_CLAIM | 300 openings in two years | Q2 FY2026 earnings call | 14:20 | 2026-05-09 | — |

**The exception.** Where the certainty class is the point the sentence is making,
write it out instead of marking it: "ตัวเลขนี้เป็นเป้าหมายที่ผู้บริหารพูดในการ
ประชุมนักวิเคราะห์ ยังไม่เคยปรากฏในงบการเงิน". A sentence that explains its own
uncertainty beats any tag, and this is the case that matters most.

## Rules

1. Major claims get an evidence marker; the marker resolves to a full entry.
2. Derived figures cite inputs and calculation logic in their appendix entry.
3. Management claims are never rewritten as facts.
4. Estimates state methodology and sensitivity when decision-relevant.
5. Conflicting sources are shown rather than silently reconciled.
5b. **Conflicting bases of the same metric are bridged once, in one place.**
   Rule 5 covers two sources disagreeing about one number. The commoner trap is
   one metric computed on two definitions — both correct, neither wrong, and
   the reader left unable to tell which answers their question. Where a metric
   appears on more than one basis, give it a single passage that states each
   basis, what each one answers, and which to use when. Do not let one figure
   headline the document while a different basis carries the argument.

   *Case:* the GULF report opened with ROCE 3.8% and argued from a ~7% return
   two paragraphs later. Both were right — 3.8% is EBIT-based and excludes
   associates; 7% is EBITDA-based and includes them — but nothing said so, and
   the gap between them turned out to be the thesis: it measures how much of
   the company's return comes from stakes rather than operations. A bridge was
   added; the discrepancy became the most useful paragraph in the section.
6. Primary sources outrank summaries where both cover the same factual claim.
7. Dates matter: show the point-in-time cutoff for historical validation, and
   carry it into the report's as-of date so the reader knows how old the
   verdict is.
8. No bracketed inline tag survives into the finished body. The marker form and
   the written-out exception above are the only two permitted shapes.

## Source notes

Appendix C should include source title, issuer/publisher, date, locator/URL where appropriate, evidence role, and claim ids used.

## Methodology provenance

When a conclusion materially depends on an external analytical framework (for example marginal-vs-average return, CAP, base rates, or young-company sales-to-capital logic), the report or methodology notes should identify the original framework source. Methodology citations do **not** substitute for company-specific evidence.
