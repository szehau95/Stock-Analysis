"""Module 2b: securities-book rate risk — FVOCI marks on book value and CET1, FVTPL hit to 3Q26 earnings, +100bp stress.

Effective FVOCI duration is calibrated to RHB Research's group CET1 sensitivities (MAYBANK 57bp, CIMB 52bp per +100bp)
using T1 FVOCI and RWA. Banks the brokers flag as shortest-duration (PBB, HLB) get 0.8x the calibrated duration.
CET1 follows BNM's CAF: 55% of cumulative FVOCI gains are deducted, so losses that only erode an existing positive
reserve cost CET1 at 45%; losses beyond the reserve hit in full. Unknown reserves are treated as zero (conservative).
"""
import numpy as np, pandas as pd
from common import CORE, OUT, RAW, cons

TAX, D_TPL = 0.24, 1.5
C = cons()
T = pd.read_csv("data/clean/scr_treasury_core6.csv").set_index("bank")
num = ["fvoci_debt_rm_bn", "fvtpl_rm_bn", "fvtpl_debt_govt_rm_bn", "ac_debt_rm_bn", "rwa_rm_bn", "fvoci_reserve_rm_bn", "cet1_sens_100bp_bp_t2", "q2_pat_rm_bn"]
T[num] = T[num].apply(pd.to_numeric, errors="coerce")

m = pd.read_csv(f"{RAW}/mgs_daily_bnm.csv", parse_dates=["date"]).set_index("date").sort_index()[["3Y", "5Y", "7Y", "10Y"]]
at = lambda d: m.loc[:d].iloc[-1]
y0, y_q3, y_now = at("2026-06-30"), at("2026-09-30"), at("2026-10-13")
peak_day = m.loc["2026-07-01":"2026-09-30", "10Y"].idxmax()
y_peak = at(peak_day)
dy = {"q3": (y_q3 - y0).mean() / 100, "peak": (y_peak - y0).mean() / 100, "now": (y_now - y0).mean() / 100, "stress": 0.01}
dy_short_q3 = (y_q3 - y0)[["3Y", "5Y"]].mean() / 100

calib = {b: T.loc[b, "cet1_sens_100bp_bp_t2"] / 1e4 * T.loc[b, "rwa_rm_bn"] / (T.loc[b, "fvoci_debt_rm_bn"] * (1 - TAX) * 0.01)
         for b in T.index if pd.notna(T.loc[b, "cet1_sens_100bp_bp_t2"])}
D_BASE = float(np.mean(list(calib.values())))
D = {b: calib.get(b, D_BASE * (0.8 if b in ("PBBANK", "HLBANK") else 1.0)) for b in T.index}


def cet1_hit(loss, reserve):
    r = 0.0 if pd.isna(reserve) else max(reserve, 0.0)
    return 0.45 * loss if loss <= r else 0.45 * r + (loss - r)


rows = []
for b in CORE:
    t = T.loc[b]
    sh = C[b]["shares"] / 1e9
    row = dict(bank=b, fvoci=t.fvoci_debt_rm_bn, fvtpl=t.fvtpl_rm_bn, ac=t.ac_debt_rm_bn, rwa=t.rwa_rm_bn, reserve=t.fvoci_reserve_rm_bn,
               fvoci_to_rwa=t.fvoci_debt_rm_bn / t.rwa_rm_bn, duration=D[b], duration_basis="calibrated (RHB Research)" if b in calib else
               ("0.8x calibrated (shortest, T2)" if b in ("PBBANK", "HLBANK") else "calibrated sector mean"))
    for k, v in dy.items():
        loss = t.fvoci_debt_rm_bn * D[b] * v * (1 - TAX)  # RM bn after tax; v is a decimal yield change
        row[f"bv_loss_{k}_rm_bn"] = loss
        row[f"bv_loss_{k}_ps"] = loss / sh
        row[f"cet1_hit_{k}_bp"] = cet1_hit(loss, t.fvoci_reserve_rm_bn) / t.rwa_rm_bn * 1e4
    eq = C[b]["bvps_yf"] * sh
    row["bv_loss_stress_pct_equity"] = row["bv_loss_stress_rm_bn"] / eq
    govt = t.fvtpl_debt_govt_rm_bn if pd.notna(t.fvtpl_debt_govt_rm_bn) else 0.7 * t.fvtpl_rm_bn
    tpl_loss = govt * D_TPL * dy_short_q3  # pre-tax, unhedged upper bound
    row.update(fvtpl_q3_loss_rm_bn=tpl_loss, fvtpl_q3_pct_q2_pbt=tpl_loss / (t.q2_pat_rm_bn / (1 - TAX)),
               fvtpl_q3_pct_fy_np=tpl_loss * (1 - TAX) / (C[b]["eps_fy0"] * sh))
    rows.append(row)
R = pd.DataFrame(rows).set_index("bank")
meta = pd.Series({"D_base": D_BASE, **{f"D_calib_{k}": v for k, v in calib.items()}, "peak_day": str(peak_day.date()),
                  **{f"dy_{k}_bp": v * 1e4 for k, v in dy.items()}, "dy_short_q3_bp": dy_short_q3 * 1e4})
R.to_csv(f"{OUT}/m2b_treasury.csv")
meta.to_csv(f"{OUT}/m2b_treasury_meta.csv")
pd.set_option("display.width", 250, "display.max_columns", 40)
print(meta.to_string())
print(R[["fvoci", "fvtpl", "ac", "rwa", "reserve", "fvoci_to_rwa", "duration", "bv_loss_q3_ps", "bv_loss_now_ps", "cet1_hit_q3_bp", "cet1_hit_peak_bp",
         "cet1_hit_now_bp", "cet1_hit_stress_bp", "bv_loss_stress_pct_equity", "fvtpl_q3_pct_q2_pbt", "fvtpl_q3_pct_fy_np"]].round(3).to_string())
