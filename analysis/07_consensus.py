"""
07_consensus.py — Module 1: consensus stack, dispersion, revision momentum, whisper triangulation.
Every number carries a source tag + date + tier. Conflicting snapshots are shown side by side, not averaged
away; the 'mean' column is the simple average of the dated snapshots listed in `snapshots`.
Writes consensus.csv (repo root) and data/consensus_notes.csv.
"""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent

# ---- dated consensus snapshots (value, source, date, tier) ----
snap = {
    "FQ4 revenue ($bn)": [(50.50, "Goldman Sachs note citing consensus", "11/09/2026", 2),
                          (50.45, "Investing.com preview", "22/09/2026", 3),
                          (50.42, "Wall St consensus via web aggregator", "~23/09/2026", 3),
                          (50.62, "alt aggregator", "~23/09/2026", 3),
                          (50.92, "TipRanks", "~24/09/2026", 3),
                          (51.20, "Motley Fool / UBS-note article", "24/09/2026", 3)],
    "FQ4 non-GAAP EPS ($)": [(31.40, "Goldman Sachs note citing consensus", "11/09/2026", 2),
                             (31.16, "Investing.com preview", "22/09/2026", 3),
                             (31.14, "web aggregator", "~23/09/2026", 3),
                             (31.27, "user variables block / aggregator", "25/09/2026", 3),
                             (31.49, "TipRanks", "~24/09/2026", 3),
                             (31.56, "Motley Fool / UBS-note article", "24/09/2026", 3)],
    "FQ4 non-GAAP GM (%)": [(87.0, "Goldman Sachs note citing consensus", "11/09/2026", 2)],
    "FQ1 FY27 revenue guide ($bn)": [(56.7, "Goldman Sachs note citing consensus", "11/09/2026", 2)],
    "FQ1 FY27 GM guide (%)": [(87.5, "Goldman Sachs note citing consensus", "11/09/2026", 2)],
    "FQ1 FY27 EPS guide ($)": [(35.25, "Goldman Sachs note citing consensus", "11/09/2026", 2)],
    "FY27 revenue ($bn)": [(260.1, "Goldman Sachs note citing consensus (label ambiguous CY/FY)", "11/09/2026", 2),
                           (249.0, "implied: Wells Fargo $261.3bn is ~5% above Street", "23/09/2026", 2)],
    "FY27 EPS ($)": [(156.53, "24/7 Wall St citing consensus", "23/09/2026", 3)],
}
# ---- named sell-side estimates (Tier 2: firm + analyst + date) ----
named = {
    "FQ4 revenue ($bn)": [(52.4, "UBS (T. Arcuri) ~24/09"), (51.9, "Goldman (J. Schneider) 11/09"),
                          (50.78, "Stifel (B. Chin) 21/09"), (53.3, "Wells Fargo (A. Rakers) 23/09, implied from FY26 $132.3bn")],
    "FQ4 non-GAAP EPS ($)": [(32.50, "UBS ~24/09"), (32.54, "Goldman 11/09"), (32.00, "Stifel 21/09")],
    "FQ4 non-GAAP GM (%)": [(87.3, "Goldman 11/09"), (87.0, "Stifel 21/09")],
    "FQ1 FY27 revenue guide ($bn)": [(57.7, "Goldman 11/09"), (56.4, "Stifel 21/09")],
    "FQ1 FY27 GM guide (%)": [(88.1, "Goldman 11/09"), (88.2, "Stifel 21/09")],
    "FQ1 FY27 EPS guide ($)": [(37.06, "Goldman 11/09")],
    "FY27 revenue ($bn)": [(261.3, "Wells Fargo 23/09"), (262.3, "Goldman 11/09 (label ambiguous)")],
    "FY27 EPS ($)": [(166.0, "Wells Fargo 23/09"), (175.0, "BofA (V. Arya) 24/09: range $150-200, midpoint")],
}
guide = {  # Tier 1: 8-K 24/06/2026 + FQ3 prepared remarks
    "FQ4 revenue ($bn)": (49.0, 50.0, 51.0),
    "FQ4 non-GAAP EPS ($)": (30.0, 31.0, 32.0),
    "FQ4 non-GAAP GM (%)": (np.nan, 86.0, np.nan),
}
whisper = {  # triangulated below — range strings
    "FQ4 revenue ($bn)": "52.0-53.5", "FQ4 non-GAAP EPS ($)": "32.5-34.0", "FQ4 non-GAAP GM (%)": "87.0-87.5",
    "FQ1 FY27 revenue guide ($bn)": "57.5-59.5", "FQ1 FY27 GM guide (%)": "88.0-88.5", "FQ1 FY27 EPS guide ($)": "36.5-38.0",
    "FY27 revenue ($bn)": "260-275", "FY27 EPS ($)": "165-185",
}
revision = {
    "FQ4 revenue ($bn)": "90d: +16% (LSEG $43.58bn pre-guide 24/06 -> ~$50.5bn); 60d: ~+1%; 30d: +0.4% to +1.4% (50.5 -> 50.7-51.2). Rising.",
    "FQ4 non-GAAP EPS ($)": "90d: +23% (LSEG $25.50 pre-guide -> ~$31.3); 30d: +0% to +0.5%. Flat-to-rising.",
    "FQ4 non-GAAP GM (%)": "Street 87.0% already ~100bp above ~86% guide.",
    "FQ1 FY27 revenue guide ($bn)": "Only dated snapshot 11/09; sell-side notes since (Stifel 21/09, UBS, Citi 23/09) lean higher. Rising.",
    "FQ1 FY27 GM guide (%)": "n/a (single snapshot)",
    "FQ1 FY27 EPS guide ($)": "n/a (single snapshot)",
    "FY27 revenue ($bn)": "Wells raised FY27-28 EPS >10% (23/09); Goldman raised CY27 +4.9% (11/09). Rising.",
    "FY27 EPS ($)": "Rising (Wells +10%, BofA $150-200).",
}

rows = []
for metric, s in snap.items():
    vals = [v for v, *_ in s]
    nm = [v for v, _ in named.get(metric, [])]
    allv = vals + nm
    g = guide.get(metric, (np.nan, np.nan, np.nan))
    rows.append({
        "metric": metric,
        "guide_low": g[0], "guide_mid": g[1], "guide_high": g[2],
        "sellside_mean_of_snapshots": round(float(np.mean(vals)), 3),
        "snapshot_median": round(float(np.median(vals)), 3),
        "high_named_or_snapshot": max(allv), "low_named_or_snapshot": min(allv),
        "n_estimates": "~29 (TipRanks: 28 Buy/1 Hold ratings)" if metric.startswith("FQ4 rev") else "n/a",
        "revision_trend_30_60_90d": revision.get(metric, ""),
        "buyside_whisper_range": whisper.get(metric, ""),
        "dispersion_high_low_over_mean_pct": round(100 * (max(allv) - min(allv)) / np.mean(vals), 2),
        "snapshots": "; ".join(f"{v} ({src}, {d}, T{t})" for v, src, d, t in s),
        "named_estimates": "; ".join(f"{v} ({who})" for v, who in named.get(metric, [])),
    })

# qualitative / no-consensus metrics
qual = [
    ("FQ4 DRAM revenue ($bn)", "no public consensus; model ~39.5-41.5 (FQ3 $31.3bn, bits +8-13% incl. 14th week, price +10-18%)"),
    ("FQ4 NAND revenue ($bn)", "no public consensus; model ~11.8-13.3 (FQ3 $9.9bn)"),
    ("FQ4 HBM revenue", "not disclosed as a line; >$1bn cumulative HBM4 shipped by FQ3 (prepared remarks 24/06)"),
    ("FQ4 BU revenue", "FQ3: CMBU 13.8 / CDBU 11.5 / MCBU 11.5 / AEBU 4.6 ($bn); GM 83/87/87/79% (8-K 24/06). No consensus."),
    ("FQ4 opex (non-GAAP)", "guide ~$1.65bn (8-K). FY27 opex +~$1bn YoY, 2H-weighted (prepared remarks)"),
    ("FQ4 capex (net)", "guide ~$10bn; FY26 ~$27bn (prepared remarks). FY27: quarterly above FQ4 level; Street $45-48bn (BofA 24/09)"),
    ("FQ4 FCF", "guided to 'increase substantially again' vs FQ3 $18.3bn; SCA deposits (~$18bn cash) sit in financing CF, NOT FCF"),
    ("Inventory days", "FQ3 120 days; DRAM below 120 (prepared remarks)"),
    ("Tax / shares", "FQ4 tax ~15.0% (Pillar Two); ~1.15bn diluted shares (8-K)"),
    ("HBM4 share / qual", "NVIDIA certified all three for Vera Rubin HBM4 (Bloomberg 05/06); est. Rubin split Hynix 60-70% / Samsung 25-30% / MU remainder (Tier 3)"),
    ("HBM 2027", "industry reports: DRAM+HBM 2027 capacity sold out (Seeking Alpha/TweakTown, Tier 3); MU HBM 2026 sold out"),
    ("SCAs", "16 signed: ~20% DRAM & ~1/3 NAND volume CY26-30; target >=50% of revenue; largest have ceiling ~CQ2-26 market price + floor; ~40% of revenue fixed/ceiling when complete; RPO ~$100bn; deposits $22bn ($18bn cash) (prepared remarks + 10-Q, Tier 1)"),
    ("Contract price trajectory", "TrendForce: server DRAM +13-18% QoQ 3Q26 (09/07); 4Q26 outlook lifted but moderating; spot cooling 16/09 (DDR5 inquiries slow, NAND wafer -0.3% w/w)"),
    ("Capex / new fabs", "ID1 first wafer mid-CY27; ID2 late CY28; NY broke ground Jan-26; Tongluo (TW) output mid-CY27; Singapore HBM packaging 1H CY27 (prepared remarks)"),
    ("Capital return", "from 09/12/2026 intends to increase capital return; 'over time return 100% of excess cash' (prepared remarks). BofA: FCF could retire 8-10% of shares"),
]
qdf = pd.DataFrame(qual, columns=["metric", "revision_trend_30_60_90d"])
df = pd.concat([pd.DataFrame(rows), qdf], ignore_index=True)
df.to_csv(REPO / "consensus.csv", index=False)

# ---- revision momentum score (-2..+2): rising estimates + rising stock = high bar ----
est_30d_change = (np.mean([50.92, 51.20]) / 50.50 - 1) * 100   # FQ4 rev, 11/09 -> 24/09 snapshots
stock_20d = 15.15                                                # from setup_summary.csv
score = (1 if est_30d_change > 0.5 else 0) + (1 if stock_20d > 10 else 0)
notes = pd.Series({
    "fq4_rev_consensus_drift_11_to_24_sep_pct": round(est_30d_change, 2),
    "mu_20d_return_pct": stock_20d,
    "revision_momentum_score_-2_to_+2": score,
    "interpretation": "Estimates drifting up while stock +15% in 20d: bar is being raised into the print (high bar).",
    "whisper_a_top_quartile": "FQ4 rev $52.4-53.3bn (UBS, Wells-implied); EPS $32.50-32.54 (UBS, GS)",
    "whisper_b_estimize_ewhispers": "EarningsWhispers EPS whisper $34.14-35.20 vs $31.33 consensus (Tier 3, unverified - page did not render; possibly stale)",
    "whisper_c_previews": "GS 'above consensus' $51.9bn/$32.54 & FQ1 $57.7bn/88.1%; Stifel FQ1 $56.4bn/88.2%; UBS $52.4bn/$32.50",
    "whisper_d_prerally": "+15.1% 20d (86th pctile of prints) & +46% off 29/07 low: price already leans to a top-quartile outcome",
    "whisper_fq4": "rev $52.0-53.5bn, EPS $32.5-34.0",
    "whisper_fq1_guide": "rev $57.5-59.5bn, GM 88.0-88.5%, EPS $36.5-38.0",
})
notes.to_csv(ROOT / "data" / "consensus_notes.csv", header=["value"])
pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 70)
print(df[["metric", "guide_mid", "sellside_mean_of_snapshots", "snapshot_median", "high_named_or_snapshot",
          "low_named_or_snapshot", "buyside_whisper_range", "dispersion_high_low_over_mean_pct"]].to_string())
print(); print(notes.to_string())
