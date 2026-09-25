#!/usr/bin/env python3
"""ACEL monthly-roll optimiser.

Screens US-listed counters for worst-of ACEL/FCN structures (12M, monthly
observation, memory KO, European KI) and ranks them by probability of
knocking out at observation #1, per the ACEL Monthly-Roll master prompt.

Model: correlated GBM Monte Carlo on monthly steps with risk-neutral drift.
Vol is term-structured: month 1 uses the IBKR 30D ATM IV (so obs #1 KO odds
run on ATM vol, as the prompt specifies) and months 2-12 use the forward vol
implied by the ~12M ATM option IV (Sep-2027 expiry). A +5 vol-pt skew bump
phases in as a name falls from 100% to the KI level, so the KI/strike leg
carries the bump. Both KO conventions are reported:
  memory_per_stock - each name locks once >= KO on an obs date (ranked on)
  simultaneous     - worst-of >= KO on the same obs date
They agree at obs #1 and differ from obs #2 onwards.

Coupons: the note is priced at par less an all-in issuer take (theta). Theta
is calibrated to the 24/09/2026 USD desk fill, which also reprices the other
September fills to within ~1% of notional. "Roll pricing" lowers theta by
UF_CUT, i.e. the same desk economics with a smaller upfront fee. Coupons are
indicative, for ranking and quote requests only.
"""
import argparse
import itertools
import json
import math
import os
from multiprocessing import Pool

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "output")

R_USD = 0.035          # flat USD discount / drift rate
SKEW_BUMP = 0.05       # +5 vol pts on the KI/strike leg
UF_CUT = 0.025         # roll pricing: all-in take 2.5 pts below the 24/09 fill
UF_ROLL = 0.010        # UF assumed under roll pricing (fee velocity / net yield columns)
N_OBS = 12
DT = 1.0 / 12
PENALTY = 0.03         # Roll Score deduction per penalty flag

KO_GRID = [80, 83, 85, 88, 90, 92, 95]
KI_GRID = [50, 55, 60, 65, 70, 75, 80]
REGIMES = (("high-vol", 0.60, 0.16), ("mid", 0.40, 0.12), ("mega", 0.0, 0.09))
MIN_CPN = 0.09         # lowest sweet-spot coupon target; eligibility floor at roll pricing


# --------------------------------------------------------------------------- data

def load_universe():
    with open(os.path.join(DATA, "universe.json")) as f:
        return json.load(f)["names"]


def load_ledger():
    with open(os.path.join(DATA, "ledger.json")) as f:
        return json.load(f)["trades"]


def load_snapshots():
    rows = [json.loads(line) for line in open(os.path.join(DATA, "snapshots_raw.jsonl"))]
    snap = pd.DataFrame(rows).set_index("ticker")
    snap["close"] = (snap["last"] - snap["change"]).round(4)   # 24.09 official close
    iv12 = pd.read_csv(os.path.join(DATA, "iv12m.csv"), index_col=0)["iv12m"]
    snap["iv12m"] = iv12.reindex(snap.index).fillna(snap["iv"])
    return snap


def forward_vol(sig_m1, sig_12m):
    """Months 2-12 vol so that month 1 at sig_m1 plus 11 months forward matches 12M variance."""
    var = (sig_12m ** 2 - sig_m1 ** 2 / 12.0) / (11.0 / 12.0)
    return np.sqrt(np.maximum(var, 0.5 * sig_m1 ** 2))


def load_closes():
    dates = pd.to_datetime(open(os.path.join(DATA, "dates_1y.txt")).read().split())
    series = {}
    folder = os.path.join(DATA, "closes")
    for fn in sorted(os.listdir(folder)):
        start, vals = None, []
        for ln in open(os.path.join(folder, fn)).read().split("\n"):
            if ln.startswith("#start"):
                start = pd.Timestamp(ln.split()[1])
            elif ln.strip():
                vals += [float(x) for x in ln.split()]
        idx = dates[-len(vals):] if start is None else dates[dates >= start][: len(vals)]
        series[fn[:-4]] = pd.Series(vals, index=idx)
    return pd.DataFrame(series).reindex(dates)


def psd_fix(c):
    w, v = np.linalg.eigh(c)
    c2 = v @ np.diag(np.clip(w, 1e-6, None)) @ v.T
    d = np.sqrt(np.diag(c2))
    return c2 / np.outer(d, d)


def corr_matrix(closes, tickers):
    rets = np.log(closes[list(tickers)]).diff()
    return psd_fix(rets.corr(min_periods=30).values)


def obs1_date(td):
    d = pd.Timestamp(td) + pd.DateOffset(months=1)
    while d.weekday() >= 5:
        d += pd.Timedelta(days=1)
    return d.date().isoformat()


# ------------------------------------------------------------------ single names

def single_name_screen(uni, snap, closes, td, obs1):
    rows = []
    for t, meta in uni.items():
        s = snap.loc[t]
        spot, iv = float(s["close"]), float(s["iv"])
        sig1m = iv / math.sqrt(12)
        hi52 = max(float(s["high_52w"]), float(s["last"]))
        lo13 = float(s["low_13w"])
        earn = pd.Timestamp(meta["earn"])
        in_window = pd.Timestamp(td) < earn <= pd.Timestamp(obs1)
        if "same day as obs #1" in meta.get("earn_status", ""):
            in_window = True   # an estimate landing on obs #1 is unsafe until confirmed
        ma20 = gap20 = chg5 = np.nan
        if t in closes and closes[t].notna().sum() >= 25:
            c = closes[t].dropna()
            ma20 = c.iloc[-20:].mean()
            gap20 = spot / ma20 - 1
            chg5 = c.iloc[-1] / c.iloc[-6] - 1
        pt = meta.get("lo_pt")
        up = meta.get("lo_upside_1709")
        rows.append({
            "ticker": t, "bbg": meta["bbg"], "name": meta["name"],
            "lo_rating": meta.get("lo_rating") or "n/r",
            "lo_upside_now": (pt / spot - 1) if pt else (up / 100 if up is not None else np.nan),
            "spot": spot, "iv": iv, "hv30": float(s["hv30"]), "ivp52": float(s["ivp_52w"]),
            "sig1m": sig1m, "hi52": hi52, "off_hi52": spot / hi52 - 1,
            "lo13": lo13, "ki_cap_13w": 0.90 * lo13 / spot,
            "ma20_gap": gap20,
            "strong_day": bool(gap20 > sig1m) if not np.isnan(gap20) else False,
            "chg5d": chg5,
            "next_earn": meta["earn"], "earn_status": meta.get("earn_status", ""),
            "earn_in_obs1": in_window,
            "div": meta.get("div", 0.0), "group": meta.get("group"),
            "has_history": t in closes.columns,
        })
    return pd.DataFrame(rows).set_index("ticker")


# ------------------------------------------------------------------ Monte Carlo

def draw_normals(n_paths, corr, seed):
    L = np.linalg.cholesky(corr)
    z = np.random.default_rng(seed).standard_normal((n_paths, N_OBS, corr.shape[0]))
    return z @ L.T


def simulate(z, sig, q, ki, sig_m1=None, r=R_USD, bump=SKEW_BUMP):
    """Monthly moneyness paths (P, 12, n); skew bump phases in from 100% to KI."""
    P, K, n = z.shape
    logm = np.zeros((P, n))
    out = np.empty((P, K, n))
    span = max(1.0 - ki, 1e-6)
    for k in range(K):
        base = sig_m1 if (k == 0 and sig_m1 is not None) else sig
        s = base + bump * np.clip((1.0 - np.exp(logm)) / span, 0.0, 1.0)
        logm = logm + (r - q - 0.5 * s * s) * DT + s * math.sqrt(DT) * z[:, k, :]
        out[:, k, :] = np.exp(logm)
    return out


def _first_hit(mat):
    return np.where(mat.any(axis=1), mat.argmax(axis=1) + 1, N_OBS + 1)


def evaluate(m, ko, strike, ki, r=R_USD):
    """Metrics for one structure on moneyness paths m (P,12,n); levels as fractions."""
    above = m >= ko
    taus = {"mem": _first_hit(np.logical_or.accumulate(above, axis=1).all(axis=2)),
            "sim": _first_hit(above.all(axis=2))}
    wo_T = m[:, -1, :].min(axis=1)
    res = {}
    for mode, tau in taus.items():
        no_ko = tau > N_OBS
        loss_evt = no_ko & (wo_T < ki)
        loss_amt = 1.0 - wo_T / strike
        res[mode] = {
            "p_ko1": float(np.mean(tau == 1)),
            "p_ko3": float(np.mean(tau <= 3)),
            "life": float(np.mean(np.minimum(tau, N_OBS))),
            "p_loss": float(np.mean(loss_evt)),
            "e_loss": float(loss_amt[loss_evt].mean()) if loss_evt.any() else 0.0,
        }
    tau = taus["mem"]
    k = np.arange(1, N_OBS + 1)
    df = np.exp(-r * k / 12.0)
    counts = np.bincount(np.minimum(tau, N_OBS + 1), minlength=N_OBS + 2)[1:] / len(tau)
    p_hit = counts[:N_OBS]
    p_alive = 1.0 - np.concatenate(([0.0], np.cumsum(p_hit)[:-1]))
    redemption = np.where(wo_T >= ki, 1.0, wo_T / strike)
    res["pricing"] = {
        "annuity": float(np.sum(df * p_alive) / 12.0),
        "pv_ko": float(np.sum(df * p_hit)),
        "pv_mat": float(df[-1] * np.mean(np.where(tau > N_OBS, redemption, 0.0))),
    }
    return res


def coupon_at(pricing, theta):
    return (1.0 - theta - pricing["pv_ko"] - pricing["pv_mat"]) / pricing["annuity"]


def theta_at(pricing, cpn):
    return 1.0 - pricing["pv_ko"] - pricing["pv_mat"] - cpn * pricing["annuity"]


# ------------------------------------------------------------------ structures

def regime(avg_iv):
    for name, lo, floor in REGIMES:
        if avg_iv >= lo:
            return name, floor
    return REGIMES[-1][0], REGIMES[-1][2]


def live_overlap(basket, ledger):
    return sorted({tr["td"] for tr in ledger if len(set(basket) & set(tr["basket"])) >= 2})


def basket_context(basket, snap, closes, uni, scr, ledger, m1=None):
    m1 = m1 or {}
    sig = np.array([snap.loc[t, "iv"] for t in basket])
    sig_m1 = np.array([m1.get(t, snap.loc[t, "iv"]) for t in basket])
    sig_fwd = forward_vol(sig_m1, np.array([snap.loc[t, "iv12m"] for t in basket]))
    corr = corr_matrix(closes, basket)
    n = len(basket)
    avg_rho = float((corr.sum() - n) / (n * (n - 1))) if n > 1 else 1.0
    avg_iv = float(sig.mean())
    reg, floor = regime(avg_iv)
    flags = []
    strong = [t for t in basket if scr.loc[t, "strong_day"]]
    if strong:
        flags.append("strong-day fix (" + "/".join(strong) + ")")
    if n == 3 and avg_rho < 0.5:
        flags.append(f"low corr (avg rho {avg_rho:.2f})")
    if any(scr.loc[t, "ivp52"] > 0.90 for t in basket):
        flags.append("IV pct > 90")
    ov = live_overlap(basket, ledger)
    if ov:
        flags.append("overlaps live " + ",".join(pd.Timestamp(d).strftime("%d/%m") for d in ov))
    info = []   # reported, not penalised (outside the prompt's penalty list)
    above_pt = [t for t in basket if scr.loc[t, "lo_upside_now"] < 0]
    if above_pt:
        info.append("px > LO PT (" + "/".join(above_pt) + ")")
    near_ob1 = [t for t in basket if 0 <= (pd.Timestamp(scr.loc[t, "next_earn"]) - pd.Timestamp(OBS1_REF[0])).days <= 3]
    if near_ob1:
        info.append("earnings <=3d after obs #1 (" + "/".join(near_ob1) + ")")
    return {
        "sig": sig, "sig_m1": sig_m1, "sig_fwd": sig_fwd,
        "q": np.array([uni[t].get("div", 0.0) for t in basket]), "corr": corr,
        "avg_rho": avg_rho, "avg_iv": avg_iv, "regime": reg, "floor": floor,
        "sig1m_avg": avg_iv / math.sqrt(12),
        "ko_cap": 100.0 * (1.0 - 0.5 * avg_iv / math.sqrt(12)),
        "ki_cap_rule": 100.0 * math.exp(-0.75 * avg_iv),
        "ki_cap_13w": 100.0 * min(scr.loc[t, "ki_cap_13w"] for t in basket),
        "near_high": any(scr.loc[t, "off_hi52"] > -0.05 for t in basket),
        "flags": flags, "info": info,
    }


def structure_row(basket, ctx, ko, strike, ki, ev, theta_desk, theta_roll):
    mem, sim, pr = ev["mem"], ev["sim"], ev["pricing"]
    cpn_desk = coupon_at(pr, theta_desk)
    cpn_roll = coupon_at(pr, theta_roll)
    eff = cpn_roll / ctx["avg_iv"]
    hard = []
    if ki > ctx["ki_cap_13w"] + 1e-9:
        hard.append("KI within 10% of 13W low")
    if mem["p_ko1"] < 0.55:
        hard.append("P(KO@1) < 55%")
    if mem["p_loss"] > 0.12:
        hard.append("P(loss) > 12%")
    soft = list(ctx["flags"])
    near_high_ko = ko >= 95 and ctx["near_high"]
    if near_high_ko:
        soft.append("KO>=95 within 5% of 52W high")
    if eff < 0.20:
        soft.append("cheap (CPN/IV < 0.20)")
    if cpn_roll < ctx["floor"]:
        soft.append(f"below {ctx['regime']} target {ctx['floor']:.0%}")
    n_pen = len(ctx["flags"]) + (1 if near_high_ko else 0)
    life = mem["life"]
    score = (0.45 * mem["p_ko1"] + 0.25 * mem["p_ko3"] + 0.20 * (1 - mem["p_loss"] / 0.12)
             + 0.10 * min(max(eff, 0.0) / 0.30, 1.0) - PENALTY * n_pen)
    return {
        "basket": "+".join(basket), "n": len(basket),
        "ko": ko, "strike": strike, "ki": ki,
        "cpn_roll": cpn_roll, "cpn_desk": cpn_desk,
        "annuity": pr["annuity"], "uplift_per_1pct_uf": 0.01 / pr["annuity"],
        "fee_room_at_floor": theta_at(pr, ctx["floor"]),
        "p_ko1": mem["p_ko1"],
        "p_ko3_mem": mem["p_ko3"], "p_ko3_sim": sim["p_ko3"],
        "life_mem": life, "life_sim": sim["life"],
        "p_loss_mem": mem["p_loss"], "p_loss_sim": sim["p_loss"],
        "e_loss_mem": mem["e_loss"],
        "client_ev": cpn_roll * life / 12 - mem["p_loss"] * mem["e_loss"],
        "cpn_iv": eff,
        "ko_cushion_sd": math.log(100.0 / ko) / ctx["sig1m_avg"],
        "ki_cushion_sd": -math.log(ki / 100.0) / ctx["avg_iv"],
        "fee_velocity": UF_ROLL * 12 / life,
        "net_uf_yield": cpn_roll - UF_ROLL * 12 / life,
        "uf_check": bool(mem["p_ko1"] > 0.70 and UF_ROLL > cpn_roll / 12),
        "avg_iv": ctx["avg_iv"], "avg_rho": ctx["avg_rho"], "regime": ctx["regime"],
        "cpn_floor": ctx["floor"],
        "ko_cap": ctx["ko_cap"], "ki_cap_rule": ctx["ki_cap_rule"], "ki_cap_13w": ctx["ki_cap_13w"],
        "hard_fail": "; ".join(hard), "flags": "; ".join(soft), "info": "; ".join(ctx["info"]),
        "roll_score": score,
        "eligible": (not hard) and cpn_roll >= MIN_CPN,
    }


def run_basket(basket, env, n_paths, seed, respect_caps=True):
    snap, closes, uni, scr, ledger, theta_desk, theta_roll, m1 = env
    ctx = basket_context(basket, snap, closes, uni, scr, ledger, m1)
    z = draw_normals(n_paths, ctx["corr"], seed)
    rows = []
    for ki in KI_GRID:
        if respect_caps and (ki > ctx["ki_cap_rule"] + 1e-9 or ki > ctx["ki_cap_13w"] + 1e-9):
            continue
        m = simulate(z, ctx["sig_fwd"], ctx["q"], ki / 100.0, sig_m1=ctx["sig_m1"])
        for ko in KO_GRID:
            if ko <= ki or (respect_caps and ko > ctx["ko_cap"] + 1e-9):
                continue
            ev = evaluate(m, ko / 100.0, ki / 100.0, ki / 100.0)
            rows.append(structure_row(basket, ctx, ko, ki, ki, ev, theta_desk, theta_roll))
    return rows


def run_structure(basket, ko, strike, ki, env, n_paths, seed):
    """Single structure, no caps (strike may differ from KI)."""
    snap, closes, uni, scr, ledger, theta_desk, theta_roll, m1 = env
    ctx = basket_context(basket, snap, closes, uni, scr, ledger, m1)
    z = draw_normals(n_paths, ctx["corr"], seed)
    m = simulate(z, ctx["sig_fwd"], ctx["q"], ki / 100.0, sig_m1=ctx["sig_m1"])
    ev = evaluate(m, ko / 100.0, strike / 100.0, ki / 100.0)
    return structure_row(basket, ctx, ko, strike, ki, ev, theta_desk, theta_roll)


_ENV = None
OBS1_REF = ["2026-11-02"]


def _init(env, obs1="2026-11-02"):
    global _ENV
    _ENV = env
    OBS1_REF[0] = obs1


def _work(args):
    basket, n_paths, seed = args
    return run_basket(basket, _ENV, n_paths, seed)


def best_per_basket(df):
    ok = df[df["eligible"]]
    return ok.sort_values("roll_score", ascending=False).groupby("basket", as_index=False).head(1)


# ------------------------------------------------------------------ main

def frontier(grid, targets=(0.09, 0.12, 0.16)):
    """Best obs #1 KO odds reachable at each coupon target, P(loss) and 13W rules enforced."""
    base = grid[~grid["hard_fail"].str.contains("13W|P\\(loss\\)", regex=True)]
    rows = []
    for col, label in (("cpn_desk", "24/09 cost"), ("cpn_roll", "roll pricing")):
        for tgt in targets:
            s = base[base[col] >= tgt].sort_values("p_ko1", ascending=False)
            for _, r in s.head(3).iterrows():
                rows.append({"pricing": label, "target": tgt, "basket": r["basket"], "ko": r["ko"],
                             "strike": r["strike"], "ki": r["ki"], "cpn": r[col], "p_ko1": r["p_ko1"],
                             "p_ko3": r["p_ko3_mem"], "life": r["life_mem"], "p_loss": r["p_loss_mem"],
                             "e_loss": r["e_loss_mem"], "flags": r["flags"]})
            if s.empty:
                rows.append({"pricing": label, "target": tgt, "basket": "none"})
    return pd.DataFrame(rows)


def name_scorecard(scr, fin, best, elig):
    top = best.head(40)
    rows = []
    for t in scr.index:
        s = scr.loc[t]
        in_top = top[top["basket"].str.split("+").apply(lambda b: t in b)]
        in_fin = fin[fin["basket"].str.split("+").apply(lambda b: t in b)]
        rows.append({"ticker": t, "bbg": s["bbg"], "lo_rating": s["lo_rating"],
                     "lo_upside_now": s["lo_upside_now"], "iv30": s["iv"], "iv12m": np.nan,
                     "off_hi52": s["off_hi52"], "ki_cap_13w": s["ki_cap_13w"], "ma20_gap": s["ma20_gap"],
                     "strong_day": s["strong_day"], "next_earn": s["next_earn"], "earn_status": s["earn_status"],
                     "eligible_td": t in elig, "n_top40": len(in_top), "n_final": len(in_fin),
                     "best_score": in_fin["roll_score"].max() if len(in_fin) else np.nan})
    return pd.DataFrame(rows).set_index("ticker")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--td", default="2026-10-01", help="proposed fixing date (after MU prints 30/09)")
    ap.add_argument("--paths", type=int, default=50000)
    ap.add_argument("--final-paths", type=int, default=200000)
    ap.add_argument("--top", type=int, default=25)
    ap.add_argument("--seed", type=int, default=20260925)
    ap.add_argument("--mu-m1-iv", type=float, default=0.531,
                    help="MU month-1 vol once the 30/09 print is out (30D IV less the implied earnings move)")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    uni, ledger = load_universe(), load_ledger()
    snap, closes = load_snapshots(), load_closes()
    obs1 = obs1_date(args.td)
    OBS1_REF[0] = obs1
    scr = single_name_screen(uni, snap, closes, args.td, obs1)
    scr["iv12m"] = snap["iv12m"].reindex(scr.index)
    scr.to_csv(os.path.join(OUT, "single_name_screen.csv"), float_format="%.4f")

    # --- calibrate the all-in issuer take on the 24/09 USD fill (no month-1 override:
    #     MU's 30/09 print sat inside that trade's first month, so its 30D IV applies)
    cal = next(t for t in ledger if t.get("calibration"))
    env0 = (snap, closes, uni, scr, ledger, 0.0, 0.0, {})
    r0 = run_structure(cal["basket"], cal["ko"], cal["strike"], cal["ki"], env0,
                       args.final_paths, args.seed)
    # r0 was priced at theta = 0, so coupon(theta) = cpn0 - theta / annuity
    theta_desk = (r0["cpn_desk"] - cal["cpn"] / 100.0) * r0["annuity"]
    theta_roll = theta_desk - UF_CUT
    checks = []
    for tr in ledger:
        if tr["td"] >= "2026-09-01" and not tr.get("calibration"):
            rr = run_structure(tr["basket"], tr["ko"], tr["strike"], tr["ki"],
                               (snap, closes, uni, scr, ledger, 0.0, 0.0, {}),
                               args.final_paths, args.seed)
            implied = (rr["cpn_desk"] - tr["cpn"] / 100.0) * rr["annuity"]
            checks.append({"td": tr["td"], "ccy": tr["ccy"], "basket": "+".join(tr["basket"]),
                           "ko": tr["ko"], "strike": tr["strike"], "ki": tr["ki"], "desk_cpn": tr["cpn"],
                           "model_cpn_at_desk_theta": round(100 * (rr["cpn_desk"] - theta_desk / rr["annuity"]), 2),
                           "implied_theta": round(implied, 4),
                           "p_ko1": round(rr["p_ko1"], 3), "p_loss": round(rr["p_loss_mem"], 3),
                           "life": round(rr["life_mem"], 2)})
    calib = {"theta_desk": theta_desk, "theta_roll": theta_roll, "uf_cut": UF_CUT,
             "fill": cal, "fill_p_ko1": r0["p_ko1"], "fill_p_loss": r0["p_loss_mem"],
             "fill_life": r0["life_mem"], "annuity": r0["annuity"],
             "note": "USD rates for all; MYR/AUD quanto not modelled, so MYR fills imply a higher theta",
             "cross_checks": checks}
    with open(os.path.join(OUT, "calibration.json"), "w") as f:
        json.dump(calib, f, indent=2, default=str)
    print(f"theta_desk {theta_desk:.4f} (24/09 fill), theta_roll {theta_roll:.4f}")
    for c in checks:
        print("  cross-check", c)

    env = (snap, closes, uni, scr, ledger, theta_desk, theta_roll, {"MU": args.mu_m1_iv})
    # basket universe: names from the LO lists with 1Y history and no print before obs #1
    elig = [t for t in scr.index if scr.loc[t, "has_history"] and not scr.loc[t, "earn_in_obs1"]
            and not uni[t].get("not_in_lo_list")]
    print(f"TD {args.td} -> obs #1 {obs1}; eligible names ({len(elig)}): {', '.join(elig)}")
    baskets = [list(b) for k in (2, 3) for b in itertools.combinations(elig, k)]
    with Pool(args.workers, initializer=_init, initargs=(env, obs1)) as pool:
        chunks = pool.map(_work, [(b, args.paths, args.seed) for b in baskets], chunksize=8)
    grid = pd.DataFrame([r for ch in chunks for r in ch])
    grid.to_csv(os.path.join(OUT, "grid_all_structures.csv.gz"), index=False, float_format="%.4f")
    best = best_per_basket(grid).sort_values("roll_score", ascending=False)
    frontier(grid).to_csv(os.path.join(OUT, "frontier.csv"), index=False, float_format="%.4f")

    # --- finalists at higher path count, fresh seed
    fin_b = [b.split("+") for b in best["basket"].head(args.top)]
    with Pool(args.workers, initializer=_init, initargs=(env, obs1)) as pool:
        chunks = pool.map(_work, [(b, args.final_paths, args.seed + 1) for b in fin_b])
    fin_all = pd.DataFrame([r for ch in chunks for r in ch])
    fin = best_per_basket(fin_all).sort_values("roll_score", ascending=False)
    fin.to_csv(os.path.join(OUT, "ranking_top.csv"), index=False, float_format="%.4f")
    fin_all.to_csv(os.path.join(OUT, "finalists_all_structures.csv"), index=False, float_format="%.4f")

    # --- coupon levers on the top 5: strike above KI (same P(loss), bigger loss if KI'd)
    levers = []
    for _, r in fin.head(5).iterrows():
        for st in (r["ki"], r["ki"] + 5, r["ki"] + 10):
            if st >= r["ko"]:
                continue
            levers.append(run_structure(r["basket"].split("+"), r["ko"], st, r["ki"], env,
                                        args.final_paths, args.seed + 1))
    pd.DataFrame(levers).to_csv(os.path.join(OUT, "strike_levers_top5.csv"), index=False, float_format="%.4f")

    # --- benchmarks: current house structures re-run for this TD, caps off
    bench_specs = [(["MU", "SNDK", "SKHY"], 95, 70, 70), (["MU", "SNDK", "SKHY"], 100, 70, 60),
                   (["MU", "SNDK", "SKHY"], 85, 60, 60), (["NVDA", "AMZN", "GOOGL"], 100, 80, 80),
                   (["MU", "AVGO"], 100, 75, 55), (["MU", "AVGO"], 90, 60, 60)]
    bench = []
    for b, ko, st, ki in bench_specs:
        row = run_structure(b, ko, st, ki, env, args.final_paths, args.seed + 2)
        row["earnings_in_obs1"] = ", ".join(f"{t} {scr.loc[t, 'next_earn']}" for t in b if scr.loc[t, "earn_in_obs1"])
        bench.append(row)
    pd.DataFrame(bench).to_csv(os.path.join(OUT, "benchmarks.csv"), index=False, float_format="%.4f")

    card = name_scorecard(scr, fin, best, elig)
    card["iv12m"] = snap["iv12m"].reindex(card.index)
    card.to_csv(os.path.join(OUT, "name_scorecard.csv"), float_format="%.4f")

    meta = {"td": args.td, "obs1": obs1, "paths": args.paths, "final_paths": args.final_paths,
            "eligible": elig, "n_baskets": len(baskets), "n_structures": len(grid),
            "n_eligible_structures": int(grid["eligible"].sum()),
            "n_hard_pass": int((grid["hard_fail"] == "").sum()),
            "n_regime_target_met": int(((grid["hard_fail"] == "") & (grid["cpn_roll"] >= grid["cpn_floor"])).sum()),
            "mu_m1_iv": args.mu_m1_iv, "r_usd": R_USD, "skew_bump": SKEW_BUMP,
            "uf_cut": UF_CUT, "uf_roll": UF_ROLL, "min_cpn": MIN_CPN}
    with open(os.path.join(OUT, "run_meta.json"), "w") as f:
        json.dump(meta, f, indent=2)

    pd.set_option("display.width", 250)
    cols = ["basket", "ko", "ki", "cpn_roll", "cpn_desk", "p_ko1", "p_ko3_mem", "life_mem",
            "p_loss_mem", "client_ev", "cpn_iv", "roll_score", "flags"]
    print(fin[cols].to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(json.dumps(meta, indent=1))


if __name__ == "__main__":
    main()
