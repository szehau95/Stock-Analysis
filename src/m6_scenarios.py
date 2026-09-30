"""MODULE 6 — 12m forward scenario model per bank (Bull/Base/Bear + full stress).
DECLARED ASSUMPTIONS (tier: analyst assumption unless noted):
 - Loans = max(Yahoo net loans, 0.65 x total assets); HLB = RM226.3b reported (T1). IEA = 0.90 x TA. Fee income = 15% of total revenue.
 - RWA = 0.55 x TA (RWA density). Tax = Yahoo FY effective rate.
 - 12m-fwd EPS = FY-weighted consensus (Yahoo, T3) aligned to each FYE; DPS = TTM payout (bounded 30-90%) x fwd EPS.
 - Bull: EPS x1.03, P/B -> max(10y mean - 0.5SD, ROE-regression fair P/B). Base: EPS x0.98, P/B unchanged.
   Bear: +25bp credit cost, -5bp NIM, -5% fees; P/B -> midpoint of (10y mean - 1.5SD) and Gordon P/B at bear ROE (COE +50bp),
         capped at current P/B and floored at 85% of the bank's 20y minimum monthly P/B (a new low is allowed, but bounded).
   Stress (reported separately): +50bp credit cost, -10bp NIM, -10% fees.
 - FX (USD/MYR): bull MYR +3%, base 0%, bear MYR -5%.
"""
import pandas as pd, numpy as np, json
from common import *
PROBS = {  # bull, base, bear — rationale in report (Module 6)
 "MAYBANK": (.25,.50,.25), "PBBANK": (.25,.55,.20), "CIMB": (.20,.50,.30), "HLBANK": (.30,.50,.20), "RHBBANK": (.20,.50,.30),
 "AMBANK": (.20,.45,.35), "BIMB": (.20,.45,.35), "ALLIANCE": (.25,.50,.25), "AFFIN": (.15,.45,.40)}
FYE = {"HLBANK": (0.75, 0.25), "AMBANK": (0.5, 0.5), "ALLIANCE": (0.5, 0.5)}   # weights on (FY0, FY1) for Oct26-Sep27 window
CET1 = {"MAYBANK": 14.96, "PBBANK": 13.9, "CIMB": 14.0, "HLBANK": 12.9, "ALLIANCE": 12.4}
FX = {"bull": 0.03, "base": 0.0, "bear": -0.05}
def run():
    F = fin(); V = pd.read_csv("output/m4_valuation.csv", index_col=0); mg = mgs().iloc[-1]
    MS = pd.read_csv("output/m4_monthly_series.csv", header=[0,1], index_col=0, parse_dates=True)
    pb_floor = {b: MS[b]["pb"][MS.index >= ("2009-01-01" if b == "BIMB" else "2006-09-30")].clip(lower=0.05).min() for b in BANKS}
    rows, stress = [], []
    for b in BANKS:
        f = F[b]; v = V.loc[b]; d = panel(b).iloc[-1]
        P0, BV0, sh, TA, tax = d.Close, d.bv, f["shares"], f["total_assets"], f["tax_rate"] or 0.24
        loans = 226.3e9 if b == "HLBANK" else max(f["net_loans"], 0.65*TA); iea = 0.90*TA; fee = 0.15*f["total_rev"]; rwa = 0.55*TA
        w0, w1 = FYE.get(b, (0.25, 0.75)); eps_f = w0*f["eps_fy0"] + w1*f["eps_fy1"]
        payout = float(np.clip(d.dps_ttm/d.eps_ttm_core, 0.30, 0.90)); sd10 = v.pb_sd_10y; mean10 = v.pb_mean_10y
        def sens(cc_bp, nim_bp, fee_pct): return (cc_bp/1e4*loans + nim_bp/1e4*iea + fee_pct*fee) * (1 - tax) / sh
        out = dict(bank=b, P0=P0, BV0=BV0, eps_fwd_cons=eps_f, payout=payout, pb0=d.pb, roe0=d.roe_ttm_core,
                   loans_bn=loans/1e9, eps_hit_per_10bp_cc=sens(10,0,0), eps_hit_per_1bp_nim=sens(0,1,0))
        scen = {}
        for name in ("bull","base","bear"):
            if name == "bull": eps = eps_f*1.03
            elif name == "base": eps = eps_f*0.98
            else: eps = eps_f*0.98 - sens(25, 5, 0.05)
            dps = max(0.0, payout*eps) if name != "bear" else min(payout*eps_f*0.98, max(0.0, 0.9*eps))  # bear: DPS capped by 90% of bear EPS
            bv1 = BV0 + eps - dps; roe1 = eps / ((BV0 + bv1)/2)
            if name == "bull": pb1 = max(mean10 - 0.5*sd10, v.pb_fair_ts_roe)
            elif name == "base": pb1 = d.pb
            else:
                coe = v.coe_fair + 0.005; g = min(v.g, max(0.0, roe1 - 0.005))
                gordon = (roe1 - g)/(coe - g) if coe > g else np.nan
                band = mean10 - 1.5*sd10
                mid = np.nanmean([band, gordon]) if not np.isnan(gordon) else band
                pb1 = max(0.85*pb_floor[b], min(mid, d.pb))
                out["bear_gordon_pb"] = gordon; out["bear_band_pb"] = band; out["pb_floor_20y"] = pb_floor[b]
            P1 = pb1*bv1; tr = (P1 + dps)/P0 - 1; tr_usd = (1 + tr)*(1 + FX[name]) - 1
            scen[name] = dict(eps=eps, dps=dps, bv1=bv1, roe1=roe1, pb1=pb1, P1=P1, tr=tr, tr_usd=tr_usd)
            out.update({f"{name}_{k}": val for k, val in scen[name].items()})
        pb_, pbs, pbe = PROBS[b]
        out["prob"] = f"{int(pb_*100)}/{int(pbs*100)}/{int(pbe*100)}"
        out["exp_tr_myr"] = pb_*scen["bull"]["tr"] + pbs*scen["base"]["tr"] + pbe*scen["bear"]["tr"]
        out["exp_tr_usd"] = pb_*scen["bull"]["tr_usd"] + pbs*scen["base"]["tr_usd"] + pbe*scen["bear"]["tr_usd"]
        out["up_down_ratio"] = scen["bull"]["tr"] / abs(scen["bear"]["tr"]) if scen["bear"]["tr"] < 0 else np.inf
        out["breakeven_pb"] = (P0 - scen["base"]["dps"]) / scen["base"]["bv1"]
        out["div_cover_bear"] = scen["bear"]["eps"] / scen["base"]["dps"]
        rows.append(out)
        # full stress
        s_eps = eps_f*0.98 - sens(50, 10, 0.10); s_hit_pat = sens(50, 10, 0.10)*sh
        s = dict(bank=b, base_eps=eps_f*0.98, stress_eps=s_eps, eps_hit_pct=s_eps/(eps_f*0.98)-1,
                 stress_roe=s_eps/BV0, div_cover_stress=s_eps/scen["base"]["dps"], stress_pat_hit_rm_bn=s_hit_pat/1e9,
                 cet1_now=CET1.get(b, np.nan))
        base_div = payout*eps_f*0.98*sh; stress_div = min(base_div, max(0.0, 0.9*s_eps*sh))
        s["stress_dps"] = stress_div/sh; s["dps_cut_pct"] = stress_div/base_div - 1
        s["cet1_hit_bp_1y"] = -(s_hit_pat - (base_div - stress_div))/rwa*1e4
        if b == "MAYBANK":
            s["etiqa_deduction_bp"] = -4.83e9/rwa*1e4
            s["cet1_post_etiqa_est"] = CET1[b] + s["etiqa_deduction_bp"]/100
        stress.append(s)
    return pd.DataFrame(rows).set_index("bank"), pd.DataFrame(stress).set_index("bank")
if __name__ == "__main__":
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 60)
    S, T = run(); S.to_csv("output/m6_scenarios.csv"); T.to_csv("output/m6_stress.csv")
    print(S[["P0","pb0","roe0","eps_fwd_cons","loans_bn","eps_hit_per_10bp_cc","eps_hit_per_1bp_nim"]].round(3).to_string())
    for sc in ("bull","base","bear"):
        print(sc.upper()); print(S[[f"{sc}_{k}" for k in ("eps","dps","roe1","pb1","P1","tr","tr_usd")]].round(3).to_string())
    print(S[["bear_band_pb","bear_gordon_pb","pb_floor_20y","bear_pb1"]].round(3).to_string())
    print(S[["prob","exp_tr_myr","exp_tr_usd","up_down_ratio","breakeven_pb","div_cover_bear"]].round(3).to_string())
    print(T.round(3).to_string())
