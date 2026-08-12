# Indicators & Calibration

Data pull, the **calibration** routines (fit parameters to *this* stock before judging), and the indicator/detection code. Read alongside Steps 1–2 of `SKILL.md`. All code is plain `yfinance + numpy + pandas` — no heavy TA dependency. Install if needed: `python3 -m pip install -q yfinance numpy pandas --break-system-packages`.

> The single most common technical error is using assumed parameters (a generic MA, a default Fib). **Calibrate first**, then read.

---

## 1. Pull weekly + daily OHLCV

```python
import yfinance as yf, numpy as np, pandas as pd
TICKER = "AOT.BK"  # use the suffixed ticker from Step 1
t = yf.Ticker(TICKER)
dly = t.history(period="2y",  interval="1d", auto_adjust=True)
wk  = t.history(period="5y",  interval="1wk", auto_adjust=True)
for df in (dly, wk):
    df.dropna(inplace=True)
```

Read the **weekly** for context (Step 2) and the **daily** for the entry (Steps 3–5).

---

## 2. Calibrate to this stock

### 2a. Which moving average does the stock respect?
Test a grid of SMAs/EMAs; "respect" = price dipped near the MA (within a fraction of ATR) and then closed back above within a few bars. Pick the MA(s) with the most clean holds.

```python
def atr(df, n=14):
    h,l,c = df["High"], df["Low"], df["Close"]
    tr = pd.concat([h-l, (h-c.shift()).abs(), (l-c.shift()).abs()], axis=1).max(axis=1)
    return tr.rolling(n).mean()

def ma_respect_score(df, length, kind="SMA", tol=0.5, bounce=5):
    a = atr(df)
    ma = df["Close"].ewm(span=length).mean() if kind=="EMA" else df["Close"].rolling(length).mean()
    near = (df["Low"] <= ma + tol*a) & (df["Low"] >= ma - tol*a)        # tagged the MA
    held = []
    idx = df.index
    for i in np.where(near.values)[0]:
        if i+bounce < len(df):
            held.append(df["Close"].iloc[i+bounce] > ma.iloc[i])         # closed back above later
    return (np.mean(held) if held else 0, len(held))                     # (hold-rate, touches)

grid = [(L,k) for L in (10,20,30,50,100,150,200) for k in ("SMA","EMA")]
scores = {f"{k}{L}": ma_respect_score(dly, L, k) for L,k in grid}
# choose the MA(s) with a high hold-rate AND a meaningful touch count
respected = sorted(scores.items(), key=lambda kv:(kv[1][0], kv[1][1]), reverse=True)
```
Use the top, sufficiently-tested MA as "the MA this stock respects" — **do not** default to 20/50.

### 2b. Swings, then Fib anchors
Detect swing highs/lows (pivots), then anchor Fib on the most significant recent swing.

```python
def pivots(df, left=5, right=5):
    H, L = df["High"].values, df["Low"].values
    hi, lo = [], []
    for i in range(left, len(df)-right):
        if H[i] == max(H[i-left:i+right+1]): hi.append(i)
        if L[i] == min(L[i-left:i+right+1]): lo.append(i)
    return hi, lo

def fib_levels(swing_low, swing_high):
    rng = swing_high - swing_low
    retr = {r: swing_high - rng*r for r in (0.236,0.382,0.5,0.618,0.786)}   # pullback zones
    ext  = {e: swing_high + rng*(e-1) for e in (1.272,1.618,2.0)}           # up-targets
    down = {e: swing_low  - rng*(e-1) for e in (1.272,1.618,2.0)}           # downside targets (decline legs)
    return retr, ext, down
```
Check which Fib levels coincided with prior reactions for this name (confluence with §2c support/resistance) and prefer those.

### 2c. Volatility, typical pullback, volume baseline
```python
a14 = atr(dly).iloc[-1]                                   # stop sizing unit
# typical pullback: drawdowns from rolling 20-bar highs
roll_hi = dly["Close"].rolling(20).max()
dd = (dly["Close"]/roll_hi - 1.0)
typical_pullback = dd[dd<0].quantile(0.5)                 # this stock's "normal" dip (median)
vol_base = dly["Volume"].rolling(50).mean().iloc[-1]      # baseline
vol_now  = dly["Volume"].iloc[-1]
rel_vol  = vol_now / vol_base                             # >~1.5 = expansion; <~0.7 = dry-up (calibrate)
```
Report ATR, the typical-pullback depth, and the volume baseline — these define what "a normal dip" and "a real volume move" mean *for this stock*.

---

## 3. Indicators

### MA stack & RSI (Wilder)
```python
for L in (10,20,50,150,200):
    dly[f"SMA{L}"] = dly["Close"].rolling(L).mean()

def rsi(s, n=14):
    d = s.diff(); up = d.clip(lower=0); dn = -d.clip(upper=0)
    rs = up.ewm(alpha=1/n, adjust=False).mean() / dn.ewm(alpha=1/n, adjust=False).mean()
    return 100 - 100/(1+rs)
dly["RSI"] = rsi(dly["Close"])
```

### RSI divergence (warning signal)
Compare the last two swing highs/lows in price vs RSI.
```python
def divergence(df, rsi_col="RSI", left=5, right=5):
    hi, lo = pivots(df, left, right)
    out = {"bearish": False, "bullish": False}
    if len(hi) >= 2:
        a,b = hi[-2], hi[-1]
        if df["High"].iloc[b] > df["High"].iloc[a] and df[rsi_col].iloc[b] < df[rsi_col].iloc[a]:
            out["bearish"] = True        # price higher-high, RSI lower-high → caution on breakouts
    if len(lo) >= 2:
        a,b = lo[-2], lo[-1]
        if df["Low"].iloc[b] < df["Low"].iloc[a] and df[rsi_col].iloc[b] > df[rsi_col].iloc[a]:
            out["bullish"] = True         # price lower-low, RSI higher-low → bottoming tell
    return out
```

### Weinstein stage (weekly heuristic)
```python
wk["MA30"] = wk["Close"].rolling(30).mean()
slope = wk["MA30"].diff(4).iloc[-1]
px, ma = wk["Close"].iloc[-1], wk["MA30"].iloc[-1]
if   px > ma and slope > 0: stage = "2 (advancing)"
elif px < ma and slope < 0: stage = "4 (declining)"
elif px > ma and slope <= 0: stage = "3 (topping)"
else: stage = "1 (basing)"
```

### Minervini Trend Template (daily, 8 checks)
```python
c   = dly["Close"].iloc[-1]
s50, s150, s200 = dly["SMA50"].iloc[-1], dly["SMA150"].iloc[-1], dly["SMA200"].iloc[-1]
s200_22ago = dly["SMA200"].iloc[-22]
lo52, hi52 = dly["Close"].iloc[-252:].min(), dly["Close"].iloc[-252:].max()
tt = [c>s150, c>s200, s150>s200, s200>s200_22ago, c>s50, s50>s150,
      c >= 1.30*lo52, c >= 0.75*hi52]   # all True = textbook stage-2 leader
trend_template_pass = all(tt)
```

### VCP contraction detection
A VCP is a sequence of progressively *shallower* pullbacks with *declining* volume into a pivot.
```python
def vcp(df, left=5, right=5):
    hi, lo = pivots(df, left, right)
    pts = sorted(hi+lo)
    legs = []                                  # successive peak→trough depths
    for i in range(1, len(pts)):
        a,b = pts[i-1], pts[i]
        depth = abs(df["Close"].iloc[b]/df["Close"].iloc[a] - 1)
        legs.append((b, depth, df["Volume"].iloc[a:b+1].mean()))
    contractions = [legs[i] for i in range(1,len(legs))
                    if legs[i][1] < legs[i-1][1] and legs[i][2] < legs[i-1][2]]
    return contractions                        # 2–4 tightening, lower-volume legs ⇒ VCP; last high ≈ pivot
```
Confirm the **pivot** (the final tight area's high) and require **volume expansion** on the breakout (`rel_vol` from §2c).

---

## 4. Data caveats
- yfinance auto-adjusts for splits/dividends; weekly bars depend on the period boundary — sanity-check the latest bar.
- Pivot/divergence detection is sensitive to the `left/right` window; widen it for noisy names.
- Calibration needs enough history; for recent IPOs or thin names, say confidence is lower and lean on structure + the fundamental case.
- Indicators describe odds, not certainties — always pair with the explicit invalidation (`playbook.md`).
