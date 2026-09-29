import pandas as pd, numpy as np
df = pd.read_csv("data/prices.csv", index_col=0, parse_dates=True)
c = df["ORCL_close"].dropna()
last = c.index[-1]
pk_all = c.idxmax(); print("All-time-in-window peak:", pk_all.date(), round(c.max(),2))
print("Last:", last.date(), c.iloc[-1], "DD from peak %:", round((c.iloc[-1]/c.max()-1)*100,1))
lo = c.idxmin(); print("Trough:", lo.date(), round(c.min(),2), "DD at trough:", round((c.min()/c.max()-1)*100,1), " rebound from trough %:", round((c.iloc[-1]/c.min()-1)*100,1))
def chg(n): return round((c.iloc[-1]/c.iloc[-1-n]-1)*100,1)
print("1D", chg(1), "1W", chg(5), "1M", chg(21), "3M", chg(63))
ye = c[:"2025-12-31"].iloc[-1]; print("YE25 close", ye, "YTD %", round((c.iloc[-1]/ye-1)*100,1))
# local peaks
print("Local peak since Apr 2026:", c["2026-04":].idxmax().date(), c["2026-04":].max())
print("Local peak since Aug 2026:", c["2026-08":].idxmax().date(), c["2026-08":].max(), "DD", round((c.iloc[-1]/c["2026-08":].max()-1)*100,1))
# benchmarks same windows
for t in ["^GSPC","^NDX","MSFT","AMZN","GOOGL","CRWV","NVDA","AVGO","SMH","IGV"]:
    s=df[t].dropna()
    f=lambda a,b: round((s[:b].iloc[-1]/s[:a].iloc[-1]-1)*100,1)
    print(f"{t:6s} since ORCLpeak {f(str(pk_all.date()), str(last.date())):7} | since 2026-06-22 {f('2026-06-22',str(last.date())):7} | since 2026-09-14 {f('2026-09-14',str(last.date())):6} | YTD {f('2025-12-31',str(last.date())):6}")
# big daily moves
r = c.pct_change()*100
print("\nDays |move|>=7% in last 12m:")
print(r["2025-09-29":][r["2025-09-29":].abs()>=7].round(1).to_string())
# gap vs intraday decomposition for last 20 days
o = df["ORCL_open"]
gap = (o/c.shift(1)-1)*100; intra=(c/o-1)*100
x = pd.DataFrame({"close":c,"ret":r,"gap":gap,"intraday":intra})["2026-08-25":].round(2)
print(x.to_string())
