# Future Compounder BF Report Template v4.0

## What changed in v4, and why

v3 fixed the shape and the voice. Two things it did not fix, both reported by the
same reader: the opening was capped at 2,000 characters, which forced the finding
into a summary that read like a specification rather than an article; and the
report ended at the verdict, so a reader who had just been told a business was
worth owning had nowhere to go with it.

v4 changes three things and leaves everything else alone:

- **The opening becomes an article.** 3,000–6,000 characters of continuous prose
  that a reader can finish instead of the report. No bullets, no question heading,
  no verdict table standing in for a paragraph. The spec is below.
- **Two movements are added after the verdict** — what the market thinks (§8) and,
  where the accumulation gate passed, how a position would be built (§9). Both draw
  on packs produced outside the core layers, and §9 appears only when it is earned.
- **The document gets a real HTML house style.** `design_system.md`,
  `report_template.html`, and `logos.md` ship with the skill; the report is no
  longer typeset from scratch each time.

## What changed in v3, and why

v2 mandated 25 numbered sections in a fixed order. That is the shape of an
analyst note, and it produced analyst notes: complete, traceable, and hard for
the person who commissioned them to act on. The reader complaint that drove this
rewrite was always the same — *"I finished it and I still don't know what to
do."*

v3 changes nothing about what evidence is required. Every v2 section survives;
the mapping table below shows where each one went. What changes is the shape and
the voice: **seven questions a reader actually asks, answered in order, with the
proving work moved to an appendix.**

The two published standards this template follows are recorded in
`research-foundations.md`: the SEC's *Plain English Handbook* (1998) for the
sentence-level rules, and the *Federal Plain Language Guidelines* (2011) for
question headings — "Question Headings are the most useful type of heading, but
only if you know what questions your audience would ask." We know them. They are
below.

---

## Who this is written for

One reader, not an audience. An intelligent adult who runs their own money, is
not an analyst, and has not read the filings. They can follow an argument; they
cannot decode vocabulary. Buffett's method, described in that handbook's own
preface — write the annual report imagining his sisters, "intelligent, but not
versed in accounting or finance" — is the standard here.

Two consequences:

- **Address that one person.** "คุณ" where it is natural; never "นักลงทุนควร
  พิจารณาว่า…". Singular, direct, second person.
- **A term the reader cannot define is a term the report has not delivered.**
  See Rule 3.

---

## The shape: seven questions, then an appendix

| # | The question | Thai form | Carries v2 sections |
|---|---|---|---|
| — | **Opening** — no heading | "สรุปให้ก่อน" | 1 |
| 1 | **What does this company actually sell, and to whom?** | เขาทำเงินจากอะไร? | 2 |
| 2 | **Where does the growth come from — a growing market, or share taken from someone else?** | การเติบโตมาจากไหน — ตลาดโต หรือแย่งของคนอื่นมา? | 3, 4, 5, 6, 7, 8 |
| 3 | **What does a new dollar put into this business earn?** | เงินที่ใส่เพิ่มไป ได้กำไรกลับมาเท่าไร? | 9, 10, 11, 12 |
| 4 | **How much room is left to put money in, and can they afford it?** | ยังมีที่ให้ใส่เงินอีกเท่าไร และหาเงินมาลงไหวไหม? | 13, 14, 16 |
| 5 | **What keeps returns this good from fading?** | อะไรทำให้กำไรดีแบบนี้อยู่ได้นาน? | 15, 17 |
| 6 | **If we are wrong, where are we wrong?** | ถ้าเราคิดผิด จะผิดตรงไหน? | 18, 19, 20 |
| 7 | **So what is the verdict, and when do we look again?** | สรุปแล้วได้เกรดอะไร และต้องกลับมาดูเมื่อไร? | 21, 22, 23 |
| 8 | **What does the market think of this business?** | ตลาดคิดยังไงกับธุรกิจนี้? | `stage_pack` (new in v4) |
| 9 | **If you were going to build a position, how?** | ถ้าจะเก็บ ควรเก็บยังไง? | `accumulation_pack` (new in v4, gated) |
| A–E | **Appendix** — the working | ภาคผนวก | 18 (table), 24, 25 |

The questions are the fixed part; the wording is not. Ask them in the report's
own language, in words that market's reader would use. The Thai column is the
form used for Thai-language reports and the one the movement specs below are
written against.

Seven questions are the argument; §8 and §9 sit after the verdict and answer what follows from it. Seven is the ceiling for the argument, not a quota. A movement with nothing decision-relevant to
say is dropped, and the ones that remain keep this order — it is the causal
order v2 protected: **scope → outside world → internal economics → runway →
duration → falsification → verdict.**

Sub-headings inside a movement are allowed and encouraged for scanning. They
follow Rule 1 like any other heading.

---

## What each movement must carry

### The article summary

**3,000–6,000 characters of continuous prose.** This is the part most readers will
read *instead of* the report, so it is written as an article, not as a form.

The v3 cap of 2,000 characters was wrong for one specific reason: at that length
the only way to fit five things was to state each in a sentence, which produced a
summary that read like a specification — accurate, complete, and impossible to care
about. The finding needs room to be explained, and a reader who understands the
argument in the first two minutes reads the rest better.

**The order of the telling**, which is a narrative order rather than a checklist:

1. What this company sells and who pays for it, in a way someone who has never
   heard of it can picture.
2. How the money machine actually works — the thing that makes this business
   different from a company that merely sells the same product.
3. The single strongest piece of evidence, with meaning before the number.
4. The thing most likely to break it, and the contradiction still unresolved.
5. The verdict, and — this is the part v3 lost — **which leg binds it**. "Strong
   but the runway is closing" is a different holding from "strong across the board".
6. What happens next. Where the gate blocked: the report stops, and the summary
   says so and says what would reopen it. Where it passed: the bands and the plan in
   two sentences, pointing to §9.

**Rules inside this block**, all stricter than in the movements:

- **No bullets.** A list here is the specification voice coming back.
- **No question heading.** Rule 1 governs the movements; the summary is prose and
  the masthead already says what it is. "สรุปให้ก่อน" is available if the layout
  needs a label.
- **No bracketed evidence tags**, and superscript markers used sparingly — this is
  the one place where flow beats traceability, and every figure here is repeated
  with its marker in the movement it belongs to.
- **First sentence of every paragraph carries the point.** Read only those six
  sentences: they must still be a complete, honest answer.
- **No term used before it is explained** (Rule 3), and the explanation happens in
  the sentence, not in a parenthesis stack.

If it runs past 6,000 characters, the movements are being duplicated. If it will
not reach 3,000, the finding is probably thinner than the report claims.

### 1 — What does this company actually sell, and to whom?
<!-- เขาทำเงินจากอะไร? -->

The Layer 0 frame in plain words: what the customer is buying and what job it
does for them, what the company is actually paid for today, and which parts of
the story are still only a plan. Carry the arena classes (`proven` / `emerging`
/ `option` / `narrative`) but say them as sentences — "ส่วนนี้ทำเงินอยู่จริง
วันนี้", "ส่วนนี้ยังเป็นแผน ยังไม่มีรายได้" — not as a taxonomy table in the
body. State the main alternative frame and why it was not chosen. Any
`SCOPE_CHALLENGE` goes here, not in a footnote.

### 2 — Where does the growth come from?
<!-- การเติบโตมาจากไหน — ตลาดโต หรือแย่งของคนอื่นมา? -->

The whole external system, because a reader who does not know where growth comes
from cannot judge whether it lasts. Cover, in whatever order the company's own
story demands: the demand regime and what causes it; who in the value chain
actually keeps the profit, and whether that is moving; the share mechanism — and
whether share was won or bought with price, capital, or acquisitions; the
decomposition of reported growth into category, share, and M&A without double
counting; whether new stores, channels, or countries add real demand or move it
around; and the promise → action → result record of what management said it
would do.

Any break in metric comparability is stated here, in the body, at the point the
affected number first appears — never quarantined in an appendix. A trend
computed across a definition change is not a trend, and the reader must learn
that before they believe the number, not after.

### 3 — What does a new dollar put into this business earn?
<!-- เงินที่ใส่เพิ่มไป ได้กำไรกลับมาเท่าไร? -->

The engine. Start from the economic unit — the one store, one yard, one
customer, one contract that the whole company is a repetition of — and follow
one unit's money: what it costs to build, what it earns, how long it takes to
pay back. Then the bridge from that unit up to the whole company and down to one
share, so the reader can see whether growth in the business actually reaches the
owner. Then the return on money already invested, beside the return on the
newest money — the second number is the one that matters, and where they differ,
say which direction the business is moving and why.

Where the accounting understates capital because research, brand, or customer
acquisition was expensed rather than capitalised, say so in words and show both
figures.

### 4 — How much room is left, and can they afford it?
<!-- ยังมีที่ให้ใส่เงินอีกเท่าไร และหาเงินมาลงไหวไหม? -->

Three questions the reader is really asking: how much more money can this
business absorb at those returns; is the company's actual behaviour with cash
consistent with that answer; and can it pay for the runway without breaking the
balance sheet or diluting the owner. Acquisitions get their own paragraph where
they are material — what was paid, what came back. Buybacks and issuance are
reported as their net effect per share, not as a list of corporate actions.

A young company with too little history uses the emerging bridge here, and the
report says plainly that a short record lowers how much we can *know*, not how
good the business *is*.

### 5 — What keeps returns this good from fading?
<!-- อะไรทำให้กำไรดีแบบนี้อยู่ได้นาน? -->

Duration. What actually stops a competitor from doing this, stated as a
mechanism rather than as the word "moat": pricing that customers accept without
leaving, customers who stay, density or scale a challenger would have to
replicate first, a regulatory or contractual position. Then the honest other
side: the reasons excess returns usually fade, and what the outside view says
about companies that have looked like this before. The base rate is a prior that
the company's evidence updates — never a verdict on its own.

### 6 — If we are wrong, where are we wrong?
<!-- ถ้าเราคิดผิด จะผิดตรงไหน? -->

The strongest opposing **reading** of evidence the reader has already seen — not
a second pass through the evidence.

Movements 2–5 established the facts. This movement's job is to read those same
facts the other way: the tailwind mistaken for skill, profit migrating out of the
company's link in the chain, share that was bought rather than won, new units
cannibalising old ones, a foreign market that will not replicate, the newest
capital earning less than the oldest, an allocator running out of ideas inside
the business, accounting flattering the return, governance taking a cut.

**Do not re-state figures already presented.** Cite where they live ("ตัวเลข
ผลตอบแทนที่นิ่งอยู่ในหัวข้อ 3") and spend the words on what those figures mean
if the bear is right. A counter-thesis that reads as a summary has not done its
work.

The reverse reality check closes the movement: what the business would have to do
— customers, units, capacity, share, revenue, margin, capital — for a 10x
outcome, and how far that is from what the engine can fund. It is a plausibility
check on the business, **not a valuation and not a price target.** The arithmetic
goes to Appendix B; the body carries the comparison and the verdict word.

Where the evidence ladder changes how much weight a claim deserves, say it here
in a sentence or two — "หลักฐานส่วนนี้ยังเป็นแค่คำอธิบาย ยังไม่มีตัวเลขระดับ
หน่วยธุรกิจมายืนยัน". The full ladder table is Appendix A.

### 7 — So what is the verdict, and when do we look again?
<!-- สรุปแล้วได้เกรดอะไร และต้องกลับมาดูเมื่อไร? -->

Four things: the verdict panel, the conditions that change it, the date, and
what is still unknown.

**The verdict panel** — see the spec below. A bare label is not a verdict.

**What would change this, both ways.** Kill conditions and upgrade conditions in
one place, from `kill_conditions` and `upgrade_conditions`. Each entry names a
metric, a direction, and a threshold, so a future filing can settle it. A section
with only kill conditions fails the template: a thesis that can only be
downgraded on evidence drifts downward with time regardless of what the business
does.

**When to look again** — see the review-schedule spec below. This is a required
part of the movement, not an optional footer. A verdict without a review date
silently claims to be true forever.

**What we still do not know.** Decision-relevant gaps, each with the source or
event that could close it, ordered by how much the verdict would move if it were
closed. A gap that would change nothing is not worth the reader's attention.

### 8 — What does the market think of this business?
<!-- ตลาดคิดยังไงกับธุรกิจนี้? -->

From `stage_pack`, and written for **every** company — including one the gate
blocked. What the market has concluded about a business you have just rejected is
still worth a section.

Two charts, monthly and weekly, each captioned with its interval, the moving
average the stage was judged against, the bar count, and whether the image was
captured or drawn. Then the cross-reading: the chart's stage beside the business
life-cycle stage, and what their agreement or disagreement means. Write it as a
sentence with dates in it — "the business is still reinvesting at high returns
while the chart has been in decline since March 2025" — never as a label.

The newest bar is excluded from the stage judgement until it closes, and the
section says so rather than leaving a reader to wonder why the stage does not match
this week's price. Where the newest closed bar already reads differently from the
confirmed stage, that pending change is stated: it is the earliest visible sign
that a multi-year phase is ending.

**What may not appear here:** an entry price, a stop, a target, an R-multiple, or
any instruction. The stage describes; it does not prescribe. A chart may never
revise a verdict — where the disagreement is severe enough to matter, that is a
`SCOPE_CHALLENGE` and the core layers re-run.

### 9 — If you were going to build a position, how?
<!-- ถ้าจะเก็บ ควรเก็บยังไง? -->

**This movement is gated.** It is written only when `accumulation_pack.gate` is
`PASSED`. Where it is `BLOCKED`, the movement carries the stop instead: what was
found, which condition failed, what would reopen it — each about the business
rather than about a lower price — and the review date. Nothing else: no band, no
staging, no size. A report that gives a rejected company a price to act on has done
harm, not analysis.

Where the gate passed, four parts in order:

**What the price is asking for.** The growth today's price already assumes, against
the growth the engine has shown it can deliver, both on the same nominal-or-real
basis. The required return is named as an assumption in the sentence that uses it,
with the range it was moved across. This is a comparison, not a valuation: no fair
value and no target price appears anywhere in the movement.

**What it would earn.** The ten-year return decomposed into business growth,
shareholder yield, and the change in the multiple, across three stated assumption
sets. The decomposition is the point — where most of the return comes from the
multiple rather than the business, say so in those words.

**The bands.** Three price ranges, each with the condition that defines it. The
condition column is not optional: a band without it has quietly become a target
price. Bands are reported with the sensitivity that produced them.

**The plan.** Conditional, always, and in parts rather than dates. Staging keys off
§8's alignment; the add, pause, and exit rules come from `upgrade_conditions`,
the data gaps, and `kill_conditions` — nothing new is invented here, which is what
makes the plan checkable a year later. A price move is not a kill condition.

The movement closes with the standing line that this is a conditional plan rather
than an instruction, and that it expires with the verdict.

---

## The verdict panel

Report the three axes separately and justify each. The panel is a table, not
three words in a paragraph — the opening's character cap exists to keep the
opening readable, and this is where the grading is shown in full.

| Element | From the thesis pack |
|---|---|
| The three axis labels | `compounding_potential` (with `potential_qualifier`), `evidence_maturity`, `confidence` |
| A row per leg | `leg_ratings` — incremental return, reinvestment capacity, duration, per-share translation, financial resilience, capital allocation |
| The binding leg, marked | `binding_leg` |
| The categorical reading | `compounder_class` |
| The growth figure the label was read from | `durable_growth`, with its window, on the **real** basis the band table uses |
| The two hurdle lines used | `hurdle_used`, with the basis |
| As of / next review / expires | `review_schedule.as_of`, `.next_review`, `.expires_on` |

Where the legs diverge, the qualifier and the binding leg are the most
decision-relevant things on the page: a reader who sees only "Strong" cannot tell
a business whose returns are excellent but whose runway is closing from one where
every leg is strong. Show the divergence.

Where `compounder_class` is `Great Business, Narrow Runway`, say what that means
in plain words — high returns on capital the business cannot absorb, so the
compounding is limited by opportunity rather than by quality.

---

## The review schedule

From `review_schedule` in the thesis pack. The reader must leave knowing three
things: **how old this verdict is, when it gets looked at again, and what would
make us look sooner.**

Present it as a short block, not as prose:

- **ข้อมูลถึงวันที่** — `as_of`. Everything below rests on evidence available on
  this date.
- **กลับมาดูอีกครั้ง** — `next_review`, with the event that makes that date the
  right one (`next_review_event`): a specific filing or result, not a calendar
  guess. Name which of the conditions above that event can settle (`settles`).
- **ทำไมถึงเป็นรอบนี้** — `cadence_basis`, one sentence. The cadence follows the
  fastest-moving evidence in the binding leg: a thesis bound by an annual capital
  budget is reviewed annually; one bound by monthly share data is not.
- **ดูก่อนกำหนดเมื่อ** — `watch_triggers`. Each names what it watches, what would
  be observable, and how long the question may stay open once it opens.
- **หมดอายุ** — `expires_on`. Past this date the verdict is stale: it may be read
  as history, but it may not carry a decision until the analysis is re-run.

This is borrowed wholesale from credit-rating surveillance, where the same
problem was solved decades ago: a rating is reviewed **at least annually**
whether or not there is news, and an unexpected event puts it on watch with a
bounded resolution window. Provenance in `research-foundations.md`.

---

## Writing rules

### Rule 1 — Every heading is a question the reader would ask

Not a framework name. The framework is how the work was done; it is not what the
reader came to find out.

| Banned heading | Write instead | Thai form |
|---|---|---|
| Evidence Ladder / บันไดหลักฐาน | How solid is the evidence here? | หลักฐานที่เรามีแน่นแค่ไหน? |
| Reverse Reality Check | What would the business have to do to grow 10x? | ถ้าจะโต 10 เท่า ธุรกิจต้องทำอะไรได้บ้าง? |
| Growth Decomposition | Which parts of the business produced that growth? | การเติบโตที่เห็น มาจากส่วนไหนบ้าง? |
| Micro → Corporate → Per-Share | Does the growth actually reach the owner? | กำไรที่โต ตกถึงผู้ถือหุ้นจริงไหม? |
| Evidence Maturity | Do we know enough about this yet? | เรารู้เรื่องนี้ดีพอหรือยัง? |
| Capital Allocation | What does management do with the cash? | ผู้บริหารเอาเงินไปทำอะไร? |
| Financial Resilience | Can the balance sheet pay for the plan? | งบดุลรับแผนนี้ไหวไหม? |

A framework name may still appear **inside** the text, once, where naming it
helps a reader who wants to look it up. It may not be a heading.

### Rule 2 — Meaning first, then the number

Start the sentence with what it means; land the number after. The number is
evidence for a claim, so the claim comes first.

*From the real CPRT report:*

- **Written as an analyst note:** "กำไรจากการดำเนินงานเพิ่มขึ้น 616.3
  ล้านดอลลาร์… คิดเป็นผลตอบแทนของเงินก้อนใหม่ราว 32%"
- **Written for a reader:** "ทุก 100 บาทที่บริษัทลงทุนเพิ่ม มันสร้างกำไรกลับมา
  ปีละ 32 บาท ซึ่งเท่ากับที่เงินก้อนเก่าทำได้ — บริษัทส่วนใหญ่พอโตขึ้นตัวเลขนี้
  จะตก แปลว่ายังไม่เจอเพดาน"

Same evidence, same precision, nothing softened. The difference is that the
second one tells the reader why they should care before it asks them to hold a
number in their head.

**The paragraph test:** the first sentence of every paragraph must carry the
point. Read a movement's heading, then read only the first sentence of each of
its paragraphs. If that does not answer the heading, the movement is not written
yet.

### Rule 3 — Explain a technical term in plain words at first use

In the sentence itself, in context — not in a glossary at the back, which the
reader will not turn to. After the first use, the short term may be used freely.

The table gives the Thai-report form. The rule is the same in any language: in an
English report, ROIC first appears as "return on invested capital — the profit
the business earns in a year against all the money tied up in it."

| Term | First-use form (Thai report) |
|---|---|
| ROIC | "ผลตอบแทนต่อเงินลงทุน — กำไรที่ได้ต่อปี เทียบกับเงินทั้งหมดที่จมอยู่ในธุรกิจ" |
| Incremental return / ROIIC | "ผลตอบแทนของเงินก้อนใหม่ — เงินที่เพิ่งลงไปรอบล่าสุดได้กำไรกลับมาเท่าไร ซึ่งมักไม่เท่ากับค่าเฉลี่ยของเงินก้อนเก่า" |
| Reinvestment rate | "สัดส่วนกำไรที่เอากลับไปลงทุนต่อ" |
| FCF | "เงินสดที่เหลือจริงหลังจ่ายค่าลงทุนแล้ว" |
| Moat | "สิ่งที่ทำให้คู่แข่งลอกเลียนไม่ได้ง่าย ๆ" |
| Cannibalization | "สาขาใหม่ไปกินยอดของสาขาเดิม ไม่ได้เพิ่มลูกค้าใหม่" |
| TAM | "ขนาดตลาดทั้งหมดที่เป็นไปได้ ซึ่งไม่ใช่ยอดขายที่บริษัทจะได้จริง" |
| Profit pool | "กำไรทั้งหมดในห่วงโซ่ธุรกิจนี้ และใครเป็นคนเก็บไป" |
| Base rate | "สถิติของบริษัทกลุ่มเดียวกันในอดีต ว่าโดยทั่วไปทำได้แค่ไหน" |
| Dilution | "หุ้นที่ออกเพิ่ม ทำให้กำไรต่อหุ้นของเจ้าของเดิมถูกหารมากขึ้น" |
| Working capital | "เงินที่ต้องจมไปกับสต็อกและลูกหนี้เพื่อให้ธุรกิจเดินได้" |

An abbreviation that appears fewer than three times in the whole report is not
worth introducing at all — write the words out.

### Rule 4 — Evidence markers go to the margin, not into the sentence

The claim labels are a strength of this pipeline and they stay. Their v2
*placement* was the problem: `[FACT: FY2026 filing, p.42]` in the middle of a
Thai sentence stops the reader mid-thought, and there were dozens of them per
page.

- **In the body:** a superscript marker carrying the class letter and the entry
  id — `F12`, `D07`, `M03` — linked to its entry in Appendix A. Class letters:
  **F** fact · **D** derived · **M** management claim · **E** estimate or
  assumption · **X** market expectation · **U** unverified. Give each class a
  colour that survives both light and dark themes, and put a legend in the
  masthead, so certainty is still visible at a glance without a click.
- **In Appendix A:** the full entry — the claim, the class, the source, the
  locator, the date, and for derived figures the inputs and the calculation.
- **Never in the body:** the bracketed inline form.
- **The exception:** when the certainty class *is* the point of the sentence, say
  it in words instead of marking it — "ตัวเลขนี้มาจากคำพูดของผู้บริหารในการ
  ประชุมนักวิเคราะห์ ยังไม่ปรากฏในงบการเงิน". That is clearer than any tag, and
  it is the case that matters most.

Nothing about traceability is relaxed. Every material number still reaches an
original source; the path is one click instead of one interruption.

### Rule 5 — If a passage proves rather than explains, it belongs in the appendix

The body says what is true and why it matters. The appendix shows the work. A
reader who trusts the argument never opens it; a reader who does not can check
every step.

Goes to the appendix by default: the reinvestment-rate annual series, the
incremental-return derivation, the per-share reconciliation, the reverse-reality
arithmetic, the full evidence ladder table, segment tables the argument does not
turn on, and methodology provenance.

Stays in the body: any number the argument turns on, any comparability break, and
any figure whose absence would let the reader believe something false.

### Rule 6 — One home per figure

A figure restated in more than three *body* movements is being repeated rather
than used. Give it one home and reference that movement elsewhere.

Two qualifications, both learned by getting this wrong on the GULF report:

- **Count distinct figures, not substrings.** A naive search made `3.3%` look
  like it appeared in five sections; three were `33.3%`, an unrelated number.
  `55,000` matched installed capacity in MW, an annual payment in THB, and the
  upper bound of an EBITDA range — three different quantities.
- **The appendix and the data-gap list do not count.** A citation and a named
  open question are supposed to restate the figure they concern.

Check before cutting: a figure doing different work in each place — framing in
movement 1, evidence in movement 3, a plausibility bound in movement 6 — is being
*used*, not repeated.

### Rule 7 — Sentence discipline

The SEC's six plain-English principles, adopted as written: active voice; short
sentences; definite, concrete, everyday words; tables for complex information; no
legal or highly technical jargon; no multiple negatives.

Two additions for this pipeline:

- **One idea per paragraph**, and paragraphs short enough to read on a phone.
- **Never state a ratio without the two things being compared.** "อัตรากำไร
  ขั้นต้น 38%" tells the reader nothing they can use; "จากรายได้ 100 บาท
  เหลือเป็นกำไรขั้นต้น 38 บาท ก่อนหักค่าใช้จ่ายสำนักงาน" is the same fact,
  usable.

---

## Appendices

| | Contents |
|---|---|
| **A — ตารางหลักฐาน** | Every marker in the body, in id order: claim, class, source, locator, date, and for derived figures the inputs and calculation. The evidence ladder table lives here. |
| **B — ตัวเลขและวิธีคำนวณ** | The working: reinvestment-rate series, incremental-return derivation, per-share reconciliation, reverse-reality arithmetic, hurdle-rate basis, the inflation basis for the real growth figure, and — where the gate passed — the price-implied expectations sensitivity grid and the band arithmetic. |
| **C — แหล่งข้อมูล** | Source title, issuer, date, locator/URL, evidence role, and the claim ids each supports. |
| **D — วิธีวิเคราะห์ที่ใช้** | Methodology provenance, only where a framework materially shaped the reading. Methodology citations never substitute for company evidence. |
| **E — ข้อจำกัด** | The standing disclaimer, in full. Also repeated in the page footer. |

---

## Presentation conventions

**Dates.** Pick one era and hold it for the whole document. A Thai-language
report uses Buddhist Era throughout; the only exceptions are URLs and the titles
of English-language sources, which are quoted verbatim. Mixing "21 ส.ค. 2026" in
a masthead with พ.ศ. 2569 in the body reads as an error because it is one.

**Print.** Apply `page-break-inside: avoid` to self-contained blocks — callouts,
tables, verdict panels — never to whole movements. A 2,600-character block that
refuses to break leaves most of a page empty.

**Figures.** `font-variant-numeric: tabular-nums` wherever digits are compared
down a column. Wide tables scroll inside their own container so the page body
never scrolls sideways.

**Navigation.** A sticky table of contents listing the movements. The reader should
be able to see the whole argument as a short list and jump to the one they care
about. On screens at or below 900px it collapses behind a fixed hamburger bar that
stays reachable however far the reader has scrolled.

**House style.** Do not typeset the report from scratch. `design_system.md` holds
the tokens and every component; `report_template.html` implements them as a fillable
scaffold with the movements, the appendices, the theme handling and the print rules
already in place; `logos.md` resolves the masthead logo. Copy the template and fill
it. The palette is green and stays green — re-theming a research document to a
company's brand colours tells the reader something untrue about its independence.

---

## Self-check before publishing

Answer these. A "no" is a rewrite, not a note.

1. Does every heading read as a question the reader would ask?
2. Read only the headings and the verdict panel — is that a complete, honest
   answer on its own?
3. Read only the first sentence of each paragraph in a movement — does it answer
   that movement's heading?
4. Is there a single technical term used before it is explained in plain words?
5. Is there a bracketed evidence tag left anywhere in the body?
6. Does the document say when it must be looked at again, and what would make
   that sooner?
7. Does the counter-thesis introduce a *reading*, or does it re-state figures?
8. Is there a passage in the body that exists to prove rather than to explain?
9. Could the reader trace any material number to an original source in one click?
10. Would the intended reader — intelligent, not an analyst — finish this knowing
    what they now believe, and what would change their mind?
11. Does the article summary read as an article — continuous prose, no bullets, no
    question heading — and does it land between 3,000 and 6,000 characters?
12. Is §9 present only because the gate passed, and absent — replaced by the stop —
    when it did not?
13. Is there a fair value, a target price, an upside percentage, or an imperative to
    buy or sell anywhere in the document?
14. Does every chart caption say whether the image was captured or drawn, and does
    every asset in the file start with `data:` rather than `http`?
15. On a 360px-wide screen: does the first viewport avoid sideways scrolling, does
    the table of contents start collapsed, does it open on the first tap, and does
    it close again?

---

_Research and educational output only. Not financial advice._
