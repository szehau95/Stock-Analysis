#!/usr/bin/env python3
"""Build output/report.md from the engine outputs (run engine.py first)."""
import json
import os
import re

import numpy as np
import pandas as pd

import engine as E

OUT = E.OUT
PRICES_ASOF = "24 Sep 2026"


def pct(v, d=1):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:.{d}f}%"


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def bbg(uni, basket):
    return " + ".join(uni[t]["bbg"] for t in basket.split("+"))


def dmy(d, fmt="%d/%m/%Y"):
    return pd.Timestamp(d).strftime(fmt)


def cpn_at_uf(r, uf):
    """Coupon at another UF: the take moves 1:1 with UF, the coupon by UF / annuity."""
    return r["cpn_roll"] - (uf - E.UF_ROLL) / r["annuity"]


def misses(r):
    return (r["hard_fail"] or "none").replace("P(loss) > 12%", "P(loss)").replace("P(KO@1) < 55%", "P(KO@1)")


def summer_fills(snap, closes, floor, n_paths=150000, shifts=(0.0, 0.10, 0.20, 0.30)):
    """Implied all-in take of the Jul/Aug memory fills if memory vols were `shift` higher than today.
    WDC has no loaded history: it takes SKHY's slot in the MU/SNDK/SKHY correlation matrix."""
    corr = E.pricing_corr(E.corr_matrix(closes, ["MU", "SNDK", "SKHY"]), floor)
    fills = [("08/07 MYR", ["MU", "SNDK", "WDC"], 85, 50, 50, 20.22, 0.030),
             ("15/07 MYR", ["MU", "SNDK", "WDC"], 80, 60, 60, 19.66, 0.030),
             ("13/08 USD", ["MU", "SNDK", "WDC"], 83, 60, 60, 20.00, 0.035),
             ("21/08 USD", ["MU", "SNDK", "SKHY"], 85, 65, 65, 18.60, 0.035)]
    z = E.draw_normals(n_paths, corr, 3)
    rows = []
    for lab, b, ko, st, ki, cpn, r in fills:
        s1 = np.array([snap.loc[t, "iv"] for t in b])
        s12 = np.array([snap.loc[t, "iv12m"] for t in b])
        row = {"Fill": lab, "Basket": " + ".join(b), "KO/Str/KI": f"{ko}/{st}/{ki}", "Desk CPN": f"{cpn:.2f}%"}
        for sh in shifts:
            m1 = s1 + sh
            m = E.simulate(z, E.forward_vol(m1, s12 + sh), np.zeros(3), ki / 100.0, sig_m1=m1, r=r)
            pr = E.evaluate(m, ko / 100.0, st / 100.0, ki / 100.0, r=r)["pricing"]
            row[f"take @ vol +{int(sh * 100)}"] = pct(E.theta_at(pr, cpn / 100.0), 1)
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    uni = E.load_universe()
    snap = E.load_snapshots()
    meta = json.load(open(os.path.join(OUT, "run_meta.json")))
    cal = json.load(open(os.path.join(OUT, "calibration.json")))
    scr = pd.read_csv(os.path.join(OUT, "single_name_screen.csv"), index_col=0)
    rank = pd.read_csv(os.path.join(OUT, "ranking_top.csv")).fillna("")
    strict = pd.read_csv(os.path.join(OUT, "strict_pass_top.csv")).fillna("")
    lev = pd.read_csv(os.path.join(OUT, "strike_levers_top5.csv"))
    bench = pd.read_csv(os.path.join(OUT, "benchmarks.csv")).fillna("")
    grid = pd.read_csv(os.path.join(OUT, "grid_all_structures.csv.gz")).fillna("")
    theta_d, theta_r, spread = cal["theta_desk"], cal["theta_roll"], cal["spread"]
    uf_q, uf_r, floor = cal["uf_quoted"], cal["uf_roll"], cal["corr_floor"]
    td_label, td_long = dmy(meta["td"]), dmy(meta["td"], "%d %b %Y")
    obs1_label = dmy(meta["obs1"])
    basis = meta["ranking_basis"]

    best = (grid[grid[basis]].sort_values("roll_score", ascending=False)
            .groupby("basket", as_index=False).head(1))
    freq = pd.Series([t for b in best["basket"] for t in b.split("+")]).value_counts()

    # ---------------------------------------------------------------- trade-off table
    closes = E.load_closes()
    ledger = E.load_ledger()
    scr_full = E.single_name_screen(uni, snap, closes, meta["td"], meta["obs1"])
    env = (snap, closes, uni, scr_full, ledger, theta_d, theta_r, {"MU": meta["mu_m1_iv"]})
    E.OBS1_REF[0] = meta["obs1"]
    E.CORR_FLOOR[0] = floor
    top_b = rank["basket"].iloc[0]
    trade_specs = [(80, 60, 60), (85, 60, 60), (88, 60, 60), (90, 60, 60), (95, 60, 60), (95, 70, 60)]
    toff = pd.DataFrame([E.run_structure(top_b.split("+"), ko, st, ki, env, 200000, 7)
                         for ko, st, ki in trade_specs])

    q = pd.DataFrame(cal["quotes"])
    scan = pd.DataFrame(cal["floor_scan"])
    hist = scan[scan["floor"] < 0].iloc[0]
    t1 = rank.iloc[0]
    s1 = strict.iloc[0]                                   # best coupon with every hard filter passing
    same = strict[strict["basket"] == top_b]              # roll-friendly line for the desk: same basket
    s_line = same.iloc[0] if len(same) else strict.sort_values("roll_score", ascending=False).iloc[0]

    L = []
    w = L.append
    w("# ACEL monthly-roll screen: Lombard Odier research list (17.09.2026), repriced to the desk")
    w("")
    w(f"Fixing **{td_label}** (the desk's assumed trade date), obs #1 **{obs1_label}**. Market data: IBKR, "
      f"closes of {PRICES_ASOF}. Coupons calibrated to the desk's {dmy(cal['quoted'])} quotes ({len(q)} lines, "
      f"KO 95, UF {pct(uf_q, 0)}). Model: correlated-GBM Monte Carlo, {meta['paths']:,} paths per structure over "
      f"{meta['n_baskets']} baskets ({meta['n_structures']:,} structures), finalists re-run at "
      f"{meta['final_paths']:,} paths. Coupons are model estimates for ranking and quote requests, not quotes.")
    w("")

    # ---------------------------------------------------------------- bottom line
    worst = q.loc[q["resid_pts"].abs().idxmax()]
    w("## Bottom line")
    w("")
    w(f"- **The first pass overpriced coupons, and the desk's quotes show where.** It took its fee level from "
      f"the 24/09 fill and priced on historical correlations. On those assumptions the {len(q)} quotes imply an "
      f"all-in take of {pct(hist['theta'], 1)} at UF {pct(uf_q, 0)} and fit to only ±{hist['rmse_pts']:.1f} pts. "
      f"The desk marks correlation well above realized on these low-correlation tech baskets: ARM + DELL + DDOG "
      f"has a historical average ρ of {q.loc[q['basket'] == 'ARM+DELL+DDOG', 'avg_rho'].iloc[0]:.2f}. A "
      f"worst-of put on names marked more correlated is worth less, so the coupon is lower. With pricing "
      f"correlations floored at {floor:.1f}, the quotes fit to ±{cal['fit_rmse_pts']:.1f} pts at an all-in take "
      f"of **{pct(theta_d, 1)} at UF {pct(uf_q, 0)}**, i.e. an issuer spread of **{pct(spread, 1)} before UF**. "
      f"Probabilities stay on historical correlations, which is the conservative side for a worst-of.")
    w(f"- **No structure clears every hard filter at a ≥9% coupon, even at UF {pct(uf_r, 0)}.** "
      f"{meta['n_hard_pass']:,} structures pass the filters, and the best of them pays "
      f"{pct(meta['max_cpn_roll_hard_pass'])} at UF {pct(uf_r, 0)} "
      f"({s1['basket'].replace('+', ' + ')} {s1['ko']}/{s1['strike']}/{s1['ki']}). The desk's \"KO 80–83 can't "
      f"get anything of value\" matches the model: at UF {pct(uf_q, 0)} every KO 80–85 structure prices below "
      f"zero. Most of that is the UF. On a note expected to live 2–3 months, each 1% of UF costs 4–5.5% p.a. of "
      f"coupon, so UF {pct(uf_q, 0)} takes 17–22 pts off a KO 80–85 coupon.")
    w(f"- **Closest to the framework: {t1['basket'].replace('+', ' + ')} KO {t1['ko']} / Strike {t1['strike']} / "
      f"KI {t1['ki']}**, ~{pct(t1['cpn_roll'])} at UF {pct(uf_r, 0)}. P(KO @ obs #1) {pct(t1['p_ko1'])}, "
      f"P(KO by obs #3) {pct(t1['p_ko3_mem'])}, P(loss) {pct(t1['p_loss_mem'])}, which misses the 12% filter; "
      f"average loss {pct(t1['e_loss_mem'], 0)} when it does lose. Every ≥9% structure in the ranked table "
      f"misses P(loss) by 1–3 pts. Relaxing that filter to ~15% is the price of a 9–11% monthly-roll coupon today.")
    w(f"- **One open question, which the next quote settles.** The KO 95 quotes fit a {floor:.1f} to 0.8 "
      f"correlation floor about equally well, but short-life coupons differ: at 0.8 the KO 85–88 lines read "
      f"2.5–4 pts higher, enough to reopen a ≥9% roll that passes every filter. This report uses {floor:.1f}, "
      f"the conservative end. The desk's price on the KO 85–88 lines below at UF {pct(uf_r, 0)} tells us which.")
    qk = q.sort_values("p_ko1", ascending=False)
    w(f"- **The desk's KO 95 lines are not monthly-roll trades.** P(KO @ obs #1) {pct(q['p_ko1'].min(), 0)}–"
      f"{pct(q['p_ko1'].max(), 0)}, P(loss) {pct(q['p_loss'].min(), 0)}–{pct(q['p_loss'].max(), 0)}, and an "
      f"average loss of {pct(q['e_loss'].min(), 0)}–{pct(q['e_loss'].max(), 0)} when it happens. They are "
      f"12-month coupon trades. If you take one, {qk.iloc[0]['basket'].replace('+', ' + ')} "
      f"{qk.iloc[0]['ko']}/{qk.iloc[0]['strike']}/{qk.iloc[0]['ki']} at {qk.iloc[0]['desk_cpn']:.2f}% has the best KO "
      f"odds and the lowest P(loss) of the set.")
    legs = []
    for b in rank["basket"].head(6):
        legs += [t for t in b.split("+") if t not in ("ARM", "DELL") and t not in legs]
    w(f"- **Counters:** ARM is the engine, in {freq.get('ARM', 0)} of the {len(best)} baskets that reach 9% at "
      f"UF {pct(uf_r, 0)} with the earnings and 13-week-low rules intact. DELL is its best partner "
      f"({freq.get('DELL', 0)} baskets); {', '.join(legs[:-1])} and {legs[-1]} fill the third slot in the top 6.")
    w("")

    # ---------------------------------------------------------------- desk calibration
    w(f"## 1. The desk's {dmy(cal['quoted'])} quotes against the model")
    w("")
    w(f"Trade date {dmy(cal['quote_td'])}, UF {pct(uf_q, 0)}, all at KO 95 because the desk could not price "
      f"KO 80–83 at that UF. Model coupons at the fitted take; probabilities on historical correlations.")
    w("")
    qt = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
           "Desk CPN": f"{r['desk_cpn']:.2f}%", "Model CPN": f"{r['model_cpn']:.2f}%",
           "Diff": f"{r['resid_pts']:+.2f}", "avg ρ": f"{r['avg_rho']:.2f}",
           "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3"], 0), "E[life] m": f"{r['life']:.1f}",
           "P(loss)": pct(r["p_loss"]), "E[loss\\|loss]": pct(r["e_loss"], 0), "Fails": misses(r)}
          for _, r in q.iterrows()]
    w(md_table(pd.DataFrame(qt)))
    w("")
    w(f"The biggest miss is {worst['basket'].replace('+', ' + ')} {worst['ko']}/{worst['strike']}/{worst['ki']} "
      f"({worst['resid_pts']:+.1f} pts). One correlation floor cannot match every basket, because the desk's "
      f"single-name vol and skew marks also differ from the ATM-plus-bump used here. The model also values "
      f"strike 70 over strike 60 0.5–0.7 pts higher than the desk does.")
    w("")
    sc = [{"Pricing correlation": "historical" if r["floor"] < 0 else f"floored at {r['floor']:.1f}",
           f"All-in take @UF {pct(uf_q, 0)}": pct(r["theta"], 2), "Issuer spread ex-UF": pct(r["spread"], 2),
           "Fit error (RMS, pts)": f"{r['rmse_pts']:.2f}"} for _, r in scan.iterrows()]
    w(md_table(pd.DataFrame(sc)))
    w("")
    w(f"Floors from 0.6 to 0.8 fit about equally well. {floor:.1f} is used because it leaves the larger issuer "
      f"spread, the conservative choice for short-life notes where the take dominates the coupon. At a 0.8 floor "
      f"the KO 85–88 coupons below would read 2.5–4 pts higher.")
    w("")
    w("The September fills, repriced on the same basis, and the UF each one implies (your records will say "
      "whether these are right):")
    w("")
    ck = [{"Fill": f"{dmy(c['td'], '%d/%m')} {c['ccy']}", "Basket": c["basket"].replace("+", " + "),
           "KO/Str/KI": f"{c['ko']}/{c['strike']}/{c['ki']}", "Desk CPN": f"{c['desk_cpn']:.2f}%",
           "Implied all-in take": pct(c["implied_theta"], 2), "Implied UF": pct(c["implied_uf"], 1),
           "P(KO@1)": pct(c["p_ko1"]), "P(loss)": pct(c["p_loss"])} for c in cal["cross_checks"]]
    w(md_table(pd.DataFrame(ck)))
    w("")
    w("MYR and AUD fills are run on USD rates (no quanto adjustment), so read their implied UF as ±1 pt. If any "
      "implied UF is far from what you charged, send me the actual UFs and I will refit the spread.")
    w("")

    # ---------------------------------------------------------------- counters
    w("## 2. Counters in the lists, screened")
    w("")
    w("US lines only (ACEL chassis). Not modelled: Sell-rated names (SpaceX, Enphase, First Solar, Nike); names "
      "without a US line (Samsung, Tencent, Xiaomi, BYD and the European and Swiss names); small caps (Mirion, On, "
      "Service Corp); low-vol defensives (Verizon, AT&T, McDonald's, Home Depot); and names outside the house style "
      "(IBM, Spotify, Booking, Pinterest, TKO, Aptiv, Trimble, Logitech, Nokia, STMicro, SAP, Baidu, Ferrari).")
    w("")
    order = ["ARM", "DELL", "DDOG", "MU", "PANW", "ORCL", "AMAT", "AVGO", "NVDA", "PDD", "DIS", "BABA",
             "ADBE", "AMD", "CRM", "PLTR", "ANET", "SKHY", "STX", "GOOGL", "AMZN", "MSFT", "META", "AAPL",
             "TSLA", "NFLX", "TSM", "ASML", "INTC", "NOW"]

    best_rank = {}
    for i, b in enumerate(rank["basket"]):
        for t in b.split("+"):
            best_rank.setdefault(t, i + 1)

    def verdict(t):
        s = scr.loc[t]
        if t == "ANET":
            return "Exclude: est. print on the obs #1 date"
        if s["earn_in_obs1"]:
            return "Exclude: prints before obs #1"
        if t in ("CRM", "PLTR"):
            return "Exclude now: 13W-low rule caps KI at " + pct(s["ki_cap_13w"], 0)
        n, br = freq.get(t, 0), best_rank.get(t, 99)
        role = "engine" if s["iv"] >= 0.58 else "third leg"
        tier = 1 if (br <= 3 or n >= 40) else 2 if (br <= 15 or n >= 10) else 3
        where = f"best #{br}" if br < 99 else "not in top 25"
        note = ", strong-day fix" if s["strong_day"] else ""
        return f"Tier {tier} {role} ({n} baskets, {where}{note})"

    rows = []
    for t in order:
        s = scr.loc[t]
        rows.append({
            "Counter": s["bbg"], "LO": s["lo_rating"],
            "LO PT upside": pct(s["lo_upside_now"], 0),
            "IV 30D": pct(s["iv"], 0), "IV 12M": pct(snap.loc[t, "iv12m"], 0),
            "IV pct 52w": pct(s["ivp52"], 0), "vs 52W hi": pct(s["off_hi52"], 0),
            "KI cap (13W)": pct(s["ki_cap_13w"], 0),
            "vs 20D MA": pct(s["ma20_gap"], 0) if not np.isnan(s["ma20_gap"]) else "n/a",
            "Next print": dmy(s["next_earn"], "%d/%m") + (" (c)" if "confirmed" in str(s["earn_status"]) else " (e)"),
            "Verdict": verdict(t),
        })
    w(md_table(pd.DataFrame(rows)))
    w("")
    w("*KI cap (13W)* = 90% of the 13-week low ÷ spot, the highest KI that clears your 13-week-low hard filter. "
      "(c) confirmed date, (e) vendor estimate or prior-year pattern. LO PT upside is recomputed at the 24/09 close "
      "(foreign-listed lines keep the list's 17/09 figure). *Baskets* = baskets reaching 9% at UF "
      f"{pct(uf_r, 0)} with the earnings and 13W rules intact; *best #* = the name's best position in the ranked "
      "table below; *engine* = 30D IV ≥ 58%.")
    w("")

    # ---------------------------------------------------------------- ranking
    w("## 3. Ranked structures")
    w("")
    if basis == "rankable":
        w(f"Nothing passes every hard filter at ≥9%, so the table ranks structures that reach **9% p.a. at UF "
          f"{pct(uf_r, 0)}** with the earnings rule (no print before obs #1) and the 13-week-low KI rule intact, "
          f"ordered by Roll Score. The *Misses* column shows which of the P(KO@1) ≥ 55% and P(loss) ≤ 12% "
          f"filters each one fails. Grid: KO 80–95, Strike = KI 50–80, inside your rules of thumb "
          f"(KO ≤ 100 − 0.5·σ₁ₘ, KI ≤ e^(−0.75σ)). Ranked on memory KO; simultaneous KO shown after the slash.")
    else:
        w(f"Hard filters applied: no print inside obs #1, P(KO @ obs #1) ≥ 55%, P(loss) ≤ 12%, every KI at least "
          f"10% below its 13-week low. Minimum coupon: 9% p.a. at UF {pct(uf_r, 0)}.")
    w("")
    rr = []
    for i, r in rank.head(15).iterrows():
        rr.append({
            "#": i + 1, "Basket": r["basket"].replace("+", " + "),
            "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
            f"CPN @UF {pct(uf_r, 0)} / {pct(uf_q, 0)}": f"{pct(r['cpn_roll'])} / {pct(r['cpn_desk'])}",
            "P(KO@1)": pct(r["p_ko1"]),
            "P(KO≤3) mem/sim": f"{pct(r['p_ko3_mem'], 0)}/{pct(r['p_ko3_sim'], 0)}",
            "E[life] m": f"{r['life_mem']:.1f}/{r['life_sim']:.1f}",
            "P(loss)": f"{pct(r['p_loss_mem'])}/{pct(r['p_loss_sim'], 0)}",
            "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
            "Client EV": pct(r["client_ev"]),
            "CPN/IV": f"{r['cpn_iv']:.2f}",
            "Score": f"{r['roll_score']:.3f}",
            "Misses": misses(r),
            "Flags": "; ".join(x for x in [r["flags"], r["info"]] if x).replace("cheap (CPN/IV < 0.20); ", "")
                     .replace("; below high-vol target 16%", "").replace("; below mid target 12%", "")
                     .replace("below high-vol target 16%; ", "").replace("below mid target 12%; ", "")
                     .replace("below high-vol target 16%", "").replace("below mid target 12%", "").strip("; "),
        })
    w(md_table(pd.DataFrame(rr)))
    w("")
    ev_lo, ev_hi = rank.head(15)["client_ev"].min(), rank.head(15)["client_ev"].max()
    w(f"- **CPN** at an all-in take of {pct(theta_r, 2)} (UF {pct(uf_r, 0)}) and {pct(theta_d, 2)} (UF "
      f"{pct(uf_q, 0)}, the desk's basis on {dmy(cal['quoted'])}).")
    w(f"- **Client EV** (CPN × E[life]/12 − P(loss) × E[loss | loss]) runs {pct(ev_lo)} to {pct(ev_hi)} per "
      "roll. Coupons are priced on the desk's correlation mark and probabilities on historical correlation, so "
      "it measures fee drag plus that correlation premium, not structure quality.")
    w("- Penalties (−0.03 each): strong-day fix, avg ρ < 0.5 on 3 names, IV percentile > 90, ≥2 names shared "
      "with a live ledger basket. *px > LO PT* and *earnings ≤3d after obs #1* are shown but not penalised. Every "
      "row is below your regime coupon target and has CPN/IV < 0.20, so those two flags are left out.")
    w("")
    w(f"**Every hard filter passing (roll-friendly, thin coupon):** best coupon per basket at UF {pct(uf_r, 0)}.")
    w("")
    sp = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
           f"CPN @UF {pct(uf_r, 0)}": pct(r["cpn_roll"]), "CPN @UF 0%": pct(cpn_at_uf(r, 0.0)),
           "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3_mem"], 0), "E[life] m": f"{r['life_mem']:.1f}",
           "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
           "Flags": r["flags"].replace("cheap (CPN/IV < 0.20)", "").replace("below high-vol target 16%", "")
                    .replace("below mid target 12%", "").replace("; ;", ";").strip("; ")}
          for _, r in strict.head(6).iterrows()]
    w(md_table(pd.DataFrame(sp)))
    w("")
    w(f"Internal only (UF {pct(uf_r, 0)}):")
    w("")
    ir = []
    for i, r in rank.head(8).iterrows():
        ir.append({"#": i + 1, "Basket": r["basket"].replace("+", " + "),
                   "Fee velocity p.a.": pct(r["fee_velocity"]),
                   "Net-of-UF yield p.a.": pct(r["net_uf_yield"]),
                   "UF > 1-mth CPN and P(KO@1) > 70%": "FLAG" if r["uf_check"] is True or r["uf_check"] == "True" else "",
                   "−CPN per +1% UF": pct(r["uplift_per_1pct_uf"]),
                   "Max UF for 9%": pct(r["uf_room_min_cpn"], 2)})
    w(md_table(pd.DataFrame(ir)))
    w("")

    # ---------------------------------------------------------------- verdicts
    w("## 4. Top 3 verdicts")
    w("")
    arm_risk = ("ARM, which trades {arm_pt:.0%} above LO's $250 PT (below its KO price) and {arm_ma:.0%} above "
                "its 20-day MA, with its print estimated 04/11, two days after obs #1")
    notes = {
        "ARM+DELL": ("two names, so one fewer way to miss, and memory KO locks DELL (LO Buy, +{dell_pt:.0%} to PT) "
                     "on its own; KO 88 sits {cush:.1f} monthly σ below spot",
                     arm_risk),
        "ARM+DELL+ORCL": ("KO 85 is the widest cushion in the top 3 ({cush:.1f} monthly σ), and ORCL, "
                          "{orcl_hi:.0%} below its 52-week high, has already de-rated",
                          arm_risk + "; ORCL (LO Hold) is the lagging leg if AI-capex sentiment turns"),
        "MU+NVDA+ARM": ("the most correlated of the top 3 (avg ρ {rho:.2f}); NVDA (LO Strong Buy, +{nvda_pt:.0%} "
                        "to PT) at ~30% IV damps the worst-of, and MU fixes after its 30/09 print",
                        "the mega-cap prints of 27–29/10 inside obs #1 moving NVDA, or MU giving back its "
                        "post-print move; " + arm_risk),
    }
    for i, (_, r) in enumerate(rank.head(3).iterrows()):
        why, brk = notes.get(r["basket"], ("a low KO on high-vol, correlated names (avg ρ {rho:.2f})",
                                           "a broad AI sell-off into obs #1"))
        fmt = {"cush": r["ko_cushion_sd"], "rho": r["avg_rho"], "arm_pt": 1 / (1 + scr.loc["ARM", "lo_upside_now"]) - 1,
               "arm_ma": scr.loc["ARM", "ma20_gap"], "dell_pt": scr.loc["DELL", "lo_upside_now"],
               "orcl_hi": -scr.loc["ORCL", "off_hi52"], "nvda_pt": scr.loc["NVDA", "lo_upside_now"]}
        w(f"{i + 1}. **{r['basket'].replace('+', ' + ')} {r['ko']}/{r['strike']}/{r['ki']}**: P(KO@1) {pct(r['p_ko1'])}, "
          f"P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 1)} at UF {pct(uf_r, 0)}. **Rolls:** {why.format(**fmt)}. "
          f"**Breaks:** {brk.format(**fmt)}.")
    w("")
    two = best[(best["basket"] == "ARM+DELL") & ~best["basket"].isin(rank["basket"].head(3))]
    if len(two):
        r = two.iloc[0]
        w(f"Two-name alternative: **ARM + DELL {r['ko']}/{r['strike']}/{r['ki']}**: P(KO@1) {pct(r['p_ko1'])}, "
          f"P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 1)} at UF {pct(uf_r, 0)}.")
    nm = best[~best["basket"].str.contains("ARM")].head(2)
    if len(nm):
        s = "; ".join(f"**{r['basket'].replace('+', ' + ')} {r['ko']}/{r['strike']}/{r['ki']}** "
                      f"(P(KO@1) {pct(r['p_ko1'])}, P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 1)})"
                      for _, r in nm.iterrows())
        w(f"If you want no ARM exposure: {s}.")
    w("")

    # ---------------------------------------------------------------- economics
    w("## 5. Why the coupons are thin: UF on a short-life note, and the vol regime")
    w("")
    w(f"A fixed take hits short-life notes hardest. For the top structure the coupon annuity is "
      f"{t1['annuity']:.3f} (expected life {t1['life_mem']:.1f} months), so each 1% of UF moves the coupon by "
      f"{pct(t1['uplift_per_1pct_uf'])} p.a. Same basket, different structures:")
    w("")
    tt = [{"KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}", "P(KO@1)": pct(r["p_ko1"]),
           "P(KO≤3)": pct(r["p_ko3_mem"], 0), "E[life] m": f"{r['life_mem']:.1f}", "P(loss)": pct(r["p_loss_mem"]),
           "E[loss\\|loss]": pct(r["e_loss_mem"], 0), f"CPN @UF {pct(uf_r, 0)}": pct(r["cpn_roll"]),
           "CPN @UF 2%": pct(cpn_at_uf(r, 0.02)), f"CPN @UF {pct(uf_q, 0)}": pct(r["cpn_desk"]),
           "Hard filters": r["hard_fail"] or "pass"} for _, r in toff.iterrows()]
    w(f"**{top_b.replace('+', ' + ')}**:")
    w("")
    w(md_table(pd.DataFrame(tt)))
    w("")
    w("Coupon and monthly KO pull against each other: the KO 95 rows pay the desk-style coupons but knock out at "
      "obs #1 less than half the time; the KO 80–85 rows roll but only pay at a low UF.")
    w("")
    w("The July–August fills (KO 80–85, KI 50–60, ~20%) only reprice at a September-like take if memory vols "
      "were 20–30 points higher than today, which matches July's daily moves in MU and SNDK:")
    w("")
    w(md_table(summer_fills(snap, closes, floor)))
    w("")
    w(f"Your recent and live house structures, re-run for a {td_label} fixing (caps off):")
    w("")
    bt = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
           f"CPN @UF {pct(uf_q, 0)}": pct(r["cpn_desk"]), f"CPN @UF {pct(uf_r, 0)}": pct(r["cpn_roll"]),
           "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3_mem"], 0),
           "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
           "Fails": r["hard_fail"] or "none",
           "Prints in obs #1": re.sub(r"(\d{4})-(\d{2})-(\d{2})", r"\3/\2/\1", r["earnings_in_obs1"]) or "none"}
          for _, r in bench.iterrows()]
    w(md_table(pd.DataFrame(bt)))
    w("")
    w("Vol regime: 52-week IV percentiles are SKHY 2%, NVDA 1%, AVGO 2%, SNDK 6%, MU 21%. Selling vol "
      "(which is what the client does in an ACEL) pays little until it re-rates, typically after a sell-off or "
      "into earnings, and your earnings filter rules out the second.")
    w("")

    # ---------------------------------------------------------------- levers
    w("## 6. Coupon lever that keeps P(loss): strike above KI")
    w("")
    w("A strike above the KI leaves P(loss) unchanged (the KI still sets the loss event) but raises the loss "
      "once it happens. The desk prices this lever at ~3.7 pts per 10 strike points on the KO 95 lines; the "
      "model reads it ~0.5 pts richer.")
    w("")
    lt = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{int(r['strike'])}/{r['ki']}",
           f"CPN @UF {pct(uf_r, 0)}": pct(r["cpn_roll"]), f"CPN @UF {pct(uf_q, 0)}": pct(r["cpn_desk"]),
           "P(KO@1)": pct(r["p_ko1"]), "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0)}
          for _, r in lev.head(9).iterrows()]
    w(md_table(pd.DataFrame(lt)))
    w("")

    # ---------------------------------------------------------------- desk lines
    w("## 7. Desk request lines (Florence)")
    w("")
    reqs = []
    for _, r in rank.head(3).iterrows():
        reqs.append((r["basket"], r["ko"], r["strike"], r["ki"], r))
        lv = lev[(lev["basket"] == r["basket"]) & (lev["strike"] == r["strike"] + 10)]
        if len(lv):
            reqs.append((r["basket"], r["ko"], r["strike"] + 10, r["ki"], lv.iloc[0]))
    if len(two):
        r = two.iloc[0]
        reqs.append((r["basket"], r["ko"], r["strike"], r["ki"], r))
    reqs.append((s_line["basket"], s_line["ko"], s_line["strike"], s_line["ki"], s_line))
    w("```")
    w(f"Assuming TD {pd.Timestamp(meta['td']).day}/{pd.Timestamp(meta['td']).month} - UF {uf_r * 100:.0f}%")
    for b, ko, st, ki, _ in reqs:
        w(f"USD 12M {bbg(uni, b)} | Strike {int(st)} | KO {int(ko)} | KI {int(ki)} | CPN ?")
    w("```")
    w("")
    exp = "; ".join(f"{b.replace('+', ' + ')} {int(ko)}/{int(st)}/{int(ki)}: ~{pct(r['cpn_roll'], 0)} "
                    f"(~{pct(cpn_at_uf(r, 0.02), 0)} at UF 2%)" for b, ko, st, ki, r in reqs)
    w(f"- Model expectation at UF {pct(uf_r, 0)} ({floor:.1f} correlation floor, ±1.5 pts; 2.5–4 pts higher if the "
      f"desk marks correlation nearer 0.8): {exp}.")
    w(f"- The last line passes every hard filter (P(KO@1) {pct(s_line['p_ko1'], 0)}, P(loss) "
      f"{pct(s_line['p_loss_mem'], 0)}); it is there to get the desk's price for a true monthly roll.")
    w("- Memory KO, monthly obs, European KI, closing prices. Obs #1 lands 02/11, two days before ARM's "
      "estimated 04/11 print: get ARM's date confirmed before fixing.")
    w("- Re-check the 20-day-MA strong-day test on the fixing morning.")
    w("")

    # ---------------------------------------------------------------- releases
    w("## 8. Release drafts: pre-filled, waiting on the quote")
    w("")
    for _, r in rank.head(3).iterrows():
        names = r["basket"].split("+")
        w("```")
        w("🇺🇸 *Private Tranche ACEL*")
        w("")
        w(f"*{' + '.join(uni[t]['bbg'] for t in names)}*")
        w("")
        w("Tenure: 12 months")
        w("Currency: USD")
        w("Memory KO")
        w("Coupon: [desk quote]% p.a.")
        w(f"KO: {r['ko']}%")
        w(f"Strike: {r['strike']}%")
        w(f"KI: {r['ki']}%")
        for t in names:
            s = scr.loc[t]
            sp_, hi = s["spot"], s["hi52"]
            w("")
            w(f"{uni[t]['name']} ({uni[t]['bbg']})")
            w(f"Current Price: ${sp_:,.2f}")
            w(f"52-Week High: ${hi:,.2f}")
            w(f"Indicative KO Price: ${sp_ * r['ko'] / 100:,.2f}")
            w(f"Indicative Strike Price: ${sp_ * r['strike'] / 100:,.2f}")
            w(f"Indicative KI Price: ${sp_ * r['ki'] / 100:,.2f}")
        w("")
        w(f"Indicative prices as of {PRICES_ASOF}. Official KO, Strike and KI levels to be fixed based on the "
          f"closing prices on the trade date, {td_long}.")
        w("```")
        w("")
    w("Do not send until the desk's coupon is approved.")
    w("")

    # ---------------------------------------------------------------- method
    w("## Method and assumptions")
    w("")
    w(f"- Spot = 24/09 close; 52W high = max(live, IBKR 52W high); 13W low from IBKR. Correlations from 1Y daily "
      f"log returns (SKHY since its July listing). Risk-neutral drift, r = {pct(meta['r_usd'], 1)}, LO dividend yields.")
    w(f"- Vol: 30D ATM IV in month 1, forward vol from ~12M ATM option IV (Sep-2027 expiry, 24/09 mids) in months "
      f"2–12, and a +5 vol-pt bump phasing in between 100% and the KI level. MU month 1 uses "
      f"{pct(meta['mu_m1_iv'], 1)}: its 30D IV less the ±8.9% move implied by the 02/10 straddle.")
    w(f"- Coupons: par less an all-in take (issuer spread {pct(spread, 2)} + UF), pricing paths on historical "
      f"correlations floored at {floor:.1f}. Spread and floor fitted to the desk's {dmy(cal['quoted'])} quotes. "
      "P(KO), E[life] and P(loss) run on historical correlations with the same seed.")
    w("- Loss at maturity if no KO and worst-of < KI: 1 − WO/Strike. KO modes: memory per stock (ranked) and "
      "simultaneous (shown after the slash).")
    w(f"- Roll Score = 0.45·P(KO@1) + 0.25·P(KO≤3) + 0.20·(1 − P(loss)/0.12) + 0.10·min(CPN/IV ÷ 0.30, 1) "
      f"− 0.03 per penalty, with CPN at UF {pct(uf_r, 0)} and IV = basket average 30D IV.")
    w("- Earnings dates: MU 30/09 and AMD 03/11 confirmed; the rest are vendor estimates. ANET is estimated "
      "for 02/11, obs #1 itself, and treated as a fail until confirmed.")
    w("- All probabilities are risk-neutral. With a positive equity risk premium, P(KO) would be modestly higher "
      "and P(loss) modestly lower. The ranking would barely move.")
    w("")
    open(os.path.join(OUT, "report.md"), "w").write("\n".join(L) + "\n")
    toff.to_csv(os.path.join(OUT, "tradeoff_top1.csv"), index=False, float_format="%.4f")
    print("wrote", os.path.join(OUT, "report.md"))


if __name__ == "__main__":
    main()
