"""Monte Carlo race model - 2026 Bahrain GP at Sepang (04/10/2026).

Lap-by-lap simulation: grid -> start shock -> lap-1 incidents -> per-lap pace,
tyre deg, overtaking friction, 2-stop strategy, SC/VSC (gap compression + cheap
stops), rain scenarios (dry / mixed / wet incl. red flag), DNF hazard.

Two layers of randomness:
  * epistemic (per batch): true pace offsets, rain-scenario mix, SC rate
  * aleatory (per sim): everything that happens on race day
The 90% interval on P(win) is the 5th-95th percentile across batches.

Inputs are taken from sources cited in REPORT.md; every number marked
ASSUMPTION is a modelling judgement, not a measurement.
"""
import argparse
import json

import numpy as np

LAPS = 56            # Sepang 5.543 km, 2017 race distance
PIT_LOSS = 21.5      # s, green-flag pit loss (ASSUMPTION, Sepang historic ~20-22 s)
SC_PIT_LOSS = 11.0
VSC_PIT_LOSS = 13.0

# grid order after penalties (RaceFans / FIA, 03/10/2026)
# code, team, dry race-pace delta vs VER s/lap (prior mean), epistemic sd,
# wet skill s/lap (negative = faster), race DNF prob, launch bias s
DRIVERS = [
    # FP2 long runs (motorsport.com): VER 0, RUS +0.19, LEC +0.32, NOR +0.43, PIA +0.78
    ("VER", "RBR", 0.00, 0.00, -0.25, 0.07, 0.00),
    ("HAM", "FER", 0.28, 0.15, -0.15, 0.05, -0.05),  # no clean long run published
    ("ANT", "MER", 0.15, 0.17, 0.00, 0.04, 0.00),    # no clean long run published; FP3 P1
    ("LEC", "FER", 0.30, 0.12, -0.05, 0.05, -0.05),
    ("NOR", "MCL", 0.42, 0.12, -0.05, 0.04, 0.00),
    ("PIA", "MCL", 0.65, 0.15, 0.00, 0.04, 0.00),
    ("RUS", "MER", 0.17, 0.12, -0.05, 0.04, 0.00),
    ("HAD", "RBR", 0.22, 0.17, 0.00, 0.08, 0.00),    # PU components already over limit
    ("GAS", "ALP", 1.28, 0.20, 0.00, 0.06, 0.00),
    ("BOR", "AUD", 1.75, 0.20, 0.00, 0.07, 0.00),
    ("LAW", "RBU", 1.63, 0.20, 0.00, 0.07, 0.00),
    ("ALO", "AST", 1.97, 0.20, -0.10, 0.08, 0.00),
    ("SAI", "WIL", 2.58, 0.20, 0.00, 0.06, 0.00),
    ("STR", "AST", 1.97, 0.20, 0.00, 0.08, 0.00),
    ("HUL", "AUD", 1.75, 0.20, 0.00, 0.07, 0.00),
    ("BEA", "HAA", 2.04, 0.20, 0.00, 0.07, 0.00),
    ("OCO", "HAA", 2.04, 0.20, 0.00, 0.07, 0.00),
    ("ALB", "WIL", 2.58, 0.20, 0.00, 0.06, 0.00),
    ("BOT", "CAD", 2.92, 0.20, 0.00, 0.08, 0.00),
    ("PER", "CAD", 2.92, 0.20, -0.05, 0.08, 0.00),
    ("COL", "ALP", 1.30, 0.20, 0.00, 0.06, 0.00),
    ("LIN", "RBU", 1.63, 0.20, 0.00, 0.07, 0.00),
]

BASE = dict(
    p_rain=(0.40, 0.45, 0.15),   # dry / mixed / wet (ASSUMPTION from Open-Meteo + BBC)
    rain_conc=20.0,              # Dirichlet concentration for epistemic rain mix
    p_sc=(0.45, 0.65, 0.85),     # P(>=1 SC/VSC) by scenario (ASSUMPTION)
    deg=0.10,                    # s/lap per lap of tyre age, net of fuel burn
    deg_sd=0.05,                 # per-sim tyre-deg multiplier sd
    form_sd=0.06,                # per-sim race-day pace sd, s/lap
    start_sd=0.35,               # s, launch/T1 shock
    grid_gap=0.40,               # s per grid slot at T1 (pole->lap-1 lead ~70%)
    pass_base=0.08,              # per-lap pass prob when on par & within range
    pass_slope=0.6,              # extra pass prob per s of pace advantage
    pace_shift={},               # code -> s/lap added (sensitivity)
    wet_shift={},
    dnf_set={},                  # code -> race DNF prob override
)


def simulate(cfg, n_batches=60, per_batch=2000, seed=1):
    rng = np.random.default_rng(seed)
    N = len(DRIVERS)
    S = n_batches * per_batch
    batch = np.repeat(np.arange(n_batches), per_batch)

    codes = [d[0] for d in DRIVERS]
    mu = np.array([d[2] + cfg["pace_shift"].get(d[0], 0.0) for d in DRIVERS])
    esd = np.array([d[3] for d in DRIVERS])
    wet = np.array([d[4] + cfg["wet_shift"].get(d[0], 0.0) for d in DRIVERS])
    pdnf = np.array([cfg["dnf_set"].get(d[0], d[5]) for d in DRIVERS])
    launch = np.array([d[6] for d in DRIVERS])
    grid = np.arange(N)

    # ---- epistemic layer (per batch) ----
    pace_b = mu + rng.normal(0, 1, (n_batches, N)) * esd
    rain_b = rng.dirichlet(np.array(cfg["p_rain"]) * cfg["rain_conc"], n_batches)
    sc_mult_b = np.clip(rng.normal(1, 0.15, n_batches), 0.6, 1.4)

    pace = pace_b[batch] + rng.normal(0, cfg["form_sd"], (S, N))          # race-day form
    u = rng.random(S)
    cum = np.cumsum(rain_b[batch], axis=1)
    scen = (u[:, None] > cum[:, :2]).sum(1)                       # 0 dry 1 mixed 2 wet
    p_sc = np.minimum(np.array(cfg["p_sc"])[scen] * sc_mult_b[batch], 0.97)
    degm = np.clip(rng.normal(1, cfg["deg_sd"], (S, N)), 0.7, 1.3)
    wet_noise = rng.normal(0, 0.30, (S, N))

    # rain window
    w0 = np.where(scen == 2, rng.integers(0, 31, S), rng.integers(5, 46, S))
    wl = np.where(scen == 2, rng.integers(15, 41, S), rng.integers(6, 21, S))
    w1 = np.minimum(w0 + wl, LAPS + 5)
    w0 = np.where(scen == 0, LAPS + 10, w0)
    w1 = np.where(scen == 0, LAPS + 10, w1)
    inten = np.where(scen == 2, 1.0, 0.6)
    red_flag = (scen == 2) & (rng.random(S) < 0.40)
    red_lap = w0 + 2

    # strategy: 2 dry stops
    s1 = rng.integers(15, 20, (S, N))
    s2 = np.minimum(s1 + rng.integers(17, 22, (S, N)), LAPS - 4)
    stops = [s1, s2]
    if (scen > 0).any():
        # rain scenarios: keep dry stops before window, add inter-on / slick-on
        in_w = (scen > 0)[:, None]
        on = w0[:, None] + rng.integers(0, 4, (S, N))
        off = w1[:, None] + rng.integers(0, 4, (S, N))
        s1 = np.where(in_w & (s1 >= w0[:, None]), 999, s1)
        s2 = np.where(in_w & (s2 >= w0[:, None]), 999, s2)
        s3 = np.where(in_w, on, 999)
        s4 = np.where(in_w & (off < LAPS - 1), off, 999)
        stops = [s1, s2, s3, s4]
    stops = np.stack(stops, -1)                                   # S,N,K

    # SC events (at most one, plus 25% chance of a second)
    has_sc = rng.random(S) < p_sc
    sc_lap = np.where(has_sc, rng.integers(2, LAPS - 1, S), 999)
    sc_type = rng.random(S) < 0.6                                  # True=SC, False=VSC
    sc2 = has_sc & (rng.random(S) < 0.25)
    sc_lap2 = np.where(sc2, rng.integers(2, LAPS - 1, S), 999)

    # DNF laps
    crash_mult = np.where(scen == 2, 2.0, np.where(scen == 1, 1.4, 1.0))
    p_d = np.minimum(pdnf[None, :] * crash_mult[:, None], 0.5)
    dnf = rng.random((S, N)) < p_d
    dnf_lap = np.where(dnf, rng.integers(1, LAPS + 1, (S, N)), 999)
    # lap-1 incident
    p_inc = np.where(grid == 0, 0.015, np.where(grid < 4, 0.03, np.where(grid < 10, 0.045, 0.055)))
    inc = rng.random((S, N)) < p_inc
    inc_dnf = inc & (rng.random((S, N)) < 0.4)
    dnf_lap = np.where(inc_dnf, 1, dnf_lap)
    inc_loss = np.where(inc & ~inc_dnf, rng.uniform(5, 30, (S, N)), 0.0)

    # ---- race ----
    T = grid[None, :] * cfg["grid_gap"] + rng.normal(0, cfg["start_sd"], (S, N)) + launch + inc_loss
    T = T.astype(float)
    age = np.zeros((S, N))
    alive = np.ones((S, N), bool)
    rows = np.arange(S)[:, None]

    for lap in range(1, LAPS + 1):
        alive &= dnf_lap > lap - 1
        inw = (lap >= w0) & (lap < w1)
        rf = (lap - w0) / np.maximum(w1 - w0, 1)
        lapnoise = np.where(inw, 0.8 + 0.4 * (scen == 2), 0.30)
        lt = pace + cfg["deg"] * degm * age + rng.normal(0, 1, (S, N)) * lapnoise[:, None]
        lt += np.where(inw, inten, 0)[:, None] * (wet + wet_noise)
        pit = (stops == lap).any(-1) & alive
        is_sc = (lap == sc_lap) | (lap == sc_lap2)
        # SC: pull stops forward if within 8 laps
        if is_sc.any():
            pull = is_sc[:, None, None] & (stops > lap) & (stops - lap <= 8) & (lap >= 8)
            first_pull = pull & (np.cumsum(pull, -1) == 1)
            stops = np.where(first_pull, lap, stops)
            pit = (stops == lap).any(-1) & alive
        loss = np.where(is_sc[:, None], np.where(sc_type[:, None], SC_PIT_LOSS, VSC_PIT_LOSS), PIT_LOSS)
        slow = rng.random((S, N)) < 0.04
        pitcost = pit * (loss + rng.normal(0, 0.4, (S, N)) + slow * rng.uniform(2, 8, (S, N)) + 1.0)
        rflap = red_flag & (lap == red_lap)
        pitcost = np.where(rflap[:, None], 0.0, pitcost)          # free change under red
        age = np.where(pit | rflap[:, None], 0, age + 1)
        Tfree = T + lt + pitcost
        Tfree = np.where(alive, Tfree, 1e9)

        # overtaking friction, processed in previous-lap order
        order = np.argsort(np.where(alive, T, 1e9), axis=1)
        Tnew = Tfree.copy()
        pass_p = cfg["pass_base"] * (1.6 if lap == 1 else 1.0)
        for k in range(1, N):
            i = order[:, k]
            m = order[:, k - 1]
            ti = Tfree[rows[:, 0], i]
            tm = Tnew[rows[:, 0], m]
            nopit = ~pit[rows[:, 0], i] & ~pit[rows[:, 0], m]
            close = (ti < tm + 0.3) & nopit & (ti < 1e8) & ~is_sc
            adv = tm + 0.3 - ti
            p = np.clip(pass_p + cfg["pass_slope"] * adv, 0, 0.9)
            ok = rng.random(S) < p
            ti_new = np.where(close & ok, ti + 0.2, np.where(close, tm + 0.3, ti))
            Tnew[rows[:, 0], i] = ti_new
        T = Tnew

        # SC / red flag gap compression
        comp = is_sc & sc_type | rflap
        if comp.any():
            o = np.argsort(T, axis=1)
            rank = np.argsort(o, axis=1)
            lead = T.min(1, keepdims=True)
            Tc = lead + 0.8 * rank
            T = np.where(comp[:, None] & alive, Tc, T)
        T = np.where(alive, T, 1e9)
        if lap == 1:
            pos_l1 = np.argsort(np.argsort(T, axis=1), axis=1)    # 0 = leader

    winner = np.argmin(T, axis=1)
    win = np.zeros((S, N))
    win[np.arange(S), winner] = 1
    pw = win.mean(0)
    pw_b = win.reshape(n_batches, per_batch, N).mean(1)
    lo, hi = np.percentile(pw_b, [5, 95], axis=0)
    by_scen = {}
    for s, name in enumerate(["dry", "mixed", "wet"]):
        msk = scen == s
        by_scen[name] = dict(share=float(msk.mean()),
                             **{c: float(win[msk, j].mean()) for j, c in enumerate(codes)})
    cond = {}
    for j, c in enumerate(codes[:8]):
        cond[c] = {f"L1_P{q + 1}": [float(win[pos_l1[:, j] == q, j].mean()), float((pos_l1[:, j] == q).mean())]
                   for q in range(4)}
    sc_any = has_sc
    cond["VER_given_SC"] = float(win[sc_any, 0].mean())
    cond["VER_given_noSC"] = float(win[~sc_any, 0].mean())
    return dict(codes=codes, p=pw.tolist(), lo=lo.tolist(), hi=hi.tolist(), by_scen=by_scen,
                cond=cond, sims=S)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--batches", type=int, default=60)
    ap.add_argument("--per", type=int, default=2000)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    r = simulate(BASE, a.batches, a.per)
    for c, p, lo, hi in sorted(zip(r["codes"], r["p"], r["lo"], r["hi"]), key=lambda x: -x[1])[:10]:
        print(f"{c}  {p:6.3f}  [{lo:5.3f}, {hi:5.3f}]")
    for k, v in r["by_scen"].items():
        top = {c: round(v[c], 3) for c in ["VER", "ANT", "HAM", "RUS", "LEC", "HAD", "NOR"]}
        print(k, round(v["share"], 3), top)
    if a.out:
        json.dump(r, open(a.out, "w"), indent=1)
