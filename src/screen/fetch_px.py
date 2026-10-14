"""Yahoo daily OHLCV + dividends since 2015 for the screen universe (T3: price mechanics only)."""
import os, yfinance as yf, pandas as pd
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
T = {"MAYBANK": "1155.KL", "PBBANK": "1295.KL", "CIMB": "1023.KL", "HLBANK": "5819.KL", "HLFG": "1082.KL",
     "RHBBANK": "1066.KL", "AMBANK": "1015.KL", "BIMB": "5258.KL", "AFFIN": "5185.KL", "ALLIANCE": "2488.KL",
     "MBSB": "1171.KL", "KLCI": "^KLSE"}
for k, t in T.items():
    h = yf.Ticker(t).history(start="2015-01-01", end="2026-10-15", auto_adjust=False, actions=True)
    h.index = h.index.tz_localize(None).normalize()
    h.to_csv(f"data/raw/scr1410/yf_{k}.csv")
    print(f"{k:9s} {len(h):5d} rows  last {h.index.max().date()}  close {h.Close.iloc[-1]:.3f}")
