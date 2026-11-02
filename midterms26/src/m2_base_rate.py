"""M2 — base rate rebuilt in code: SPX (+NDX/RUT/SOX on own coverage) after every midterm since 1950."""
import sys, pandas as pd, numpy as np
from common import *
rng = np.random.default_rng(20261103)
OUT = ROOT / 'out'; OUT.mkdir(exist_ok=True)
pd.set_option('display.width', 220); pd.set_option('display.max_columns', 40)
B = 20000

def event_table(alias, conv='eday', years=None):
    s = load(alias); rows = []
    for y, ed in MIDTERMS.items():
        if years and y not in years: continue
        t0 = t0_date(s, ed, conv)
        if t0 is None or t0 < s.index[0] + pd.Timedelta(days=3): continue
        for w in WINDOWS:
            st = window_stats(s, t0, w)
            if st: rows.append(dict(year=y, window=w, **st))
    return pd.DataFrame(rows)

def summarise(ev):
    g = ev.groupby('window', sort=False)
    out = pd.DataFrame({'n': g.ret.size(), 'mean': g.ret.mean(), 'median': g.ret.median(), 'std': g.ret.std(),
                        'min': g.ret.min(), 'max': g.ret.max(), 'hit': g.ret.apply(lambda x: (x > 0).mean()),
                        'worst_maxdd': g.maxdd.min(), 'med_maxdd': g.maxdd.median(), 'mean_maxrun': g.maxrun.mean()})
    return out.reindex([w for w in WINDOWS if w in out.index])

def november_starts(s, years):
    out = {}
    for y in years:
        t0 = t0_date(s, election_day(y), 'eday')
        if t0 is not None: out[y] = t0
    return out

def tests(alias, ev, ctrl_start='1950-01-01', ctrl_stop='2025-12-31'):
    s = load(alias); res = []
    yrs = range(max(1950, s.index[0].year + (1 if s.index[0].month > 10 else 0)), 2026)
    nov = november_starts(s, yrs)
    for w in WINDOWS:
        x = ev.loc[ev.window == w, 'ret'].values; n = len(x)
        if n == 0: continue
        allr = fwd_all(s, w, max(ctrl_start, str(s.index[0].date())), ctrl_stop)
        # (a) random-date permutation: mean of n random start days vs observed
        draws = np.array([rng.choice(allr.values, n, replace=False).mean() for _ in range(B // 4)])
        p_a = (np.sum(draws >= x.mean()) + 1) / (len(draws) + 1)
        boot_a = rng.choice(x, (B, n)).mean(1) - allr.mean()  # benchmark mean treated as known (long-run drift)
        # (b) same calendar start (election-day-equivalent close), non-midterm years
        cyc = {}
        for y, t0 in nov.items():
            st = window_stats(s, t0, w)
            if st: cyc[y] = st['ret']
        cyc = pd.Series(cyc); mid = cyc[cyc.index.isin(MIDTERMS.keys())]; non = cyc[~cyc.index.isin(MIDTERMS.keys())]
        obs = mid.mean() - non.mean(); pool = cyc.values; k = len(mid)
        perm = np.array([(lambda p: p[:k].mean() - p[k:].mean())(rng.permutation(pool)) for _ in range(B // 4)])
        p_b = (np.sum(perm >= obs) + 1) / (len(perm) + 1)
        boot_b = rng.choice(mid.values, (B, k)).mean(1) - rng.choice(non.values, (B, len(non))).mean(1)
        # (c) presidential-cycle year means (same calendar start)
        pos = {0: 'Y4 election', 1: 'Y1 post-elec', 2: 'Y2 midterm', 3: 'Y3 pre-elec'}
        cy = cyc.groupby(cyc.index % 4).agg(['mean', 'median', 'count', lambda z: (z > 0).mean()])
        cy.index = [pos[i] for i in cy.index]; cy.columns = ['mean', 'median', 'n', 'hit']
        res.append(dict(window=w, n=n, mid_mean=x.mean(), mid_median=np.median(x), mid_hit=(x > 0).mean(),
                        all_mean=allr.mean(), all_median=allr.median(), all_hit=(allr > 0).mean(), all_n=len(allr),
                        excess_a=x.mean() - allr.mean(), ci_a=np.percentile(boot_a, [2.5, 97.5]), p_a=p_a,
                        non_mean=non.mean(), non_hit=(non > 0).mean(), non_n=len(non), excess_b=obs,
                        ci_b=np.percentile(boot_b, [2.5, 97.5]), p_b=p_b, cycle=cy))
    return res

def verdict(p, hit):
    v = 'REAL' if p <= 0.05 else ('WEAK' if p <= 0.10 else 'NOT DISTINGUISHABLE FROM DRIFT')
    return v + ('' if hit >= 0.70 else ' | NOT A PATTERN (hit<70%)')

if __name__ == '__main__':
    aliases = sys.argv[1:] or ['SPX']
    for alias in aliases:
        s = load(alias)
        print(f'\n================ {alias}  (Yahoo daily close, PRICE RETURN; coverage {s.index[0].date()} .. {s.index[-1].date()}) ================')
        convs = {}
        for conv in ['eday', 'fri', 'oct31']:
            ev = event_table(alias, conv); convs[conv] = ev
            ev.to_csv(OUT / f'm2_events_{alias}_{conv}.csv', index=False)
        ev = convs['eday']
        print('T0 dates (eday convention):', {int(y): str(d.date()) for y, d in ev.groupby('year').t0.first().items()})
        print('\n-- Event study, T0 = election-day close (prior close where the exchange shut on election day) --')
        print(summarise(ev).to_string(float_format=lambda v: f'{v:8.4f}'))
        for conv in ['fri', 'oct31']:
            sm = summarise(convs[conv])
            print(f'\n-- Robustness T0={conv}: mean/median/hit/min --')
            print(sm[['n', 'mean', 'median', 'hit', 'min', 'worst_maxdd']].to_string(float_format=lambda v: f'{v:8.4f}'))
        print('\n-- Controls, excess return, bootstrap 95% CI, one-sided permutation p --')
        for r in tests(alias, ev):
            print(f"{r['window']:>4} n={r['n']:>2} mid mean {r['mid_mean']:+.4f} med {r['mid_median']:+.4f} hit {r['mid_hit']:.2f} | "
                  f"(a) all-days 1950-2025 mean {r['all_mean']:+.4f} hit {r['all_hit']:.2f} -> excess {r['excess_a']:+.4f} CI [{r['ci_a'][0]:+.4f},{r['ci_a'][1]:+.4f}] p={r['p_a']:.3f} {verdict(r['p_a'], r['mid_hit'])} | "
                  f"(b) same-date non-midterm n={r['non_n']} mean {r['non_mean']:+.4f} hit {r['non_hit']:.2f} -> excess {r['excess_b']:+.4f} CI [{r['ci_b'][0]:+.4f},{r['ci_b'][1]:+.4f}] p={r['p_b']:.3f} {verdict(r['p_b'], r['mid_hit'])}")
            if r['window'] in ('6M', '12M'):
                print('      (c) cycle-year, same Nov start:', r['cycle'].round(4).to_dict('index'))
        # per-year table for 6M/12M + path stats
        wide = ev.pivot(index='year', columns='window', values='ret')[[w for w in WINDOWS if w in ev.window.unique()]]
        dd12 = ev[ev.window == '12M'].set_index('year')[['maxdd', 'maxdd_date', 'maxrun', 'rec_date', 'rec_tdays']]
        per = wide.join(dd12)
        per.to_csv(OUT / f'm2_peryear_{alias}.csv')
        print('\n-- Per midterm (eday T0) --'); print(per.to_string(float_format=lambda v: f'{v:+.4f}'))
        for w in ['6M', '12M']:
            x = ev[ev.window == w].set_index('year').ret
            if len(x) < 3: continue
            loo = {y: x.drop(y).mean() for y in x.index}
            top = x.sort_values(ascending=False)
            print(f'\n-- Outlier dependence {w}: mean {x.mean():+.4f} | ex top2 {top.iloc[2:].mean():+.4f} | top3 share of total {top.iloc[:3].sum() / x.sum():.2%} '
                  f'| LOO range [{min(loo.values()):+.4f}, {max(loo.values()):+.4f}] | top3 {dict(top.iloc[:3].round(4))} | bottom3 {dict(top.iloc[-3:].round(4))}')
