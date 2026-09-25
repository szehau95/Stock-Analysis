"""
10_rally_vs_stn.py — Module 6: transparent Rally vs Sell-the-News scoring model.
Each factor scored -2 (strong sell-the-news) .. +2 (strong rally); weights sum to 1.
Score -> probabilities via a tilt on MU's own last-16-print base rates:
    P_rally ∝ base_rally * exp(k*score), P_stn ∝ base_stn * exp(-k*score), P_chop ∝ base_chop, k = 0.6
(rally = 1-day move > +3%, sell-the-news = < -3%, chop = within +/-3%).  Cross-checked against the Module-5 MC.
"""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
ev = pd.read_csv(REPO / "hist_moves.csv")
setup = pd.read_csv(ROOT / "data" / "setup_summary.csv", index_col=0)["value"]
bp = pd.read_csv(ROOT / "data" / "beat_probabilities.csv", index_col=0)["value"]
opt = pd.read_csv(ROOT / "data" / "options_summary.csv", index_col=0)["value"]
mc = pd.read_csv(ROOT / "data" / "scenario_mc_summary.csv", index_col=0)["value"]

last16 = ev.tail(16)
base = dict(rally=(last16.r1 > 0.03).mean(), stn=(last16.r1 < -0.03).mean(), chop=(last16.r1.abs() <= 0.03).mean())

F = [
    # factor, weight, score, evidence
    ("Pre-print run-up percentile", 0.15, -1.5,
     f"20d +{float(setup['drift20_asof_2409_pct']):.1f}% (as of 24/09) = {float(setup['drift20_pctile_vs_all_prints']):.0f}th pctile of prints since 2017; "
     f"+{float(setup['rel_drift20_vs_soxx_pp']):.1f}pp vs SOXX; +{float(setup['mu_pct_above_low']):.0f}% off 29/07 low; +16.6% in the week to 22/09"),
    ("IV rank / implied vs realised", 0.10, 0.25,
     f"IV30 61% at 52w IV pctl ~20% (not euphoric); straddle-implied {float(opt['B_implied_move_2026-10-02_pct']):.1f}% vs "
     f"last-8 mean |1d| {float(opt['hist8_mean_abs_r1_pct']):.1f}% -> options not over-bid"),
    ("Estimate revision momentum", 0.15, -1.0,
     "FQ4 consensus drifting up (+1.1% 11/09->24/09), FY27 EPS raised (Wells +10%, GS +4.9%) while stock +15%: bar being raised into print"),
    ("Guide vs whisper gap (Module 2c)", 0.25, -1.25,
     f"P(FQ1 guide > consensus) {100*float(bp['P(FQ1 rev guide mid > consensus $56.7bn)']):.0f}%, "
     f"P(> whisper) {100*float(bp['P(FQ1 rev guide mid > whisper mid $58.5bn)']):.0f}%; 14->13 week optics: E[headline QoQ] "
     f"+{float(bp['E[FQ1 guide headline QoQ %]']):.1f}% vs FQ4 +{float(bp['E[FQ4 actual headline QoQ % vs FQ3 $41.456bn]']):.0f}%"),
    ("Positioning crowding", 0.10, -0.75,
     "GS HF crowding at record (Q2-26); MU = Coatue's top Q2 buy; DRAM ETF AUM $26bn; call-over-put skew +4.3 vol pts; "
     "offset: SI only 2.6-3.3% of float (DTC ~1) though multi-year high; Burry short = squeeze fuel on a clean beat"),
    ("Valuation vs peak-cycle history", 0.10, 0.5,
     f"{float(setup['pe_fy27_cons_at_2409']):.1f}x FY27 consensus EPS $156.53 vs P/E on realised peak NTM EPS 3.4x (2018) / 8.9x (2021); "
     "mean PT $1,515-1,565 (+40-45%): valuation cushions a dip, doesn't stop a sell-the-news day"),
    ("Historical analogs", 0.15, -1.0,
     "Up-cycle beat-and-raise often sold: Mar-18 -8.0%, Jun-24 -7.1%, Sep-25 -2.8%, Mar-26 -3.8% (r5 -17%) vs rallies Dec-25 +10.2%, "
     "Jun-26 +15.7% (guide +15-32% vs cons). Last 14-week FQ4 (Sep-20): guide -14% headline QoQ, stock -7.4%. "
     "Peers on record prints: SK Hynix Q2-26 -9%, Samsung Q2-26 -7% (capex). Last 16Q: P(down | beat vs guide) = 62%"),
]
df = pd.DataFrame(F, columns=["factor", "weight", "score_-2_to_+2", "evidence"])
assert abs(df.weight.sum() - 1) < 1e-9
score = float((df.weight * df["score_-2_to_+2"]).sum())
k = 0.6
raw = dict(rally=base["rally"] * np.exp(k * score), stn=base["stn"] * np.exp(-k * score), chop=base["chop"])
tot = sum(raw.values())
prob = {kk: 100 * v / tot for kk, v in raw.items()}
df["contribution"] = df.weight * df["score_-2_to_+2"]
df.to_csv(ROOT / "data" / "stn_score_factors.csv", index=False)
out = pd.Series({
    "composite_score_-2_to_+2": score,
    "base_rate_rally_gt3_pct": 100 * base["rally"], "base_rate_stn_lt-3_pct": 100 * base["stn"],
    "base_rate_chop_pct": 100 * base["chop"],
    "P_rally_pct": prob["rally"], "P_sell_the_news_pct": prob["stn"], "P_chop_pct": prob["chop"],
    "MC_cross_check_P_rally_gt3": float(mc["P_rally_gt_+3pct"]),
    "MC_cross_check_P_stn_lt-3": float(mc["P_selloff_lt_-3pct"]),
    "MC_cross_check_P_chop": float(mc["P_chop_within_+/-3pct"]),
})
out.to_csv(ROOT / "data" / "stn_score_summary.csv", header=["value"])
pd.set_option("display.width", 220); pd.set_option("display.max_colwidth", 90)
print(df[["factor", "weight", "score_-2_to_+2", "contribution"]].to_string())
print(); print(out.round(2).to_string())
top3 = df.reindex(df.contribution.abs().sort_values(ascending=False).index).head(3)
print("\ntop-3 drivers:", "; ".join(top3.factor))
