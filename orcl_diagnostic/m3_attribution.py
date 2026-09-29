"""Module 3 - return attribution for ORCL. All arithmetic here, none in context."""
import pandas as pd, numpy as np
df = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
px = df[["ORCL","^NDX","^GSPC","MSFT","AMZN","GOOGL","CRWV","NVDA","AVGO","SMH","IGV"]].dropna(subset=["ORCL","^NDX"])
lr = np.log(px).diff()
# Baskets (equal-weight daily log-ret mean)
lr["AI_INFRA"] = lr[["CRWV","NVDA","AVGO","SMH"]].mean(axis=1, skipna=True)      # compute/neocloud/semis
lr["HYPERSCALER"] = lr[["MSFT","AMZN","GOOGL"]].mean(axis=1)
lr["PEER_ALL"] = lr[["MSFT","AMZN","GOOGL","CRWV","NVDA","AVGO","SMH","IGV"]].mean(axis=1, skipna=True)

def ols(y, X):
    X = np.column_stack([np.ones(len(X)), X]); b, *_ = np.linalg.lstsq(X, y, rcond=None); return b

def decompose(start, end, label, beta_window="in", ai_col="AI_INFRA"):
    w = lr.loc[start:end].iloc[1:].dropna(subset=["ORCL","^NDX",ai_col,"IGV"])  # returns after start close
    est = w if beta_window=="in" else lr.loc[:start].iloc[-251:-1].dropna(subset=["ORCL","^NDX",ai_col,"IGV"])
    # step1: sector factors orthogonalised to NDX (estimated on same est window)
    def orth(col):
        a,b = ols(est[col].values, est["^NDX"].values)
        # remove only the market-beta component; keep the sector's own drift so it can explain the move
        return w[col] - b*w["^NDX"], est[col] - b*est["^NDX"]
    ai_w, ai_e = orth(ai_col); sw_w, sw_e = orth("IGV")
    a, bm, bai, bsw = ols(est["ORCL"].values, np.column_stack([est["^NDX"], ai_e, sw_e]))
    mkt = bm*w["^NDX"].sum(); ai = bai*ai_w.sum(); sw = bsw*sw_w.sum()
    tot = w["ORCL"].sum(); idio = tot - mkt - ai - sw
    r2 = 1 - np.var(est["ORCL"] - (a + bm*est["^NDX"] + bai*ai_e + bsw*sw_e))/np.var(est["ORCL"])
    out = pd.Series({"total_logret":tot, "market(NDX)":mkt, "AI-infra (ex-mkt)":ai, "software IGV (ex-mkt)":sw, "idiosyncratic":idio})
    pct = (out/tot*100).round(0)
    print(f"\n=== {label} [sector={ai_col}]: {w.index[0].date()}..{w.index[-1].date()}  betas[{beta_window}] NDX={bm:.2f} AI={bai:.2f} IGV={bsw:.2f} R2={r2:.2f}")
    print(f"simple return ORCL {np.expm1(tot)*100:.1f}%  NDX {np.expm1(w['^NDX'].sum())*100:.1f}%  AI_INFRA {np.expm1(w['AI_INFRA'].sum())*100:.1f}%  IGV {np.expm1(w['IGV'].sum())*100:.1f}%  HYPERSCALER {np.expm1(w['HYPERSCALER'].sum())*100:.1f}%")
    print(pd.DataFrame({"logret":out.round(4), "% of move":pct}).to_string())
    # daily residual for worst days
    resid = w["ORCL"] - (bm*w["^NDX"] + bai*ai_w + bsw*sw_w)
    return w, resid

res = {}
for (s,e,l) in [("2025-09-10","2026-09-28","A. Full drawdown from peak"),
                ("2026-06-01","2026-09-28","B. Since Jun-1 local high"),
                ("2026-09-08","2026-09-28","C. Recent leg from Sep-8 high"),
                ("2026-09-10","2026-09-28","D. Since Q1 FY27 release day")]:
    for bw in (["in","pre"] if l[0] in "AC" else ["in"]):
        w, r = decompose(s,e,l,bw)
        res[(l,bw)] = (w,r)
    if l[0] in "AC":
        decompose(s,e,l,"in",ai_col="CRWV")

# worst days
for key in [("A. Full drawdown from peak","in"),("C. Recent leg from Sep-8 high","in")]:
    w, r = res[key]
    t = pd.DataFrame({"ORCL%":np.expm1(w["ORCL"])*100,"NDX%":np.expm1(w["^NDX"])*100,"AI_INFRA%":np.expm1(w["AI_INFRA"])*100,
                      "HYPER%":np.expm1(w["HYPERSCALER"])*100,"IGV%":np.expm1(w["IGV"])*100,"resid%":r*100}).round(2)
    print(f"\nTop 5 worst days - {key[0]}"); print(t.nsmallest(5,"ORCL%").to_string())

# Rolling 20D correlation to AI_INFRA and to NDX
rc = pd.DataFrame({"corr_AI":lr["ORCL"].rolling(20).corr(lr["AI_INFRA"]),"corr_NDX":lr["ORCL"].rolling(20).corr(lr["^NDX"]),
                   "corr_CRWV":lr["ORCL"].rolling(20).corr(lr["CRWV"])})
print("\nRolling 20D correlation (month-end samples + latest):")
print(rc.resample("ME").last().loc["2025-09":].round(2).to_string()); print("latest", rc.iloc[-1].round(2).to_dict())
rc.to_csv("data/rolling_corr.csv")
# Realized vol
print("\n20D realized vol ann.: ORCL %.1f%%  60D %.1f%%" % (lr["ORCL"].iloc[-20:].std()*np.sqrt(252)*100, lr["ORCL"].iloc[-60:].std()*np.sqrt(252)*100))
