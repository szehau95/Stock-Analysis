"""Yahoo daily OHLCV + dividends (T3) to 29/10/2026 for the three context banks used in the dividend-yield comparison."""
import os, yfinance as yf
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
for k, t in {"BIMB": "5258.KL", "ALLIANCE": "2488.KL", "AFFIN": "5185.KL"}.items():
    h = yf.Ticker(t).history(start="2015-01-01", end="2026-10-30", auto_adjust=False, actions=True)
    h.index = h.index.tz_localize(None).normalize()
    h.to_csv(f"data/raw/scr2910/yf_{k}.csv")
    print(k, h.index.max().date(), round(h.Close.iloc[-1], 3), h[h.Dividends > 0].Dividends.loc["2025-06-01":].to_dict())
