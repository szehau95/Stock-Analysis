"""Colleague-claim test (annual SPX by government configuration) + Table 1 probabilities + Table 8 aggregation."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, 'src'); from common import load, election_day, t0_date
OUT = __import__('pathlib').Path('out'); pd.set_option('display.width', 230); pd.set_option('display.max_columns', 30)
# ---- government configuration by Congress elected at E (seated Jan E+1 .. Jan E+3): (president party, House, Senate)
G = {1926: 'RRR', 1928: 'RRR', 1930: 'RDR', 1932: 'DDD', 1934: 'DDD', 1936: 'DDD', 1938: 'DDD', 1940: 'DDD', 1942: 'DDD', 1944: 'DDD', 1946: 'DRR', 1948: 'DDD',
     1950: 'DDD', 1952: 'RRR', 1954: 'RDD', 1956: 'RDD', 1958: 'RDD', 1960: 'DDD', 1962: 'DDD', 1964: 'DDD', 1966: 'DDD', 1968: 'RDD', 1970: 'RDD', 1972: 'RDD',
     1974: 'RDD', 1976: 'DDD', 1978: 'DDD', 1980: 'RDR', 1982: 'RDR', 1984: 'RDR', 1986: 'RDD', 1988: 'RDD', 1990: 'RDD', 1992: 'DDD', 1994: 'DRR', 1996: 'DRR',
     1998: 'DRR', 2000: 'RRD', 2002: 'RRR', 2004: 'RRR', 2006: 'RDD', 2008: 'DDD', 2010: 'DRD', 2012: 'DRD', 2014: 'DRR', 2016: 'RRR', 2018: 'RDR', 2020: 'DDD',
     2022: 'DRD', 2024: 'RRR'}
def cat(c):
    p, h, s = c
    if h == s == p: return f'Unified {p}'
    if h != s: return 'Divided: split Congress'
    return f'Divided: {p} pres + {h} Congress'
spx = load('SPX'); ye = spx.groupby(spx.index.year).last(); cal = ye.pct_change().dropna()
rows = []
for y, r in cal.items():
    if y > 2025: continue
    E = y - 1 if y % 2 else y - 2
    rows.append(dict(year=y, ret=r, cfg=cat(G[E])))
C = pd.DataFrame(rows)
C['divided'] = np.where(C.cfg.str.startswith('Divided'), 'Divided (all)', 'Unified (all)')
def table(df, col):
    g = df.groupby(col).ret; return pd.DataFrame({'n': g.size(), 'mean': g.mean(), 'median': g.median(), 'hit': g.apply(lambda x: (x > 0).mean()), 'min': g.min()})
print('COLLEAGUE CLAIM TEST — SPX PRICE return (Yahoo ^GSPC; pre-1957 = S&P 90 composite); TR not available (Shiller file blocked) -> TR adds ~dividend yield to every bucket')
for start in (1928, 1950, 1980):
    d = C[C.year >= start + 1] if start == 1928 else C[C.year >= start]
    t = pd.concat([table(d, 'cfg'), table(d, 'divided')]); t.index.name = f'calendar {d.year.min()}-{d.year.max()}'
    print(t.to_string(float_format=lambda v: f'{v:+.4f}'))
# election-to-election (Nov E -> Nov E+2, annualised), config set at E
rows = []
for E in range(1928, 2025, 2):
    t0 = t0_date(spx, election_day(E)); t1 = t0_date(spx, election_day(E + 2))
    if t1 is None or election_day(E + 2) > spx.index[-1]: continue
    rows.append(dict(E=E, ret=(spx[t1] / spx[t0]) ** 0.5 - 1, cfg=cat(G[E])))
X = pd.DataFrame(rows); X['divided'] = np.where(X.cfg.str.startswith('Divided'), 'Divided (all)', 'Unified (all)')
for start in (1928, 1950, 1980):
    d = X[X.E >= start]; t = pd.concat([table(d, 'cfg'), table(d, 'divided')]); t.index.name = f'elec-to-elec {d.E.min()}-{d.E.max() + 2} (ann.)'
    print(t.to_string(float_format=lambda v: f'{v:+.4f}'))
from scipy.stats import kruskal
for nm, d in [('calendar 1950-2025', C[C.year >= 1950]), ('elec-to-elec 1950-2024', X[X.E >= 1950])]:
    grp = [g.ret.values for _, g in d.groupby('cfg') if len(g) >= 3]; print(f'Kruskal-Wallis across configurations, {nm}: p = {kruskal(*grp).pvalue:.3f}')
# ---- Table 1 probabilities: market (normalised, Kalshi+PM avg) and ours (2/3 market + 1/3 model on Senate)
k = {'S3': 0.705, 'S2': 0.245, 'S1': 0.0645, 'S4': 0.0045}; pm = {'S3': 0.715, 'S2': 0.225, 'S1': 0.055, 'S4': 0.0065}
kn = {s: v / sum(k.values()) for s, v in k.items()}; pn = {s: v / sum(pm.values()) for s, v in pm.items()}
mkt = {s: (kn[s] + pn[s]) / 2 for s in k}
pDH = mkt['S3'] + mkt['S2']; pDS_mkt = mkt['S3'] + mkt['S4']; pDS_model = 0.57
pDS_ours = 2 / 3 * pDS_mkt + 1 / 3 * pDS_model; pDS_given_RH = mkt['S4'] / (mkt['S1'] + mkt['S4'])
x = (pDS_ours - (1 - pDH) * pDS_given_RH) / pDH
ours = {'S3': pDH * x, 'S2': pDH * (1 - x), 'S1': (1 - pDH) * (1 - pDS_given_RH), 'S4': (1 - pDH) * pDS_given_RH}
print('\nScenario probs  market(norm avg Kalshi/PM):', {s: round(v, 4) for s, v in mkt.items()}, '| P(D House) mkt', round(pDH, 4), '| P(D Senate) mkt', round(pDS_mkt, 4))
print('                 ours (Senate = 2/3 market + 1/3 DDHQ 57%):', {s: round(v, 4) for s, v in ours.items()}, '| P(D Senate) ours', round(pDS_ours, 4))
json.dump({'market': mkt, 'ours': ours}, open(OUT / 'table1_probs.json', 'w'))
# ---- Table 8 aggregation by underlying
LG = pd.read_csv(OUT / 'm9_client_legs.csv'); D = pd.read_csv(OUT / 'm9_client_deals.csv').set_index('deal'); P = pd.read_csv(OUT / 'm9_personal.csv')
IN = pd.read_csv(OUT / 'm9_underlying_inputs.csv', index_col=0)
pers = {'SOX': 'SOXL', 'AMAT UW': 'AMA', 'ARM UW': 'ARMG', 'MU UW': 'MU', 'IREN': 'IREN 15JAN27 22C'}
rank = {'RED': 2, 'AMBER': 1, 'GREEN': 0}
rows = []
for t, g in LG.groupby('ticker'):
    deals = g.deal.unique(); prin = D.loc[deals, 'prin_myr'].sum()
    nxt = g.sort_values('next_obs').iloc[0]
    pr = P[P.pos == pers.get(t, '-')]
    rows.append(dict(name=t, pers_mv_myr=float(pr.mv_myr.sum()) if len(pr) else 0.0, pers_event_myr=float(pr.event_risk_myr.sum()) if len(pr) else 0.0,
                     tranches=len(deals), tranche_prin_myr=prin, worst_ki_dist=g.ki_dist.min(), below_ki=int((g.ki_dist < 0).sum()),
                     next_obs=nxt.next_obs, ko_dist_next=nxt.ko_dist, wk_move=IN.loc[t, 'wk_move'], move3m=IN.loc[t, 'iv'] * 0.5,
                     p_ki_bear_max=D.loc[deals, 'p_ki_bear'].max(), flag=max(g.flag, key=lambda f: rank[f]),
                     n_red=int((g.flag == 'RED').sum()), n_amber=int((g.flag == 'AMBER').sum())))
for nm, under in [('SOXL (SOX)', 'SOX'), ('IREN calls', 'IREN')]:
    pr = P[P.pos == pers[under]]
    rows.append(dict(name=nm, pers_mv_myr=float(pr.mv_myr.sum()), pers_event_myr=float(pr.event_risk_myr.sum()), tranches=0, tranche_prin_myr=0.0, worst_ki_dist=np.nan,
                     below_ki=0, next_obs='-', ko_dist_next=np.nan, wk_move=float(pr.wk_implied_move.iloc[0]), move3m=np.nan, p_ki_bear_max=np.nan, flag='CONCENTRATION' if pr.pct_nlv.iloc[0] > 0.1 else '-', n_red=0, n_amber=0))
T8 = pd.DataFrame(rows).sort_values(['tranche_prin_myr', 'pers_mv_myr'], ascending=False); T8.to_csv(OUT / 'table8_book_impact.csv', index=False)
print('\nTABLE 8 aggregation:'); print(T8.to_string(index=False, float_format=lambda v: f'{v:,.3f}'))
print('\nDeals by RED/AMBER (worst leg):', LG.groupby('deal').flag.apply(lambda f: max(f, key=lambda z: rank[z])).value_counts().to_dict())
print('Deals with worst-of below KI now:', int((D.worst_now < D.KI).sum()), 'principal RM', f"{D.loc[D.worst_now < D.KI, 'prin_myr'].sum():,.0f}")
urgent = D[D.days_to_fv <= 120].sort_values('days_to_fv')
print('\nFV <= 120 days:'); print(urgent[['legs', 'worst_now', 'KI', 'strike', 'fv', 'days_to_fv', 'prin_myr', 'p_ki_base', 'el_base_myr', 'lgd_base', 'clients']].to_string(float_format=lambda v: f'{v:,.3f}'))
