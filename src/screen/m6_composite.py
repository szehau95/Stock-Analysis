"""Module 6: value score, composite, quadrant, weight sensitivity and rule-based lean/confidence (core six)."""
import numpy as np, pandas as pd
from common import CORE, ASOF, OUT, pct_score

F = pd.read_csv(f"{OUT}/m14_fundamentals_all9.csv", index_col=0).loc[CORE]
Q = pd.read_csv(f"{OUT}/m24_core6.csv", index_col=0)
T = pd.read_csv(f"{OUT}/m5_technicals.csv", index_col=0)

V = pd.DataFrame(index=CORE)
V["mispricing"] = pct_score(F.mispricing)
V["resid"] = pct_score(F.resid_pct, higher_better=False)
V["pb_z5"] = pct_score(F.pb_z5, higher_better=False)
V["dy_ntm"] = pct_score(F.dy_ntm)
V["value_score"] = 0.40 * V.mispricing + 0.30 * V.resid + 0.15 * V.pb_z5 + 0.15 * V.dy_ntm
# robustness: value score with a uniform beta of 1 in the COE
V["value_score_beta1"] = 0.40 * pct_score(F.mispricing_beta1) + 0.30 * V.resid + 0.15 * V.pb_z5 + 0.15 * V.dy_ntm

S = pd.DataFrame(index=CORE)
S["value"], S["quality"], S["tech"] = V.value_score, Q.quality_score, T.tech_score
S["value_beta1"] = V.value_score_beta1


def comp(w):
    return w[0] * S.value + w[1] * S.quality + w[2] * S.tech


S["composite"] = comp((0.40, 0.30, 0.30))
S["comp_value_tilt"] = comp((0.60, 0.20, 0.20))
S["comp_tech_tilt"] = comp((0.20, 0.30, 0.50))
S["comp_beta1"] = 0.40 * S.value_beta1 + 0.30 * S.quality + 0.30 * S.tech
for c in ["composite", "comp_value_tilt", "comp_tech_tilt", "comp_beta1"]:
    S[f"rank_{c}"] = S[c].rank(ascending=False).astype(int)

cheap = S.value >= 50
up = S.tech >= 50
S["quadrant"] = np.select([cheap & up, cheap & ~up, ~cheap & up], ["ACTIONABLE BUY", "VALUE TRAP WATCH", "MOMENTUM HOLD"], "AVOID / UNDERWEIGHT")
S["regime"] = T.regime
S["flip_trigger"] = T.flip_trigger

quad_b1 = np.select([(S.value_beta1 >= 50) & up, (S.value_beta1 >= 50) & ~up, (S.value_beta1 < 50) & up],
                    ["ACTIONABLE BUY", "VALUE TRAP WATCH", "MOMENTUM HOLD"], "AVOID / UNDERWEIGHT")
S["quadrant_beta1"] = quad_b1
up_c = T.tech_score_cons >= 50
S["tech_cons"] = T.tech_score_cons
S["quadrant_t1cons"] = np.select([cheap & up_c, cheap & ~up_c, ~cheap & up_c], ["ACTIONABLE BUY", "VALUE TRAP WATCH", "MOMENTUM HOLD"], "AVOID / UNDERWEIGHT")
S["chk_quadrant_t1cons"] = S.quadrant == S.quadrant_t1cons
S["comp_t1cons"] = 0.40 * S.value + 0.30 * S.quality + 0.30 * S.tech_cons
S["rank_comp_t1cons"] = S.comp_t1cons.rank(ascending=False).astype(int)

# v1.1 news-flow flag: a negative broker action in the 30 days to ASOF whose stated reason (here: treasury MTM / 3Q26
# results risk) is not yet in reported numbers. It blocks an Overweight until the next print resolves it.
BA = pd.read_csv("data/clean/scr_broker_actions.csv")
BA["d"] = pd.to_datetime(BA.date.str.replace("~", "", regex=False), dayfirst=True)
recent_neg = BA[(BA.negative == 1) & (BA.d >= ASOF - pd.Timedelta(days=30)) & (BA.d <= ASOF) & BA.bank.isin(CORE)]
S["recent_negative_action"] = [", ".join(f"{r.house} {r.to}" for r in recent_neg[recent_neg.bank == b].itertuples()) for b in S.index]
S["flagged"] = S.recent_negative_action != ""
S["rate_risk_cet1_bp_100"] = Q.rate_risk_cet1_bp_100


def lean(rank, quad, flagged):
    """OW = top-2 in ACTIONABLE BUY / VALUE TRAP WATCH and not flagged; UW = AVOID and bottom-2; else Neutral."""
    ow = (rank <= 2) & quad.isin(["ACTIONABLE BUY", "VALUE TRAP WATCH"]) & ~flagged
    uw = (quad == "AVOID / UNDERWEIGHT") & (rank >= 5)
    return pd.Series(np.select([ow, uw], ["Overweight", "Underweight"], "Neutral"), index=rank.index)


S["lean"] = lean(S.rank_composite, S.quadrant, S.flagged)
S["top2_but_flagged"] = (S.rank_composite <= 2) & S.quadrant.isin(["ACTIONABLE BUY", "VALUE TRAP WATCH"]) & S.flagged
# Confidence = does the lean survive each alternative specification? (4/4 High, 3/4 Medium, <=2 Low)
alts = {"value_tilt": (S.rank_comp_value_tilt, S.quadrant), "tech_tilt": (S.rank_comp_tech_tilt, S.quadrant),
        "beta1": (S.rank_comp_beta1, S.quadrant_beta1), "t1cons": (S.rank_comp_t1cons, S.quadrant_t1cons)}
for k, (r, q) in alts.items():
    S[f"lean_{k}"] = lean(r, q, S.flagged)
    S[f"chk_{k}"] = S[f"lean_{k}"] == S.lean
n_ok = S[[f"chk_{k}" for k in alts]].sum(axis=1)
S["checks_passed"] = n_ok
S["confidence"] = np.select([n_ok == 4, n_ok == 3], ["High", "Medium"], "Low")

# Top pick: highest composite among Overweights. A gap to the next Overweight-eligible name under 2 points is a tie,
# broken by (1) no news-flow flag, (2) lower rate risk (CET1 bp per +100bp), (3) better quadrant.
elig = S[S.quadrant.isin(["ACTIONABLE BUY", "VALUE TRAP WATCH"])].sort_values("composite", ascending=False)
qrank = {"ACTIONABLE BUY": 0, "VALUE TRAP WATCH": 1}
if len(elig) > 1 and elig.composite.iloc[0] - elig.composite.iloc[1] < 2:
    tied = elig[elig.composite >= elig.composite.iloc[0] - 2].copy()
    tied["q"] = tied.quadrant.map(qrank)
    top = tied.sort_values(["flagged", "rate_risk_cet1_bp_100", "q"]).index[0]
    tie_note = f"tie among {list(tied.index)} broken on flag, rate risk, quadrant"
else:
    top, tie_note = elig.index[0], "no tie"
S["top_pick"] = S.index == top
survives = bool((S.loc[top, "rank_comp_value_tilt"] == 1) and (S.loc[top, "rank_comp_tech_tilt"] == 1))
order_conf = ["Low", "Medium", "High"]
S["top_pick_designation_conf"] = ""
S.loc[top, "top_pick_designation_conf"] = order_conf[max(0, order_conf.index(S.loc[top, "confidence"]) - (0 if survives else 1))]
print("TIE:", tie_note)

pd.set_option("display.width", 250, "display.max_columns", 40)
print(V.round(1).to_string())
print(S.sort_values("composite", ascending=False).round(1).to_string())
print("TOP:", top, "survives both sensitivities:", survives)
S.join(V.drop(columns=["value_score"])).to_csv(f"{OUT}/m6_composite.csv")
