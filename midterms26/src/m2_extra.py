"""M2 add-ons: NDX/RUT/SOX event studies, second-half decay, cycle overlay, midterm-year drawdowns, 2026 placement,
outcome buckets (Table 1/4 inputs), realised 1D/3D after midterms (M7 input)."""
import pandas as pd, numpy as np
from common import *
from m2_base_rate import event_table, summarise, tests, verdict
OUT = ROOT / 'out'; pd.set_option('display.width', 230); pd.set_option('display.max_columns', 40)
f4 = lambda v: f'{v:+.4f}'
# ---- 1. other indices on own coverage
t2 = []
for a in ['SPX', 'NDX', 'RUT', 'SOX']:
    ev = event_table(a, 'eday'); ev.to_csv(OUT / f'm2_events_{a}_eday.csv', index=False)
    sm = summarise(ev); ts = {r['window']: r for r in tests(a, ev)}
    for w in ['1D', '1W', '1M', '3M', '6M', '12M']:
        if w not in sm.index: continue
        r = ts[w]; m = sm.loc[w]
        t2.append(dict(index=a, window=w, n=int(m.n), years=f"{ev.year.min()}-{ev.year.max()}", mean=m['mean'], median=m['median'], hit=m.hit, min=m['min'],
                       worst_maxdd=ev[ev.window == w].maxdd.min(), uncond_mean=r['all_mean'], excess=r['excess_a'], p_all=r['p_a'],
                       same_date_nonmid=r['non_mean'], excess_b=r['excess_b'], p_samedate=r['p_b'],
                       verdict=verdict(max(r['p_a'], r['p_b']), m.hit)))
T2 = pd.DataFrame(t2); T2.to_csv(OUT / 'table2_base_rate.csv', index=False)
print('TABLE 2 inputs (price return; T0 = election-day close; p one-sided; verdict on the weaker of the two controls)')
print(T2.to_string(index=False, float_format=f4))
# ---- 2. second-half decay: return 6M->12M vs unconditional 6M drift
s = load('SPX'); ev = pd.read_csv(OUT / 'm2_events_SPX_eday.csv', parse_dates=['t0', 'end'])
w6 = ev[ev.window == '6M'].set_index('year'); w12 = ev[ev.window == '12M'].set_index('year')
h2 = (1 + w12.ret) / (1 + w6.ret) - 1
all6 = fwd_all(s, '6M', '1950-01-01', '2025-12-31')
print(f'\nSecond half (T0+6M -> T0+12M), SPX: mean {h2.mean():+.4f} median {h2.median():+.4f} hit {(h2 > 0).mean():.2f} min {h2.min():+.4f} (vs unconditional 6M mean {all6.mean():+.4f}, hit {(all6 > 0).mean():.2f})')
print('   by year:', h2.round(4).to_dict())
# ---- 3. cycle overlay: midterm-year 30/09 -> pre-election-year 30/06 (the "sweet spot") vs same window in other cycle years
def seg(y, a=(9, 30), b=(6, 30)):
    t0 = s.index[s.index <= pd.Timestamp(y, *a)][-1]; t1 = s.index[s.index <= pd.Timestamp(y + 1, *b)][-1]
    return s[t1] / s[t0] - 1
sw = pd.Series({y: seg(y) for y in range(1950, 2026)})
grp = sw.groupby(sw.index % 4).agg(['mean', 'median', 'count', lambda z: (z > 0).mean(), 'min'])
grp.index = [{0: 'Y4 election', 1: 'Y1 post-elec', 2: 'Y2 midterm', 3: 'Y3 pre-elec'}[i] for i in grp.index]; grp.columns = ['mean', 'median', 'n', 'hit', 'min']
print('\nQ4(Y) -> Q2(Y+1) [30/09 -> 30/06], SPX price, by cycle year of the start:'); print(grp.to_string(float_format=f4))
# ---- 4. midterm-year drawdown (peak-to-trough, 1 Jan -> election day) + 2026 placement
def ytd_dd(x, y, stop):
    seg_ = x[(x.index >= pd.Timestamp(y, 1, 1)) & (x.index <= stop)]
    if len(seg_) < 50: return np.nan, None, None
    dd = seg_ / seg_.cummax() - 1; tr = dd.idxmin(); pk = seg_[:tr].idxmax()
    return dd.min(), pk, tr
rows = []
for a in ['SPX', 'SPXEW', 'RSP', 'NDX', 'RUT', 'SOX']:
    x = load(a)
    for y in list(MIDTERMS) + [2026]:
        stop = MIDTERMS.get(y, pd.Timestamp('2026-10-30'))
        d, pk, tr = ytd_dd(x, y, stop)
        if not np.isnan(d): rows.append(dict(index=a, year=y, maxdd_ytd_to_eday=d, peak=pk.date(), trough=tr.date(),
                                            aug_oct_dd=ytd_dd(x[x.index >= pd.Timestamp(y, 8, 1)], y, pd.Timestamp(y, 10, 31))[0]))
DD = pd.DataFrame(rows); DD.to_csv(OUT / 'm2_midterm_year_drawdowns.csv', index=False)
for a in ['SPX', 'RSP', 'SPXEW', 'SOX', 'RUT', 'NDX']:
    d = DD[DD['index'] == a]; hist = d[d.year < 2026]
    if not len(hist): continue
    now = d[d.year == 2026]
    print(f"\n{a}: midterm-year max DD (1 Jan->eday) median {hist.maxdd_ytd_to_eday.median():+.4f}, mean {hist.maxdd_ytd_to_eday.mean():+.4f}, n={len(hist)} | "
          f"Aug-Oct DD median {hist.aug_oct_dd.median():+.4f}; share of years with Aug-Oct DD <= -7%: {(hist.aug_oct_dd <= -0.07).mean():.2f} ({int((hist.aug_oct_dd <= -0.07).sum())}/{hist.aug_oct_dd.notna().sum()})"
          + (f" || 2026: YTD max DD {now.maxdd_ytd_to_eday.iloc[0]:+.4f} ({now.peak.iloc[0]} -> {now.trough.iloc[0]}), Aug-Oct DD {now.aug_oct_dd.iloc[0]:+.4f}, pct rank of 2026 YTD DD vs history {(hist.maxdd_ytd_to_eday < now.maxdd_ytd_to_eday.iloc[0]).mean():.2f}" if len(now) else ''))
sp1990 = DD[(DD['index'] == 'SPX') & (DD.year >= 1990) & (DD.year < 2026)]
print('SPX Aug-Oct DD by midterm year since 1990:', sp1990.set_index('year').aug_oct_dd.round(4).to_dict())
rsp = DD[(DD['index'].isin(['RSP'])) & (DD.year < 2026)]
print('RSP (EW proxy) Aug-Oct DD by midterm year:', rsp.set_index('year').aug_oct_dd.round(4).to_dict())
# ---- 5. outcome buckets (Table 1 / Table 4 inputs) on SPX + SOX
spx = w12.ret; spx6 = w6.ret; sox = pd.read_csv(OUT / 'm2_events_SOX_eday.csv'); sox12 = sox[sox.window == '12M'].set_index('year').ret
dd12 = w12.maxdd
def bucket(years, label):
    years = [y for y in years if y in spx.index]
    r12 = spx.loc[years]; r6 = spx6.loc[years]
    so = sox12.reindex(years).dropna()
    return dict(bucket=label, years=','.join(map(str, years)), n=len(years), spx6_mean=r6.mean(), spx6_med=r6.median(), spx6_min=r6.min(),
                spx12_mean=r12.mean(), spx12_med=r12.median(), spx12_min=r12.min(), worst_maxdd12=dd12.loc[years].min(),
                sox12=(';'.join(f'{y}:{v:+.3f}' for y, v in so.items()) or 'n/a'), tag='LOW-N' if len(years) < 5 else '')
B4 = pd.DataFrame([bucket([1950, 1962, 1966, 1978], 'S1 unified held both'), bucket([1950, 1962, 1966, 1978, 2002], 'S1+ incl. 2002 (won unified)'),
                   bucket([2010, 2018, 2022], 'S2 unified lost House'), bucket([1954, 1994, 2006], 'S3 unified lost both'),
                   bucket([1986, 2014], 'S4~ nearest: lost Senate (from split)'),
                   bucket([1958, 1970, 1974, 1990, 1998], 'Opposition Congress unchanged'), bucket([1982], 'Split unchanged'),
                   bucket(list(MIDTERMS), 'ALL midterms')])
B4.to_csv(OUT / 'table4_buckets.csv', index=False); print('\nOutcome buckets (SPX price, T0 eday):'); print(B4.to_string(index=False, float_format=f4))
from scipy.stats import kruskal
g = [spx.loc[[1950, 1962, 1966, 1978]].values, spx.loc[[2010, 2018, 2022]].values, spx.loc[[1954, 1994, 2006]].values]
print('Kruskal-Wallis S1 vs S2 vs S3 (12M):', kruskal(*g)); print('Kruskal-Wallis S1 vs S2 vs S3 (6M):', kruskal(*[spx6.loc[[1950, 1962, 1966, 1978]].values, spx6.loc[[2010, 2018, 2022]].values, spx6.loc[[1954, 1994, 2006]].values]))
rng = np.random.default_rng(7); lab = np.array([1] * 4 + [2] * 3 + [3] * 3); vals = np.r_[g[0], g[1], g[2]]
def fstat(v, l): return np.var([v[l == k].mean() for k in (1, 2, 3)])
obs = fstat(vals, lab); perm = np.array([fstat(vals, rng.permutation(lab)) for _ in range(20000)])
print(f'Permutation (between-bucket variance of 12M means) p = {(np.sum(perm >= obs) + 1) / 20001:.3f}')
pp = CLASS.pres_party.reindex(spx.index)
print('President party split 12M:', {k: (round(v.mean(), 4), round(v.median(), 4), len(v)) for k, v in spx.groupby(pp)})
# ---- 6. realised 1D/3D after midterms 1990-2022 (abs moves) for M7 event-vol comparison
rr = []
for a in ['SPX', 'NDX', 'RUT', 'SOX', 'VIX']:
    x = load(a)
    for y, ed in MIDTERMS.items():
        if y < 1990: continue
        t0 = t0_date(x, ed, 'eday')
        if t0 is None: continue
        i = x.index.get_loc(t0)
        if i + 3 >= len(x): continue
        rr.append(dict(index=a, year=y, r1d=x.iloc[i + 1] / x.iloc[i] - 1, r3d=x.iloc[i + 3] / x.iloc[i] - 1,
                       r1d_chg=x.iloc[i + 1] - x.iloc[i] if a == 'VIX' else np.nan, lvl=x.iloc[i]))
RR = pd.DataFrame(rr); RR.to_csv(OUT / 'm7_realised_post_midterm.csv', index=False)
piv = RR[RR['index'] != 'VIX'].pivot_table(index='year', columns='index', values=['r1d', 'r3d']); print('\nRealised post-midterm moves (T0 eday close -> +1/+3 trading days):'); print(piv.to_string(float_format=f4))
print('Mean |1D|:', RR[RR['index'] != 'VIX'].groupby('index').r1d.apply(lambda z: z.abs().mean()).round(4).to_dict(),
      '| Mean |3D|:', RR[RR['index'] != 'VIX'].groupby('index').r3d.apply(lambda z: z.abs().mean()).round(4).to_dict())
v = RR[RR['index'] == 'VIX'].set_index('year'); print('VIX at T0 and 1D change (pts):', {y: (round(r.lvl, 2), round(r.r1d_chg, 2)) for y, r in v.iterrows()})
