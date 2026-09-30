"""Fetch daily OHLCV + dividends + splits from Yahoo (tier-3; used for price mechanics only, cross-checked vs IBKR)."""
import yfinance as yf, pandas as pd
T = {"MAYBANK":"1155.KL","PBBANK":"1295.KL","CIMB":"1023.KL","HLBANK":"5819.KL","RHBBANK":"1066.KL","AMBANK":"1015.KL",
     "BIMB":"5258.KL","ALLIANCE":"2488.KL","AFFIN":"5185.KL","KLCI":"^KLSE",
     "DBS":"D05.SI","OCBC":"O39.SI","UOB":"U11.SI","BBCA":"BBCA.JK","BBRI":"BBRI.JK","BMRI":"BMRI.JK","KBANK":"KBANK.BK","BBL":"BBL.BK",
     "STI":"^STI","JCI":"^JKSE","USDMYR":"MYR=X","DXY":"DX-Y.NYB","UST10":"^TNX","BRENT":"BZ=F","EWM":"EWM",
     "TENAGA":"5347.KL","YTLPOWR":"6742.KL","GAMUDA":"5398.KL","PCHEM":"5183.KL","IHH":"5225.KL","CDB":"6947.KL","SUNWAY":"5211.KL","YTL":"4677.KL","IOICORP":"1961.KL","PMETAL":"8869.KL","TM":"4863.KL","SIMEPLT":"5285.KL"}
out = {}
for k, t in T.items():
    h = yf.Ticker(t).history(start="2000-01-01", auto_adjust=False, actions=True)
    h.index = h.index.tz_localize(None).normalize()
    h.to_csv(f"data/raw/yf_{k}.csv")
    print(k, len(h), h.index.max().date(), round(h.Close.iloc[-1], 3), "splits:", h.loc[h["Stock Splits"] > 0, "Stock Splits"].to_dict() if "Stock Splits" in h else {})
