"""Month-end MGS benchmark yields from BNM FMIP (tier-1). Tries last 8 business days of each month."""
import requests, pandas as pd, concurrent.futures as cf, time
from bs4 import BeautifulSoup
def get(d):
    for _ in range(3):
        try:
            r = requests.get("https://financialmarkets.bnm.gov.my/benchmark-yields", params={"date": d}, timeout=40)
            s = BeautifulSoup(r.text, "lxml"); t = s.find("table", id="mgs-table")
            if not t: return None
            out = {}
            for tr in t.find_all("tr"):
                c = [x.get_text(strip=True) for x in tr.find_all("td")]
                if c and c[0] in ("3Y","5Y","7Y","10Y","15Y","20Y","30Y"):
                    try: out[c[0]] = float(c[5])
                    except: pass
            return out or None
        except Exception: time.sleep(2)
    return None
def month(m):
    for d in pd.bdate_range(m - pd.offsets.MonthBegin(1), m)[::-1][:8]:
        o = get(d.strftime("%Y-%m-%d"))
        if o and "10Y" in o: return dict(date=d, **o)
    return dict(date=m)
months = pd.date_range("2004-01-31", "2026-09-30", freq="ME")
with cf.ThreadPoolExecutor(6) as ex: res = list(ex.map(month, months))
df = pd.DataFrame(res).sort_values("date"); df.to_csv("data/clean/mgs_monthly_bnm.csv", index=False)
print(df.dropna(subset=["10Y"]).date.min(), len(df.dropna(subset=["10Y"])), "of", len(df)); print(df.tail(14).to_string())
