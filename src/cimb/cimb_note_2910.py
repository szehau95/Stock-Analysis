"""CIMB single-name note, AS_OF 29/10/2026 close: why it fell, peer/history multiples, rate and Indonesia risk, 12m target.

Prices: Yahoo daily to 29/10/2026 (T3; CIMB close matches the client's screenshot). MGS: BNM FMIP benchmark (T1).
Balance sheet, P&L, capital: CIMB Group condensed interim FS 30/06/2026 (T1). Niaga 9M26: The Edge 29/10/2026 (T2).
"""
import os, sys
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
sys.path.insert(0, "src/screen")
from common import panel, quarterly  # noqa: E402

RAW, OUT = "data/raw/scr2910", "output/cimb"
os.makedirs(OUT, exist_ok=True)
ASOF = pd.Timestamp("2026-10-29")
BANKS = ["MAYBANK", "PBBANK", "CIMB", "HLBANK", "RHBBANK", "AMBANK"]
ERP, G, TAX = 0.06, 0.04, 0.24


def px(k):
    h = pd.read_csv(f"{RAW}/yf_{k}.csv", index_col=0, parse_dates=True)
    h.index = pd.to_datetime(h.index).normalize()
    return h[~h.index.duplicated()].sort_index().loc[:ASOF]


P = {k: px(k) for k in BANKS + ["KLCI"]}
close = pd.DataFrame({k: v.Close for k, v in P.items()}).dropna()

# ---- 1. What happened: returns over windows, and CIMB's large down days vs peers and volume ----
win = {"1M (30/09->29/10)": "2026-09-30", "since 13/10 screen": "2026-10-13", "YTD (31/12/2025)": "2025-12-31"}
ret = pd.DataFrame({k: close.loc[ASOF] / close.loc[:d].iloc[-1] - 1 for k, d in win.items()})
adjc = pd.DataFrame({k: v["Adj Close"] for k, v in P.items() if k != "KLCI"}).dropna()  # total return: ex-dividend gaps are not selling
for k, d in win.items():
    ret[f"TR {k}"] = adjc.loc[ASOF] / adjc.loc[:d].iloc[-1] - 1
r = close.pct_change()
vol = P["CIMB"].Volume
vmult = vol / vol.rolling(20).median().shift(1)
big = r.loc["2026-09-01":, "CIMB"].sort_values().head(4).index.sort_values()
days = pd.DataFrame({"CIMB": r.loc[big, "CIMB"], "peer_median_ex_CIMB": r.loc[big, [b for b in BANKS if b != "CIMB"]].median(axis=1),
                     "KLCI": r.loc[big, "KLCI"], "CIMB_close": close.loc[big, "CIMB"], "vol_x_20d_median": vmult.loc[big],
                     "vol_m": vol.loc[big] / 1e6})
days["CIMB_vs_peers_pp"] = (days.CIMB - days.peer_median_ex_CIMB) * 100

# ---- 2. Rates: MGS since the last reported balance sheet (30/06) and since the screen (13/10) ----
m_old = pd.read_csv("data/raw/scr1410/mgs_daily_bnm.csv", parse_dates=["date"])
m_new = pd.read_csv(f"{RAW}/mgs_daily_bnm.csv", parse_dates=["date"])
mgs = pd.concat([m_old, m_new]).drop_duplicates("date", keep="last").set_index("date").sort_index()[["3Y", "5Y", "7Y", "10Y"]].ffill()
at = lambda d: mgs.loc[:d].iloc[-1]
MGS10 = at(ASOF)["10Y"] / 100
dy_since_jun = (at(ASOF) - at("2026-06-30")).mean() / 100      # average 3/5/7/10Y move, decimal
dy_since_sep = (at(ASOF) - at("2026-09-30")).mean() / 100      # 4Q-to-date
dy_short_4q = (at(ASOF) - at("2026-09-30"))[["3Y", "5Y"]].mean() / 100

# ---- 3. CIMB T1 inputs (FS 30/06/2026, RM bn unless stated) ----
T1 = dict(equity=70.261905, goodwill=6.004259, intang=2.012954, naps=6.50, np_1h26=3.854697, eps_1h26_sen=35.69,
          np_1h25=3.862122, inc_1h26=10.972354, inc_1h25=11.100769, opex_1h26=5.069536, opex_1h25=5.130922,
          ppop_1h26=5.902818, ppop_1h25=5.969847, ecl_1h26=0.798352, ecl_1h25=0.696118, pbt_1h26=5.158443, pbt_1h25=5.274629,
          nii_1h26=5.371835, nii_1h25=5.604576, isl_1h26=2.416183, isl_1h25=2.481054, fee_1h26=1.187921, fee_1h25=1.196457,
          onoii_1h26=1.996415, onoii_1h25=1.818682, loans=450.594779, loans_dec=444.920430, dep=483.734893, inv_acc=35.984177,
          fvoci=83.682439, fvtpl=66.730107, fvtpl_govt=46.318, ac=82.165817, rwa=389.749722, cet1_pre=0.14458, cet1_post=0.13911,
          fvoci_reserve=-0.451390, fx_reserve=-3.925736, oci_fx_1h26=-1.201185, oci_fvoci_1h26=-0.645524, assets=794.851196)
SH = T1["np_1h26"] / (T1["eps_1h26_sen"] / 100)                  # weighted shares, bn (10.80)
tbvps = (T1["equity"] - T1["goodwill"] - T1["intang"]) / SH
qa = quarterly("CIMB").sort_values("qdate")
eps_t4q = qa.eps_sen.iloc[-4:].sum() / 100
dps_t4q = qa.dps_sen.iloc[-4:].sum() / 100
dps_ord = dps_t4q - qa.dps_sen.iloc[-4:][qa.dps_sen.iloc[-4:] < 10].sum() / 100  # strip the 7-sen special (3Q25)
bv_hist = qa.set_index("qdate").nta.iloc[-13:]                     # NAPS by quarter (screen data, T3; ties to T1 6.50)
bv_cagr_3y = (bv_hist.iloc[-1] / bv_hist.iloc[0]) ** (1 / 3) - 1

fin = pd.Series({
    "operating income 1H26 yoy": T1["inc_1h26"] / T1["inc_1h25"] - 1,
    "NII (conventional) yoy": T1["nii_1h26"] / T1["nii_1h25"] - 1,
    "Islamic banking income yoy": T1["isl_1h26"] / T1["isl_1h25"] - 1,
    "net fee income yoy": T1["fee_1h26"] / T1["fee_1h25"] - 1,
    "other NOII yoy": T1["onoii_1h26"] / T1["onoii_1h25"] - 1,
    "NOII share of income 1H26": (T1["fee_1h26"] + T1["onoii_1h26"]) / T1["inc_1h26"],
    "opex yoy": T1["opex_1h26"] / T1["opex_1h25"] - 1,
    "CIR 1H26": T1["opex_1h26"] / T1["inc_1h26"],
    "PPOP yoy": T1["ppop_1h26"] / T1["ppop_1h25"] - 1,
    "loan ECL yoy": T1["ecl_1h26"] / T1["ecl_1h25"] - 1,
    "PBT yoy": T1["pbt_1h26"] / T1["pbt_1h25"] - 1,
    "net profit yoy": T1["np_1h26"] / T1["np_1h25"] - 1,
    "LDR (customer deposits)": T1["loans"] / T1["dep"],
    "LDR (deposits + investment accounts)": T1["loans"] / (T1["dep"] + T1["inv_acc"]),
    "securities / total assets": (T1["fvoci"] + T1["fvtpl"] + T1["ac"]) / T1["assets"],
    "FVTPL share of securities": T1["fvtpl"] / (T1["fvoci"] + T1["fvtpl"] + T1["ac"]),
    "CET1 after proposed dividend": T1["cet1_post"],
    "BVPS 3y CAGR (2Q23-2Q26)": bv_cagr_3y,
    "1H26 OCI: FX translation (RM bn)": T1["oci_fx_1h26"],
    "1H26 OCI: FVOCI debt (RM bn)": T1["oci_fvoci_1h26"],
})

# ---- 4. Rate risk: FVOCI marks (reserve is already negative, so losses hit CET1 in full) and 4QTD FVTPL ----
D = pd.read_csv("output/screen/m2b_treasury.csv", index_col=0).loc["CIMB", "duration"]  # calibrated to RHB Research 52bp
loss = lambda dy: T1["fvoci"] * D * dy * (1 - TAX)
rate = pd.Series({
    "MGS10 29/10": MGS10, "avg 3-10Y move since 30/06 (bp)": dy_since_jun * 1e4, "avg move 4QTD (bp)": dy_since_sep * 1e4,
    "effective FVOCI duration (calibrated)": D,
    "BV hit since 30/06 (sen/share)": loss(dy_since_jun) / SH * 100,
    "CET1 hit since 30/06 (bp)": max(loss(dy_since_jun), 0) / T1["rwa"] * 1e4,
    "BV hit per +100bp (% of equity)": loss(0.01) / T1["equity"],
    "CET1 hit per +100bp (bp)": loss(0.01) / T1["rwa"] * 1e4,
    "4QTD FVTPL govt mark, unhedged pre-tax (RM m)": T1["fvtpl_govt"] * 1.5 * dy_short_4q * 1e3,
})

# ---- 5. Indonesia: Niaga's weight and the 3Q run-rate drop (derived from T2 figures) ----
NIAGA = dict(np_9m_rm=1.01, np_9m_idr=4.49, stake=0.9145, roe_9m=0.109, roe_3q=0.076)
# 9M ROE is the average of 1H (two quarters) and 3Q, so the 1H run-rate solves 2*r1 + r3 = 3*roe_9m
roe_1h = (3 * NIAGA["roe_9m"] - NIAGA["roe_3q"]) / 2
q_np_1h = NIAGA["np_9m_rm"] / (2 + NIAGA["roe_3q"] / roe_1h)       # equity broadly flat over 9M (assumption, stated)
q_np_3q = q_np_1h * NIAGA["roe_3q"] / roe_1h
grp_q = T1["np_1h26"] / 2
indo = pd.Series({"Niaga implied 1H ROE": roe_1h, "Niaga quarterly NP 1H avg (RM bn)": q_np_1h, "Niaga 3Q NP (RM bn)": q_np_3q,
                  "Niaga share of group NP (1H run-rate, attributable)": q_np_1h * NIAGA["stake"] / grp_q,
                  "3Q drag vs 1H run-rate, % of group quarterly NP": (q_np_1h - q_np_3q) * NIAGA["stake"] / grp_q,
                  "privatisation cost (PIVB est., RM bn)": 0.8,
                  "privatisation cost, CET1 bp (if fully deducted)": 0.8 / T1["rwa"] * 1e4})

# ---- 6. Peer multiples at 29/10 (BV/EPS/DPS from the 14/10 screen, latest reported quarter) ----
F = pd.read_csv("output/screen/m14_fundamentals_all9.csv", index_col=0).loc[BANKS]
peer = pd.DataFrame({"price": close.loc[ASOF, BANKS]})
peer["P/B"] = peer.price / F.bvps
peer["P/B core (HLB ex-BoCD)"] = peer.price.where(peer.index != "HLBANK", peer.price - F.addon_ps) / F.bv_core
peer["P/TBV"] = peer.price / F.tbvps
peer["P/E T4Q"] = peer.price / F.eps_t4q_core
peer["DY T4Q"] = F.dps_t4q / peer.price
peer["ROE T4Q"] = F.roe_t4q_core
peer["5y P/B mean"] = F.pb5_mean
peer["5y P/B low"] = np.nan
peer["P/B z (5y)"] = (peer["P/B"] - F.pb5_mean) / F.pb5_sd
peer["off 52w high"] = peer.price / F.hi52 - 1
peer.loc["CIMB", ["P/B", "P/B core (HLB ex-BoCD)"]] = close.loc[ASOF, "CIMB"] / T1["naps"]
peer.loc["CIMB", "P/TBV"] = close.loc[ASOF, "CIMB"] / tbvps
peer.loc["CIMB", "P/E T4Q"] = close.loc[ASOF, "CIMB"] / eps_t4q
peer.loc["CIMB", "DY T4Q"] = dps_t4q / close.loc[ASOF, "CIMB"]
pb_hist = panel("CIMB").pb.dropna()
pb_hist = pd.concat([pb_hist, close.CIMB[close.index > pb_hist.index.max()] / T1["naps"]])
pb5 = pb_hist[pb_hist.index > ASOF - pd.DateOffset(years=5)]
peer.loc["CIMB", "5y P/B low"] = pb5.min()
peer.loc["CIMB", "P/B z (5y)"] = (peer.loc["CIMB", "P/B"] - pb5.mean()) / pb5.std()
hist = pd.Series({"5y mean": pb5.mean(), "5y sd": pb5.std(), "5y min": pb5.min(), "5y max": pb5.max(),
                  "percentile now": (pb5 < peer.loc["CIMB", "P/B"]).mean()}).round(4)
hist["date of 5y min"], hist["date of 5y max"] = str(pb5.idxmin().date()), str(pb5.idxmax().date())

# ---- 7. Beta and COE (3y weekly vs KLCI, Blume) ----
w = pd.concat([close.CIMB.resample("W-FRI").last().pct_change(), close.KLCI.resample("W-FRI").last().pct_change()], axis=1).dropna()
w = w[w.index > ASOF - pd.DateOffset(years=3)]
b_raw = np.cov(w.iloc[:, 0], w.iloc[:, 1])[0, 1] / w.iloc[:, 1].var()
b_blume = 0.67 * b_raw + 0.33
coe = {"beta=1": MGS10 + ERP, "midpoint": MGS10 + (1 + b_blume) / 2 * ERP, "Blume": MGS10 + b_blume * ERP}
jpb = lambda roe, k, g=G: (roe - g) / (k - g)
grid = pd.DataFrame({f"COE {k} {v:.1%}": [jpb(x, v) for x in (0.10, 0.105, 0.11, 0.115, 0.12)] for k, v in coe.items()},
                    index=["ROE 10.0%", "ROE 10.5%", "ROE 11.0%", "ROE 11.5%", "ROE 12.0%"])
px_now = close.loc[ASOF, "CIMB"]
implied_coe = G + (eps_t4q / T1["naps"] - G) / (px_now / T1["naps"])  # P/B = (ROE-g)/(COE-g) solved for COE at T4Q ROE

# ---- 8. 12-month scenarios: target P/B (justified) x forward BVPS; TSR adds 12m ordinary DPS ----
# Forward BVPS = 30/06 NAPS + 16 months of retained earnings at scenario ROE (55% payout, the stated policy)
#               - FVOCI mark from the scenario yield move (no reserve buffer) - FX translation (bear repeats 1H26's loss).
# Buybacks/specials are cash returns at ~book and are left out of both BV and TSR (TSR-neutral to first order).
def scen(roe, k, dy, fx_bn, payout=0.55, months=16):
    bv = T1["naps"] * (1 + roe * (1 - payout)) ** (months / 12) - loss(dy) / SH - (-fx_bn) / SH
    pb = jpb(roe, k)
    tp = pb * bv
    dps = roe * T1["naps"] * payout
    return dict(roe=roe, coe=k, yld_move_bp=dy * 1e4, fx_bn=fx_bn, fwd_bvps=bv, target_pb=pb, value=tp, dps_12m=dps,
                tsr=(tp + dps) / px_now - 1)


S = pd.DataFrame({
    "Bear": scen(0.100, coe["Blume"], 0.0075, T1["oci_fx_1h26"]),
    "Base": scen(0.110, coe["midpoint"], 0.0, 0.0),
    "Bull": scen(0.120, coe["beta=1"], -0.0025, 0.0),
}).T
S["prob"] = [0.25, 0.50, 0.25]
pw_value = (S.value * S.prob).sum()
pw_tsr = (S.tsr * S.prob).sum()
alt_specs = pd.Series({"all-Blume COE (screen method)": jpb(0.11, coe["Blume"]) * S.loc["Base", "fwd_bvps"],
                       "all-beta=1 COE": jpb(0.11, coe["beta=1"]) * S.loc["Base", "fwd_bvps"],
                       "5y mean P/B x fwd BV": pb5.mean() * S.loc["Base", "fwd_bvps"],
                       "Kenanga 1.03x x fwd BV": 1.03 * S.loc["Base", "fwd_bvps"]})
# Rating rule (fixed before looking at the answer): Buy if 12m TSR > base COE + 5pp; Reduce if TSR < 0; else Hold.
rating = "Buy" if pw_tsr > coe["midpoint"] + 0.05 else ("Reduce" if pw_tsr < 0 else "Hold")
pw_dps = (S.dps_12m * S.prob).sum()
buy_below = (pw_value + pw_dps) / (1 + coe["midpoint"] + 0.05)   # price at which the expected TSR clears the Buy hurdle
reduce_above = pw_value + pw_dps                                  # price at which the expected TSR turns negative

# ---- 9. Technicals on dividend-adjusted closes (last bar has no pending adjustment, so levels are comparable) ----
adj = P["CIMB"]["Adj Close"]
ema = lambda n: adj.ewm(span=n, adjust=False).mean().iloc[-1]
tech = pd.Series({"close": px_now, "EMA9": ema(9), "EMA21": ema(21), "EMA50": ema(50), "SMA200": adj.rolling(200).mean().iloc[-1],
                  "40w MA": adj.resample("W-FRI").last().rolling(40).mean().iloc[-1],
                  "52w high (raw)": P["CIMB"].High.iloc[-252:].max(), "52w low (raw, incl. today)": P["CIMB"].Low.iloc[-252:].min(),
                  "drawdown from 52w high": px_now / P["CIMB"].High.iloc[-252:].max() - 1,
                  "below SMA200": px_now / adj.rolling(200).mean().iloc[-1] - 1,
                  "BB lower (20,2)": adj.rolling(20).mean().iloc[-1] - 2 * adj.rolling(20).std().iloc[-1],
                  "14d RSI": (lambda d: 100 - 100 / (1 + d.clip(lower=0).ewm(alpha=1 / 14).mean().iloc[-1] /
                                                     (-d.clip(upper=0)).ewm(alpha=1 / 14).mean().iloc[-1]))(adj.diff()),
                  }).round(4)
prev = close.CIMB.iloc[:-1]
tech["last raw close at or below today's"] = str(prev[prev <= px_now].index.max().date()) if (prev <= px_now).any() else "n/a"

pd.set_option("display.width", 250, "display.max_columns", 30)
blocks = {"returns": ret, "big_days": days, "financials_1h26": fin, "rate_risk": rate, "indonesia": indo, "peers": peer,
          "pb_history": hist, "jpb_grid": grid, "scenarios": S, "alt_specs": alt_specs, "technicals": tech}
for k, v in blocks.items():
    print(f"\n== {k} ==")
    print((v.round(4) if not (isinstance(v, pd.Series) and v.dtype == object) else v).to_string())
    v.to_csv(f"{OUT}/{k}.csv")
summary = pd.Series({"price": px_now, "shares_bn": SH, "tbvps": tbvps, "eps_t4q": eps_t4q, "dps_t4q": dps_t4q, "dps_ordinary_t4q": dps_ord,
                     "beta_raw": b_raw, "beta_blume": b_blume, "coe_beta1": coe["beta=1"], "coe_mid": coe["midpoint"], "coe_blume": coe["Blume"],
                     "implied_coe_t4q_roe": implied_coe, "pw_value": pw_value, "pw_dps": pw_dps, "pw_tsr": pw_tsr,
                     "buy_below": buy_below, "reduce_above": reduce_above, "rating": rating,
                     "rote_1h26_ann": T1["np_1h26"] * 2 / (T1["equity"] - T1["goodwill"] - T1["intang"])})
print("\n== summary ==")
print(summary.to_string())
summary.to_csv(f"{OUT}/summary.csv")
