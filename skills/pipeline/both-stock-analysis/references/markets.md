# Markets Reference

Lookup data for Step 1 (market confirmation) and Step 3 (country/currency overrides in `company-valuation`).

> These are **starting defaults**. Risk-free rates move daily and country risk premiums (CRP) are revised periodically. For a live analysis, fetch the current local 10Y sovereign yield, and sanity-check the CRP against Aswath Damodaran's latest published country-risk-premium table (updated roughly annually on the NYU Stern site). When in doubt, state the date/source of the rate you used.

---

## 1. Exchange suffixes (yfinance) & currency

Resolve a company name to the correctly-suffixed ticker before running any sub-skill. A wrong or missing suffix silently returns the wrong listing or no data.

| Market / Exchange | yfinance suffix | Currency | Example |
|---|---|---|---|
| **United States** (NYSE / NASDAQ) | *(none)* | USD | `AAPL`, `NVDA` |
| **Thailand** (SET) | `.BK` | THB | `PTT.BK`, `CPALL.BK`, `AOT.BK`, `KBANK.BK`, `DELTA.BK` |
| London (LSE) | `.L` | GBP (often GBp/pence!) | `SHEL.L`, `HSBA.L` |
| Tokyo (TSE) | `.T` | JPY | `7203.T` (Toyota), `6758.T` (Sony) |
| Hong Kong (HKEX) | `.HK` | HKD | `0700.HK` (Tencent), `9988.HK` (Alibaba) |
| Shanghai | `.SS` | CNY | `600519.SS` (Kweichow Moutai) |
| Shenzhen | `.SZ` | CNY | `000333.SZ` (Midea) |
| India (NSE / BSE) | `.NS` / `.BO` | INR | `RELIANCE.NS`, `TCS.NS` |
| Germany (XETRA) | `.DE` | EUR | `SAP.DE`, `SIE.DE` |
| Euronext Paris | `.PA` | EUR | `MC.PA` (LVMH) |
| Euronext Amsterdam | `.AS` | EUR | `ASML.AS` |
| Switzerland (SIX) | `.SW` | CHF | `NESN.SW`, `ROG.SW` |
| Toronto (TSX) | `.TO` | CAD | `RY.TO`, `SHOP.TO` |
| Australia (ASX) | `.AX` | AUD | `BHP.AX`, `CBA.AX` |
| Korea (KRX) | `.KS` / `.KQ` | KRW | `005930.KS` (Samsung) |
| Taiwan (TWSE) | `.TW` | TWD | `2330.TW` (TSMC) |
| Singapore (SGX) | `.SI` | SGD | `D05.SI` (DBS) |
| Brazil (B3) | `.SA` | BRL | `PETR4.SA`, `VALE3.SA` |
| Saudi (Tadawul) | `.SR` | SAR | `2222.SR` (Aramco) |

**Watch-outs:**
- **London prices** are frequently quoted in **pence (GBp)**, not pounds — divide by 100 before comparing to a per-share value in GBP.
- Many non-US tickers are **numeric** (Tokyo, HK, China, Korea, Taiwan) — keep leading zeros.
- US ADRs of foreign companies (e.g., `TSM`, `BABA`) trade in USD; decide with the user whether they want the local listing or the ADR.

---

## 2. Valuation parameters by market

Override `company-valuation`'s US defaults with the row matching the home market. `ke = rf + beta × (mature ERP + CRP)`. Keep cash flows and the discount rate in the **same currency**.

| Market | Risk-free proxy (10Y sovereign) | Approx. recent yield* | Mature-mkt ERP | Country risk premium (CRP) | Total ERP | Terminal g cap (≈ nominal GDP) |
|---|---|---|---|---|---|---|
| **US** | 10Y UST | live (~4.5%) | 5.5% | 0.0% | ~5.5% | 2.5% |
| **Thailand** | Thai 10Y govt bond | ~2.5–3.0% | 5.5% | ~0.9% | ~6.4% | 3.0–3.5% |
| UK | 10Y Gilt | ~4.0% | 5.5% | ~0.0% | ~5.5% | 2.5% |
| Japan | 10Y JGB | ~1.0–1.5% | 5.5% | ~0.0% | ~5.5% | 1.0–1.5% |
| Germany / Eurozone core | 10Y Bund | ~2.5% | 5.5% | ~0.0% | ~5.5% | 2.0% |
| China | 10Y CGB | ~1.7–2.5% | 5.5% | ~0.6% | ~6.1% | 3.5–4.0% |
| India | 10Y G-Sec | ~6.5–7.0% | 5.5% | ~2.0% | ~7.5% | 5.0–6.0% |
| Hong Kong | use US UST + HKD peg note | ~4.0% | 5.5% | ~0.3% | ~5.8% | 2.5% |
| Brazil | 10Y NTN-F | ~11–13% | 5.5% | ~3.0% | ~8.5% | 5.0–6.0% |
| Taiwan | 10Y govt bond | ~1.5% | 5.5% | ~0.4% | ~5.9% | 2.5–3.0% |
| Korea | 10Y KTB | ~3.0% | 5.5% | ~0.5% | ~6.0% | 2.5–3.0% |

\* Yields drift — **fetch the live figure** for the analysis and note it. The CRP and ERP figures are approximate Damodaran-style ranges; verify against the latest published table for anything decision-grade.

**Rules of thumb:**
- Terminal growth **must never exceed** the risk-free rate, and should sit at or below the home economy's long-run **nominal** GDP growth.
- High-inflation/high-rate markets (Brazil, India) carry both higher risk-free rates *and* higher nominal terminal growth — keep the relationship consistent; don't pair a 12% discount rate with 2.5% terminal growth unless the cash flows are real (inflation-adjusted).
- For a USD-comparison fair value on a foreign stock, either (a) value in local currency then convert at spot, or (b) build the DCF in USD using USD cash flows and a USD discount rate — never blend.

---

## 3. Index symbols (for market-context slides)

| Market | Index | yfinance symbol |
|---|---|---|
| US | S&P 500 | `^GSPC` |
| US | NASDAQ Composite | `^IXIC` |
| Thailand | SET Index | `^SET.BK` *(verify; if unavailable, use the `SET.BK` proxy or an SET ETF)* |
| UK | FTSE 100 | `^FTSE` |
| Japan | Nikkei 225 | `^N225` |
| Hong Kong | Hang Seng | `^HSI` |
| Germany | DAX | `^GDAXI` |
| India | NIFTY 50 | `^NSEI` |

---

## 4. Thailand (SET) specifics

- Suffix `.BK`; currency **THB**.
- The SET is **bank- and energy-heavy** (PTT, banks like KBANK/SCB/BBL) plus large retail/consumer names (CPALL, CPF) — peer sets for relative valuation should be regional (SET / ASEAN) where US peers aren't comparable.
- For Thai **banks**, prefer P/B and P/TBV over DCF (let `company-valuation` route to the financials path).
- Use the Thai 10Y government bond as the risk-free rate and add the Thailand CRP to the ERP.
- Offer the final deck in **Thai or English** per the user's preference.
