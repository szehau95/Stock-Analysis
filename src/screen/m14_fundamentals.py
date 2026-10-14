"""Modules 1-4: freshness, fundamentals, valuation (justified P/B, regression, history, dividends, consensus), quality score."""
import numpy as np, pandas as pd, statsmodels.api as sm
from common import (CORE, CONTEXT, ASOF, MGS10, ERP, G, FY_END_NEXT, HLB_ASSOC, OUT, px, panel, quarterly, kpi, cons, pct_score)

K, C = kpi(), cons()
klci = px("KLCI").Close


def beta_blume(b):
    """3y weekly beta vs KLCI, Blume-adjusted (same build as the 30/09 run)."""
    w = pd.concat([px(b).Close.resample("W-FRI").last().pct_change(), klci.resample("W-FRI").last().pct_change()], axis=1).dropna()
    w = w[w.index > ASOF - pd.DateOffset(years=3)]
    raw = np.cov(w.iloc[:, 0], w.iloc[:, 1])[0, 1] / w.iloc[:, 1].var()
    return 0.67 * raw + 0.33, raw


def ntm_eps(b):
    c = C[b]
    w0 = max(0.0, (pd.Timestamp(FY_END_NEXT[b]) - ASOF).days / 365)
    return w0 * c["eps_fy0"] + (1 - w0) * c["eps_fy1"], w0


rows = []
for b in CORE + CONTEXT:
    p, d, q = px(b), panel(b), quarterly(b)
    last = d.iloc[-1]
    P = p.Close.iloc[-1]
    adv3m = (p.Close * p.Volume).iloc[-63:].mean() / 1e6
    q = q.sort_values("qdate")
    lq = q.iloc[-1]
    roe_lq_ann = lq.eps_core_sen_adj / 100 * 4 / ((lq.bv + q.iloc[-2].bv) / 2)
    roe_t4q_core = last.roe_ttm_core
    qa = q.reset_index(drop=True)
    roe_q = pd.Series([qa.eps_core_sen_adj[i] / 100 * 4 / ((qa.bv[i] + qa.bv[i - 1]) / 2) for i in range(len(qa) - 4, len(qa))])
    roe_slope_4q = np.polyfit(np.arange(4), roe_q.values, 1)[0]  # pp/quarter, last four quarterly annualised core ROEs
    bv, eps_t4q, dps_t4q = last.bv, last.eps_ttm_core, last.dps_ttm_q
    payout = dps_t4q / last.eps_ttm if last.eps_ttm > 0 else np.nan
    r = dict(bank=b, core=b in CORE, price=P, adv3m_rm_m=adv3m, mcap_rm_bn=P * C[b]["shares"] / 1e9,
             hi52=p.High.iloc[-252:].max(), lo52=p.Low.iloc[-252:].min(),
             qdate=last.qdate, announced=last.announced, bvps=bv, eps_t4q_core=eps_t4q, dps_t4q=dps_t4q, payout_t4q=payout,
             roe_t4q_core=roe_t4q_core, roe_t4q_headline=last.roe_ttm, roe_lq_ann=roe_lq_ann, roe_trend_4q=roe_slope_4q, roe_q_last4=roe_q.round(4).tolist())
    # 5y point-in-time P/B history (panel to 30/09, extended with new closes on the latest BV)
    hist = d.pb.dropna()
    ext = (p.Close[p.index > hist.index.max()] / bv)
    pb = pd.concat([hist, ext])
    pb5 = pb[pb.index > ASOF - pd.DateOffset(years=5)]
    r.update(pb=P / bv, pb5_mean=pb5.mean(), pb5_sd=pb5.std(), pb_z5=(P / bv - pb5.mean()) / pb5.std(),
             pb5_pctile=(pb5 < P / bv).mean())
    bB, braw = beta_blume(b)
    eps_ntm, w0 = ntm_eps(b)
    c = C[b]
    r.update(beta_raw=braw, beta_blume=bB, coe=MGS10 + bB * ERP, eps_ntm=eps_ntm, w_fy0=w0,
             pe_t4q=P / eps_t4q, pe_ntm=P / eps_ntm, ey_ntm=eps_ntm / P, dy_t4q=dps_t4q / P,
             dy_ntm=eps_ntm * payout / P, eps_rev_3m=c["eps_fy1"] / c["eps_fy1_90d"] - 1,
             tp_median=c.get("tp_median"), tp_mean=c.get("tp_mean"), n_analysts=c.get("n_fy1"),
             recs_buy=c["recs_0m"]["strongBuy"] + c["recs_0m"]["buy"], recs_hold=c["recs_0m"]["hold"],
             recs_sell=c["recs_0m"]["sell"] + c["recs_0m"]["strongSell"])
    rows.append(r)
F = pd.DataFrame(rows).set_index("bank")

# P/TBV from Yahoo quarterly balance sheet (T3)
import json
TRX = pd.read_csv(f"{OUT}/m2b_treasury.csv", index_col=0)
bs = json.load(open("data/raw/scr1410/yf_bs.json"))
F["tbvps"] = [bs[b]["Tangible Book Value"] / bs[b]["Ordinary Shares Number"] if b in bs else np.nan for b in F.index]
F["ptbv"] = F.price / F.tbvps

# HLBANK core basis: strip associates (mainly Bank of Chengdu) from earnings AND equity; value the stake at market.
h = HLB_ASSOC
avg_eq_ex = ((h["equity_now"] - h["carry_now"]) + (h["equity_4q_ago"] - h["carry_4q_ago"])) / 2
roe_ex = (h["pat_t4q"] - h["share_profit_t4q"]) / avg_eq_ex
bv_ex = (h["equity_now"] - h["carry_now"]) / h["shares"]
bocd_mv_ps = h["bocd_stake"] * h["bocd_px"] * h["bocd_shares"] * h["cnymyr"] / h["shares"]
bocd_carry_ps = h["carry_now"] / h["shares"]
F["roe_core_rank"] = F.roe_t4q_core
F["bv_core"] = F.bvps
F["addon_ps"] = 0.0
F.loc["HLBANK", ["roe_core_rank", "bv_core", "addon_ps"]] = [roe_ex, bv_ex, bocd_mv_ps]
# Treasury adjustment (Module 2b): June BV is pre-yield-spike; mark FVOCI to 13/10 (after tax) before any P/B or fair value.
TR = pd.read_csv(f"{OUT}/m2b_treasury.csv", index_col=0)
F["bv_fvoci_mark_ps"] = TR.bv_loss_now_ps.reindex(F.index).fillna(0.0)
F["bvps_unadj"] = F.bvps
F["bvps"] = F.bvps - F.bv_fvoci_mark_ps
F["bv_core"] = F.bv_core - F.bv_fvoci_mark_ps
F["pb"] = F.price / F.bvps
F["pb_core"] = (F.price - F.addon_ps) / F.bv_core
hlb_note = dict(roe_headline=h["pat_t4q"] / ((h["equity_now"] + h["equity_4q_ago"]) / 2), roe_ex_assoc=roe_ex, bv_ex_ps=bv_ex,
                bocd_mv_ps=bocd_mv_ps, bocd_carry_ps=bocd_carry_ps, assoc_share_of_pat=h["share_profit_t4q"] / h["pat_t4q"],
                bocd_mv_rm_bn=bocd_mv_ps * h["shares"] / 1e9)

# Module 3.1-3.2 justified P/B and mispricing (base g = 4%; sensitivity g 3%/5% and COE +/-50bp)
def jpb(roe, coe, g=G):
    return (roe - g) / (coe - g)


F["jpb"] = jpb(F.roe_core_rank, F.coe)
F["fair_value"] = F.jpb * F.bv_core + F.addon_ps
F["mispricing"] = F.fair_value / F.price - 1
for tag, kw in {"g3": dict(g=0.03), "g5": dict(g=0.05)}.items():
    F[f"fv_{tag}"] = jpb(F.roe_core_rank, F.coe, **kw) * F.bv_core + F.addon_ps
F["fv_coe_up"] = jpb(F.roe_core_rank, F.coe + 0.005) * F.bv_core + F.addon_ps
F["fv_coe_dn"] = jpb(F.roe_core_rank, F.coe - 0.005) * F.bv_core + F.addon_ps
F["coe_beta1"] = MGS10 + ERP
F["mispricing_beta1"] = (jpb(F.roe_core_rank, F.coe_beta1) * F.bv_core + F.addon_ps) / F.price - 1
F["mispricing_g3"] = F.fv_g3 / F.price - 1
F["mispricing_g5"] = F.fv_g5 / F.price - 1
roe_lq = F.roe_lq_ann.where(F.index != "HLBANK", F.roe_core_rank)  # HLB: no quarterly ex-associate split; keep T4Q ex-assoc
F["mispricing_lq"] = (jpb(roe_lq, F.coe) * F.bv_core + F.addon_ps) / F.price - 1
F["mispricing_lq_beta1"] = (jpb(roe_lq, F.coe_beta1) * F.bv_core + F.addon_ps) / F.price - 1
F["fv_hlb_bocd_at_carry"] = np.where(F.index == "HLBANK", F.jpb * F.bv_core + bocd_carry_ps, np.nan)
F["implied_coe"] = G + (F.roe_core_rank - G) / F.pb_core  # COE that justifies today's core P/B at g
F["implied_erp"] = (F.implied_coe - MGS10) / F.beta_blume

# Module 3.3 cross-sectional P/B vs core ROE (9 listed banks; HLB on ex-associate basis)
X = sm.add_constant(F.roe_core_rank)
ols9 = sm.OLS(F.pb_core, X).fit()
F["pb_fit"] = ols9.predict(X)
F["resid_pb"] = F.pb_core - F.pb_fit
F["resid_pct"] = F.pb_core / F.pb_fit - 1
core_mask = F.core
ols6 = sm.OLS(F.loc[core_mask, "pb_core"], sm.add_constant(F.loc[core_mask, "roe_core_rank"])).fit()
reg = dict(n9=int(ols9.nobs), a9=ols9.params.iloc[0], b9=ols9.params.iloc[1], r2_9=ols9.rsquared, se_b9=ols9.bse.iloc[1],
           n6=int(ols6.nobs), a6=ols6.params.iloc[0], b6=ols6.params.iloc[1], r2_6=ols6.rsquared)
F["resid_pct_core6fit"] = np.nan
F.loc[core_mask, "resid_pct_core6fit"] = F.loc[core_mask, "pb_core"] / ols6.predict(sm.add_constant(F.loc[core_mask, "roe_core_rank"])) - 1

# Module 3.5 dividend support
F["dy_spread_mgs"] = F.dy_ntm - MGS10
F["fv_vs_cons"] = F.fair_value / F.tp_median - 1

# Module 2/4 KPI merge (core six only)
Q = F.loc[CORE].copy()
for col in ["nim_pct", "nim_yoy_bps", "casa_pct", "cir_pct", "gil_pct", "llc_pct", "credit_cost_bps", "cet1_pct", "tcr_pct",
            "lcr_pct", "loan_growth_yoy_pct", "roe_reported_pct", "opr_sens_bps_per25", "guidance_status", "events", "tier"]:
    Q[col] = K.loc[CORE, col]
num = ["nim_pct", "casa_pct", "cir_pct", "gil_pct", "llc_pct", "credit_cost_bps", "cet1_pct", "tcr_pct", "lcr_pct", "loan_growth_yoy_pct"]
Q[num] = Q[num].apply(pd.to_numeric, errors="coerce")
# CET1 for the buffer: reported, less the FVOCI mark to 13/10 (Module 2b); MAYBANK also pro forma for the RM4.83b Etiqa
# buyout on T1 group RWA RM440.5b (-1.10pp; the 30/09 run used an RWA proxy of ~RM580b and understated it at -0.83pp).
Q["rwa_t1_rm_bn"] = TRX.rwa
Q["cet1_treasury_hit_pp"] = TRX.cet1_hit_now_bp / 100
Q["cet1_for_buffer"] = Q.cet1_pct - Q.cet1_treasury_hit_pp
Q.loc["MAYBANK", "cet1_for_buffer"] -= 4.83 / Q.loc["MAYBANK", "rwa_t1_rm_bn"] * 100
Q["cet1_buffer_pp"] = Q.cet1_for_buffer - 13.0
Q["excess_cet1_rm_bn_est"] = Q.cet1_buffer_pp / 100 * Q.rwa_t1_rm_bn
Q["rate_risk_cet1_bp_100"] = TRX.cet1_hit_stress_bp
Q["rate_risk_bv_pct_100"] = TRX.bv_loss_stress_pct_equity
Q["payout_flag"] = np.select([Q.cet1_buffer_pp < 0, (Q.cet1_buffer_pp < 0.5) & (Q.payout_t4q > 0.6)],
                             ["WATCH: CET1 below 13% ref", "WATCH: thin buffer, high payout"], "ok")

# Module 4 quality score (percentile within core six; UNVERIFIED -> 50)
QS = pd.DataFrame(index=Q.index)
QS["roe_level"] = pct_score(Q.roe_core_rank)
QS["roe_trend"] = pct_score(Q.roe_trend_4q)
QS["casa"] = pct_score(Q.casa_pct)
QS["cir"] = pct_score(Q.cir_pct, higher_better=False)
QS["gil"] = pct_score(Q.gil_pct, higher_better=False)
QS["llc"] = pct_score(Q.llc_pct)
QS["cet1_buffer"] = pct_score(Q.cet1_buffer_pp)
QS["rate_risk"] = pct_score(Q.rate_risk_cet1_bp_100, higher_better=False)
W10 = dict(roe_level=.30, roe_trend=.10, casa=.15, cir=.10, gil=.15, llc=.10, cet1_buffer=.10)
W = {**{k: 0.9 * v for k, v in W10.items()}, "rate_risk": 0.10}  # v1.1: securities-book rate risk added at 10%
QS["quality_score_w10"] = sum(QS[k] * w for k, w in W10.items())
QS["quality_score"] = sum(QS[k] * w for k, w in W.items())

F.to_csv(f"{OUT}/m14_fundamentals_all9.csv")
Q.join(QS).to_csv(f"{OUT}/m24_core6.csv")
pd.Series({**reg, **hlb_note}).to_csv(f"{OUT}/m3_regression_hlb.csv")

pd.set_option("display.width", 250, "display.max_columns", 40)
print("REGRESSION", {k: round(v, 3) for k, v in reg.items()})
print("HLB", {k: round(v, 4) for k, v in hlb_note.items()})
print(F[["price", "bvps", "pb", "pb_core", "roe_t4q_core", "roe_core_rank", "roe_lq_ann", "roe_trend_4q", "beta_blume", "coe", "jpb",
         "fair_value", "mispricing", "resid_pct", "pb_z5", "pe_t4q", "pe_ntm", "dy_ntm", "eps_rev_3m", "tp_median", "fv_vs_cons", "adv3m_rm_m"]].round(3).to_string())
print(Q[["casa_pct", "cir_pct", "gil_pct", "llc_pct", "cet1_pct", "cet1_treasury_hit_pp", "cet1_for_buffer", "cet1_buffer_pp", "excess_cet1_rm_bn_est", "rate_risk_cet1_bp_100", "payout_t4q", "payout_flag"]].round(3).to_string())
print(QS.round(1).to_string())
