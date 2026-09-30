"""Daily MGS 10Y/3Y/5Y closes from BNM FMIP (tier-1), 2025-01-01..AS_OF, for factor attribution."""
import requests, pandas as pd, concurrent.futures as cf, time
from bs4 import BeautifulSoup
def get(d):
    for _ in range(3):
        try:
            r = requests.get("https://financialmarkets.bnm.gov.my/benchmark-yields", params={"date": d}, timeout=40)
            s = BeautifulSoup(r.text, "lxml"); t = s.find("table", id="mgs-table"); h6 = s.find("h6")
            if not t: return None
            out = {"req": d, "trading_date": h6.get_text(" ", strip=True).replace("Trading Date:", "").strip() if h6 else None}
            for tr in t.find_all("tr"):
                c = [x.get_text(strip=True) for x in tr.find_all("td")]
                if c and c[0] in ("3Y","5Y","7Y","10Y","15Y","20Y","30Y"):
                    try: out[c[0]] = float(c[5])
                    except: pass
            return out
        except Exception: time.sleep(2)
    return None
days = [d.strftime("%Y-%m-%d") for d in pd.bdate_range("2025-01-01", "2026-09-29")]
with cf.ThreadPoolExecutor(8) as ex: res = [r for r in ex.map(get, days) if r]
df = pd.DataFrame(res); df.to_csv("data/clean/mgs_daily_bnm.csv", index=False)
print(len(df)); print(df.tail(10).to_string())
