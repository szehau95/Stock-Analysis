"""MODULE 7 support: P/B-band price references, board-lot sizing vs cash buffer, indicative ELN downside, composite metrics."""
import pandas as pd, numpy as np
from scipy.stats import norm
from common import *
V = pd.read_csv("output/m4_valuation.csv", index_col=0); S = pd.read_csv("output/m6_scenarios.csv", index_col=0)
rows = []
for b in BANKS:
    d = panel(b); bv = d.bv.iloc[-1]; v = V.loc[b]
    r = dict(bank=b, px=d.Close.iloc[-1], bv=bv, pb=d.pb.iloc[-1])
    for k, m in {"mean":0, "-0.5sd":-0.5, "-1sd":-1, "-1.5sd":-1.5}.items(): r[f"px_at_{k}"] = bv*(v.pb_mean_10y + m*v.pb_sd_10y)
    r["px_at_roe_fair"] = bv*v.pb_fair_ts_roe; r["px_at_gordon"] = bv*v.pb_gordon
    rv = np.log(d.Close/d.Close.shift(1)).dropna()[-252:].std()*np.sqrt(252); r["vol_1y"] = rv
    rows.append(r)
L = pd.DataFrame(rows).set_index("bank"); L.to_csv("output/m7_levels.csv")
pd.set_option("display.width", 220); print(L.round(2).to_string())
# composite
w = mcap_weights(); print("weights", w.round(3).to_dict())
for c in ["pb","roe_core","dy","pe_core","dy_spread","erp_implied","erp_implied_pctile_10y","pb_pctile_10y","dy_spread_pctile_10y","resid_ts_roe_sd"]:
    print(c, round((V[c]*w).sum(), 4))
print("composite exp_tr_myr", round((S.exp_tr_myr*w).sum(),4), "exp_tr_usd", round((S.exp_tr_usd*w).sum(),4), "bull", round((S.bull_tr*w).sum(),4), "base", round((S.base_tr*w).sum(),4), "bear", round((S.bear_tr*w).sum(),4))
# Indicative 6m ELN on MAYBANK: investor sells put at strike K=92% (European, BS), coupon = put premium / K annualised
for b in ["MAYBANK","PBBANK","HLBANK"]:
    P = L.loc[b,"px"]; K = 0.92*P; T = 0.5; r_ = 0.0275; q = V.loc[b,"dy"]; sig = max(L.loc[b,"vol_1y"], 0.15)
    d1 = (np.log(P/K) + (r_ - q + 0.5*sig**2)*T)/(sig*np.sqrt(T)); d2 = d1 - sig*np.sqrt(T)
    put = K*np.exp(-r_*T)*norm.cdf(-d2) - P*np.exp(-q*T)*norm.cdf(-d1)
    cpn_pa = (put/K)/T + r_   # indicative gross coupon incl. funding, before issuer margin
    bear_px = S.loc[b,"bear_P1"]; stress_mid = P*0.80
    for lbl, PT in {"bear 12m px": bear_px, "-20% at maturity": stress_mid}.items():
        loss = (min(PT, K) / K - 1) + cpn_pa*T if PT < K else cpn_pa*T
        print(f"ELN {b}: px {P:.2f} strike {K:.2f} vol {sig:.3f} put {put:.3f} indicative coupon {cpn_pa*100:.1f}% p.a.; scenario {lbl} {PT:.2f} -> 6m P&L on notional {loss*100:.1f}% (shares delivered at {K:.2f})")
# sizing vs cash buffer (IBKR snapshot 30/09/2026, USD)
nlv, cash, fx = 43372.31, 3852.25, px("USDMYR").Close.iloc[-1]
for floor in (0.06, 0.08):
    dep = max(0, cash - floor*nlv); print(f"cash floor {floor:.0%}: deployable USD {dep:,.0f} = RM {dep*fx:,.0f}")
for b in ["HLBANK","PBBANK","MAYBANK","ALLIANCE"]:
    p = L.loc[b,"px"]; print(b, "board lot (100 sh) RM", round(100*p,0), "USD", round(100*p/fx,0), "= % NLV", round(100*p/fx/nlv*100,2))
