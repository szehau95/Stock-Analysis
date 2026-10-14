"""Module 6: value score, composite, quadrant, weight sensitivity and rule-based lean/confidence (core six)."""
import numpy as np, pandas as pd
from common import CORE, OUT, pct_score

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
# Lean confidence: consistency checks passed (4 = High, 3 = Medium, <=2 = Low)
S["chk_value_tilt"] = (S.rank_comp_value_tilt - S.rank_composite).abs() <= 1
S["chk_tech_tilt"] = (S.rank_comp_tech_tilt - S.rank_composite).abs() <= 1
S["chk_quadrant_beta1"] = S.quadrant == S.quadrant_beta1
n_ok = S[["chk_value_tilt", "chk_tech_tilt", "chk_quadrant_beta1", "chk_quadrant_t1cons"]].sum(axis=1)
S["checks_passed"] = n_ok
S["confidence"] = np.select([n_ok == 4, n_ok == 3], ["High", "Medium"], "Low")
# Lean: OW = top-2 composite in an actionable/value-watch quadrant; UW = AVOID quadrant and bottom-2 composite; else Neutral
S["lean"] = np.select([(S.rank_composite <= 2) & S.quadrant.isin(["ACTIONABLE BUY", "VALUE TRAP WATCH"]),
                       (S.quadrant == "AVOID / UNDERWEIGHT") & (S.rank_composite >= 5)], ["Overweight", "Underweight"], "Neutral")
for b in S.index:  # prompt rule: top-pick designation loses a notch unless #1 under both weight sensitivities
    S.loc[b, "survives_both_as_no1"] = bool((S.loc[b, "rank_comp_value_tilt"] == 1) and (S.loc[b, "rank_comp_tech_tilt"] == 1))
top = S.composite.idxmax()
survives = S.loc[top, "survives_both_as_no1"]

pd.set_option("display.width", 250, "display.max_columns", 40)
print(V.round(1).to_string())
print(S.sort_values("composite", ascending=False).round(1).to_string())
print("TOP:", top, "survives both sensitivities:", survives)
S.join(V.drop(columns=["value_score"])).to_csv(f"{OUT}/m6_composite.csv")
