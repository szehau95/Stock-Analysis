"""
mc_core.py — single source of truth for the Monte Carlo used by 08 (Module 2c) and 09 (Module 5).

CENTRAL assumptions (all in PARAMS; every run of 08/09 prints the params it used):
  FQ4 (14 wk) revenue = $50.0bn guide mid x (1 + beat); beat ~ mixture
        5%  N(-1.5%, 1.2%) | 65% N(+3.5%, 2.0%) | 30% N(+8.5%, 3.0%)
  FQ4 GM = 1 - $7.0bn/rev + N(+0.3pp, 0.5pp);  EPS from opex/other/tax/shares (reproduces $31.00 guide)
  FQ1 FY27 (13 wk) guide mid = FQ4 rev/14*13*(1+g_week); g_week ~ N(g_mu, g_sd), corr with FQ4 beat = rho
        g_mu = 15%: bottom-up bits +3-5% x price/mix +6-12% = ~13% (TrendForce: 4Q26 contract up but moderating;
        SCA ceilings on ~20% DRAM / ~1/3 NAND volume), +2pp credit for HBM4 mix and the Korea Sept 1-20 chip-export
        surge (+31% MoM like-for-like vs ~+5% seasonal; Hynix-led HBM4, so only partly transferable to MU).
        Street-implied g_week on a $52bn FQ4 is ~17.4% (GS/Stifel imply ~19.7% on their FQ4s) -> swept in sensitivity.
  Response: 1-day move ~ N(a_print + a_guide + a_tone + POS, SD)   (back-tested on last 10 prints)
  Exogenous tails with fixed probabilities replace base mass.
"""
import numpy as np
import pandas as pd

PARAMS = dict(
    N=200_000, seed=20260930,
    beat_mix_p=(0.05, 0.65, 0.30), beat_mu=(-1.5, 3.5, 8.5), beat_sd=(1.2, 2.0, 3.0),
    cogs4=7.0, gm_eps_mu=0.0030, gm_eps_sd=0.0050,
    opex4=(1.67, 0.03), other4=(0.55, 0.10), tax=(0.15, 0.005), shares=1.149,
    g_mu=0.15, g_sd=0.05, rho=0.25, bits=(0.03, 0.015), cost_per_bit=(0.0, 0.02),
    opex1=(1.70, 0.04), other1=(0.45, 0.10),
    POS=-1.5, SD=4.25,
)
CONS = dict(rev4=50.685, rev4_hi=51.20, eps4=31.34, gm4=87.0, rev1=56.7, gm1=87.5, eps1=35.25)
WHISPER = dict(rev4=52.75, eps4=33.25, rev1=58.5, gm1=88.25, eps1=37.25)

A_P = {"Miss": -6.0, "In-line": -2.5, "Beat": 0.5, "Big beat": 2.5}
A_G = {"Sandbag (flat/down QoQ)": -9.0, "Below (severe)": -8.0, "Below": -4.5, "In-line": -1.5,
       "Above cons < whisper": 2.5, "Above whisper": 7.0}
A_T = {"Mixed": -3.5, "Clean": 0.0, "Very bullish": 4.0}
TONE_GIVEN_GUIDE = {  # P(Very bullish, Clean, Mixed | guide state)
    "Above whisper": (0.45, 0.45, 0.10),
    "Above cons < whisper": (0.20, 0.50, 0.30),
    "In-line": (0.12, 0.48, 0.40),
    "Below": (0.10, 0.40, 0.50),
    "Below (severe)": (0.08, 0.32, 0.60),
    "Sandbag (flat/down QoQ)": (0.05, 0.35, 0.60),
}
TAILS = {  # name: (prob, mu, sd, headline, read-through)
    "T1 Capex shock (FY27 capex >= $55bn / greenfield pull-in)": (0.040, -8.0, 4.0,
        "'Micron's spending spree revives supply-glut fears'", "MU/Hynix/Samsung down; AMAT/LRCX/KLAC UP 3-6%"),
    "T2 Pricing-peak language (pricing flattening in 2027, SCA ceilings binding)": (0.030, -12.0, 4.0,
        "'Micron signals memory price peak'", "all memory -8..-15%; SNDK/WDC/STX down; SOXX -3..-5%"),
    "T3 SCA accounting noise (deposits/RPO/revenue-timing confusion)": (0.015, -4.0, 3.0,
        "'Quality-of-earnings questions cloud record quarter'", "MU-specific; peers flat"),
    "T5 Macro shock on the day (tariff Phase 2 incl. memory, rates, geopolitics)": (0.020, -6.0, 5.0,
        "'Chip stocks slide on tariff/macro headline'", "broad SOXX down; Korea memory down"),
    "T6 Export-control headline (China/HBM rules)": (0.010, -5.0, 4.0,
        "'New export curbs hit memory makers'", "Korea memory down more than MU; semicap down"),
    "T7 Management headline (CEO succession / exec exits)": (0.010, -2.0, 4.0,
        "'Micron names successor / exec shuffle'", "MU-specific"),
    "T8 Positive exogenous shock (memory tariff exemption / hyperscaler capex raise same day)": (0.015, 5.0, 4.0,
        "'Chip stocks jump on tariff relief / capex headline'", "SOXX up; Korea memory up"),
}


def simulate(**over):
    p = {**PARAMS, **over}
    rng = np.random.default_rng(p["seed"])
    N = p["N"]
    reg = rng.choice(3, size=N, p=p["beat_mix_p"])
    beat = (np.array(p["beat_mu"])[reg] + np.array(p["beat_sd"])[reg] * rng.standard_normal(N)) / 100
    rev4 = 50.0 * (1 + beat)
    gm4 = 1 - p["cogs4"] / rev4 + rng.normal(p["gm_eps_mu"], p["gm_eps_sd"], N)
    eps4 = (rev4 * gm4 - rng.normal(*p["opex4"], N) + rng.normal(*p["other4"], N)) \
        * (1 - rng.normal(*p["tax"], N)) / p["shares"]
    z2 = p["rho"] * (beat - beat.mean()) / beat.std() + np.sqrt(1 - p["rho"] ** 2) * rng.standard_normal(N)
    g_week = p["g_mu"] + p["g_sd"] * z2
    rev1 = rev4 / 14 * 13 * (1 + g_week)
    bits = rng.normal(*p["bits"], N)
    price = (1 + g_week) / (1 + bits) - 1
    gm1 = 1 - (1 - gm4) * (1 + rng.normal(*p["cost_per_bit"], N)) / (1 + price)
    eps1 = (rev1 * gm1 - rng.normal(*p["opex1"], N) + rng.normal(*p["other1"], N)) \
        * (1 - rng.normal(*p["tax"], N)) / p["shares"]

    print_state = np.select([rev4 < 50.2, rev4 < 51.2, rev4 < 53.5], ["Miss", "In-line", "Beat"], "Big beat")
    gap1 = rev1 / CONS["rev1"] - 1
    guide_state = np.select(
        [rev1 <= rev4, gap1 < -0.05, gap1 < -0.015, gap1 <= 0.015, rev1 <= WHISPER["rev1"]],
        ["Sandbag (flat/down QoQ)", "Below (severe)", "Below", "In-line", "Above cons < whisper"], "Above whisper")
    u = rng.random(N)
    tone = np.empty(N, dtype=object)
    for g, (pvb, pcl, _) in TONE_GIVEN_GUIDE.items():
        m = guide_state == g
        tone[m] = np.where(u[m] < pvb, "Very bullish", np.where(u[m] < pvb + pcl, "Clean", "Mixed"))
    mu = (pd.Series(print_state).map(A_P).to_numpy() + pd.Series(guide_state).map(A_G).to_numpy()
          + pd.Series(tone).map(A_T).to_numpy() + p["POS"])
    move = mu + p["SD"] * rng.standard_normal(N)

    names = list(TAILS)
    cum = np.cumsum([TAILS[t][0] for t in names])
    tail_idx = np.searchsorted(cum, rng.random(N), side="right")
    is_tail = tail_idx < len(names)
    tail_name = np.full(N, "", dtype=object)
    for k, nm in enumerate(names):
        m = tail_idx == k
        move[m] = TAILS[nm][1] + TAILS[nm][2] * rng.standard_normal(m.sum())
        tail_name[m] = nm
    return pd.DataFrame(dict(rev4=rev4, beat=beat, gm4=100 * gm4, eps4=eps4, g_week=g_week, rev1=rev1,
                             gm1=100 * gm1, eps1=eps1, print_state=print_state, guide_state=guide_state,
                             tone=tone, move=move, is_tail=is_tail, tail_name=tail_name)), p


def headline_stats(df, implied=8.92):
    beat_print = (df.rev4 > CONS["rev4"]) & (df.eps4 > CONS["eps4"])
    beat_raise = beat_print & (df.rev1 > CONS["rev1"])
    return {
        "EV_1d_move_pct": df.move.mean(),
        "median_1d_move_pct": df.move.median(),
        "P_up_pct": 100 * (df.move > 0).mean(),
        "P_down_pct": 100 * (df.move < 0).mean(),
        "P_rally_gt_+3pct": 100 * (df.move > 3).mean(),
        "P_selloff_lt_-3pct": 100 * (df.move < -3).mean(),
        "P_chop_within_+/-3pct": 100 * (df.move.abs() <= 3).mean(),
        "E_abs_move_pct": df.move.abs().mean(),
        f"P_abs_move_gt_implied_{implied}pct": 100 * (df.move.abs() > implied).mean(),
        "P_print_beat_pct": 100 * beat_print.mean(),
        "P_beat_AND_down_pct (sell-the-news)": 100 * (beat_print & (df.move < 0)).mean(),
        "P_down_given_beat_pct": 100 * (beat_print & (df.move < 0)).sum() / max(beat_print.sum(), 1),
        "P_beat_and_raise_pct": 100 * beat_raise.mean(),
        "P_down_given_beat_and_raise_pct": 100 * (beat_raise & (df.move < 0)).sum() / max(beat_raise.sum(), 1),
        "P_FQ1_guide_gt_consensus_pct": 100 * (df.rev1 > CONS["rev1"]).mean(),
        "P_exogenous_tails_pct": 100 * df.is_tail.mean(),
        "p05_move": df.move.quantile(0.05), "p25_move": df.move.quantile(0.25),
        "p75_move": df.move.quantile(0.75), "p95_move": df.move.quantile(0.95),
    }
