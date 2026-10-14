"""Module 5: weekly trend + daily entry technicals, structure levels, R:R and technical score (core six)."""
import numpy as np, pandas as pd
from common import CORE, ASOF, OUT, px, cons

C = cons()


def wilder(s, n):
    return s.ewm(alpha=1 / n, adjust=False).mean()


def rsi(c, n=14):
    d = c.diff()
    return 100 - 100 / (1 + wilder(d.clip(lower=0), n) / wilder(-d.clip(upper=0), n))


def macd(c):
    m = c.ewm(span=12, adjust=False).mean() - c.ewm(span=26, adjust=False).mean()
    s = m.ewm(span=9, adjust=False).mean()
    return m, s, m - s


def atr_adx(h, l, c, n=14):
    tr = pd.concat([h - l, (h - c.shift()).abs(), (l - c.shift()).abs()], axis=1).max(axis=1)
    up, dn = h.diff(), -l.diff()
    pdm = up.where((up > dn) & (up > 0), 0.0)
    ndm = dn.where((dn > up) & (dn > 0), 0.0)
    atr = wilder(tr, n)
    pdi, ndi = 100 * wilder(pdm, n) / atr, 100 * wilder(ndm, n) / atr
    adx = wilder(100 * (pdi - ndi).abs() / (pdi + ndi), n)
    return atr, adx, pdi, ndi


def pivots(h, l, k):
    """Fractal swing highs/lows: bar is the extreme of a +/-k window (confirmed only, so the last k bars are excluded)."""
    hi = h[(h == h.rolling(2 * k + 1, center=True).max())].dropna()
    lo = l[(l == l.rolling(2 * k + 1, center=True).min())].dropna()
    return hi, lo


def volume_nodes(c, v, bins=40, top=0.75):
    """High-volume price nodes over the window (volume-at-close histogram; local maxima above the `top` quantile)."""
    hist, edges = np.histogram(c, bins=bins, weights=v)
    mids = (edges[:-1] + edges[1:]) / 2
    thr = np.quantile(hist, top)
    peaks = [mids[i] for i in range(len(hist)) if hist[i] >= thr and hist[i] == hist[max(0, i - 1):i + 2].max()]
    return np.array(peaks)


def weekly(d):
    return d.resample("W-FRI").agg({"Open": "first", "High": "max", "Low": "min", "Close": "last", "Volume": "sum"}).dropna()


klci = px("KLCI").Close
caps = pd.Series({b: C[b]["mcap"] for b in CORE})
rets = pd.DataFrame({b: px(b)["Adj Close"].pct_change() for b in CORE}).dropna(how="all")
wts = caps / caps.sum()
sector = (1 + (rets.fillna(0) * wts).sum(axis=1)).cumprod()  # cap-weighted core-six dividend-adjusted composite (sector proxy)

rows, levels = [], []
for b in CORE:
    d = px(b)
    d = d[d.Volume > 0].copy()
    f = d["Adj Close"] / d["Close"]  # dividend adjustment: ex-div gaps are payouts, not supply; ~1.0 for post-ex-date bars
    for col in ("Open", "High", "Low", "Close"):
        d[col] = d[col] * f
    c, h, l, v = d.Close, d.High, d.Low, d.Volume
    P = c.iloc[-1]
    sma = {n: c.rolling(n).mean() for n in (20, 50, 200)}
    atr, adx, pdi, ndi = atr_adx(h, l, c)
    A = atr.iloc[-1]
    m, s, hst = macd(c)
    wk = weekly(d)
    wk = wk[wk.index <= pd.Timestamp("2026-10-09")]  # completed weeks only
    wc = wk.Close
    w40 = wc.rolling(40).mean()
    wm, ws, wh = macd(wc)
    obv = (np.sign(c.diff()).fillna(0) * v).cumsum()
    mfm = ((c - l) - (h - c)) / (h - l).replace(0, np.nan)
    cmf20 = (mfm.fillna(0) * v).rolling(20).sum() / v.rolling(20).sum()
    # golden/death cross state and date of last cross
    diff = (sma[50] - sma[200]).dropna()
    cross_idx = diff.index[np.sign(diff).diff().fillna(0) != 0]
    last_cross = cross_idx[-1] if len(cross_idx) else None
    # relative strength (price basis)
    def ret(series, n):
        return series.iloc[-1] / series.iloc[-1 - n] - 1
    k = klci.reindex(c.index).ffill()
    sec = sector.reindex(c.index).ffill()
    rs_line = c / k
    rs = dict(rs3m_klci=ret(c, 63) - ret(k, 63), rs6m_klci=ret(c, 126) - ret(k, 126),
              rs3m_sector=ret(c, 63) - ret(sec, 63), rs6m_sector=ret(c, 126) - ret(sec, 126),
              rs_line_52w_pos=(rs_line.iloc[-1] - rs_line.iloc[-252:].min()) / (rs_line.iloc[-252:].max() - rs_line.iloc[-252:].min()),
              rs_line_new_high=bool(rs_line.iloc[-5:].max() >= rs_line.iloc[-252:].max()),
              rs_line_new_low=bool(rs_line.iloc[-5:].min() <= rs_line.iloc[-252:].min()))
    hi52, lo52 = h.iloc[-252:].max(), l.iloc[-252:].min()
    # structure (3-6m horizon): weekly pivots (k=3, 3y), daily pivots (k=15, 1y), 52w extremes, major volume nodes (top 15%),
    # and the 50/200-DMA + 40W lines as dynamic levels; levels within 0.6 ATR are clustered into one zone.
    dh, dl = pivots(h.iloc[-260:], l.iloc[-260:], 15)
    whp, wlp = pivots(wk.High.iloc[-156:], wk.Low.iloc[-156:], 3)
    nodes = volume_nodes(c.iloc[-252:].values, v.iloc[-252:].values, top=0.85)
    dyn = np.array([sma[50].iloc[-1], sma[200].iloc[-1], w40.iloc[-1]])
    lv = np.sort(np.r_[dh.values, dl.values, whp.values, wlp.values, [hi52, lo52], nodes, dyn])
    clusters, cur = [], [lv[0]]
    for x in lv[1:]:
        if x - cur[-1] <= 0.6 * A:
            cur.append(x)
        else:
            clusters.append(cur); cur = [x]
    clusters.append(cur)
    zones = [(float(np.mean(z)), len(z)) for z in clusters]
    res_above = [z for z, n in zones if z >= P + 1.5 * A]
    sup_below = [z for z, n in zones if z <= P - 1.0 * A]
    near_sup = [z for z, n in zones if P - 1.0 * A < z < P]
    heavy_near = [z for z, n in zones if P < z < P + 1.5 * A and n >= 3]
    trigger_near = heavy_near[0] if heavy_near else np.nan  # immediate heavy resistance that must be reclaimed before T1
    rng = hi52 - lo52
    t1 = res_above[0] if res_above else lo52 + 1.272 * rng
    fib1618 = lo52 + 1.618 * rng
    nxt = [z for z in res_above if z >= t1 * 1.03]
    t2 = nxt[0] if nxt else fib1618  # next significant zone >=3% beyond T1; 52w-range 1.618 extension only when clear of all resistance
    s1 = sup_below[-1] if sup_below else P - 2 * A
    stop_struct = s1 - 0.25 * A
    stop_atr = P - 2 * A
    logical = [x for x in (stop_struct, stop_atr) if P - x >= 1.5 * A]  # inside 1.5 ATR is daily noise, not a stop
    stop = max(logical) if logical else stop_atr
    stop_basis = "structure" if stop == stop_struct else "2xATR"
    entry_lo = max(near_sup[-1] if near_sup else P - 0.75 * A, stop + 0.75 * A)
    entry_hi = P + 0.25 * A
    up, dn = t1 / P - 1, stop / P - 1
    rr = up / abs(dn)
    # regime: weekly primary trend (40W level and slope) confirmed by the daily 200-DMA
    sl50 = sma[50].iloc[-1] / sma[50].iloc[-11] - 1
    sl200 = sma[200].iloc[-1] / sma[200].iloc[-21] - 1
    sl40w = w40.iloc[-1] / w40.iloc[-5] - 1
    up_cond = (wc.iloc[-1] > w40.iloc[-1]) and (sl40w > 0) and (P > sma[200].iloc[-1]) and (sma[50].iloc[-1] > sma[200].iloc[-1])
    dn_cond = (wc.iloc[-1] < w40.iloc[-1]) and (sl40w < 0) and (P < sma[200].iloc[-1])
    regime = "Uptrend" if up_cond else ("Downtrend" if dn_cond else "Range")
    # scores
    trend_pts = (20 * (P > sma[200].iloc[-1]) + 15 * (P > sma[50].iloc[-1]) + 10 * (P > sma[20].iloc[-1]) +
                 15 * (sma[50].iloc[-1] > sma[200].iloc[-1]) + 15 * (sl200 > 0) + 10 * (sl50 > 0) + 15 * (wc.iloc[-1] > w40.iloc[-1]))
    rs_score = np.mean([np.clip(50 + x * 500, 0, 100) for x in (rs["rs3m_klci"], rs["rs6m_klci"], rs["rs3m_sector"], rs["rs6m_sector"])])

    def rsi_pts(x):
        return float(np.clip((x - 30) / 35 * 100, 0, 100)) if x <= 70 else max(0.0, 100 - (x - 70) * 10)

    def macd_pts(mm, ss, hh):
        return 50 * (mm.iloc[-1] > ss.iloc[-1]) + 25 * (hh.iloc[-1] > hh.iloc[-4]) + 25 * (mm.iloc[-1] > 0)
    adx_pts = 50.0 if adx.iloc[-1] < 20 else (100.0 if pdi.iloc[-1] > ndi.iloc[-1] else 0.0)
    r_d, r_w = rsi(c).iloc[-1], rsi(wc).iloc[-1]
    mom_d = 0.4 * rsi_pts(r_d) + 0.3 * macd_pts(m, s, hst) + 0.3 * adx_pts
    mom_w = 0.6 * rsi_pts(r_w) + 0.4 * macd_pts(wm, ws, wh)
    mom_score = 0.5 * mom_d + 0.5 * mom_w
    rr_score = float(np.clip(rr / 3 * 100, 0, 100))
    ext20 = (P - sma[20].iloc[-1]) / A
    penalty = 10 * (r_d > 75) + 10 * (ext20 > 2)
    tech = 0.35 * trend_pts + 0.25 * rs_score + 0.20 * mom_score + 0.20 * rr_score - penalty
    # post-trigger plan: buy a weekly close above the flip level; stop just under the reclaimed band; next two zones as targets
    flip = max(w40.iloc[-1], sma[200].iloc[-1])
    flip_targets = [z for z, n in zones if z >= flip + 1.5 * A]
    flip_t1 = flip_targets[0] if flip_targets else lo52 + 1.272 * rng
    flip_t2 = next((z for z in flip_targets if z >= flip_t1 * 1.03), max(fib1618, flip_t1 * 1.03))
    flip_stop = flip - 1.5 * A
    # conservative variant: the immediate heavy resistance (if any) is T1
    t1_cons = trigger_near if not np.isnan(trigger_near) else t1
    rr_cons = (t1_cons / P - 1) / abs(dn)
    tech_cons = tech - 0.20 * (rr_score - float(np.clip(rr_cons / 3 * 100, 0, 100)))
    rows.append(dict(bank=b, price=P, sma20=sma[20].iloc[-1], sma50=sma[50].iloc[-1], sma200=sma[200].iloc[-1], w40=w40.iloc[-1],
                     wclose=wc.iloc[-1], slope50_10d=sl50, slope200_20d=sl200, slope40w_4w=sl40w, cross="golden" if diff.iloc[-1] > 0 else "death",
                     last_cross=last_cross.date() if last_cross is not None else None, regime=regime, bias=('above' if P > w40.iloc[-1] else 'below') + ' 40W', trigger_near=trigger_near, flip_trigger=max(w40.iloc[-1], sma[200].iloc[-1]),
                     rsi_d=r_d, rsi_w=r_w, macd_d_above_sig=bool(m.iloc[-1] > s.iloc[-1]), macd_d_hist_rising=bool(hst.iloc[-1] > hst.iloc[-4]),
                     macd_w_above_sig=bool(wm.iloc[-1] > ws.iloc[-1]), macd_w_hist_rising=bool(wh.iloc[-1] > wh.iloc[-4]),
                     adx=adx.iloc[-1], pdi=pdi.iloc[-1], ndi=ndi.iloc[-1], atr=A, atr_pct=A / P, ext20_atr=ext20,
                     obv_20d_up=bool(obv.iloc[-1] > obv.iloc[-21]), obv_above_50dma=bool(obv.iloc[-1] > obv.rolling(50).mean().iloc[-1]),
                     cmf20=cmf20.iloc[-1], hi52=hi52, lo52=lo52, pct_from_52wh=P / hi52 - 1, **rs,
                     entry_lo=entry_lo, entry_hi=entry_hi, stop=stop, stop_basis=stop_basis, support=s1, t1=t1, t2=t2,
                     upside_t1=up, downside=dn, rr=rr, trend_pts=trend_pts, rs_score=rs_score, mom_score=mom_score,
                     rr_score=rr_score, penalty=penalty, tech_score=tech, t1_cons=t1_cons, rr_cons=rr_cons, tech_score_cons=tech_cons, flip_entry=flip, flip_stop=flip_stop, flip_t1=flip_t1, flip_t2=flip_t2))
    levels.append(dict(bank=b, zones_above=[(round(z, 2), n) for z, n in zones if z > P][:5],
                       zones_below=[(round(z, 2), n) for z, n in zones if z < P][-5:], volume_nodes=[round(x, 2) for x in nodes]))

T = pd.DataFrame(rows).set_index("bank")
T.to_csv(f"{OUT}/m5_technicals.csv")
pd.DataFrame(levels).set_index("bank").to_csv(f"{OUT}/m5_structure.csv")
pd.set_option("display.width", 250, "display.max_columns", 60)
print(T[["price", "atr", "slope200_20d", "slope40w_4w", "sma20", "sma50", "sma200", "w40", "regime", "cross", "last_cross", "rsi_d", "rsi_w", "adx", "pdi", "ndi", "macd_d_above_sig", "macd_w_above_sig"]].round(3).to_string())
print(T[["rs3m_klci", "rs6m_klci", "rs3m_sector", "rs6m_sector", "rs_line_52w_pos", "rs_line_new_high", "rs_line_new_low", "obv_20d_up", "cmf20", "pct_from_52wh", "ext20_atr"]].round(3).to_string())
print(T[["trigger_near", "flip_trigger", "entry_lo", "entry_hi", "support", "stop", "stop_basis", "t1", "t2", "upside_t1", "downside", "rr", "trend_pts", "rs_score", "mom_score", "rr_score", "penalty", "tech_score"]].round(3).to_string())
print(pd.DataFrame(levels).set_index("bank").to_string())
