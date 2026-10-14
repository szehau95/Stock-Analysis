"""BNM FMIP benchmark MGS yields (T1) for 30/09/2026..13/10/2026, appended to the AS_OF 30/09 daily series."""
import os, time, requests, pandas as pd
from bs4 import BeautifulSoup
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
def get(d):
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
rows = [r for r in (get(d.strftime("%Y-%m-%d")) for d in pd.bdate_range("2026-09-30", "2026-10-13")) if r]
old = pd.read_csv("data/clean/mgs_daily_bnm.csv").rename(columns={"req": "date"}).drop(columns="trading_date")
df = pd.concat([old, pd.DataFrame(rows)]).drop_duplicates("date", keep="last").dropna(subset=["10Y"])
df.to_csv("data/raw/scr1410/mgs_daily_bnm.csv", index=False)
print(df.tail(12).to_string(index=False))
