"""Yahoo FY financials + consensus snapshot (tier-3, lead-gen/cross-check; sensitivities only)."""
import yfinance as yf, pandas as pd, json
T = {"MAYBANK":"1155.KL","PBBANK":"1295.KL","CIMB":"1023.KL","HLBANK":"5819.KL","RHBBANK":"1066.KL","AMBANK":"1015.KL","BIMB":"5258.KL","ALLIANCE":"2488.KL","AFFIN":"5185.KL"}
out = {}
def g(df, k, i=0):
    try: return float(df.loc[k].iloc[i])
    except Exception: return None
for b, t in T.items():
    tk = yf.Ticker(t); bs, inc, info = tk.balance_sheet, tk.income_stmt, tk.info
    r = dict(fy=str(bs.columns[0].date()) if len(bs.columns) else None,
             net_loans=g(bs,"Net Loan"), total_assets=g(bs,"Total Assets"), equity=g(bs,"Stockholders Equity"),
             nii=g(inc,"Net Interest Income"), total_rev=g(inc,"Total Revenue"), pbt=g(inc,"Pretax Income"),
             tax_rate=g(inc,"Tax Rate For Calcs"), ni=g(inc,"Net Income Common Stockholders"), ni_norm=g(inc,"Normalized Income"),
             unusual=g(inc,"Total Unusual Items"), ni_prev=g(inc,"Net Income Common Stockholders",1),
             shares=info.get("sharesOutstanding"), mcap=info.get("marketCap"), beta_yf=info.get("beta"))
    try:
        et = tk.eps_trend; er = tk.eps_revisions; ee = tk.earnings_estimate
        r.update(eps_fy0=float(et.loc["0y","current"]), eps_fy0_90d=float(et.loc["0y","90daysAgo"]), eps_fy0_30d=float(et.loc["0y","30daysAgo"]),
                 eps_fy1=float(et.loc["+1y","current"]), eps_fy1_90d=float(et.loc["+1y","90daysAgo"]),
                 rev_up30_fy0=int(er.loc["0y","upLast30days"]), rev_dn30_fy0=int(er.loc["0y","downLast30days"]),
                 rev_up30_fy1=int(er.loc["+1y","upLast30days"]), rev_dn30_fy1=int(er.loc["+1y","downLast30days"]),
                 n_analysts=int(ee.loc["0y","numberOfAnalysts"]))
    except Exception as e: r["cons_err"] = str(e)[:80]
    try: r.update({"tp_"+k: v for k, v in tk.analyst_price_targets.items()})
    except Exception: pass
    try:
        rec = tk.recommendations; r["recs_0m"] = rec.iloc[0][["strongBuy","buy","hold","sell","strongSell"]].astype(int).to_dict()
    except Exception: pass
    out[b] = r
    print(b, {k: (round(v,4) if isinstance(v,float) else v) for k, v in r.items()})
json.dump(out, open("data/clean/yf_fin_consensus.json","w"), indent=1, default=str)
