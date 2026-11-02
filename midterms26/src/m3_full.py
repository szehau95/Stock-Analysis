"""M3 full: Table 3 (midterm by midterm) with House swing, chamber flips, Fed direction, 10Y, CAPE, recession <=12M, SPX TR approx."""
import sys, re, html, numpy as np, pandas as pd
sys.path.insert(0, 'src'); from common import load, MIDTERMS, CLASS, t0_date
OUT = __import__('pathlib').Path('out'); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
def fred(n):
    d = pd.read_csv(f'data/raw/fred/{n}.csv'); d.columns = ['date', 'v']; d['date'] = pd.to_datetime(d.date); d['v'] = pd.to_numeric(d.v, errors='coerce'); return d.dropna().set_index('date').v
# House party divisions (history.house.gov): total, [footnote], D, R
t = open('data/raw/house_party_divisions.htm', encoding='utf-8', errors='ignore').read()
txt = html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', t)))
seats = {}
for m in re.finditer(r'(\d+)(?:st|nd|rd|th) \((\d{4})[–-](\d{4})\)\s+((?:\d+\s+){2,5})', txt):
    nums = [int(x) for x in m.group(4).split()]
    tot = nums[0]; rest = nums[1:]
    if rest and rest[0] < 20: rest = rest[1:]
    if len(rest) >= 2: seats[int(m.group(1))] = dict(D=rest[0], R=rest[1], total=tot)
sh = pd.read_csv('data/raw/shiller/shiller_mirror.csv', parse_dates=['Date']).set_index('Date')
fedfunds, disc, gs10, usrec, cpi = fred('FEDFUNDS'), fred('INTDSRUSM193N'), fred('GS10'), fred('USREC'), fred('CPIAUCSL')
ev = pd.read_csv(OUT / 'm2_events_SPX_eday.csv', parse_dates=['t0', 'end', 'maxdd_date']); sox = pd.read_csv(OUT / 'm2_events_SOX_eday.csv')
spx = load('SPX')
def at(s, d): x = s[:d]; return x.iloc[-1] if len(x) else np.nan
rows = []
for y, ed in MIDTERMS.items():
    c = CLASS.loc[y]; cong_after = (y - 1786) // 2; cong_before = cong_after - 1; p = c.pres_party
    sw = seats[cong_after][p] - seats[cong_before][p] if cong_after in seats and cong_before in seats else np.nan
    flipped = [ch for ch, i in (('House', 0), ('Senate', 2)) if c.before[i] != c.after[i]]
    oct_ = pd.Timestamp(y, 10, 1); apr = pd.Timestamp(y, 4, 1)
    if y >= 1955: f0, f6, src = at(fedfunds, oct_), at(fedfunds, apr), 'FF'
    else: f0, f6, src = at(disc, oct_), at(disc, apr), 'disc'
    dF = f0 - f6; fed = 'hiking' if dF >= 0.25 else ('cutting' if dF <= -0.25 else 'hold')
    y10 = at(gs10, oct_) if y >= 1954 else at(sh['Long Interest Rate'], oct_)
    cape = at(sh['PE10'], oct_)
    rec = int(usrec[(usrec.index > oct_) & (usrec.index <= oct_ + pd.DateOffset(months=12))].max() > 0)
    e = ev[ev.year == y].set_index('window')
    # TR approx: add Shiller monthly dividends (annualised D/12 per month) accrued over the window
    def tr(w):
        t0, t1 = e.loc[w, 't0'], e.loc[w, 'end']; P0, P1 = spx[t0], spx[t1]
        months = pd.date_range(t0 + pd.offsets.MonthBegin(1), t1, freq='MS')
        dv = sh['Dividend'].replace(0, np.nan).ffill().reindex(months, method='ffill').fillna(0).sum() / 12
        return (P1 + dv) / P0 - 1
    s12 = sox[(sox.year == y) & (sox.window == '12M')].ret
    rows.append(dict(year=y, president=f"{c.president} ({p})", before_after=f"{c.before} -> {c.after}", house_swing=sw, flipped='+'.join(flipped) or '-',
                     spx6=e.loc['6M', 'ret'], spx12=e.loc['12M', 'ret'], spx12_tr=tr('12M'), spx6_tr=tr('6M'), maxdd12=e.loc['12M', 'maxdd'],
                     sox12=s12.iloc[0] if len(s12) else np.nan, fed=f"{fed} ({dF:+.2f}, {src})", y10=y10, cape=cape, rec12=rec, bucket=c.bucket))
T3 = pd.DataFrame(rows).set_index('year'); T3.to_csv(OUT / 'table3_midterms.csv')
print(T3.to_string(float_format=lambda v: f'{v:+.3f}' if abs(v) < 5 else f'{v:.1f}'))
print(f"\nTR approx (Shiller dividends): 6M mean {T3.spx6_tr.mean():+.4f} | 12M mean {T3.spx12_tr.mean():+.4f} median {T3.spx12_tr.median():+.4f} hit {(T3.spx12_tr > 0).mean():.2f} (price 12M mean {T3.spx12.mean():+.4f})")
print('House swing vs SPX 12M: Spearman', round(T3[['house_swing', 'spx12']].corr('spearman').iloc[0, 1], 3), '| president-party seat loss mean', T3.house_swing.mean())
print('Weak 12M cluster (<+7%):', T3[T3.spx12 < 0.07][['president', 'spx12', 'fed', 'rec12']].to_dict('index'))
