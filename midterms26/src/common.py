"""Shared loaders, event dates and window logic for the midterm playbook. All maths here, never in chat."""
import pandas as pd, numpy as np, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
MIDTERMS = {1950: '1950-11-07', 1954: '1954-11-02', 1958: '1958-11-04', 1962: '1962-11-06', 1966: '1966-11-08',
            1970: '1970-11-03', 1974: '1974-11-05', 1978: '1978-11-07', 1982: '1982-11-02', 1986: '1986-11-04',
            1990: '1990-11-06', 1994: '1994-11-08', 1998: '1998-11-03', 2002: '2002-11-05', 2006: '2006-11-07',
            2010: '2010-11-02', 2014: '2014-11-04', 2018: '2018-11-06', 2022: '2022-11-08'}
MIDTERMS = {y: pd.Timestamp(d) for y, d in MIDTERMS.items()}
ELECTION_2026 = pd.Timestamp('2026-11-03')
# 0.2 classification (verified against House/Senate party-division histories; see out/seed_verification.txt)
CLASS = pd.DataFrame([
    (1950, 'Truman', 'D', 'D/D', 'D/D', 'Unified, held both', 'S1'),
    (1954, 'Eisenhower', 'R', 'R/R', 'D/D', 'Unified -> lost both', 'S3'),
    (1958, 'Eisenhower', 'R', 'D/D', 'D/D', 'Opposition Congress, unchanged', '-'),
    (1962, 'Kennedy', 'D', 'D/D', 'D/D', 'Unified, held both', 'S1'),
    (1966, 'Johnson', 'D', 'D/D', 'D/D', 'Unified, held both', 'S1'),
    (1970, 'Nixon', 'R', 'D/D', 'D/D', 'Opposition Congress, unchanged', '-'),
    (1974, 'Ford', 'R', 'D/D', 'D/D', 'Opposition Congress, unchanged', '-'),
    (1978, 'Carter', 'D', 'D/D', 'D/D', 'Unified, held both', 'S1'),
    (1982, 'Reagan', 'R', 'D/R', 'D/R', 'Split, unchanged', '-'),
    (1986, 'Reagan', 'R', 'D/R', 'D/D', 'Split -> lost Senate', 'S4~'),
    (1990, 'Bush41', 'R', 'D/D', 'D/D', 'Opposition Congress, unchanged', '-'),
    (1994, 'Clinton', 'D', 'D/D', 'R/R', 'Unified -> lost both', 'S3'),
    (1998, 'Clinton', 'D', 'R/R', 'R/R', 'Opposition Congress, unchanged', '-'),
    (2002, 'Bush43', 'R', 'R/D', 'R/R', 'Split -> won Senate (unified)', 'S1+'),
    (2006, 'Bush43', 'R', 'R/R', 'D/D', 'Unified -> lost both', 'S3'),
    (2010, 'Obama', 'D', 'D/D', 'R/D', 'Unified -> lost House', 'S2'),
    (2014, 'Obama', 'D', 'R/D', 'R/R', 'Split -> lost Senate', 'S4~'),
    (2018, 'Trump', 'R', 'R/R', 'D/R', 'Unified -> lost House', 'S2'),
    (2022, 'Biden', 'D', 'D/D', 'R/D', 'Unified -> lost House', 'S2'),
], columns=['year', 'president', 'pres_party', 'before', 'after', 'path', 'bucket']).set_index('year')
WINDOWS = ['1D', '1W', '1M', '3M', '6M', '12M']

def load(alias, col='close'):
    df = pd.read_csv(RAW / 'yahoo' / f'{alias}.csv', parse_dates=['date'])
    s = df.set_index('date')[col].astype(float).dropna()
    s = s[~s.index.duplicated(keep='last')].sort_index()
    return s[s > 0]

def election_day(year):
    """First Tuesday after the first Monday in November."""
    d = pd.Timestamp(year, 11, 1)
    first_mon = d + pd.Timedelta(days=(0 - d.weekday()) % 7)
    return first_mon + pd.Timedelta(days=1)

def t0_date(s, eday, conv='eday'):
    """T0 = last close on/before the anchor. eday: election day (if exchange shut that day, prior close);
    fri: Friday before election day; oct31: 31 Oct of that year."""
    anchor = {'eday': eday, 'fri': eday - pd.Timedelta(days=4), 'oct31': pd.Timestamp(eday.year, 10, 31)}[conv]
    idx = s.index[s.index <= anchor]
    return idx[-1] if len(idx) else None

def end_date(s, t0, w):
    i0 = s.index.get_loc(t0)
    if w == '1D':
        return s.index[i0 + 1] if i0 + 1 < len(s) else None
    tgt = t0 + (pd.Timedelta(days=7) if w == '1W' else pd.DateOffset(months=int(w[:-1])))
    if tgt > s.index[-1]:
        return None
    return s.index[s.index <= tgt][-1]

def window_stats(s, t0, w):
    te = end_date(s, t0, w)
    if te is None:
        return None
    p0 = s.loc[t0]; path = s.loc[t0:te].iloc[1:]
    rel = path / p0 - 1
    trough_d = rel.idxmin(); dd = min(rel.min(), 0.0)
    rec_d = None
    if dd < 0:
        after = s.loc[trough_d:]; back = after[after >= p0]
        rec_d = back.index[0] if len(back) else None
    return dict(t0=t0, end=te, ret=s.loc[te] / p0 - 1, maxdd=dd, maxdd_date=trough_d if dd < 0 else pd.NaT,
                maxrun=max(rel.max(), 0.0), rec_date=rec_d,
                rec_tdays=(s.index.get_loc(rec_d) - s.index.get_loc(t0)) if rec_d is not None else np.nan)

def fwd_all(s, w, start=None, stop=None):
    """Vectorised forward returns from every trading day (same window definition as window_stats)."""
    idx = s.index; v = s.values
    if w == '1D':
        r = pd.Series(np.r_[v[1:] / v[:-1] - 1, np.nan], index=idx)
    else:
        off = pd.Timedelta(days=7) if w == '1W' else pd.DateOffset(months=int(w[:-1]))
        tgt = pd.DatetimeIndex(idx + off)
        pos = np.searchsorted(idx.values, tgt.values, side='right') - 1
        ok = tgt <= idx[-1]
        r = pd.Series(np.where(ok, v[np.clip(pos, 0, len(v) - 1)] / v - 1, np.nan), index=idx)
    if start: r = r[r.index >= pd.Timestamp(start)]
    if stop: r = r[r.index <= pd.Timestamp(stop)]
    return r.dropna()
