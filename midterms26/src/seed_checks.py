"""Data-derivable 0.1 seed facts, recomputed from raw series."""
import pandas as pd, numpy as np, json
import sys; sys.path.insert(0, "src"); from common import *
f = lambda v: f'{v:+.2%}'
spx, sox, rut, ndx = load('SPX'), load('SOX'), load('RUT'), load('NDX')
y26 = lambda s: s[s.index >= '2026-01-01']
# SOX peak / drawdown / H1
s = y26(sox); pk = s.idxmax(); print(f'SOX 2026 closing peak {pk.date()} {s.max():,.2f}; 30/10 {sox.iloc[-1]:,.2f} -> {f(sox.iloc[-1] / s.max() - 1)} from peak; Oct-end vs 30/09 {f(sox.iloc[-1] / sox[:"2026-09-30"].iloc[-1] - 1)}')
h1 = {}
for y in range(1995, 2027):
    a = sox[sox.index <= f'{y - 1}-12-31']; b = sox[sox.index <= f'{y}-06-30']
    if len(a) and len(b): h1[y] = b.iloc[-1] / a.iloc[-1] - 1
h1 = pd.Series(h1).sort_values(ascending=False); print(f'SOX H1 2026 {f(h1[2026])}; rank {list(h1.index).index(2026) + 1} of {len(h1)} full H1s since 1995; next best {h1.drop(2026).idxmax()} {f(h1.drop(2026).max())}')
print(f'SOX 2026 YTD max DD path: trough after peak {s[pk:].idxmin().date()} {f(s[pk:].min() / s.max() - 1)}')
# RUT
r = y26(rut); print(f'RUT 2026 closing high {r.idxmax().date()} {r.max():,.2f}; 30/10 {rut.iloc[-1]:,.2f} -> {f(rut.iloc[-1] / r.max() - 1)}')
# SPX record
allmax = spx.cummax(); rec = spx[spx == allmax]; last_rec = rec.index[-1]
print(f'SPX last record close {last_rec.date()} {spx[last_rec]:,.2f}; 30/10 {spx.iloc[-1]:,.2f} -> {f(spx.iloc[-1] / spx[last_rec] - 1)}; 2026 YTD {f(spx.iloc[-1] / spx[:"2025-12-31"].iloc[-1] - 1)}')
print(f'NDX 2026 high {y26(ndx).idxmax().date()} {y26(ndx).max():,.2f} -> {f(ndx.iloc[-1] / y26(ndx).max() - 1)}')
# 10Y October range (FRED DGS10) and 2Y
def fred(n):
    d = pd.read_csv(f'data/raw/fred/{n}.csv'); d.columns = ['date', 'v']; d['date'] = pd.to_datetime(d.date); d['v'] = pd.to_numeric(d.v, errors='coerce'); return d.dropna().set_index('date').v
t10 = fred('DGS10'); o = t10['2026-10-01':'2026-10-31']; print(f'UST10Y (FRED DGS10) Oct-2026 range {o.min():.2f}-{o.max():.2f} (max {o.idxmax().date()}); last {t10.index[-1].date()} {t10.iloc[-1]:.2f}; 2026 max {t10["2026"].max():.2f} on {t10["2026"].idxmax().date()}')
t2 = fred('DGS2'); print(f'UST2Y last {t2.index[-1].date()} {t2.iloc[-1]:.2f}; Oct range {t2["2026-10"].min():.2f}-{t2["2026-10"].max():.2f}')
# Brent early Oct: futures (Yahoo BZ=F) and Dated (FRED)
bz = load('BRENT'); db = fred('DCOILBRENTEU')
print(f'Brent fut 01-10/10: {bz["2026-10-01":"2026-10-10"].round(2).to_dict()}')
print(f'Brent fut Oct range {bz["2026-10"].min():.2f}-{bz["2026-10"].max():.2f}; 02/11 {bz.iloc[-1]:.2f}; 2026 max {bz["2026"].max():.2f} on {bz["2026"].idxmax().date()} | Dated Brent (FRED) early Oct {db["2026-10-01":"2026-10-10"].round(2).tolist()} last {db.index[-1].date()} {db.iloc[-1]:.2f}')
# Energy vs SPX ex-energy YTD (XLE proxy; energy weight at 31/12/2025 approximated from XLE/SPX history is not available -> use 3.0% assumption, sensitivity shown)
xle = load('XLE'); spy = load('SPX')
rE = xle.iloc[-1] / xle[:'2025-12-31'].iloc[-1] - 1; rS = spy.iloc[-1] / spy[:'2025-12-31'].iloc[-1] - 1
for w in (0.028, 0.03, 0.032):
    rx = (rS - w * rE) / (1 - w); print(f'Energy (XLE price) YTD {f(rE)} | SPX YTD {f(rS)} | SPX ex-energy (w_E={w:.1%}) {f(rx)} | gap {(rE - rx) * 100:+.1f}pp')
# Fed: last hike before Sep-2026
up = fred('DFEDTARU'); ch = up.diff(); hikes = ch[ch > 0]; print('Fed target-upper increases since 2022:', {d.date().isoformat(): v for d, v in up[hikes.index].loc['2022':].items()})
# Fed funds futures -> December hike probability (ZQ prices from TradingView 02/11: Nov 96.12, Dec 95.99, Jan 95.93)
effr = fred('DFF').iloc[-1]; zqz, zqf = 95.99, 95.93
dec_avg = 100 - zqz; post = (dec_avg * 31 - effr * 9) / 22; jan_avg = 100 - zqf
print(f'EFFR {effr:.2f} | Dec ZQ avg {dec_avg:.2f} -> post-09/12 rate {post:.3f} -> implied hike {post - effr:+.3f} = P(+25bp) {(post - effr) / 0.25:.0%} | Jan ZQ avg {jan_avg:.2f} -> P(+25bp by Jan) {(jan_avg - effr) / 0.25:.0%}')
# Polymarket odds on 30/10 vs now
h = json.load(open('data/raw/odds/polymarket_history.json'))
for k, v in h.items():
    if not v: continue
    ser = pd.Series({pd.to_datetime(p['t'], unit='s'): p['p'] for p in v}).sort_index()
    def at(d): x = ser[:d]; return x.iloc[-1] if len(x) else np.nan
    print(f'PM {k.split("::")[0][:28]:<28} {k.split("::")[1]:<18} 30/10 {at("2026-10-31 00:00"):.3f} | 26/10 {at("2026-10-27 00:00"):.3f} | 01/09 {at("2026-09-02 00:00"):.3f} | now {ser.iloc[-1]:.3f}')
