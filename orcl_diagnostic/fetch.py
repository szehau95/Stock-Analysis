import json, urllib.request, pandas as pd, time
T = ["ORCL","MSFT","AMZN","GOOGL","CRWV","NVDA","AVGO","SMH","IGV","^GSPC","^NDX","QQQ","SPY","^TNX","HYG","LQD"]
out = {}
for t in T:
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=2y&interval=1d"
    req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
    for i in range(3):
        try:
            d = json.load(urllib.request.urlopen(req, timeout=30)); break
        except Exception as e:
            print(t, e); time.sleep(2)
    r = d["chart"]["result"][0]
    idx = pd.to_datetime(r["timestamp"], unit="s").tz_localize("UTC").tz_convert("America/New_York").normalize().tz_localize(None)
    q = r["indicators"]["quote"][0]
    adj = r["indicators"].get("adjclose",[{}])[0].get("adjclose")
    out[t] = pd.Series(adj if adj else q["close"], index=idx)
    out[t+"_close"] = pd.Series(q["close"], index=idx)
    out[t+"_open"] = pd.Series(q["open"], index=idx)
    out[t+"_vol"] = pd.Series(q["volume"], index=idx)
df = pd.DataFrame(out)
df = df[~df.index.duplicated(keep="last")]
df.to_csv("data/prices.csv")
print(df.shape, df.index.min(), df.index.max())
print(df[["ORCL_close","^GSPC","^NDX"]].tail(5))
