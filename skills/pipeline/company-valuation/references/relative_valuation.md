# Relative Valuation — Detailed Reference

Relative valuation implies a price by applying peer multiples. Fast, market-anchored, and captures sentiment — but "garbage in, garbage out" when peers are poorly chosen.

## Peer Selection Heuristics

Aim for 4–6 peers. More is noisier, fewer is brittle.

| Criterion | Priority |
|---|---|
| Same GICS industry | Must |
| Similar business model (e.g., SaaS vs perpetual license) | Must |
| Similar growth rate (within ±10 percentage points) | Strong preference |
| Similar margin profile | Preference |
| Similar capital structure | Nice to have |
| Similar geographic exposure | Nice to have |

**Avoid:** Mega-cap diversified companies as peers for pure-play small/mid-caps (e.g., MSFT is not a good peer for DDOG).

## Peer Validation Gate (REQUIRED before computing any multiple)

The "Same GICS industry = Must" heuristic above is **advisory and routinely ignored**. Without an enforced check, a hotel gets used as a peer for a palm-oil producer and the median multiple silently becomes meaningless. This gate makes the check mechanical. **Run it on every peer set before computing a single multiple.**

```python
# Uses sector/industry already pulled for the target in Step 3.
target_sector   = info.get("sector")     # e.g. "Consumer Defensive"
target_industry = info.get("industry")   # e.g. "Farm Products"

validated, rejected, flagged = [], [], []
for p in PEERS:
    pi = yf.Ticker(p).info
    ps, pi_ind = pi.get("sector"), pi.get("industry")
    if ps and target_sector and ps != target_sector:
        rejected.append((p, ps, pi_ind))                 # HARD REJECT
    elif pi_ind and target_industry and pi_ind != target_industry:
        flagged.append((p, pi_ind))                       # SOFT FLAG
    else:
        validated.append(p)

print(f"REJECTED (different sector — never use): {rejected}")
print(f"FLAGGED   (same sector, different sub-industry — justify): {flagged}")
print(f"OK        (same sector + same sub-industry): {validated}")
PEERS = validated + [p for p,_ in flagged]   # flagged allowed, rejected never
```

**Hard gate (REJECT — different GICS sector):** Never compute a multiple using a cross-sector peer. A hotel as a peer for a palm-oil producer, a bank as a peer for a software firm, a semiconductor as a peer for a retailer — all produce garbage implied prices. If a candidate fails the hard gate, **discard it and find a same-sector replacement** before continuing.

**Fallback order when no same-sector peer is found:**
1. **Regional same-sector peers first** (e.g. a Thai palm-oil producer → Indonesian/Singapore-listed palm pure-plays). See the regional rows in "Common Peer Sets (Fallback)" below. This is the correct fix, not a compromise.
2. **Wider sector same-region peers** (e.g. broader ASEAN agribusiness) — soft-flag and justify.
3. **Skip relative valuation entirely** and rely on DCF + justified-multiple (P/B justified by ROE, EV/EBITDA justified by WACC). State this explicitly in the output. **Never** fall back to a wrong-sector peer to "fill the table."

**Soft flag (same sector, different sub-industry):** Usable, but (1) show the flag in the peer table, (2) state one line on why it belongs, (3) consider a −10% to −20% multiple adjustment. Example: "Farm Products" target vs "Agricultural Inputs" peer — same Consumer Staples sector, adjacent sub-industry, soft-flag is fine.

**Special case — sub-industry is far despite same sector:** If the sub-industries are economically unrelated (e.g. "Farm Products" target vs "Resorts & Casinos" peer — both can land in Consumer sectors), treat it as a **hard reject**. When in doubt, reject: the cost of one fewer peer is far smaller than the cost of a corrupted median.

## Multiples Cheat Sheet

| Multiple | Best for | Avoid for |
|---|---|---|
| P/E (trailing) | Mature, profitable companies | Unprofitable, cyclical troughs |
| P/E (forward) | Growing, earnings-visible | Early-stage, wide estimate dispersion |
| PEG (P/E ÷ growth) | High-growth profitable | Mature low-growth |
| EV/Revenue | Unprofitable, early SaaS | Mature mixed-margin |
| EV/EBITDA | Mid-to-late stage across capital structures | Financials, REITs |
| EV/EBIT | Capital-intensive (excludes D&A smoothing) | Non-comparable D&A conventions |
| P/B | Banks, insurance | Asset-light businesses |
| P/TBV | Banks | Non-financials |
| P/FFO, P/AFFO | REITs | Anything else |
| EV/Sub, EV/MAU | Streaming, social | Not meaningful elsewhere |

## Computing Implied Price

For each multiple, take peer **median** (not mean — medians are robust to outliers).

```
# Equity multiples
Implied price (P/E) = peer median P/E × target EPS_TTM

# Enterprise multiples
Implied EV (EV/Rev)   = peer median EV/Rev × target Revenue_TTM
Implied EV (EV/EBITDA)= peer median EV/EBITDA × target EBITDA_TTM

Net debt = Total Debt − Cash
Implied equity value = Implied EV − Net debt − Minority interest − Preferred
Implied price = Implied equity value / diluted shares
```

## Adjustments — When NOT to Apply Peer Median Blindly

Adjust ±10–30% based on target vs peer median:

| If target has... | Adjust implied multiple |
|---|---|
| Higher growth rate (>500bps above peer median) | +10% to +30% |
| Lower growth rate | −10% to −30% |
| Higher margin (>300bps above peer median) | +10% to +20% |
| Lower margin | −10% to −20% |
| Better balance sheet / lower leverage | +5% to +10% |
| Higher leverage / covenant risk | −10% to −20% |
| Dominant market position / moat | +10% to +20% |
| Category laggard / market share loss | −10% to −20% |
| Regulatory overhang / activist target | −5% to −15% |

Always state the adjustment and the reason.

## Rule of 40 for SaaS

For software/SaaS peers, add Rule of 40 as a supplementary anchor:

```
Rule of 40 = Revenue Growth % + FCF Margin %
```

| Rule of 40 score | Peer EV/Revenue premium |
|---|---|
| ≥ 50 | Top quartile — use 75th percentile peer multiple |
| 40–50 | Above median — use median + 10% |
| 30–40 | Below median — use median − 10% |
| < 30 | Bottom quartile — use 25th percentile peer multiple |

## Common Peer Sets (Fallback)

Hardcoded starter sets when industry classification is ambiguous. Expand as needed.

**US-listed:**

| Theme | Peers |
|---|---|
| Enterprise software (large-cap) | MSFT, ORCL, CRM, NOW, SAP, WDAY |
| Horizontal SaaS mid-cap | DDOG, MDB, NET, SNOW, TEAM, ZS |
| Cybersecurity | CRWD, PANW, ZS, S, NET, FTNT |
| Semiconductors (compute / GPU) | NVDA, AMD, AVGO, INTC, QCOM |
| Semiconductor equipment | AMAT, LRCX, KLAC, ASML |
| Mega-cap internet | GOOGL, META, AMZN, MSFT, AAPL |
| E-commerce | AMZN, SHOP, MELI, SE, ETSY |
| Payments | V, MA, PYPL, AXP, SQ |
| US mega-bank | JPM, BAC, C, WFC, GS, MS |
| Regional banks | PNC, TFC, USB, KEY |
| Life insurance | MET, PRU, LNC, AFL |
| P&C insurance | TRV, CB, ALL, PGR |
| Consumer staples | KO, PEP, PG, CL, UL, MDLZ |
| Tobacco | MO, PM, BTI |
| Fast food | MCD, CMG, YUM, QSR, SBUX |
| Apparel / luxury | LVMUY, NKE, LULU, RL |
| Auto (legacy) | F, GM, STLA, TM, HMC |
| Auto (EV) | TSLA, LCID, RIVN, NIO, XPEV |
| Airlines (US) | DAL, UAL, AAL, LUV, ALK |
| Oil & gas majors | XOM, CVX, SHEL, BP, TTE |
| E&P pure-plays | COP, EOG, PXD, DVN, OXY |
| Pharma (large-cap) | PFE, JNJ, MRK, LLY, ABBV, BMY |
| Biotech large-cap | AMGN, GILD, REGN, VRTX |
| Medical devices | MDT, ABT, BSX, SYK, ISRG |
| Industrial conglomerates | GE, HON, MMM, ITW, EMR |
| Defense | LMT, RTX, NOC, GD, BA |
| Telecom | T, VZ, TMUS, CMCSA |
| Utilities | NEE, DUK, SO, D, AEP |
| REITs (diversified) | PLD, AMT, EQIX, CCI, SPG |
| Streaming | NFLX, DIS, WBD, PARA |

**Regional / non-US (USE THESE for non-US targets — US peers are usually the wrong peer set):**

| Theme | Peers | Notes |
|---|---|---|
| Palm oil (Indonesia-listed) | AALI.JK, LSIP.JK, SGRO.JK, SMAR.JK | Pure-plays; Indonesia = ~55% of global supply |
| Palm oil (Singapore-listed, Indonesia ops) | E5H.SI (Wilmar), F34.SI (First Resources), P34.SI (Bumitama), GGR.SI (Golden Agri) | Often larger + more liquid than .JK |
| Palm oil (Malaysia-listed) | IOICORP.KL, KLK.KL, SDG.KL (Sime Darby Plantation), GENP.KL | Malaysia = ~25% of global supply; yfinance .KL data can be patchy — cross-check |
| Thai banks | BBL.BK, KBANK.BK, SCB.BK, KTB.BK, TTB.BK, TISCO.BK | Use P/B and P/TBV, not DCF |
| Thai energy (integrated oil & gas) | PTT.BK, TOP.BK, BCP.BK, SPRC.BK, PTG.BK | PTT is the benchmark; include up/downstream mix |
| Thai retail / consumer staples | CPALL.BK, CPAXT.BK, HMPRO.BK, DOHOME.BK, CRC.BK | Mix of convenience, DIY, department store |
| Thai agribusiness (non-palm) | CPF.BK (protein), TUFF.BK (tuna), ASIAN.BK (seafood) | Distinguish protein/seafood from crops |
| ASEAN telecom | ADVANC.BK, INTUCH.BK, D04.SI (Singtel), 6862.HK (HKT), TLKM.JK | Regulated, capex-heavy |
| Thai REITs | CPNREIT.BK, WHART.BK, FTREIT.BK, PRO.BK, LHFG.BK | Use P/FFO, P/AFFO, NAV — not DCF |
| Japan autos | 7203.T (Toyota), 7267.T (Honda), 7269.T (Suzuki), 7201.T (Nissan), 7205.T (Subaru) | Note keiretsu cross-holdings |
| Japan electronics/conglomerates | 6758.T (Sony), 6501.T (Hitachi), 6702.T (Fujitsu), 8035.T (Tokyo Electron) | |
| China internet | 9988.HK (Alibaba), 0700.HK (Tencent), 3690.HK (Meituan), PDD | Use HK listings, not ADRs, when possible |
| China EV / battery | 1211.HK (BYD), 2015.HK (Li Auto), NIO, XPEV, 300750.SZ (CATL) | |
| India IT services | INFY.NS, TCS.NS, WIT.NS (Wipro), HCLTECH.NS | |
| European luxury | MC.PA (LVMH), RMS.PA (Hermès), CFR.SW (Richemont), BRBY.L (Burberry) | |

When the target's industry is not in either table, **prefer regional same-sector peers found via a screener over a US same-sub-industry peer from the table above** — a regional peer captures local regulation, FX, and cost structure that a US peer cannot.

## Cross-Check: Target vs Peers Table

Always produce a table of peers with:
- Ticker / name
- Market cap
- Revenue growth (LTM, forward)
- Gross margin, EBITDA margin, operating margin
- P/E (fwd), EV/Revenue, EV/EBITDA
- Peer median (bottom row)

This lets the user see at a glance whether the target "deserves" a premium/discount.

## Common Pitfalls

- **Wrong-industry peers (the #1 cause of relative-valuation errors):** A peer from a different GICS sector (e.g. a hotel as a peer for a palm-oil producer, a semiconductor as a peer for a retailer) silently corrupts the median multiple and produces a meaningless implied price that still *looks* rigorous. **Always run the Peer Validation Gate above before computing any multiple.** The damage is invisible until someone notices the peer set is wrong — by then the headline fair value has already propagated into the report. When in doubt, drop the peer or skip the method.
- **Using a single multiple**: Triangulate with ≥2 multiples. EV/EBITDA should agree with EV/Revenue within ±15% when applied to same peer set.
- **Outlier peers**: Exclude if P/E > 100 or EV/Rev > 50 unless target is similarly extreme.
- **Peer in trough**: If peer is in distress or restructuring, their multiple compresses — excluding them or adjusting.
- **Different fiscal year ends**: Normalize to TTM.
- **Stock-based comp**: EV/EBITDA without SBC adjustment overstates multiples for SaaS. Consider EV/EBITDA (ex-SBC) for SaaS peers.
- **Currency**: International peers — normalize to USD and note FX sensitivity.
- **Non-US target, US-only peer set**: A common variant of the wrong-industry error. US peers carry different regulation, FX, cost structure, and capital-market norms than a regional target. Use the regional peer sets above, or skip the method.
