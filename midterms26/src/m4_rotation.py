"""M4: sector / industry / factor rotation after midterms on Ken French daily TOTAL returns (CRSP, VW), 1950-2022 and 1982-2022.
Relative = arithmetic excess over the CRSP VW market. Also: MS reconciliation, hardest-hit-bounce test, energy check, 2026 starting points."""
import sys, numpy as np, pandas as pd
from scipy.stats import spearmanr
sys.path.insert(0, 'src'); from common import load, MIDTERMS
from ff_data import industries_vw, factors3, factors5, mom, strev
OUT = __import__('pathlib').Path('out'); rng = np.random.default_rng(42); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); pd.set_option('display.max_rows', 200)
ind = industries_vw(); f3 = factors3(); f5 = factors5(); um = mom(); sr = strev()
mkt = (f3['Mkt-RF'] + f3['RF']).rename('MKT')
G = {  # industry groups of the playbook universe (FF49 proxies)
 'Semis & equip [Chips]': ['Chips'], 'Software [Softw]': ['Softw'], 'Tech hardware [Hardw]': ['Hardw'], 'Banks': ['Banks'], 'Diversified fin [Fin]': ['Fin'],
 'Pharma & biotech [Drugs]': ['Drugs'], 'Health services [Hlth] (managed-care proxy)': ['Hlth'], 'Aero & defense [Aero+Guns]': ['Aero', 'Guns'],
 'Construction [Cnstr] (homebuilder proxy)': ['Cnstr'], 'Utilities [Util]': ['Util'], 'Energy [Oil]': ['Oil'], 'Real estate [RlEst] (REIT proxy, weak)': ['RlEst'],
 # GICS-like sector composites (equal-weight of member industries)
 'S: Energy': ['Oil', 'Coal'], 'S: Materials': ['Chems', 'Steel', 'Mines', 'Gold', 'Paper', 'Boxes', 'BldMt'], 'S: Industrials': ['Mach', 'ElcEq', 'Aero', 'Guns', 'Ships', 'Trans', 'FabPr', 'Cnstr', 'Whlsl'],
 'S: Cons Disc': ['Autos', 'Rtail', 'Meals', 'Clths', 'Txtls', 'Toys', 'PerSv', 'Rubbr'], 'S: Cons Staples': ['Food', 'Soda', 'Beer', 'Smoke', 'Agric', 'Hshld'],
 'S: Health Care': ['Hlth', 'MedEq', 'Drugs'], 'S: Financials': ['Banks', 'Insur', 'Fin'], 'S: Info Tech': ['Chips', 'Hardw', 'Softw', 'LabEq'],
 'S: Comm Services': ['Telcm', 'Books', 'Fun'], 'S: Utilities': ['Util'], 'S: Real Estate': ['RlEst']}
series = {k: ind[v].mean(axis=1, skipna=True) for k, v in G.items()}
CYC = ['Autos', 'Rtail', 'Meals', 'Clths', 'Mach', 'ElcEq', 'Trans', 'Chips', 'Hardw', 'Steel', 'Chems', 'Banks', 'Fin', 'Cnstr', 'BldMt', 'Mines']
DEF = ['Food', 'Soda', 'Beer', 'Smoke', 'Hshld', 'Hlth', 'MedEq', 'Drugs', 'Util', 'Telcm']
FAC = {'F: Growth-Value (-HML)': -f3['HML'], 'F: Small-Large (SMB)': f3['SMB'], 'F: LowQ-HighQ (-RMW)': -f5['RMW'], 'F: Momentum (UMD)': um['Mom'],
       'F: ST reversal': sr['ST_Rev'], 'F: Cyclicals-Defensives': ind[CYC].mean(axis=1) - ind[DEF].mean(axis=1)}
idx = mkt.index
def t0(ed): return idx[idx <= ed][-1]
def end(d, months): tg = d + pd.DateOffset(months=months); return idx[idx <= tg][-1] if tg <= idx[-1] else None
def comp(r, a, b): x = r[(r.index > a) & (r.index <= b)].dropna(); return np.prod(1 + x) - 1 if len(x) > 20 else np.nan
def path_dd(r, a, b): x = (1 + r[(r.index > a) & (r.index <= b)].fillna(0)).cumprod(); return min(x.min() - 1, 0)
rows = []
for y, ed in MIDTERMS.items():
    a = t0(ed); b6, b12 = end(a, 6), end(a, 12); p6 = idx[idx <= a - pd.DateOffset(months=6)][-1]
    m6, m12, mp = comp(mkt, a, b6), comp(mkt, a, b12), comp(mkt, p6, a)
    for k, r in list(series.items()) + list(FAC.items()):
        isf = k.startswith('F:')
        if r[(r.index > a) & (r.index <= b12)].notna().sum() < 100: continue
        a6, a12, pre = comp(r, a, b6), comp(r, a, b12), comp(r, p6, a)
        rel6, rel12, prerel = (a6, a12, pre) if isf else (a6 - m6, a12 - m12, pre - mp)
        # pre-election relative drawdown (relative index vs its max over prior 6M)
        rr = (r - (0 if isf else mkt))[(r.index > p6) & (r.index <= a)].fillna(0); ri = (1 + rr).cumprod(); prerdd = ri.iloc[-1] / ri.max() - 1
        rows.append(dict(year=y, name=k, abs6=a6, abs12=a12, rel6=rel6, rel12=rel12, pre_rel6=prerel, pre_rel_dd=prerdd, maxdd12=path_dd(r, a, b12)))
E = pd.DataFrame(rows); E.to_csv(OUT / 'm4_events.csv', index=False)
# unconditional relative 12M from every start day 1950-2025 (for permutation p)
def fwd12(r, rel=True):
    lr = np.log1p((r - (mkt if rel else 0)).fillna(0)) if rel else np.log1p(r.fillna(0))
    c = lr.cumsum(); out = {}
    ds = c.index[(c.index >= '1950-01-01') & (c.index <= '2025-09-30')]
    pos_end = np.searchsorted(c.index.values, (ds + pd.DateOffset(months=12)).values, side='right') - 1
    return pd.Series(np.expm1(c.values[pos_end] - c.loc[ds].values), index=ds)
def summarise(E, years, label):
    out = []
    for k, g in E[E.year.isin(years)].groupby('name', sort=False):
        x = g.rel12.dropna(); n = len(x)
        if n == 0: continue
        r = series.get(k, FAC.get(k)); isf = k.startswith('F:')
        u = fwd12(r, rel=not isf) if not isf else pd.Series(np.expm1(np.log1p(r.fillna(0)).cumsum().pipe(lambda c: c.shift(-252) - c)).dropna().loc['1950':'2025-09'])
        draws = np.array([rng.choice(u.values, n, replace=False).mean() for _ in range(3000)])
        p_hi = (np.sum(draws >= x.mean()) + 1) / 3001; p_lo = (np.sum(draws <= x.mean()) + 1) / 3001
        top = x.sort_values(ascending=False)
        out.append(dict(name=k, n=n, abs12_med=g.abs12.median(), rel6_mean=g.rel6.mean(), rel12_mean=x.mean(), rel12_med=x.median(), hit=(x > 0).mean(),
                        worst_rel=x.min(), ex_top_mean=top.iloc[1:].mean() if n > 2 else np.nan, worst_dd12=g.maxdd12.min(), uncond_rel12=u.mean(),
                        p=min(p_hi, p_lo) * 2, tags=('LOW-N ' if n < 5 else '') + ('NOT A PATTERN' if 0.3 < (x > 0).mean() < 0.7 else ''), sample=label))
    return pd.DataFrame(out)
S19 = summarise(E, list(MIDTERMS), '1950-2022'); S11 = summarise(E, [y for y in MIDTERMS if y >= 1982], '1982-2022')
S = pd.concat([S19, S11]); S.to_csv(OUT / 'table5_rotation.csv', index=False)
cols = ['name', 'n', 'abs12_med', 'rel6_mean', 'rel12_mean', 'rel12_med', 'hit', 'worst_rel', 'ex_top_mean', 'worst_dd12', 'uncond_rel12', 'p', 'tags']
f = lambda v: f'{v:+.3f}'
print('TABLE 5 inputs — 1982-2022 (n<=11, MS-comparable), CRSP VW TOTAL return, rel = excess over CRSP VW market, p = two-sided random-start-date permutation vs unconditional rel 12M')
print(S11[cols].to_string(index=False, float_format=f))
print('\n1950-2022 (n<=19):'); print(S19[cols].to_string(index=False, float_format=f))
# MS reconciliation: which convention fits MS numbers?
MS = {'Semis & equip [Chips]': (21.7, 39.5), 'Software [Softw]': (11.3, 17.4), 'Tech hardware [Hardw]': (10.9, 16.8), 'Diversified fin [Fin]': (6.2, 5.7),
      'Utilities [Util]': (-7.2, -7.3), 'Real estate [RlEst] (REIT proxy, weak)': (-4.2, -8.1), 'Banks': (-8.3, -8.8), 'Energy [Oil]': (-8.2, -10.7)}
g11 = E[E.year >= 1982].groupby('name')[['abs6', 'abs12', 'rel6', 'rel12']].mean() * 100
rec = pd.DataFrame({k: dict(MS6=v[0], MS12=v[1], abs6=g11.loc[k, 'abs6'], abs12=g11.loc[k, 'abs12'], rel6=g11.loc[k, 'rel6'], rel12=g11.loc[k, 'rel12']) for k, v in MS.items()}).T
mae_abs = (rec[['abs6', 'abs12']].values - rec[['MS6', 'MS12']].values).__abs__().mean(); mae_rel = (rec[['rel6', 'rel12']].values - rec[['MS6', 'MS12']].values).__abs__().mean()
sign_rel = (np.sign(rec[['rel6', 'rel12']].values) == np.sign(rec[['MS6', 'MS12']].values)).mean(); sign_abs = (np.sign(rec[['abs6', 'abs12']].values) == np.sign(rec[['MS6', 'MS12']].values)).mean()
print('\nMS reconciliation 1982-2022 (means, %):'); print(rec.round(1).to_string())
print(f'Mean abs error vs MS: absolute {mae_abs:.1f}pp | relative {mae_rel:.1f}pp ; sign agreement: absolute {sign_abs:.0%} | relative {sign_rel:.0%}')
# hardest-hit bounce: industries only (49), pooled + per-midterm cross-section
H = []
for y, ed in MIDTERMS.items():
    a = t0(ed); b12 = end(a, 12); p6 = idx[idx <= a - pd.DateOffset(months=6)][-1]
    m12, mp = comp(mkt, a, b12), comp(mkt, p6, a)
    for c in ind.columns:
        r = ind[c]
        if r[(r.index > p6) & (r.index <= b12)].isna().mean() > 0.05: continue
        rr = (r - mkt)[(r.index > p6) & (r.index <= a)].fillna(0); ri = (1 + rr).cumprod()
        H.append(dict(year=y, ind=c, pre_rel6=comp(r, p6, a) - mp, pre_rel_dd=ri.iloc[-1] / ri.max() - 1, post_rel12=comp(r, a, b12) - m12))
H = pd.DataFrame(H).dropna()
for pre in ['pre_rel6', 'pre_rel_dd']:
    rho, p = spearmanr(H[pre], H.post_rel12); per = H.groupby('year').apply(lambda g: spearmanr(g[pre], g.post_rel12)[0])
    print(f'Hardest-hit bounce ({pre}): pooled Spearman {rho:+.3f} (p={p:.3f}, n={len(H)}) | per-midterm mean {per.mean():+.3f}, t={per.mean() / per.std() * np.sqrt(len(per)):.2f}, positive in {(per > 0).sum()}/{len(per)}')
q = H.groupby('year').apply(lambda g: g.assign(qd=pd.qcut(g.pre_rel6, 5, labels=False)))
qq = q.groupby('qd').post_rel12.agg(['mean', 'median', 'count']); qq.index = ['Q1 worst pre-6M', 'Q2', 'Q3', 'Q4', 'Q5 best pre-6M']; print('Post-12M relative by pre-6M relative quintile (within each midterm):'); print(qq.to_string(float_format=f))
# energy check: WTI 6M change into the election (FRED WTISPLC Apr->Oct)
w = pd.read_csv('data/raw/fred/WTISPLC.csv'); w.columns = ['d', 'v']; w['d'] = pd.to_datetime(w.d); w = w.set_index('d').v.astype(float)
oil = pd.Series({y: w[:f'{y}-10-01'].iloc[-1] / w[:f'{y}-04-01'].iloc[-1] - 1 for y in MIDTERMS})
en = E[E.name == 'Energy [Oil]'].set_index('year')
EC = pd.DataFrame({'wti_6m_into_eday': oil, 'energy_pre_rel6': en.pre_rel6, 'energy_rel6': en.rel6, 'energy_rel12': en.rel12})
print('\nEnergy check (WTI Apr->Oct of midterm year vs Oil-industry relative returns):'); print(EC.round(3).to_string())
up = EC[EC.wti_6m_into_eday >= 0.15]; dn = EC[EC.wti_6m_into_eday < 0.15]
print(f"Oil up >=15% into vote: years {list(up.index)} -> energy rel12 mean {up.energy_rel12.mean():+.3f}, median {up.energy_rel12.median():+.3f} (n={len(up)}) | others mean {dn.energy_rel12.mean():+.3f} (n={len(dn)})")
lead = EC[EC.energy_pre_rel6 >= 0.05]; print(f"Energy leading into vote (pre-6M rel >= +5pp): years {list(lead.index)} -> rel12 mean {lead.energy_rel12.mean():+.3f}, hit {(lead.energy_rel12 > 0).mean():.2f} (n={len(lead)})")
print('Spearman(energy pre_rel6, energy rel12):', round(spearmanr(EC.energy_pre_rel6, EC.energy_rel12)[0], 3))
# 2026 starting points (ETF proxies vs SPX, through 30/10/2026)
spx = load('SPX'); P = {}
for nm, a in [('Semis SMH', 'SMH'), ('Software IGV', 'IGV'), ('Tech XLK', 'XLK'), ('Banks KRE', 'KRE'), ('Financials XLF', 'XLF'), ('Health XLV', 'XLV'), ('Managed care IHF', 'IHF'), ('Biotech IBB', 'IBB'), ('Aero/def ITA', 'ITA'), ('Homebuilders XHB', 'XHB'), ('Utilities XLU', 'XLU'), ('Energy XLE', 'XLE'), ('E&P XOP', 'XOP'), ('Oil svcs OIH', 'OIH'), ('REITs XLRE', 'XLRE'), ('Grid GRID', 'GRID'), ('Small IWM', 'IWM'), ('EW RSP', 'RSP'), ('Materials XLB', 'XLB'), ('Industrials XLI', 'XLI'), ('Discretionary XLY', 'XLY'), ('Staples XLP', 'XLP'), ('Comm XLC', 'XLC')]:
    s = load(a); last = s.index[-1]; b = s[s.index <= last - pd.DateOffset(months=6)].iloc[-1]; bs = spx[spx.index <= last - pd.DateOffset(months=6)].iloc[-1]
    rel = (s / s.reindex(spx.index).ffill().pipe(lambda z: z) if False else None)
    rr = (s / spx).dropna(); rr6 = rr[rr.index > last - pd.DateOffset(months=6)]
    P[nm] = dict(ytd=s.iloc[-1] / s[:'2025-12-31'].iloc[-1] - 1, rel_ytd=(s.iloc[-1] / s[:'2025-12-31'].iloc[-1]) - (spx.iloc[-1] / spx[:'2025-12-31'].iloc[-1]),
                 pre_rel6=(s.iloc[-1] / b) - (spx.iloc[-1] / bs), pre_rel_dd=rr6.iloc[-1] / rr6.max() - 1, off_high=s.iloc[-1] / s[s.index > last - pd.Timedelta(days=365)].max() - 1)
P = pd.DataFrame(P).T.sort_values('pre_rel6'); P.to_csv(OUT / 'm4_2026_starting_points.csv'); print('\n2026 starting points (price, vs SPX, to 30/10/2026):'); print(P.to_string(float_format=f))
