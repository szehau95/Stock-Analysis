"""CIMB securities book deep-dive, AS_OF 29/10/2026: what is held where, how marks reach P&L/equity/CET1, the +100bp maths.

T1: CIMB Group condensed interim FS 30/06/2026 (notes A9, A10, A12, A28, statements of comprehensive income and equity);
    BNM Capital Adequacy Framework (Capital Components) 14/06/2024 paras 22.1-22.3; BNM FMIP MGS yields.
T2: RHB Research CET1 sensitivity (BusinessToday 06/10/2026); JPMorgan FVTPL share (The Edge 07/10/2026).
"""
import os
import pandas as pd

os.chdir(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")))
OUT = "output/cimb"
TAX, SH = 0.24, 10.800496  # statutory rate used across the screen; weighted shares (1H26 NP / basic EPS)

# ---- 1. Holdings by accounting bucket and issuer type, RM bn, 30/06/2026 (A9, A10, A12) ----
H = pd.DataFrame({
    "FVTPL": {"MY govt (MGS, GII, MGTB, BNM notes)": 5.651367 + 6.563236 + 1.416380 + 3.642291,
              "Foreign govt bonds": 19.515329, "Foreign govt T-bills": 9.530123,
              "MY corporate / Cagamas / NID / CP / PN": 1.075031 + 2.949185 + 2.114036 + 0.274477 + 3.781243,
              "Foreign corporate": 5.330866, "Equities, funds (not debt)": 3.340963 + 1.281979 + 0.223937 + 0.007687 + 0.031977},
    "FVOCI": {"MY govt (MGS, GII, MGTB, BNM notes)": 4.590396 + 8.062719, "Foreign govt bonds": 24.428651, "Foreign govt T-bills": 0.0,
              "MY corporate / Cagamas / NID / CP / PN": 0.999351 + 0.444753 + 0.020164 + 28.738484,
              "Foreign corporate": 16.397921, "Equities, funds (not debt)": 0.0},
    "Amortised cost": {"MY govt (MGS, GII, MGTB, BNM notes)": 11.946526 + 25.320519,
                       "Foreign govt bonds": 9.013433, "Foreign govt T-bills": 10.636326,
                       "MY corporate / Cagamas / NID / CP / PN": 0.398227 + 0.112980 + 0.184497 + 20.810751,
                       "Foreign corporate": 3.994439, "Equities, funds (not debt)": 0.0},
})
H.loc["Total"] = H.sum()
debt = H.drop(index=["Total", "Equities, funds (not debt)"]).sum()
mix = pd.Series({"debt securities total": debt.sum(), "FVTPL share of debt securities": debt["FVTPL"] / debt.sum(),
                 "FVOCI share": debt["FVOCI"] / debt.sum(), "AC share": debt["Amortised cost"] / debt.sum(),
                 "FVOCI foreign share": (H.loc["Foreign govt bonds", "FVOCI"] + H.loc["Foreign corporate", "FVOCI"]) / H.loc["Total", "FVOCI"],
                 "FVOCI corporate share": (H.loc["MY corporate / Cagamas / NID / CP / PN", "FVOCI"] + H.loc["Foreign corporate", "FVOCI"]) / H.loc["Total", "FVOCI"],
                 "FVTPL bills+BNM notes share (short-dated)": (1.416380 + 3.642291 + 9.530123) / H.loc["Total", "FVTPL"]})

# ---- 2. FVOCI debt reserve walk, 1H26 (RM m; statement of comprehensive income / changes in equity) ----
walk = pd.Series({"reserve 01/01/2026 (attributable)": 194.134, "fair-value change (market)": -562.392,
                  "realised gains recycled to P&L on disposal": -270.990, "ECL change": -2.249, "tax": 167.976, "FX": -5.167,
                  "total OCI (group)": -672.822, "of which non-controlling": -27.298, "attributable": -645.524,
                  "reserve 30/06/2026 (attributable)": -451.390})
assert abs(walk["reserve 01/01/2026 (attributable)"] + walk["attributable"] - walk["reserve 30/06/2026 (attributable)"]) < 0.01


# ---- 3. BNM CAF paras 22.1/22.3: 55% of cumulative FVOCI gains are deducted from CET1; losses count in full ----
def cet1_counted(reserve):
    return 0.45 * reserve if reserve > 0 else reserve


cet1_cost_1h26 = cet1_counted(walk["reserve 01/01/2026 (attributable)"]) - cet1_counted(walk["reserve 30/06/2026 (attributable)"])
RWA, EQ, CET1_CAP, CET1_POST = 389.749722, 70.261905, 54.216280, 0.13911

# ---- 4. +100bp: duration backed out of RHB Research's 52bp, then applied to book value and per share ----
SENS_T2 = 0.0052
D = SENS_T2 * RWA / (H.loc["Total", "FVOCI"] * (1 - TAX) * 0.01)
fvoci_pre = H.loc["Total", "FVOCI"] * D * 0.01
fvoci_post = fvoci_pre * (1 - TAX)
# Trading-book duration and hedges are not disclosed: assume 0.25y for bills/BNM notes and 1.5y for other trading debt,
# unhedged -> an upper bound (CIMB carries RM16.6b of derivative assets, much of it likely hedging this book)
TPL_BILLS = 1.416380 + 3.642291 + 9.530123
tpl_debt = H.loc["Total", "FVTPL"] - H.loc["Equities, funds (not debt)", "FVTPL"]
tpl_pre = (TPL_BILLS * 0.25 + (tpl_debt - TPL_BILLS) * 1.5) * 0.01
up100 = pd.Series({
    "implied FVOCI effective duration (yrs)": D,
    "FVOCI loss pre-tax (RM bn)": fvoci_pre, "FVOCI loss after tax (RM bn)": fvoci_post,
    "CET1 hit (bp of RWA)": fvoci_post / RWA * 1e4, "book value hit (% of equity)": fvoci_post / EQ, "book value hit (sen/share)": fvoci_post / SH * 100,
    "FVTPL debt loss pre-tax, unhedged (RM bn, assumed duration)": tpl_pre,
    "  as % of 2Q26 PBT": tpl_pre / 2.607469, "  CET1 (bp, after tax, unhedged)": tpl_pre * (1 - TAX) / RWA * 1e4,
    "AC economic loss at same duration (not booked, RM bn)": H.loc["Total", "Amortised cost"] * D * 0.01,
    "buffer value if reserve were still +RM194m (CET1 bp)": 0.55 * 0.194134 / RWA * 1e4,
})

# ---- 5. Marks since the last balance sheet (MGS proxy) and capital headroom vs the 14% target ----
m = pd.concat([pd.read_csv("data/raw/scr1410/mgs_daily_bnm.csv", parse_dates=["date"]),
               pd.read_csv("data/raw/scr2910/mgs_daily_bnm.csv", parse_dates=["date"])]).drop_duplicates("date", keep="last")
m = m.set_index("date").sort_index()[["3Y", "5Y", "7Y", "10Y"]].ffill()
at = lambda d: m.loc[:d].iloc[-1]
moves = pd.DataFrame({"30/06": at("2026-06-30"), "30/09": at("2026-09-30"), "29/10": at("2026-10-29")})
dy = {"3Q26 (30/06->30/09)": (moves["30/09"] - moves["30/06"]).mean() / 100, "4QTD (30/09->29/10)": (moves["29/10"] - moves["30/09"]).mean() / 100,
      "since 30/06": (moves["29/10"] - moves["30/06"]).mean() / 100}
marks = pd.DataFrame({k: {"avg 3-10Y MGS move (bp)": v * 1e4, "FVOCI after-tax (RM m)": -H.loc["Total", "FVOCI"] * D * v * (1 - TAX) * 1e3,
                          "CET1 (bp)": -H.loc["Total", "FVOCI"] * D * v * (1 - TAX) / RWA * 1e4,
                          "BV (sen/share)": -H.loc["Total", "FVOCI"] * D * v * (1 - TAX) / SH * 100} for k, v in dy.items()}).T
headroom = pd.Series({"CET1 after proposed dividend": CET1_POST, "gap to 14% (bp)": (CET1_POST - 0.14) * 1e4,
                      "gap to 14% (RM m of CET1 capital)": (CET1_POST - 0.14) * RWA * 1e3,
                      "CET1 bp per +10bp parallel move": up100["CET1 hit (bp of RWA)"] / 10})

pd.set_option("display.width", 220, "display.max_columns", 20)
blocks = {"bb_holdings": H, "bb_mix": mix, "bb_reserve_walk": walk, "bb_up100": up100, "bb_marks": marks, "bb_headroom": headroom}
for k, v in blocks.items():
    print(f"\n== {k} ==")
    print(v.round(4).to_string())
    v.to_csv(f"{OUT}/{k}.csv")
print(f"\nCET1 cost of the 1H26 reserve move under BNM CAF 22.1/22.3: RM{cet1_cost_1h26:.0f}m = {cet1_cost_1h26 / 1e3 / RWA * 1e4:.1f}bp "
      f"(book value fell RM{-walk['attributable']:.0f}m)")
dy_1h = (at("2026-06-30") - at("2025-12-31")).mean() / 100
pred = -H.loc["Total", "FVOCI"] * D * dy_1h * 1e3
print(f"Back-test 1H26: avg 3-10Y MGS {dy_1h * 1e4:+.1f}bp -> model FVOCI fair-value change RM{pred:.0f}m pre-tax vs reported "
      f"RM{walk['fair-value change (market)']:.0f}m (ratio {walk['fair-value change (market)'] / pred:.2f}x; ~49% of the book is foreign paper "
      "and 56% corporate, so MGS alone understates)")
