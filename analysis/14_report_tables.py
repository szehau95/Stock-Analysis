"""
14_report_tables.py — renders the data tables used in MU_earnings_report.md directly from the CSV outputs
(so report numbers cannot drift from the code). Writes analysis/data/report_tables.md
"""
import pathlib
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
out = []


def esc(df):
    """escape pipes inside cell text so GitHub markdown tables keep their columns"""
    return df.apply(lambda col: col.map(lambda v: v.replace("|", "\\|") if isinstance(v, str) else v))


ga = pd.read_csv(ROOT / "data" / "guide_vs_actual.csv")
ev = pd.read_csv(REPO / "hist_moves.csv")
m = ga.merge(ev[["report_date", "r1", "r5", "pre20", "phase"]], on="report_date", how="left").tail(16)
t = pd.DataFrame({
    "Print": pd.to_datetime(m.report_date).dt.strftime("%d/%m/%Y"),
    "Phase": m.phase,
    "Rev $bn": (m.rev_act_m / 1000).round(2),
    "Guide mid $bn": (m.prev_rev_guide_mid_m / 1000).round(2),
    "Rev vs guide mid": m.rev_vs_guide_mid_pct.map(lambda x: f"{x:+.1f}%"),
    "GM vs guide": m.gm_vs_guide_bp.map(lambda x: f"{x:+.0f}bp"),
    "EPS": m.eps_act.round(2),
    "Next-Q guide QoQ": m.next_guide_qoq_pct.map(lambda x: f"{x:+.1f}%"),
    "Pre-20d": (100 * m.pre20).map(lambda x: f"{x:+.1f}%"),
    "1d": (100 * m.r1).map(lambda x: f"{x:+.1f}%"),
    "5d": (100 * m.r5).map(lambda x: f"{x:+.1f}%"),
})
out += ["## T_track16", t.pipe(esc).to_markdown(index=False)]

sc = pd.read_csv(REPO / "scenarios.csv")
sc["id"] = sc.scenario.str.split(" ").str[0]
order = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8a", "S8b", "S9", "S10", "S11", "T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8"]
sc["o"] = sc.id.map({k: i for i, k in enumerate(order)})
sc = sc.sort_values("o")
t2 = pd.DataFrame({
    "Scenario": sc.scenario,
    "Prob": sc.probability_pct.map(lambda x: f"{x:.1f}%"),
    "E[1d]": sc.expected_1d_move_pct.map(lambda x: f"{x:+.1f}%"),
    "Range p10/p90": [f"{a:+.0f}% / {b:+.0f}%" for a, b in zip(sc.range_p10_pct, sc.range_p90_pct)],
    "Med FQ4 rev": sc.median_fq4_rev_bn.map(lambda x: f"${x:.1f}bn"),
    "Med FQ1 guide": sc.median_fq1_guide_bn.map(lambda x: f"${x:.1f}bn"),
    "Headline": sc.headline,
    "Peer / read-through": sc.peer_readthrough,
})
out += ["## T_scen", t2.pipe(esc).to_markdown(index=False), f"\nsum = {sc.probability_pct.sum():.1f}%"]

sens = pd.read_csv(ROOT / "data" / "scenario_sensitivity.csv")
pv = sens.pivot(index="g_mu_pct", columns="positioning", values="EV").round(1)
pu = sens.pivot(index="g_mu_pct", columns="positioning", values="P_up").round(0)
s15 = sens[sens.positioning == -1.5].set_index("g_mu_pct")
t3 = pd.DataFrame({
    "FQ1 per-week growth (mean)": [f"{x:.1f}%" for x in pv.index],
    "P(FQ1 guide > $56.7bn)": [f"{s15.loc[x, 'P_FQ1_guide_gt_cons']:.0f}%" for x in pv.index],
    "EV (pos 0)": [f"{v:+.1f}%" for v in pv[0.0]],
    "EV (pos -1.5, central)": [f"{v:+.1f}%" for v in pv[-1.5]],
    "EV (pos -3)": [f"{v:+.1f}%" for v in pv[-3.0]],
    "P(up) central": [f"{v:.0f}%" for v in pu[-1.5]],
    "P(beat & down) central": [f"{s15.loc[x, 'P_beat_and_down']:.0f}%" for x in pv.index],
})
out += ["## T_sens", t3.pipe(esc).to_markdown(index=False)]

cal = pd.read_csv(ROOT / "data" / "calibration.csv")
t4 = cal.assign(date=pd.to_datetime(cal.date).dt.strftime("%d/%m/%Y"))[["date", "print", "guide", "tone", "positioning", "predicted", "actual_r1", "error", "direction_hit"]]
out += ["## T_calib", t4.round(1).pipe(esc).to_markdown(index=False)]

stn = pd.read_csv(ROOT / "data" / "stn_score_factors.csv")
out += ["## T_stn", stn[["factor", "weight", "score_-2_to_+2", "contribution", "evidence"]].round(3).pipe(esc).to_markdown(index=False)]

ed = pd.read_csv(REPO / "edge_scores.csv")
out += ["## T_edge", ed.pipe(esc).to_markdown(index=False)]

bk = pd.read_csv(ROOT / "data" / "book_exposure.csv")
out += ["## T_book", bk[["symbol", "quantity", "market_value_usd", "weight_pct_nlv", "beta_to_MU_print", "corr", "mu_beta_exposure_usd"]].round(2).pipe(esc).to_markdown(index=False)]

cons = pd.read_csv(REPO / "consensus.csv")
c = cons.dropna(subset=["sellside_mean_of_snapshots"])
t5 = pd.DataFrame({
    "Metric": c.metric,
    "Guide lo/mid/hi": [("—" if pd.isna(a) else f"{a:g}") + " / " + ("—" if pd.isna(b) else f"{b:g}") + " / " + ("—" if pd.isna(cc) else f"{cc:g}")
                        for a, b, cc in zip(c.guide_low, c.guide_mid, c.guide_high)],
    "Mean (snapshots)": c.sellside_mean_of_snapshots,
    "Median": c.snapshot_median,
    "High": c.high_named_or_snapshot,
    "Low": c.low_named_or_snapshot,
    "Whisper": c.buyside_whisper_range,
    "Dispersion": c.dispersion_high_low_over_mean_pct.map(lambda x: f"{x:.1f}%"),
})
out += ["## T_cons", t5.pipe(esc).to_markdown(index=False)]
(ROOT / "data" / "report_tables.md").write_text("\n\n".join(out))
print("\n\n".join(out))
