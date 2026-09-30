"""MODULE 1 — Premise validation & price forensics."""
import pandas as pd, numpy as np
from common import *
EVENTS = {  # date -> catalyst tag (tier-2 press, date-anchored); used to label large down days
 "2026-03-02":"US/Israel strikes on Iran (28/02) — first trading day; Brent spike",
 "2026-03-03":"Iran war: Brent >$81, risk-off", "2026-03-09":"Iran war escalation: KLCI -2.55% (steepest 2026 fall pre-Sep)",
 "2026-05-28":"1Q26 results: Maybank/CIMB soft, PBB flat; ME-conflict provision fears", "2026-05-29":"1Q26 results digestion / MSCI May SAIR effective",
 "2026-06-01":"MSCI rebalance flows; RM2.53b weekly foreign outflow", "2026-08-03":"Maybank RM4.83b Etiqa buyout (CET1 drag, DRP)",
 "2026-08-04":"Maybank Etiqa buyout reaction", "2026-08-20":"FBM KLCI 50 revamp announced (FS weight 42.8%->36.8%)",
 "2026-08-21":"FBM KLCI 50 revamp reaction", "2026-08-26":"PBB 2Q26 results", "2026-08-27":"Maybank/HLB 2Q results; Maybank DRP",
 "2026-08-28":"RHB/CIMB 2Q results",
 "2026-09-01":"1st session after 2Q results + Merdeka: FS foreign outflow -RM462.9m in shortened week (MBSB)",
 "2026-09-18":"FS foreign outflow -RM309.7m in w/e 18/09 despite market net inflow (MBSB)",
 "2026-06-03":"foreign-outflow phase: RM2.53b net sold in w/e 29/05 (MSCI May SAIR effective 29/05)",
 "2026-02-27":"FY25 results window (Maybank/CIMB 26-27/02)",
 "2026-08-18":"Affin 2Q26 results (14/08, profit -11%) digestion; FS outflow w/e 21/08",
 "2026-08-19":"AMMB 1QFY27 results (18/08); FS outflow w/e 21/08", "2026-09-11":"MGS10Y peaks 4.18% (HLIB)", "2026-09-29":"KLCI -1.56% to 9-month low: oil + bond yields at multi-year highs",
}
def dd_table():
    kl = px("KLCI"); fx = px("USDMYR").Close.reindex(kl.index).ffill()
    comp_pr, comp_tr = composite("pr"), composite("tr")
    rows, downs, exdivs = [], [], []
    ytd0 = pd.Timestamp("2025-12-31")
    def stats(name, close, tr, kind="stock", volume=None, opn=None, divs=None, ann=None):
        c = close.dropna(); t = tr.reindex(c.index).ffill()
        win = c[c.index > ASOF - pd.Timedelta(days=365)]
        hi_d = win.idxmax(); hi = win.max(); cur = c.iloc[-1]
        lo_d = c[c.index >= hi_d].idxmin(); lo = c[c.index >= hi_d].min()
        base = lambda s, dt: s[:dt].iloc[-1]
        r = dict(name=name, hi_52w=hi, hi_date=hi_d.date(), current=cur, trough=lo, trough_date=lo_d.date(),
                 pk_trough_pr=lo/hi-1, dd_pr=cur/hi-1, dd_tr=t.iloc[-1]/t[hi_d]-1,
                 ytd_pr=cur/base(c,ytd0)-1, ytd_tr=t.iloc[-1]/base(t,ytd0)-1,
                 m1=cur/c.iloc[-22]-1, m3=cur/c.iloc[-64]-1,
                 dd_tr_usd=(t.iloc[-1]/t[hi_d])*(fx[hi_d]/fx.iloc[-1])-1 if kind!="peer" else np.nan)
        r["div_share_of_pr_dd"] = (r["dd_pr"]-r["dd_tr"])/r["dd_pr"] if r["dd_pr"] < 0 else np.nan
        kl_c = kl.Close
        r["rel_klci_since_hi"] = r["dd_pr"] - (kl_c.iloc[-1]/kl_c[:hi_d].iloc[-1]-1)
        r["rel_comp_since_hi"] = r["dd_pr"] - (comp_pr.iloc[-1]/comp_pr[:hi_d].iloc[-1]-1)
        if divs is not None:
            dv = divs[(divs.index > hi_d) & (divs > 0)]
            r["exdiv_in_window"] = "; ".join(f"{d.strftime('%d/%m/%Y')}:{v:.3f}" for d, v in dv.items())
            r["dps_in_window"] = dv.sum()
        if opn is not None:   # largest down days since high
            ret = t.pct_change(); gap = (opn + divs.reindex(c.index).fillna(0)) / c.shift(1) - 1   # dividend-neutral returns/gaps
            vol_rel = volume / volume.rolling(60).mean()
            sub = ret[ret.index > hi_d].nsmallest(5)
            for d, v in sub.items():
                tag = EVENTS.get(d.strftime("%Y-%m-%d"), "")
                if divs is not None and divs.get(d, 0) > 0: tag = (tag + "; " if tag else "") + f"EX-DIV {divs[d]:.3f} ({divs[d]/c.shift(1)[d]*100:.1f}% of px)"
                if ann is not None and any(abs((d - a).days) <= 1 for a in ann): tag = (tag + "; " if tag else "") + "own results window"
                downs.append(dict(bank=name, date=d.date(), ret=v, gap_open=gap[d], vol_x60d=vol_rel[d], catalyst=tag or "no specific catalyst identified (market/flow)"))
            n_gap = int(((gap < -0.02) & (gap.index > hi_d)).sum())
            r["top5_down_sum"] = sub.sum(); r["gapdown_days_gt2pct"] = n_gap
            maxdd = (t[t.index >= hi_d] / t[t.index >= hi_d].cummax()).min() - 1
            r["max_dd_tr"] = maxdd; r["days_tr_le_-2pct"] = int((ret[ret.index > hi_d] <= -0.02).sum())
            share = min(1.0, np.log1p(sub).sum() / np.log1p(maxdd)) if maxdd < 0 else np.nan
            r["top5_share_of_tr_dd"] = share
            r["pattern"] = "event-driven" if share > 0.6 else ("mixed" if share > 0.4 else "orderly drift")
        # two-leg decomposition: leg1 = 52w high -> trough before 15/07/2026 ; leg2 = Jul-Sep high -> now (TR basis)
        mid = pd.Timestamp("2026-07-15")
        l1 = t[(t.index >= hi_d) & (t.index < mid)]
        if len(l1) > 1:
            r["leg1_tr"] = l1.min() / t[hi_d] - 1; r["leg1_trough"] = l1.idxmin().date()
        l2 = t[t.index >= mid]; l2h = l2.idxmax()
        r["leg2_high"] = l2h.date(); r["leg2_tr"] = t.iloc[-1] / t[l2h] - 1
        r["rebound_between"] = (t[l2h] / l1.min() - 1) if len(l1) > 1 else np.nan
        return r
    for b in BANKS:
        d = panel(b); a = pd.read_csv(f"data/clean/quarterly_{b}.csv", parse_dates=["announced"]).announced.dropna()
        rows.append(stats(b, d.Close, d.tr_idx, volume=d.Volume, opn=d.Open, divs=d.Dividends, ann=list(a[a > ASOF - pd.Timedelta(days=400)])))
    rows.append(stats("BANK COMPOSITE (cap-wtd)", comp_pr, comp_tr, kind="comp"))
    rows.append(stats("FBM KLCI", kl.Close, kl.Close, kind="idx"))
    # KLCI ex-banks: (a) algebraic with FS weight 40% (b) equal-wt basket of 11 non-bank KLCI names
    w = 0.40
    klr = kl.Close.pct_change(); cr = comp_pr.pct_change().reindex(klr.index)
    exb = (1 + ((klr - w * cr) / (1 - w)).fillna(0)).cumprod()
    rows.append(stats("KLCI ex-banks (algebraic, FS wt 40%)", exb, exb, kind="idx"))
    nb = ["TENAGA","YTLPOWR","GAMUDA","PCHEM","IHH","CDB","SUNWAY","YTL","IOICORP","PMETAL","TM","SIMEPLT"]
    NB = pd.DataFrame({k: px(k).Close for k in nb}).pct_change().loc["2015":]
    nbi = (1 + NB.mean(axis=1, skipna=True)).cumprod()
    rows.append(stats("Non-bank KLCI basket (EW, 12 names)", nbi, nbi, kind="idx"))
    out = pd.DataFrame(rows).set_index("name")
    # peers in local ccy and USD
    peers = {"DBS":"USDSGD","OCBC":"USDSGD","UOB":"USDSGD","BBCA":"USDIDR","BBRI":"USDIDR","BMRI":"USDIDR","KBANK":"USDTHB","BBL":"USDTHB"}
    prow = []
    for p, f in peers.items():
        h = px(p); fxs = px(f).Close.reindex(h.index).ffill()
        tr = ((h.Close + h.Dividends) / h.Close.shift(1)).fillna(1).cumprod()
        r = stats(p, h.Close, tr, kind="peer")
        hi_d = pd.Timestamp(r["hi_date"])
        r["dd_tr_usd"] = (tr.iloc[-1] / tr[hi_d]) * (fxs[hi_d] / fxs.iloc[-1]) - 1
        r["ytd_tr_usd"] = (tr.iloc[-1] / tr[:ytd0].iloc[-1]) * (fxs[:ytd0].iloc[-1] / fxs.iloc[-1]) - 1
        prow.append(r)
    pe = pd.DataFrame(prow).set_index("name")
    return out, pe, pd.DataFrame(downs)
if __name__ == "__main__":
    out, pe, downs = dd_table()
    out.to_csv("output/m1_drawdowns.csv"); pe.to_csv("output/m1_peers.csv"); downs.to_csv("output/m1_down_days.csv", index=False)
    pd.set_option("display.width", 250); pd.set_option("display.max_columns", 40); pd.set_option("display.max_colwidth", 80)
    cols2 = ["max_dd_tr","days_tr_le_-2pct","leg1_trough","leg1_tr","rebound_between","leg2_high","leg2_tr","top5_share_of_tr_dd","pattern"]
    print(out[cols2].round(3).to_string())
    cols = ["hi_52w","hi_date","current","trough","trough_date","dd_pr","dd_tr","dd_tr_usd","div_share_of_pr_dd","ytd_pr","ytd_tr","m1","m3","rel_klci_since_hi","rel_comp_since_hi","top5_down_sum","gapdown_days_gt2pct","pattern"]
    print(out[cols].round(3).to_string())
    print(out[["exdiv_in_window"]].to_string())
    print(pe[["hi_date","dd_pr","dd_tr","dd_tr_usd","ytd_pr","ytd_tr_usd","m3"]].round(3).to_string())
    print(downs.round(3).to_string())
