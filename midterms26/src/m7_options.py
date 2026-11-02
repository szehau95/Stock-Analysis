"""M7 — implied moves from CBOE delayed chains (Tier 1 exchange data). Stores compact chains; prints ATM straddles,
event-day forward implied move (SPX/NDX/RUT/SOX), election-week (06/11) straddles and 3M ATM IV for T1/T2 underlyings."""
import json, gzip, re, sys, time, urllib.request, pathlib, datetime as dt
import numpy as np, pandas as pd
RAW = pathlib.Path('data/raw/cboe'); RAW.mkdir(parents=True, exist_ok=True)
OUT = pathlib.Path('out')
SYMS = sys.argv[1:] or ['_SPX', '_NDX', '_RUT', '_SOX', 'SPY', 'QQQ', 'IWM', 'SMH', 'SOXX', 'SOXL', 'AMAT', 'ARM', 'MU', 'IREN', 'INTC', 'AVGO', 'NVDA',
                        'SNDK', 'SKHY', 'MRVL', 'GOOGL', 'AMZN', 'ASML', 'AMD', 'WDC', 'QCOM', 'MSFT', 'XLE', 'XLF', 'XLU', 'KRE', 'TSM']
pat = re.compile(r'^([A-Z]+?)(\d{6})([CP])(\d{8})$')
NOW = pd.Timestamp.utcnow().tz_localize(None)
GTH = {'_SPX', '_VIX', '_XSP'}  # Cboe global-trading-hours products quote live on Monday; everything else = Friday 30/10 close
FRI_CLOSE = pd.Timestamp('2026-10-30 20:00')  # 16:00 EDT
def tyears(exp, sym='_SPX'):  # time from quote time to 16:00 ET (21:00 UTC, EST) on expiry date, in years (calendar)
    ref = NOW if sym in GTH else FRI_CLOSE
    return max((pd.Timestamp(exp) + pd.Timedelta(hours=21) - ref).total_seconds(), 3600) / (365.0 * 86400)
rows_atm, chains = [], {}
for sym in SYMS:
    url = f'https://cdn.cboe.com/api/global/delayed_quotes/options/{sym}.json'
    js = None
    for a in range(3):
        try:
            js = json.load(urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'}), timeout=90)); break
        except Exception as e:
            err = e; time.sleep(3)
    if js is None:
        print(f'{sym}: FAILED {err}'); continue
    d = js['data']; spot = d.get('current_price') or d.get('close'); ts = js.get('timestamp')
    recs = []
    for o in d['options']:
        m = pat.match(o['option'])
        if not m: continue
        root, ymd, cp, k = m.groups(); k = int(k) / 1000
        if not (0.4 * spot <= k <= 1.8 * spot): continue
        recs.append((root, pd.Timestamp('20' + ymd), cp, k, o.get('bid'), o.get('ask'), o.get('iv'), o.get('delta'), o.get('open_interest'), o.get('volume')))
    ch = pd.DataFrame(recs, columns=['root', 'exp', 'cp', 'k', 'bid', 'ask', 'iv', 'delta', 'oi', 'vol'])
    ch['mid'] = np.where((ch.bid > 0) & (ch.ask > 0), (ch.bid + ch.ask) / 2, np.nan)
    ch.to_csv(RAW / f'{sym.strip("_")}.csv.gz', index=False, compression='gzip')
    chains[sym] = (spot, ts, ch)
    for exp, g in ch.groupby('exp'):
        if exp < pd.Timestamp('2026-11-02') or exp > pd.Timestamp('2027-03-31'): continue
        roots = g.root.value_counts().index.tolist()
        g = g[g.root == roots[0]] if len(roots) > 1 and (g.root == roots[0]).sum() > 20 else g
        c = g[g.cp == 'C'].set_index('k'); p = g[g.cp == 'P'].set_index('k')
        ks = c.index.intersection(p.index)
        ks = [k for k in ks if pd.notna(c.loc[k, 'mid']) and pd.notna(p.loc[k, 'mid'])] if len(ks) else []
        if not ks: continue
        kk = min(ks, key=lambda k: abs(c.loc[k, 'mid'] - p.loc[k, 'mid']) if abs(k / spot - 1) < 0.1 else 1e18)
        cm, pm = c.loc[kk, 'mid'], p.loc[kk, 'mid']
        fwd = kk + cm - pm; strad = cm + pm; T = tyears(exp, sym)
        ivs = [v for v in (c.loc[kk, 'iv'], p.loc[kk, 'iv']) if v and v > 0.01]
        iv_atm = float(np.mean(ivs)) if ivs else np.nan
        iv_from_strad = strad / fwd / np.sqrt(2 * T / np.pi)  # Brenner-Subrahmanyam inversion
        rows_atm.append(dict(sym=sym.strip('_'), ts=ts, spot=spot, exp=exp.date(), T_days=T * 365, k_atm=kk, fwd=fwd, straddle=strad,
                             move_pct=strad / fwd, iv_cboe=iv_atm, iv_strad=iv_from_strad, spread_pct=((c.loc[kk, 'ask'] - c.loc[kk, 'bid']) + (p.loc[kk, 'ask'] - p.loc[kk, 'bid'])) / strad))
    print(f'{sym:>6} spot {spot:>10.2f} ts {ts} | {ch.exp.nunique()} expiries, {len(ch)} contracts kept')
A = pd.DataFrame(rows_atm); A.to_csv(OUT / 'm7_atm_by_expiry.csv', index=False)
pd.set_option('display.width', 230); pd.set_option('display.max_rows', 500)
# event-day forward implied move (03/11 -> 04/11 expiry) and election-week move (to 06/11)
ev = []
for sym, g in A.groupby('sym'):
    g = g.set_index('exp'); idx = [pd.Timestamp(x) for x in g.index]
    def pick(date):
        dd = [x for x in g.index if pd.Timestamp(x) == pd.Timestamp(date)]
        return g.loc[dd[0]] if dd else None
    r3, r4, r6 = pick('2026-11-03'), pick('2026-11-04'), pick('2026-11-06')
    if r3 is None: r3 = pick('2026-11-02')  # Mon/Wed/Fri listers: Mon->Wed spans Tue+Wed sessions; one normal day removed below
    gap_days = 0 if (r3 is not None and str(r3.name) == '2026-11-03') else 1
    first_after = min([x for x in g.index if pd.Timestamp(x) >= pd.Timestamp('2026-11-04')], default=None)
    rf = g.loc[first_after] if first_after is not None else None
    # 3M ATM IV: interpolate total variance at 91 calendar days
    gg = g[g.iv_strad.notna()].copy(); gg['tv'] = gg.iv_strad ** 2 * gg.T_days / 365
    iv3m = np.nan
    if len(gg) >= 2:
        x = gg.T_days.values; y = gg.tv.values; o = np.argsort(x); x, y = x[o], y[o]
        if x.min() <= 91 <= x.max(): iv3m = float(np.sqrt(np.interp(91, x, y) / (91 / 365)))
    ev_move = np.nan; base_iv = np.nan
    if r3 is not None and r4 is not None:
        tv3 = r3.iv_strad ** 2 * r3.T_days / 365; tv4 = r4.iv_strad ** 2 * r4.T_days / 365
        later = g[[pd.Timestamp(x) >= pd.Timestamp('2026-11-13') for x in g.index]]
        base_iv = float(later.iv_strad.iloc[0]) if len(later) else np.nan
        ev_move = float(np.sqrt(max(tv4 - tv3 - gap_days * (base_iv ** 2 / 252 if base_iv == base_iv else 0), 0)))
    later = g[[pd.Timestamp(x) >= pd.Timestamp('2026-11-13') for x in g.index]]
    if len(later): base_iv = float(later.iv_strad.iloc[0])
    ev.append(dict(sym=sym, spot=g.spot.iloc[0], first_exp_after_eday=first_after, straddle_move_first=(rf.move_pct if rf is not None else np.nan),
                   iv_first=(rf.iv_strad if rf is not None else np.nan), wk_exp=('2026-11-06' if r6 is not None else None),
                   wk_move_0611=(r6.move_pct if r6 is not None else np.nan), wk_iv_0611=(r6.iv_strad if r6 is not None else np.nan),
                   event_day_1sd=ev_move, event_day_straddle_equiv=ev_move * np.sqrt(2 / np.pi) if ev_move == ev_move else np.nan,
                   normal_day_1sd=base_iv / np.sqrt(252) if base_iv == base_iv else np.nan, iv_3m=iv3m, move_3m_1sd=iv3m * 0.5 if iv3m == iv3m else np.nan,
                   ts=g.ts.iloc[0]))
E = pd.DataFrame(ev); E.to_csv(OUT / 'm7_implied_moves.csv', index=False)
print(E.to_string(index=False, float_format=lambda v: f'{v:.4f}'))
for s in ['SPX', 'NDX', 'RUT', 'SOX']:
    print(f'\n{s} ATM by expiry (first 10):'); print(A[A.sym == s].head(10)[['exp', 'T_days', 'k_atm', 'fwd', 'straddle', 'move_pct', 'iv_cboe', 'iv_strad', 'spread_pct']].to_string(index=False, float_format=lambda v: f'{v:.4f}'))
