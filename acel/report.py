#!/usr/bin/env python3
"""Build output/report.md from the engine outputs (run engine.py first)."""
import json
import os

import numpy as np
import pandas as pd

import engine as E

OUT = E.OUT
TD_LABEL = "01/10/2026"
TD_LONG = "01 Oct 2026"
PRICES_ASOF = "24 Sep 2026"


def pct(v, d=1):
    return "n/a" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{100 * v:.{d}f}%"


def num(v, d=2):
    return f"{v:,.{d}f}"


def md_table(df):
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "|".join("---" for _ in cols) + "|"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
    return "\n".join(lines)


def bbg(uni, basket):
    return " + ".join(uni[t]["bbg"] for t in basket.split("+"))


def summer_fills(snap, closes, n_paths=150000, shifts=(0.0, 0.10, 0.20, 0.30)):
    """Implied all-in take of the Jul/Aug memory fills if memory vols were `shift` higher than today.
    WDC has no loaded history: it takes SKHY's slot in the MU/SNDK/SKHY correlation matrix."""
    corr = E.corr_matrix(closes, ["MU", "SNDK", "SKHY"])
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
    lev = pd.read_csv(os.path.join(OUT, "strike_levers_top5.csv"))
    bench = pd.read_csv(os.path.join(OUT, "benchmarks.csv")).fillna("")
    grid = pd.read_csv(os.path.join(OUT, "grid_all_structures.csv.gz")).fillna("")
    theta_d, theta_r = cal["theta_desk"], cal["theta_roll"]

    best = (grid[grid["eligible"]].sort_values("roll_score", ascending=False)
            .groupby("basket", as_index=False).head(1))
    freq = pd.Series([t for b in best["basket"] for t in b.split("+")]).value_counts()

    # ---------------------------------------------------------------- trade-off table
    closes = E.load_closes()
    ledger = E.load_ledger()
    scr_full = E.single_name_screen(uni, snap, closes, "2026-10-01", meta["obs1"])
    env = (snap, closes, uni, scr_full, ledger, theta_d, theta_r, {"MU": meta["mu_m1_iv"]})
    E.OBS1_REF[0] = meta["obs1"]
    top_b = rank["basket"].iloc[0]
    trade_specs = [(80, 60, 60), (85, 60, 60), (90, 60, 60), (95, 60, 60), (95, 70, 60), (100, 70, 60)]
    toff = []
    for ko, st, ki in trade_specs:
        r = E.run_structure(top_b.split("+"), ko, st, ki, env, 200000, 7)
        toff.append(r)
    toff = pd.DataFrame(toff)

    L = []
    w = L.append
    w("# ACEL monthly-roll screen: Lombard Odier research list (17.09.2026)")
    w("")
    w(f"Fixing assumed **{TD_LABEL}** (first clean date after MU reports on 30/09 after the close), "
      f"obs #1 **{pd.Timestamp(meta['obs1']).strftime('%d/%m/%Y')}**. Market data: IBKR, closes of {PRICES_ASOF}. "
      f"Model: correlated-GBM Monte Carlo, {meta['paths']:,} paths per structure over {meta['n_baskets']} baskets "
      f"({meta['n_structures']:,} structures), finalists re-run at {meta['final_paths']:,} paths. "
      "Coupons are model estimates for ranking and quote requests, not quotes.")
    w("")

    # ---------------------------------------------------------------- bottom line
    t1 = rank.iloc[0]
    w("## Bottom line")
    w("")
    w(f"- **Best counters from the three lists right now: ARM and DELL** as the engine (highest usable vol, "
      f"prints after obs #1, KI headroom to the 13-week low), with DDOG, PDD or AVGO as the third name "
      f"(then BABA, ORCL, PANW, NVDA, DIS). ARM is in {freq.get('ARM', 0)} and DELL in "
      f"{freq.get('DELL', 0)} of the {len(best)} baskets that clear every hard filter at a ≥9% roll-priced coupon.")
    w(f"- **Top structure: {t1['basket'].replace('+', ' + ')}, KO {t1['ko']} / Strike {t1['strike']} / KI {t1['ki']}**: "
      f"P(KO @ obs #1) {pct(t1['p_ko1'])}, P(KO by obs #3) {pct(t1['p_ko3_mem'])}, P(loss) {pct(t1['p_loss_mem'])}, "
      f"but an average loss of {pct(t1['e_loss_mem'], 0)} when it does lose.")
    w(f"- **The catch is coupon, not KO.** No structure in the universe clears your hard filters *and* your "
      f"regime coupon targets (0 of {meta['n_structures']:,}). At the all-in cost implied by the 24/09 fill "
      f"({pct(theta_d, 2)} of notional), roll-friendly structures price at roughly **−2% to +2% p.a.**; with "
      f"2.5 pts less UF they reach **~9–12% p.a.** Each 1% of UF costs ~4% p.a. of coupon on a note expected "
      f"to live ~3 months.")
    w("- **Why your structures drifted from KO 80–85 to 95–100 (Jul→Sep):** the July/August fills (KO 80–85, "
      "KI 50–60, ~20%) only reconcile with the September fee level if memory vols were ~20–30 points higher "
      "than today, which fits July's realized swings. Memory IVs now sit at their 2nd–21st 52-week percentile, "
      "so holding 15–17% forced KO and KI up. That is what the September trades did.")
    b0 = bench[(bench["basket"] == "MU+SNDK+SKHY") & (bench["ko"] == 95)].iloc[0]
    w(f"- **The current memory basket fails the framework on every hard filter.** MU+SNDK+SKHY 95/70/70: "
      f"P(KO @ obs #1) {pct(b0['p_ko1'])}, P(loss) {pct(b0['p_loss_mem'])} (E[loss | loss] {pct(b0['e_loss_mem'], 0)}); "
      f"SK hynix (27/10) and Sandisk (~30/10) report inside obs #1, and KI 70 sits above the 13-week-low limit "
      f"(SNDK {pct(scr.loc['SNDK', 'ki_cap_13w'], 0)}, SKHY {pct(scr.loc['SKHY', 'ki_cap_13w'], 0)}, MU {pct(scr.loc['MU', 'ki_cap_13w'], 0)}).")
    w("")

    # ---------------------------------------------------------------- counters
    w("## 1. Counters in the lists, screened")
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
        if t == "AMD":
            return "Avoid: strong-day fix, px 24% above LO PT"
        n, br = freq.get(t, 0), best_rank.get(t, 99)
        role = "engine" if s["iv"] >= 0.58 else "third leg"
        tier = 1 if (br <= 3 or n >= 20) else 2 if (br <= 15 or n >= 5) else 3
        where = f"best #{br}" if br < 99 else "not in top 25"
        return f"Tier {tier} {role} ({n} baskets, {where})"

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
            "Next print": pd.Timestamp(s["next_earn"]).strftime("%d/%m") + (" (c)" if "confirmed" in str(s["earn_status"]) else " (e)"),
            "Verdict": verdict(t),
        })
    w(md_table(pd.DataFrame(rows)))
    w("")
    w("*KI cap (13W)* = 90% of the 13-week low ÷ spot, the highest KI that clears your 13-week-low hard filter. "
      "(c) confirmed date, (e) vendor estimate or prior-year pattern. LO PT upside is recomputed at the 24/09 close "
      "(foreign-listed lines keep the list's 17/09 figure). *Baskets* = filter-passing baskets containing the name; "
      "*best #* = its best position in the ranked table below; *engine* = 30D IV ≥ 58%.")
    w("")

    # ---------------------------------------------------------------- ranking
    w("## 2. Ranked structures")
    w("")
    w(f"Hard filters applied: no print inside obs #1, P(KO @ obs #1) ≥ 55%, P(loss) ≤ 12%, every KI at least 10% "
      f"below its 13-week low. Minimum coupon: 9% p.a. at roll pricing (the lowest target in your sweet-spot table). "
      f"Grid: KO 80–95, Strike = KI 50–80, inside your rules of thumb (KO ≤ 100 − 0.5·σ₁ₘ, KI ≤ e^(−0.75σ)). "
      f"Ranked on memory KO; simultaneous KO shown after the slash.")
    w("")
    rr = []
    for i, r in rank.head(15).iterrows():
        rr.append({
            "#": i + 1, "Basket": r["basket"].replace("+", " + "),
            "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
            "CPN roll / 24-09 cost": f"{pct(r['cpn_roll'])} / {pct(r['cpn_desk'])}",
            "P(KO@1)": pct(r["p_ko1"]),
            "P(KO≤3) mem/sim": f"{pct(r['p_ko3_mem'], 0)}/{pct(r['p_ko3_sim'], 0)}",
            "E[life] m": f"{r['life_mem']:.1f}/{r['life_sim']:.1f}",
            "P(loss)": f"{pct(r['p_loss_mem'])}/{pct(r['p_loss_sim'], 0)}",
            "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
            "Client EV": pct(r["client_ev"]),
            "CPN/IV": f"{r['cpn_iv']:.2f}",
            "Score": f"{r['roll_score']:.3f}",
            "Flags": "; ".join(x for x in [r["flags"], r["info"]] if x).replace("cheap (CPN/IV < 0.20); ", "")
                     .replace("; below high-vol target 16%", "").replace("; below mid target 12%", "")
                     .replace("below high-vol target 16%; ", "").replace("below mid target 12%; ", ""),
        })
    w(md_table(pd.DataFrame(rr)))
    w("")
    w(f"- **CPN roll** = model coupon at an all-in take of {pct(theta_r, 2)} (the 24/09 fill's {pct(theta_d, 2)} "
      f"less 2.5 pts of UF). **24-09 cost** = same structure at the 24/09 fill's all-in cost.")
    w("- **Client EV** (CPN × E[life]/12 − P(loss) × E[loss | loss]) comes out near −2.6% for every row. In a "
      "model where coupons and probabilities share one risk-neutral measure, it collapses to roughly minus the "
      "all-in fee plus a little funding, so it measures fee drag, not structure quality. At the 24/09 cost it "
      "is about −5% per roll.")
    w("- Penalties (−0.03 each): strong-day fix, avg ρ < 0.5 on 3 names, IV percentile > 90, ≥2 names shared "
      "with a live ledger basket. *px > LO PT* and *earnings ≤3d after obs #1* are shown but not penalised. Every "
      "row is below your regime coupon target and most have CPN/IV < 0.20, so those two flags are left out.")
    w("")
    w("Internal only (UF 1.0% under roll pricing):")
    w("")
    ir = []
    for i, r in rank.head(8).iterrows():
        ir.append({"#": i + 1, "Basket": r["basket"].replace("+", " + "),
                   "Fee velocity p.a.": pct(r["fee_velocity"]),
                   "Net-of-UF yield p.a.": pct(r["net_uf_yield"]),
                   "UF > 1-mth CPN and P(KO@1) > 70%": "FLAG" if r["uf_check"] is True or r["uf_check"] == "True" else "",
                   "+CPN per 1% UF cut": pct(r["uplift_per_1pct_uf"])})
    w(md_table(pd.DataFrame(ir)))
    w("")

    # ---------------------------------------------------------------- verdicts
    w("## 3. Top 3 verdicts")
    w("")
    v = rank.head(3)
    notes = {
        "ARM+DELL+DDOG": ("KO 80 sits {cush:.1f} monthly σ below spot and memory KO locks each name as it clears",
                          "ARM (LO Hold, PT $250 = 82% of spot, just above its $245 KO) de-rating into obs #1, or "
                          "an ARM/DDOG print landing before 02/11 (both estimated 04–05/11)"),
        "ARM+DELL+PDD": ("same ARM + DELL engine, with PDD (LO Buy, +41% to PT) as a near-uncorrelated third leg",
                         "an ARM-led AI-hardware sell-off in October; PDD adds China headline risk"),
        "AVGO+ARM+DELL": ("AVGO (LO Buy, +43% to PT) is the quality anchor and the best-correlated third leg "
                          "(avg ρ {rho:.2f}), which helps the worst-of KO",
                          "an AI-complex sell-off into the mega-cap prints of 27–29/10, which fall inside obs #1"),
    }
    for i, (_, r) in enumerate(v.iterrows()):
        why, brk = notes.get(r["basket"], ("a low KO on high-vol names", "a broad AI sell-off into obs #1"))
        fmt = {"cush": r["ko_cushion_sd"], "rho": r["avg_rho"]}
        w(f"{i + 1}. **{r['basket'].replace('+', ' + ')} {r['ko']}/{r['strike']}/{r['ki']}**: P(KO@1) {pct(r['p_ko1'])}, "
          f"P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 0)} at roll pricing. **Rolls:** {why.format(**fmt)}. "
          f"**Breaks:** {brk.format(**fmt)}.")
    w("")
    two = rank[rank["basket"] == "ARM+DELL"]
    if len(two):
        r = two.iloc[0]
        w(f"Best-coupon alternative: **ARM + DELL {r['ko']}/{r['strike']}/{r['ki']}** (two names): P(KO@1) {pct(r['p_ko1'])}, "
          f"P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 0)} at roll pricing.")
    nm = best[~best["basket"].str.contains("ARM")].head(2)
    if len(nm):
        s = "; ".join(f"**{r['basket'].replace('+', ' + ')} {r['ko']}/{r['strike']}/{r['ki']}** "
                      f"(P(KO@1) {pct(r['p_ko1'])}, P(loss) {pct(r['p_loss_mem'])}, ~{pct(r['cpn_roll'], 0)})"
                      for _, r in nm.iterrows())
        w(f"If you want no ARM exposure: {s}.")
    w("")

    # ---------------------------------------------------------------- economics
    w("## 4. Why the coupons are thin: fee load and vol regime")
    w("")
    w(f"The model prices each note at par less an all-in issuer take, calibrated to the 24/09 USD fill "
      f"(MU + SNDK + SKHY 95/70/70 at 16.20%), which implies **{pct(theta_d, 2)} of notional** (UF plus the "
      f"issuer's margin plus model error). The other September fills imply a similar take:")
    w("")
    ck = [{"Fill": f"{pd.Timestamp(c['td']).strftime('%d/%m')} {c['ccy']}", "Basket": c["basket"].replace("+", " + "),
           "KO/Str/KI": f"{c['ko']}/{c['strike']}/{c['ki']}", "Desk CPN": f"{c['desk_cpn']:.2f}%",
           "Implied all-in take": pct(c["implied_theta"], 2), "P(KO@1)": pct(c["p_ko1"]),
           "P(loss)": pct(c["p_loss"])} for c in cal["cross_checks"]]
    w(md_table(pd.DataFrame(ck)))
    w("")
    w("MYR and AUD fills are run on USD rates (no quanto adjustment), so read their implied take as ±1 pt. "
      "The term structure matters: 30-day IVs for NVDA, AVGO, PDD and PLTR sit 9–11 vol points under their "
      "12-month IVs, so the model uses 30D IV for month 1 (your obs #1 odds) and the 12M-implied forward vol "
      "for months 2–12. With flat 30D vols the NVDA + AMZN + GOOGL fill read 4.1 pts too low; with the term "
      "structure it reads within 1.3 pts.")
    w("")
    w(f"A fixed take hits short-life notes hardest. For the top structure the coupon annuity is "
      f"{t1['annuity']:.3f}, so each 1% of fee is worth {pct(t1['uplift_per_1pct_uf'])} p.a. of coupon:")
    w("")
    tt = [{"KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}", "P(KO@1)": pct(r["p_ko1"]),
           "P(KO≤3)": pct(r["p_ko3_mem"], 0), "E[life] m": f"{r['life_mem']:.1f}", "P(loss)": pct(r["p_loss_mem"]),
           "E[loss\\|loss]": pct(r["e_loss_mem"], 0), "CPN @24/09 cost": pct(r["cpn_desk"]),
           "CPN @roll": pct(r["cpn_roll"]), "Hard filters": r["hard_fail"] or "pass"} for _, r in toff.iterrows()]
    w(f"**{top_b.replace('+', ' + ')}**, same basket, different structures:")
    w("")
    w(md_table(pd.DataFrame(tt)))
    w("")
    k85, k90 = toff[toff["ko"] == 85].iloc[0], toff[toff["ko"] == 90].iloc[0]
    w(f"At the September cost this basket pays {pct(k85['cpn_desk'], 1)} at KO 85 (P(KO@1) {pct(k85['p_ko1'], 0)}, "
      f"P(loss) {pct(k85['p_loss_mem'], 0)}) and {pct(k90['cpn_desk'], 1)} at KO 90 (P(KO@1) {pct(k90['p_ko1'], 0)}, "
      f"P(loss) {pct(k90['p_loss_mem'], 0)}). Getting to 12–16% means breaking your P(KO@1) and P(loss) filters: "
      "today, coupon and monthly KO pull against each other.")
    w("")
    w("The July–August fills (KO 80–85, KI 50–60, ~20%) only reprice at a September-like all-in take if memory "
      "vols were 20–30 points higher than today, which matches July's daily moves in MU and SNDK:")
    w("")
    w(md_table(summer_fills(snap, closes)))
    w("")
    w("Your recent and live house structures, re-run for a 01/10 fixing (caps off):")
    w("")
    bt = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{r['strike']}/{r['ki']}",
           "CPN @24/09 cost": pct(r["cpn_desk"]), "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3_mem"], 0),
           "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
           "Fails": r["hard_fail"] or "none", "Prints in obs #1": r["earnings_in_obs1"] or "none"}
          for _, r in bench.iterrows()]
    w(md_table(pd.DataFrame(bt)))
    w("")
    w("Vol regime: 52-week IV percentiles are SKHY 2%, NVDA 1%, AVGO 2%, SNDK 6%, MU 21%. Selling vol "
      "(which is what the client does in an ACEL) pays little until it re-rates, typically after a sell-off or "
      "into earnings, and your earnings filter rules out the second.")
    w("")

    # ---------------------------------------------------------------- levers
    w("## 5. Coupon lever that keeps P(loss): strike above KI")
    w("")
    w("A strike above the KI leaves P(loss) unchanged (the KI still sets the loss event) but raises the loss "
      "once it happens. You have used it before (04/09 75/55, 09/09 80/70).")
    w("")
    lt = [{"Basket": r["basket"].replace("+", " + "), "KO/Str/KI": f"{r['ko']}/{int(r['strike'])}/{r['ki']}",
           "CPN @roll": pct(r["cpn_roll"]), "CPN @24/09": pct(r["cpn_desk"]), "P(KO@1)": pct(r["p_ko1"]),
           "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0)}
          for _, r in lev.head(9).iterrows()]
    w(md_table(pd.DataFrame(lt)))
    w("")

    # ---------------------------------------------------------------- desk lines
    w("## 6. Desk request lines (Florence)")
    w("")
    w("```")
    reqs = []
    for _, r in rank.head(3).iterrows():
        reqs.append((r["basket"], r["ko"], r["strike"], r["ki"]))
        reqs.append((r["basket"], r["ko"], r["strike"] + 10, r["ki"]))
    if len(two):
        r = two.iloc[0]
        reqs.append((r["basket"], r["ko"], r["strike"], r["ki"]))
    if len(nm):
        r = nm.iloc[0]
        reqs.append((r["basket"], r["ko"], r["strike"], r["ki"]))
    for b, ko, st, ki in reqs:
        w(f"USD 12M {bbg(uni, b)} | Strike {int(st)} | KO {int(ko)} | KI {int(ki)} | CPN ?")
    w("```")
    w("")
    w("- Ask for each line at your standard UF and at UF 1.0%. The model expects roughly −2% to +1% and "
      "9–12.5% respectively, with the strike-70 variants ~3 pts higher.")
    w("- Memory KO, monthly obs, European KI, closing prices. Preferred fixing 01/10, after MU's 30/09 print "
      "has moved the AI-hardware complex. Obs #1 then lands 02/11, 2–3 days before ARM's and DDOG's estimated "
      "prints: get both dates confirmed first, and if either lands on or before 02/11, fix by 29/09 instead.")
    w("- Re-check the 20-day-MA strong-day test on the fixing morning.")
    w("")

    # ---------------------------------------------------------------- releases
    w("## 7. Release drafts: pre-filled, waiting on the quote")
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
            sp, hi = s["spot"], s["hi52"]
            w("")
            w(f"{uni[t]['name']} ({uni[t]['bbg']})")
            w(f"Current Price: ${sp:,.2f}")
            w(f"52-Week High: ${hi:,.2f}")
            w(f"Indicative KO Price: ${sp * r['ko'] / 100:,.2f}")
            w(f"Indicative Strike Price: ${sp * r['strike'] / 100:,.2f}")
            w(f"Indicative KI Price: ${sp * r['ki'] / 100:,.2f}")
        w("")
        w(f"Indicative prices as of {PRICES_ASOF}. Official KO, Strike and KI levels to be fixed based on the "
          f"closing prices on the trade date, {TD_LONG}.")
        w("```")
        w("")
    w("Do not send until Florence's coupon is approved. Update the trade date if you fix on 29/09.")
    w("")

    # ---------------------------------------------------------------- method
    w("## Method and assumptions")
    w("")
    w(f"- Spot = 24/09 close; 52W high = max(live, IBKR 52W high); 13W low from IBKR. Correlations from 1Y daily "
      f"log returns (SKHY since its July listing). Risk-neutral drift, r = {pct(meta['r_usd'], 1)}, LO dividend yields.")
    w(f"- Vol: 30D ATM IV in month 1, forward vol from ~12M ATM option IV (Sep-2027 expiry, 24/09 mids) in months "
      f"2–12, and a +5 vol-pt bump phasing in between 100% and the KI level. MU month 1 uses "
      f"{pct(meta['mu_m1_iv'], 1)}: its 30D IV less the ±8.9% move implied by the 02/10 straddle.")
    w("- Loss at maturity if no KO and worst-of < KI: 1 − WO/Strike. KO modes: memory per stock (ranked) and "
      "simultaneous (shown after the slash).")
    w("- Roll Score = 0.45·P(KO@1) + 0.25·P(KO≤3) + 0.20·(1 − P(loss)/0.12) + 0.10·min(CPN/IV ÷ 0.30, 1) "
      "− 0.03 per penalty, with CPN at roll pricing and IV = basket average 30D IV.")
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
