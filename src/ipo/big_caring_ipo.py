"""Big Caring Group Bhd IPO (indicative RM1.08) — deal metrics, valuation, scenarios and client sizing. As of 20/10/2026.

Sources: T1 = SC draft prospectus (exposure 02/04/2026, updated 28/07/2026); T2 = Reuters/The Edge/company statements (14-15/10/2026),
GWM Investment (MY) term email (20/10/2026); T3 = TradingView peer multiples (20/10/2026). Every estimate is labelled EST.
"""
import os
import numpy as np, pandas as pd

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = os.path.join(ROOT, "output", "ipo")
os.makedirs(OUT, exist_ok=True)

# ---- Deal terms ----
PRICE = 1.08                       # indicative issue price, GWM email (T2/internal)
SH_POST = 7_381_835_680            # enlarged shares after IPO (T1)
IPO_SH, OFS_SH, NEW_SH, GREENSHOE_SH = 1_882_368_000, 1_291_821_000, 590_547_000, 225_146_000  # T1
FEE = 0.025 * 1.08                 # 2.5% placement fee + 8% SST on the fee (GWM email)
LISTING_EXP = 50e6                 # EST: company's share of listing expenses (draft blank)
REPAY = 400e6                      # EST: bank borrowings repaid from proceeds (draft blank); range 300-500m
COST_DEBT, TAX = 0.045, 0.24       # EST: borrowing cost; statutory tax

# ---- Financials (RM) ----
FY = pd.DataFrame({
    "revenue": [1110.651e6, 2171.359e6, 3412.027e6, 4000e6],
    "ebitda": [106.549e6, 194.646e6, 380.717e6, np.nan],
    "pat": [41.194e6, 47.791e6, 143.019e6, 231.8e6],
    "patami": [37.020e6, 37.223e6, 122.295e6, np.nan],
}, index=["FY23", "FY24", "FY25", "FY26"])  # FY23-25 T1 (FYE June); FY26 revenue/PAT T2 (company via Reuters, 14/10/2026)
BS25 = dict(borrowings=985.277e6 + 345.906e6, leases=250.489e6 + 67.102e6, cash=294.896e6, other_inv=51.138e6,
            equity_owners=422.082e6, intangibles=1343.708e6, nci=106.699e6, cfo=350.919e6, capex=85.4e6,
            supplier_income=88.046e6 + 32.272e6, pbt=219.324e6)  # T1, 30/06/2025
STORES_SEP26, STORES_ADDED_FY26 = 668, 58  # T2

# FY26 PATAMI (EST): FY25 NCI share of PAT applied to FY26 PAT; range 10%-18%
nci_share25 = (FY.loc["FY25", "pat"] - FY.loc["FY25", "patami"]) / FY.loc["FY25", "pat"]
patami26 = {"low": FY.loc["FY26", "pat"] * (1 - 0.18), "base": FY.loc["FY26", "pat"] * (1 - nci_share25), "high": FY.loc["FY26", "pat"] * (1 - 0.10)}
int_saving = REPAY * COST_DEBT * (1 - TAX)
patami26_pf = patami26["base"] + int_saving

# ---- Deal metrics ----
mcap = PRICE * SH_POST
deal = {
    "Market cap at RM1.08 (RM bn)": mcap / 1e9,
    "Base IPO size (RM bn)": IPO_SH * PRICE / 1e9,
    "… of which offer for sale (RM bn)": OFS_SH * PRICE / 1e9,
    "… of which new shares to company (RM bn)": NEW_SH * PRICE / 1e9,
    "OFS share of base deal": OFS_SH / IPO_SH,
    "Deal incl. greenshoe (RM bn)": (IPO_SH + GREENSHOE_SH) * PRICE / 1e9,
    "Free float post-IPO (base)": IPO_SH / SH_POST,
    "Valuation vs RM12bn pre-marketing talk (T2)": mcap / 12e9 - 1,
    "Valuation vs RM20bn earlier report (T3)": mcap / 20e9 - 1,
}

# ---- Multiples ----
net_bank_debt25 = BS25["borrowings"] - BS25["cash"] - BS25["other_inv"]
net_proceeds = NEW_SH * PRICE - LISTING_EXP
nbd_pf = net_bank_debt25 - net_proceeds  # FY25 balance sheet, pro forma for IPO cash (EST)
ebitda26_est = FY.loc["FY26", "revenue"] * 0.12  # EST: FY25 IFRS16 margin 11.2% + 0.8pp operating leverage
ev_pf = mcap + nbd_pf + BS25["leases"] + BS25["nci"]
eq_pf = BS25["equity_owners"] + patami26["base"] - 24.96e6 + net_proceeds  # FY25 equity + FY26 retained (less RM24.96m dividend) + IPO
mult = {
    "P/E FY25 PATAMI (T1)": mcap / FY.loc["FY25", "patami"],
    "P/E FY26 PAT, group (T2)": mcap / FY.loc["FY26", "pat"],
    "P/E FY26 PATAMI EST (base; range)": mcap / patami26["base"],
    "  … range low/high": (mcap / patami26["high"], mcap / patami26["low"]),
    "P/E FY26 PATAMI EST, pro forma interest saving": mcap / patami26_pf,
    "P/S FY26": mcap / FY.loc["FY26", "revenue"],
    "EV/EBITDA FY25 (IFRS16, pro forma IPO cash)": ev_pf / FY.loc["FY25", "ebitda"],
    "EV/EBITDA FY26 EST (12% margin)": ev_pf / ebitda26_est,
    "Net bank debt / EBITDA FY25 (pre-IPO)": net_bank_debt25 / FY.loc["FY25", "ebitda"],
    "Net bank debt / EBITDA pro forma IPO (FY25 basis)": nbd_pf / FY.loc["FY25", "ebitda"],
    "Gearing incl. leases FY25 (T1)": 3.1,
    "Pro forma P/B (EST)": mcap / eq_pf,
    "Pro forma NTA (RM bn, EST)": (eq_pf - BS25["intangibles"]) / 1e9,
    "Supplier income / PBT FY25 (T1)": BS25["supplier_income"] / BS25["pbt"],
    "FCF FY25 (CFO - capex) / mkt cap": (BS25["cfo"] - BS25["capex"]) / mcap,
    "Dividend yield @50% payout on FY26 PATAMI EST": 0.5 * patami26_pf / mcap,
}

# ---- Peers (T3 TradingView, 20/10/2026) ----
peers = pd.DataFrame([
    ("99 Speed Mart", "MY consumer staple", 38.7, 27, 1.4), ("QL Resources", "MY consumer staple", 30.6, 0, 1.3),
    ("Farm Fresh", "MY consumer staple", 26.9, 9, 1.1), ("IHH Healthcare", "MY healthcare", 31.4, 1, 1.4),
    ("KPJ Healthcare", "MY healthcare", 26.4, 15, 1.9), ("Sunway Healthcare", "MY healthcare (IPO 03/2026)", 84.6, np.nan, np.nan),
    ("MR D.I.Y.", "MY retail", 17.4, 4, 7.4), ("FPT Retail (Long Chau)", "Regional pharmacy", 22.8, 111, np.nan),
    ("Yifeng Pharmacy", "Regional pharmacy", 17.7, 13, 2.8), ("DaShenLin", "Regional pharmacy", 15.1, 29, 4.7),
    ("LBX Pharmacy", "Regional pharmacy", 25.7, 4, 3.9), ("MatsukiyoCocokara", "Regional pharmacy/drugstore", 17.8, 5, 2.2),
    ("Tsuruha", "Regional pharmacy/drugstore", 17.5, 16, 2.2), ("DFI Retail (Guardian)", "Regional health & beauty", 11.7, np.nan, 5.0),
], columns=["Company", "Group", "P/E TTM", "EPS growth % TTM", "Div. yield %"])
med = peers[peers.Company != "Sunway Healthcare"].groupby(peers.Group.str.split(" ").str[0] + " " + peers.Group.str.split(" ").str[1])["P/E TTM"].median()
my_growth_median = peers[peers.Group.isin(["MY consumer staple", "MY healthcare"]) & (peers.Company != "Sunway Healthcare")]["P/E TTM"].median()
regional_median = peers[peers.Group.str.startswith("Regional")]["P/E TTM"].median()

# ---- FY27E scenarios and 12-month value (EST) ----
store_avg26 = (STORES_SEP26 - 12 - STORES_ADDED_FY26) + STORES_ADDED_FY26 / 2   # start-FY26 base + half-year of FY26 openings
SCEN = {  # sssg, new stores FY27, new-store productivity, PATAMI margin change (pp), target P/E, probability
    "Bear": dict(sssg=0.02, adds=35, prod=0.6, dm=-0.003, pe=24, p=0.25),
    "Base": dict(sssg=0.07, adds=45, prod=0.7, dm=+0.002, pe=32, p=0.50),
    "Bull": dict(sssg=0.09, adds=50, prod=0.8, dm=+0.004, pe=38, p=0.25),
}
rows = []
m26 = patami26_pf / FY.loc["FY26", "revenue"]
start27 = STORES_SEP26 - 12
for k, s in SCEN.items():
    avg27 = start27 + s["adds"] / 2
    store_growth = (avg27 / store_avg26 - 1) * s["prod"]
    rev27 = FY.loc["FY26", "revenue"] * (1 + s["sssg"] + store_growth)
    pat27 = rev27 * (m26 + s["dm"])
    val = pat27 * s["pe"] / SH_POST
    div12 = 0.5 * patami26_pf / SH_POST
    rows.append(dict(scenario=k, prob=s["p"], sssg=s["sssg"], rev_growth=rev27 / FY.loc["FY26", "revenue"] - 1,
                     patami27=pat27 / 1e6, patami_growth=pat27 / patami26_pf - 1, target_pe=s["pe"], value_ps=val,
                     ret_vs_ipo=val / PRICE - 1, total_ret_net_fee=(val + div12) / (PRICE * (1 + FEE)) - 1))
SC = pd.DataFrame(rows).set_index("scenario")
ev_val = (SC.value_ps * SC.prob).sum()
ev_tr = (SC.total_ret_net_fee * SC.prob).sum()
implied_pe27 = mcap / (SC.loc["Base", "patami27"] * 1e6)
peg = implied_pe27 / (SC.loc["Base", "patami_growth"] * 100)

# ---- Aftermarket reference (T3 TradingView first bars; T2 IPO prices) ----
ref = pd.DataFrame([
    ("99 Speed Mart", "09/09/2024", 1.65, 1.88, 3.09), ("Sunway Healthcare", "18/03/2026", 1.45, 1.85, 2.09),
], columns=["IPO", "Listed", "IPO price", "Day-1 close", "Price 20/10/2026"])
ref["Day-1"] = ref["Day-1 close"] / ref["IPO price"] - 1
ref["Since IPO"] = ref["Price 20/10/2026"] / ref["IPO price"] - 1

# ---- Client sizing: 65-year-old, RM50m net worth, RM250k bid ----
NW, BID = 50e6, 250_000
fills = [0.3, 0.6, 1.0]
day1 = [-0.10, 0.0, 0.027, 0.10, 0.20, 0.30]
cl = pd.DataFrame(index=[f"{int(f*100)}% fill (RM{BID*f/1e3:,.0f}k)" for f in fills],
                  columns=[f"Day-1 {d:+.1%}" for d in day1])
for f in fills:
    alloc = BID * f
    for d in day1:
        cl.loc[f"{int(f*100)}% fill (RM{alloc/1e3:,.0f}k)", f"Day-1 {d:+.1%}"] = alloc * (1 + d) - alloc * (1 + FEE) - alloc * (1 + d) * 0.002
cl = cl.astype(float)
sizing = {"Bid as % of net worth": BID / NW, "Fee incl. SST": FEE, "Fee on full fill (RM)": BID * FEE,
          "Break-even day-1 return (fee + ~0.2% exit costs)": FEE + 0.002,
          "Bear-case 12m loss on full fill (RM)": BID * SC.loc["Bear", "total_ret_net_fee"],
          "Bear-case loss as % of net worth": BID * SC.loc["Bear", "total_ret_net_fee"] / NW}

# ---- Output ----
def md_kv(d, pct_keys=()):
    lines = ["| Metric | Value |", "|---|---|"]
    for k, v in d.items():
        if isinstance(v, tuple):
            s = " / ".join(f"{x:.1f}×" for x in v)
        elif "RM bn" in k or "(RM)" in k:
            s = f"{v:,.2f}" if "RM bn" in k else f"RM{v:,.0f}"
        elif any(t in k for t in ("share of", "Free float", "vs RM", "/ PBT", "/ mkt cap", "yield", "% of", "Fee incl", "Break-even")):
            s = f"{v:+.1%}" if "vs RM" in k else f"{v:.1%}"
        else:
            s = f"{v:.1f}×"
        lines.append(f"| {k} | {s} |")
    return "\n".join(lines)


with open(os.path.join(OUT, "big_caring_tables.md"), "w") as f:
    f.write("## DEAL\n\n" + md_kv(deal) + "\n\n")
    f.write("## FIN\n\n" + (FY / 1e6).round(1).to_markdown() + f"\n\nFY26 PATAMI EST: base RM{patami26['base']/1e6:.1f}m (FY25 NCI share {nci_share25:.1%}); "
            f"range RM{patami26['low']/1e6:.1f}m–RM{patami26['high']/1e6:.1f}m; pro forma +RM{int_saving/1e6:.1f}m interest saving = RM{patami26_pf/1e6:.1f}m.\n\n")
    f.write("## MULT\n\n" + md_kv(mult) + "\n\n")
    f.write("## PEERS\n\n" + peers.to_markdown(index=False) + f"\n\nMedian P/E — MY consumer/healthcare (ex-Sunway Healthcare): {my_growth_median:.1f}×; regional pharmacy/drugstore: {regional_median:.1f}×.\n\n")
    sc_out = SC.copy()
    for c in ["prob", "sssg", "rev_growth", "patami_growth", "ret_vs_ipo", "total_ret_net_fee"]:
        sc_out[c] = sc_out[c].map(lambda x: f"{x:.0%}" if c == "prob" else f"{x:+.1%}")
    sc_out["patami27"] = sc_out["patami27"].map(lambda x: f"{x:.0f}")
    sc_out["value_ps"] = sc_out["value_ps"].map(lambda x: f"RM{x:.2f}")
    f.write("## SCEN\n\n" + sc_out.to_markdown() + f"\n\nProbability-weighted value RM{ev_val:.2f}; expected 12m total return net of fee {ev_tr:+.1%}. "
            f"Implied P/E on base FY27E: {implied_pe27:.1f}×; PEG {peg:.1f}.\n\n")
    r = ref.copy()
    for c in ["Day-1", "Since IPO"]:
        r[c] = r[c].map(lambda x: f"{x:+.1%}")
    f.write("## REF\n\n" + r.to_markdown(index=False) + "\n\n")
    f.write("## SIZING\n\n" + md_kv(sizing) + "\n\n")
    f.write("## CLIENT\n\n" + cl.round(0).map(lambda x: f"RM{x:,.0f}").to_markdown() + "\n")

pd.set_option("display.width", 220)
print({k: (round(v, 3) if not isinstance(v, tuple) else tuple(round(x, 1) for x in v)) for k, v in deal.items()})
print({k: (round(v, 3) if not isinstance(v, tuple) else tuple(round(x, 1) for x in v)) for k, v in mult.items()})
print("PATAMI26", {k: round(v / 1e6, 1) for k, v in patami26.items()}, "pf", round(patami26_pf / 1e6, 1), "store_avg26", store_avg26)
print("medians", med.round(1).to_dict(), "MY", my_growth_median, "regional", regional_median)
print(SC.round(3).to_string())
print("EV value", round(ev_val, 3), "EV TR net fee", round(ev_tr, 4), "implied PE27", round(implied_pe27, 1), "PEG", round(peg, 2))
print(ref.round(3).to_string())
print({k: round(v, 4) for k, v in sizing.items()})
print(cl.round(0).to_string())

# ---- Assemble report: substitute {{KEY}} blocks from the tables file into the narrative ----
import re
blocks = dict(re.findall(r"^## (\S+)\n\n(.*?)(?=^## |\Z)", open(os.path.join(OUT, "big_caring_tables.md")).read(), flags=re.S | re.M))
narr = os.path.join(ROOT, "reports", "ipo_big_caring_narrative.md")
if os.path.exists(narr):
    txt = open(narr).read()
    missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", txt)) - set(blocks))
    assert not missing, f"missing tables: {missing}"
    open(os.path.join(ROOT, "reports", "IPO_Big_Caring_Group_20102026.md"), "w").write(re.sub(r"\{\{(\w+)\}\}", lambda m: blocks[m.group(1)].strip(), txt))
    print("report assembled")
