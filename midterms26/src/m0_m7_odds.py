"""M0 live baseline (universe levels / % off 52W high / 1M-3M-YTD) and M7 odds-beta (sector excess returns vs daily
changes in prediction-market Senate-control odds, last ~90 days)."""
import json, sys, numpy as np, pandas as pd, statsmodels.api as sm
sys.path.insert(0, 'src'); from common import load
OUT = __import__('pathlib').Path('out'); pd.set_option('display.width', 220); pd.set_option('display.max_rows', 200)
U = [('SPX', 'SPX'), ('NDX', 'NDX'), ('RUT', 'RUT'), ('SOX', 'SOX'), ('S&P500 EW', 'SPXEW'), ('DJIA', 'DJIA'), ('VIX', 'VIX'), ('VIX3M', 'VIX3M'), ('SKEW', 'SKEW'),
     ('UST10Y (TNX)', 'TNX'), ('DXY', 'DXY'), ('USD/MYR', 'USDMYR'), ('Brent fut', 'BRENT'), ('WTI fut', 'WTI'), ('Gold fut', 'GOLD'), ('BTC', 'BTC'),
     ('ES fut', 'ES'), ('NQ fut', 'NQ'), ('RTY fut', 'RTY'), ('TWSE', 'TWSE'), ('TSMC 2330', 'TSMC'), ('KOSPI', 'KOSPI'), ('SK Hynix', 'SKHYNIX'), ('Samsung', 'SAMSUNG'),
     ('FBM KLCI', 'KLCI'), ('Nikkei', 'NIKKEI'), ('HSI', 'HSI'), ('XLE', 'XLE'), ('XLK', 'XLK'), ('XLF', 'XLF'), ('XLU', 'XLU'), ('SMH', 'SMH'), ('KRE', 'KRE'), ('IWF/IWD', None)]
rows = []
for name, a in U:
    if a is None: continue
    s = load(a); last = s.index[-1]
    w52 = s[s.index > last - pd.Timedelta(days=365)]
    def ret(days): b = s[s.index <= last - pd.Timedelta(days=days)]; return s.iloc[-1] / b.iloc[-1] - 1 if len(b) else np.nan
    ytd = s.iloc[-1] / s[:'2025-12-31'].iloc[-1] - 1 if len(s[:'2025-12-31']) else np.nan
    rows.append(dict(name=name, asof=last.date(), level=s.iloc[-1], off_52wH=s.iloc[-1] / w52.max() - 1, hi_date=w52.idxmax().date(), r1m=ret(30), r3m=ret(91), ytd=ytd))
gv = load('IWF') / load('IWD'); rows.append(dict(name='Growth/Value (IWF/IWD)', asof=gv.index[-1].date(), level=gv.iloc[-1], off_52wH=gv.iloc[-1] / gv[-252:].max() - 1, hi_date=gv[-252:].idxmax().date(),
                                                 r1m=gv.iloc[-1] / gv.iloc[-22] - 1, r3m=gv.iloc[-1] / gv.iloc[-64] - 1, ytd=gv.iloc[-1] / gv[:'2025-12-31'].iloc[-1] - 1))
for nm, a, b in [('EW/Cap (RSP/SPY-proxy SPX)', 'RSP', 'SPX'), ('Small/Large (IWM/SPX)', 'IWM', 'SPX'), ('HighBeta/LowVol (SPHB/SPLV)', 'SPHB', 'SPLV'), ('Mom (MTUM/SPX)', 'MTUM', 'SPX'), ('Quality (QUAL/SPX)', 'QUAL', 'SPX')]:
    r = (load(a) / load(b)).dropna(); rows.append(dict(name=nm, asof=r.index[-1].date(), level=r.iloc[-1], off_52wH=r.iloc[-1] / r[-252:].max() - 1, hi_date=r[-252:].idxmax().date(),
                                                       r1m=r.iloc[-1] / r.iloc[-22] - 1, r3m=r.iloc[-1] / r.iloc[-64] - 1, ytd=r.iloc[-1] / r[:'2025-12-31'].iloc[-1] - 1))
M0 = pd.DataFrame(rows); M0.to_csv(OUT / 'm0_baseline.csv', index=False)
print('M0 baseline (Yahoo daily closes; US cash = 30/10 close; futures/FX/Asia = 02/11; YTD vs 31/12/2025 close; price)')
print(M0.to_string(index=False, float_format=lambda v: f'{v:,.4f}'))
# HY OAS
h = pd.read_csv('data/raw/fred/BAMLH0A0HYM2.csv'); h.columns = ['d', 'v']; h['v'] = pd.to_numeric(h.v, errors='coerce'); h = h.dropna()
print(f"HY OAS (FRED, ICE BofA) last {h.d.iloc[-1]} {h.v.iloc[-1]:.2f}% | 3Y range {h.v.min():.2f}-{h.v.max():.2f} | pct-rank {(h.v < h.v.iloc[-1]).mean():.0%}")
# ---------- odds-beta ----------
H = json.load(open('data/raw/odds/polymarket_history.json'))
def pm(key):
    k = [x for x in H if x.endswith(key)][0]; v = H[k]
    return pd.Series({pd.to_datetime(p['t'], unit='s'): p['p'] for p in v}).sort_index()
sen_d = pm('which-party-will-win-the-senate-in-2026::Democratic Party') if False else pm('Democratic Party') if False else None
keys = {k: k for k in H}
sen = [k for k in H if k.startswith('which-party-will-win-the-senate') and k.endswith('Democratic Party')][0]
dsw = [k for k in H if k.endswith('Democrats Sweep')][0]; rrs = [k for k in H if k.endswith('Republicans Sweep')][0]; s2 = [k for k in H if k.endswith('R Senate, D House')][0]
def ser(k): return pd.Series({pd.to_datetime(p['t'], unit='s'): p['p'] for p in H[k]}).sort_index()
spx = load('SPX'); days = spx.index[(spx.index >= '2026-08-01') & (spx.index <= '2026-10-30')]
def at_close(s):  # last odds print at/before 01:00 UTC next day (~20:00 ET, after the cash close)
    return pd.Series({d: s[:d + pd.Timedelta(hours=25)].iloc[-1] for d in days})
O = pd.DataFrame({'P_Dsen': at_close(ser(sen)), 'P_DD': at_close(ser(dsw)), 'P_RR': at_close(ser(rrs)), 'P_DR': at_close(ser(s2))})
dO = O.diff().dropna()
names = ['SMH', 'SOXX', 'XLK', 'IGV', 'XLF', 'KRE', 'XLE', 'XOP', 'XLU', 'GRID', 'XLV', 'IHF', 'IBB', 'ITA', 'XHB', 'XLI', 'XLB', 'XLY', 'XLP', 'XLRE', 'XLC', 'IWM', 'RSP', 'SPHB', 'SPLV', 'MTUM', 'QUAL', 'IWF', 'IWD', 'SOXL', 'MU', 'AMAT', 'ARM', 'NVDA']
res = []
for n in names:
    s = load(n); r = (s.reindex(days).pct_change() - spx.reindex(days).pct_change()).dropna()  # excess vs SPX
    raw = s.reindex(days).pct_change().dropna()
    for reg in ['P_Dsen', 'P_RR']:
        x = dO[reg].reindex(r.index).dropna(); y = r.reindex(x.index)
        m = sm.OLS(y, sm.add_constant(x)).fit(cov_type='HC1')
        res.append(dict(name=n, regressor=reg, n=len(y), beta_per10pp=m.params[reg] * 0.10, t=m.tvalues[reg], r2=m.rsquared))
R = pd.DataFrame(res); R.to_csv(OUT / 'm7_odds_beta.csv', index=False)
x = dO['P_Dsen']; m = sm.OLS(spx.reindex(days).pct_change().reindex(x.index), sm.add_constant(x)).fit(cov_type='HC1')
print(f"\nOdds-beta window {days[0].date()}..{days[-1].date()} (n={len(dO)} trading days). P(D Senate) moved {O.P_Dsen.iloc[0]:.3f} -> {O.P_Dsen.iloc[-1]:.3f}; daily |dP| mean {dO.P_Dsen.abs().mean():.4f}, max {dO.P_Dsen.abs().max():.3f}")
print(f"SPX abs return on +10pp P(D Senate): {m.params['P_Dsen'] * 0.1:+.4%} (t={m.tvalues['P_Dsen']:.2f}, R2={m.rsquared:.3f})")
piv = R[R.regressor == 'P_Dsen'].sort_values('t')
print('Excess return vs SPX per +10pp P(D Senate) (HC1 t-stats):'); print(piv[['name', 'n', 'beta_per10pp', 't', 'r2']].to_string(index=False, float_format=lambda v: f'{v:+.4f}'))
