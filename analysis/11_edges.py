"""
11_edges.py — Module 7: where the edge is. Quantifies each edge candidate, then scores Edge (0-5) x Confidence.
Inputs: hist_moves.csv, data/options_summary.csv, data/scenario_mc_summary.csv, mc_core simulation, prices.
Writes edge_scores.csv (repo root) and data/edge_stats.csv
"""
import pathlib
import numpy as np
import pandas as pd
from mc_core import simulate

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
ev = pd.read_csv(REPO / "hist_moves.csv", parse_dates=["report_date"])
opt = pd.read_csv(ROOT / "data" / "options_summary.csv", index_col=0)["value"].astype(float)
mcs = pd.read_csv(ROOT / "data" / "scenario_mc_summary.csv", index_col=0)["value"].astype(float)
C = pd.read_csv(ROOT / "data" / "prices_close.csv", index_col=0, parse_dates=True)
st = {}

# ---------- read-through: beta & correlation of peers' print-day moves to MU (last 16 prints) ----------
l16 = ev.tail(16)
for col in ["soxx_r1", "hynix_r1", "samsung_r1", "nvda_r1", "lrcx_r1", "amat_r1", "klac_r1", "wdc_r1", "stx_r1"]:
    x, y = l16["r1"], l16[col]
    ok = x.notna() & y.notna()
    if ok.sum() >= 8:
        st[f"beta_{col}_to_MU_r1"] = np.polyfit(x[ok], y[ok], 1)[0]
        st[f"corr_{col}_MU_r1"] = np.corrcoef(x[ok], y[ok])[0, 1]
sn = ev.dropna(subset=["sndk_r1"])
if len(sn) >= 4:
    st["beta_sndk_r1_to_MU_r1 (n=%d)" % len(sn)] = np.polyfit(sn.r1, sn.sndk_r1, 1)[0]

# ---------- post-print drift (days 2-20) conditional on print-day sign ----------
for lab, sub in [("last16", l16), ("upcycle_all", ev[ev.phase == "up"])]:
    st[f"{lab}_mean_d2_20_after_up_day"] = sub[sub.r1 > 0].d2_20.mean()
    st[f"{lab}_mean_d2_20_after_down_day"] = sub[sub.r1 < 0].d2_20.mean()
    st[f"{lab}_pct_down_days_recovered_by_d20"] = (sub[sub.r1 < 0].d2_20 > -sub[sub.r1 < 0].r1).mean()
    st[f"{lab}_pct_up_days_extended_d2_20"] = (sub[sub.r1 > 0].d2_20 > 0).mean()
    st[f"{lab}_n"] = len(sub)
big_down = ev[(ev.r1 < -0.05) & (ev.phase == "up")]
st["upcycle_prints_r1_lt_-5pct_n"] = len(big_down)
st["upcycle_prints_r1_lt_-5pct_mean_d2_20"] = big_down.d2_20.mean()

# ---------- skew vs model distribution ----------
df, _ = simulate()
st["MC_P_move_lt_-10"] = 100 * (df.move < -10).mean()
st["MC_P_move_gt_+10"] = 100 * (df.move > 10).mean()
st["MC_P_move_lt_-7"] = 100 * (df.move < -7).mean()
st["MC_P_move_gt_+7"] = 100 * (df.move > 7).mean()
st["MC_skewness"] = float(pd.Series(df.move).skew())
st["mkt_call_minus_put_iv_7pct_OTM_volpts"] = opt["skew_1002_call_minus_put_volpts"]
# lognormal-ish market-implied tail probs at +/-7% using the strike IVs for the 02/10 expiry (T from 25/09 09:45)
from scipy.stats import norm
T = 7.26 / 365
for strike, ivk, lab in [(1020, opt["skew_1002_put1020_iv"], "P_mkt_S_lt_1020"), (1170, opt["skew_1002_call1170_iv"], "P_mkt_S_gt_1170")]:
    d2 = (np.log(1094.45 / strike) - 0.5 * ivk ** 2 * T) / (ivk * np.sqrt(T))
    st[lab] = 100 * (norm.cdf(-d2) if strike < 1094.45 else norm.cdf(d2))
st["MC_P_below_1020_equiv(-6.8%)"] = 100 * (df.move < -6.8).mean()
st["MC_P_above_1170_equiv(+6.9%)"] = 100 * (df.move > 6.9).mean()

# ---------- vol ----------
st["straddle_implied_1002_live_pct"] = opt["B_implied_move_2026-10-02_pct"]
st["event_only_E_abs_move_pct_range"] = f"{opt['strip_b_fwdVar_event_E_abs_move_pct']:.1f}-{opt['strip_a_preEventExpiry_event_E_abs_move_pct']:.1f}"
st["model_E_abs_1d_move_pct"] = mcs["E_abs_move_pct"]
st["hist16_mean_abs_window_t-4_t+2_pct"] = opt["hist16_mean_abs_window_pct"]
st["hist16_pct_window_gt_implied"] = opt["hist16_pct_window_gt_implied"]

# ---------- relative value: drawdowns / rebounds since 2026 high ----------
for t in ["MU", "000660.KS", "005930.KS", "SNDK", "DRAM", "SOXX", "AMAT", "LRCX"]:
    s = C[t].dropna().loc["2026-01-01":]
    st[f"{t}_pct_vs_2026_high"] = 100 * (s.iloc[-1] / s.max() - 1)
    st[f"{t}_max_drawdown_2026_pct"] = 100 * (s / s.cummax() - 1).min()

# ---------- structured products: buffers vs implied / realised tails ----------
st["KI_buffer_multiple_of_implied_at_30pct"] = 30 / opt["B_implied_move_2026-10-02_pct"]
st["MU_Jul26_drawdown_pct"] = st["MU_max_drawdown_2026_pct"]

stats = pd.Series(st)
stats.to_csv(ROOT / "data" / "edge_stats.csv", header=["value"])

E = [
    ("1 Directional", 3.0, "Medium",
     f"Model EV {mcs['EV_1d_move_pct']:+.1f}%, P(down) {mcs['P_down_pct']:.0f}% vs a market that prices upside richer. "
     "Lean survives the growth sweep (EV<0 for FQ1 per-week growth <=20%).",
     "Personal book: underweight MU into print (trim, don't flip). Institutional: Oct-9 1020/940 put spread (defined risk)."),
    ("2 Vol (straddle)", 1.5, "Low",
     f"Straddle +/-{opt['B_implied_move_2026-10-02_pct']:.1f}% ~= model E|move| {mcs['E_abs_move_pct']:.1f}% and last-8 mean |1d| "
     f"{opt['hist8_mean_abs_r1_pct']:.1f}%; t-4->t+2 window exceeded implied only {opt['hist16_pct_window_gt_implied']:.0f}% of prints "
     "but event-only vol (E|move| 6.3-7.4%) is not rich. Net: noise.",
     "No outright long/short straddle. If forced: short Oct-2 iron condor wings >= +/-12% (calendar risk from 20% tails)."),
    ("3 Skew", 3.5, "Medium",
     f"Market: 7%-OTM call IV {100*opt['skew_1002_call1170_iv']:.1f}% > put IV {100*opt['skew_1002_put1020_iv']:.1f}% (+{opt['skew_1002_call_minus_put_volpts']:.1f} vol pts). "
     f"Model distribution is shifted left (mean {mcs['EV_1d_move_pct']:+.1f}%): P(< -6.8%) {st['MC_P_below_1020_equiv(-6.8%)']:.0f}% vs market-implied "
     f"P(S<1020) {st['P_mkt_S_lt_1020']:.0f}%; P(> +6.9%) {st['MC_P_above_1170_equiv(+6.9%)']:.0f}% vs market-implied P(S>1170) {st['P_mkt_S_gt_1170']:.0f}%. "
     "The market over-prices the right tail and under-prices the left.",
     "Buy Oct-9 1020/940 put spread, sell Oct-9 1170/1240 call spread: ~$3.8 net debit (BS on IBKR IVs, verify live). 1 lot = $109k notional, max loss ~$7.4k -> institutional sizing only, NOT for a $43k book."),
    ("4 Relative value", 2.0, "Low",
     f"MU {st['MU_pct_vs_2026_high']:.0f}% vs 2026 high while SK Hynix {st['000660.KS_pct_vs_2026_high']:.0f}%, SNDK {st['SNDK_pct_vs_2026_high']:.0f}%, "
     f"DRAM ETF {st['DRAM_pct_vs_2026_high']:.0f}%: MU carries the most 'already-recovered' expectations; 14->13-week optics are MU-specific.",
     "Pair: short MU / long SK Hynix (KRX, reopens 28/09) into the print; hedges sector beta, isolates MU optics. Small size; KRX access/FX friction."),
    ("5 Read-through", 2.5, "Medium",
     f"Hynix next-session beta {st.get('beta_hynix_r1_to_MU_r1', np.nan):.2f} (corr {st.get('corr_hynix_r1_MU_r1', np.nan):.2f}); "
     f"LRCX beta {st.get('beta_lrcx_r1_to_MU_r1', np.nan):.2f}, AMAT beta {st.get('beta_amat_r1_to_MU_r1', np.nan):.2f}. "
     "Capex channel is the exception: an FY27 capex guide >= $50bn is MU-negative but semicap-positive (T1).",
     "Korea memory at the 01/10 open reprices at ~0.3x MU's move (hynix beta 0.34, Samsung 0.16); semicap: fade MU-driven weakness in AMAT/LRCX only if the capex guide is >= $45-50bn."),
    ("6 Post-print drift", 1.5, "Low",
     f"Up-cycle prints: mean days 2-20 drift after a down day {100*st['upcycle_all_mean_d2_20_after_down_day']:+.1f}% vs after an up day "
     f"{100*st['upcycle_all_mean_d2_20_after_up_day']:+.1f}%; only {100*st['upcycle_all_pct_down_days_recovered_by_d20']:.0f}% of up-cycle down days were recovered by day 20; "
     f"up-cycle days < -5% (n={st['upcycle_prints_r1_lt_-5pct_n']:.0f}: Mar-18, Jun-21, Jun-24) extended {100*st['upcycle_prints_r1_lt_-5pct_mean_d2_20']:+.1f}% over days 2-20.",
     "Do NOT bottom-fish day 1 of a sell-the-news: historically the first down day is not the low. Re-assess after Samsung prelim (~07/10)."),
    ("7 Structured-product timing", 3.5, "High",
     "Event premium sits in the weekly (Oct-2 IV 79% vs IV30 61%, 52w IV pctl ~20%): a 3-6M KIKO/ELN struck pre-print earns little extra coupon "
     f"but carries the full gap risk (model p05 {mcs['p05_move']:.0f}%; MU drew down {st['MU_max_drawdown_2026_pct']:.0f}% in Jun-Jul 2026).",
     "Issue AFTER the print (01-02/10) on single-name MU (not a worst-of memory basket: Hynix/SNDK drawdowns -55/-57%); strike 90-95%, KI 60% for 6M (40% buffer = ~4.5x implied move), 65% only for <=3M."),
]
edges = pd.DataFrame(E, columns=["edge", "score_0_5", "confidence", "evidence", "expression"])
edges.to_csv(REPO / "edge_scores.csv", index=False)
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 140)
print(stats.to_string())
print(); print(edges[["edge", "score_0_5", "confidence"]].to_string())
