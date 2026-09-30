import pandas as pd, numpy as np, json, os
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
BANKS = ["MAYBANK","PBBANK","CIMB","HLBANK","RHBBANK","AMBANK","BIMB","ALLIANCE","AFFIN"]
ASOF = pd.Timestamp("2026-09-30")
def px(k):
    h = pd.read_csv(f"data/raw/yf_{k}.csv", index_col=0, parse_dates=True)
    h.index = pd.to_datetime(h.index).normalize(); h = h[~h.index.duplicated()].sort_index()
    h = h[h.index <= ASOF]
    return h
def panel(b):
    d = pd.read_csv(f"data/clean/panel_{b}.csv", index_col=0, parse_dates=True, low_memory=False)
    for c in ["qdate","announced"]: d[c] = pd.to_datetime(d[c])
    return d[d.index <= ASOF]
def fin(): return json.load(open("data/clean/yf_fin_consensus.json"))
def mgs():
    m = pd.read_csv("data/clean/mgs_monthly_bnm.csv", parse_dates=["date"]).dropna(subset=["10Y"]).set_index("date")["10Y"] / 100
    return m
def mcap_weights():
    f = fin(); w = pd.Series({b: f[b]["mcap"] for b in BANKS}); return w / w.sum()
def composite(kind="tr", weights=None):
    """Cap-weighted (current-cap, rebalanced daily) bank composite index built from daily returns."""
    w = mcap_weights() if weights is None else weights
    rets = {}
    for b in BANKS:
        d = panel(b)
        rets[b] = d.tr_idx.pct_change() if kind == "tr" else d.Close.pct_change()
    R = pd.DataFrame(rets).dropna(how="all")
    W = R.notna().mul(w, axis=1); W = W.div(W.sum(axis=1), axis=0)
    r = (R.fillna(0) * W).sum(axis=1)
    return (1 + r).cumprod()
def fmt_pct(x, d=1): return "n/a" if pd.isna(x) else f"{x*100:+.{d}f}%"
