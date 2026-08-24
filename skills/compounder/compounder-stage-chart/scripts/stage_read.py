#!/usr/bin/env python3
"""Read the long-term stage of a chart and cross it with the business life cycle.

Pulls weekly and monthly bars, classifies each timeframe into a Weinstein stage at
long-horizon settings (30-week SMA weekly, 10-month SMA monthly), dates the current
stage, renders a self-contained SVG for each timeframe, and writes `stage_pack.json`.

The newest bar is excluded from every judgement until its period closes — a month
four days old is not a monthly bar — and the exclusion is recorded rather than
assumed. Method and provenance: ../references/stage-classification.md.

    python stage_read.py CPRT --out run/CPRT-2026-08-24/

Research and educational output only. Not financial advice.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

# --- settings, from references/stage-classification.md -------------------

TIMEFRAMES = {
    "monthly": {
        "interval": "1mo",
        "period": "10y",
        "ma_length": 10,
        "ma_label": "10-month SMA",
        "slope_lookback": 6,
        "slope_rising": 0.02,
        "slope_falling": -0.02,
    },
    "weekly": {
        "interval": "1wk",
        "period": "5y",
        "ma_length": 30,
        "ma_label": "30-week SMA",
        "slope_lookback": 13,
        "slope_rising": 0.015,
        "slope_falling": -0.015,
    },
}

RANGE_WINDOW = 12          # bars used for the high/low context window
RECENT_HIGH_WINDOW = 3     # a high inside this many bars counts as "now"
CONFIRM_BARS = 2           # bars a new classification must hold before it counts
VOLUME_RECENT = 3
VOLUME_BASE = 12

STAGE_1, STAGE_2, STAGE_3, STAGE_4 = "STAGE_1", "STAGE_2", "STAGE_3", "STAGE_4"
TRANSITIONAL = "TRANSITIONAL"

STAGE_WORDS = {
    STAGE_1: "base",
    STAGE_2: "advance",
    STAGE_3: "top",
    STAGE_4: "decline",
    TRANSITIONAL: "between stages",
}

# Stage → design-system judgement token used for the background band.
STAGE_TOKEN = {
    STAGE_1: "--line-soft",
    STAGE_2: "--good-soft",
    STAGE_3: "--warn-soft",
    STAGE_4: "--risk-soft",
    TRANSITIONAL: "--surface-2",
}


# --- data ----------------------------------------------------------------

def fetch(ticker: str, interval: str, period: str):
    import yfinance as yf

    df = yf.Ticker(ticker).history(period=period, interval=interval, auto_adjust=True)
    if df is None or df.empty:
        return None
    df = df.dropna(subset=["Close"])
    return df


def period_is_closed(stamp, interval: str, today: date) -> bool:
    """Has the bar's own period ended?"""
    d = stamp.date() if hasattr(stamp, "date") else stamp
    if interval == "1mo":
        return (d.year, d.month) < (today.year, today.month)
    # weekly bars are stamped on the Monday of their week
    return (today - d).days >= 7


# --- classification ------------------------------------------------------

def sma(values, length):
    out = []
    for i in range(len(values)):
        if i + 1 < length:
            out.append(None)
        else:
            window = values[i + 1 - length: i + 1]
            out.append(sum(window) / length)
    return out


def slope_class(ma, i, cfg):
    """rising / flat / falling, from the average's own change over the lookback."""
    j = i - cfg["slope_lookback"]
    if j < 0 or ma[i] is None or ma[j] is None or ma[j] == 0:
        return None
    change = (ma[i] - ma[j]) / abs(ma[j])
    if change > cfg["slope_rising"]:
        return "rising"
    if change < cfg["slope_falling"]:
        return "falling"
    return "flat"


def classify_bar(closes, highs, lows, ma, i, cfg):
    """The four stages, plus TRANSITIONAL where the inputs disagree.

    Rules and their tie-breaks are stated in references/stage-classification.md;
    this function is the executable copy of that text.
    """
    slope = slope_class(ma, i, cfg)
    if slope is None or ma[i] is None:
        return None
    above = closes[i] >= ma[i]

    if slope == "rising" and above:
        return STAGE_2
    if slope == "falling" and not above:
        return STAGE_4
    if slope != "flat":
        # rising average with price below it, or falling with price above it
        return TRANSITIONAL

    lo = max(0, i + 1 - RANGE_WINDOW)
    window_closes = closes[lo: i + 1]
    if not window_closes:
        return TRANSITIONAL
    high_at = lo + window_closes.index(max(window_closes))
    if i - high_at < RECENT_HIGH_WINDOW:
        # making its highest close right now while the average is still flat:
        # an advance the average has not confirmed yet
        return TRANSITIONAL

    top = max(highs[lo: i + 1])
    bottom = min(lows[lo: i + 1])
    span = top - bottom
    position = 0.5 if span <= 0 else (closes[i] - bottom) / span
    return STAGE_3 if position >= 0.5 else STAGE_1


def confirmed_series(raw):
    """Require CONFIRM_BARS consecutive bars before a change is recognised."""
    out = []
    current = None
    for i, value in enumerate(raw):
        if value is None:
            out.append(None)
            continue
        if current is None:
            current = value
        elif value != current:
            run = 1
            j = i - 1
            while j >= 0 and raw[j] == value:
                run += 1
                j -= 1
            if run >= CONFIRM_BARS:
                current = value
        out.append(current)
    return out


def stage_runs(dates, stages):
    runs = []
    for d, s in zip(dates, stages):
        if s is None:
            continue
        if runs and runs[-1]["stage"] == s:
            runs[-1]["end"] = d
        else:
            runs.append({"stage": s, "start": d, "end": d})
    return runs


def volume_context(volumes, i):
    lo_recent = max(0, i + 1 - VOLUME_RECENT)
    lo_base = max(0, i + 1 - VOLUME_BASE)
    recent = volumes[lo_recent: i + 1]
    base = volumes[lo_base: i + 1]
    if not recent or not base or sum(base) == 0:
        return None
    return round((sum(recent) / len(recent)) / (sum(base) / len(base)), 2)


def invalidation(closes, ma, i, cfg, stage):
    """What observation would falsify this read, in price terms."""
    level = ma[i]
    if level is None:
        return "UNRESOLVED — the moving average is not yet defined on this history"
    unit = cfg["ma_label"]
    if stage == STAGE_2:
        return (f"a close below the {unit} (currently {level:,.2f}) held for "
                f"{CONFIRM_BARS} bars, or the average turning down over "
                f"{cfg['slope_lookback']} bars")
    if stage == STAGE_4:
        return (f"a close above the {unit} (currently {level:,.2f}) held for "
                f"{CONFIRM_BARS} bars, or the average turning up over "
                f"{cfg['slope_lookback']} bars")
    if stage == STAGE_3:
        return (f"a new highest close above {max(closes[-RANGE_WINDOW:]):,.2f} with the "
                f"{unit} turning up, or a close below the {unit} ({level:,.2f})")
    if stage == STAGE_1:
        return (f"a close above {max(closes[-RANGE_WINDOW:]):,.2f} with the {unit} "
                f"({level:,.2f}) turning up, or a close below "
                f"{min(closes[-RANGE_WINDOW:]):,.2f}")
    return (f"the {unit} ({level:,.2f}) resolving to a rising or falling slope over "
            f"{cfg['slope_lookback']} bars")


def read_timeframe(ticker, name, cfg, today):
    df = fetch(ticker, cfg["interval"], cfg["period"])
    if df is None or len(df) < cfg["ma_length"] + cfg["slope_lookback"]:
        return None, {
            "timeframe": name,
            "status": "UNAVAILABLE",
            "reason": ("no bars returned" if df is None else
                       f"only {0 if df is None else len(df)} bars — "
                       f"{cfg['ma_length'] + cfg['slope_lookback']} needed for a "
                       f"{cfg['ma_label']} read"),
        }

    stamps = list(df.index)
    closed = [period_is_closed(s, cfg["interval"], today) for s in stamps]
    excluded = None
    if closed and not closed[-1]:
        excluded = stamps[-1].date().isoformat()

    dates = [s.date().isoformat() for s in stamps]
    closes = [float(v) for v in df["Close"]]
    highs = [float(v) for v in df["High"]]
    lows = [float(v) for v in df["Low"]]
    volumes = [float(v) for v in df["Volume"]] if "Volume" in df else [0.0] * len(closes)

    last_open_close = closes[-1]
    last_open_date = dates[-1]

    n = len(closes) - (1 if excluded else 0)
    j_dates, j_closes, j_highs, j_lows, j_vol = (
        dates[:n], closes[:n], highs[:n], lows[:n], volumes[:n])

    ma = sma(j_closes, cfg["ma_length"])
    raw = [classify_bar(j_closes, j_highs, j_lows, ma, i, cfg) for i in range(n)]
    stages = confirmed_series(raw)
    runs = stage_runs(j_dates, stages)

    i = n - 1
    current = stages[i]
    since = runs[-1]["start"] if runs and runs[-1]["stage"] == current else None

    # The confirmed stage is what the pack reports, but the newest closed bar may
    # already read differently. That pending change is the most decision-relevant
    # thing on a weekly chart, and hiding it behind the confirmation rule leaves a
    # read that contradicts its own stated price position and slope.
    latest_raw = raw[i]
    pending = None
    if latest_raw is not None and latest_raw != current:
        run_len = 0
        j = i
        while j >= 0 and raw[j] == latest_raw:
            run_len += 1
            j -= 1
        pending = {
            "reads": latest_raw,
            "since": j_dates[max(i - run_len + 1, 0)],
            "bars_held": run_len,
            "bars_to_confirm": max(CONFIRM_BARS - run_len, 0),
        }

    read = {
        "timeframe": name,
        "status": "READ",
        "stage": current or "UNRESOLVED",
        "stage_word": STAGE_WORDS.get(current, "unresolved"),
        "moving_average": cfg["ma_label"],
        "moving_average_value": round(ma[i], 4) if ma[i] is not None else None,
        "price_position": (None if ma[i] is None else
                           ("above" if j_closes[i] >= ma[i] else "below")),
        "slope": slope_class(ma, i, cfg) or "UNRESOLVED",
        "slope_lookback_bars": cfg["slope_lookback"],
        "stage_since": since or "UNRESOLVED",
        "volume_vs_baseline": volume_context(j_vol, i),
        "invalidates_if": invalidation(j_closes, ma, i, cfg, current),
        "pending_change": pending or "NONE",
        "bars_used": n,
        "last_closed_bar": j_dates[i],
    }
    series = {
        "dates": j_dates, "closes": j_closes, "highs": j_highs, "lows": j_lows,
        "volumes": j_vol, "ma": ma, "stages": stages, "runs": runs,
        "excluded_bar": excluded,
        "excluded_close": last_open_close if excluded else None,
        "excluded_date": last_open_date if excluded else None,
        "ma_label": cfg["ma_label"],
    }
    return (read, series), None


# --- alignment -----------------------------------------------------------

EARLY_STAGES = {"Introduction", "Growth"}
LATE_STAGES = {"Mature", "Shake-out", "Decline"}


def align(business_stage, chart_stage):
    if not business_stage or business_stage == "UNRESOLVED":
        return "UNRESOLVED", "the business life-cycle stage was not supplied"
    if chart_stage in (None, TRANSITIONAL, "UNRESOLVED"):
        return "UNRESOLVED", "the monthly chart sits between stages"
    if business_stage in EARLY_STAGES:
        if chart_stage in (STAGE_1, STAGE_2):
            return "MOVING_TOGETHER", "a growing business in a rising chart"
        return ("MARKET_SEES_DAMAGE_FIRST",
                "the business still reads as growing while the chart has turned down")
    if business_stage in LATE_STAGES:
        if chart_stage == STAGE_1:
            return ("MARKET_HAS_NOT_PRICED_IT",
                    "the chart has gone nowhere while the business economics ran on")
        if chart_stage == STAGE_2:
            return ("LATE_AND_EXTENDED",
                    "the business has stopped growing into new capital while the "
                    "price has kept rising")
        return "MOVING_TOGETHER", "a business past its growth phase in a falling chart"
    return "UNRESOLVED", f"unrecognised business stage '{business_stage}'"


# --- SVG -----------------------------------------------------------------

W, H = 1000, 430
PAD_L, PAD_R, PAD_T, PAD_B = 62, 16, 26, 46
PRICE_H = 268
VOL_TOP = PAD_T + PRICE_H + 18
VOL_H = 56


def esc(text):
    return (str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def render_svg(ticker, name, cfg, series, currency, business_bands=None):
    dates, closes, ma = series["dates"], series["closes"], series["ma"]
    n = len(closes)
    if n < 2:
        return None

    lo = min(min(closes), min(v for v in ma if v is not None) if any(
        v is not None for v in ma) else min(closes))
    hi = max(max(closes), max(v for v in ma if v is not None) if any(
        v is not None for v in ma) else max(closes))
    if series["excluded_close"] is not None:
        lo, hi = min(lo, series["excluded_close"]), max(hi, series["excluded_close"])
    span = (hi - lo) or 1.0
    lo -= span * 0.06
    hi += span * 0.06
    span = hi - lo

    total = n + (1 if series["excluded_bar"] else 0)
    plot_w = W - PAD_L - PAD_R

    def x(i):
        return PAD_L + (plot_w * i / max(total - 1, 1))

    def y(v):
        return PAD_T + PRICE_H * (1 - (v - lo) / span)

    parts = [
        f'<svg viewBox="0 0 {W} {H}" width="100%" height="auto" role="img" '
        f'xmlns="http://www.w3.org/2000/svg" '
        f'aria-label="{esc(ticker)} {esc(name)} chart with '
        f'{esc(series["ma_label"])} and stage bands" '
        f'style="font-family:inherit;max-width:100%;height:auto">'
    ]

    # stage bands
    index_of = {d: i for i, d in enumerate(dates)}
    for run in series["runs"]:
        a, b = index_of.get(run["start"]), index_of.get(run["end"])
        if a is None or b is None:
            continue
        x0, x1 = x(a), x(min(b + 1, total - 1))
        token = STAGE_TOKEN.get(run["stage"], "--surface-2")
        parts.append(
            f'<rect x="{x0:.1f}" y="{PAD_T}" width="{max(x1 - x0, 1):.1f}" '
            f'height="{PRICE_H}" fill="var({token}, #EEE)" opacity="0.55"/>')
        # 78px is about the width of the label itself; anything narrower would have
        # its label spill into the neighbouring band and read as the wrong stage.
        if x1 - x0 > 78:
            label = f'{run["stage"].replace("STAGE_", "S")} · {run["start"][:7]}'
            # A label drawn from the left runs off the plot when its band ends at
            # the right edge, which is exactly where the current stage always is.
            right_edge = x1 > W - PAD_R - 70
            lx, anchor = ((x1 - 5, 'end') if right_edge else (x0 + 5, 'start'))
            parts.append(
                f'<text x="{lx:.1f}" y="{PAD_T + 14}" font-size="11" '
                f'text-anchor="{anchor}" '
                f'fill="var(--ink-3, #767C80)">{esc(label)}</text>')

    # business life-cycle bands, drawn as a thin strip under the price
    if business_bands:
        strip_y = PAD_T + PRICE_H + 2
        for band in business_bands:
            a, b = index_of.get(band.get("start")), index_of.get(band.get("end"))
            if a is None or b is None:
                continue
            x0, x1 = x(a), x(b)
            parts.append(
                f'<rect x="{x0:.1f}" y="{strip_y}" width="{max(x1 - x0, 1):.1f}" '
                f'height="6" fill="var(--accent, #1D4F3F)" opacity="0.35"/>')
            if x1 - x0 > 60:
                parts.append(
                    f'<text x="{x0 + 4:.1f}" y="{strip_y + 5}" font-size="9" '
                    f'fill="var(--ink-3, #767C80)">{esc(band.get("stage", ""))}</text>')

    # axes
    for k in range(5):
        v = lo + span * k / 4
        yy = y(v)
        parts.append(
            f'<line x1="{PAD_L}" y1="{yy:.1f}" x2="{W - PAD_R}" y2="{yy:.1f}" '
            f'stroke="var(--line-soft, #E4E1D7)" stroke-width="1"/>')
        parts.append(
            f'<text x="{PAD_L - 8}" y="{yy + 4:.1f}" font-size="11" text-anchor="end" '
            f'fill="var(--ink-3, #767C80)" style="font-variant-numeric:tabular-nums">'
            f'{v:,.0f}</text>')

    step = max(1, total // 6)
    for i in range(0, n, step):
        parts.append(
            f'<text x="{x(i):.1f}" y="{H - 10}" font-size="11" text-anchor="middle" '
            f'fill="var(--ink-3, #767C80)">{esc(dates[i][:7])}</text>')

    # volume
    vols = series["volumes"]
    vmax = max(vols) or 1.0
    bar_w = max(plot_w / max(total, 1) * 0.72, 0.7)
    for i, v in enumerate(vols):
        h = VOL_H * (v / vmax)
        parts.append(
            f'<rect x="{x(i) - bar_w / 2:.1f}" y="{VOL_TOP + VOL_H - h:.1f}" '
            f'width="{bar_w:.1f}" height="{h:.1f}" fill="var(--ink-3, #767C80)" '
            f'opacity="0.28"/>')
    base = sum(vols[-VOLUME_BASE:]) / min(len(vols), VOLUME_BASE)
    by = VOL_TOP + VOL_H - VOL_H * (base / vmax)
    parts.append(
        f'<line x1="{PAD_L}" y1="{by:.1f}" x2="{W - PAD_R}" y2="{by:.1f}" '
        f'stroke="var(--ink-3, #767C80)" stroke-width="1" stroke-dasharray="3 3" '
        f'opacity="0.7"/>')
    parts.append(
        f'<text x="{W - PAD_R}" y="{VOL_TOP - 4}" font-size="10" text-anchor="end" '
        f'fill="var(--ink-3, #767C80)">volume · {VOLUME_BASE}-bar average dashed</text>')

    # moving average, then price on top
    ma_points = " ".join(f"{x(i):.1f},{y(v):.1f}"
                         for i, v in enumerate(ma) if v is not None)
    if ma_points:
        parts.append(
            f'<polyline points="{ma_points}" fill="none" '
            f'stroke="var(--accent, #1D4F3F)" stroke-width="2" opacity="0.85"/>')
    price_points = " ".join(f"{x(i):.1f},{y(v):.1f}" for i, v in enumerate(closes))
    parts.append(
        f'<polyline points="{price_points}" fill="none" stroke="var(--ink, #16181A)" '
        f'stroke-width="1.7"/>')

    # the unclosed bar, drawn but visibly separate
    if series["excluded_close"] is not None:
        xi, yi = x(total - 1), y(series["excluded_close"])
        parts.append(
            f'<line x1="{x(n - 1):.1f}" y1="{y(closes[-1]):.1f}" x2="{xi:.1f}" '
            f'y2="{yi:.1f}" stroke="var(--ink, #16181A)" stroke-width="1.7" '
            f'stroke-dasharray="3 3" opacity="0.65"/>')
        parts.append(
            f'<circle cx="{xi:.1f}" cy="{yi:.1f}" r="3.2" fill="none" '
            f'stroke="var(--ink, #16181A)" stroke-width="1.5"/>')

    # stage_since marker
    runs = series["runs"]
    if runs:
        a = index_of.get(runs[-1]["start"])
        if a is not None:
            parts.append(
                f'<line x1="{x(a):.1f}" y1="{PAD_T}" x2="{x(a):.1f}" '
                f'y2="{PAD_T + PRICE_H}" stroke="var(--ink-2, #454A4D)" '
                f'stroke-width="1" stroke-dasharray="4 3" opacity="0.8"/>')
            label = (f'{runs[-1]["stage"].replace("STAGE_", "stage ")} '
                     f'since {runs[-1]["start"]}')
            near_right = x(a) > W - PAD_R - 150
            lx, anchor = ((x(a) - 6, 'end') if near_right else (x(a) + 5, 'start'))
            parts.append(
                f'<text x="{lx:.1f}" y="{PAD_T + PRICE_H - 6:.1f}" font-size="11" '
                f'text-anchor="{anchor}" '
                f'fill="var(--ink-2, #454A4D)">{esc(label)}</text>')

    parts.append(
        f'<text x="{PAD_L}" y="{PAD_T - 10}" font-size="12" '
        f'fill="var(--ink-2, #454A4D)">{esc(ticker)} · {esc(name)} · '
        f'{esc(series["ma_label"])} · {esc(currency)} · {n} closed bars</text>')
    parts.append("</svg>")
    return "".join(parts)


# --- pack ----------------------------------------------------------------

# The run's packs in order; the newest one on disk carries the fullest ledger.
UPSTREAM_PACKS = (
    "compounder_thesis_pack",
    "reinvestment_runway_pack",
    "economic_engine_pack",
    "market_growth_pack",
    "business_identity_pack",
)


def inherited_ledger(out_dir):
    """Every evidence entry the core layers recorded, in the order they recorded it."""
    for name in UPSTREAM_PACKS:
        path = Path(out_dir) / f"{name}.json"
        if not path.exists():
            continue
        try:
            doc = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        doc = doc.get(name, doc)
        entries = doc.get("evidence_ledger")
        if isinstance(entries, list) and entries:
            return list(entries)
    return []


def build(ticker, out_dir, business_stage=None, raw_business_stage=None,
          currency="", today=None):
    today = today or datetime.now(timezone.utc).date()
    reads, series, unavailable = {}, {}, []

    for name, cfg in TIMEFRAMES.items():
        result, missing = read_timeframe(ticker, name, cfg, today)
        if missing:
            unavailable.append(missing)
            continue
        read, s = result
        reads[name] = read
        series[name] = s

    if not reads:
        raise SystemExit(f"no usable bars for {ticker}: {unavailable}")

    monthly = reads.get("monthly", {})
    weekly = reads.get("weekly", {})
    alignment, why = align(business_stage, monthly.get("stage"))

    clauses = []
    if monthly and weekly and monthly.get("stage") != weekly.get("stage"):
        clauses.append(f"monthly reads {monthly.get('stage')} since "
                       f"{monthly.get('stage_since')}; weekly reads "
                       f"{weekly.get('stage')} since {weekly.get('stage_since')}")
    for name, r in reads.items():
        change = r.get("pending_change")
        if isinstance(change, dict):
            clauses.append(f"the newest closed {name} bar reads {change['reads']} "
                           f"({change['bars_held']} bar(s) held, "
                           f"{change['bars_to_confirm']} more to confirm)")
    conflict = "; ".join(clauses) if clauses else "NONE"

    assets = []
    for name, s in series.items():
        svg = render_svg(ticker, name, TIMEFRAMES[name], s, currency or "price")
        assets.append({
            "timeframe": name,
            "source": "RENDERED_SVG",
            "captured_on": today.isoformat(),
            "interval": TIMEFRAMES[name]["interval"],
            "bars": len(s["closes"]),
            "moving_average": s["ma_label"],
            "asset": svg,
            "caption": (f"{ticker} · {name} · {s['ma_label']} · "
                        f"rendered {today.isoformat()}"),
        })

    # One ledger per run, appended and never replaced: this layer inherits every
    # entry the core layers recorded and adds its own on the end. Starting a fresh
    # list here would drop the audit trail, and the pack validator rejects it.
    ledger = inherited_ledger(out_dir)
    for name, s in series.items():
        ledger.append({
            "id": f"P{sum(1 for e in ledger if str(e.get('id', '')).startswith('P')) + 1:02d}",
            "claim": (f"{ticker} {name} closes and volume, {len(s['closes'])} closed "
                      f"bars to {s['dates'][-1]}"),
            "class": "FACT",
            "source": "Yahoo Finance via yfinance",
            "locator": f"interval={TIMEFRAMES[name]['interval']}, "
                       f"period={TIMEFRAMES[name]['period']}, auto_adjust=True",
            "as_of": today.isoformat(),
            "origin_layer": "stage_pack",
            "limitation": ("unofficial endpoint; split- and dividend-adjusted series "
                           "are restated retroactively, so a figure quoted from an "
                           "older run may not reproduce"),
        })

    last_close = None
    for name in ("weekly", "monthly"):
        s = series.get(name)
        if s:
            last_close = s["excluded_close"] if s["excluded_close"] is not None \
                else s["closes"][-1]
            break

    pack = {
        "schema_version": "future-compounder-v2.2",
        "as_of": today.isoformat(),
        "ticker": ticker,
        "price_context": {
            "last_close": round(last_close, 4) if last_close is not None else None,
            "currency": currency or "UNRESOLVED",
            "as_of": today.isoformat(),
        },
        "monthly_read": monthly or "UNAVAILABLE",
        "weekly_read": weekly or "UNAVAILABLE",
        "stage_conflict": conflict,
        "business_stage": {
            "adjusted": business_stage or "UNRESOLVED",
            "raw": raw_business_stage or business_stage or "UNRESOLVED",
            "source": "economic_engine_pack.life_cycle_stage",
        },
        "stage_alignment": {
            "reading": alignment,
            "because": why,
            "sentence": "UNRESOLVED — write this in the report from the two reads",
        },
        "chart_assets": assets,
        "data_quality": {
            "unclosed_bar_excluded": {
                name: s["excluded_bar"] for name, s in series.items()
            },
            "bars_used": {name: len(s["closes"]) for name, s in series.items()},
            "unavailable_timeframes": unavailable,
            "adjustment": "split- and dividend-adjusted closes (yfinance auto_adjust)",
            "source": "yfinance — unofficial Yahoo Finance data, cross-check before use",
        },
        "evidence_ledger": ledger,
    }

    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "stage_pack.json").write_text(
        json.dumps(pack, ensure_ascii=False, indent=2), encoding="utf-8")
    return pack


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("ticker")
    ap.add_argument("--out", required=True, help="run directory to write stage_pack.json into")
    ap.add_argument("--business-stage", default=None,
                    help="adjusted life_cycle_stage from economic_engine_pack")
    ap.add_argument("--raw-business-stage", default=None)
    ap.add_argument("--currency", default="")
    args = ap.parse_args(argv)

    business = args.business_stage
    raw = args.raw_business_stage
    engine = Path(args.out) / "economic_engine_pack.json"
    if business is None and engine.exists():
        doc = json.loads(engine.read_text(encoding="utf-8"))
        doc = doc.get("economic_engine_pack", doc)
        lc = doc.get("life_cycle_stage") or {}
        business = lc.get("stage")
        raw = raw or lc.get("raw_stage")

    pack = build(args.ticker, args.out, business, raw, args.currency)
    m, w = pack["monthly_read"], pack["weekly_read"]
    print(f"{args.ticker}: monthly {m.get('stage')} since {m.get('stage_since')} · "
          f"weekly {w.get('stage')} since {w.get('stage_since')} · "
          f"alignment {pack['stage_alignment']['reading']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
