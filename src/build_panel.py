"""Build point-in-time daily panel per bank (current share basis).
- Price: Yahoo Close (split-adjusted) ; dividends: Yahoo (split-adjusted, by ex-date)
- Fundamentals: klsescreener transcription of Bursa quarterly filings (raw basis) -> rebased to current share basis by
  detecting the NTA discontinuity nearest each split; mapped to trading days by *announcement date* (no look-ahead).
"""
import pandas as pd, numpy as np
BANKS = ["MAYBANK","PBBANK","CIMB","HLBANK","RHBBANK","AMBANK","BIMB","ALLIANCE","AFFIN"]

def load_px(k):
    h = pd.read_csv(f"data/raw/yf_{k}.csv", index_col=0, parse_dates=True)
    h.index = pd.to_datetime(h.index).normalize()
    h = h[~h.index.duplicated()].sort_index()
    return h

def rebase_quarterly(bank, splits):
    q = pd.read_csv(f"data/clean/quarterly_{bank}.csv", parse_dates=["qdate","announced"]).sort_values("qdate").reset_index(drop=True)
    q["factor"] = 1.0
    log = []
    for d, r in splits.items():
        if d <= q.qdate.min():   # split predates the fundamentals history: nothing to rebase
            log.append((d.date(), r, "pre-history", None)); continue
        if r >= 1.2:   # large split/bonus: find the NTA jump nearest the split date
            near = q.index[(q.qdate >= d - pd.Timedelta(days=270)) & (q.qdate <= d + pd.Timedelta(days=200))]
            best, bi = 0, None
            for i in near:
                if i + 1 < len(q):
                    ratio = q.nta[i] / q.nta[i+1] * (q.factor[i+1] / q.factor[i])
                    score = -abs(np.log(ratio) - np.log(r))
                    if bi is None or score > best: best, bi = score, i
            q.loc[:bi, "factor"] *= r
            log.append((d.date(), r, q.qdate[bi].date(), round(q.nta[bi]/q.nta[bi+1], 3)))
        else:          # small adjustment: rule = figures announced before split date are on old basis
            q.loc[q.announced < d, "factor"] *= r
            log.append((d.date(), r, "announce-rule", None))
    for c in ["eps_sen","dps_sen","nta"]:
        q[c + "_adj"] = q[c] / q["factor"]
    return q, log

# --- Core-earnings overrides (earnings-quality check). Each entry documented in output/core_adjustments.csv ---
ONE_OFF = {  # bank: {qdate: reason}  -> EPS replaced by median of 4 neighbouring quarters
 "MAYBANK": {"2009-06-30": "BII goodwill impairment (one-off, RM1.9b-class)"},
 "AMBANK":  {"2007-03-31": "4QFY07 exceptional impairment/loss", "2021-03-31": "1MDB global settlement RM2.83b (4QFY21)"},
 "AFFIN":   {"2022-09-30": "Gain on disposal of Affin Hwang Asset Management stake"},
 "CIMB":    {"2018-06-30": "Gain on disposal of 50% CIMB Securities International (CITIC Sec)"},
 "HLBANK":  {"2013-03-31": "Source transcription error (EPS=0.00)"},
}
SPREAD_FY = {"CIMB": ("2021-03-31","2021-06-30","2021-09-30","2021-12-31")}  # quarterly mis-allocation; annual reconciles
CUKAI_MAKMUR = {"DEC": ("2022-03-31","2022-12-31"), "HLBANK": ("2021-09-30","2022-06-30"), "AMBANK": ("2021-06-30","2022-03-31"), "ALLIANCE": ("2021-06-30","2022-03-31")}
CM_FACTOR = 0.90   # reported PAT / PAT ex-prosperity-tax (approx; Maybank ~0.895, PBB ~0.906 per FY22 disclosures)

def core_eps(bank, q):
    e = q.eps_sen_adj.copy(); notes = []
    for qd, why in ONE_OFF.get(bank, {}).items():
        i = q.index[q.qdate == qd]
        if len(i):
            i = i[0]; nb = [q.eps_sen_adj[j] for j in (i-2, i-1, i+1, i+2) if 0 <= j < len(q)]
            new = float(np.median(nb)); notes.append((bank, qd, "one-off", why, e[i], new)); e[i] = new
    if bank in SPREAD_FY:
        idx = q.index[q.qdate.isin(pd.to_datetime(SPREAD_FY[bank]))]
        avg = e[idx].mean(); notes += [(bank, str(q.qdate[i].date()), "re-spread", "quarterly mis-allocation; FY total kept", e[i], avg) for i in idx]; e[idx] = avg
    a, z = CUKAI_MAKMUR.get(bank, CUKAI_MAKMUR["DEC"])
    m = (q.qdate >= a) & (q.qdate <= z)
    for i in q.index[m]: notes.append((bank, str(q.qdate[i].date()), "cukai-makmur", f"add back prosperity tax (x1/{CM_FACTOR})", e[i], e[i]/CM_FACTOR))
    e[m] = e[m] / CM_FACTOR
    return e, notes

def build(bank):
    px = load_px(bank)
    splits = px.loc[px["Stock Splits"] > 0, "Stock Splits"].to_dict()
    q, log = rebase_quarterly(bank, splits)
    if bank == "CIMB":   # source transcription error: 12/2005 NTA inconsistent with neighbours
        i = q.index[q.qdate == "2005-12-31"]
        if len(i): q.loc[i, "nta_adj"] = (q.nta_adj[i[0]-1] + q.nta_adj[i[0]+1]) / 2
    q["eps_core_sen_adj"], notes = core_eps(bank, q)
    build.notes += notes
    q["eps_ttm"] = q.eps_sen_adj.rolling(4).sum() / 100
    q["eps_ttm_core"] = q.eps_core_sen_adj.rolling(4).sum() / 100
    q["bv"] = q.nta_adj
    q["bv_avg"] = (q.bv + q.bv.shift(4)) / 2
    q["roe_ttm"] = q.eps_ttm / q.bv_avg
    q["roe_ttm_core"] = q.eps_ttm_core / q.bv_avg
    q["dps_ttm_q"] = q.dps_sen_adj.rolling(4).sum() / 100
    q["eps_ttm_yoy"] = q.eps_ttm / q.eps_ttm.shift(4) - 1
    q["pl_ttm"] = q.pl.rolling(4).sum()
    q.to_csv(f"data/clean/quarterly_adj_{bank}.csv", index=False)
    # point-in-time mapping on announcement date
    qa = q.dropna(subset=["announced"]).sort_values("announced")[["announced","qdate","bv","eps_ttm","roe_ttm","eps_ttm_yoy","eps_ttm_core","roe_ttm_core","dps_ttm_q"]]
    d = px[["Open","High","Low","Close","Volume","Dividends"]].copy()
    d["tr_idx"] = (d.Close + d.Dividends).div(d.Close.shift(1)).fillna(1).cumprod()
    d["dps_ttm"] = d.Dividends.rolling("365D").sum()
    d = pd.merge_asof(d.reset_index().rename(columns={"index":"date","Date":"date"}).sort_values("date"), qa, left_on="date", right_on="announced", direction="backward").set_index("date")
    d["pb"] = d.Close / d.bv
    d["pe"] = d.Close / d.eps_ttm
    d["pe_core"] = d.Close / d.eps_ttm_core
    d["dy"] = d.dps_ttm / d.Close
    d.to_csv(f"data/clean/panel_{bank}.csv")
    return d, log

build.notes = []
if __name__ == "__main__":
    for b in BANKS:
        d, log = build(b)
        last = d.iloc[-1]
        pass
        print(f"{b:9s} core_roe={last.roe_ttm_core:5.3f} px={last.Close:6.2f} bv={last.bv:6.3f} pb={last.pb:4.2f} pe={last.pe:5.1f} roe={last.roe_ttm:5.3f} dy={last.dy:5.3f} qdate={last.qdate.date()} | splits->{log}")

    pd.DataFrame(build.notes, columns=["bank","qdate","type","reason","eps_reported_sen","eps_core_sen"]).to_csv("output/core_adjustments.csv", index=False)
