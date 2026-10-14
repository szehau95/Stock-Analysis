import os, json
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
os.chdir(ROOT)
RAW, OUT = "data/raw/scr1410", "output/screen"
os.makedirs(OUT, exist_ok=True)

CORE = ["MAYBANK", "PBBANK", "CIMB", "HLBANK", "RHBBANK", "AMBANK"]
CONTEXT = ["BIMB", "ALLIANCE", "AFFIN"]  # regression context only (listed banks with point-in-time panels)
ASOF = pd.Timestamp("2026-10-13")  # last complete Bursa session; 14/10 bar was still forming at build time
MGS10 = 0.0383  # BNM FMIP benchmark 10Y, 13/10/2026 (T1)
OPR = 0.0275  # BNM MPS 03/09/2026 (T1)
ERP, G = 0.06, 0.04
FY_END_NEXT = {"MAYBANK": "2026-12-31", "PBBANK": "2026-12-31", "CIMB": "2026-12-31", "RHBBANK": "2026-12-31",
               "HLBANK": "2027-06-30", "AMBANK": "2027-03-31", "BIMB": "2026-12-31", "ALLIANCE": "2027-03-31", "AFFIN": "2026-12-31"}

# HLB associates (mainly 17.8% of Bank of Chengdu): FY26 share of profit (T1, HLFG deck p13);
# carrying values Jun-26 / Jun-25 (T3, Yahoo balance sheet); BOCD close 13/10/2026 CNY19.25 x 4.2384b shares; CNYMYR 0.6097 (T3).
HLB_ASSOC = dict(share_profit_t4q=1380e6, carry_now=10.352e9, carry_4q_ago=9.211e9, equity_now=41.790e9, equity_4q_ago=39.287e9,
                 pat_t4q=4531e6, shares=2.050444e9, bocd_stake=0.178, bocd_px=19.25, bocd_shares=4.238435e9, cnymyr=0.6097)


def px(k, asof=ASOF):
    h = pd.read_csv(f"{RAW}/yf_{k}.csv", index_col=0, parse_dates=True)
    h.index = pd.to_datetime(h.index).normalize()
    h = h[~h.index.duplicated()].sort_index()
    return h[h.index <= asof]


def panel(b):
    d = pd.read_csv(f"data/clean/panel_{b}.csv", index_col=0, parse_dates=True, low_memory=False)
    return d


def quarterly(b):
    return pd.read_csv(f"data/clean/quarterly_adj_{b}.csv", parse_dates=["qdate", "announced"])


def kpi():
    return pd.read_csv("data/clean/scr_kpi_core6.csv").set_index("bank")


def cons():
    return json.load(open(f"{RAW}/yf_consensus.json"))


def pct_score(s, higher_better=True):
    """Percentile score 0-100 within the set; NaN -> 50 (neutral, flagged as UNVERIFIED upstream)."""
    s = pd.to_numeric(s, errors="coerce")
    r = s.rank(ascending=higher_better, method="average")
    n = s.notna().sum()
    out = (r - 1) / (n - 1) * 100 if n > 1 else r * 0 + 50
    return out.fillna(50)


def fmt(x, d=2, pct=False):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return "n/a"
    return f"{x*100:.{d}f}%" if pct else f"{x:.{d}f}"
