"""Render the screen's markdown tables from module outputs into output/screen/tables.md (one ## block per table key)."""
import ast
import numpy as np, pandas as pd
from common import CORE, ASOF, MGS10, OUT, kpi, cons

F = pd.read_csv(f"{OUT}/m14_fundamentals_all9.csv", index_col=0, parse_dates=["qdate", "announced"])
Q = pd.read_csv(f"{OUT}/m24_core6.csv", index_col=0)
T = pd.read_csv(f"{OUT}/m5_technicals.csv", index_col=0)
S = pd.read_csv(f"{OUT}/m6_composite.csv", index_col=0)
R = pd.read_csv(f"{OUT}/m3_regression_hlb.csv", index_col=0).iloc[:, 0]
K, C = kpi(), cons()
CODE = {"MAYBANK": "1155", "PBBANK": "1295", "CIMB": "1023", "HLBANK": "5819", "RHBBANK": "1066", "AMBANK": "1015"}
order = S.sort_values("composite", ascending=False).index.tolist()
lab = {b: (b + " †" if b == "HLBANK" else b) for b in F.index}


def p(x, d=1):
    return "n/a" if pd.isna(x) else f"{x*100:+.{d}f}%"


def pu(x, d=1):
    return "n/a" if pd.isna(x) else f"{x*100:.{d}f}%"


def n(x, d=2):
    return "n/a" if pd.isna(x) else f"{x:.{d}f}"


def kv(b, c, suf=""):
    v = K.loc[b, c]
    return "UNVERIFIED" if (pd.isna(v) or str(v).strip() == "" or str(v) == "UNVERIFIED") else f"{v}{suf}"


def md(rows, cols):
    out = "| " + " | ".join(cols) + " |\n|" + "|".join("---" for _ in cols) + "|\n"
    return out + "\n".join("| " + " | ".join(str(x) for x in r) + " |" for r in rows) + "\n"


blocks = {}
blocks["M1_FRESHNESS"] = md([[lab[b], CODE[b], K.loc[b, "period"], pd.Timestamp(K.loc[b, "qtr_end"]).strftime("%d/%m/%Y"),
                              pd.Timestamp(K.loc[b, "announced"]).strftime("%d/%m/%Y"), (ASOF - pd.Timestamp(K.loc[b, "announced"])).days,
                              K.loc[b, "next_results_est"], n(F.loc[b, "price"]), n(F.loc[b, "mcap_rm_bn"], 1),
                              f"{n(F.loc[b,'hi52'])} / {n(F.loc[b,'lo52'])}", n(F.loc[b, "adv3m_rm_m"], 1),
                              "Actionable" if F.loc[b, "adv3m_rm_m"] >= 5 else "ILLIQUID"] for b in CORE],
                            ["Bank", "Code", "Latest Q", "Q end", "Announced", "Days to 13/10", "Next results", "Close 13/10 (RM)",
                             "Mkt cap (RM bn)", "52W H / L", "3M ADV (RM m)", "Liquidity"])
blocks["M1_EVENTS"] = md([[lab[b], K.loc[b, "events"]] for b in CORE], ["Bank", "Corporate events / distortions (Module 1.4)"])

blocks["M2_VALUATION"] = md([[lab[b], n(F.loc[b, "pb"]), f"{n(F.loc[b,'pb5_mean'])} ({n(F.loc[b,'pb5_mean']-F.loc[b,'pb5_sd'])}–{n(F.loc[b,'pb5_mean']+F.loc[b,'pb5_sd'])})",
                              f"{F.loc[b,'pb_z5']:+.2f}", n(F.loc[b, "ptbv"]), n(F.loc[b, "pe_t4q"], 1), n(F.loc[b, "pe_ntm"], 1),
                              pu(F.loc[b, "ey_ntm"]), pu(F.loc[b, "dy_t4q"]), pu(F.loc[b, "dy_ntm"])] for b in CORE],
                            ["Bank", "P/B", "P/B 5Y mean (±1SD)", "P/B z (5Y)", "P/TBV", "P/E T4Q core", "P/E NTM", "EY NTM", "DY T4Q", "DY NTM"])
blocks["M2_PROFIT"] = md([[lab[b], pu(F.loc[b, "roe_t4q_core"]), pu(F.loc[b, "roe_core_rank"]) if b == "HLBANK" else "=",
                           pu(F.loc[b, "roe_lq_ann"]), " → ".join(f"{x*100:.1f}" for x in ast.literal_eval(F.loc[b, "roe_q_last4"])),
                           f"{F.loc[b,'roe_trend_4q']*100:+.2f}pp", f"{kv(b,'nim_pct','%')} ({kv(b,'nim_yoy_bps','bp')} y/y)",
                           kv(b, "cir_pct", "%"), kv(b, "loan_growth_yoy_pct", "%"), kv(b, "casa_pct", "%"), p(F.loc[b, "eps_rev_3m"])] for b in CORE],
                         ["Bank", "Core ROE T4Q (headline basis)", "Core ROE ranked", "Latest Q ann.", "Last 4Q ROE path (%)", "4Q slope /qtr",
                          "NIM", "CIR", "Loan growth y/y", "CASA", "FY+1 EPS rev. 3M"])
blocks["M2_RISK"] = md([[lab[b], kv(b, "gil_pct", "%"), "UNVERIFIED", kv(b, "credit_cost_bps", "bp"), f"{kv(b,'llc_pct','%')} ({K.loc[b,'llc_basis'] if pd.notna(K.loc[b,'llc_basis']) else 'n/a'})",
                         kv(b, "cet1_pct", "%"), f"{Q.loc[b,'cet1_for_buffer']:.2f}%" + (" (incl. Etiqa −1.10pp)" if b == "MAYBANK" else ""), kv(b, "tcr_pct", "%"), kv(b, "lcr_pct", "%"),
                         pu(F.loc[b, "payout_t4q"], 0), n(Q.loc[b, "excess_cet1_rm_bn_est"], 1), Q.loc[b, "payout_flag"]] for b in CORE],
                       ["Bank", "GIL", "Stage 2", "Credit cost", "LLC (basis)", "CET1 reported", "CET1 adj. (FVOCI to 13/10)", "TCR", "LCR", "Payout T4Q", "CET1 >13% (RM bn, T1 RWA)", "Payout vs CET1"])
blocks["M2_TARGETS"] = md([[lab[b], K.loc[b, "guidance"], K.loc[b, "guidance_status"], K.loc[b, "opr_sens_bps_per25"], K.loc[b, "tier"]] for b in CORE],
                          ["Bank", "FY guidance (mgmt)", "YTD vs guidance", "NIM per 25bp OPR cut (bp)", "KPI tier"])

blocks["M3_JPB"] = md([[lab[b], f"{F.loc[b,'beta_raw']:.2f} / {F.loc[b,'beta_blume']:.2f}", pu(F.loc[b, "coe"]), pu(F.loc[b, "roe_core_rank"]),
                        n(F.loc[b, "jpb"]), n(F.loc[b, "pb_core"]), n(F.loc[b, "bv_core"]), n(F.loc[b, "fair_value"]), p(F.loc[b, "mispricing"]),
                        p(F.loc[b, "mispricing_beta1"]), p(F.loc[b, "mispricing_lq"]), p(F.loc[b, "mispricing_lq_beta1"]),
                        f"{n(F.loc[b,'fv_g3'])} / {n(F.loc[b,'fv_g5'])}", f"{n(F.loc[b,'fv_coe_up'])} / {n(F.loc[b,'fv_coe_dn'])}",
                        pu(F.loc[b, "implied_coe"]), pu(F.loc[b, "implied_erp"])] for b in CORE],
                      ["Bank", "β raw / Blume", "COE", "Core ROE", "Justified P/B", "Actual P/B (core)", "BVPS (core)", "Fair value", "Mispricing",
                       "… at β=1", "… on latest-Q ROE", "… latest-Q ROE & β=1", "FV g=3% / 5%", "FV COE +50bp / −50bp", "Implied COE", "Implied ERP"])
blocks["M3_REG"] = md([[lab[b], "core" if F.loc[b, "core"] else "context", pu(F.loc[b, "roe_core_rank"]), n(F.loc[b, "pb_core"]), n(F.loc[b, "pb_fit"]),
                        p(F.loc[b, "resid_pct"]), p(F.loc[b, "resid_pct_core6fit"]) if F.loc[b, "core"] else "–",
                        "cheap" if F.loc[b, "resid_pct"] < -0.05 else ("rich" if F.loc[b, "resid_pct"] > 0.05 else "on line")]
                       for b in F.sort_values("resid_pct").index],
                      ["Bank", "Set", "Core ROE", "P/B (core)", "Fitted P/B", "Residual (9-bank fit)", "Residual (core-6 fit)", "Read"])
blocks["M3_DIV_CONS"] = md([[lab[b], pu(F.loc[b, "dy_ntm"]), f"{(F.loc[b,'dy_ntm']-MGS10)*100:+.1f}pp", pu(F.loc[b, "payout_t4q"], 0),
                             n(F.loc[b, "tp_median"]), int(F.loc[b, "n_analysts"]), f"{int(F.loc[b,'recs_buy'])}/{int(F.loc[b,'recs_hold'])}/{int(F.loc[b,'recs_sell'])}",
                             n(F.loc[b, "fair_value"]), p(F.loc[b, "fv_vs_cons"]), "YES" if abs(F.loc[b, "fv_vs_cons"]) > 0.15 else "no"] for b in CORE],
                           ["Bank", "DY NTM", "Spread vs MGS10 3.83%", "Payout", "Cons. TP median", "# analysts", "Buy/Hold/Sell", "Our FV", "FV vs cons.", ">15% gap"])
QS = S[[]].join(Q[["quality_score"]])
blocks["M4_QUALITY"] = md([[lab[b], pu(Q.loc[b, "roe_core_rank"]), f"{Q.loc[b,'roe_trend_4q']*100:+.2f}pp", kv(b, "casa_pct", "%"), kv(b, "cir_pct", "%"),
                            kv(b, "gil_pct", "%"), kv(b, "llc_pct", "%"), f"{Q.loc[b,'cet1_buffer_pp']:+.2f}pp", f"−{Q.loc[b,'rate_risk_cet1_bp_100']:.0f}bp",
                            *[f"{Q.loc[b,c]:.0f}" for c in ["roe_level", "roe_trend", "casa", "cir", "gil", "llc", "cet1_buffer", "rate_risk"]],
                            f"{Q.loc[b,'quality_score_w10']:.1f}", f"**{Q.loc[b,'quality_score']:.1f}**"]
                           for b in Q.sort_values("quality_score", ascending=False).index],
                          ["Bank", "Core ROE", "ROE slope", "CASA", "CIR", "GIL", "LLC", "CET1 adj. vs 13%", "CET1 per +100bp", "ROE (27)", "Trend (9)", "CASA (13.5)", "CIR (9)",
                           "GIL (13.5)", "LLC (9)", "CET1 (9)", "Rate risk (10)", "Quality v1.0 wts", "Quality v1.1"])

blocks["M5_TREND"] = md([[lab[b], n(T.loc[b, "price"]), n(T.loc[b, "sma20"]), n(T.loc[b, "sma50"]), n(T.loc[b, "sma200"]), n(T.loc[b, "w40"]),
                          f"{T.loc[b,'cross']} ({pd.Timestamp(T.loc[b,'last_cross']).strftime('%d/%m/%y')})", f"{T.loc[b,'slope40w_4w']*100:+.1f}%",
                          T.loc[b, "regime"], n(T.loc[b, "rsi_d"], 0), n(T.loc[b, "rsi_w"], 0),
                          f"{'↑' if T.loc[b,'macd_d_above_sig'] else '↓'}{'+' if T.loc[b,'macd_d_hist_rising'] else '−'} / {'↑' if T.loc[b,'macd_w_above_sig'] else '↓'}{'+' if T.loc[b,'macd_w_hist_rising'] else '−'}",
                          f"{T.loc[b,'adx']:.0f} ({'+DI' if T.loc[b,'pdi']>T.loc[b,'ndi'] else '−DI'})"] for b in order],
                        ["Bank", "Close", "20DMA", "50DMA", "200DMA", "40W", "50/200 cross (date)", "40W slope 4w", "Regime", "RSI D", "RSI W",
                         "MACD D / W (vs signal, hist)", "ADX (lead)"])
blocks["M5_RS"] = md([[lab[b], p(T.loc[b, "rs3m_klci"]), p(T.loc[b, "rs6m_klci"]), p(T.loc[b, "rs3m_sector"]), p(T.loc[b, "rs6m_sector"]),
                       f"{T.loc[b,'rs_line_52w_pos']*100:.0f}%", "no" if not (T.loc[b, "rs_line_new_high"] or T.loc[b, "rs_line_new_low"]) else ("new high" if T.loc[b, "rs_line_new_high"] else "new low"),
                       p(T.loc[b, "pct_from_52wh"]), "up" if T.loc[b, "obv_20d_up"] else "down", f"{T.loc[b,'cmf20']:+.2f}"] for b in order],
                     ["Bank", "3M vs KLCI", "6M vs KLCI", "3M vs sector", "6M vs sector", "RS line in 52W range", "RS 52W extreme", "From 52W high", "OBV 20d", "CMF 20d"])
blocks["M5_LEVELS"] = md([[lab[b], f"{n(T.loc[b,'entry_lo'])}–{n(T.loc[b,'entry_hi'])}", f"{n(T.loc[b,'stop'])} ({T.loc[b,'stop_basis']})",
                           n(T.loc[b, "trigger_near"]) if pd.notna(T.loc[b, "trigger_near"]) else "–", n(T.loc[b, "t1"]), n(T.loc[b, "t2"]),
                           p(T.loc[b, "upside_t1"]), p(T.loc[b, "downside"]), n(T.loc[b, "rr"]), n(T.loc[b, "rr_cons"]),
                           n(T.loc[b, "flip_entry"]), f"{n(T.loc[b,'flip_stop'])} / {n(T.loc[b,'flip_t1'])} / {n(T.loc[b,'flip_t2'])}"] for b in order],
                         ["Bank", "Entry zone", "Stop (basis)", "Immediate hurdle", "T1", "T2", "Upside T1", "Downside", "R:R", "R:R to hurdle",
                          "Flip trigger (weekly close >)", "Post-flip stop / T1 / T2"])
blocks["M5_SCORE"] = md([[lab[b], f"{T.loc[b,'trend_pts']:.0f}", f"{T.loc[b,'rs_score']:.0f}", f"{T.loc[b,'mom_score']:.0f}", f"{T.loc[b,'rr_score']:.0f}",
                          f"−{T.loc[b,'penalty']:.0f}", f"**{T.loc[b,'tech_score']:.1f}**", f"{T.loc[b,'tech_score_cons']:.1f}"] for b in order],
                        ["Bank", "Trend (35)", "RS (25)", "Momentum (20)", "R:R (20)", "Penalty", "Tech score", "… conservative T1"])

blocks["M6_COMPOSITE"] = md([[lab[b], f"{S.loc[b,'value']:.0f}", f"{S.loc[b,'quality']:.0f}", f"{S.loc[b,'tech']:.0f}", f"**{S.loc[b,'composite']:.1f}**",
                              int(S.loc[b, "rank_composite"]), int(S.loc[b, "rank_comp_value_tilt"]), int(S.loc[b, "rank_comp_tech_tilt"]), int(S.loc[b, "rank_comp_beta1"]),
                              S.loc[b, "quadrant"], S.loc[b, "quadrant_beta1"], S.loc[b, "quadrant_t1cons"],
                              S.loc[b, "recent_negative_action"] if isinstance(S.loc[b, "recent_negative_action"], str) and S.loc[b, "recent_negative_action"] else "–",
                              f"**{S.loc[b,'lean']}**", " / ".join({"Overweight": "OW", "Neutral": "N", "Underweight": "UW"}[S.loc[b, f"lean_{k}"]] for k in ["value_tilt", "tech_tilt", "beta1", "t1cons"]),
                              f"{S.loc[b,'confidence']} ({int(S.loc[b,'checks_passed'])}/4)"] for b in order],
                            ["Bank", "Value", "Quality", "Tech", "Composite 40/30/30", "Rank", "Rank 60/20/20", "Rank 20/30/50", "Rank (β=1)",
                             "Quadrant", "Quadrant (β=1)", "Quadrant (cons. T1)", "Negative broker action ≤30d", "Lean", "Lean under 60/20/20 · 20/30/50 · β=1 · cons. T1",
                             "Confidence (lean stable)"])
blocks["M6_VALUE"] = md([[lab[b], f"{S.loc[b,'mispricing']:.0f}", f"{S.loc[b,'resid']:.0f}", f"{S.loc[b,'pb_z5']:.0f}", f"{S.loc[b,'dy_ntm']:.0f}",
                          f"**{S.loc[b,'value']:.0f}**", f"{S.loc[b,'value_beta1']:.0f}"] for b in order],
                        ["Bank", "Mispricing (40)", "P/B–ROE resid. (30)", "P/B z 5Y (15)", "DY NTM (15)", "Value score", "… with β=1 COE"])

blocks["M8_SCORECARD"] = md([[lab[b], n(F.loc[b, "price"]), n(F.loc[b, "mcap_rm_bn"], 1), n(F.loc[b, "pb_core"]), n(F.loc[b, "jpb"]), p(F.loc[b, "mispricing"], 0),
                              pu(F.loc[b, "roe_core_rank"]), pu(F.loc[b, "dy_ntm"]), f"{Q.loc[b,'cet1_for_buffer']:.1f}%", f"−{Q.loc[b,'rate_risk_cet1_bp_100']:.0f}bp", kv(b, "gil_pct", "%"), T.loc[b, "regime"],
                              n(T.loc[b, "rsi_d"], 0), p(T.loc[b, "upside_t1"], 1), n(T.loc[b, "stop"]), n(T.loc[b, "rr"], 1),
                              f"{S.loc[b,'value']:.0f} / {S.loc[b,'quality']:.0f} / {S.loc[b,'tech']:.0f} / **{S.loc[b,'composite']:.1f}**",
                              S.loc[b, "quadrant"], f"**{S.loc[b,'lean']}**", S.loc[b, "confidence"]] for b in order],
                            ["Bank", "Price", "Mkt cap RMbn", "P/B (core)", "Fair P/B", "Mispricing", "Core ROE", "FY+1 yld", "CET1 adj.", "CET1 per +100bp", "GIL", "Trend", "RSI",
                             "Upside T1", "Stop", "R:R", "V / Q / T / Composite", "Quadrant", "Lean", "Confidence"])

TR = pd.read_csv(f"{OUT}/m2b_treasury.csv", index_col=0)
TM = pd.read_csv(f"{OUT}/m2b_treasury_meta.csv", index_col=0).iloc[:, 0]
TM = pd.Series({k: (v if k == 'peak_day' else float(v)) for k, v in TM.items()})
blocks["M2B_BOOK"] = md([[lab[b], n(TR.loc[b, "fvoci"], 1), n(TR.loc[b, "ac"], 1), n(TR.loc[b, "fvtpl"], 1), n(TR.loc[b, "rwa"], 1),
                          n(TR.loc[b, "reserve"], 2) if pd.notna(TR.loc[b, "reserve"]) else "UNVERIFIED (0 assumed)", pu(TR.loc[b, "fvoci_to_rwa"]),
                          f"{TR.loc[b,'fvoci'] / (F.loc[b,'bvps_unadj'] * C[b]['shares'] / 1e9):.2f}×", f"{TR.loc[b,'duration']:.1f}y", TR.loc[b, "duration_basis"]]
                         for b in TR.sort_values("fvoci_to_rwa", ascending=False).index],
                        ["Bank", "FVOCI debt (RM bn)", "Amortised cost (RM bn)", "FVTPL (RM bn)", "Group RWA (RM bn)", "FVOCI reserve (RM bn)", "FVOCI / RWA",
                         "FVOCI / equity", "Effective duration", "Duration basis"])
blocks["M2B_IMPACT"] = md([[lab[b], f"−{TR.loc[b,'cet1_hit_q3_bp']:.0f}bp", f"−{TR.loc[b,'cet1_hit_peak_bp']:.0f}bp", f"−{TR.loc[b,'cet1_hit_now_bp']:.0f}bp",
                            f"−{TR.loc[b,'bv_loss_now_ps']:.3f} ({TR.loc[b,'bv_loss_now_ps'] / F.loc[b,'bvps_unadj'] * 100:.1f}%)",
                            f"**−{TR.loc[b,'cet1_hit_stress_bp']:.0f}bp**", f"−{TR.loc[b,'bv_loss_stress_pct_equity'] * 100:.1f}%",
                            f"{TR.loc[b,'fvtpl_q3_pct_q2_pbt'] * 100:.1f}%", f"{TR.loc[b,'fvtpl_q3_pct_fy_np'] * 100:.1f}%"]
                           for b in TR.sort_values("cet1_hit_stress_bp", ascending=False).index],
                          ["Bank", f"CET1: Q3 (+{TM['dy_q3_bp']:.0f}bp)", f"CET1: peak {TM['peak_day']} (+{TM['dy_peak_bp']:.0f}bp)",
                           f"CET1: to 13/10 (+{TM['dy_now_bp']:.0f}bp)", "BV/share marked to 13/10", "CET1: further +100bp", "BV: further +100bp",
                           "3Q26 FVTPL hit, % of 2Q PBT (unhedged max)", "… % of FY26e profit"])
BA = pd.read_csv("data/clean/scr_broker_actions.csv")
blocks["M1_BROKERS"] = md([[r.date, r.bank, r.house, r.action, f"{r._5} → {r.to}" if isinstance(r._5, str) and r._5 not in ("", "n/a") else (r.to if isinstance(r.to, str) else "–"),
                            r.stated_reason, r.factor_mapped, r.tier] for r in BA.itertuples()],
                          ["Date", "Bank", "House", "Action", "Rating / TP", "Stated reason", "Factor in model", "Tier"])
V0S = pd.read_csv(f"{OUT}/v1.0/m6_composite.csv", index_col=0)
V0F = pd.read_csv(f"{OUT}/v1.0/m14_fundamentals_all9.csv", index_col=0)
V0Q = pd.read_csv(f"{OUT}/v1.0/m24_core6.csv", index_col=0)
blocks["M0_RECON"] = md([[lab[b], p(V0F.loc[b, "mispricing"], 0), p(F.loc[b, "mispricing"], 0), f"{V0Q.loc[b,'quality_score']:.0f} → {Q.loc[b,'quality_score']:.0f}",
                          f"{V0S.loc[b,'composite']:.1f} (#{int(V0S.loc[b,'rank_composite'])})", f"{S.loc[b,'composite']:.1f} (#{int(S.loc[b,'rank_composite'])})",
                          f"{V0S.loc[b,'lean']} ({V0S.loc[b,'confidence']})", f"**{S.loc[b,'lean']} ({S.loc[b,'confidence']})**",
                          "TOP PICK" if S.loc[b, "top_pick"] else ("was top pick" if b == V0S.composite.idxmax() else "")] for b in order],
                        ["Bank", "Mispricing v1.0", "v1.1", "Quality v1.0 → v1.1", "Composite v1.0", "Composite v1.1", "Lean v1.0", "Lean v1.1", ""])

with open(f"{OUT}/tables.md", "w") as f:
    for k, v in blocks.items():
        f.write(f"## {k}\n\n{v}\n")
print("tables:", list(blocks))
print("regression:", {k: round(float(v), 3) for k, v in R.items()})
