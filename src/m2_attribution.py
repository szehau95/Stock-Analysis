"""MODULE 2 quantitative support:
 (a) weekly factor model of bank TR on dMGS10, non-bank domestic equity, dUST10, USDMYR, Brent -> attribute each leg
 (b) price-change decomposition from 52w high: dlnP = dlnBV + dlnPB  and  dlnP = dlnEPS_core + dlnPE ; + dividend
 (c) dividend-yield spread vs MGS: now vs 1y ago
 (d) EPF/KWAP substantial-shareholder net activity in 2026 (Bursa filings via klsescreener transcription)"""
import pandas as pd, numpy as np, statsmodels.api as sm, re
from common import *
def weekly_factors():
    md = pd.read_csv("data/clean/mgs_daily_bnm.csv", parse_dates=["req"]).set_index("req").sort_index()
    mg = md["10Y"].astype(float)/100
    comp = composite("tr")
    nb = ["TENAGA","YTLPOWR","GAMUDA","PCHEM","IHH","CDB","SUNWAY","YTL","IOICORP","PMETAL","TM","SIMEPLT"]
    NB = pd.DataFrame({k: px(k).Close for k in nb}).pct_change(); nbi = (1 + NB.mean(axis=1)).cumprod()
    f = pd.DataFrame({"bank": comp, "nonbank": nbi, "mgs10": mg, "ust10": px("UST10").Close/100,
                      "usdmyr": px("USDMYR").Close, "brent": px("BRENT").Close}).ffill()
    f = f[f.index >= "2025-01-03"]
    w = f.resample("W-FRI").last()
    X = pd.DataFrame({"r_bank": w.bank.pct_change(), "r_nonbank": w.nonbank.pct_change(), "d_mgs": w.mgs10.diff()*1e4,
                      "d_ust": w.ust10.diff()*1e4, "r_myr": -w.usdmyr.pct_change(), "r_brent": w.brent.pct_change()}).dropna()
    return X, f
def factor_attr():
    X, f = weekly_factors()
    est = X[X.index < "2026-07-15"]
    fac = ["r_nonbank","d_mgs","d_ust","r_myr","r_brent"]
    m = sm.OLS(est.r_bank, sm.add_constant(est[fac])).fit(cov_type="HC1")
    legs = {"Leg1 11/02->03/06/2026": ("2026-02-11","2026-06-05"), "Leg2 05/08->30/09/2026": ("2026-08-07","2026-10-02"),
            "Since peak 11/02->30/09": ("2026-02-11","2026-10-02"), "YTD": ("2026-01-02","2026-10-02")}
    rows = []
    for name, (a, z) in legs.items():
        s = X[(X.index > a) & (X.index <= z)]
        contrib = {k: (m.params[k]*s[k]).sum() for k in fac}
        actual = np.prod(1 + s.r_bank) - 1
        r = dict(leg=name, weeks=len(s), actual_bank_tr=actual, **{"contrib_"+k: v for k, v in contrib.items()},
                 alpha_drift=m.params["const"]*len(s))
        r["residual_unexplained"] = np.log1p(actual) - sum(contrib.values()) - r["alpha_drift"]
        r["mgs_move_bps"] = s.d_mgs.sum(); r["ust_move_bps"] = s.d_ust.sum(); r["brent_move"] = np.prod(1+s.r_brent)-1
        r["nonbank_move"] = np.prod(1+s.r_nonbank)-1; r["myr_move"] = np.prod(1+s.r_myr)-1
        rows.append(r)
    return m, pd.DataFrame(rows).set_index("leg")
def decomposition():
    rows = []
    for b in BANKS:
        d = panel(b); win = d[d.index > ASOF - pd.Timedelta(days=365)]; hi = win.Close.idxmax()
        a, z = d.loc[hi], d.iloc[-1]
        dlnP = np.log(z.Close/a.Close); dlnTR = np.log(z.tr_idx/a.tr_idx)
        r = dict(bank=b, from_date=hi.date(), price_chg=np.exp(dlnP)-1, tr_chg=np.exp(dlnTR)-1,
                 bv_effect=np.log(z.bv/a.bv), pb_effect=np.log(z.pb/a.pb),
                 eps_effect=np.log(z.eps_ttm_core/a.eps_ttm_core), pe_effect=np.log(z.pe_core/a.pe_core),
                 dividend_effect=dlnTR - dlnP)
        tot = dlnP
        r["pct_of_price_decline_from_multiple(PE)"] = r["pe_effect"]/tot if tot < 0 else np.nan
        r["pct_of_price_decline_from_EPS"] = r["eps_effect"]/tot if tot < 0 else np.nan
        # dividend-yield spread vs MGS now vs 1y ago
        mg = pd.read_csv("data/clean/mgs_daily_bnm.csv", parse_dates=["req"]).set_index("req")["10Y"].astype(float)/100
        t1 = ASOF - pd.DateOffset(years=1)
        r["dy_now"] = z.dy; r["dy_1y_ago"] = d.dy.asof(t1); r["mgs_now"] = mg.asof(ASOF); r["mgs_1y_ago"] = mg.asof(t1)
        r["spread_now"] = r["dy_now"] - r["mgs_now"]; r["spread_1y_ago"] = r["dy_1y_ago"] - r["mgs_1y_ago"]
        r["spread_at_52w_high"] = d.dy.asof(hi) - mg.asof(hi); r["mgs_at_high"] = mg.asof(hi)
        rows.append(r)
    return pd.DataFrame(rows).set_index("bank")
def local_institutions():
    rows = []
    for b in BANKS:
        s = pd.read_csv(f"data/clean/substantial_{b}.csv")
        s["date"] = pd.to_datetime(s.date_change, format="%d %b %Y", errors="coerce")
        s["sh"] = pd.to_numeric(s.shares.astype(str).str.replace(",",""), errors="coerce")
        s["sign"] = s.type.map({"Acquired":1,"Disposed":-1}).fillna(0)
        for who, pat in {"EPF":"EMPLOYEES PROVIDENT","KWAP":"KWAP|PERSARAAN","PNB/ASNB":"AMANAH SAHAM|PERMODALAN NASIONAL"}.items():
            x = s[s.name.str.upper().str.contains(pat, na=False)]
            for per, (a, z) in {"2026YTD":("2026-01-01","2026-09-30"), "Aug-Sep26":("2026-08-01","2026-09-30"), "Feb-Jun26":("2026-02-01","2026-06-30")}.items():
                y = x[(x.date >= a) & (x.date <= z)]
                rows.append(dict(bank=b, holder=who, period=per, net_shares_m=(y.sh*y.sign).sum()/1e6, n_filings=len(y)))
    L = pd.DataFrame(rows)
    px_now = {b: panel(b).Close.iloc[-1] for b in BANKS}
    L["net_rm_m_at_current_px"] = L.apply(lambda r: r.net_shares_m*px_now[r.bank], axis=1)
    return L.pivot_table(index=["bank"], columns=["holder","period"], values="net_rm_m_at_current_px", aggfunc="sum").round(0)
if __name__ == "__main__":
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40)
    m, A = factor_attr(); print(m.summary().tables[1]); print("R2", round(m.rsquared,3), "n", int(m.nobs))
    A.to_csv("output/m2_factor_attribution.csv"); print(A.round(4).T.to_string())
    D = decomposition(); D.to_csv("output/m2_decomposition.csv"); print(D.round(3).to_string())
    L = local_institutions(); L.to_csv("output/m2_local_institutions.csv"); print(L.to_string())
