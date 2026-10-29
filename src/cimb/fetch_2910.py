"""Refresh inputs for the 29/10/2026 CIMB note: Yahoo daily OHLCV (T3) for the core six + KLCI, BNM FMIP MGS yields (T1) 14-29/10."""
import os, time, requests, yfinance as yf, pandas as pd
from bs4 import BeautifulSoup
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
RAW = "data/raw/scr2910"
os.makedirs(RAW, exist_ok=True)
T = {"MAYBANK": "1155.KL", "PBBANK": "1295.KL", "CIMB": "1023.KL", "HLBANK": "5819.KL", "RHBBANK": "1066.KL", "AMBANK": "1015.KL",
     "KLCI": "^KLSE"}
for k, t in T.items():
    h = yf.Ticker(t).history(start="2015-01-01", end="2026-10-30", auto_adjust=False, actions=True)
    h.index = h.index.tz_localize(None).normalize()
    h.to_csv(f"{RAW}/yf_{k}.csv")


def mgs(d):
    for _ in range(3):
        try:
            r = requests.get("https://financialmarkets.bnm.gov.my/benchmark-yields", params={"date": d}, timeout=40)
            t = BeautifulSoup(r.text, "lxml").find("table", id="mgs-table")
            if not t:
                return None
            out = {"date": d}
            for tr in t.find_all("tr"):
                c = [x.get_text(strip=True) for x in tr.find_all("td")]
                if c and c[0] in ("3Y", "5Y", "7Y", "10Y"):
                    try:
                        out[c[0]] = float(c[5])
                    except ValueError:
                        pass
            return out
        except requests.RequestException:
            time.sleep(2)
    return None


rows = [r for r in (mgs(d.strftime("%Y-%m-%d")) for d in pd.bdate_range("2026-10-14", "2026-10-29")) if r]
pd.DataFrame(rows).dropna(subset=["10Y"]).to_csv(f"{RAW}/mgs_daily_bnm.csv", index=False)
