"""
03_prices.py
Daily adjusted closes for MU, peers and read-through names (yfinance), saved to data/prices.csv.
Report dates come from SEC EDGAR 8-K acceptance timestamps (data/earnings_dates.csv): all ~16:00 ET,
so reaction day t+1 = first session after the filing date.
"""
import pathlib
import pandas as pd
import yfinance as yf

ROOT = pathlib.Path(__file__).resolve().parent
TICKERS = ["MU", "SOXX", "SMH", "DRAM", "SNDK", "WDC", "STX", "NVDA", "AMD", "AVGO", "MRVL", "LRCX", "AMAT",
           "KLAC", "TEL", "000660.KS", "005930.KS", "^GSPC", "QQQ", "^VIX"]

px = yf.download(TICKERS, start="2017-01-01", auto_adjust=True, progress=False)
close = px["Close"].copy()
opn = px["Open"].copy()
close.to_csv(ROOT / "data" / "prices_close.csv")
opn.to_csv(ROOT / "data" / "prices_open.csv")
print(close.tail(8).round(2).to_string())
print("\nfirst valid:", {t: str(close[t].first_valid_index())[:10] for t in TICKERS})
