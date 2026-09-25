#!/usr/bin/env python3
"""Back out ~12M ATM implied vol from Sep-2027 option mids (quotes as of the 24/09/2026 close)."""
import os
import numpy as np
import pandas as pd
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
R = 0.035
ASOF = np.datetime64("2026-09-24")


def bs(S, K, T, r, q, s, cp):
    d1 = (np.log(S / K) + (r - q + 0.5 * s * s) * T) / (s * np.sqrt(T))
    d2 = d1 - s * np.sqrt(T)
    if cp == "c":
        return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)


def implied(p, S, K, T, q, cp):
    return brentq(lambda s: bs(S, K, T, R, q, s, cp) - p, 0.01, 5.0)


def main():
    import json
    uni = json.load(open(os.path.join(HERE, "data", "universe.json")))["names"]
    qt = pd.read_csv(os.path.join(HERE, "data", "iv12m_quotes.csv"))
    rows = []
    for _, r in qt.iterrows():
        T = (np.datetime64(r["expiry"]) - ASOF).astype(int) / 365.0
        q = uni[r["ticker"]].get("div", 0.0)
        ivs = []
        if not np.isnan(r["call_bid"]):
            ivs.append(implied((r["call_bid"] + r["call_ask"]) / 2, r["spot_close"], r["strike"], T, q, "c"))
        if not np.isnan(r["put_bid"]):
            ivs.append(implied((r["put_bid"] + r["put_ask"]) / 2, r["spot_close"], r["strike"], T, q, "p"))
        rows.append({"ticker": r["ticker"], "T": round(T, 3), "iv12m": float(np.mean(ivs)),
                     "iv12m_call": ivs[0], "iv12m_put": ivs[1] if len(ivs) > 1 else np.nan})
    out = pd.DataFrame(rows).set_index("ticker")
    out.to_csv(os.path.join(HERE, "data", "iv12m.csv"), float_format="%.4f")
    print(out.round(4).to_string())


if __name__ == "__main__":
    main()
