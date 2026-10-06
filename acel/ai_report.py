#!/usr/bin/env python3
"""Write output/ai_pullback_2026-10-06/report.md from ai_screen.py's outputs (run that first).

Re-runs the desk-request lines, the best baskets without ARM and an ARM ex-earnings scenario at
the finalist path count and seed, so every number quoted comes off the same paths as the
finalists table.
"""
import json
import math
import os
import re

import numpy as np
import pandas as pd

import ai_screen as A
import engine as E
from iv12m import implied
from report import md_table, pct

OUT = A.OUT
DESK = [  # basket, KO, strike, KI, UF the desk is asked to quote at
    ("ORCL+ARM+AMAT", 95, 75, 65, 0.04),
    ("ARM+AMAT", 100, 75, 65, 0.04),
    ("ORCL+ARM+AVGO", 100, 75, 65, 0.04),
    ("ORCL+ARM+AMAT", 90, 75, 65, 0.02),
    ("ARM+AMAT", 95, 75, 65, 0.02),
    ("ORCL+ARM+AVGO", 92, 75, 65, 0.02),
]
REF = {  # structures quoted in the text
    "no_lever": ("ORCL+ARM+AMAT", 95, 65, 65),
    "uf1": ("ORCL+ARM+AMAT", 88, 75, 65),
    "clean": ("ORCL+AMAT+AVGO", 100, 75, 65),   # best basket without ARM at UF 2%
}
TD_AFTER = "2026-11-06"   # first fixing after ARM's 04/11 print
TOP5 = ["ORCL", "ARM", "AMAT", "AVGO", "BIDU"]
SOURCES = {
    "ARM": "https://newsroom.arm.com/news/arm-announces-earnings-release-date-for-second-quarter-fiscal-year-ending-2027",
    "AVGO": "https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial",
    "AMAT": "https://www.tipranks.com/stocks/amat/earnings",
    "ORCL": "https://www.tipranks.com/stocks/orcl/earnings",
    "BIDU": "https://www.tipranks.com/stocks/bidu/earnings",
    "BABA": "https://www.tipranks.com/stocks/baba/earnings",
    "ADBE": "https://www.tipranks.com/stocks/adbe/earnings",
    "NOW": "https://www.tipranks.com/stocks/now/earnings",
}


def d(x, fmt="%d/%m/%Y"):
    return pd.Timestamp(x).strftime(fmt)


def lv(r):
    return f"{int(r['ko'])}/{int(r['strike'])}/{int(r['ki'])}"


def nm(b):
    return " + ".join(b.split("+"))


def bbg_line(uni, b):
    return " + ".join(uni[t]["bbg"] for t in b.split("+"))


def arm_event():
    """ARM's implied 04/11 move from the weeklies either side of the print."""
    q = pd.read_csv(os.path.join(A.DATA, "arm_event_quotes_2026-10-06.csv"))
    now = pd.Timestamp(q["snap_utc"].iloc[0])
    ivs, ts = [], []
    for _, r in q.iterrows():
        exp = pd.Timestamp(r["expiry"]).tz_localize("America/New_York") + pd.Timedelta(hours=16)
        t = (exp - now).total_seconds() / (365 * 86400)
        c = implied((r["call_bid"] + r["call_ask"]) / 2, r["spot"], r["strike"], t, 0.0, "c")
        p = implied((r["put_bid"] + r["put_ask"]) / 2, r["spot"], r["strike"], t, 0.0, "p")
        ivs.append((c + p) / 2)
        ts.append(t)
    base, post = ivs
    return {"base": base, "post": post, "move": math.sqrt((post ** 2 - base ** 2) * ts[1])}


def misses(r):
    out = []
    if "prints before obs #1" in str(r["rule_flags"]):
        out.append("print")
    if r["p_ko1"] < 0.55:
        out.append("P(KO@1)")
    if r["p_loss_mem"] > 0.12:
        out.append("P(loss)")
    return ", ".join(out) or "none"


def short_flags(r):
    out = []
    for f in str(r.get("rule_flags") or "").split("; "):
        if f.startswith("prints before"):
            continue                                   # shown under Misses
        m = re.match(r"<30% off high \((.*)\)", f)
        if m:
            out.append(m.group(1).replace("/", ", ").replace("-", "−") + " off high")
            continue
        m = re.match(r"(KO|KI) above (\d+) rule of thumb", f)
        if m:
            out.append(f"{m.group(1)} > {m.group(2)} rule")
            continue
        if f:
            out.append(f)
    for f in str(r.get("flags") or "").split("; "):
        if f.startswith("strong-day"):
            out.append(f.replace("strong-day fix", "strong day"))
        elif f.startswith("low corr"):
            out.append("avg ρ < 0.5")
        elif f.startswith(("IV pct", "overlaps")):
            out.append(f)
    return "; ".join(out)


def ranked(df, cpn_col, start=1):
    rows = []
    for i, (_, r) in enumerate(df.iterrows(), start):
        rows.append({
            "#": i, "Basket": nm(r["basket"]), "KO/Str/KI": lv(r), "CPN": pct(r[cpn_col]),
            "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3_mem"], 0),
            "P(KO ever)": pct(r["p_ko_ever"], 0), "E[life] m": f"{r['life_mem']:.1f}",
            "P(loss)": pct(r["p_loss_mem"]), "E[loss\\|loss]": pct(r["e_loss_mem"], 0),
            "avg ρ": f"{r['avg_rho']:.2f}", "Misses": misses(r), "Flags": short_flags(r),
        })
    return md_table(pd.DataFrame(rows))


def print_cell(r):
    t = pd.Timestamp(r["next_earn"])
    if t < pd.Timestamp(A.ASOF):
        return f"{d(t)} (reported)"
    st = str(r["earn_status"])
    tag = "confirmed" if ("confirmed" in st and "unconfirmed" not in st) else (
        "company" if "company" in st else "est.")
    return f"{d(t)} {tag}"


def screen_note(t, r, priced):
    if t in priced:
        return "**priced**"
    if not r["core_ai"]:
        return "outside AI theme"
    if r["corrected"]:
        return "≥30% off, prints first" if r["earn_in_obs1"] else "≥30% off"
    if r["near_miss"]:
        return "25–30% off, prints first" if r["earn_in_obs1"] else "25–30% off"
    return "<25% off"


def main():
    cal, obs1, uni, snap, ledger, closes, scr = A.setup()
    meta = json.load(open(os.path.join(OUT, "run_meta.json")))
    n_paths, seed = meta["final_paths"], meta.get("seed", 20261006) + 1
    fin = pd.read_csv(os.path.join(OUT, "finalists.csv"))
    card = pd.read_csv(os.path.join(OUT, "names.csv"), index_col=0)
    grid = pd.read_csv(os.path.join(OUT, "grid.csv.gz"))
    priced = meta["priced"]
    ev = arm_event()

    env = (snap, closes, uni, scr, ledger, {})
    env_x = (snap, closes, uni, scr, ledger, {"ARM": ev["base"]})   # ARM month 1 without the print

    def run(b, ko, st, ki, e=env):
        return A.run_line(b.split("+"), ko, st, ki, e, n_paths, seed, cal)

    lines = []
    for i, (b, ko, st, ki, uf) in enumerate(DESK, 1):
        r, x = run(b, ko, st, ki), run(b, ko, st, ki, env_x)
        col = f"cpn_uf{uf * 100:.0f}"
        r.update({"line": i, "uf": uf, "cpn": r[col], "cpn_x": x[col], "p_ko1_x": x["p_ko1"],
                  "p_loss_x": x["p_loss_mem"]})
        lines.append(r)
    lines = pd.DataFrame(lines)
    lines.to_csv(os.path.join(OUT, "desk_lines.csv"), index=False, float_format="%.4f")
    ref = {k: run(*v) for k, v in REF.items()}

    # best baskets without ARM: highest coupon at UF 4%, best P(KO@1) at >=15% for UF 2% / 1%
    na = grid[~grid["basket"].str.contains("ARM")]
    picks = [na.sort_values("cpn_uf4", ascending=False).groupby("basket").head(1).head(3)]
    picks += [A.best_at(na, uf).head(3) for uf in (0.02, 0.01)]
    seen, noarm = set(), []
    for p in picks:
        for _, r in p.iterrows():
            key = (r["basket"], r["ko"], r["strike"], r["ki"])
            if key not in seen:
                seen.add(key)
                noarm.append(run(r["basket"], int(r["ko"]), int(r["strike"]), int(r["ki"])))
    noarm = pd.DataFrame(noarm).sort_values("cpn_uf4", ascending=False)
    noarm.to_csv(os.path.join(OUT, "no_arm.csv"), index=False, float_format="%.4f")

    # true monthly rolls: every hard filter (grid, 50k paths)
    strict = grid[(grid["p_ko1"] >= 0.55) & (grid["p_loss_mem"] <= 0.12)
                  & ~grid["rule_flags"].fillna("").str.contains("prints before")]
    strict_best = strict.sort_values("cpn_uf1", ascending=False).iloc[0]

    corr = np.log(closes[priced]).diff().corr(min_periods=30)
    f4 = fin[fin["uf"] == 0.04].sort_values("p_ko1", ascending=False)
    f2 = fin[fin["uf"] == 0.02].sort_values("p_ko1", ascending=False)
    f1 = fin[fin["uf"] == 0.01].sort_values("p_ko1", ascending=False)
    L = lines.set_index("line")
    l1, l2, l4, l5 = (L.loc[i] for i in (1, 2, 4, 5))
    s = scr
    obs1_after = E.obs1_date(TD_AFTER)
    after_in = [t for t in priced if pd.Timestamp(TD_AFTER) < pd.Timestamp(s.loc[t, "next_earn"]) <= pd.Timestamp(obs1_after)]
    after_out = [t for t in priced if t not in after_in]
    uplift = 0.01 / lines["annuity"]
    corrected = s[s["corrected"] & s["core_ai"]].sort_values("off_hi52")
    corrected_clean = [t for t in corrected.index if not s.loc[t, "earn_in_obs1"]]
    corrected_late = [t for t in corrected.index if s.loc[t, "earn_in_obs1"]]
    n4 = len(f4)
    arm_share = f4["basket"].str.contains("ARM").mean() if n4 else float("nan")

    def ivs(t):
        return f"{s.loc[t, 'iv']:.0%} / {s.loc[t, 'iv12m']:.0%}"

    def off(t):
        return f"{s.loc[t, 'off_hi52']:.0%}".replace("-", "−")

    def rho(a, b):
        return f"{corr.loc[a, b]:.2f}".replace("-", "−")

    md = []
    w = md.append
    w("# AI pull-back screen: ACEL counters off their highs, for a 15% coupon\n")
    w(f"Fixing **{d(A.TD)}**, obs #1 **{d(obs1)}**. Market data: IBKR, 06/10/2026 pre-market snapshot "
      f"(spot, 30D ATM IV, HV30, 52-week and 13-week ranges), daily closes to 05/10/2026, Sep-2027 ATM option mids "
      f"for the 12M vol of the priced names. Coupons use the desk calibration of 28/09/2026 (issuer spread "
      f"{cal['spread']:.2%} + UF, pricing correlations floored at {cal['corr_floor']:.1f}). {meta['n_baskets']} baskets "
      f"of 1–3 names from {len(priced)} counters, {meta['n_structures']:,} structures at {meta['paths']:,} paths. "
      f"Finalists and desk lines re-run at {n_paths:,} paths. Coupons are model estimates for quote requests, not quotes. "
      f"Desk terms means UF 4%, the basis of the 28/09 quotes.\n")

    # ---------------------------------------------------------------- bottom line
    w("## Bottom line\n")
    w(f"- **A 15% coupon at desk terms needs ARM in the basket.** {len(corrected)} AI names on the lists are ≥30% off "
      f"their 52-week highs: {', '.join(f'{t} ({off(t)})' for t in corrected.index)}. "
      f"{', '.join(corrected_late)} print before obs #1, which leaves {', '.join(corrected_clean)}. "
      f"These four were priced with ARM, AMAT and AVGO (both {off('AMAT')}). ARM (30D IV {s.loc['ARM', 'iv']:.0%}) is "
      f"what funds 15% at UF 4%: {'all' if arm_share == 1 else f'{arm_share:.0%} of'} {n4} baskets that get there "
      f"contain it. Without ARM the ceiling at desk terms is "
      f"**{noarm['cpn_uf4'].max():.1%}**, at KO 100.")
    w(f"- **Best at desk terms: ORCL + ARM + AMAT, KO 95 / Strike 75 / KI 65, ~{l1['cpn']:.1%}.** "
      f"P(KO@1) {pct(l1['p_ko1'])}, P(KO by obs #3) {pct(l1['p_ko3_mem'], 0)}, P(KO ever) {pct(l1['p_ko_ever'], 0)}. "
      f"P(loss) {pct(l1['p_loss_mem'])}, with an average loss of {pct(l1['e_loss_mem'], 0)} when it happens. "
      f"This is a 12-month coupon trade, not a monthly roll. It misses the P(KO@1) and P(loss) filters, and "
      f"ARM reports on {d(s.loc['ARM', 'next_earn'])}, three sessions before obs #1.")
    w(f"- **Lower UF buys KO odds.** At UF 2% the same basket pays {l4['cpn']:.1%} at KO 90, with "
      f"P(KO@1) {pct(l4['p_ko1'])}. At UF 1% it pays {ref['uf1']['cpn_uf1']:.1%} at KO 88, with P(KO@1) "
      f"{pct(ref['uf1']['p_ko1'])}. On these notes (expected life {lines['life_mem'].min():.1f}–"
      f"{lines['life_mem'].max():.1f} months), each 1% of UF is worth {100 * uplift.min():.1f}–{100 * uplift.max():.1f} "
      f"pts of coupon.")
    w(f"- **ARM's print is worth ~{100 * (l1['cpn'] - l1['cpn_x']):.1f} pts of that coupon.** Its weeklies price a "
      f"±{ev['move']:.0%} move on {d(s.loc['ARM', 'next_earn'])} (30/10 expiry {ev['base']:.0%} IV, 06/11 expiry "
      f"{ev['post']:.0%}). With the print taken out of month 1, line 1 would pay {l1['cpn_x']:.1%} instead of "
      f"{l1['cpn']:.1%}, and P(KO@1) would be {pct(l1['p_ko1_x'])} instead of {pct(l1['p_ko1'])}. The extra coupon "
      f"is payment for carrying the print into obs #1.")
    w(f"- **Top 5 counters: {', '.join(TOP5)}.** ORCL ({off('ORCL')}) is the anchor: the deepest correction on the "
      f"list, {s.loc['ORCL', 'iv']:.0%} IV, and no print until ~{d(s.loc['ORCL', 'next_earn'])}. ARM funds the "
      f"coupon. AMAT is ARM's most correlated partner (ρ {rho('ARM', 'AMAT')}), but it is only {off('AMAT')} off its "
      f"high and {s.loc['AMAT', 'ma20_gap']:.0%} above its 20-day average, so fixing now locks in a high strike. "
      f"AVGO ({off('AVGO')}, LO Buy) adds KO odds at the lowest vol of the seven priced. BIDU ({off('BIDU')}) edges BABA "
      f"({off('BABA')}, LO Buy) on correlation to the US names. ADBE is {off('ADBE').lstrip('−')} off but has traded "
      f"against the semis (ρ {rho('ADBE', 'AMAT')} to AMAT), which works against you in a worst-of.")
    w(f"- **Memory: your instinct holds on the numbers.** MU ({off('MU')}), SKHY ({off('SKHY')}) and SNDK "
      f"({off('SNDK')}) are not 30% off their highs. SKHY, SNDK and WDC ({off('WDC')}) report before obs #1.")
    w(f"- **Nothing at ≥15% passes every hard filter.** A true monthly roll on these names (P(KO@1) ≥ 55%, "
      f"P(loss) ≤ 12%, no print before obs #1) pays at most {strict_best['cpn_uf1']:.1%} at UF 1% "
      f"({nm(strict_best['basket'])} {lv(strict_best)}).\n")

    # ---------------------------------------------------------------- IV screen
    w("## 1. IV screen: every AI name on the lists\n")
    w(f"Sorted by distance from the 52-week high. 30D IV is IBKR's ATM implied vol. For the {len(priced)} priced "
      f"names, 12M IV is from Sep-2027 ATM mids of 06/10/2026. Other names use the 24/09/2026 marks, and '—' means "
      f"no long-dated quote was pulled. IV pct is where today's 30D IV sits in its 1-year range. Obs #1 is "
      f"{d(obs1)}.\n")
    rows = []
    for t, r in s.sort_values("off_hi52").iterrows():
        rows.append({
            "Counter": t, "Theme": r["theme"], "LO": r["lo_rating"], "Off 52W high": off(t),
            "30D IV": pct(r["iv"], 0), "12M IV": "—" if r["iv12m_src"] == "30D" else pct(r["iv12m"], 0),
            "HV30": pct(r["hv30"], 0), "IV pct": pct(r["ivp52"], 0), "Next print": print_cell(r),
            "Before obs #1": "yes" if r["earn_in_obs1"] else "no", "Screen": screen_note(t, r, priced),
        })
    w(md_table(pd.DataFrame(rows)) + "\n")
    hv = s[s["core_ai"]].sort_values("iv", ascending=False).head(8)
    hv_clean = [t for t in hv.index if not hv.loc[t, "earn_in_obs1"]]
    hv_corr = [t for t in hv.index if hv.loc[t, "corrected"]]
    best_clean = s[s["core_ai"] & s["corrected"] & ~s["earn_in_obs1"]].sort_values("iv", ascending=False)
    w(f"- **Where the vol is:** {', '.join(f'{t} {v:.0%}' for t, v in hv['iv'].items())}. All but "
      f"{', '.join(hv_clean) or 'none'} report before obs #1, and only {' and '.join(hv_corr)} are ≥30% off their "
      f"highs. The highest-vol ≥30% name with a clean obs #1 is {best_clean.index[0]} at "
      f"{best_clean['iv'].iloc[0]:.0%}.")
    rest = best_clean.iloc[1:]
    w(f"- **The other clean ≥30% names sit at {rest['iv'].min():.0%}–{rest['iv'].max():.0%} IV** "
      f"({', '.join(f'{t} {v:.0%}' for t, v in rest['iv'].items())}). That is well short of what 15% needs at KO 95 "
      f"with the strike above KI. BIDU's and AVGO's IV is near the bottom of their "
      f"1-year ranges ({s.loc['BIDU', 'ivp52']:.0%} and {s.loc['AVGO', 'ivp52']:.0%} percentile): cheap vol, so "
      f"they add little coupon.")
    w(f"- **ARM's 30D IV ({s.loc['ARM', 'iv']:.0%}) includes the {d(s.loc['ARM', 'next_earn'])} print.** "
      f"Without it, ARM's vol is ~{ev['base']:.0%} (section 5). NOW ({off('NOW')}, LO Strong Buy, "
      f"{s.loc['NOW', 'iv']:.0%} IV) and IBM ({off('IBM')}) also price prints that land before obs #1.\n")

    # ---------------------------------------------------------------- top 5
    w("## 2. Top 5 counters\n")
    w("Ranked on the best P(KO @ obs #1) each name reaches inside a basket that pays at least 15%. The basket can "
      "differ by UF, and the best basket at desk terms is the same for the top three.\n")
    rows = []
    for i, t in enumerate(TOP5, 1):
        c = card.loc[t]
        up = s.loc[t, "lo_upside_now"]
        lo = s.loc[t, "lo_rating"] + ("" if np.isnan(up) else f" ({up:+.0%} to PT)".replace("-", "−"))
        rows.append({
            "#": i, "Counter": t, "Off 52W high": off(t), "30D / 12M IV": ivs(t),
            "Next print": print_cell(s.loc[t]),
            "Best P(KO@1), CPN ≥15%: UF 4% · 2% · 1%": " · ".join(pct(c[f"best_p_ko1_uf{u}"], 0) for u in (4, 2, 1)),
            "Best basket at desk terms": nm(c["best_basket_uf4"]) if isinstance(c["best_basket_uf4"], str) else "—",
            "LO": lo,
        })
    for t in [x for x in card.index if x not in TOP5]:
        c = card.loc[t]
        rows.append({
            "#": "", "Counter": f"*{t}*", "Off 52W high": off(t), "30D / 12M IV": ivs(t),
            "Next print": print_cell(s.loc[t]),
            "Best P(KO@1), CPN ≥15%: UF 4% · 2% · 1%": " · ".join(pct(c[f"best_p_ko1_uf{u}"], 0) for u in (4, 2, 1)),
            "Best basket at desk terms": nm(c["best_basket_uf4"]) if isinstance(c["best_basket_uf4"], str) else "—",
            "LO": s.loc[t, "lo_rating"] + ("" if np.isnan(s.loc[t, "lo_upside_now"]) else
                                           f" ({s.loc[t, 'lo_upside_now']:+.0%} to PT)".replace("-", "−")),
        })
    w(md_table(pd.DataFrame(rows)) + "\n")
    w(f"1. **ORCL**: {off('ORCL')} off its high, the deepest correction on the list. {ivs('ORCL')} IV, and the "
      f"13-week low allows a KI up to {s.loc['ORCL', 'ki_cap_13w']:.0%}. Next print ~{d(s.loc['ORCL', 'next_earn'])}, "
      f"well after obs #1. It is in the best basket at every UF. LO Hold, at its PT.")
    w(f"2. **ARM**: {off('ARM')}, with the highest IV on the list ({ivs('ARM')}). It funds the coupon: every basket "
      f"that reaches 15% at desk terms contains it. It fails your earnings rule: confirmed print "
      f"{d(s.loc['ARM', 'next_earn'])} after the close, three sessions before obs #1, priced at ±{ev['move']:.0%}. "
      f"The 13-week low ({snap.loc['ARM', 'low_13w']:.2f}) caps KI at {100 * s.loc['ARM', 'ki_cap_13w']:.0f}. "
      f"LO Hold, {abs(s.loc['ARM', 'lo_upside_now']):.0%} above its {uni['ARM']['lo_pt']} PT.")
    w(f"3. **AMAT**: {off('AMAT')}, short of your 30% line. {ivs('AMAT')} IV, and the best correlation on the list "
      f"to ARM ({rho('ARM', 'AMAT')}) and AVGO ({rho('AMAT', 'AVGO')}). It prints ~{d(s.loc['AMAT', 'next_earn'])}, "
      f"three days after obs #1. Strong-day flag: {s.loc['AMAT', 'ma20_gap']:.0%} above its 20-day average after a "
      f"rally from 474 on 24/09/2026, so fixing now locks in a high strike. LO Hold, above its {uni['AMAT']['lo_pt']} PT.")
    w(f"4. **AVGO**: {off('AVGO')}, also short of 30%. The lowest IV of the group ({ivs('AVGO')}) but the best house "
      f"view (LO Buy, {s.loc['AVGO', 'lo_upside_now']:+.0%} to the {uni['AVGO']['lo_pt']} PT), and it moves with ARM and AMAT (ρ "
      f"{rho('ARM', 'AVGO')} / {rho('AMAT', 'AVGO')}). It buys KO odds and costs coupon. Next print "
      f"{d(s.loc['AVGO', 'next_earn'])} (company plan).")
    w(f"5. **BIDU**: {off('BIDU')}, {ivs('BIDU')} IV, sitting {s.loc['BIDU', 'spot'] / snap.loc['BIDU', 'low_13w'] - 1:.0%} "
      f"above its 13-week low. Correlation to ORCL/ARM/AMAT is {rho('BIDU', 'ORCL')}/{rho('BIDU', 'ARM')}/"
      f"{rho('BIDU', 'AMAT')}, against BABA's {rho('BABA', 'ORCL')}/{rho('BABA', 'ARM')}/{rho('BABA', 'AMAT')}, which "
      f"is why it edges BABA on KO odds. **BABA** ({off('BABA')}, LO Buy) is the swap if you want the house view behind "
      f"the fifth name, since the numbers are within 1–2 pts. BIDU's 12M vol comes off a wide market.\n")
    w(f"**On a strict 30% line**, AMAT and AVGO drop out and BABA and ADBE come in. ADBE is the wrong partner. Over "
      f"the past year it traded as the 'AI loser' side of the trade (ρ {rho('ADBE', 'AMAT')} to AMAT, "
      f"{rho('ADBE', 'ARM')} to ARM), so in a worst-of it works as a hedge against the semis, which is the opposite "
      f"of what an ACEL needs. Its best P(KO@1) at ≥15% is the lowest of the seven.\n")
    w("1-year correlations of daily returns, priced names:\n")
    ct = corr.copy()
    ct = ct.map(lambda v: f"{v:.2f}".replace("-", "−"))
    ct.insert(0, "", ct.index)
    w(md_table(ct) + "\n")

    # ---------------------------------------------------------------- ranked baskets
    w("## 3. Baskets that clear 15%\n")
    w("For each basket, the structure with the highest P(KO @ obs #1) that pays at least 15%. KO grid 85–100, KI "
      "50–70 (capped at 90% of every name's 13-week low), strike at KI, KI+5 or KI+10. Probabilities on historical "
      "correlations, memory KO. *Misses* are the master prompt's hard filters.\n")
    w(f"### At desk terms (UF 4%): {n4} baskets, all with ARM\n")
    w(ranked(f4, "cpn") + "\n")
    w("### With a lower UF\n")
    w("UF 2%:\n")
    w(ranked(f2.head(8), "cpn") + "\n")
    w("UF 1%:\n")
    w(ranked(f1.head(8), "cpn") + "\n")
    w(f"Re-run on fresh paths, a few UF 1% lines land just under 15% (e.g. ARM + AMAT 90/75/65 at "
      f"{f1[f1['basket'] == 'ARM+AMAT']['cpn'].iloc[0]:.1%}). Treat them as ~15%.\n" if
      (f1["cpn"] < 0.15).any() and (f1["basket"] == "ARM+AMAT").any() else "")
    w("### Without ARM (no print before obs #1)\n")
    w("The best coupons at desk terms, and the best KO odds at ≥15% with a lower UF:\n")
    rows = []
    for _, r in noarm.iterrows():
        rows.append({"Basket": nm(r["basket"]), "KO/Str/KI": lv(r), "CPN UF 4%": pct(r["cpn_uf4"]),
                     "CPN UF 2%": pct(r["cpn_uf2"]), "CPN UF 1%": pct(r["cpn_uf1"]),
                     "P(KO@1)": pct(r["p_ko1"]), "P(KO≤3)": pct(r["p_ko3_mem"], 0),
                     "P(KO ever)": pct(r["p_ko_ever"], 0), "P(loss)": pct(r["p_loss_mem"]),
                     "E[loss\\|loss]": pct(r["e_loss_mem"], 0), "avg ρ": f"{r['avg_rho']:.2f}",
                     "Flags": short_flags(r)})
    w(md_table(pd.DataFrame(rows)) + "\n")
    w(f"Without ARM, 15% needs UF 2% or less and KO 95–100, and P(KO@1) tops out around "
      f"{noarm[noarm['cpn_uf1'] >= 0.15]['p_ko1'].max():.0%}. The ARM baskets above do better on every count except "
      f"the print.\n")

    # ---------------------------------------------------------------- verdicts
    w("## 4. Top 3 verdicts\n")
    w(f"1. **ORCL + ARM + AMAT 95/75/65 at desk terms, ~{l1['cpn']:.1%}.** P(KO@1) {pct(l1['p_ko1'])}, "
      f"P(KO≤3) {pct(l1['p_ko3_mem'], 0)}, P(loss) {pct(l1['p_loss_mem'])}. **Rolls:** ORCL has already de-rated "
      f"{off('ORCL').lstrip('−')} and does not report until mid-December. ARM and AMAT are the most correlated pair "
      f"on the list ({rho('ARM', 'AMAT')}), so the worst-of behaves closer to a two-name basket. **Breaks:** ARM's "
      f"{d(s.loc['ARM', 'next_earn'])} print (±{ev['move']:.0%}) lands three sessions before obs #1. AMAT is being "
      f"fixed after a {s.loc['AMAT', 'ma20_gap']:.0%} run above its 20-day average. With the strike at 75 above the "
      f"KI of 65, a breach costs at least {1 - 65 / 75:.0%}. Without the strike lever (95/65/65) the coupon is "
      f"{ref['no_lever']['cpn_uf4']:.1%}.")
    w(f"2. **ORCL + ARM + AMAT 90/75/65 at UF 2%, ~{l4['cpn']:.1%}.** The best KO odds at 15%: P(KO@1) "
      f"{pct(l4['p_ko1'])}, P(KO≤3) {pct(l4['p_ko3_mem'], 0)}, P(KO ever) {pct(l4['p_ko_ever'], 0)}, P(loss) "
      f"{pct(l4['p_loss_mem'])}. **Rolls:** KO 90 sits {math.log(100 / 90) / (l4['avg_iv'] / math.sqrt(12)):.1f} "
      f"monthly σ below spot instead of {math.log(100 / 95) / (l1['avg_iv'] / math.sqrt(12)):.1f} at KO 95. "
      f"**Costs:** 2 pts of UF. At desk terms the same line prices ~{l4['cpn_uf4']:.1%}. The breaks are the same as "
      f"line 1.")
    w(f"3. **ARM + AMAT 95/75/65 at UF 2%, ~{l5['cpn']:.1%}** (your pair). P(KO@1) {pct(l5['p_ko1'])}, "
      f"P(loss) {pct(l5['p_loss_mem'])}. **Rolls:** two names, so one fewer way to miss, and the most correlated pair "
      f"on the list. **Breaks:** both legs are AI semis: if the trade unwinds, nothing in the basket diversifies it. "
      f"At desk terms the pair reaches {l2['cpn']:.1%} only at KO 100 (P(KO@1) {pct(l2['p_ko1'])}).\n")
    w(f"If ARM's print before obs #1 is a deal-breaker, there are two choices. One is the clean-calendar basket "
      f"(ORCL + AMAT + AVGO, ~{ref['clean']['cpn_uf4']:.1%} at desk terms at KO 100, P(KO@1) "
      f"{pct(ref['clean']['p_ko1'])}), which falls short of 15%. "
      f"The other is to wait for the post-print window in section 5.\n")

    # ---------------------------------------------------------------- ARM event
    w("## 5. ARM's print: what it adds, and the window after it\n")
    w(f"ARM's weekly options: the 30/10 expiry (before the print) trades at {ev['base']:.1%} IV and the 06/11 expiry "
      f"(after it) at {ev['post']:.1%}. The difference prices a one-day move of ±{ev['move']:.1%} on "
      f"{d(s.loc['ARM', 'next_earn'])}. The table re-runs each ARM line with month-1 vol at {ev['base']:.0%}, the "
      f"ex-print level, at today's spot and with everything else unchanged.\n")
    rows = []
    for _, r in lines.iterrows():
        rows.append({"Line": int(r["line"]), "Basket": nm(r["basket"]), "KO/Str/KI": lv(r),
                     "UF": f"{r['uf']:.0%}", "CPN now": pct(r["cpn"]), "CPN ex-print": pct(r["cpn_x"]),
                     "P(KO@1) now": pct(r["p_ko1"]), "P(KO@1) ex-print": pct(r["p_ko1_x"]),
                     "P(loss) now": pct(r["p_loss_mem"]), "P(loss) ex-print": pct(r["p_loss_x"])})
    w(md_table(pd.DataFrame(rows)) + "\n")
    gap = 100 * (lines["cpn"] - lines["cpn_x"])
    w(f"- The print adds {gap.min():.1f}–{gap.max():.1f} pts of coupon and costs "
      f"{100 * (lines['p_ko1_x'] - lines['p_ko1']).min():.0f}–{100 * (lines['p_ko1_x'] - lines['p_ko1']).max():.0f} "
      f"pts off P(KO@1). The extra coupon pays for the extra risk; it is not free.")
    w(f"- **Calendar.** ARM ({d(s.loc['ARM', 'next_earn'])}) and AMAT (~{d(s.loc['AMAT', 'next_earn'])}) report eight "
      f"days apart, so any fixing between now and mid-November carries one of them into obs #1. The first clean ARM "
      f"window is a fixing around {d(TD_AFTER)} (obs #1 {d(obs1_after)}). {', '.join(after_out)} are clear then, while "
      f"{', '.join(after_in)} report before that obs #1. So the post-print trade is ORCL + ARM + AVGO, at a coupon "
      f"closer to the ex-print column, from wherever the stocks are after the print.\n")

    # ---------------------------------------------------------------- desk lines
    w("## 6. Desk request lines (Florence)\n")
    for uf in (0.04, 0.02):
        sub = lines[lines["uf"] == uf]
        w("```")
        w(f"Assuming TD {pd.Timestamp(A.TD).day}/{pd.Timestamp(A.TD).month} - UF {uf:.0%}")
        for _, r in sub.iterrows():
            w(f"USD 12M {bbg_line(uni, r['basket'])} | Strike {int(r['strike'])} | KO {int(r['ko'])} | "
              f"KI {int(r['ki'])} | CPN ?")
        w("```\n")
        w("- Model expectation at UF " + f"{uf:.0%}" + " (±1.5 pts): " + "; ".join(
            f"{nm(r['basket'])} {lv(r)}: ~{100 * r['cpn']:.0f}% (P(KO@1) {r['p_ko1']:.0%}, P(loss) {r['p_loss_mem']:.0%})"
            for _, r in sub.iterrows()) + ".\n")
    w(f"- ARM reports {d(s.loc['ARM', 'next_earn'])} after the close (confirmed), three sessions before obs #1 on "
      f"{d(obs1)}. Every line fails the earnings rule on ARM, and none passes P(KO@1) ≥ 55% or P(loss) ≤ 12%.")
    w(f"- AMAT reports ~{d(s.loc['AMAT', 'next_earn'])} (estimate), three days after obs #1. Strong-day fix on AMAT: "
      f"re-check the 20-day-MA test on the fixing morning.")
    w("- KO 95–100 sits above the KO ≤ 100 − 0.5·σ₁ₘ rule of thumb on the UF 4% lines. KI 65 is 1–2 pts above the "
      "e^(−0.75σ) rule on the ARM + AMAT lines. KI 65 is the most the 13-week-low rule allows with ARM in the basket.")
    w("- Memory KO, monthly obs, European KI, closing prices.")
    w("- No release drafts: releases follow approved quotes only.\n")

    # ---------------------------------------------------------------- calendar
    w("## 7. Earnings calendar\n")
    cal_names = priced + [t for t in ["NOW", "IBM", "WDC", "SNDK"] if t not in priced]
    rows = []
    for t in sorted(cal_names, key=lambda x: s.loc[x, "next_earn"]):
        r = s.loc[t]
        rows.append({"Counter": t, "Next print": print_cell(r), "Detail": str(r["earn_status"]),
                     f"Before obs #1 ({d(obs1)})": "yes" if r["earn_in_obs1"] else "no",
                     "Source": f"[link]({SOURCES[t]})" if t in SOURCES else "vendor estimate"})
    w(md_table(pd.DataFrame(rows)) + "\n")

    # ---------------------------------------------------------------- method
    w("## Method and assumptions\n")
    w(f"- Spot is the 06/10/2026 IBKR snapshot (pre-market, so the prior close for most names). The 52-week high and "
      f"13-week low come from IBKR. Correlations use 1-year daily log returns to 05/10/2026. Drift is risk-neutral "
      f"at r = 3.5%, with LO dividend yields.")
    w("- Vol: 30D ATM IV in month 1 (it includes ARM's print), forward vol from the Sep-2027 ATM IV in months 2–12, "
      "and a +5 vol-pt skew bump phasing in between 100% and the KI level.")
    w(f"- Coupons: par less an all-in take of issuer spread {cal['spread']:.2%} + UF. Pricing paths use historical "
      f"correlations floored at {cal['corr_floor']:.1f}. Both are fitted to the desk's 28/09/2026 quotes, ±1.1 pts. "
      f"Coupon at another UF = coupon + ΔUF / annuity. P(KO), E[life] and P(loss) run on historical correlations with "
      f"the same seed.")
    w("- Loss at maturity if there is no KO and the worst-of ends below KI: 1 − WO/Strike. KO is memory per stock.")
    w(f"- Universe: the {len(s)} tech and AI-related names on the attached LO lists (Comm Services, IT, Consumer Discretionary of "
      f"17/09/2026 and IT of 04/08/2026). Priced: AI names ≥25% off their 52-week high with no print before obs #1, "
      f"plus ARM and AMAT ({', '.join(priced)}). Every 1–3-name basket was priced.")
    w("- Hard rules enforced: KI ≤ 90% of each name's 13-week low. Reported, not enforced: prints before obs #1, the "
      "30% line, and the KO/KI rules of thumb. Enforcing them leaves nothing at 15%.")
    w("- None of the baskets shares two names with a ledger trade, so the live-overlap flag does not apply, whichever "
      "tranches have knocked out.")
    w("- All probabilities are risk-neutral. With a positive equity risk premium, P(KO) would be modestly higher and "
      "P(loss) modestly lower.")
    w(f"- ARM ex-print vol: the 305 strike's call/put mids on the 30/10 and 06/11 weeklies at "
      f"{pd.Timestamp(pd.read_csv(os.path.join(A.DATA, 'arm_event_quotes_2026-10-06.csv'))['snap_utc'].iloc[0]):%H:%M} UTC "
      f"06/10/2026. Move = √((σ₂² − σ₁²)·T₂), with month-1 vol set to σ₁.")

    with open(os.path.join(OUT, "report.md"), "w") as f:
        f.write("\n".join(md) + "\n")
    print(lines[["line", "basket", "ko", "strike", "ki", "uf", "cpn", "cpn_x", "p_ko1", "p_ko1_x", "p_ko3_mem",
                 "p_ko_ever", "life_mem", "p_loss_mem", "e_loss_mem", "annuity"]].round(4).to_string(index=False))
    print({k: (round(v["cpn_uf4"], 4), round(v["cpn_uf2"], 4), round(v["cpn_uf1"], 4), round(v["p_ko1"], 4))
           for k, v in ref.items()})
    print(noarm[["basket", "ko", "strike", "ki", "cpn_uf4", "cpn_uf2", "cpn_uf1", "p_ko1", "p_loss_mem"]].round(4)
          .to_string(index=False))
    print("strict best:", strict_best[["basket", "ko", "strike", "ki", "cpn_uf1", "cpn_uf4", "p_ko1", "p_loss_mem"]].to_dict())
    print("event:", ev, "obs1 after:", obs1_after, "in:", after_in)


if __name__ == "__main__":
    main()
