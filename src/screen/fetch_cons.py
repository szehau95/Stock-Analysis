"""Yahoo consensus snapshot (T3): EPS trend/revisions, target prices, recommendations, shares."""
import os, json, yfinance as yf
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
T = {"MAYBANK": "1155.KL", "PBBANK": "1295.KL", "CIMB": "1023.KL", "HLBANK": "5819.KL", "RHBBANK": "1066.KL",
     "AMBANK": "1015.KL", "BIMB": "5258.KL", "ALLIANCE": "2488.KL", "AFFIN": "5185.KL", "HLFG": "1082.KL", "MBSB": "1171.KL"}
out = {}
for b, t in T.items():
    tk = yf.Ticker(t); r = {}
    info = tk.info
    r.update(shares=info.get("sharesOutstanding"), mcap=info.get("marketCap"), bvps_yf=info.get("bookValue"),
             fy_end=info.get("lastFiscalYearEnd"), beta_yf=info.get("beta"))
    try:
        et, er, ee = tk.eps_trend, tk.eps_revisions, tk.earnings_estimate
        for p in ["0y", "+1y"]:
            k = "fy0" if p == "0y" else "fy1"
            r[f"eps_{k}"] = float(et.loc[p, "current"]); r[f"eps_{k}_90d"] = float(et.loc[p, "90daysAgo"])
            r[f"up30_{k}"] = int(er.loc[p, "upLast30days"]); r[f"dn30_{k}"] = int(er.loc[p, "downLast30days"])
            r[f"n_{k}"] = int(ee.loc[p, "numberOfAnalysts"])
    except Exception as e:
        r["cons_err"] = str(e)[:80]
    try:
        r.update({"tp_" + k: v for k, v in tk.analyst_price_targets.items()})
    except Exception:
        pass
    try:
        rec = tk.recommendations
        r["recs_0m"] = rec.iloc[0][["strongBuy", "buy", "hold", "sell", "strongSell"]].astype(int).to_dict()
    except Exception:
        pass
    out[b] = r
    print(b, {k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})
json.dump(out, open("data/raw/scr1410/yf_consensus.json", "w"), indent=1, default=str)
