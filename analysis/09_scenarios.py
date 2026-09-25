"""
09_scenarios.py — Module 5: Print x Guide x Tone scenario matrix, tails, EV, P(beat AND down), histogram.

Structure
  1. Joint (print, guide) states come from the Module-2c Monte Carlo (08_beat_probability.py, same seeds/assumptions).
       Print  : Miss (<$50.2bn, <-1% vs cons) | In-line ($50.2-51.2bn) | Beat ($51.2-53.5bn) | Big beat (>$53.5bn)
       Guide  : Below cons (<-1.5% vs $56.7bn; 'severe' if <-5%) | In-line (+/-1.5%) |
                Above cons, below whisper ($57.55-58.5bn) | Above whisper (>$58.5bn)
       Sandbag tail T4 = FQ1 guide mid <= FQ4 actual (flat/down headline QoQ on the 13-week quarter).
  2. Tone | guide state (explicit conditional table below).
  3. 1-day reaction ~ N(mu, 4.25%), mu = a_print + a_guide + a_tone + positioning.
       Coefficients were back-tested on the last 10 prints (see CALIB): 8/10 direction hits, MAE 3.7pp,
       residual sd ~4.3pp -> cell sd 4.25pp.
  4. Fixed-probability exogenous tails (capex shock, pricing-peak language, SCA accounting noise, macro shock,
     export-control, management headline) replace base-matrix mass one-for-one.
Outputs: scenarios.csv (repo root), data/scenario_mc_summary.csv, data/scenario_cells.csv, data/calibration.csv,
         charts/scenario_move_hist.png
"""
import pathlib
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
(REPO / "charts").mkdir(exist_ok=True)

from mc_core import simulate, headline_stats, TAILS, CONS, WHISPER, A_P, A_G, A_T, PARAMS
CONS1, WHIS1, CONS4 = CONS["rev1"], WHISPER["rev1"], CONS["rev4"]
df, P_USED = simulate()
N = len(df)
print_state, guide_state, tone, is_tail = df.print_state.to_numpy(), df.guide_state.to_numpy(), df.tone.to_numpy(), df.is_tail.to_numpy()
move = df.move.to_numpy()
scen = df.tail_name.to_numpy().copy()
rev4, rev1, eps4 = df.rev4.to_numpy(), df.rev1.to_numpy(), df.eps4.to_numpy()

# ---------------- collapse base cells into named scenarios ----------------
pb = np.isin(print_state, ["Beat", "Big beat"])
def name_base(ps, gs, tn):
    beat_ = ps in ("Beat", "Big beat")
    if gs == "Sandbag (flat/down QoQ)":
        return "T4 Guide sandbagged: flat/down headline QoQ on 13-week FQ1"
    if ps == "Miss":
        return "S11 Print miss (any guide)"
    if ps == "In-line":
        return "S9 In-line print, guide >= consensus" if gs in ("In-line", "Above cons < whisper", "Above whisper") \
            else "S10 In-line print, guide below consensus"
    if gs == "Above whisper":
        return "S1 Blowout: beat + guide above whisper + very bullish tone" if tn == "Very bullish" \
            else "S2 Beat & raise above whisper (clean or mixed tone)"
    if gs == "Above cons < whisper":
        return "S4 Beat, guide above cons/below whisper, mixed tone" if tn == "Mixed" \
            else "S3 Beat, guide above cons/below whisper, clean/bullish"
    if gs == "In-line":
        return "S6 Beat, in-line guide, mixed tone" if tn == "Mixed" else "S5 Beat, in-line guide, clean/bullish"
    if gs in ("Below", "Below (severe)"):
        if tn == "Very bullish":
            return "S7 Beat, guide below cons but very bullish offsets (buyback/SCA expansion)"
        return "S8b Beat, guide well below cons (<-5%), clean/mixed" if gs == "Below (severe)" \
            else "S8a Beat, guide modestly below cons (13-week optics), clean/mixed"
    return "other"

key = pd.Series(list(zip(print_state, guide_state, tone)))
lut = {k: name_base(*k) for k in set(key)}
base_names = key.map(lut).to_numpy()
scen = np.where(is_tail, scen, base_names)

df = pd.DataFrame(dict(scenario=scen, move=move, print_state=print_state, guide_state=guide_state, tone=tone,
                       rev4=rev4, rev1=rev1, eps4=eps4))
df.loc[is_tail, ["print_state", "guide_state", "tone"]] = "exogenous"

META = {
    "S1 Blowout: beat + guide above whisper + very bullish tone": ("'Micron smashes estimates, guides FQ1 far above Street; 2027 sold out at higher prices; big buyback'", "Hynix/Samsung +5-10% next KRX session; SNDK/WDC/STX up; AMAT/LRCX up on capex; SOXX +2-3%"),
    "S2 Beat & raise above whisper (clean or mixed tone)": ("'Micron beat-and-raise tops whisper'", "Korea memory +3-6%; SOXX +1-2%"),
    "S3 Beat, guide above cons/below whisper, clean/bullish": ("'Solid beat, guide above consensus but not the buy-side number'", "memory peers flat-to-up; muted"),
    "S4 Beat, guide above cons/below whisper, mixed tone": ("'Beat and raise, but capex jump / price moderation cap the upside'", "memory peers down 1-4%; semicap up on capex"),
    "S5 Beat, in-line guide, clean/bullish": ("'Record quarter, in-line outlook; stock digests run'", "flat-to-down memory; SOXX flat"),
    "S6 Beat, in-line guide, mixed tone": ("'Growth deceleration and capex overshadow record results'", "Korea memory -3-6%; SNDK down"),
    "S7 Beat, guide below cons but very bullish offsets (buyback/SCA expansion)": ("'Soft headline guide, but $bn buyback / new SCAs reassure'", "mixed; MU outperforms peers"),
    "S8a Beat, guide modestly below cons (13-week optics), clean/mixed": ("'Micron's guide falls short as growth slows' (14->13 week optics)", "Korea memory -4-8%; SOXX -1-2%"),
    "S8b Beat, guide well below cons (<-5%), clean/mixed": ("'Micron outlook disappoints; peak-cycle fears return'", "Korea memory -6-10%; SNDK/WDC -5-10%; SOXX -2-3%"),
    "S9 In-line print, guide >= consensus": ("'In-line quarter, guide steadies nerves'", "flat"),
    "S10 In-line print, guide below consensus": ("'Micron merely meets the Street and guides light'", "Korea memory -5-8%"),
    "S11 Print miss (any guide)": ("'Micron misses as SCA price caps bite'", "memory complex -6-12%"),
    "T4 Guide sandbagged: flat/down headline QoQ on 13-week FQ1": ("'Micron guides revenue flat - peak growth is here' (14->13 week optics + conservatism)", "Korea memory -6-10%; SOXX -2-3%"),
}
for t, v in TAILS.items():
    META[t] = (v[3], v[4])

impl = 8.92   # live straddle-implied move (02/10 expiry), %
g = df.groupby("scenario")
tab = pd.DataFrame({
    "probability_pct": 100 * g.size() / N,
    "expected_1d_move_pct": g.move.mean(),
    "range_p10_pct": g.move.quantile(0.10),
    "range_p90_pct": g.move.quantile(0.90),
    "p_up_within_pct": 100 * g.move.apply(lambda s: (s > 0).mean()),
    "median_fq4_rev_bn": g.rev4.median(),
    "median_fq1_guide_bn": g.rev1.median(),
})
tab["headline"] = [META.get(s, ("", ""))[0] for s in tab.index]
tab["peer_readthrough"] = [META.get(s, ("", ""))[1] for s in tab.index]
tab = tab.sort_index()
tab.round(2).to_csv(REPO / "scenarios.csv")

# full cell matrix for transparency
cells = df[~is_tail].groupby(["print_state", "guide_state", "tone"]).move.agg(["size", "mean"]).reset_index()
cells["probability_pct"] = 100 * cells["size"] / N
cells.drop(columns="size").round(3).to_csv(ROOT / "data" / "scenario_cells.csv", index=False)

# ---------------- headline statistics (shared definition in mc_core.headline_stats) ----------------
S = headline_stats(df.assign(is_tail=is_tail), implied=impl)
pd.Series(S).to_csv(ROOT / "data" / "scenario_mc_summary.csv", header=["value"])

# ---------------- sensitivity: FQ1 per-week growth assumption x positioning penalty ----------------
# g_mu = 12% (bottom-up bear) ... 17.4% (Street-implied on a $52bn FQ4) ... 20% (GS/Stifel-implied)
sens = []
for g_mu in [0.12, 0.13, 0.14, 0.15, 0.16, 0.174, 0.20, 0.22]:
    for pos in [0.0, -1.5, -3.0]:
        d_, _ = simulate(g_mu=g_mu, POS=pos, N=60_000)
        h = headline_stats(d_, implied=impl)
        sens.append(dict(g_mu_pct=100 * g_mu, positioning=pos, EV=h["EV_1d_move_pct"], P_up=h["P_up_pct"],
                         P_down=h["P_down_pct"], P_FQ1_guide_gt_cons=h["P_FQ1_guide_gt_consensus_pct"],
                         P_beat_and_down=h["P_beat_AND_down_pct (sell-the-news)"]))
sens = pd.DataFrame(sens)
sens.round(2).to_csv(ROOT / "data" / "scenario_sensitivity.csv", index=False)

# ---------------- calibration table (judgmental labels, consensus per LSEG/Zacks where cited) ----------------
CALIB = [  # date, print, guide, tone, positioning, actual r1 %, note
    ("2024-03-20", "Big beat", "Above whisper", "Very bullish", -1.5, 14.13, "HBM sold out 2024/25; drift20 +18%"),
    ("2024-06-26", "Beat", "In-line", "Clean", -1.5, -7.12, "guide $7.6bn ~ cons $7.58bn (recall)"),
    ("2024-09-25", "Beat", "Above whisper", "Very bullish", 0.0, 14.73, "guide $8.7bn vs ~$8.3bn (recall)"),
    ("2024-12-18", "In-line", "Below (severe)", "Mixed", 0.0, -16.18, "guide $7.9bn vs ~$8.98bn (recall)"),
    ("2025-03-20", "Beat", "Above cons < whisper", "Mixed", 0.0, -8.04, "GM pressure/NAND"),
    ("2025-06-25", "Beat", "Above cons < whisper", "Clean", -1.5, -0.98, "drift20 +32%"),
    ("2025-09-23", "In-line", "Above cons < whisper", "Clean", -1.5, -2.82, "guide $12.5bn vs $11.94bn LSEG; drift20 +43%"),
    ("2025-12-17", "Beat", "Above whisper", "Very bullish", 0.0, 10.21, "guide $18.7bn vs ~$14.2bn LSEG (recall)"),
    ("2026-03-18", "Big beat", "Above whisper", "Mixed", -1.5, -3.78, "FY26 capex raised; r5 -17%"),
    ("2026-06-24", "Big beat", "Above whisper", "Very bullish", -1.5, 15.74, "guide $50bn vs $43.58bn LSEG; SCAs"),
]
cal = pd.DataFrame(CALIB, columns=["date", "print", "guide", "tone", "positioning", "actual_r1", "note"])
cal["predicted"] = cal["print"].map(A_P) + cal["guide"].map(A_G) + cal["tone"].map(A_T) + cal["positioning"]
cal["error"] = cal.actual_r1 - cal.predicted
cal["direction_hit"] = np.sign(cal.actual_r1) == np.sign(cal.predicted)
cal.to_csv(ROOT / "data" / "calibration.csv", index=False)

# ---------------- histogram (dataviz: diverging blue/red poles, hairline grid, 2px surface gaps) ----------------
SURF, INK, INK2, MUTED, GRID, BASE = "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7"
UP, DOWN = "#2a78d6", "#e34948"
bins = np.arange(-30, 30.5, 1.0)
hist, edges = np.histogram(df.move.clip(-29.99, 29.99), bins=bins)
pct = 100 * hist / N
centers = (edges[:-1] + edges[1:]) / 2
fig, ax = plt.subplots(figsize=(9.5, 4.6), dpi=150)
fig.patch.set_facecolor(SURF); ax.set_facecolor(SURF)
cols = [UP if c > 0 else DOWN for c in centers]
ax.bar(centers, pct, width=1.0, color=cols, edgecolor=SURF, linewidth=1.2, zorder=3)
ax.axhline(0, color=BASE, linewidth=1, zorder=4)
for x in (-impl, impl):
    ax.axvline(x, color=MUTED, linestyle=(0, (4, 3)), linewidth=1.2, zorder=2)
ax.axvline(S["EV_1d_move_pct"], color=INK, linewidth=1.5, zorder=5)
ymax = pct.max()
ax.text(impl + 0.4, ymax * 1.16, f"implied +{impl:.1f}%", color=INK2, fontsize=8.5, va="top")
ax.text(-impl - 0.4, ymax * 1.16, f"implied -{impl:.1f}%", color=INK2, fontsize=8.5, va="top", ha="right")
ax.text(S["EV_1d_move_pct"] + 0.4, ymax * 1.04, f"EV {S['EV_1d_move_pct']:+.1f}%", color=INK, fontsize=9, fontweight="bold")
ax.text(-27, ymax * 0.55, f"down day\n{S['P_down_pct']:.0f}%", color=INK, fontsize=10)
ax.text(19, ymax * 0.55, f"up day\n{S['P_up_pct']:.0f}%", color=INK, fontsize=10)
ax.set_xlim(-30, 30); ax.set_ylim(0, ymax * 1.2)
ax.set_xlabel("MU 1-day move after the 30/09/2026 print (%, close-to-close)", color=INK2, fontsize=9)
ax.set_ylabel("probability per 1pp bin (%)", color=INK2, fontsize=9)
ax.set_title("MU post-print move distribution: scenario Monte Carlo (200k draws)", color=INK, fontsize=11, loc="left")
ax.grid(axis="y", color=GRID, linewidth=0.6, zorder=0)
for sp in ("top", "right", "left"):
    ax.spines[sp].set_visible(False)
ax.spines["bottom"].set_color(BASE)
ax.tick_params(colors=MUTED, labelsize=8)
from matplotlib.patches import Patch
ax.legend(handles=[Patch(color=DOWN, label="down move"), Patch(color=UP, label="up move")], frameon=False,
          fontsize=8.5, loc="upper left", bbox_to_anchor=(0.0, 0.93), labelcolor=INK2)
fig.tight_layout()
fig.savefig(REPO / "charts" / "scenario_move_hist.png", facecolor=SURF)

pd.set_option("display.width", 250); pd.set_option("display.max_colwidth", 60)
print(tab[["probability_pct", "expected_1d_move_pct", "range_p10_pct", "range_p90_pct", "median_fq4_rev_bn",
           "median_fq1_guide_bn"]].round(2).to_string())
print("\nsum of probabilities:", round(tab.probability_pct.sum(), 3))
print(); print(pd.Series(S).round(2).to_string())
print("\nsensitivity (EV / P_up by FQ1 per-week growth and positioning):")
print(sens.pivot(index="g_mu_pct", columns="positioning", values="EV").round(2).to_string())
print(sens.pivot(index="g_mu_pct", columns="positioning", values="P_up").round(1).to_string())
print(sens[sens.positioning==-1.5][["g_mu_pct","P_FQ1_guide_gt_cons","P_beat_and_down"]].round(1).to_string())
print("\ncalibration:"); print(cal[["date", "predicted", "actual_r1", "error", "direction_hit"]].round(2).to_string())
print("MAE", round(cal.error.abs().mean(), 2), "resid sd", round(cal.error.std(), 2), "dir hit", cal.direction_hit.mean())
