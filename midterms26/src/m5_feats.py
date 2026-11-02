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
