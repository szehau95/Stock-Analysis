"""
13_playbook.py — Module 9 inputs: gap-vs-close behaviour on MU print days (fade vs follow), threshold map,
and the MYT timeline for 30/09-01/10/2026. Writes data/playbook_gap_stats.csv, data/playbook_thresholds.csv
"""
import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
ev = pd.read_csv(REPO / "hist_moves.csv").tail(16).copy()
ev["intraday"] = (1 + ev.r1) / (1 + ev.gap) - 1          # open(t+1) -> close(t+1)
up, dn = ev[ev.gap > 0.02], ev[ev.gap < -0.02]
g = pd.Series({
    "n_gap_up_gt2": len(up), "mean_gap_up": 100 * up.gap.mean(), "mean_intraday_after_gap_up": 100 * up.intraday.mean(),
    "pct_gap_up_extended": 100 * (up.intraday > 0).mean(),
    "n_gap_down_lt-2": len(dn), "mean_gap_down": 100 * dn.gap.mean(), "mean_intraday_after_gap_down": 100 * dn.intraday.mean(),
    "pct_gap_down_extended": 100 * (dn.intraday < 0).mean(),
    "corr_gap_r1": ev[["gap", "r1"]].corr().iloc[0, 1],
})
g.to_csv(ROOT / "data" / "playbook_gap_stats.csv", header=["value"])

T = [
    ("1 FQ1 revenue guide mid", ">= $58.5bn (whisper)", "$57.55-58.5bn", "$55.85-57.55bn (cons $56.7bn +/-1.5%)", "$53.9-55.85bn",
     "< $53.9bn, or <= FQ4 actual (flat/down headline)", "S1/S2 +7..+11% | S3/S4 +3/-1% | S5/S6 -1/-5% | S8a -7% | S8b/T4 -11..-13%"),
    ("2 FQ1 GM guide", ">= 88.5%", "88.0-88.5%", "87.5-88.0% (cons 87.5%)", "87.0-87.5%", "< 87.0%", "tone driver: GM >= 88% offsets a light revenue headline"),
    ("3 FQ1 EPS guide", ">= $37.25", "$36.0-37.25", "$34.5-36.0 (cons $35.25)", "$33.0-34.5", "< $33.0", "confirms 1+2"),
    ("4 FQ4 actual revenue", ">= $53.5bn", "$52.75-53.5bn", "$51.2-52.75bn", "$50.2-51.2bn", "< $50.2bn", "print is ~85% likely to beat; only a miss is news"),
    ("4 FQ4 non-GAAP EPS", ">= $34.0", "$33.25-34.0", "$31.6-33.25", "$31.0-31.6", "< $31.0", "check tax (15%), shares (~1.15bn), other income (~$0.55bn)"),
    ("5 FY27 capex", "<= $42bn", "$42-45bn", "$45-50bn (BofA $45-48bn)", "$50-55bn", ">= $55bn (T1 capex shock)", "MU down / AMAT-LRCX up on T1"),
    ("6 Capital return", ">= $50bn authorisation + timeline", "$25-50bn", "framework only, restated", "no update", "deferred", "Very-bullish tone trigger"),
    ("6 SCA update", ">20 SCAs, >=50% revenue, deposits > $30bn, new-product premia", "more SCAs, deposits up", "16 SCAs restated", "", "ceilings binding / price bands questioned", ""),
    ("6 Pricing language", "'increases continue into CQ4 and 1H27'", "'prices up, moderating'", "'meaningful moderation' (June wording)", "'stabilising'", "'plateau / flat / declines'", "T2 if bearish"),
]
th = pd.DataFrame(T, columns=["read_order_item", "very_bullish", "bullish", "in_line", "bearish", "very_bearish", "maps_to"])
th.to_csv(ROOT / "data" / "playbook_thresholds.csv", index=False)
print(g.round(2).to_string())
print(ev[["report_date", "gap", "r1", "intraday"]].assign(**{c: lambda d, c=c: (100 * d[c]).round(1) for c in ["gap", "r1", "intraday"]}).to_string())
