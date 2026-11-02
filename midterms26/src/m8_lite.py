"""M8-lite: regime-adjusted SPX 6M/12M bear/base/bull (probabilities stated), NDX/RUT/SOX beta-scaled; all arithmetic here."""
import sys, json, numpy as np, pandas as pd
sys.path.insert(0, 'src'); from common import load, MIDTERMS, election_day, t0_date, window_stats
import m5_feats as F
OUT = __import__('pathlib').Path('out'); spx = load('SPX'); M5 = json.load(open(OUT / 'm5_regime.json'))
rows = []
for y in range(1950, 2026):
    t0 = t0_date(spx, election_day(y)); s6, s12 = window_stats(spx, t0, '6M'), window_stats(spx, t0, '12M')
    f = F.feats(y); rows.append(dict(year=y, r6=s6['ret'] if s6 else np.nan, r12=s12['ret'] if s12 else np.nan, mid=int(y in MIDTERMS), cape=f['cape'], fed=f['fed_d6m']))
AN = pd.DataFrame(rows).set_index('year'); q75 = AN.cape.quantile(0.75)
out = {}
for h in ['r6', 'r12']:
    d = AN.dropna(subset=[h]); base = d.loc[d.mid == 1, h].mean(); med = d.loc[d.mid == 1, h].median()
    e_cape = d.loc[d.cape >= q75, h].mean() - d.loc[d.cape < q75, h].mean(); e_fed = d.loc[d.fed >= 0.25, h].mean() - d.loc[d.fed < 0.25, h].mean()
    adj = base + e_cape + e_fed
    tail = d.loc[d.cape >= q75, h].quantile(0.10)  # high-valuation adverse tail (all Novembers)
    P = {'bull': 0.30, 'base': 0.50, 'bear': 0.20}
    R = {'bull': med, 'base': adj, 'bear': tail}
    out[h] = dict(raw_mean=base, raw_median=med, cape_effect=e_cape, fed_effect=e_fed, base=adj, bear=tail, bull=med, probs=P, pw=sum(P[k] * R[k] for k in P),
                  n_mid=int(d.mid.sum()), n_all=len(d), n_cape_q=int((d.cape >= q75).sum()))
print('SPX regime-adjusted (price):'); print(pd.DataFrame(out).T[['raw_mean', 'raw_median', 'cape_effect', 'fed_effect', 'bear', 'base', 'bull', 'pw', 'n_mid', 'n_all', 'n_cape_q']].round(4).to_string())
# betas of NDX/RUT/SOX to SPX: 2Y weekly log returns
b = {}
for a in ['NDX', 'RUT', 'SOX']:
    w = pd.concat([np.log(load(a)).resample('W-FRI').last().diff(), np.log(spx).resample('W-FRI').last().diff()], axis=1, sort=True).dropna()[-104:]
    b[a] = float(np.cov(w.iloc[:, 0], w.iloc[:, 1])[0, 1] / w.iloc[:, 1].var())
sc = {}
for a, be in b.items():
    for h in ['r6', 'r12']:
        o = out[h]; sc[(a, h)] = dict(beta=be, bear=be * o['bear'], base=be * o['base'], bull=be * o['bull'], pw=be * o['pw'])
print('\nBeta-scaled (2Y weekly beta to SPX; linear approximation, ignores own base rates):'); print(pd.DataFrame(sc).T.round(4).to_string())
# own post-midterm base rates for reference
T2 = pd.read_csv(OUT / 'table2_base_rate.csv'); print('\nOwn post-midterm base rates (price):'); print(T2[T2.window.isin(['6M', '12M']) & T2['index'].isin(['NDX', 'RUT', 'SOX'])][['index', 'window', 'n', 'mean', 'median', 'hit', 'min', 'verdict']].round(4).to_string(index=False))
json.dump(dict(spx=out, beta_scaled={f'{k[0]}_{k[1]}': v for k, v in sc.items()}), open(OUT / 'm8_lite.json', 'w'), default=float)
