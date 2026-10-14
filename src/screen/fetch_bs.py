"""Yahoo quarterly balance sheet snapshot (T3): equity, intangibles, associates, shares -> TBVPS for P/TBV."""
import os, json, yfinance as yf
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
T = {"MAYBANK": "1155.KL", "PBBANK": "1295.KL", "CIMB": "1023.KL", "HLBANK": "5819.KL", "RHBBANK": "1066.KL", "AMBANK": "1015.KL"}
KEYS = ["Stockholders Equity", "Goodwill And Other Intangible Assets", "Tangible Book Value", "Investmentsin Associatesat Cost",
        "Ordinary Shares Number", "Total Assets"]
out = {}
for b, t in T.items():
    q = yf.Ticker(t).quarterly_balance_sheet
    col = q.columns[0]
    out[b] = {"date": str(col.date()), **{k: (float(q.loc[k, col]) if k in q.index and q.loc[k, col] == q.loc[k, col] else None) for k in KEYS}}
    print(b, out[b])
json.dump(out, open("data/raw/scr1410/yf_bs.json", "w"), indent=1)
