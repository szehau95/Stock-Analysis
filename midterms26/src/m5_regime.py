"""M5: regime adjustment. Feature vector at each midterm T0 vs today; z-scored nearest-neighbour analogs; simple conditional splits
(midterms only and all November starts 1950-2025); regime-adjusted SPX 6M/12M distribution. Price return unless stated."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, 'src'); from common import load, MIDTERMS, election_day, t0_date, window_stats
OUT = __import__('pathlib').Path('out'); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
def fred(n):
    d = pd.read_csv(f'data/raw/fred/{n}.csv'); d.columns = ['date', 'v']; d['date'] = pd.to_datetime(d.date); d['v'] = pd.to_numeric(d.v, errors='coerce'); return d.dropna().set_index('date').v
FF_, DISC, GS10, DGS10, DFF, CPI, WTI, USREC = (fred(x) for x in ['FEDFUNDS', 'INTDSRUSM193N', 'GS10', 'DGS10', 'DFF', 'CPIAUCSL', 'WTISPLC', 'USREC'])
sh = pd.read_csv('data/raw/shiller/shiller_mirror.csv', parse_dates=['Date']).set_index('Date')
spx = load('SPX')
def at(s, d): x = s[:d]; return x.iloc[-1] if len(x) else np.nan
def feats(y):
    o, a = pd.Timestamp(y, 10, 1), pd.Timestamp(y, 4, 1)
    fed = (at(FF_, o) - at(FF_, a)) if y >= 1955 else (at(DISC, o) - at(DISC, a))
    y10 = at(GS10, o) if y >= 1954 else at(sh['Long Interest Rate'], o)
    y10a = at(GS10, a) if y >= 1954 else at(sh['Long Interest Rate'], a)
    ed = election_day(y); t0 = t0_date(spx, ed); seg = spx[str(y)][:t0]; dd = (seg / seg.cummax() - 1).min()
    return dict(fed_d6m=fed, y10=y10, y10_d6m=y10 - y10a, cpi_yoy=at(CPI, pd.Timestamp(y, 9, 1)) / at(CPI, pd.Timestamp(y - 1, 9, 1)) - 1,
                cape=at(sh['PE10'], o), ytd=spx[t0] / spx[:f'{y - 1}-12-31'].iloc[-1] - 1, mdd=dd, oil_d6m=at(WTI, o) / at(WTI, a) - 1)
X = pd.DataFrame({y: feats(y) for y in MIDTERMS}).T
ev = pd.read_csv(OUT / 'm2_events_SPX_eday.csv'); R = ev.pivot(index='year', columns='window', values='ret')[['6M', '12M']]
R['dd12'] = ev[ev.window == '12M'].set_index('year').maxdd
R['rec12'] = [int(USREC[(USREC.index > pd.Timestamp(y, 10, 1)) & (USREC.index <= pd.Timestamp(y + 1, 10, 1))].max() > 0) for y in R.index]
# today (2026): T0 proxy = 30/10/2026 close
wti = load('WTI'); oct26 = lambda s: s['2026-10-01':'2026-10-31'].mean()
today = dict(fed_d6m=oct26(DFF) - at(FF_, pd.Timestamp(2026, 4, 1)), y10=oct26(DGS10), y10_d6m=oct26(DGS10) - at(GS10, pd.Timestamp(2026, 4, 1)),
             cpi_yoy=at(CPI, pd.Timestamp(2026, 9, 1)) / at(CPI, pd.Timestamp(2025, 9, 1)) - 1, cape=41.1,
             ytd=spx.iloc[-1] / spx[:'2025-12-31'].iloc[-1] - 1, mdd=(spx['2026'] / spx['2026'].cummax() - 1).min(), oil_d6m=oct26(wti) / at(WTI, pd.Timestamp(2026, 4, 1)) - 1)
X.loc[2026] = today
print('Feature vector (T0 = Oct of midterm year; 2026 = Oct-2026 averages; CAPE 2026 = 41.1, Tier 2-3 estimate):'); print(X.round(3).to_string())
H = X.loc[list(MIDTERMS)]; mu, sd = H.mean(), H.std(ddof=0); Z = (X - mu) / sd
d = np.sqrt(((Z.loc[list(MIDTERMS)] - Z.loc[2026]) ** 2).sum(1)).sort_values()
print('\n2026 z-scores vs midterm history:', Z.loc[2026].round(2).to_dict())
A = pd.DataFrame({'dist': d}).join(R).join(H)
def match(y):
    zz = (Z.loc[y] - Z.loc[2026]).abs(); return ', '.join(zz[zz < 0.5].index)
A['matching(|dz|<0.5)'] = [match(y) for y in A.index]
print('\nTABLE 6 — nearest-neighbour analogs (z-scored Euclidean, 8 features):'); print(A.head(6)[['dist', '6M', '12M', 'dd12', 'matching(|dz|<0.5)', 'fed_d6m', 'y10', 'cape', 'cpi_yoy', 'oil_d6m']].round(3).to_string())
A.to_csv(OUT / 'table6_analogs.csv')
# kernel-weighted outcome distribution
h = d.median(); w = np.exp(-(d / h) ** 2 / 2); w = w / w.sum(); neff = 1 / (w ** 2).sum()
def wq(x, w, q):
    o = np.argsort(x.values); xs, ws = x.values[o], w.values[o]; c = np.cumsum(ws) - ws / 2; return float(np.interp(q, c, xs))
K = {}
for c in ['6M', '12M', 'dd12']:
    x = R.loc[d.index, c]; ww = w.loc[d.index]
    K[c] = dict(raw_mean=R[c].mean(), raw_median=R[c].median(), k_mean=float((x * ww).sum()), k_p25=wq(x, ww, 0.25), k_median=wq(x, ww, 0.5), k_p75=wq(x, ww, 0.75))
print(f'\nKernel-weighted (Gaussian, h = median distance {h:.2f}; n_eff = {neff:.1f}):'); print(pd.DataFrame(K).round(4).to_string())
lofo = {}
for f in X.columns:
    cols = [c for c in X.columns if c != f]; dd_ = np.sqrt(((Z.loc[list(MIDTERMS), cols] - Z.loc[2026, cols]) ** 2).sum(1)); ww = np.exp(-(dd_ / dd_.median()) ** 2 / 2); ww /= ww.sum()
    lofo[f] = float((R['12M'] * ww).sum()) - K['12M']['k_mean']
print('Leave-one-feature-out change in kernel 12M mean (+ = that feature was pulling the estimate DOWN):', {k: round(v, 4) for k, v in sorted(lofo.items(), key=lambda kv: -abs(kv[1]))})
# conditional splits — midterms only
def split(mask, label, df=R):
    a, b = df.loc[mask[mask].index, '12M'], df.loc[mask[~mask].index, '12M']
    return dict(split=label, n_yes=len(a), mean_yes=a.mean(), med_yes=a.median(), min_yes=a.min(), n_no=len(b), mean_no=b.mean(), med_no=b.median(), min_no=b.min())
S = [split(H.fed_d6m >= 0.25, 'Fed hiking at T0'), split(H.cape >= H.cape.quantile(0.75), 'CAPE top quartile'), split(R.rec12 == 1, 'Recession within 12M'),
     split(H.y10_d6m > 0.25, '10Y up >25bp in prior 6M'), split(H.oil_d6m >= 0.15, 'Oil up >=15% in prior 6M'), split(H.mdd > -0.10, 'Shallow midterm-yr DD (>-10%)'),
     split((H.fed_d6m >= 0.25) & (H.cape >= H.cape.median()), 'Fed hiking AND CAPE above median')]
SP = pd.DataFrame(S); print('\nConditional splits, MIDTERMS (12M SPX price):'); print(SP.round(4).to_string(index=False))
# all November starts 1950-2025 (bigger n): same splits on every year's e-day-equivalent start
rows = []
for y in range(1950, 2026):
    t0 = t0_date(spx, election_day(y)); st = window_stats(spx, t0, '12M')
    if st is None: continue
    f_ = feats(y); rows.append(dict(year=y, r12=st['ret'], dd12=st['maxdd'], midterm=int(y in MIDTERMS), **f_))
AN = pd.DataFrame(rows).set_index('year')
def split2(mask, label):
    a, b = AN.loc[mask, 'r12'], AN.loc[~mask, 'r12']
    return dict(split=label, n_yes=len(a), mean_yes=a.mean(), med_yes=a.median(), p10_yes=a.quantile(0.10), neg_share_yes=(a < 0).mean(), n_no=len(b), mean_no=b.mean(), med_no=b.median(), neg_share_no=(b < 0).mean())
q75 = AN.cape.quantile(0.75)
S2 = [split2(AN.fed_d6m >= 0.25, 'Fed hiking'), split2(AN.cape >= q75, f'CAPE top quartile (>= {q75:.1f})'), split2((AN.fed_d6m >= 0.25) & (AN.cape >= q75), 'Fed hiking AND CAPE top quartile'),
      split2(AN.y10_d6m > 0.25, '10Y up >25bp'), split2(AN.midterm == 1, 'Midterm year'), split2((AN.midterm == 1) & (AN.cape >= AN.cape.median()), 'Midterm AND CAPE above median')]
SP2 = pd.DataFrame(S2); print('\nConditional splits, ALL November starts 1950-2025 (12M SPX price, n=75):'); print(SP2.round(4).to_string(index=False))
# regime-adjusted SPX 12M: base-rate (midterm) + regime effect measured on the bigger sample (CAPE top quartile, Fed hiking), additive, then scenario set
eff_cape = SP2.iloc[1].mean_yes - SP2.iloc[1].mean_no; eff_fed = SP2.iloc[0].mean_yes - SP2.iloc[0].mean_no
base_mid = R['12M'].mean(); adj = base_mid + eff_cape + eff_fed
print(f'\nRegime effects (all-Nov sample): CAPE top quartile {eff_cape:+.4f}, Fed hiking {eff_fed:+.4f} -> midterm base {base_mid:+.4f} -> additive regime-adjusted mean {adj:+.4f}; kernel 12M mean {K["12M"]["k_mean"]:+.4f}, median {K["12M"]["k_median"]:+.4f}')
json.dump(dict(kernel=K, lofo=lofo, eff_cape=eff_cape, eff_fed=eff_fed, adj_mean=adj, neff=neff, today=today), open(OUT / 'm5_regime.json', 'w'), default=float)
