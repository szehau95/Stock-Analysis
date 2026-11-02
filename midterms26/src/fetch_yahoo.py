"""Download full daily history from Yahoo chart API straight to CSV (keeps raw series out of chat context).
Usage: python fetch_yahoo.py OUTDIR SYMBOL[=alias] ...  (prices: close + adjclose where provided)"""
import sys, json, time, urllib.request, urllib.parse, pandas as pd, pathlib
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for arg in sys.argv[2:]:
    sym, _, alias = arg.partition('|')
    alias = alias or sym.replace('^','').replace('=','_')
    url = ("https://query1.finance.yahoo.com/v8/finance/chart/" + urllib.parse.quote(sym) +
           "?period1=-1325376000&period2=1800000000&interval=1d&events=div%7Csplit&includeAdjustedClose=true")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            js = json.load(urllib.request.urlopen(req, timeout=60)); break
        except Exception as e:
            err = e; time.sleep(2 ** (attempt + 1))
    else:
        print(f"{sym}: FAILED {err}"); continue
    r = js["chart"]["result"][0]; q = r["indicators"]["quote"][0]
    df = pd.DataFrame({"date": pd.to_datetime(r["timestamp"], unit="s", utc=True)
                       .tz_convert(r["meta"].get("exchangeTimezoneName", "America/New_York")).tz_localize(None).normalize(),
                       "open": q["open"], "high": q["high"], "low": q["low"], "close": q["close"], "volume": q["volume"]})
    if "adjclose" in r["indicators"]:
        df["adjclose"] = r["indicators"]["adjclose"][0]["adjclose"]
    df = df.dropna(subset=["close"]).drop_duplicates("date", keep="last").sort_values("date")
    df.to_csv(out / f"{alias}.csv", index=False)
    print(f"{sym:>10} -> {alias}.csv  {len(df):>6} rows  {df.date.iloc[0].date()} .. {df.date.iloc[-1].date()}  last={df.close.iloc[-1]:.2f}  tz={r['meta'].get('exchangeTimezoneName')}")
