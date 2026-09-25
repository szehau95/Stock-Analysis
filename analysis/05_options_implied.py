"""
05_options_implied.py  — Module 3a / 3b
Inputs : data/ibkr_options_20260924close.csv (IBKR MCP snapshots), prices_close.csv, earnings_dates.csv
Outputs: data/options_summary.csv
  1. Straddle-implied move (ATM straddle / spot) for the first expiry after the print (02/10/2026)
  2. Event-vol strip: event variance = total var(event expiry) - n_days * base daily var
       base daily var from (a) pre-event expiry 28/09 and (b) forward var between 02/10 and 09/10
  3. Skew: ±7% OTM put vs call IV on the event expiry; term structure
  4. Historical comparison: realized |1-day| move and realized |straddle-window| move
     (close t0-4 -> close t0+2, i.e. same window the 02/10 straddle covers) for the last 16 prints
"""
import pathlib
import numpy as np
import pandas as pd
from scipy.stats import norm

ROOT = pathlib.Path(__file__).resolve().parent
opt = pd.read_csv(ROOT / "data" / "ibkr_options_20260924close.csv")
C = pd.read_csv(ROOT / "data" / "prices_close.csv", index_col=0, parse_dates=True)["MU"].dropna()
ed = pd.read_csv(ROOT / "data" / "earnings_dates.csv", parse_dates=["filing_date"])


def bs_straddle(S, K, T, vol):
    """Black-Scholes straddle, r=q=0 (4-7 day tenor; rates immaterial). T in years (calendar)."""
    if T <= 0:
        return abs(S - K)
    d1 = (np.log(S / K) + 0.5 * vol * vol * T) / (vol * np.sqrt(T))
    d2 = d1 - vol * np.sqrt(T)
    call = S * norm.cdf(d1) - K * norm.cdf(d2)
    put = K * norm.cdf(-d2) - S * norm.cdf(-d1)
    return call + put


out = {}
# ---------------- snapshot A: 24/09/2026 close (spot 1080.53), quotes mid ----------------
S0 = 1080.53
a = opt[opt.status == "FROZEN_DELAYED"].copy()
a["mid"] = (a.bid + a.ask) / 2
straddle_1002 = a[(a.expiry == "2026-10-02") & (a.strike == 1080)].mid.sum()
straddle_0928 = a[(a.expiry == "2026-09-28") & (a.strike == 1080)].mid.sum()
straddle_1009 = a[(a.expiry == "2026-10-09") & (a.strike == 1080)].mid.sum()
out["A_spot"] = S0
out["A_straddle_1002_mid"] = straddle_1002
out["A_implied_move_1002_pct"] = 100 * straddle_1002 / S0
out["A_implied_move_0928_pct"] = 100 * straddle_0928 / S0
out["A_implied_move_1009_pct"] = 100 * straddle_1009 / S0

# ---------------- snapshot B: live 25/09/2026 ~09:45 ET (spot 1094.45), IBKR model IVs ----------------
S1 = 1094.45
b = opt[opt.status.str.startswith("DELAYED_LIVE")].copy()
iv = {e: b[(b.expiry == e) & (b.strike == 1095)].iv_annual.iloc[0] for e in ["2026-09-28", "2026-10-02", "2026-10-09"]}
# calendar time from 25/09 09:45 ET to 16:00 ET expiry day
now = pd.Timestamp("2026-09-25 09:45")
Tcal = {e: (pd.Timestamp(e + " 16:00") - now).total_seconds() / 86400 / 365 for e in iv}
# trading days remaining (fraction of today's session left + full sessions)
frac_today = (16 - 9.75) / 6.5
Ttd = {"2026-09-28": frac_today + 1, "2026-10-02": frac_today + 5, "2026-10-09": frac_today + 10}
totvar = {e: iv[e] ** 2 * Tcal[e] for e in iv}
for e in iv:
    out[f"B_iv_{e}"] = iv[e]
    out[f"B_straddle_{e}"] = bs_straddle(S1, 1095, Tcal[e], iv[e])
    out[f"B_implied_move_{e}_pct"] = 100 * out[f"B_straddle_{e}"] / S1
# event strip, method (a): base daily var from pre-event 28/09 expiry
base_a = totvar["2026-09-28"] / Ttd["2026-09-28"]
ev_a = totvar["2026-10-02"] - Ttd["2026-10-02"] * base_a
# method (b): base daily var from forward variance 02/10 -> 09/10 (5 normal sessions)
base_b = (totvar["2026-10-09"] - totvar["2026-10-02"]) / 5
ev_b = totvar["2026-10-02"] - Ttd["2026-10-02"] * base_b
for tag, base, ev in [("a_preEventExpiry", base_a, ev_a), ("b_fwdVar", base_b, ev_b)]:
    out[f"strip_{tag}_base_daily_vol_pct"] = 100 * np.sqrt(base)
    out[f"strip_{tag}_base_annual_vol_pct"] = 100 * np.sqrt(base * 252)
    out[f"strip_{tag}_event_sigma_pct"] = 100 * np.sqrt(max(ev, 0))
    out[f"strip_{tag}_event_E_abs_move_pct"] = 100 * np.sqrt(max(ev, 0)) * np.sqrt(2 / np.pi)
# skew (event expiry, ±7% OTM)
p1020 = b[(b.expiry == "2026-10-02") & (b.strike == 1020)].iv_annual.iloc[0]
c1170 = b[(b.expiry == "2026-10-02") & (b.strike == 1170)].iv_annual.iloc[0]
out["skew_1002_put1020_iv"] = p1020
out["skew_1002_call1170_iv"] = c1170
out["skew_1002_call_minus_put_volpts"] = 100 * (c1170 - p1020)
# 24/09 close skew check (1000P/1160C ~ ±7.4%)
out["skew_A_put1000_iv"] = a[(a.expiry == "2026-10-02") & (a.strike == 1000)].iv_annual.iloc[0]
out["skew_A_call1160_iv"] = a[(a.expiry == "2026-10-02") & (a.strike == 1160)].iv_annual.iloc[0]
# OI context (event expiry)
out["oi_1002_put1000"] = 1713
out["oi_1002_call1080"] = 1053

# ---------------- historical realized: 1-day and straddle-window ----------------
dates = C.index
rows = []
for d in ed.filing_date:
    p = dates.get_indexer([d])[0]
    if p < 4 or p + 2 >= len(dates):
        continue
    rows.append(dict(report_date=d.date(),
                     r1=C.iloc[p + 1] / C.iloc[p] - 1,
                     window=C.iloc[p + 2] / C.iloc[p - 4] - 1))
h = pd.DataFrame(rows).tail(16)
imp_1d_event = out["strip_a_preEventExpiry_event_E_abs_move_pct"] / 100
imp_window = out["A_implied_move_1002_pct"] / 100
out["hist16_mean_abs_r1_pct"] = 100 * h.r1.abs().mean()
out["hist8_mean_abs_r1_pct"] = 100 * h.tail(8).r1.abs().mean()
out["hist16_mean_abs_window_pct"] = 100 * h.window.abs().mean()
out["hist8_mean_abs_window_pct"] = 100 * h.tail(8).window.abs().mean()
out["hist16_pct_window_gt_implied"] = 100 * (h.window.abs() > imp_window).mean()
out["hist16_pct_r1_gt_event_sigma"] = 100 * (h.r1.abs() > out["strip_a_preEventExpiry_event_sigma_pct"] / 100).mean()
out["hist16_pct_r1_gt_straddle_move"] = 100 * (h.r1.abs() > imp_window).mean()
# June-2026 datapoint (Saxo, 23/06/2026): implied +/-11.03%, realized r1 +15.74%
out["jun26_implied_pct_saxo"] = 11.03
out["jun26_realized_r1_pct"] = 15.74

s = pd.Series(out)
s.to_csv(ROOT / "data" / "options_summary.csv", header=["value"])
print(s.round(4).to_string())
print("\nlast 16 straddle-window moves:\n", (h.set_index("report_date") * 100).round(2).to_string())
