#!/usr/bin/env python3
"""
read_report.py — read a finished BF-Report and check whether it agrees with
itself, before anyone argues about whether it is right.

Why this exists
---------------
stock-grill used to consume "the output of five skills", which in practice
meant whatever was still in context. Reading the report file instead has two
consequences. The obvious one: you attack the document that will actually be
acted on, rather than a remembered version of it. The less obvious one, and the
reason for this script: once the input is a single file with a fixed section
structure, a whole class of error becomes mechanically checkable — the report
contradicting itself.

That class is worth catching first because it is invisible from inside. A
scenario target that quietly ignores the fair value two sections above it, a
current price that differs between the valuation and the technical read because
they were fetched an hour apart, probabilities that do not sum to 100 — none of
these are wrong opinions. They are wrong arithmetic, and arguing about the
thesis on top of them wastes the argument.

What it does NOT do: judge whether the thesis is any good. That is R1-R5, and
it needs a reader. This is R0.

stdlib only.

Usage
-----
  read_report.py TU_BF-Report.html                 # R0 checks, human readable
  read_report.py report.html --extract             # structured JSON for the grill
  read_report.py report.html --json                # checks as JSON
  read_report.py report.html --currency THB

Exit codes: 0 clean, 1 findings, 2 unreadable.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser
from typing import Any, Dict, List, Optional, Tuple

SECTION_NAMES = {
    "s1": "Business & Narrative",
    "s2": "Financial Dashboard",
    "s3": "Valuation",
    "s4": "Earnings & Sentiment",
    "s5": "Technical Timing",
    "s6": "Scenarios & Investment Plan",
    "s7": "Key Risks",
}

# Numbers that read as money: 1,234.56 / ฿1,234 / $1,234 / 1234
MONEY_RE = re.compile(r"[฿$€£¥]?\s?\d{1,3}(?:,\d{3})*(?:\.\d+)?|\b\d+\.\d+\b")
PCT_RE = re.compile(r"(-?\d{1,3}(?:\.\d+)?)\s?%")
# A number carrying a currency mark. Needed because "+55%" and "฿55.00" both
# reduce to 55 once the symbols are stripped, and reading a return figure as a
# price target produced a confident, wrong finding on a correct report. The
# house style requires every figure to carry its unit, so the mark is a
# reliable discriminator when it is present.
CURRENCY_NUM_RE = re.compile(r"[฿$€£¥]\s?(\d{1,3}(?:,\d{3})*(?:\.\d+)?)")
# Any number immediately followed by a percent sign, so it can be subtracted
# from the price candidates when no currency marks exist at all.
PCT_NUM_RE = re.compile(r"(-?\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s?%")

PRICE_LABEL_RE = re.compile(r"current price|ราคาปัจจุบัน|last price|spot", re.I)
FV_LABEL_RE = re.compile(r"fair value|มูลค่าที่เหมาะสม|intrinsic value", re.I)
PROB_LABEL_RE = re.compile(r"prob|ความน่าจะเป็น|weight", re.I)
SCENARIO_RE = re.compile(r"\b(bull|base|bear)\b|กรณีดี|กรณีฐาน|กรณีแย่", re.I)


class ReportParser(HTMLParser):
    """Walks the document, keeping track of which numbered section we are in.

    Deliberately tolerant: a report that has been hand-edited, translated, or
    built from an older template must still parse. Anything it cannot find is
    reported as not-found rather than assumed.
    """

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.sections: Dict[str, Dict[str, Any]] = {}
        self.current = "head"
        self._stack: List[Tuple[str, Dict[str, str]]] = []
        self._text: List[str] = []
        self.stats: List[Dict[str, str]] = []
        self._stat: Optional[Dict[str, str]] = None
        self._stat_field: Optional[str] = None
        self.anchors: set = set()
        self.links: List[str] = []
        self.tables: List[List[List[str]]] = []
        self._table: Optional[List[List[str]]] = None
        self._row: Optional[List[str]] = None
        self._cell: Optional[List[str]] = None
        self.title = ""
        self._in_title = False

    # -- helpers
    def _cls(self, attrs: Dict[str, str]) -> str:
        return attrs.get("class", "") or ""

    def handle_starttag(self, tag, attrs_list):
        attrs = dict(attrs_list)
        self._stack.append((tag, attrs))
        aid = attrs.get("id")
        if aid:
            self.anchors.add(aid)
            if re.fullmatch(r"s\d+", aid):
                self.current = aid
                self.sections.setdefault(aid, {"text": [], "numbers": [], "pcts": []})
        if tag == "title":
            self._in_title = True
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.links.append(attrs["href"][1:])
        cls = self._cls(attrs)
        if tag == "div" and "stat" in cls.split():
            self._stat = {"section": self.current, "value": "", "label": "", "delta": ""}
        if self._stat is not None and tag == "div":
            c = cls.split()
            if "v" in c:
                self._stat_field = "value"
            elif "k" in c:
                self._stat_field = "label"
            elif "d" in c:
                self._stat_field = "delta"
        if tag == "table":
            self._table = []
        if tag == "tr" and self._table is not None:
            self._row = []
        if tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        if tag in ("td", "th") and self._cell is not None and self._row is not None:
            self._row.append(" ".join("".join(self._cell).split()))
            self._cell = None
        if tag == "tr" and self._row is not None and self._table is not None:
            if any(c for c in self._row):
                self._table.append(self._row)
            self._row = None
        if tag == "table" and self._table is not None:
            if self._table:
                self.tables.append({"section": self.current, "rows": self._table})
            self._table = None
        if tag == "div":
            if self._stat_field:
                self._stat_field = None
            elif self._stat is not None:
                # closing the .stat wrapper
                if self._stat.get("value") or self._stat.get("label"):
                    self.stats.append(self._stat)
                self._stat = None
        if self._stack:
            self._stack.pop()

    def handle_data(self, data):
        if self._in_title:
            self.title += data
            return
        txt = data.strip()
        if not txt:
            return
        if self._cell is not None:
            self._cell.append(data)
            return
        if self._stat is not None and self._stat_field:
            self._stat[self._stat_field] += txt
            return
        sec = self.sections.setdefault(
            self.current, {"text": [], "numbers": [], "pcts": []}
        )
        sec["text"].append(txt)


def _num(s: str) -> Optional[float]:
    s = re.sub(r"[฿$€£¥,\s]", "", s)
    try:
        return float(s)
    except ValueError:
        return None


def extract(html: str) -> Dict[str, Any]:
    p = ReportParser()
    p.feed(html)
    out: Dict[str, Any] = {
        "title": " ".join(p.title.split()),
        "sections_found": sorted(k for k in p.sections if re.fullmatch(r"s\d+", k)),
        "sections_expected": sorted(SECTION_NAMES),
        "stats": p.stats,
        "tables": p.tables,
        "anchors": sorted(p.anchors),
        "internal_links": sorted(set(p.links)),
        "placeholders": [],
    }
    # unfilled template markers are worth catching before anything else
    for m in re.findall(r"\[[a-zA-Z฿$][^\]\n]{0,60}\]", html):
        out["placeholders"].append(m)
    out["placeholders"] = sorted(set(out["placeholders"]))[:40]
    if "<!-- FILL" in html:
        out["fill_markers"] = html.count("<!-- FILL")
    # Table cells are captured into `tables`, not into the section's prose, so
    # a section's numbers must be gathered from both. Scenario targets live in
    # a table in every real report — reading only the prose meant the
    # target-vs-fair-value check silently never fired.
    table_text: Dict[str, List[str]] = {}
    for t in p.tables:
        table_text.setdefault(t["section"], []).extend(
            cell for row in t["rows"] for cell in row
        )

    for sid, sec in p.sections.items():
        if not re.fullmatch(r"s\d+", sid):
            continue
        prose = " ".join(sec["text"])
        blob = prose + " " + " ".join(table_text.get(sid, []))
        sec["numbers"] = [n for n in (_num(x) for x in MONEY_RE.findall(blob)) if n is not None]
        sec["pcts"] = [float(x) for x in PCT_RE.findall(blob)]
        money = [n for n in (_num(x) for x in CURRENCY_NUM_RE.findall(blob)) if n is not None]
        if money:
            sec["money"] = money
            sec["money_basis"] = "currency-marked"
        else:
            pcts = {n for n in (_num(x) for x in PCT_NUM_RE.findall(blob)) if n is not None}
            sec["money"] = [n for n in sec["numbers"] if n not in pcts]
            sec["money_basis"] = "percent-excluded (no currency marks found)"
        sec["chars"] = len(prose)          # prose only — a table is not narrative
        sec["table_cells"] = len(table_text.get(sid, []))
        sec.pop("text", None)
    out["sections"] = {k: v for k, v in p.sections.items() if re.fullmatch(r"s\d+", k)}
    return out


# --- R0 checks --------------------------------------------------------------

def _finding(sev: str, code: str, msg: str, evidence: Any = None) -> Dict[str, Any]:
    f = {"severity": sev, "code": code, "message": msg}
    if evidence is not None:
        f["evidence"] = evidence
    return f


def check(html: str, ex: Dict[str, Any], tol_pct: float) -> List[Dict[str, Any]]:
    F: List[Dict[str, Any]] = []

    # 1. unfilled template
    if ex.get("fill_markers"):
        F.append(_finding("high", "UNFILLED",
                          f"{ex['fill_markers']} <!-- FILL --> marker(s) left in the document",
                          None))
    ph = [p for p in ex["placeholders"] if re.search(r"\[(฿|\$)?0|placeholder|TICKER|date\]", p, re.I)]
    if ph:
        F.append(_finding("high", "PLACEHOLDER",
                          "template placeholders still present — the report was not fully filled",
                          ph[:8]))

    # 2. missing sections
    missing = [s for s in SECTION_NAMES if s not in ex["sections_found"]]
    if missing:
        F.append(_finding("medium", "SECTION_MISSING",
                          "expected section(s) absent: " +
                          ", ".join(f"§{s[1:]} {SECTION_NAMES[s]}" for s in missing)))

    # 3. broken internal links
    broken = [l for l in ex["internal_links"] if l not in ex["anchors"]]
    if broken:
        F.append(_finding("medium", "LINK_BROKEN",
                          "cross-reference(s) point at anchors that do not exist", broken))

    # 4. current price consistent across sections
    prices: List[Tuple[str, float]] = []
    for st in ex["stats"]:
        if PRICE_LABEL_RE.search(st.get("label", "")):
            v = _num(st.get("value", ""))
            if v:
                prices.append((st.get("section", "?"), v))
    if len(prices) > 1:
        lo, hi = min(p[1] for p in prices), max(p[1] for p in prices)
        if lo and (hi - lo) / lo * 100 > tol_pct:
            F.append(_finding("high", "PRICE_DISAGREE",
                              f"'current price' differs by {(hi-lo)/lo*100:.1f}% between sections "
                              f"(>{tol_pct}%) — the sections were built from different data pulls",
                              [{"section": s, "value": v} for s, v in prices]))

    # 5. fair value present and scenario targets anchored to it
    fvs = [( st.get("section","?"), _num(st.get("value",""))) for st in ex["stats"]
           if FV_LABEL_RE.search(st.get("label",""))]
    fvs = [(s, v) for s, v in fvs if v]
    if not fvs:
        F.append(_finding("medium", "FV_NOT_FOUND",
                          "no 'fair value' stat card found — §3's headline number could not be "
                          "located, so scenario targets cannot be checked against it"))
    else:
        fv = fvs[0][1]
        s6 = ex["sections"].get("s6", {})
        basis = s6.get("money_basis", "")
        tgts = [n for n in s6.get("money", []) if fv and 0.2 * fv < n < 5 * fv]
        if tgts:
            hi = max(tgts)
            if hi > fv * 1.6:
                sev = "medium" if basis == "currency-marked" else "low"
                F.append(_finding(sev, "TARGET_UNANCHORED",
                                  f"§6 contains a target ({hi:,.2f}) more than 60% above the §3 "
                                  f"fair value ({fv:,.2f}). A bull case may legitimately exceed "
                                  f"fair value, but the report must say which driver changes to "
                                  f"get there — check that it does"
                                  + ("" if basis == "currency-marked" else
                                     f" [low confidence: {basis}]"),
                                  {"fair_value": fv, "highest_target": hi, "basis": basis}))

    # 6. scenario probabilities
    probs: List[float] = []
    for t in ex["tables"]:
        if t["section"] != "s6":
            continue
        rows = t["rows"]
        if not rows:
            continue
        header = [c.lower() for c in rows[0]]
        pcol = next((i for i, c in enumerate(header) if PROB_LABEL_RE.search(c)), None)
        if pcol is None:
            continue
        for r in rows[1:]:
            if pcol < len(r) and SCENARIO_RE.search(" ".join(r)):
                m = PCT_RE.search(r[pcol])
                if m:
                    probs.append(float(m.group(1)))
    if probs:
        total = sum(probs)
        if abs(total - 100) > 1.0:
            F.append(_finding("high", "PROB_SUM",
                              f"scenario probabilities sum to {total:.0f}%, not 100%", probs))
        if len(probs) == 3 and max(probs) < 50:
            F.append(_finding("medium", "PROB_NO_VIEW",
                              f"no scenario carries >=50% ({probs}) — investment-synthesis's own "
                              f"rule says a near-even split means there is no real view"))
    elif "s6" in ex["sections_found"]:
        F.append(_finding("low", "PROB_NOT_FOUND",
                          "could not find scenario probabilities in §6 — check they are stated"))

    # 7. sources / as-of in the appendix
    tail = html[-14000:].lower()
    if not re.search(r"source|แหล่งข้อมูล|data source", tail):
        F.append(_finding("medium", "NO_SOURCES",
                          "no sources section found near the end — every figure should be "
                          "traceable to where it came from"))
    if not re.search(r"as of|as-of|ณ วันที่|ข้อมูล ณ", html, re.I):
        F.append(_finding("medium", "NO_ASOF",
                          "no as-of date found — a report without one cannot be judged stale"))

    # 8. fallback-sourced data acknowledged
    if re.search(r"\bFALLBACK\b", html):
        F.append(_finding("low", "FALLBACK_PRESENT",
                          "the report contains FALLBACK-tagged figures — confirm the flag is "
                          "explained to the reader, not just printed"))

    # 9. disclaimer
    if not re.search(r"not financial advice|ไม่ใช่คำแนะนำ", html, re.I):
        F.append(_finding("high", "NO_DISCLAIMER",
                          "the not-financial-advice disclaimer is missing"))

    # 10. thin sections
    for sid in ex["sections_found"]:
        n = ex["sections"][sid].get("chars", 0)
        if n < 200:
            F.append(_finding("low", "SECTION_THIN",
                              f"§{sid[1:]} {SECTION_NAMES.get(sid,'')} has only {n} characters "
                              f"of prose — likely a stub"))
    return F


def render(ex: Dict[str, Any], findings: List[Dict[str, Any]]) -> str:
    L = [f"# R0 — internal consistency: {ex['title'] or '(untitled report)'}", ""]
    L.append(f"sections found: {', '.join('§'+s[1:] for s in ex['sections_found']) or 'none'}")
    L.append(f"stat cards: {len(ex['stats'])} · tables: {len(ex['tables'])} · "
             f"internal links: {len(ex['internal_links'])}")
    L.append("")
    if not findings:
        L.append("No internal inconsistencies found. The report does not contradict itself —")
        L.append("which says nothing yet about whether it is right. Proceed to R1.")
        return "\n".join(L)
    order = {"high": 0, "medium": 1, "low": 2}
    for f in sorted(findings, key=lambda x: order.get(x["severity"], 3)):
        L.append(f"[{f['severity'].upper():6}] {f['code']}")
        L.append(f"         {f['message']}")
        if f.get("evidence"):
            ev = json.dumps(f["evidence"], ensure_ascii=False)
            L.append(f"         evidence: {ev[:300]}")
        L.append("")
    hi = sum(1 for f in findings if f["severity"] == "high")
    L.append(f"{len(findings)} finding(s), {hi} high.")
    if hi:
        L.append("Resolve the high findings before R1 — arguing about a thesis built on numbers")
        L.append("that disagree with each other wastes the argument.")
    return "\n".join(L)


def main() -> int:
    p = argparse.ArgumentParser(description="Read a BF-Report and run the R0 consistency pass")
    p.add_argument("report", help="Path to the BF-Report .html")
    p.add_argument("--extract", action="store_true", help="Emit the structured extract instead of checks")
    p.add_argument("--json", action="store_true", help="Emit findings as JSON")
    p.add_argument("--tolerance", type=float, default=1.0,
                   help="Percent disagreement allowed between repeated figures (default 1.0)")
    p.add_argument("--out", default=None)
    args = p.parse_args()

    try:
        with open(args.report, encoding="utf-8", errors="replace") as f:
            html = f.read()
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    ex = extract(html)
    if args.extract:
        payload = ex
    else:
        findings = check(html, ex, args.tolerance)
        payload = {"report": args.report, "title": ex["title"],
                   "sections_found": ex["sections_found"], "findings": findings}

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

    if args.extract or args.json:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(render(ex, payload["findings"]))
    return 0 if (args.extract or not payload.get("findings")) else 1


if __name__ == "__main__":
    sys.exit(main())
