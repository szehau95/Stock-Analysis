"""Dividend yields across Malaysian banks at the 29/10/2026 close: trailing (ordinary vs special), latest FY, payout,
forward estimate, own 5y history, spread over MGS10, and upcoming ex-date windows.

Dividends: KLSE Screener history (T3, Bursa entitlement data) cross-checked against Yahoo ex-date amounts (T3).
EPS: quarterly reported EPS (T3, ties to T1 for CIMB). MGS10: BNM FMIP 29/10/2026 (T1). Forward EPS: Yahoo consensus (T3).
"""
import os
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)

ASOF, RAW, OUT = pd.Timestamp("2026-10-29"), "data/raw/scr2910", "output/cimb"
CORE = ["MAYBANK", "PBBANK", "CIMB", "HLBANK", "RHBBANK", "AMBANK"]
CTX = ["BIMB", "ALLIANCE", "AFFIN"]
LATEST_FY = {"MAYBANK": "31 Dec 2025", "PBBANK": "31 Dec 2025", "CIMB": "31 Dec 2025", "RHBBANK": "31 Dec 2025", "HLBANK": "30 Jun 2026",
             "AMBANK": "31 Mar 2026", "BIMB": "31 Dec 2025", "ALLIANCE": "31 Mar 2026", "AFFIN": "31 Dec 2025"}
PRIOR_FY = {"MAYBANK": "31 Dec 2024", "PBBANK": "31 Dec 2024", "CIMB": "31 Dec 2024", "RHBBANK": "31 Dec 2024", "HLBANK": "30 Jun 2025",
            "AMBANK": "31 Mar 2025", "BIMB": "31 Dec 2024", "ALLIANCE": "31 Mar 2025", "AFFIN": "31 Dec 2024"}
MGS10 = pd.read_csv(f"{RAW}/mgs_daily_bnm.csv", parse_dates=["date"]).set_index("date")["10Y"].loc[:ASOF].iloc[-1] / 100
F = pd.read_csv("output/screen/m14_fundamentals_all9.csv", index_col=0)  # 14/10 screen: NTM EPS, T4Q payout, prices


def ks_divs(b):
    d = pd.read_csv(f"data/clean/dividends_ks_{b}.csv", header=0, names=["announced", "fy", "type", "ex", "paid", "amt", "unit"])
    d = d[d.unit == "Currency"].copy()
    d["ex"] = pd.to_datetime(d.ex, format="%d %b %Y")
    d["special"] = d.type.str.contains("Special", case=False)
    return d


def fy_eps(b, fy_label):
    q = pd.read_csv(f"data/clean/quarterly_{b}.csv")
    q["fy_norm"] = q.fy.str.replace(",", "", regex=False)
    sel = q[q.fy_norm == fy_label]
    return sel.eps_sen.sum() / 100 if len(sel) == 4 else np.nan


rows = []
for b in CORE + CTX:
    h = pd.read_csv(f"{RAW}/yf_{b}.csv", index_col=0, parse_dates=True)
    h.index = pd.to_datetime(h.index).normalize()
    P = h.Close.loc[:ASOF].iloc[-1]
    d = ks_divs(b)
    win = d[(d.ex > ASOF - pd.DateOffset(years=1)) & (d.ex <= ASOF)]
    yf_ttm = h.Dividends.loc[ASOF - pd.DateOffset(years=1) + pd.Timedelta(days=1):ASOF].sum()
    fy = d[d.fy == LATEST_FY[b]]
    eps_fy = fy_eps(b, LATEST_FY[b])
    pfy = d[d.fy == PRIOR_FY[b]]
    reg_sorted = d.loc[~d.special].sort_values("ex")
    first_now, first_prev = reg_sorted.amt.iloc[-1], reg_sorted.amt.iloc[-3] if len(reg_sorted) >= 3 else np.nan  # same slot last year
    # own-history yield: daily trailing-365d ordinary DPS (by ex-date) / close; medians, because a 365-day window dips for a
    # few days whenever a payment's ex-date drifts later than a year after the one it replaces
    reg = d.loc[~d.special].set_index("ex").amt.sort_index()
    cl = h.Close.loc[ASOF - pd.DateOffset(years=5):ASOF]
    ttm = pd.Series([reg.loc[t - pd.Timedelta(days=365) + pd.Timedelta(days=1):t].sum() for t in cl.index], index=cl.index)
    dy5 = ttm / cl
    f = F.loc[b]
    ord_payout = win.loc[~win.special, "amt"].sum() / f.eps_t4q_core  # specials stripped so they are not extrapolated
    dy_fwd = f.eps_ntm * ord_payout / P  # 14/10 consensus NTM EPS x trailing ordinary payout, at the 29/10 price
    dy3 = dy5.loc[ASOF - pd.DateOffset(years=3):]
    last_ex = d.ex.max()
    rows.append(dict(bank=b, group="core" if b in CORE else "context", price=P,
                     dps_ttm=win.amt.sum(), dps_ttm_ordinary=win.loc[~win.special, "amt"].sum(), yahoo_ttm_check=yf_ttm,
                     dy_ttm=win.amt.sum() / P, dy_ttm_ordinary=win.loc[~win.special, "amt"].sum() / P,
                     fy=LATEST_FY[b], dps_fy=fy.amt.sum(), dps_fy_growth=fy.amt.sum() / pfy.amt.sum() - 1 if len(pfy) else np.nan,
                     latest_payment=first_now, latest_vs_same_slot_ly=first_now / first_prev - 1, dy_fy=fy.amt.sum() / P, eps_fy=eps_fy, payout_fy=fy.amt.sum() / eps_fy,
                     dy_fwd_est=dy_fwd, dy3_median=dy3.median(), dy5_median=dy5.median(), dy5_p10=dy5.quantile(0.1), dy5_p90=dy5.quantile(0.9),
                     dy_vs_3y_pp=(win.loc[~win.special, "amt"].sum() / P - dy3.median()) * 100,
                     spread_mgs10_pp=(win.loc[~win.special, "amt"].sum() / P - MGS10) * 100,
                     last_ex=last_ex.date(), n_payments_ttm=len(win)))
D = pd.DataFrame(rows).set_index("bank")
K = pd.read_csv("data/clean/scr_kpi_core6.csv").set_index("bank")
D["cet1_pct_latest"] = pd.to_numeric(K.cet1_pct, errors="coerce").reindex(D.index)
D["ttm_check_ok"] = (D.dps_ttm - D.yahoo_ttm_check).abs() < 0.005

# CIMB capital-return optionality: remaining RM2b pledge if paid as specials (RM0.85b per The Edge 21/10; RM1.3b per HLIB/TA 02/09)
SH_CIMB = 10.800496
cimb_extra = pd.Series({f"RM{x}bn remaining": x / SH_CIMB / D.loc["CIMB", "price"] for x in (0.85, 1.3)})
# Malaysia's 2% tax on individuals' chargeable dividend income above RM100k (from YA2025): net yield on the marginal ringgit
D["dy_ttm_ordinary_after_2pct"] = D.dy_ttm_ordinary * 0.98

pd.set_option("display.width", 250, "display.max_columns", 30)
cols = ["price", "dps_ttm", "dps_ttm_ordinary", "dy_ttm", "dy_ttm_ordinary", "dps_fy", "fy", "dy_fy", "dps_fy_growth", "latest_payment", "latest_vs_same_slot_ly", "payout_fy", "cet1_pct_latest", "dy_fwd_est",
        "dy3_median", "dy5_median", "dy5_p10", "dy5_p90", "dy_vs_3y_pp", "spread_mgs10_pp", "last_ex", "ttm_check_ok"]
print(f"MGS10 {MGS10:.2%} (BNM, 29/10/2026)")
print(D[cols].sort_values("dy_ttm_ordinary", ascending=False).round(4).to_string())
print("\nCIMB extra yield if the remaining capital return were paid as special dividends:\n", cimb_extra.round(4).to_string())
D.to_csv(f"{OUT}/div_yield.csv")
cimb_extra.to_csv(f"{OUT}/div_cimb_capital_return.csv")
