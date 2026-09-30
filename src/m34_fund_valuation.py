"""MODULE 3 (fundamentals scorecard) + MODULE 4 (historical valuation framework).
Assumptions (declared, adjustable):"""
ERP = 0.060          # Malaysia equity risk premium used for 'fair' COE (MGS10Y + beta*ERP); sensitivity 5-7%
G_FLOOR, G_CAP = 0.02, 0.05   # sustainable growth g = core ROE x (1 - payout), bounded
WEIGHTS = {  # Module 3 scorecard weights (sum = 1.0)
 "roe_core": .20, "roe_trend": .10, "eps_growth": .10, "revisions": .10, "nim_trend": .10,
 "asset_quality": .10, "credit_cost": .05, "cet1": .10, "cir": .05, "div_sustain": .10}
import pandas as pd, numpy as np
import statsmodels.api as sm
from common import *

def quarterly(b):
    q = pd.read_csv(f"data/clean/quarterly_adj_{b}.csv", parse_dates=["qdate","announced"])
    return q

def monthly_panel(b):
    d = panel(b)
    m = d.resample("ME").last()
    mg = mgs(); m["mgs10"] = mg.reindex(m.index, method="nearest", tolerance=pd.Timedelta(days=5))
    return m

def beta_weekly(b, years=3):
    d = panel(b).tr_idx.resample("W-FRI").last().pct_change()
    k = px("KLCI").Close.resample("W-FRI").last().pct_change()
    x = pd.concat([d, k], axis=1).dropna().iloc[-52*years:]
    b_ = np.polyfit(x.iloc[:,1], x.iloc[:,0], 1)[0]
    return b_, 0.67*b_ + 0.33   # raw, Blume-adjusted

def m3_scorecard():
    F = fin(); K = pd.read_csv("data/clean/kpi_latest.csv").set_index("bank")
    rows = []
    for b in BANKS:
        q = quarterly(b); q10 = q[q.qdate >= q.qdate.max() - pd.DateOffset(years=10)]
        last = q.iloc[-1]; r = dict(bank=b, qdate=last.qdate.date())
        # core vs reported (Yahoo FY normalized vs reported, tier 3)
        gap = F[b]["ni_norm"]/F[b]["ni"] - 1 if F[b].get("ni_norm") else np.nan
        r["core_vs_reported_FY"] = gap
        haircut = (1 + gap) if (abs(gap) > 0.03 and gap < 0) else 1.0   # rule: use core where it differs >3% (downside only)
        r["roe_core"] = last.roe_ttm_core * haircut
        roe_hist = q10.roe_ttm_core.dropna()
        r["roe_core_z10y"] = (r["roe_core"] - roe_hist.mean()) / roe_hist.std()
        r["roe_core_10y_avg"] = roe_hist.mean()
        r["roe_trend_4q"] = q.roe_ttm_core.iloc[-1] - q.roe_ttm_core.iloc[-5]
        r["roe_last12q"] = " ".join(f"{x*100:.1f}" for x in q.roe_ttm_core.iloc[-12:])
        r["eps_ttm_core"] = last.eps_ttm_core
        r["eps_growth_yoy"] = last.eps_ttm_core / q.eps_ttm_core.iloc[-5] - 1
        r["eps_growth_z10y"] = (r["eps_growth_yoy"] - (q10.eps_ttm_core/q10.eps_ttm_core.shift(4)-1).mean()) / (q10.eps_ttm_core/q10.eps_ttm_core.shift(4)-1).std()
        r["bv_growth_yoy"] = last.bv / q.bv.iloc[-5] - 1
        dps = panel(b).dps_ttm.iloc[-1]; r["dps_ttm"] = dps; r["payout_ttm"] = dps / last.eps_ttm_core
        r["dy"] = dps / panel(b).Close.iloc[-1]
        f = F[b]; r["cons_eps_fy0"] = f.get("eps_fy0"); r["cons_eps_fy1"] = f.get("eps_fy1")
        r["rev_90d_fy0"] = f["eps_fy0"]/f["eps_fy0_90d"]-1; r["rev_90d_fy1"] = f["eps_fy1"]/f["eps_fy1_90d"]-1
        r["rev_breadth_30d"] = (f["rev_up30_fy0"]+f["rev_up30_fy1"]-f["rev_dn30_fy0"]-f["rev_dn30_fy1"]) / max(1, 2*f["n_analysts"])
        r["n_analysts"] = f["n_analysts"]; r["tp_mean"] = f.get("tp_mean")
        for k in ["nim_pct","nim_yoy_bps","casa_pct","cir_pct","credit_cost_bps","gil_pct","llc_pct","cet1_pct","loan_growth_pct","profit_yoy_pct"]:
            r[k] = K.loc[b, k] if b in K.index else np.nan
        rows.append(r)
    S = pd.DataFrame(rows).set_index("bank")
    # scoring: percentile rank across universe; missing -> 0.5 (neutral); direction-adjusted
    def pr(s, higher_better=True):
        x = s.rank(pct=True) if higher_better else (-s).rank(pct=True)
        return x.fillna(0.5)
    sc = pd.DataFrame(index=S.index)
    sc["roe_core"] = pr(S.roe_core); sc["roe_trend"] = pr(S.roe_trend_4q); sc["eps_growth"] = pr(S.eps_growth_yoy)
    sc["revisions"] = pr(S.rev_90d_fy0*0.5 + S.rev_breadth_30d*0.05)
    sc["nim_trend"] = pr(S.nim_yoy_bps)
    sc["asset_quality"] = (pr(S.gil_pct, False) + pr(S.llc_pct)) / 2
    sc["credit_cost"] = pr(S.credit_cost_bps, False); sc["cet1"] = pr(S.cet1_pct); sc["cir"] = pr(S.cir_pct, False)
    sc["div_sustain"] = pr(-(S.payout_ttm - 0.55).abs())   # closest to ~55% payout = most sustainable
    S["score"] = sum(sc[k]*w for k, w in WEIGHTS.items()); S["rank"] = S.score.rank(ascending=False).astype(int)
    S["data_coverage"] = S[["nim_yoy_bps","gil_pct","llc_pct","credit_cost_bps","cet1_pct","cir_pct"]].notna().mean(axis=1)
    return S.sort_values("score", ascending=False), sc

def m4_valuation():
    out, series = [], {}
    mg_now = mgs().iloc[-1]
    for b in BANKS:
        m = monthly_panel(b); start = "2009-01-01" if b == "BIMB" else "2006-09-30"
        m = m[m.index >= start].dropna(subset=["pb"])
        cur = panel(b).iloc[-1]; q = quarterly(b)
        r = dict(bank=b, pb=cur.pb, roe_core=cur.roe_ttm_core, pe_core=cur.pe_core, dy=cur.dy, mgs10=mg_now)
        for yrs in (10, 15, 20):
            w = m[m.index >= ASOF - pd.DateOffset(years=yrs)].pb
            r[f"pb_mean_{yrs}y"] = w.mean(); r[f"pb_sd_{yrs}y"] = w.std()
            r[f"pb_z_{yrs}y"] = (cur.pb - w.mean())/w.std(); r[f"pb_pctile_{yrs}y"] = (w < cur.pb).mean()
        w10 = m[m.index >= ASOF - pd.DateOffset(years=10)]
        pe = w10.pe_core.replace([np.inf,-np.inf], np.nan); pe = pe[(pe > 0) & (pe < 40)]
        r["pe_mean_10y"] = pe.mean(); r["pe_z_10y"] = (cur.pe_core - pe.mean())/pe.std(); r["pe_pctile_10y"] = (pe < cur.pe_core).mean()
        # dividend-yield spread vs MGS10Y
        m["dy_spread"] = m.dy - m.mgs10
        ds = m.dy_spread.dropna(); r["dy_spread"] = cur.dy - mg_now
        r["dy_spread_mean_20y"] = ds.mean(); r["dy_spread_z"] = (r["dy_spread"] - ds.mean())/ds.std(); r["dy_spread_pctile"] = (ds < r["dy_spread"]).mean()
        ds10 = ds[ds.index >= ASOF - pd.DateOffset(years=10)]; r["dy_spread_pctile_10y"] = (ds10 < r["dy_spread"]).mean()
        # P/B vs ROE time-series regression (monthly, core ROE) ; + MGS10Y
        x = m[["pb","roe_ttm_core","mgs10"]].dropna(); x = x[(x.roe_ttm_core > 0) & (x.roe_ttm_core < 0.35)]
        X1 = sm.add_constant(x[["roe_ttm_core"]]); f1 = sm.OLS(x.pb, X1).fit()
        pred1 = f1.params["const"] + f1.params["roe_ttm_core"]*r["roe_core"]
        r["ts_slope_roe"] = f1.params["roe_ttm_core"]; r["ts_r2"] = f1.rsquared
        r["pb_fair_ts_roe"] = pred1; r["resid_ts_roe_sd"] = (cur.pb - pred1)/np.sqrt(f1.mse_resid)
        X2 = sm.add_constant(x[["roe_ttm_core","mgs10"]]); f2 = sm.OLS(x.pb, X2).fit()
        pred2 = f2.params["const"] + f2.params["roe_ttm_core"]*r["roe_core"] + f2.params["mgs10"]*mg_now
        r["pb_fair_ts_roe_mgs"] = pred2; r["resid_ts_roe_mgs_sd"] = (cur.pb - pred2)/np.sqrt(f2.mse_resid)
        r["ts_r2_roe_mgs"] = f2.rsquared; r["mgs_coef"] = f2.params["mgs10"]
        # Gordon: g = ROE*(1-payout) bounded; beta (Blume) ; fair COE ; implied COE ; implied ERP history
        payout = min(0.9, max(0.3, cur.dps_ttm / cur.eps_ttm_core)) if cur.eps_ttm_core > 0 else 0.5
        g = min(G_CAP, max(G_FLOOR, r["roe_core"]*(1-payout)))
        braw, bblume = beta_weekly(b)
        coe = mg_now + bblume*ERP
        r.update(payout=payout, g=g, beta_raw=braw, beta_blume=bblume, coe_fair=coe)
        r["pb_gordon"] = (r["roe_core"] - g)/(coe - g)
        r["coe_implied"] = g + (r["roe_core"] - g)/cur.pb
        r["erp_implied"] = (r["coe_implied"] - mg_now)/bblume
        r["roe_implied_at_fair_coe"] = g + cur.pb*(coe - g)
        # implied ERP history (monthly), using contemporaneous core ROE, payout (bounded) and MGS; beta held at current
        pay_h = (m.dps_ttm/m.eps_ttm_core).clip(0.3, 0.9).fillna(0.5)
        g_h = (m.roe_ttm_core*(1-pay_h)).clip(G_FLOOR, G_CAP)
        m["coe_implied"] = g_h + (m.roe_ttm_core - g_h)/m.pb
        m["erp_implied"] = (m.coe_implied - m.mgs10)/bblume
        e = m.erp_implied.dropna(); e = e[(e > -0.05) & (e < 0.25)]
        r["erp_implied_mean_20y"] = e.mean(); r["erp_implied_pctile"] = (e < r["erp_implied"]).mean()
        e10 = e[e.index >= ASOF - pd.DateOffset(years=10)]; r["erp_implied_pctile_10y"] = (e10 < r["erp_implied"]).mean(); r["erp_implied_mean_10y"] = e10.mean()
        # ROE regime: 10y avg vs pre-2016 avg (structural reset test)
        rr = m.roe_ttm_core
        r["roe_avg_2007_15"] = rr["2007":"2015"].mean(); r["roe_avg_2016_26"] = rr["2016":].mean()
        r["pb_avg_2007_15"] = m.pb["2007":"2015"].mean(); r["pb_avg_2016_26"] = m.pb["2016":].mean()
        series[b] = m
        out.append(r)
    V = pd.DataFrame(out).set_index("bank")
    # cross-sectional P/B vs core ROE today
    X = sm.add_constant(V[["roe_core"]]); f = sm.OLS(V.pb, X).fit()
    V["xs_pb_fair"] = f.predict(X); V["xs_resid"] = V.pb - V.xs_pb_fair
    V.attrs["xs"] = dict(const=f.params["const"], slope=f.params["roe_core"], r2=f.rsquared)
    return V, series

if __name__ == "__main__":
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 60)
    S, sc = m3_scorecard(); S.to_csv("output/m3_scorecard.csv"); sc.to_csv("output/m3_subscores.csv")
    print(S[["score","rank","roe_core","roe_core_10y_avg","roe_core_z10y","roe_trend_4q","eps_growth_yoy","rev_90d_fy0","rev_90d_fy1","rev_breadth_30d","dy","payout_ttm","core_vs_reported_FY","data_coverage"]].round(3).to_string())
    print(S[["roe_last12q"]].to_string())
    V, series = m4_valuation(); V.to_csv("output/m4_valuation.csv")
    pd.concat({b: s[["pb","roe_ttm_core","pe_core","dy","mgs10","dy_spread","coe_implied","erp_implied"]] for b, s in series.items()}, axis=1).to_csv("output/m4_monthly_series.csv")
    print(V[["pb","pb_mean_10y","pb_z_10y","pb_pctile_10y","pb_pctile_20y","pe_core","pe_z_10y","dy","dy_spread","dy_spread_z","dy_spread_pctile"]].round(3).to_string())
    print(V[["roe_core","pb_fair_ts_roe","resid_ts_roe_sd","ts_r2","pb_fair_ts_roe_mgs","resid_ts_roe_mgs_sd","ts_r2_roe_mgs","mgs_coef"]].round(3).to_string())
    print(V[["g","beta_blume","coe_fair","pb_gordon","coe_implied","erp_implied","erp_implied_mean_20y","erp_implied_pctile","erp_implied_pctile_10y","roe_implied_at_fair_coe","xs_pb_fair","xs_resid"]].round(3).to_string())
    print(V[["roe_avg_2007_15","roe_avg_2016_26","pb_avg_2007_15","pb_avg_2016_26"]].round(3).to_string())
    print("XS regression:", V.attrs["xs"])
