"""Edge / ROI / Kelly / depth from CLOB snapshot (~13:12 MYT 04/10/2026) + model output."""
import json

import numpy as np

FEE = 0.05  # Polymarket Sports taker feeRate; fee = C * feeRate * p * (1 - p)  (docs.polymarket.com)

# CLOB asks (price, size) of the YES token, best first; bids best first (snapshot via clob.polymarket.com/book)
BOOK = {
    "VER": dict(asks=[(.62, 10), (.63, 11160.91), (.64, 3667.13), (.65, 6814.37)],
                bids=[(.61, 98.69), (.60, 1048.6), (.59, 85), (.58, 6174.48), (.57, 6515)]),
    "ANT": dict(asks=[(.21, 464.46), (.22, 5073.95), (.23, 2899.99)], bids=[(.20, 565.25), (.19, 3637), (.18, 1104.5)]),
    "HAM": dict(asks=[(.10, 3102.6), (.105, 192.62), (.106, 31), (.116, 500), (.119, 20.1), (.126, 659.04), (.127, 3000)],
                bids=[(.095, 30), (.094, 20), (.084, 2000)]),
    "LEC": dict(asks=[(.035, 5180), (.039, 179.35), (.045, 250), (.047, 200), (.05, 100), (.052, 139.88), (.053, 10000)],
                bids=[(.03, 100), (.022, 350), (.02, 10000)]),
    "RUS": dict(asks=[(.033, 305.3), (.036, 505), (.037, 200), (.039, 2000), (.04, 100), (.042, 3000)],
                bids=[(.02, 100), (.015, 67), (.011, 818), (.01, 12015)]),
    "NOR": dict(asks=[(.029, 768.85), (.03, 605), (.032, 1140.8), (.036, 963.37), (.037, 2000), (.04, 250)],
                bids=[(.02, 9190.45), (.018, 1000), (.016, 1999)]),
    "HAD": dict(asks=[(.023, 4713.91), (.027, 250), (.031, 1000), (.034, 200), (.037, 500), (.041, 1564.07)],
                bids=[(.013, 1200), (.012, 20), (.011, 1000), (.01, 9978.71)]),
    "PIA": dict(asks=[(.012, 64.31), (.017, 486.8), (.018, 1122.63), (.02, 500), (.021, 9307), (.022, 1700)],
                bids=[(.008, 333), (.007, 150), (.005, 20000)]),
}


def fill(levels, usd):
    """VWAP incl. taker fee for spending `usd` walking `levels`; None if displayed depth insufficient."""
    left, sh, fee = usd, 0.0, 0.0
    for p, sz in levels:
        cost_per = p * (1 + FEE * (1 - p))
        take = min(sz, left / cost_per)
        sh += take
        fee += take * FEE * p * (1 - p)
        left -= take * cost_per
        if left <= 1e-9:
            return (usd - fee) / sh, usd / sh
    return None


def eff(p):
    return p * (1 + FEE * (1 - p))


res = json.load(open("base_result.json"))
pooled = res["pooled"]
lo = {c: np.mean([r["lo"][i] for r in res["runs"]]) for i, c in enumerate(res["runs"][0]["codes"])}
hi = {c: np.mean([r["hi"][i] for r in res["runs"]]) for i, c in enumerate(res["runs"][0]["codes"])}

print("OVERROUND: sum YES best ask (8 contenders) =",
      round(sum(b["asks"][0][0] for b in BOOK.values()), 3),
      "| sum YES best bid =", round(sum(b["bids"][0][0] for b in BOOK.values()), 3))

print("\nDEPTH (YES): VWAP price / all-in cost per share incl. fee, for $50 / $200 / $1000")
for c, b in BOOK.items():
    out = []
    for usd in (50, 200, 1000):
        f = fill(b["asks"], usd)
        out.append("n/a(depth)" if f is None else f"{f[0]:.4f}/{f[1]:.4f}")
    print(f"  {c} YES", " | ".join(out))
no_levels = [(round(1 - p, 4), s) for p, s in BOOK["VER"]["bids"]]
print("  VER NO ", " | ".join(f"{f[0]:.4f}/{f[1]:.4f}" for f in (fill(no_levels, u) for u in (50, 200, 1000))))


def kelly(p, c):
    return max(0.0, (p - c) / (1 - c))


print("\nEDGE TABLE (top-of-book, fee-inclusive cost c = ask*(1+0.05*(1-ask)))")
print("side      ask    cost   P_model [90% int]        edge_pp  EV/$1   ROI%   1/4K(pt)  1/4K(cons)")
rows = []
for c, b in BOOK.items():
    a = b["asks"][0][0]
    cst = eff(a)
    p, l, h = pooled[c], lo[c], hi[c]
    rows.append((f"{c} YES", a, cst, p, l, h, l))
    nb = round(1 - b["bids"][0][0], 4)
    rows.append((f"{c} NO", nb, eff(nb), 1 - p, 1 - h, 1 - l, 1 - h))
for name, a, cst, p, l, h, cons in rows:
    ev = p / cst - 1
    print(f"{name:8s} {a:6.3f} {cst:6.4f}  {p:6.4f} [{l:5.3f},{h:5.3f}]  {100 * (p - cst):+6.2f}  "
          f"{ev:+6.3f} {100 * ev:+7.1f}  {100 * 0.25 * kelly(p, cst):5.2f}%   {100 * 0.25 * kelly(cons, cst):5.2f}%")

# bookmaker prior: oddschecker best prices (fractional), top 8
odds = dict(VER=1 / 2, ANT=7 / 2, HAM=7, LEC=14, HAD=16, RUS=18, NOR=20, PIA=33)
imp = {k: 1 / (v + 1) for k, v in odds.items()}
s = sum(imp.values())
prop = {k: v / s for k, v in imp.items()}
lo_k, hi_k = 0.5, 3.0
for _ in range(100):
    k = (lo_k + hi_k) / 2
    if sum(v ** k for v in imp.values()) > 1:
        lo_k = k
    else:
        hi_k = k
power = {kk: v ** k for kk, v in imp.items()}
print(f"\nBOOKMAKER best-price implied sum = {s:.3f}; power-devig k = {k:.3f}")
print("driver raw   prop   power  PM_mid  model")
mid = {c: (b["asks"][0][0] + b["bids"][0][0]) / 2 for c, b in BOOK.items()}
for c in odds:
    print(f"  {c}  {imp[c]:.3f}  {prop[c]:.3f}  {power[c]:.3f}  {mid[c]:.4f}  {pooled[c]:.4f}")
