#!/usr/bin/env python3
"""
ta_engine.py - Technical Analysis v2 / v2.1: screenshot-free engine (Entry / Exit / Breakout / Short).

Claude Code rebuild of the project doc `claude/ta-engine.py`, which is not reachable from
Claude Code. Written from the master-prompt spec (M1-M9, M10 log row + score_call).
Every number in a brief comes from this file's output or a live tool, labelled.

Indicators match the TradingView defaults the master prompt names:
  EMA 9/21/20/50/200 (ta.ema), SMA 200, Bollinger 20/2 (population stdev), RSI 14 (ta.rma)
  + SMA 9 signal, ATR 14 (ta.rma of true range), OBV + EMA 13 signal, 20D volume SMA.
  AVWAP = anchored VWAP on hlc3 from the anchor bar (inclusive).

Usage (see --help):
  python3 ta_engine.py data/1810.json --warmup data/1810_warmup.json --asof 2026-11-04 \
      --nlv <NLV_USD> --risk 0.5 --fx <USDMYR> --ccy HKD --usd-local <USDHKD> --lot 200 \
      --bench data/HSTECH.json data/HSI.json data/QQQ.json --earnings 2026-11-24 \
      --book <path outside repo>/book.json --json <path outside repo>/out.json
  Account and client inputs (--nlv, --book, --acel-*) are runtime arguments only; never commit them.
"""
import argparse
import json
import math
import sys

import numpy as np
import pandas as pd

VERSION = "2.0-cc (rebuilt from master-prompt spec, 05/11/2026)"
FIB_R = [0.236, 0.382, 0.5, 0.618, 0.786]
FIB_X = [1.272, 1.618]


# ----------------------------------------------------------------------------- data
class ChecksumError(Exception):
    pass


def load_bars(path, closes_only=False):
    """Load a TradingView get-ohlcv (format=columns) dump and assert its summary checksum."""
    d = json.load(open(path))
    s = d.get("summary", {})
    n = len(d["t"])
    keys = ["t", "c"] if closes_only else ["t", "o", "h", "l", "c"]
    errs = []
    for k in keys:
        if d.get(k) is None or len(d[k]) != n:
            errs.append(f"len({k}) != len(t)={n}")
    if d.get("v") is not None and not closes_only and len(d["v"]) != n:
        errs.append("len(v) != len(t)")
    if "count" in s and s["count"] != n:
        errs.append(f"count {s['count']} != {n}")
    if not closes_only:
        if "high" in s and not math.isclose(max(d["h"]), s["high"], abs_tol=1e-9):
            errs.append(f"high {max(d['h'])} != {s['high']}")
        if "low" in s and not math.isclose(min(d["l"]), s["low"], abs_tol=1e-9):
            errs.append(f"low {min(d['l'])} != {s['low']}")
        if "first_open" in s and not math.isclose(d["o"][0], s["first_open"], abs_tol=1e-9):
            errs.append("first_open mismatch")
        if d.get("v") and "total_volume" in s and int(round(sum(d["v"]))) != int(s["total_volume"]):
            errs.append(f"total_volume {int(round(sum(d['v'])))} != {s['total_volume']}")
        bad = [i for i in range(n) if not (d["l"][i] <= min(d["o"][i], d["c"][i]) + 1e-9
                                           and d["h"][i] >= max(d["o"][i], d["c"][i]) - 1e-9)]
        if bad:
            errs.append(f"OHLC inconsistent at {bad[:5]}")
    else:
        if "high" in s and max(d["c"]) > s["high"] + 1e-9:
            errs.append("close above period high")
        if "low" in s and min(d["c"]) < s["low"] - 1e-9:
            errs.append("close below period low")
    if "last_close" in s and not math.isclose(d["c"][-1], s["last_close"], abs_tol=1e-9):
        errs.append(f"last_close {d['c'][-1]} != {s['last_close']}")
    if "first_t" in s and d["t"][0] != s["first_t"]:
        errs.append("first_t mismatch")
    if "last_t" in s and d["t"][-1] != s["last_t"]:
        errs.append("last_t mismatch")
    if any(b <= a for a, b in zip(d["t"], d["t"][1:])):
        errs.append("t not strictly increasing")
    if errs:
        raise ChecksumError(f"{path}: " + "; ".join(errs))
    idx = pd.DatetimeIndex(pd.to_datetime(d["t"], unit="s").normalize(), name="date")
    df = pd.DataFrame({"c": d["c"]}, index=idx, dtype=float)
    if not closes_only:
        for k in "ohl":
            df[k] = np.asarray(d[k], dtype=float)
        df["v"] = np.asarray(d["v"], dtype=float) if d.get("v") else np.nan
    return df, d.get("symbol", path)


# ----------------------------------------------------------------------- indicators
def ema(s, n):
    return s.ewm(span=n, adjust=False).mean()


def sma(s, n):
    return s.rolling(n).mean()


def rma(s, n):
    """TradingView ta.rma: seeded with the SMA of the first n values, then Wilder smoothing."""
    vals = s.to_numpy(dtype=float)
    out = np.full(len(vals), np.nan)
    ok = np.where(~np.isnan(vals))[0]
    if len(ok) < n:
        return pd.Series(out, index=s.index)
    first = ok[0]
    start = first + n - 1
    out[start] = vals[first:start + 1].mean()
    for i in range(start + 1, len(vals)):
        out[i] = (out[i - 1] * (n - 1) + vals[i]) / n
    return pd.Series(out, index=s.index)


def rsi(c, n=14):
    ch = c.diff()
    up = rma(ch.clip(lower=0), n)
    dn = rma((-ch).clip(lower=0), n)
    r = 100 - 100 / (1 + up / dn)
    r = r.where(dn != 0, 100.0)
    return r


def true_range(df):
    pc = df["c"].shift(1)
    tr = pd.concat([df["h"] - df["l"], (df["h"] - pc).abs(), (df["l"] - pc).abs()], axis=1).max(axis=1)
    tr.iloc[0] = df["h"].iloc[0] - df["l"].iloc[0]
    return tr


def obv(df):
    sign = np.sign(df["c"].diff()).fillna(0)
    return (sign * df["v"]).cumsum()


def pivots(h, l, left, right, upto):
    """Confirmed pivots up to index `upto` (needs `right` bars after). Returns (highs, lows) index lists."""
    ph, pl = [], []
    for i in range(left, upto - right + 1):
        if h[i] > h[i - left:i].max() and h[i] >= h[i + 1:i + right + 1].max():
            ph.append(i)
        if l[i] < l[i - left:i].min() and l[i] <= l[i + 1:i + right + 1].min():
            pl.append(i)
    return ph, pl


def zigzag(ph, pl, h, l):
    """Alternating pivot sequence [(idx, 'H'|'L', price)]; consecutive same-type keeps the extreme."""
    ev = sorted([(i, "H", h[i]) for i in ph] + [(i, "L", l[i]) for i in pl])
    zz = []
    for e in ev:
        if zz and zz[-1][1] == e[1]:
            if (e[1] == "H" and e[2] >= zz[-1][2]) or (e[1] == "L" and e[2] <= zz[-1][2]):
                zz[-1] = e
        else:
            zz.append(e)
    return zz


def atr_zigzag(H, L, atr, mult=3.0, start=0):
    """Swing pivots where each reversal is >= mult x ATR (ATR at the reversal bar).
    Returns (pivots [(idx, 'H'|'L', price)], active_extreme (idx, type, price))."""
    piv = []
    trend, ext_i, ext_p = None, start, None
    hi_i, lo_i = start, start
    for k in range(start, len(H)):
        if np.isnan(atr[k]):
            continue
        thr = mult * atr[k]
        if trend is None:
            if H[k] > H[hi_i]:
                hi_i = k
            if L[k] < L[lo_i]:
                lo_i = k
            if H[hi_i] - L[lo_i] >= thr:
                if hi_i > lo_i:
                    piv.append((lo_i, "L", L[lo_i]))
                    trend, ext_i, ext_p = "up", hi_i, H[hi_i]
                else:
                    piv.append((hi_i, "H", H[hi_i]))
                    trend, ext_i, ext_p = "down", lo_i, L[lo_i]
            continue
        if trend == "up":
            if H[k] >= ext_p:
                ext_i, ext_p = k, H[k]
            elif ext_p - L[k] >= thr:
                piv.append((ext_i, "H", ext_p))
                trend, ext_i, ext_p = "down", k, L[k]
        else:
            if L[k] <= ext_p:
                ext_i, ext_p = k, L[k]
            elif H[k] - ext_p >= thr:
                piv.append((ext_i, "L", ext_p))
                trend, ext_i, ext_p = "up", k, H[k]
    active = (ext_i, "H" if trend == "up" else "L", ext_p) if trend else None
    return piv, active


def avwap(df, anchor_pos):
    tp = (df["h"] + df["l"] + df["c"]) / 3
    pv = (tp * df["v"]).iloc[anchor_pos:].cumsum()
    vv = df["v"].iloc[anchor_pos:].cumsum()
    return pv / vv


def fib_levels(lo, hi, direction, extensions=False):
    """direction 'up' = swing low->high (levels are pullback supports below the high);
    'down' = swing high->low (levels are retracement resistances above the low)."""
    rng = hi - lo
    lv = {}
    for r in FIB_R:
        lv[f"{r * 100:.1f}%"] = hi - r * rng if direction == "up" else lo + r * rng
    if extensions:
        for x in FIB_X:
            lv[f"x{x}"] = lo + x * rng if direction == "up" else hi - x * rng
    return lv


def busdays_between(d0, d1, holidays=()):
    """Sessions after d0 up to and including d1 (Mon-Fri, minus holidays)."""
    a = (pd.Timestamp(d0) + pd.Timedelta(days=1)).date()
    b = (pd.Timestamp(d1) + pd.Timedelta(days=1)).date()
    return int(np.busday_count(a, b, holidays=list(holidays)))


def norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def r2(x, nd=2):
    if x is None or (isinstance(x, float) and (math.isnan(x) or math.isinf(x))):
        return None
    return round(float(x), nd)


# --------------------------------------------------------------------------- engine
def run(a):
    df, sym = load_bars(a.data)
    checks = ["summary checksum OK: " + a.data]
    closes_full = df["c"].copy()
    if a.warmup:
        w, _ = load_bars(a.warmup, closes_only=True)
        if w.index[-1] >= df.index[0]:
            raise ChecksumError("warm-up overlaps the main window")
        closes_full = pd.concat([w["c"], df["c"]])
        checks.append(f"warm-up closes OK: {a.warmup} ({len(w)} bars before {df.index[0].date()})")

    asof = pd.Timestamp(a.asof) if a.asof else df.index[-1]
    dropped = df.index[df.index > asof]
    df = df.loc[df.index <= asof].copy()
    closes_full = closes_full.loc[closes_full.index <= asof]
    n = len(df)
    i = n - 1
    D = df.index
    c, h, l, v = df["c"], df["h"], df["l"], df["v"]
    H, L, C = h.to_numpy(), l.to_numpy(), c.to_numpy()

    # ---- indicators (close-based ones use warm-up history so EMA200 is converged)
    ind = pd.DataFrame(index=D)
    for p in (9, 21, 20, 50, 200):
        ind[f"ema{p}"] = ema(closes_full, p).reindex(D)
    ind["sma200"] = sma(closes_full, 200).reindex(D)
    bb_mid = sma(closes_full, 20)
    bb_sd = closes_full.rolling(20).std(ddof=0)
    ind["bb_mid"] = bb_mid.reindex(D)
    ind["bb_up"] = (bb_mid + 2 * bb_sd).reindex(D)
    ind["bb_lo"] = (bb_mid - 2 * bb_sd).reindex(D)
    ind["rsi"] = rsi(closes_full, 14).reindex(D)
    ind["rsi_sig"] = sma(ind["rsi"], 9)
    ind["atr"] = rma(true_range(df), 14)
    ind["obv"] = obv(df)
    ind["obv_sig"] = ema(ind["obv"], 13)
    ind["vma20"] = sma(v, 20)
    last = ind.iloc[i]
    ATR = float(last["atr"])
    px = float(C[i])

    # ---- structure
    win = min(400, n)
    w0 = n - win
    cyc_hi_pos = w0 + int(np.argmax(H[w0:]))
    cyc_lo_pos = w0 + int(np.argmin(L[w0:]))
    yr = df.loc[df.index > asof - pd.Timedelta(days=365)]
    hi52, lo52 = float(yr["h"].max()), float(yr["l"].min())
    ph, pl = pivots(H, L, 5, 5, i)
    zz = zigzag(ph, pl, H, L)

    # ---- AVWAP anchors
    anchors = []
    for s_ in (a.avwap or []):
        pos = int(D.searchsorted(pd.Timestamp(s_)))
        anchors.append((f"AVWAP {D[pos].strftime('%d/%m/%y')} (user)", pos))
    if not anchors:
        anchors.append((f"AVWAP cycle high {D[cyc_hi_pos].strftime('%d/%m/%y')}", cyc_hi_pos))
        if pl:
            anchors.append((f"AVWAP swing low {D[pl[-1]].strftime('%d/%m/%y')}", pl[-1]))
    av = {}
    for name, pos in anchors:
        av[name] = {"anchor": str(D[pos].date()), "value": float(avwap(df, pos).iloc[-1]), "pos": pos}
    av_cyc = next((x["value"] for k, x in av.items() if "cycle high" in k), None)

    # ---- FIB: MACRO (cycle low <-> cycle high) and TACTICAL (last leg >= 3 ATR)
    if a.fib:
        lo_p = int(D.searchsorted(pd.Timestamp(a.fib[0])))
        hi_p = int(D.searchsorted(pd.Timestamp(a.fib[1])))
        macro = {"lo": float(L[lo_p]), "hi": float(H[hi_p]), "lo_date": str(D[lo_p].date()),
                 "hi_date": str(D[hi_p].date()), "dir": "up" if lo_p < hi_p else "down", "src": "user"}
    else:
        macro = {"lo": float(L[cyc_lo_pos]), "hi": float(H[cyc_hi_pos]), "lo_date": str(D[cyc_lo_pos].date()),
                 "hi_date": str(D[cyc_hi_pos].date()), "dir": "up" if cyc_lo_pos < cyc_hi_pos else "down",
                 "src": "engine 400-bar cycle"}
    macro["levels"] = fib_levels(macro["lo"], macro["hi"], macro["dir"])

    # TACTICAL = last swing >= 3x ATR on a zigzag whose reversals are >= 3x ATR (minor
    # pullbacks inside a leg do not restart it); active leg if it already spans >= 3x ATR.
    tactical = None
    zpiv, zact = atr_zigzag(H, L, ind["atr"].to_numpy(), 3.0, start=w0)
    legs = []
    if zpiv and zact:
        p0, t0, x0 = zpiv[-1]
        legs.append(("up" if t0 == "L" else "down", p0, zact[0], x0, zact[2], True))
        for k in range(len(zpiv) - 1, 0, -1):
            (q0, s0, y0), (q1, s1, y1) = zpiv[k - 1], zpiv[k]
            legs.append(("up" if s0 == "L" else "down", q0, q1, y0, y1, False))
    for dirn, p0, p1, x0, x1, act in legs:
        if abs(x1 - x0) >= 3 * ATR:
            lo_, hi_ = (x0, x1) if dirn == "up" else (x1, x0)
            tactical = {"dir": dirn, "lo": float(lo_), "hi": float(hi_), "from": str(D[p0].date()), "to": str(D[p1].date()),
                        "active_leg": act, "range_atr": r2(abs(x1 - x0) / ATR), "method": "3xATR-reversal zigzag"}
            tactical["levels"] = fib_levels(lo_, hi_, dirn, extensions=True)
            break

    # ---- confluence components
    comps = []

    def add(p, label, w=1.0, kind="line", force=False):
        if p is None or (isinstance(p, float) and math.isnan(p)):
            return
        comps.append({"p": float(p), "label": label, "w": w, "kind": kind, "force": force})

    for nm, col in [("EMA9", "ema9"), ("EMA21", "ema21"), ("EMA20", "ema20"), ("EMA50", "ema50"),
                    ("EMA200", "ema200"), ("SMA200", "sma200"), ("BB upper", "bb_up"), ("BB lower", "bb_lo")]:
        add(last[col], nm)
    for nm, x in av.items():
        add(x["value"], nm, kind="avwap")
    for k, p in macro["levels"].items():
        add(p, f"MACRO fib {k}", kind="fib")
    if tactical:
        for k, p in tactical["levels"].items():
            add(p, f"TAC fib {k}", kind="fib")
    for j in ph:
        if j >= w0:
            add(H[j], f"swing high {D[j].strftime('%d/%m/%y')}", kind="swing")
    for j in pl:
        if j >= w0:
            add(L[j], f"swing low {D[j].strftime('%d/%m/%y')}", kind="swing")
    add(H[cyc_hi_pos], f"cycle high {D[cyc_hi_pos].strftime('%d/%m/%y')}", kind="extreme", force=True)
    add(L[cyc_lo_pos], f"cycle low {D[cyc_lo_pos].strftime('%d/%m/%y')}", kind="extreme", force=True)
    add(hi52, "52W high", kind="extreme", force=True)
    add(lo52, "52W low", kind="extreme", force=True)
    step = a.round_step or (10 ** math.floor(math.log10(px)) / 2)
    k0 = math.floor(px * 0.6 / step)
    for k in range(k0, k0 + int(px * 0.9 / step) + 2):
        rp = k * step
        if 0.6 * px <= rp <= 1.5 * px:
            add(rp, f"round {rp:g}", w=0.5, kind="round")

    # ---- cluster into zones <= 0.5 ATR wide
    comps.sort(key=lambda x: x["p"])
    zones = []
    for cp in comps:
        if zones and cp["p"] - zones[-1]["lo"] <= a.zone_atr * ATR:
            z = zones[-1]
            z["items"].append(cp)
            z["hi"] = cp["p"]
        else:
            zones.append({"lo": cp["p"], "hi": cp["p"], "items": [cp]})
    for z in zones:
        z["n"] = sum(x["w"] for x in z["items"])
        z["force"] = any(x["force"] for x in z["items"])
        z["components"] = [x["label"] for x in z["items"]]
        if z["lo"] <= px <= z["hi"]:
            dist = 0.0
        elif z["lo"] > px:
            dist = z["lo"] - px
        else:
            dist = z["hi"] - px
        z["dist"] = dist
        z["dist_pct"] = dist / px * 100
        z["dist_atr"] = dist / ATR
        z["at_price"] = (z["lo"] - 0.5 * ATR) <= px <= (z["hi"] + 0.5 * ATR)
        z["side"] = "AT" if z["at_price"] else ("R" if z["lo"] > px else "S")
        z["touched_today"] = z["lo"] <= H[i] and z["hi"] >= L[i]

    def ztxt(z):
        return f"{z['lo']:.2f}-{z['hi']:.2f}" if z["hi"] - z["lo"] > 1e-9 else f"{z['lo']:.2f}"

    def is_target(z, min_n):
        return z["n"] >= min_n or z["force"]

    def targets_above(p, min_n):
        return sorted([z for z in zones if z["lo"] > p + 1e-9 and is_target(z, min_n)], key=lambda z: z["lo"])

    def targets_below(p, min_n):
        return sorted([z for z in zones if z["hi"] < p - 1e-9 and is_target(z, min_n)], key=lambda z: -z["hi"])

    # Mean-reversion targets (plans A, S, live setups) are measured beyond the AT-PRICE band:
    # the trade expects a move back through the current congestion to the next level.
    # Calibrated on the 17/07/2026 MU validation-log fade (T1 816.57 / T2 750, not the at-price 937).
    at_top = max([z["hi"] for z in zones if z["at_price"]] + [px])
    at_bot = min([z["lo"] for z in zones if z["at_price"]] + [px])

    def targets_up_beyond(p, min_n):
        floor_ = max(p, at_top)
        return sorted([z for z in zones if z["lo"] > floor_ + 1e-9 and is_target(z, min_n)], key=lambda z: z["lo"])

    def targets_down_beyond(p, min_n):
        ceil_ = min(p, at_bot)
        return sorted([z for z in zones if z["hi"] < ceil_ - 1e-9 and is_target(z, min_n)], key=lambda z: -z["hi"])

    def next_zone_up(z0):
        """T2: the next zone of any strength beyond the T1 zone (log: fade T2 = lone round 750)."""
        nz = sorted([x for x in zones if x["lo"] > z0["hi"] + 1e-9], key=lambda x: x["lo"])
        return nz[0]["lo"] if nz else None

    def next_zone_down(z0):
        nz = sorted([x for x in zones if x["hi"] < z0["lo"] - 1e-9], key=lambda x: -x["hi"])
        return nz[0]["hi"] if nz else None

    res_zones = sorted([z for z in zones if z["lo"] > px and z["n"] >= 2], key=lambda z: z["lo"])
    sup_zones = sorted([z for z in zones if z["hi"] < px and z["n"] >= 2], key=lambda z: -z["hi"])
    at_zones = [z for z in zones if z["at_price"]]
    near = [z for z in zones if abs(z["dist_atr"]) <= 2.0]
    lis = max(near, key=lambda z: (z["n"], -abs(z["dist"]))) if near else None

    # ---- M1 phase (daily)
    def rising(s, k=5):
        return bool(s.iloc[-1] > s.iloc[-1 - k])

    def falling(s, k=5):
        return bool(s.iloc[-1] < s.iloc[-1 - k])

    e20, e50, e200 = ind["ema20"], ind["ema50"], ind["ema200"]
    plv = [L[j] for j in pl]
    lower_low = (len(plv) >= 2 and plv[-1] < plv[-2]) or (len(plv) >= 1 and L[max(0, i - 4):i + 1].min() < plv[-1])
    no_lower_low = not lower_low
    uptrend_ctx = bool(e50.iloc[-1] > e200.iloc[-1]) and rising(e50)
    flat20 = abs(e20.iloc[-1] - e20.iloc[-11]) < 0.5 * ATR
    rng20 = float(H[i - 19:i + 1].max() - L[i - 19:i + 1].min())
    obv_rising = bool(ind["obv_sig"].iloc[-1] > ind["obv_sig"].iloc[-11])

    # ---- M4 RSI + M5 OBV divergences across the last two confirmed pivots
    def div_scan(series, kind, thr):
        out = {}
        R = series.to_numpy()
        for side, piv, arr in (("high", ph, H), ("low", pl, L)):
            res = {"status": "NONE"}
            if len(piv) >= 2:
                p1, p2 = piv[-2], piv[-1]
                x1, x2, y1, y2 = arr[p1], arr[p2], R[p1], R[p2]
                res.update({"p1": str(D[p1].date()), "p2": str(D[p2].date()), "price1": r2(x1), "price2": r2(x2),
                            "ind1": r2(y1, 2 if kind == "rsi" else 0), "ind2": r2(y2, 2 if kind == "rsi" else 0),
                            "age_bars": i - p2})
                typ = None
                hidden_ok = kind == "rsi"  # OBV: regular divergence only (spec M5)
                if side == "high":
                    if x2 > x1 and y2 < y1:
                        typ = "regular bearish"
                    elif x2 < x1 and y2 > y1:
                        typ = "hidden bearish" if hidden_ok else None
                        if not hidden_ok:
                            res["note"] = "price lower high, OBV higher high: volume leading price (no regular divergence)"
                else:
                    if x2 < x1 and y2 > y1:
                        typ = "regular bullish"
                    elif x2 > x1 and y2 < y1:
                        typ = "hidden bullish" if hidden_ok else None
                        if not hidden_ok:
                            res["note"] = "price higher low, OBV lower low: volume lagging price (no regular divergence)"
                if typ is None and "note" not in res:
                    res["note"] = "confirmation (price and indicator same direction)"
                if typ:
                    diff = abs(y2 - y1)
                    res["type"] = typ
                    res["diff"] = r2(diff, 2 if kind == "rsi" else 0)
                    if kind == "rsi":
                        res["status"] = "CONFIRMED" if diff >= thr else "MARGINAL"
                    else:
                        res["status"] = "CONFIRMED"
                    after = C[p2 + 1:i + 1]
                    if typ == "hidden bearish" and len(after) and after.max() > x1:
                        res["status"] = "VOID"
                        res["void_reason"] = f"close {after.max():.2f} above pivot-1 high {x1:.2f}"
                    if typ == "hidden bullish" and len(after) and after.min() < x1:
                        res["status"] = "VOID"
                        res["void_reason"] = f"close {after.min():.2f} below pivot-1 low {x1:.2f}"
            # pending: an unconfirmed extreme in the last 5 bars vs the last confirmed pivot
            if piv:
                p2 = piv[-1]
                lo5 = max(p2 + 1, i - 4)
                if lo5 <= i:
                    if side == "high":
                        q = lo5 + int(np.argmax(H[lo5:i + 1]))
                        if H[q] > arr[p2] and R[q] < R[p2]:
                            res["pending"] = {"type": "regular bearish", "bar": str(D[q].date()), "price": r2(H[q]),
                                              "ind": r2(R[q], 2 if kind == "rsi" else 0),
                                              "vs": r2(R[p2], 2 if kind == "rsi" else 0)}
                    else:
                        q = lo5 + int(np.argmin(L[lo5:i + 1]))
                        if L[q] < arr[p2] and R[q] > R[p2]:
                            res["pending"] = {"type": "regular bullish", "bar": str(D[q].date()), "price": r2(L[q]),
                                              "ind": r2(R[q], 2 if kind == "rsi" else 0),
                                              "vs": r2(R[p2], 2 if kind == "rsi" else 0)}
                    if "pending" in res:
                        pdiff = abs(res["pending"]["ind"] - res["pending"]["vs"])
                        if kind == "rsi" and pdiff < thr:
                            res["pending"]["grade"] = f"MARGINAL ({pdiff:.2f} pts < {thr:g})"
                        if res["status"] == "NONE":
                            res["status"] = "PENDING" if not (kind == "rsi" and pdiff < thr) else "PENDING-MARGINAL"
            out[side] = res
        return out

    rsi_div = div_scan(ind["rsi"], "rsi", a.div_pts)
    obv_div = div_scan(ind["obv"], "obv", 0)
    bull_div = any(x.get("status") == "CONFIRMED" and "bullish" in x.get("type", "") for x in rsi_div.values()) or \
        any(x.get("status") == "CONFIRMED" and x.get("type") == "regular bullish" for x in obv_div.values())
    bear_rsi_obv = (rsi_div["high"].get("status") == "CONFIRMED" and rsi_div["high"].get("type") == "regular bearish"
                    and obv_div["high"].get("type") == "regular bearish")

    rules = {
        "MARKUP": bool(px > e20.iloc[-1] > e50.iloc[-1] > e200.iloc[-1]) and rising(e20) and no_lower_low,
        "EARLY MARKDOWN": uptrend_ctx and px < e50.iloc[-1] and av_cyc is not None and px < av_cyc and lower_low,
        "MARKDOWN": bool(e20.iloc[-1] < e50.iloc[-1]) and falling(e20) and px < e50.iloc[-1],
        "DISTRIBUTION": uptrend_ctx and (px < e20.iloc[-1] or bear_rsi_obv) and px >= e50.iloc[-1],
        "ACCUMULATION": px < e50.iloc[-1] and px < e200.iloc[-1] and rng20 < 6 * ATR and flat20 and (obv_rising or bull_div),
    }
    phase_d = next((k for k, ok in rules.items() if ok), "TRANSITION")

    # ---- weekly phase (resampled; EMA 10/20/40)
    wk = df.resample("W-FRI").agg({"o": "first", "h": "max", "l": "min", "c": "last", "v": "sum"}).dropna(subset=["c"])
    wc_full = closes_full.resample("W-FRI").last().dropna()
    we10, we20, we40 = (ema(wc_full, p).reindex(wk.index) for p in (10, 20, 40))
    watr = rma(true_range(wk), 14)
    WH, WL = wk["h"].to_numpy(), wk["l"].to_numpy()
    wph, wpl = pivots(WH, WL, 2, 2, len(wk) - 1)
    wplv = [WL[j] for j in wpl]
    w_ll = (len(wplv) >= 2 and wplv[-1] < wplv[-2]) or (len(wplv) >= 1 and WL[-2:].min() < wplv[-1])
    wpx = float(wk["c"].iloc[-1])
    wA = float(watr.iloc[-1])
    w_up_ctx = bool(we20.iloc[-1] > we40.iloc[-1]) and bool(we20.iloc[-1] > we20.iloc[-4])
    w_rules = {
        "MARKUP": bool(wpx > we10.iloc[-1] > we20.iloc[-1] > we40.iloc[-1]) and bool(we10.iloc[-1] > we10.iloc[-3]) and not w_ll,
        "EARLY MARKDOWN": w_up_ctx and wpx < we20.iloc[-1] and w_ll,
        "MARKDOWN": bool(we10.iloc[-1] < we20.iloc[-1]) and bool(we10.iloc[-1] < we10.iloc[-3]) and wpx < we20.iloc[-1],
        "DISTRIBUTION": w_up_ctx and wpx < we10.iloc[-1] and wpx >= we20.iloc[-1],
        "ACCUMULATION": wpx < we20.iloc[-1] and wpx < we40.iloc[-1] and float(WH[-8:].max() - WL[-8:].min()) < 6 * wA
                        and abs(we10.iloc[-1] - we10.iloc[-5]) < 0.5 * wA,
    }
    phase_w = next((k for k, ok in w_rules.items() if ok), "TRANSITION")
    bias = {"MARKUP": 1, "ACCUMULATION": 0.5, "TRANSITION": 0, "DISTRIBUTION": -0.5, "EARLY MARKDOWN": -1, "MARKDOWN": -1}

    # ---- M2 fib position
    def fib_pos(fb):
        if not fb:
            return None
        ends = {"0% (low)" if fb["dir"] == "down" else "100% (low)": fb["lo"],
                "100% (high)" if fb["dir"] == "down" else "0% (high)": fb["hi"]}
        lv = sorted(list(fb["levels"].items()) + list(ends.items()), key=lambda kv: kv[1])
        up = next(((k, p) for k, p in lv if p > px), None)
        dn = next(((k, p) for k, p in reversed(lv) if p <= px), None)
        lab = "IN BAND"
        for k, p in sorted(lv, key=lambda kv: -abs(kv[1] - px)):  # nearest qualifying level wins
            was_below = (C[max(0, i - 5):i] < p).any()
            was_above = (C[max(0, i - 5):i] > p).any()
            if px >= p + 0.25 * ATR and was_below:
                lab = f"BREAKOUT over {k} ({p:.2f})"
            elif px <= p - 0.25 * ATR and was_above:
                lab = f"LOST LEVEL {k} ({p:.2f})"
        for k, p in lv:
            if abs(px - p) <= 0.25 * ATR:
                lab = f"RETEST {k} ({p:.2f})"
        return {"band": f"{dn[0] if dn else 'below all'} {dn[1]:.2f} -> {up[0] if up else 'above all'} {up[1]:.2f}"
                if dn and up else ("above all levels" if dn else "below all levels"),
                "next_up": None if not up else {"level": up[0], "price": r2(up[1]), "pct": r2((up[1] / px - 1) * 100),
                                                "atr": r2((up[1] - px) / ATR)},
                "next_dn": None if not dn else {"level": dn[0], "price": r2(dn[1]), "pct": r2((dn[1] / px - 1) * 100),
                                                "atr": r2((dn[1] - px) / ATR)},
                "label": lab}

    # ---- M4 RSI regime
    rv = ind["rsi"].iloc[-40:]
    if rv.min() >= 40:
        regime = "BULL (40-80 held)"
    elif rv.max() <= 60:
        regime = "BEAR (20-60 held)"
    else:
        regime = f"MIXED: 40-bar range {rv.min():.1f}-{rv.max():.1f}"
        if ind["rsi"].iloc[-10:].max() > 60 and rv.min() < 40:
            regime += " (bear ceiling 60 broken - regime-shift attempt)"
    rsi_cross = None
    s_ = np.sign(ind["rsi"] - ind["rsi_sig"]).to_numpy()
    for k in range(i, 0, -1):
        if s_[k] != s_[k - 1] and not np.isnan(s_[k - 1]):
            rsi_cross = str(D[k].date())
            break

    # ---- M5 OBV near-term
    ob, obs = ind["obv"].to_numpy(), ind["obv_sig"].to_numpy()
    sd = np.sign(ob - obs)
    obv_cross = None
    for k in range(i, 13, -1):
        if sd[k] != sd[k - 1]:
            obv_cross = {"date": str(D[k].date()), "dir": "up" if sd[k] > 0 else "down"}
            break
    last20 = df.iloc[-20:]
    chg = df["c"].diff().iloc[-20:]
    upv = float(last20["v"][chg > 0].sum())
    dnv = float(last20["v"][chg < 0].sum())
    vol_ratio = float(v.iloc[-1] / ind["vma20"].iloc[-1])
    obv_20d_high = bool(ob[i] >= ob[i - 19:i + 1].max() - 1e-6)

    # ---- M6 ATR
    atrp = ind["atr"] / c * 100
    yr_mask = D > asof - pd.Timedelta(days=365)
    atr_pct_pctile = float((atrp[yr_mask] <= atrp.iloc[-1]).mean() * 100)
    atr_usd_pctile = float((ind["atr"][yr_mask] <= ATR).mean() * 100)

    # ---- sizing
    nlv = a.nlv
    usd_local = a.usd_local or 1.0

    def size(entry, stop, half=False):
        if not nlv or entry is None or stop is None:
            return None
        full_r_usd = nlv * a.risk / 100
        risk_usd = full_r_usd * (0.5 if half else 1.0)
        rps = abs(entry - stop)
        sh_risk = math.floor(risk_usd * usd_local / rps / a.lot) * a.lot
        sh_cap = math.floor(nlv * a.max_name / 100 * usd_local / entry / a.lot) * a.lot
        sh = max(0, min(sh_risk, sh_cap))
        notional = sh * entry
        usd = notional / usd_local
        return {"shares": sh, "lots": sh // a.lot, "binding": "risk budget" if sh_risk <= sh_cap else f"{a.max_name:g}% name cap",
                "notional_local": r2(notional, 0), "usd": r2(usd, 0), "myr": r2(usd * a.fx, 0) if a.fx else None,
                "pct_nlv": r2(usd / nlv * 100, 1), "risk_usd": r2(sh * rps / usd_local, 0),
                "risk_R": r2(sh * rps / usd_local / full_r_usd, 2), "half_risk": half}

    def rr15_price_long(t1, stop):
        return (t1 + 1.5 * stop) / 2.5

    def rr15_price_short(t1, stop):
        return (t1 + 1.5 * stop) / 2.5

    def clamp_long_stop(entry, raw):
        note = None
        risk = entry - raw
        stop = raw
        if risk < 1.0 * ATR:
            stop, note = entry - 1.0 * ATR, "widened to 1.0x ATR floor"
        elif risk > 2.5 * ATR:
            stop, note = entry - 2.5 * ATR, "structure stop beyond 2.5x ATR - capped (structure not fully respected)"
        return stop, note

    def clamp_short_stop(entry, raw):
        note = None
        risk = raw - entry
        stop = raw
        if risk < 1.0 * ATR:
            stop, note = entry + 1.0 * ATR, "widened to 1.0x ATR floor"
        elif risk > 2.5 * ATR:
            stop, note = entry + 2.5 * ATR, "structure stop beyond 2.5x ATR - capped"
        return stop, note

    plans = {}
    minn = a.target_n

    # A. LONG ON SUPPORT
    cand = [z for z in zones if z["hi"] < px and z["lo"] >= px - 4 * ATR and z["n"] >= 2]
    if cand:
        z = max(cand, key=lambda z: (z["n"], z["hi"]))
        entry = z["hi"]
        stop, note = clamp_long_stop(entry, z["lo"] - 0.5 * ATR)
        tz = targets_up_beyond(entry, minn)
        t1 = tz[0]["lo"] if tz else None
        t2 = next_zone_up(tz[0]) if tz else None
        mode ="pullback (MARKUP)" if phase_d == "MARKUP" else "reversal only: tag, close back above zone top + RSI higher low; no resting bids"
        plans["A"] = {"name": "LONG ON SUPPORT", "mode": mode, "zone": ztxt(z), "zone_n": z["n"], "zone_components": z["components"],
                      "trigger": f"tag {z['hi']:.2f} then close > {z['hi']:.2f}" + ("" if phase_d == "MARKUP" else " with RSI higher low"),
                      "entry": r2(entry), "stop": r2(stop), "stop_note": note, "hard_stop": r2(entry - 1.5 * (entry - stop)),
                      "t1": r2(t1), "t2": r2(t2), "rr1": r2((t1 - entry) / (entry - stop)) if t1 else None,
                      "rr2": r2((t2 - entry) / (entry - stop)) if t2 else None,
                      "price_rr15": r2(rr15_price_long(t1, stop)) if t1 else None,
                      "risk_atr": r2((entry - stop) / ATR), "risk_ps": r2(entry - stop),
                      "risk_pct": r2((entry - stop) / entry * 100), "hard_risk_ps": r2(1.5 * (entry - stop)),
                      "size": size(entry, stop, half=True)}

    # B. BREAKOUT LADDER
    base_low = float(L[i - 19:i + 1].min())
    ladder = []
    over = sorted([z for z in zones if z["hi"] > px], key=lambda z: z["lo"])
    for z in over:
        if z["lo"] > px * (1 + a.ladder_pct / 100):
            break
        lvl = z["hi"]
        trig = lvl + 0.25 * ATR
        stop = lvl - 0.75 * ATR
        mm = trig + (lvl - base_low)
        tz = sorted([x for x in zones if x["hi"] > trig + 1e-9 and x["lo"] > lvl + 1e-9 and is_target(x, minn)],
                    key=lambda x: x["lo"])  # next UNCLEARED zone (may straddle the trigger)
        t1z = tz[0] if tz else None
        t1, t1_src = (mm, "measured move") if (t1z is None or mm < t1z["lo"]) else (t1z["lo"], f"zone {ztxt(t1z)}")
        if t1z is not None and t1z["lo"] <= trig:
            t1, t1_src = trig, f"trigger inside next zone {ztxt(t1z)}"
        if t1_src != "measured move":
            t2 = next_zone_up(t1z) or (mm if mm > t1 else None)
        else:
            nxt = sorted([x for x in zones if x["lo"] > mm], key=lambda x: x["lo"])
            t2 = nxt[0]["lo"] if nxt else None
        rr1 = (t1 - trig) / (trig - stop)
        rr2 = (t2 - trig) / (trig - stop) if t2 else None
        chase = lvl + 1.0 * ATR
        if px >= trig:
            if px > chase:
                status = "CLEARED - above chase limit, wait for retest"
            elif vol_ratio >= 1.5 and obv_20d_high:
                status = "TRIGGERED on close"
            else:
                status = f"close >= trigger but vol {vol_ratio:.2f}x / OBV 20D high {obv_20d_high}"
        else:
            status = "pending"
        ladder.append({"zone": ztxt(z), "n": z["n"], "components": z["components"], "level": r2(lvl), "trigger": r2(trig),
                       "stop": r2(stop), "hard_stop": r2(trig - 1.5 * (trig - stop)), "t1": r2(t1), "t1_src": t1_src,
                       "t2": r2(t2), "rr1": r2(rr1), "rr2": r2(rr2), "chase_limit": r2(chase),
                       "price_rr15": r2(rr15_price_long(t1, stop)), "status": status,
                       "risk_ps": r2(trig - stop), "risk_pct": r2((trig - stop) / trig * 100),
                       "dist_pct": r2((trig / px - 1) * 100), "dist_atr": r2((trig - px) / ATR)})
    first_ok = next((r for r in ladder if r["rr1"] is not None and r["rr1"] >= a.rr_min), None)
    if first_ok:
        plans["B"] = dict(first_ok, name="BREAKOUT (first rung R/R >= %.1f)" % a.rr_min,
                          size=size(first_ok["trigger"], first_ok["stop"], half=False))

    # S. FADE SHORT
    cand = [z for z in zones if z["lo"] > px and z["hi"] <= px + 4 * ATR and z["n"] >= 2]
    if cand:
        z = max(cand, key=lambda z: (z["n"], -z["lo"]))
        entry = z["lo"]
        stop, note = clamp_short_stop(entry, z["hi"] + 0.5 * ATR)
        tz = targets_down_beyond(entry, minn)
        t1 = tz[0]["hi"] if tz else None
        t2 = next_zone_down(tz[0]) if tz else None
        plans["S"] = {"name": "FADE SHORT", "phase_qualified": phase_d in ("MARKDOWN", "DISTRIBUTION", "EARLY MARKDOWN"),
                      "zone": ztxt(z), "zone_n": z["n"], "zone_components": z["components"],
                      "trigger": f"rally into {ztxt(z)} then close < {z['lo']:.2f}", "entry": r2(entry), "stop": r2(stop),
                      "stop_note": note, "hard_stop": r2(entry + 1.5 * (stop - entry)), "t1": r2(t1), "t2": r2(t2),
                      "rr1": r2((entry - t1) / (stop - entry)) if t1 else None,
                      "rr2": r2((entry - t2) / (stop - entry)) if t2 else None,
                      "price_rr15": r2(rr15_price_short(t1, stop)) if t1 else None,
                      "risk_atr": r2((stop - entry) / ATR), "risk_ps": r2(stop - entry),
                      "risk_pct": r2((stop - entry) / entry * 100), "hard_risk_ps": r2(1.5 * (stop - entry)),
                      "size": size(entry, stop)}

    # C. EXIT (if held)
    if len(sup_zones) >= 2:
        plans["C"] = {"name": "EXIT (if held)", "trim_below": r2(sup_zones[0]["lo"]), "trim_zone": ztxt(sup_zones[0]),
                      "exit_below": r2(sup_zones[1]["lo"]), "exit_zone": ztxt(sup_zones[1]), "basis": "daily close"}

    repair = max(float(last["ema50"]), av_cyc or -1e9)
    live = []
    for z in zones:
        if z["n"] >= 3 and z["touched_today"] and z["at_price"]:
            if L[i] <= z["hi"] and px > z["hi"]:
                stop, note = clamp_long_stop(px, z["lo"] - 0.5 * ATR)
                tz = targets_up_beyond(px, minn)
                t1 = tz[0]["lo"] if tz else None
                live.append({"type": "support bounce", "zone": ztxt(z), "n": z["n"], "entry": r2(px), "stop": r2(stop),
                             "stop_note": note, "t1": r2(t1), "rr1": r2((t1 - px) / (px - stop)) if t1 else None,
                             "risk_ps": r2(px - stop), "risk_pct": r2((px - stop) / px * 100)})
            if H[i] >= z["lo"] and px < z["lo"]:
                stop, note = clamp_short_stop(px, z["hi"] + 0.5 * ATR)
                tz = targets_down_beyond(px, minn)
                t1 = tz[0]["hi"] if tz else None
                live.append({"type": "resistance failure", "zone": ztxt(z), "n": z["n"], "entry": r2(px), "stop": r2(stop),
                             "stop_note": note, "t1": r2(t1), "rr1": r2((px - t1) / (stop - px)) if t1 else None,
                             "risk_ps": r2(stop - px), "risk_pct": r2((stop - px) / px * 100)})

    # ---- M8 PM overlay
    rs = {}
    for bpath in (a.bench or []):
        b, bsym = load_bars(bpath)
        checks.append("summary checksum OK: " + bpath)
        b = b.loc[b.index <= asof]
        rs[bsym] = {"asof": str(b.index[-1].date())}
        for N in (20, 60):
            if len(b) > N and n > N:
                rs_stock = C[i] / C[i - N] - 1
                rs_b = b["c"].iloc[-1] / b["c"].iloc[-1 - N] - 1
                rs[bsym][f"{N}D"] = {"stock_pct": r2(rs_stock * 100), "bench_pct": r2(rs_b * 100),
                                     "spread_pp": r2((rs_stock - rs_b) * 100)}

    event = None
    if a.earnings:
        ses = busdays_between(asof, a.earnings, a.holidays or [])
        event = {"date": a.earnings, "status": a.earnings_status, "sessions": ses, "EVENT_flag": ses <= a.event_sessions}
    implied = None
    if a.implied_move:
        implied = {"pct": a.implied_move, "expiry": a.implied_exp, "hkd": r2(px * a.implied_move / 100)}

    book = None
    if a.book:
        bk = json.load(open(a.book))
        cash_pct = bk["cash_usd"] / bk["nlv_usd"] * 100
        fac = {}
        for p in bk["positions"]:
            fac.setdefault(p["factor"], 0.0)
            fac[p["factor"]] += p["mv_usd"] * p.get("lev", 1)
        dom = max(fac.items(), key=lambda kv: kv[1]) if fac else None
        book = {"nlv_usd": bk["nlv_usd"], "cash_usd": bk["cash_usd"], "cash_pct": r2(cash_pct, 1),
                "cash_buffer_target_pct": a.cash_buffer, "cash_ok": cash_pct >= a.cash_buffer,
                "factor_notional_usd": {k: r2(x, 0) for k, x in fac.items()},
                "factor_pct_nlv": {k: r2(x / bk["nlv_usd"] * 100, 0) for k, x in fac.items()},
                "dominant": dom[0] if dom else None, "new_name_factor": a.factor,
                "adds_to_dominant": bool(dom and a.factor == dom[0]), "existing_name_pct": 0.0 if not a.held else None}

    acel = None
    if a.acel_ki:
        ses = busdays_between(asof, a.acel_fv, a.holidays or [])
        T = ses / 252
        acel = {"KI": a.acel_ki, "KO": a.acel_ko, "strike": a.acel_strike or a.acel_ki, "FV": a.acel_fv,
                "sessions_to_FV": ses, "basis": "European KI: FV close only"}
        for lab, spot in (("asof_close", px), ("live", a.live)):
            if not spot:
                continue
            row = {"spot": spot, "to_KI_pct": r2((a.acel_ki / spot - 1) * 100), "to_KI_atr": r2((a.acel_ki - spot) / ATR),
                   "to_KO_pct": r2((a.acel_ko / spot - 1) * 100) if a.acel_ko else None,
                   "delivery_loss_pct_if_KI": r2((spot / (a.acel_strike or a.acel_ki) - 1) * 100)}
            for sig in (a.acel_vol or []):
                sv = sig / 100 * math.sqrt(T)
                d2 = (math.log(spot / a.acel_ki) - 0.5 * sv * sv) / sv
                row[f"P(FV>=KI) sigma {sig:g}%"] = r2(norm_cdf(d2) * 100, 1)
            acel[lab] = row
        if implied:
            acel["KI_vs_implied_move"] = r2(((a.acel_ki / (a.live or px)) - 1) * 100 / a.implied_move, 2)

    # ---- M9 verdict (mechanical; the PM writes the final call)
    blocks = []
    if event and event["EVENT_flag"]:
        blocks.append("EVENT <= %d sessions: no new BUY on TA alone" % a.event_sessions)
    if book and not book["cash_ok"]:
        blocks.append(f"cash {book['cash_pct']}% < {a.cash_buffer}% buffer: BUY blocked until funded")
    big_down = px < float(last["ema50"]) and av_cyc is not None and px < av_cyc and vol_ratio >= 1.5 and C[i] < C[i - 1]
    if big_down:
        blocks.append("close below EMA50 and AVWAP on >= 1.5x volume: no BUY")
    trig_long = next((r for r in ladder if r["status"] == "TRIGGERED on close" and r["rr1"] >= a.rr_min), None)
    live_long = any(x["type"] == "support bounce" and (x["rr1"] or 0) >= a.rr_min for x in live)
    live_short = any(x["type"] == "resistance failure" and (x["rr1"] or 0) >= a.rr_min for x in live) \
        and phase_d in ("MARKDOWN", "DISTRIBUTION", "EARLY MARKDOWN")
    if a.held:
        mech = "TRIM" if bear_rsi_obv else "HOLD"
    elif trig_long:
        mech = "BUY (breakout)"
    elif live_long:
        mech = "BUY (support, half risk)"
    elif live_short:
        mech = "SELL (fade)"
    else:
        mech = "WAIT"
    if mech.startswith("BUY") and blocks:
        mech = "WAIT (BUY blocked: " + "; ".join(blocks) + ")"
    bd, bw = bias[phase_d], bias[phase_w]
    conf = "H" if (bd != 0 and bd * bw > 0) else ("L" if bd * bw < 0 else "M")
    if mech.startswith("BUY (support") and conf == "H":
        conf = "M"  # v2.1: pullback / bounce longs capped at M (MU walk-forward)

    # v2.1 holder note (chart-only)
    if bear_rsi_obv:
        holder = "TRIM: confirmed bearish RSI + OBV divergence"
    elif big_down:
        holder = "TRIM: close below EMA50 and AVWAP(cycle high) on >= 1.5x volume"
    elif sup_zones:
        holder = f"HOLD while daily closes stay above {sup_zones[0]['lo']:.2f} (first support zone {ztxt(sup_zones[0])})"
    else:
        holder = "HOLD: no support zone with n >= 2 below price"
    for p_ in plans.values():
        if p_.get("size") is None:
            p_.pop("size", None)

    out = {
        "engine": VERSION, "symbol": sym, "asof": str(asof.date()), "bars": n, "close": px,
        "dropped_bars_after_asof": [str(x.date()) for x in dropped], "checks": checks,
        "live": {"price": a.live, "time": a.live_time, "vol": a.live_vol} if a.live else None,
        "indicators": {k: r2(last[k], 4 if k in ("obv", "obv_sig") else 3) for k in
                       ["ema9", "ema21", "ema20", "ema50", "ema200", "sma200", "bb_lo", "bb_mid", "bb_up", "rsi", "rsi_sig",
                        "atr", "vma20"]},
        "obv": {"obv": r2(ob[i], 0), "sig": r2(obs[i], 0), "side": "above" if ob[i] > obs[i] else "below",
                "sig_slope_5": "rising" if obs[i] > obs[i - 5] else "falling", "last_cross": obv_cross,
                "updown_vol_20d": r2(upv / dnv if dnv else float("inf")), "vol_vs_20d": r2(vol_ratio),
                "obv_20d_high": obv_20d_high, "div": obv_div},
        "phase": {"daily": phase_d, "weekly": phase_w, "rules_daily": rules, "rules_weekly": w_rules,
                  "detail": {"ema20_rising": rising(e20), "ema50_rising": rising(e50), "lower_low": bool(lower_low),
                             "uptrend_ctx": uptrend_ctx, "rng20_atr": r2(rng20 / ATR), "ema20_flat": bool(flat20),
                             "obv_rising": obv_rising,
                             "weekly": {"close": r2(wpx), "ema10": r2(we10.iloc[-1]), "ema20": r2(we20.iloc[-1]),
                                        "ema40": r2(we40.iloc[-1]), "lower_low": bool(w_ll), "week_ending": str(wk.index[-1].date()),
                                        "partial_week": bool(D[-1] < wk.index[-1])}}},
        "structure": {"cycle_high": {"price": float(H[cyc_hi_pos]), "date": str(D[cyc_hi_pos].date())},
                      "cycle_low": {"price": float(L[cyc_lo_pos]), "date": str(D[cyc_lo_pos].date())},
                      "hi52": hi52, "lo52": lo52,
                      "zigzag_last6": [{"date": str(D[p].date()), "type": t, "price": r2(x)} for p, t, x in zz[-6:]],
                      "base_low_20d": base_low},
        "avwap": {k: {"anchor": x["anchor"], "value": r2(x["value"], 3)} for k, x in av.items()},
        "fib": {"macro": dict(macro, levels={k: r2(p, 3) for k, p in macro["levels"].items()}, position=fib_pos(macro)),
                "tactical": None if not tactical else dict(tactical, levels={k: r2(p, 3) for k, p in tactical["levels"].items()},
                                                           position=fib_pos(tactical))},
        "zones": [{"zone": ztxt(z), "lo": r2(z["lo"], 3), "hi": r2(z["hi"], 3), "n": z["n"], "side": z["side"],
                   "dist_pct": r2(z["dist_pct"]), "dist_atr": r2(z["dist_atr"]), "components": z["components"]}
                  for z in zones if abs(z["dist_pct"]) <= a.map_pct],
        "at_price": [ztxt(z) + f" (n={z['n']:g})" for z in at_zones],
        "top_resistance": [{"zone": ztxt(z), "n": z["n"], "dist_pct": r2(z["dist_pct"]), "dist_atr": r2(z["dist_atr"]),
                            "components": z["components"]} for z in res_zones[:3]],
        "top_support": [{"zone": ztxt(z), "n": z["n"], "dist_pct": r2(z["dist_pct"]), "dist_atr": r2(z["dist_atr"]),
                         "components": z["components"]} for z in sup_zones[:3]],
        "line_in_sand_candidate": None if not lis else {"zone": ztxt(lis), "n": lis["n"], "components": lis["components"]},
        "rsi": {"value": r2(last["rsi"]), "sig": r2(last["rsi_sig"]), "side": "above" if last["rsi"] > last["rsi_sig"] else "below",
                "last_signal_cross": rsi_cross, "regime": regime, "div": rsi_div},
        "atr": {"atr": r2(ATR, 3), "pct": r2(ATR / px * 100), "pctile_1y_atr_pct": r2(atr_pct_pctile, 0),
                "pctile_1y_atr_abs": r2(atr_usd_pctile, 0)},
        "plans": plans, "ladder": ladder, "trend_repair": r2(repair), "live_setups": live,
        "pm": {"rs": rs, "event": event, "implied": implied, "book": book, "acel": acel},
        "verdict": {"mechanical": mech, "confidence": conf, "blocks": blocks, "bias_daily": bd, "bias_weekly": bw,
                    "holder_note": holder, "big_down_bar": bool(big_down)},
        "params": {"risk_pct": a.risk, "max_name_pct": a.max_name, "cash_buffer_pct": a.cash_buffer, "rr_min": a.rr_min,
                   "zone_atr": a.zone_atr, "target_min_n": minn, "lot": a.lot, "ccy": a.ccy, "usd_local": a.usd_local,
                   "usdmyr": a.fx, "round_step": step},
    }
    return out


# ------------------------------------------------------------------------- scoring
def score_call(df, direction, trigger, entry_rule, stop, hard_stop, t1, t2=None, start=None, max_bars=60):
    """M10: score one logged call on daily bars after `start`.
    entry_rule: 'close_above' | 'close_below' (fill at that close) | 'limit' (fill when touched).
    Exit: closing stop (close through stop), intraday hard stop, or T1 touch (half) / T2 touch (rest)."""
    d = df.loc[df.index > pd.Timestamp(start)] if start else df
    fill = None
    for k, (ix, r) in enumerate(d.iterrows()):
        if fill is None:
            if (entry_rule == "close_above" and r.c >= trigger) or (entry_rule == "close_below" and r.c <= trigger):
                fill, fdate, fk = r.c, ix, k
            elif entry_rule == "limit" and r.l <= trigger <= r.h:
                fill, fdate, fk = trigger, ix, k
            continue
        risk = abs(fill - stop)
        sgn = 1 if direction == "long" else -1
        mfe = max(0.0, sgn * ((r.h if sgn > 0 else r.l) - fill)) / risk
        mae = max(0.0, -sgn * ((r.l if sgn > 0 else r.h) - fill)) / risk
        if (sgn > 0 and r.l <= hard_stop) or (sgn < 0 and r.h >= hard_stop):
            return {"fill": fill, "fill_date": str(fdate.date()), "exit": "hard stop", "date": str(ix.date()),
                    "R": -abs(fill - hard_stop) / risk, "mfe": mfe, "mae": mae}
        if (sgn > 0 and r.h >= t1) or (sgn < 0 and r.l <= t1):
            return {"fill": fill, "fill_date": str(fdate.date()), "exit": "T1", "date": str(ix.date()),
                    "R": abs(t1 - fill) / risk, "mfe": mfe, "mae": mae}
        if (sgn > 0 and r.c <= stop) or (sgn < 0 and r.c >= stop):
            return {"fill": fill, "fill_date": str(fdate.date()), "exit": "closing stop", "date": str(ix.date()),
                    "R": sgn * (r.c - fill) / risk, "mfe": mfe, "mae": mae}
        if k - fk >= max_bars:
            return {"fill": fill, "fill_date": str(fdate.date()), "exit": "time", "date": str(ix.date()),
                    "R": sgn * (r.c - fill) / risk, "mfe": mfe, "mae": mae}
    return {"fill": fill, "exit": "open" if fill else "not filled"}


# ---------------------------------------------------------------------------- CLI
def main():
    p = argparse.ArgumentParser(description="TA v2 PM engine (Claude Code rebuild)")
    p.add_argument("data")
    p.add_argument("--warmup", help="closes-only JSON before the main window (EMA200 warm-up)")
    p.add_argument("--asof", help="last COMPLETED session YYYY-MM-DD (drops a forming bar)")
    p.add_argument("--nlv", type=float)
    p.add_argument("--risk", type=float, default=0.5, help="% NLV per planned R")
    p.add_argument("--max-name", type=float, default=10.0)
    p.add_argument("--cash-buffer", type=float, default=5.0)
    p.add_argument("--fx", type=float, help="USD/MYR")
    p.add_argument("--ccy", default="USD")
    p.add_argument("--usd-local", type=float, help="local units per USD (e.g. USDHKD)")
    p.add_argument("--lot", type=int, default=1, help="board lot")
    p.add_argument("--bench", nargs="*")
    p.add_argument("--earnings")
    p.add_argument("--earnings-status", default="ESTIMATED")
    p.add_argument("--event-sessions", type=int, default=10)
    p.add_argument("--holidays", nargs="*")
    p.add_argument("--avwap", nargs="*")
    p.add_argument("--fib", nargs=2, metavar=("LOW_DATE", "HIGH_DATE"))
    p.add_argument("--held", action="store_true")
    p.add_argument("--book")
    p.add_argument("--factor", default=None, help="risk-factor tag of this name for the book overlay")
    p.add_argument("--implied-move", type=float, help="front-expiry ATM straddle, % of spot")
    p.add_argument("--implied-exp")
    p.add_argument("--live", type=float)
    p.add_argument("--live-time")
    p.add_argument("--live-vol", type=float)
    p.add_argument("--acel-ki", type=float)
    p.add_argument("--acel-ko", type=float)
    p.add_argument("--acel-strike", type=float)
    p.add_argument("--acel-fv")
    p.add_argument("--acel-vol", type=float, nargs="*", help="vols (%) for P(FV close >= KI)")
    p.add_argument("--rr-min", type=float, default=1.5)
    p.add_argument("--div-pts", type=float, default=2.0)
    p.add_argument("--zone-atr", type=float, default=0.5)
    p.add_argument("--target-n", type=float, default=2.0, help="min zone strength used as a target")
    p.add_argument("--ladder-pct", type=float, default=30.0)
    p.add_argument("--map-pct", type=float, default=20.0)
    p.add_argument("--round-step", type=float)
    p.add_argument("--json")
    a = p.parse_args()
    try:
        out = run(a)
    except ChecksumError as e:
        print("CHECKSUM FAILURE - stop and re-pull:", e, file=sys.stderr)
        sys.exit(2)
    js = json.dumps(out, indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
    if a.json:
        open(a.json, "w").write(js)
    print(js)


if __name__ == "__main__":
    main()
