"""
04_event_study.py  — Module 2a / 3b / 3c / 6 analog inputs
Post-earnings reactions for every MU print since FQ4-17 (dates = SEC 8-K filing dates, all after close).
  r1   : close(t0) -> close(t+1)          1-day reaction
  gap  : close(t0) -> open(t+1)           overnight gap
  r5   : close(t0) -> close(t+5)
  d2_20: close(t+1) -> close(t+20)        post-print drift
  pre10/pre20 : close(t-10|t-20) -> close(t0)   pre-print run-up, and relative to SOXX
  pre20_at_t4 : close(t-24)->close(t-4)   run-up measured 4 sessions before print (apples-to-apples with today)
  hynix_r1   : SK Hynix KRX session after the print vs prior KRX close
Writes hist_moves.csv (repo root) and analysis/data/event_study_summary.csv
"""
import pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
C = pd.read_csv(ROOT / "data" / "prices_close.csv", index_col=0, parse_dates=True)
O = pd.read_csv(ROOT / "data" / "prices_open.csv", index_col=0, parse_dates=True)
ed = pd.read_csv(ROOT / "data" / "earnings_dates.csv", parse_dates=["filing_date"])
ga = pd.read_csv(ROOT / "data" / "guide_vs_actual.csv", parse_dates=["report_date"])

us = C[["MU", "SOXX", "SMH", "NVDA", "LRCX", "AMAT", "KLAC", "WDC", "STX", "SNDK", "^GSPC"]].dropna(subset=["MU"])
uo = O[["MU"]].reindex(us.index)
kr = C[["000660.KS", "005930.KS"]].dropna(subset=["000660.KS"])
dates = us.index


def pos(d):
    return dates.get_indexer([d])[0]


rows = []
for d in ed.filing_date:
    p = pos(d)
    if p < 0 or p + 1 >= len(dates):
        continue
    def ret(t, a, b):
        if a < 0 or b >= len(dates):
            return np.nan
        return us[t].iloc[b] / us[t].iloc[a] - 1
    row = dict(report_date=d.date(), t1_date=dates[p + 1].date())
    row["mu_close_t0"] = us.MU.iloc[p]
    row["r1"] = ret("MU", p, p + 1)
    row["gap"] = uo.MU.iloc[p + 1] / us.MU.iloc[p] - 1
    row["r5"] = ret("MU", p, p + 5)
    row["d2_20"] = ret("MU", p + 1, p + 20)
    row["pre10"] = ret("MU", p - 10, p)
    row["pre20"] = ret("MU", p - 20, p)
    row["pre20_at_t4"] = ret("MU", p - 24, p - 4)
    row["soxx_r1"] = ret("SOXX", p, p + 1)
    row["soxx_pre20"] = ret("SOXX", p - 20, p)
    row["rel_r1_vs_soxx"] = row["r1"] - row["soxx_r1"]
    row["rel_pre20_vs_soxx"] = row["pre20"] - row["soxx_pre20"]
    for t in ["NVDA", "LRCX", "AMAT", "KLAC", "WDC", "STX", "SNDK"]:
        row[f"{t.lower()}_r1"] = ret(t, p, p + 1)
    # Korea: first KRX session strictly after US report date vs last KRX close on/before it
    kb = kr.loc[:d]
    ka = kr.loc[d + pd.Timedelta(days=1):]
    if len(kb) and len(ka):
        row["hynix_r1"] = ka["000660.KS"].iloc[0] / kb["000660.KS"].iloc[-1] - 1
        row["samsung_r1"] = ka["005930.KS"].iloc[0] / kb["005930.KS"].iloc[-1] - 1
    rows.append(row)

ev = pd.DataFrame(rows)
ev["report_date"] = pd.to_datetime(ev.report_date)
ev = ev.merge(ga[["report_date", "rev_act_m", "gm_act", "eps_act", "prev_rev_guide_mid_m", "rev_vs_guide_mid_pct",
                  "eps_vs_guide_mid_pct", "gm_vs_guide_bp", "rev_guide_mid_m", "gm_guide_mid", "eps_guide_mid",
                  "next_guide_qoq_pct"]], on="report_date", how="left")
# cycle phase: upcycle if next-quarter GM guide > current GM actual, else downcycle (2020+ where parsed)
ev["phase"] = np.where(ev.gm_guide_mid > ev.gm_act, "up", np.where(ev.gm_guide_mid.notna(), "down", "n/a"))
# manual phase for 2017-19 (guidance filed as image): memory upcycle to FQ3-18, downcycle FQ4-18..FQ1-20
manual = {"2017-09-26": "up", "2017-12-19": "up", "2018-03-22": "up", "2018-06-20": "up",
          "2018-09-20": "down", "2018-12-18": "down", "2019-03-20": "down", "2019-06-25": "down",
          "2019-09-26": "down", "2019-12-18": "down"}
for k, v in manual.items():
    ev.loc[ev.report_date == pd.Timestamp(k), "phase"] = v
ev["beat_rev_guide"] = ev.rev_vs_guide_mid_pct > 0
ev["abs_r1"] = ev.r1.abs()
ev.to_csv(REPO / "hist_moves.csv", index=False, float_format="%.5f")

LB = 16
last = ev.tail(LB)
summ = {
    "n_quarters": len(last),
    "mean_abs_r1": last.abs_r1.mean(), "median_abs_r1": last.abs_r1.median(),
    "mean_r1": last.r1.mean(), "pct_up_r1": (last.r1 > 0).mean(),
    "mean_abs_r5": last.r5.abs().mean(), "mean_r5": last.r5.mean(),
    "mean_abs_gap": last.gap.abs().mean(),
    "beat_rate_rev_vs_guide_mid": last.beat_rev_guide.mean(),
    "mean_rev_beat_pct": last.rev_vs_guide_mid_pct.mean(),
    "median_rev_beat_pct": last.rev_vs_guide_mid_pct.median(),
    "pct_beat_but_down": ((last.beat_rev_guide) & (last.r1 < 0)).mean(),
    "p_down_given_beat": ((last.beat_rev_guide) & (last.r1 < 0)).sum() / last.beat_rev_guide.sum(),
    "mean_hynix_r1": last.hynix_r1.mean(), "corr_mu_hynix_r1": last[["r1", "hynix_r1"]].corr().iloc[0, 1],
    "mean_abs_r1_all_since2017": ev.abs_r1.mean(),
    "mean_abs_r1_last8": ev.tail(8).abs_r1.mean(),
}
pd.Series(summ).to_csv(ROOT / "data" / "event_study_summary.csv", header=["value"])
pd.set_option("display.width", 250)
cols = ["report_date", "phase", "rev_vs_guide_mid_pct", "next_guide_qoq_pct", "pre20", "rel_pre20_vs_soxx", "gap",
        "r1", "r5", "d2_20", "rel_r1_vs_soxx", "hynix_r1", "lrcx_r1", "amat_r1"]
print((ev[cols].set_index("report_date") * 1).round(3).to_string())
print()
print(pd.Series(summ).round(4).to_string())
by = ev.groupby("phase").agg(n=("r1", "size"), mean_r1=("r1", "mean"), mean_abs_r1=("abs_r1", "mean"),
                             pct_up=("r1", lambda s: (s > 0).mean()), mean_d2_20=("d2_20", "mean"))
print(); print(by.round(4).to_string())
