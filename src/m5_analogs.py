"""MODULE 5 — Historical analog study (bank composite + per-bank base rates)."""
import pandas as pd, numpy as np
from common import *
LABELS = [  # (start, end, trigger) — episode trigger labels from date-anchored history (tier-2 general record)
 ("2000-01-01","2001-12-31","Dot-com bust / post-AFC bank merger overhang / 9-11"),
 ("2002-01-01","2003-06-30","2002-03 global bear market / Iraq war / SARS"),
 ("2004-01-01","2005-12-31","2004-05 rate-hike cycle (Fed), post-GE11 consolidation"),
 ("2006-01-01","2006-12-31","May-Jun 2006 EM sell-off"),
 ("2007-06-01","2009-06-30","GFC + GE12 'political tsunami' (08/03/2008)"),
 ("2010-01-01","2010-06-30","Euro sovereign crisis I"),
 ("2011-01-01","2012-06-30","Euro sovereign crisis II / US downgrade"),
 ("2013-01-01","2016-12-31","Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era)"),
 ("2017-01-01","2019-06-30","GE14 (09/05/2018) + 2018 EM/trade-war sell-off"),
 ("2019-07-01","2021-12-31","COVID-19 + 200bp OPR cuts + moratorium"),
 ("2022-01-01","2023-12-31","Cukai Makmur (Budget 2022) + Fed hikes / foreign outflows"),
 ("2024-01-01","2025-12-31","2025 US tariff shock / OPR cut (07/2025)"),
 ("2026-01-01","2026-12-31","2026 Iran war/oil shock + global yield spike + KLCI-50 reweight"),
]
def label(d):
    for a, z, t in LABELS:
        if pd.Timestamp(a) <= d <= pd.Timestamp(z): return t
    return "unlabelled"
def comp_fundamentals():
    w = mcap_weights(); cols = {}
    for k in ["pb","roe_ttm_core","dy","eps_ttm_core","pe_core"]:
        cols[k] = pd.DataFrame({b: panel(b)[k] for b in BANKS})
    W = cols["pb"].notna().mul(w, axis=1); W = W.div(W.sum(axis=1), axis=0)
    agg = pd.DataFrame({k: (v.clip(lower=-1, upper=50) * W).sum(axis=1) for k, v in cols.items() if k != "eps_ttm_core"})
    # EPS index: cap-weighted average of per-bank log EPS changes (dilution-agnostic, per-share basis)
    e = cols["eps_ttm_core"].where(cols["eps_ttm_core"] > 0)
    de = np.log(e).diff().fillna(0).clip(-0.5, 0.5)
    agg["eps_idx"] = np.exp((de * W).sum(axis=1).cumsum())
    return agg
def fwd(idx, d, months):
    t = d + pd.DateOffset(months=months)
    if t > idx.index[-1]: return np.nan
    return idx.asof(t) / idx.asof(d) - 1
def max_further_dd(idx, d, months=12):
    s = idx[(idx.index >= d) & (idx.index <= d + pd.DateOffset(months=months))]
    return s.min() / s.iloc[0] - 1 if len(s) > 5 else np.nan
def episodes_rolling(idx, thresh=0.15, merge_gap=60):
    """Episodes = contiguous spells where drawdown from rolling-252d high <= -thresh (gaps < merge_gap days merged).
    peak = date of the rolling high that defines the trough; recovery = first date after trough back at that high."""
    hi = idx.rolling(252, min_periods=60).max(); dd = idx / hi - 1
    mask = dd <= -thresh; spells, cur = [], None
    for d, m in mask.items():
        if m:
            if cur and (d - cur[1]).days <= merge_gap: cur[1] = d
            else:
                if cur: spells.append(cur)
                cur = [d, d]
    if cur: spells.append(cur)
    out = []
    for a, z in spells:
        seg = idx[(idx.index >= a - pd.Timedelta(days=5)) & (idx.index <= z + pd.Timedelta(days=5))]
        tg = seg.idxmin(); pk_val = hi[tg]
        pk = idx[(idx.index <= tg) & (idx.index >= tg - pd.Timedelta(days=400))].idxmax()
        rec = idx[(idx.index > tg) & (idx >= idx[pk])]
        out.append((pk, tg, rec.index[0] if len(rec) else None))
    # de-duplicate by peak (keep deepest trough)
    ded = {}
    for pk, tg, rec in out:
        if pk not in ded or idx[tg] < idx[ded[pk][0]]: ded[pk] = (tg, rec)
    return [(pk, tg, rec) for pk, (tg, rec) in sorted(ded.items())]
def episodes(idx, thresh=0.15):
    """Peak-to-trough episodes on running-max basis; episode closes when prior peak is regained."""
    eps, peak_d, peak, trough_d, trough, in_ep = [], idx.index[0], idx.iloc[0], None, None, False
    for d, v in idx.items():
        if v >= peak:
            if in_ep and trough / peak - 1 <= -thresh: eps.append((peak_d, trough_d, d))
            peak, peak_d, trough, trough_d, in_ep = v, d, v, d, False
        else:
            if v < (trough if trough is not None else v + 1): trough, trough_d = v, d
            if v / peak - 1 <= -thresh: in_ep = True
    if in_ep: eps.append((peak_d, trough_d, None))
    return eps
def run():
    tr = composite("tr"); F = comp_fundamentals(); mg = mgs()
    E = []
    cur_depth = tr.iloc[-1] / tr[tr.index > ASOF - pd.Timedelta(days=365)].max() - 1
    for pk, tg, rec in episodes_rolling(tr):
        r = dict(peak=pk.date(), trough=tg.date(), recovered=rec.date() if rec is not None else "not yet",
                 trigger=label(tg), peak_to_trough=tr[tg]/tr[pk]-1, days_to_trough=(tg-pk).days,
                 days_to_recover=(rec-tg).days if rec is not None else np.nan)
        for k in ["pb","roe_ttm_core","dy","pe_core"]:
            r[f"{k}_peak"] = F[k].asof(pk) if pk >= pd.Timestamp("2003-06-30") else np.nan
            r[f"{k}_trough"] = F[k].asof(tg) if tg >= pd.Timestamp("2003-06-30") else np.nan
        r["mgs10_trough"] = mg.asof(tg) if tg >= mg.index[0] else np.nan
        ok = pk >= pd.Timestamp("2003-06-30")
        r["eps_chg_peak_to_trough"] = F.eps_idx.asof(tg)/F.eps_idx.asof(pk)-1 if ok else np.nan
        r["eps_chg_trough_to_+12m"] = F.eps_idx.asof(tg + pd.DateOffset(months=12))/F.eps_idx.asof(tg)-1 if tg + pd.DateOffset(months=12) <= ASOF else np.nan
        r["roe_chg_peak_to_+24m"] = F.roe_ttm_core.asof(min(ASOF, tg + pd.DateOffset(months=24))) - F.roe_ttm_core.asof(pk) if ok else np.nan
        e1, e2 = r["eps_chg_peak_to_trough"], r["eps_chg_trough_to_+12m"]
        if not ok: r["type"] = "n/a (pre-fundamentals data)"
        elif r["roe_chg_peak_to_+24m"] <= -0.025 and (pd.isna(e2) or e2 < 0.05): r["type"] = "ROE reset (structural)"
        elif e1 <= -0.05 or (not pd.isna(e2) and e2 <= -0.05): r["type"] = "EPS-revision-led"
        else: r["type"] = "Multiple-only derating"
        for mth in (3, 6, 12, 36): r[f"fwd{mth}m_from_trough"] = fwd(tr, tg, mth)
        # first date the drawdown from the episode peak reached the current depth
        s = tr[(tr.index >= pk) & (tr.index <= tg)]; hit = s[s / tr[pk] - 1 <= cur_depth]
        if len(hit):
            h = hit.index[0]; r["first_hit_current_depth"] = h.date()
            for mth in (3, 6, 12, 36): r[f"fwd{mth}m_from_hit"] = fwd(tr, h, mth)
            r["further_dd_after_hit"] = tr[tg] / tr[h] - 1
            r["pb_at_hit"] = F.pb.asof(h); r["dy_at_hit"] = F.dy.asof(h)
        E.append(r)
    E = pd.DataFrame(E)
    return E, cur_depth, F
def base_rates(series, depth, cooldown_recover=0.5, horizon=12):
    """Events: first crossing of drawdown-from-rolling-52w-high <= depth; re-arm only after drawdown recovers above depth*cooldown."""
    roll_hi = series.rolling(252, min_periods=120).max(); dd = series / roll_hi - 1
    ev, armed = [], True
    for d, v in dd.dropna().items():
        if armed and v <= depth: ev.append(d); armed = False
        elif not armed and v > depth * cooldown_recover: armed = True
    rows = []
    for d in ev:
        if d + pd.DateOffset(months=horizon) > series.index[-1]: continue
        rows.append(dict(date=d, fwd12=fwd(series, d, 12), fwd6=fwd(series, d, 6), fwd36=fwd(series, d, 36), mdd12=max_further_dd(series, d, 12)))
    R = pd.DataFrame(rows)
    if R.empty: return dict(n=0), R
    return dict(n=len(R), hit_rate_12m=(R.fwd12 > 0).mean(), median_12m=R.fwd12.median(), mean_12m=R.fwd12.mean(), worst_12m=R.fwd12.min(),
                best_12m=R.fwd12.max(), median_6m=R.fwd6.median(), median_36m=R.fwd36.median(), hit_rate_36m=(R.fwd36.dropna() > 0).mean(),
                median_max_further_dd=R.mdd12.median(), worst_max_further_dd=R.mdd12.min()), R
if __name__ == "__main__":
    pd.set_option("display.width", 260); pd.set_option("display.max_columns", 60)
    E, cur_depth, F = run(); E.to_csv("output/m5_episodes.csv", index=False)
    print("Composite current TR drawdown from 52w high:", round(cur_depth, 4))
    print(E[["peak","trough","recovered","trigger","type","peak_to_trough","days_to_trough","days_to_recover"]].round(3).to_string())
    print(E[["trough","pb_trough","roe_ttm_core_trough","dy_trough","mgs10_trough","eps_chg_peak_to_trough","eps_chg_trough_to_+12m","roe_chg_peak_to_+24m"]].round(3).to_string())
    print(E[["trough","fwd3m_from_trough","fwd6m_from_trough","fwd12m_from_trough","fwd36m_from_trough","first_hit_current_depth","fwd12m_from_hit","fwd36m_from_hit","further_dd_after_hit"]].round(3).to_string())
    now = F.iloc[-1]; print("NOW composite:", now.round(4).to_dict())
    # base rates: composite and per bank at their own current depth
    rows = []
    comp = composite("tr"); s, R = base_rates(comp, cur_depth); rows.append(dict(series="COMPOSITE", depth=cur_depth, **s)); R.to_csv("output/m5_events_composite.csv", index=False)
    for b in BANKS:
        t = panel(b).tr_idx; t = t[t.index >= ("2009-01-01" if b == "BIMB" else "2000-01-01")]
        dpt = t.iloc[-1] / t[t.index > ASOF - pd.Timedelta(days=365)].max() - 1
        s, R = base_rates(t, dpt); rows.append(dict(series=b, depth=dpt, **s))
        # conditional: also require P/B at/below current 10y percentile band? (valuation-conditioned) -> P/B <= current P/B * 1.1
        R.to_csv(f"output/m5_events_{b}.csv", index=False)
    B = pd.DataFrame(rows).set_index("series"); B.to_csv("output/m5_base_rates.csv"); print(B.round(3).to_string())
    # valuation-conditioned base rates on composite: dates where composite P/B within +/-10% of today's AND ROE within +/-1.5pp
    pbn, roen = now.pb, now.roe_ttm_core
    cand = F[(F.pb.between(pbn*0.9, pbn*1.1)) & (F.roe_ttm_core.between(roen-0.015, roen+0.015))].index
    cand = [d for d in cand if d + pd.DateOffset(months=12) <= ASOF]
    fw = pd.Series({d: fwd(comp, d, 12) for d in cand}).dropna()
    print("Valuation-conditioned (PB+-10%, ROE+-1.5pp) daily obs:", len(fw), "hit", round((fw>0).mean(),3), "median", round(fw.median(),3), "p10", round(fw.quantile(.1),3), "years:", sorted(set(pd.DatetimeIndex(fw.index).year)))
    fw.to_csv("output/m5_valuation_conditioned.csv")

def similarity(thresh=0.08):
    """Match current setup to history on FUNDAMENTALS (not price): ROE vs trailing-5y avg, EPS change peak->trough,
    P/B vs trailing-5y mean, dMGS10 and dUST10 over the episode, Brent change."""
    tr = composite("tr"); F = comp_fundamentals(); mg = mgs(); ust = px("UST10").Close/100; br = px("BRENT").Close
    def feats(pk, tg):
        if pk < pd.Timestamp("2008-06-30"): return None
        f5 = F[(F.index > tg - pd.DateOffset(years=5)) & (F.index <= tg)]
        return dict(roe_vs_5y=F.roe_ttm_core.asof(tg) - f5.roe_ttm_core.mean(), pb_vs_5y=F.pb.asof(tg)/f5.pb.mean()-1,
                    eps_chg=F.eps_idx.asof(tg)/F.eps_idx.asof(pk)-1, d_mgs=(mg.asof(tg)-mg.asof(pk))*1e4,
                    d_ust=(ust.asof(tg)-ust.asof(pk))*1e4, brent=br.asof(tg)/br.asof(pk)-1 if pk >= br.index[0] else np.nan,
                    dd=tr[tg]/tr[pk]-1)
    rows = []
    for pk, tg, rec in episodes_rolling(tr, thresh):
        f = feats(pk, tg)
        if f is None: continue
        f.update(peak=pk.date(), trough=tg.date(), trigger=label(tg), fwd12=fwd(tr, tg, 12), fwd36=fwd(tr, tg, 36),
                 e12=F.eps_idx.asof(min(ASOF, tg + pd.DateOffset(months=12)))/F.eps_idx.asof(tg)-1)
        rows.append(f)
    H = pd.DataFrame(rows)
    pk_now = tr[tr.index > ASOF - pd.Timedelta(days=365)].idxmax()
    cur = feats(pk_now, ASOF); cur.update(peak=pk_now.date(), trough=ASOF.date(), trigger="CURRENT")
    k = ["roe_vs_5y","pb_vs_5y","eps_chg","d_mgs","d_ust","brent"]
    Z = H[k].copy(); sd = Z.std()
    dist = (((Z - pd.Series(cur)[k].astype(float)) / sd) ** 2).sum(axis=1, min_count=4) ** 0.5
    H["distance_to_now"] = dist
    return H.sort_values("distance_to_now"), cur
if __name__ == "__main__":
    H, cur = similarity(0.08); H.to_csv("output/m5_similarity.csv", index=False)
    print("CURRENT:", {k: (round(v,3) if isinstance(v,float) else v) for k, v in cur.items()})
    print(H[["peak","trough","trigger","dd","roe_vs_5y","pb_vs_5y","eps_chg","d_mgs","d_ust","brent","e12","fwd12","fwd36","distance_to_now"]].round(3).to_string())
