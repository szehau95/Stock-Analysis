"""Render report tables (markdown) from module outputs."""
import pandas as pd, numpy as np
from common import *
P = lambda x, d=1: "n/a" if pd.isna(x) else f"{x*100:+.{d}f}%"
p = lambda x, d=1: "n/a" if pd.isna(x) else f"{x*100:.{d}f}%"
f2 = lambda x, d=2: "n/a" if pd.isna(x) else f"{x:.{d}f}"
out = []
M1 = pd.read_csv("output/m1_drawdowns.csv", index_col=0)
t = pd.DataFrame({"52w high (date)": [f"{r.hi_52w:.2f} ({pd.Timestamp(r.hi_date).strftime('%d/%m/%Y')})" for r in M1.itertuples()],
  "Current": M1.current.map(lambda x: f"{x:,.2f}"), "Px DD": M1.dd_pr.map(P), "TR DD": M1.dd_tr.map(P), "TR DD (USD)": M1.dd_tr_usd.map(P),
  "Ex-div share of px DD": [("n/a" if (pd.isna(x) or (n not in BANKS and not n.startswith("BANK"))) else f"{x*100:.0f}%") for n, x in M1.div_share_of_pr_dd.items()],
  "YTD px": M1.ytd_pr.map(P), "YTD TR": M1.ytd_tr.map(P), "1m": M1.m1.map(P), "3m": M1.m3.map(P),
  "vs KLCI since high": M1.rel_klci_since_hi.map(P), "Leg1 TR (trough)": [("n/a" if pd.isna(r.leg1_tr) else f"{r.leg1_tr*100:+.1f}% ({pd.Timestamp(r.leg1_trough).strftime('%d/%m')})") for r in M1.itertuples()],
  "Leg2 TR (from)": [f"{r.leg2_tr*100:+.1f}% ({pd.Timestamp(r.leg2_high).strftime('%d/%m')})" for r in M1.itertuples()]}, index=M1.index)
out.append(("M1_TABLE", t.to_markdown()))
ex = M1[["exdiv_in_window","days_tr_le_-2pct","top5_share_of_tr_dd","pattern"]].dropna(subset=["pattern"])
ex = ex.assign(top5_share_of_tr_dd=ex.top5_share_of_tr_dd.map(lambda x: f"{x*100:.0f}%"), **{"days_tr_le_-2pct": ex["days_tr_le_-2pct"].astype(int)})
out.append(("M1_EXDIV", ex.rename(columns={"exdiv_in_window":"Ex-div in window (DD/MM/YYYY:RM)","days_tr_le_-2pct":"Days TR<=-2%","top5_share_of_tr_dd":"Top-5 days / max TR DD","pattern":"Pattern"}).to_markdown()))
PE = pd.read_csv("output/m1_peers.csv", index_col=0)
out.append(("M1_PEERS", pd.DataFrame({"52w high": PE.hi_date.map(lambda x: pd.Timestamp(x).strftime('%d/%m/%Y')), "Px DD": PE.dd_pr.map(P), "TR DD (USD)": PE.dd_tr_usd.map(P), "YTD px (LCY)": PE.ytd_pr.map(P), "YTD TR (USD)": PE.ytd_tr_usd.map(P), "3m": PE.m3.map(P)}).to_markdown()))
DN = pd.read_csv("output/m1_down_days.csv")
DN["date"] = pd.to_datetime(DN.date).dt.strftime("%d/%m/%Y"); DN["ret"] = DN.ret.map(P); DN["gap_open"] = DN.gap_open.map(P); DN["vol_x60d"] = DN.vol_x60d.map(lambda x: f"{x:.1f}x")
out.append(("M1_DOWNDAYS", DN.rename(columns={"ret":"TR day","gap_open":"Gap at open","vol_x60d":"Vol vs 60d"}).to_markdown(index=False)))
FA = pd.read_csv("output/m2_factor_attribution.csv", index_col=0)
fa = FA[["weeks","actual_bank_tr","contrib_r_nonbank","contrib_d_mgs","contrib_d_ust","contrib_r_myr","contrib_r_brent","alpha_drift","residual_unexplained","mgs_move_bps","ust_move_bps","brent_move","nonbank_move"]].copy()
for c in fa.columns:
    if c not in ("weeks","mgs_move_bps","ust_move_bps"): fa[c] = fa[c].map(P)
out.append(("M2_FACTORS", fa.T.to_markdown()))
D = pd.read_csv("output/m2_decomposition.csv", index_col=0)
dd = pd.DataFrame({"From (52w high)": D.from_date.map(lambda x: pd.Timestamp(x).strftime('%d/%m/%Y')), "Price chg": D.price_chg.map(P), "TR chg": D.tr_chg.map(P),
   "EPS(core TTM) effect": D.eps_effect.map(P), "P/E effect": D.pe_effect.map(P), "BV effect": D.bv_effect.map(P), "P/B effect": D.pb_effect.map(P), "Dividend effect": D.dividend_effect.map(P),
   "DY-MGS spread now": D.spread_now.map(lambda x: f"{x*100:+.2f}pp"), "1y ago": D.spread_1y_ago.map(lambda x: f"{x*100:+.2f}pp"), "at 52w high": D.spread_at_52w_high.map(lambda x: f"{x*100:+.2f}pp")})
out.append(("M2_DECOMP", dd.to_markdown()))
LI = pd.read_csv("output/m2_local_institutions.csv", header=[0,1], index_col=0)
out.append(("M2_LOCAL", LI.fillna(0).astype(int).to_markdown()))
S = pd.read_csv("output/m3_scorecard.csv", index_col=0)
s3 = pd.DataFrame({"Rank": S["rank"], "Score": S.score.map(f2), "Core ROE": S.roe_core.map(p), "10y avg": S.roe_core_10y_avg.map(p), "ROE z(10y)": S.roe_core_z10y.map(f2),
  "ΔROE 4Q": S.roe_trend_4q.map(lambda x: f"{x*1e4:+.0f}bp"), "EPS g YoY": S.eps_growth_yoy.map(P), "NIM": S.nim_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.2f}%"),
  "NIM YoY": S.nim_yoy_bps.map(lambda x: "n/a" if pd.isna(x) else f"{x:+.0f}bp"), "CASA": S.casa_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.1f}%"), "CIR": S.cir_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.1f}%"),
  "CC (bp)": S.credit_cost_bps.map(lambda x: "n/a" if pd.isna(x) else f"{x:.0f}"), "GIL": S.gil_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.2f}%"), "LLC": S.llc_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.0f}%"),
  "CET1": S.cet1_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.1f}%"), "Loans YoY": S.loan_growth_pct.map(lambda x: "n/a" if pd.isna(x) else f"{x:.1f}%"),
  "DPS TTM (RM)": S.dps_ttm.map(lambda x: f"{x:.3f}"), "Payout": S.payout_ttm.map(p), "DY": S.dy.map(p), "Cons FY0 rev 90d": S.rev_90d_fy0.map(P), "Rev breadth 30d": S.rev_breadth_30d.map(f2),
  "Core vs rep (FY)": S.core_vs_reported_FY.map(P), "KPI coverage": S.data_coverage.map(lambda x: f"{x*100:.0f}%")})
out.append(("M3_SCORE", s3.to_markdown()))
out.append(("M3_ROE12Q", S[["roe_last12q"]].rename(columns={"roe_last12q":"Core ROE TTM % (oldest -> latest, 12Q)"}).to_markdown()))
V = pd.read_csv("output/m4_valuation.csv", index_col=0)
v1 = pd.DataFrame({"P/B": V.pb.map(f2), "10y mean": V.pb_mean_10y.map(f2), "z(10y)": V.pb_z_10y.map(f2), "%ile 10y": V.pb_pctile_10y.map(lambda x: f"{x*100:.0f}"),
  "%ile 15y": V.pb_pctile_15y.map(lambda x: f"{x*100:.0f}"), "%ile 20y": V.pb_pctile_20y.map(lambda x: f"{x*100:.0f}"), "ROE 07-15": V.roe_avg_2007_15.map(p), "ROE 16-26": V.roe_avg_2016_26.map(p),
  "P/B 07-15": V.pb_avg_2007_15.map(f2), "P/B 16-26": V.pb_avg_2016_26.map(f2), "P/E core": V.pe_core.map(lambda x: f"{x:.1f}x"), "P/E z(10y)": V.pe_z_10y.map(f2),
  "DY": V.dy.map(p), "DY-MGS": V.dy_spread.map(lambda x: f"{x*100:+.2f}pp"), "spread %ile 20y": V.dy_spread_pctile.map(lambda x: f"{x*100:.0f}"), "spread %ile 10y": V.dy_spread_pctile_10y.map(lambda x: f"{x*100:.0f}")})
out.append(("M4_BANDS", v1.to_markdown()))
v2 = pd.DataFrame({"Core ROE": V.roe_core.map(p), "TS fair P/B (ROE)": V.pb_fair_ts_roe.map(f2), "Resid (SD)": V.resid_ts_roe_sd.map(f2), "R²": V.ts_r2.map(f2),
  "g": V.g.map(p), "β (Blume)": V.beta_blume.map(f2), "COE=MGS+β·6%": V.coe_fair.map(p), "Gordon P/B": V.pb_gordon.map(f2), "Actual/Gordon": (V.pb/V.pb_gordon-1).map(P),
  "Implied COE": V.coe_implied.map(p), "Implied ERP": V.erp_implied.map(p), "ERP %ile 20y": V.erp_implied_pctile.map(lambda x: f"{x*100:.0f}"), "ERP %ile 10y": V.erp_implied_pctile_10y.map(lambda x: f"{x*100:.0f}"),
  "ROE implied @fair COE": V.roe_implied_at_fair_coe.map(p), "XS fair P/B": V.xs_pb_fair.map(f2), "XS resid": V.xs_resid.map(lambda x: f"{x:+.2f}")})
out.append(("M4_REGR", v2.to_markdown()))
E = pd.read_csv("output/m5_episodes.csv")
e = pd.DataFrame({"Peak": pd.to_datetime(E.peak).dt.strftime("%d/%m/%Y"), "Trough": pd.to_datetime(E.trough).dt.strftime("%d/%m/%Y"), "Trigger": E.trigger, "Type": E.type,
  "Pk-Tr": E.peak_to_trough.map(P), "Days": E.days_to_trough, "P/B@tr": E.pb_trough.map(f2), "ROE@tr": E.roe_ttm_core_trough.map(p), "DY@tr": E.dy_trough.map(p), "MGS@tr": E.mgs10_trough.map(p),
  "EPS pk->tr": E.eps_chg_peak_to_trough.map(P), "EPS tr->+12m": E["eps_chg_trough_to_+12m"].map(P),
  "+3m": E.fwd3m_from_trough.map(P), "+6m": E.fwd6m_from_trough.map(P), "+12m": E.fwd12m_from_trough.map(P), "+36m": E.fwd36m_from_trough.map(P),
  "Hit -6.7% on": pd.to_datetime(E.first_hit_current_depth).dt.strftime("%d/%m/%Y"), "+12m from hit": E.fwd12m_from_hit.map(P), "+36m from hit": E.fwd36m_from_hit.map(P), "Further DD after hit": E.further_dd_after_hit.map(P)})
out.append(("M5_EPISODES", e.to_markdown(index=False)))
H = pd.read_csv("output/m5_similarity.csv")
h = pd.DataFrame({"Peak": pd.to_datetime(H.peak).dt.strftime("%d/%m/%Y"), "Trough": pd.to_datetime(H.trough).dt.strftime("%d/%m/%Y"), "Trigger": H.trigger, "DD": H.dd.map(P),
  "ROE vs 5y": H.roe_vs_5y.map(lambda x: f"{x*1e4:+.0f}bp"), "P/B vs 5y": H.pb_vs_5y.map(P), "EPS pk->tr": H.eps_chg.map(P), "ΔMGS": H.d_mgs.map(lambda x: f"{x:+.0f}bp"), "ΔUST": H.d_ust.map(lambda x: f"{x:+.0f}bp"),
  "Brent": H.brent.map(P), "EPS +12m": H.e12.map(P), "Fwd +12m": H.fwd12.map(P), "Fwd +36m": H.fwd36.map(P), "Distance": H.distance_to_now.map(f2)})
out.append(("M5_SIMILARITY", h.to_markdown(index=False)))
B = pd.read_csv("output/m5_base_rates.csv", index_col=0)
b = pd.DataFrame({"Current TR depth": B.depth.map(P), "n events": B.n, "Hit 12m": B.hit_rate_12m.map(lambda x: f"{x*100:.0f}%"), "Median 12m": B.median_12m.map(P), "Worst 12m": B.worst_12m.map(P),
  "Median 36m": B.median_36m.map(P), "Hit 36m": B.hit_rate_36m.map(lambda x: f"{x*100:.0f}%"), "Median further DD (12m)": B.median_max_further_dd.map(P), "Worst further DD": B.worst_max_further_dd.map(P)})
out.append(("M5_BASERATES", b.to_markdown()))
S6 = pd.read_csv("output/m6_scenarios.csv", index_col=0)
s6 = pd.DataFrame({"Prob B/Ba/Be": S6.prob, "Bull TR": S6.bull_tr.map(P), "Bull P/B": S6.bull_pb1.map(f2), "Base TR": S6.base_tr.map(P), "Bear TR": S6.bear_tr.map(P), "Bear P/B": S6.bear_pb1.map(f2), "Bear ROE": S6.bear_roe1.map(p),
  "E[TR] MYR": S6.exp_tr_myr.map(P), "E[TR] USD": S6.exp_tr_usd.map(P), "Up/Down": S6.up_down_ratio.map(f2), "Break-even P/B": S6.breakeven_pb.map(f2), "Div cover (bear)": S6.div_cover_bear.map(lambda x: f"{x:.2f}x"),
  "12m-fwd EPS (cons)": S6.eps_fwd_cons.map(lambda x: f"{x:.3f}"), "Base DPS": S6.base_dps.map(lambda x: f"{x:.3f}")})
out.append(("M6_SCEN", s6.to_markdown()))
T = pd.read_csv("output/m6_stress.csv", index_col=0)
t6 = pd.DataFrame({"Base EPS": T.base_eps.map(lambda x: f"{x:.3f}"), "Stress EPS": T.stress_eps.map(lambda x: f"{x:.3f}"), "EPS hit": T.eps_hit_pct.map(P), "Stress ROE": T.stress_roe.map(p),
  "PAT hit (RM b)": T.stress_pat_hit_rm_bn.map(lambda x: f"{x:.2f}"), "Div cover": T.div_cover_stress.map(lambda x: f"{x:.2f}x"), "DPS cut": T.dps_cut_pct.map(P),
  "CET1 now": T.cet1_now.map(lambda x: "n/a" if pd.isna(x) else f"{x:.2f}%"), "CET1 Δ (1y, bp)": T.cet1_hit_bp_1y.map(lambda x: f"{x:+.0f}")})
out.append(("M6_STRESS", t6.to_markdown()))
L = pd.read_csv("output/m7_levels.csv", index_col=0)
l = pd.DataFrame({"Px": L.px.map(f2), "BVPS": L.bv.map(f2), "@10y mean": L.px_at_mean.map(f2), "@-0.5SD": L["px_at_-0.5sd"].map(f2), "@-1SD": L["px_at_-1sd"].map(f2), "@-1.5SD": L["px_at_-1.5sd"].map(f2),
  "@ROE-fair": L.px_at_roe_fair.map(f2), "@Gordon": L.px_at_gordon.map(f2), "1y vol": L.vol_1y.map(p)})
out.append(("M7_LEVELS", l.to_markdown()))
C = pd.read_csv("output/core_adjustments.csv"); C = C[C.type != "cukai-makmur"]
out.append(("CORE_ADJ", C.round(2).to_markdown(index=False)))
with open("output/tables.md", "w") as fh:
    for k, v in out: fh.write(f"<!--{k}-->\n{v}\n\n")
print("ok", [k for k, _ in out])
