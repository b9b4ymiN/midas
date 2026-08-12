# BF Technical Analysis

Read a stock's chart the way a seasoned discretionary trader does — **top-down, calibrated to the specific stock, and multi-style** — to judge timing, entry zones, stops, and risk (R), and connect it to the fundamental fair value.

## What it does

- Pulls **weekly + daily** data and **calibrates parameters to this stock first** (which MA it respects, Fib levels that held, ATR, typical pullback, volume baseline) — never assumed defaults
- Reads **top-down**: weekly for context (trend, Weinstein stage, Trend Template, major S/R, trendlines/channels), daily for the entry
- **Diagnoses the chart's condition, then prescribes** — waiting to break (incl. VCP), pullback in an uptrend, at support / possible bottom, broken downtrend awaiting a pullback, or downtrend intact — so a bottoming chart is read on its own terms, never rejected
- Runs the **context toolkit** with confirmations *and* warnings (RSI divergence, failed breakouts, overhead supply, abnormal pullbacks) and **Fib/channel targets**, all as **zones**; conviction scales with **confluence**
- Outputs **entry zone · stop · target(s) · R-multiple · timing verdict**, with the **fair value as the long-term magnet**

## Triggers

`technical analysis of X`, `is this a good entry`, `chart read`, `support and resistance`, `trend and Fibonacci`, `VCP / pivot / breakout`, `where's the stop`, `is the bottom in`, `when to buy`. Also runs as **Step 4.5** of `both-stock-analysis`, feeding `investment-synthesis` and `bf-report`.

## Prerequisites

- yfinance + numpy + pandas (`pip install ... --break-system-packages` if missing)
- Ideally the fundamental fair value from `company-valuation` (sets the magnet and the bottom-plus-valuation case); works standalone otherwise with that flagged

## Output

A technical read: calibrated parameters, weekly context, the diagnosed condition, the read + confluence (confirmations / warnings / Fib-channel targets), the risk geometry (entry zone / stop / target / R), and a conditional timing verdict.

## Reference Files

- `references/playbook.md` — Top-down method, condition decision tree, per-condition toolkits, confluence scoring
- `references/indicators.md` — Weekly+daily pull, calibration routines, MA/RSI/divergence/stage/Trend-Template/VCP code
- `references/levels_and_risk.md` — S/R, trendlines/channels, Fibonacci, and risk geometry (entry/stop/target → R)

## Disclaimer

For research and educational purposes only. Not financial advice. Technicals inform timing and risk, not whether to own the business.
