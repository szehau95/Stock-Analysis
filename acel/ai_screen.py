#!/usr/bin/env python3
"""AI pull-back screen: which AI counters, already ~30% off their 52-week high, give an ACEL the
best chance of knocking out at a coupon of at least 15% p.a.?

As of 06/10/2026 for a fixing this week (TD 08/10/2026, obs #1 09/11/2026). Reuses engine.py:
correlated-GBM MC, 30D IV for month 1 and the 12M-implied forward vol after it, a +5 vol-pt
skew bump on the KI leg, memory KO, pricing correlations floored at 0.6 and the issuer spread
fitted to the desk's 28/09 quotes (output/calibration.json). Market data: IBKR snapshot of
06/10/2026 (intraday), Sep-2027 ATM option mids for the 12M vol, daily closes to 05/10/2026.
"""
import argparse
import itertools
import json
import math
import os

import numpy as np
import pandas as pd

import engine as E
from iv12m import implied

DATA = E.DATA
OUT = os.path.join(E.OUT, "ai_pullback_2026-10-06")
ASOF = "2026-10-06"
TD = "2026-10-08"
MIN_CPN = 0.15               # the coupon the client wants
UF_LEVELS = (0.04, 0.02, 0.01)
DRAWDOWN = -0.30             # "already corrected > 30%": off the 52-week high
NEAR_MISS = -0.25            # priced as well, flagged
USER_PICKS = ("AMAT", "ARM")  # always priced, flagged if a rule fails
KO_GRID = [85, 88, 90, 92, 95, 100]
KI_GRID = [50, 55, 60, 65, 70]
STRIKE_ADD = [0, 5, 10]      # strike above KI: the lever the desk priced on 28/09

THEME = {
    "NVDA": "AI semis", "AMD": "AI semis", "AVGO": "AI semis", "ARM": "AI semis", "MRVL": "AI semis",
    "TSM": "AI semis", "INTC": "AI semis", "AMAT": "AI semi equipment", "ASML": "AI semi equipment",
    "MU": "Memory", "SKHY": "Memory", "SNDK": "Memory", "WDC": "Storage", "STX": "Storage",
    "DELL": "AI hardware", "ANET": "AI networking",
    "MSFT": "Hyperscaler", "GOOGL": "Hyperscaler", "AMZN": "Hyperscaler", "META": "Hyperscaler",
    "ORCL": "AI cloud", "BABA": "China AI cloud", "BIDU": "China AI",
    "NOW": "AI software", "CRM": "AI software", "ADBE": "AI software", "SAP": "AI software",
    "IBM": "AI software", "PLTR": "AI software", "DDOG": "AI software",
    "PANW": "Security software", "TSLA": "Autonomy / robotics", "AAPL": "Devices",
}
CORE_AI = {k for k, v in THEME.items() if v not in ("Security software", "Devices", "Autonomy / robotics")}


def load_universe():
    uni = E.load_universe()
    ov = json.load(open(os.path.join(DATA, "universe_overrides_2026-10-06.json")))["names"]
    for t, m in ov.items():
        uni[t] = {**uni.get(t, {}), **m}
    return uni


def load_snap():
    rows = [json.loads(line) for line in open(os.path.join(DATA, "snapshots_2026-10-06.jsonl"))]
    snap = pd.DataFrame(rows).set_index("ticker")
    snap["close"] = snap["last"]          # 06/10 intraday price is the reference spot
    return snap


def load_iv12m(snap, uni):
    """12M ATM vol: Sep-2027 mids of 06/10 where pulled, else the 24/09 value, else 30D IV."""
    qt = pd.read_csv(os.path.join(DATA, "iv12m_quotes_2026-10-06.csv"))
    new = {}
    for _, r in qt.iterrows():
        T = (pd.Timestamp(r["expiry"]) - pd.Timestamp(ASOF)).days / 365.0
        q = uni[r["ticker"]].get("div", 0.0)
        ivs = [implied((r["call_bid"] + r["call_ask"]) / 2, r["spot_close"], r["strike"], T, q, "c"),
               implied((r["put_bid"] + r["put_ask"]) / 2, r["spot_close"], r["strike"], T, q, "p")]
        new[r["ticker"]] = float(np.mean(ivs))
    old = pd.read_csv(os.path.join(DATA, "iv12m.csv"), index_col=0)["iv12m"]
    iv12, src = {}, {}
    for t in snap.index:
        if t in new:
            iv12[t], src[t] = new[t], "06/10"
        elif t in old.index:
            iv12[t], src[t] = float(old[t]), "24/09"
        else:
            iv12[t], src[t] = float(snap.loc[t, "iv"]), "30D"
    return pd.Series(iv12), pd.Series(src)


def load_closes():
    """1Y daily closes to 05/10: the 24/09 file plus the IBKR top-up (and BIDU's full year)."""
    old = E.load_closes()
    upd = pd.read_csv(os.path.join(DATA, "closes_update_2026-10-05.csv"), parse_dates=["date"])
    wide = upd.pivot(index="date", columns="ticker", values="close")
    c = old.reindex(old.index.union(wide.index))
    for t in wide.columns:
        c[t] = c[t].combine_first(wide[t]) if t in c.columns else wide[t]
    return c[c.index > pd.Timestamp("2025-10-06")]


def screen(uni, snap, iv12, iv12_src, closes, obs1):
    rows = []
    last_day = closes.index.max()
    for t in snap.index:
        m, s = uni[t], snap.loc[t]
        spot, iv = float(s["last"]), float(s["iv"])
        sig1m = iv / math.sqrt(12)
        earn = pd.Timestamp(m["earn"])
        inside = pd.Timestamp(TD) < earn <= pd.Timestamp(obs1)
        gap20 = np.nan
        if t in closes.columns and closes[t].notna().sum() > 25 and pd.notna(closes.loc[last_day, t]):
            gap20 = spot / closes[t].dropna().iloc[-20:].mean() - 1
        pt = m.get("lo_pt")
        up = (pt / spot - 1) if pt else (m["lo_upside_1709"] / 100 if m.get("lo_upside_1709") is not None else np.nan)
        off = spot / max(float(s["high_52w"]), spot) - 1
        rows.append({
            "ticker": t, "bbg": m["bbg"], "name": m["name"], "theme": THEME.get(t, ""),
            "core_ai": t in CORE_AI, "lo_rating": m.get("lo_rating") or "n/r", "lo_upside_now": up,
            "spot": spot, "hi52": float(s["high_52w"]), "off_hi52": off,
            "iv": iv, "iv12m": float(iv12[t]), "iv12m_src": iv12_src[t], "hv30": float(s["hv30"]),
            "ivp52": float(s["ivp_52w"]), "ki_cap_13w": 0.90 * float(s["low_13w"]) / spot,
            "ma20_gap": gap20, "strong_day": bool(gap20 > sig1m) if not np.isnan(gap20) else False,
            "next_earn": m["earn"], "earn_status": m.get("earn_status", ""), "earn_in_obs1": inside,
            "corrected": off <= DRAWDOWN, "near_miss": DRAWDOWN < off <= NEAR_MISS,
            "div": m.get("div", 0.0),
        })
    return pd.DataFrame(rows).set_index("ticker")


def pricing_set(scr):
    ok = scr["core_ai"] & ~scr["earn_in_obs1"] & (scr["off_hi52"] <= NEAR_MISS)
    names = list(scr.index[ok])
    names += [t for t in USER_PICKS if t not in names]
    return sorted(names, key=lambda t: scr.loc[t, "off_hi52"])


def rule_flags(basket, ctx, scr, ko, ki):
    """Rules this screen reports instead of enforcing: the print and drawdown screens, and the
    prompt's KO/KI rules of thumb (enforced, they leave nothing at 15%)."""
    out = []
    late = [t for t in basket if scr.loc[t, "earn_in_obs1"]]
    if late:
        out.append("prints before obs #1 (" + "/".join(f"{t} {pd.Timestamp(scr.loc[t, 'next_earn']):%d/%m}" for t in late) + ")")
    near = [t for t in basket if scr.loc[t, "near_miss"]]
    if near:
        out.append("<30% off high (" + "/".join(f"{t} {scr.loc[t, 'off_hi52']:.0%}" for t in near) + ")")
    if ko > ctx["ko_cap"] + 1e-9:
        out.append(f"KO above {ctx['ko_cap']:.1f} rule of thumb")
    if ki > ctx["ki_cap_rule"] + 1e-9:
        out.append(f"KI above {ctx['ki_cap_rule']:.1f} rule of thumb")
    return "; ".join(out)


def p_ko_ever(m, ko):
    """P(memory KO by obs #12) on moneyness paths m."""
    tau = E._first_hit(np.logical_or.accumulate(m >= ko / 100.0, axis=1).all(axis=2))
    return float(np.mean(tau <= E.N_OBS))


def price_basket(basket, snap, closes, uni, scr, ledger, cal, n_paths, seed):
    ctx = E.basket_context(list(basket), snap, closes, uni, scr, ledger, {})
    z, z_px = E._paths(ctx, n_paths, seed)
    rows = []
    for ki in KI_GRID:
        if ki > ctx["ki_cap_13w"] + 1e-9:          # 13-week-low rule (hard)
            continue
        m, m_px = E._sim_pair(ctx, z, z_px, ki / 100.0)
        for ko in KO_GRID:
            if ko <= ki:
                continue
            p_ever = p_ko_ever(m, ko)
            for add in STRIKE_ADD:
                st = ki + add
                if st >= ko:
                    continue
                ev = E._eval_pair(m, m_px, ko / 100.0, st / 100.0, ki / 100.0)
                r = E.structure_row(list(basket), ctx, ko, st, ki, ev, cal["theta_desk"], cal["theta_roll"])
                for uf in UF_LEVELS:
                    r[f"cpn_uf{uf * 100:.0f}"] = r["cpn_roll"] - (uf - cal["uf_roll"]) / r["annuity"]
                r["p_ko_ever"] = p_ever
                r["rule_flags"] = rule_flags(basket, ctx, scr, ko, ki)
                rows.append(r)
    return rows


def run_line(basket, ko, strike, ki, env, n_paths, seed, cal):
    """One structure on fresh paths: engine metrics, coupons at each UF, P(KO ever), rule flags.
    env = (snap, closes, uni, scr, ledger, m1); m1 overrides month-1 vols by ticker."""
    snap, closes, uni, scr, ledger, m1 = env
    ctx = E.basket_context(list(basket), snap, closes, uni, scr, ledger, m1)
    z, z_px = E._paths(ctx, n_paths, seed)
    m, m_px = E._sim_pair(ctx, z, z_px, ki / 100.0)
    ev = E._eval_pair(m, m_px, ko / 100.0, strike / 100.0, ki / 100.0)
    r = E.structure_row(list(basket), ctx, ko, strike, ki, ev, cal["theta_desk"], cal["theta_roll"])
    for uf in UF_LEVELS:
        r[f"cpn_uf{uf * 100:.0f}"] = r["cpn_roll"] - (uf - cal["uf_roll"]) / r["annuity"]
    r["p_ko_ever"] = p_ko_ever(m, ko)
    r["rule_flags"] = rule_flags(basket, ctx, scr, ko, ki)
    return r


def setup():
    """Calibration, obs #1 and the market data shared by the screen and the report."""
    cal = json.load(open(os.path.join(E.OUT, "calibration.json")))
    E.CORR_FLOOR[0] = cal["corr_floor"]
    obs1 = E.obs1_date(TD)
    E.OBS1_REF[0] = obs1
    uni, snap, ledger = load_universe(), load_snap(), E.load_ledger()
    iv12, iv12_src = load_iv12m(snap, uni)
    snap["iv12m"] = iv12
    closes = load_closes()
    scr = screen(uni, snap, iv12, iv12_src, closes, obs1)
    return cal, obs1, uni, snap, ledger, closes, scr


def best_at(grid, uf, min_cpn=MIN_CPN):
    col = f"cpn_uf{uf * 100:.0f}"
    ok = grid[grid[col] >= min_cpn]
    ok = ok.sort_values(["p_ko1", "p_ko3_mem", "p_loss_mem"], ascending=[False, False, True])
    return ok.groupby("basket", as_index=False).head(1).reset_index(drop=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--paths", type=int, default=50000)
    ap.add_argument("--final-paths", type=int, default=200000)
    ap.add_argument("--seed", type=int, default=20261006)
    ap.add_argument("--reuse-grid", action="store_true", help="read grid.csv.gz instead of re-pricing it")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    cal, obs1, uni, snap, ledger, closes, scr = setup()
    scr.to_csv(os.path.join(OUT, "screen.csv"), float_format="%.4f")

    names = pricing_set(scr)
    baskets = [b for k in (1, 2, 3) for b in itertools.combinations(names, k)]
    print(f"TD {TD} -> obs #1 {obs1}; priced: {', '.join(names)} ({len(baskets)} baskets)")
    grid_file = os.path.join(OUT, "grid.csv.gz")
    if args.reuse_grid:
        grid = pd.read_csv(grid_file)
    else:
        grid = pd.DataFrame([r for b in baskets
                             for r in price_basket(b, snap, closes, uni, scr, ledger, cal, args.paths, args.seed)])
        grid.to_csv(grid_file, index=False, float_format="%.4f")

    # finalists: best ≥15% structure per basket at each UF, re-run at more paths on a fresh seed
    env = (snap, closes, uni, scr, ledger, {})
    fin_rows = []
    for uf in UF_LEVELS:
        for _, r in best_at(grid, uf).iterrows():
            rr = run_line(r["basket"].split("+"), r["ko"], r["strike"], r["ki"], env,
                          args.final_paths, args.seed + 1, cal)
            rr["uf"] = uf
            rr["cpn"] = rr[f"cpn_uf{uf * 100:.0f}"]
            fin_rows.append(rr)
    fin = pd.DataFrame(fin_rows)
    fin.to_csv(os.path.join(OUT, "finalists.csv"), index=False, float_format="%.4f")

    # name scorecard: what each counter achieves inside its best ≥15% basket
    card = []
    for t in names:
        row = {"ticker": t}
        for uf in UF_LEVELS:
            f = fin[(fin["uf"] == uf) & fin["basket"].str.split("+").apply(lambda b: t in b)]
            f = f[f["cpn"] >= MIN_CPN - 0.005]
            top = f.sort_values("p_ko1", ascending=False).head(1)
            row[f"best_p_ko1_uf{uf * 100:.0f}"] = float(top["p_ko1"].iloc[0]) if len(top) else np.nan
            row[f"best_basket_uf{uf * 100:.0f}"] = top["basket"].iloc[0] if len(top) else ""
        card.append(row)
    card = pd.DataFrame(card).set_index("ticker").join(
        scr[["off_hi52", "iv", "iv12m", "ivp52", "next_earn", "earn_in_obs1", "lo_rating", "lo_upside_now",
             "ki_cap_13w", "strong_day"]])
    card.to_csv(os.path.join(OUT, "names.csv"), float_format="%.4f")

    meta = {"asof": ASOF, "td": TD, "obs1": obs1, "min_cpn": MIN_CPN, "uf_levels": UF_LEVELS,
            "priced": names, "n_baskets": len(baskets), "n_structures": len(grid),
            "paths": args.paths, "final_paths": args.final_paths, "seed": args.seed, "theta_desk": cal["theta_desk"],
            "spread": cal["spread"], "corr_floor": cal["corr_floor"]}
    json.dump(meta, open(os.path.join(OUT, "run_meta.json"), "w"), indent=2)
    pd.set_option("display.width", 250)
    cols = ["basket", "ko", "strike", "ki", "cpn", "p_ko1", "p_ko3_mem", "p_ko_ever", "life_mem",
            "p_loss_mem", "e_loss_mem", "avg_rho", "rule_flags"]
    for uf in UF_LEVELS:
        f = fin[fin["uf"] == uf].sort_values("p_ko1", ascending=False)
        print(f"\n== best structure with CPN >= {MIN_CPN:.0%} at UF {uf:.0%} ==")
        print(f[cols].head(15).to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print(card.round(3).to_string())


if __name__ == "__main__":
    main()
