import json, urllib.request, pandas as pd, numpy as np
# Live IBKR positions/balances pulled 29-Sep-2026 (USD market values)
hold = {"AMAT":13020.83,"ARM":3666,"AVGO":2790.48,"BE":1305,"LRCX":2495.20,"MU":6299.22,"QCOM":2805,"SOXX":6678.86,"VRT":2434.31}
nlv, cash = 42160.48, 313.26
w = pd.Series(hold)/nlv*100
print("Weights pct NLV:", w.round(1).to_dict(), "| cash pct NLV: {:.2f}".format(cash/nlv*100))
print("Semis/AI-infra share of NLV: {:.1f}".format(w.sum()))
S={}
for t in list(hold)+["ORCL"]:
    req=urllib.request.Request(f"https://query1.finance.yahoo.com/v8/finance/chart/{t}?range=1y&interval=1d",headers={"User-Agent":"Mozilla/5.0"})
    d=json.load(urllib.request.urlopen(req,timeout=30))["chart"]["result"][0]
    S[t]=pd.Series(d["indicators"]["adjclose"][0]["adjclose"],index=pd.to_datetime(d["timestamp"],unit="s").normalize())
px=pd.DataFrame(S).dropna(); r=np.log(px).diff().dropna()
book=(r[list(hold)]*(pd.Series(hold)/sum(hold.values()))).sum(axis=1)
print("ORCL corr to book (1y daily): {:.2f} ; last 60d: {:.2f}".format(r["ORCL"].corr(book), r["ORCL"].iloc[-60:].corr(book.iloc[-60:])))
print("ORCL corr to each (1y):", r.corr()["ORCL"].drop("ORCL").round(2).to_dict())
