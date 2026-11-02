"""Ken French daily files -> tidy DataFrames (returns in decimals, TOTAL return, CRSP)."""
import pandas as pd, numpy as np, io, re, pathlib
FF = pathlib.Path(__file__).resolve().parents[1] / 'data' / 'raw' / 'ff'
def _section(path, start_pat, n_skip_header=0):
    lines = open(path, encoding='latin-1').read().splitlines()
    i = next(k for k, l in enumerate(lines) if re.search(start_pat, l)) + 1
    while not lines[i].strip().startswith(','): i += 1
    hdr = ['date'] + [h.strip() for h in lines[i].split(',')[1:]]
    rows = []
    for l in lines[i + 1:]:
        if not re.match(r'^\s*\d{8}\s*,', l): break
        rows.append([x.strip() for x in l.split(',')])
    df = pd.DataFrame(rows, columns=hdr[:len(rows[0])])
    df['date'] = pd.to_datetime(df.date, format='%Y%m%d')
    df = df.set_index('date').apply(pd.to_numeric, errors='coerce')
    return df.where(df > -99, np.nan) / 100.0
def industries_vw(): return _section(FF / '49_Industry_Portfolios_Daily.csv', r'Average Value Weighted Returns -- Daily')
def factors3(): return _section(FF / 'F-F_Research_Data_Factors_daily.csv', r'compounds to 1-month|Tbill return')
def factors5(): return _section(FF / 'F-F_Research_Data_5_Factors_2x3_daily.csv', r'compounds to 1-month|Tbill return')
def mom(): return _section(FF / 'F-F_Momentum_Factor_daily.csv', r'Prior return|prior return')
def strev(): return _section(FF / 'F-F_ST_Reversal_Factor_daily.csv', r'Prior return|prior return')
if __name__ == '__main__':
    for nm, f in [('ind', industries_vw), ('ff3', factors3), ('ff5', factors5), ('mom', mom), ('strev', strev)]:
        d = f(); print(nm, d.shape, d.index[0].date(), d.index[-1].date(), list(d.columns)[:8])
