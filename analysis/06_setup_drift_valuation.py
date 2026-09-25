"""
06_setup_drift_valuation.py  — Module 3c / 3d / Rule 5 (14-week normalisation)
  * Current pre-print drift (as of 24/09 close = t0-4, and live 25/09) vs the historical distribution of the
    same-horizon drift (close t0-24 -> t0-4) for every print since FQ4-17; relative to SOXX.
  * Recovery context: drawdown from 2026 high, rebound from July low.
  * Valuation: P/E on FY27 consensus; history of P/E on *realised* next-4Q EPS around prior memory peaks
    (memory trades at trough P/E on peak EPS); reverse-engineered EPS the price requires at peak multiples.
  * Per-week normalisation of FQ3 -> FQ4 -> FQ1 FY27 (13w -> 14w -> 13w).
"""
import re, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
C = pd.read_csv(ROOT / "data" / "prices_close.csv", index_col=0, parse_dates=True)
ed = pd.read_csv(ROOT / "data" / "earnings_dates.csv", parse_dates=["filing_date"])
ga = pd.read_csv(ROOT / "data" / "guide_vs_actual.csv", parse_dates=["report_date"])
mu, sx = C["MU"].dropna(), C["SOXX"].dropna()
out = {}

# ---------------- pre-print drift ----------------
d_asof = pd.Timestamp("2026-09-24")
p = mu.index.get_indexer([d_asof])[0]
out["mu_close_2409"] = mu.iloc[p]
out["drift20_asof_2409_pct"] = 100 * (mu.iloc[p] / mu.iloc[p - 20] - 1)
out["drift10_asof_2409_pct"] = 100 * (mu.iloc[p] / mu.iloc[p - 10] - 1)
out["drift5_asof_2409_pct"] = 100 * (mu.iloc[p] / mu.iloc[p - 5] - 1)
ps = sx.index.get_indexer([d_asof])[0]
out["soxx_drift20_asof_2409_pct"] = 100 * (sx.iloc[ps] / sx.iloc[ps - 20] - 1)
out["rel_drift20_vs_soxx_pp"] = out["drift20_asof_2409_pct"] - out["soxx_drift20_asof_2409_pct"]
live = 1094.45
out["drift20_live_2509_pct"] = 100 * (live / mu.iloc[p - 19] - 1)
hist = []
for d in ed.filing_date:
    q = mu.index.get_indexer([d])[0]
    qs = sx.index.get_indexer([d])[0]
    if q < 24 or qs < 24:
        continue
    hist.append(dict(report_date=d.date(), drift20_t4=mu.iloc[q - 4] / mu.iloc[q - 24] - 1,
                     rel20_t4=(mu.iloc[q - 4] / mu.iloc[q - 24]) - (sx.iloc[qs - 4] / sx.iloc[qs - 24]),
                     drift20_t0=mu.iloc[q] / mu.iloc[q - 20] - 1, r1=mu.iloc[q + 1] / mu.iloc[q] - 1 if q + 1 < len(mu) else np.nan))
h = pd.DataFrame(hist)
cur = out["drift20_asof_2409_pct"] / 100
out["drift20_pctile_vs_all_prints"] = 100 * (h.drift20_t4 < cur).mean()
out["drift20_pctile_vs_last16"] = 100 * (h.tail(16).drift20_t4 < cur).mean()
out["rel20_pctile_vs_all_prints"] = 100 * (h.rel20_t4 < out["rel_drift20_vs_soxx_pp"] / 100).mean()
# conditional reaction: prints where t-4 drift20 > 10% vs <= 10%
hi = h[h.drift20_t4 > 0.10]
lo = h[h.drift20_t4 <= 0.10]
out["n_prints_drift20_gt10"] = len(hi)
out["mean_r1_when_drift20_gt10_pct"] = 100 * hi.r1.mean()
out["pct_up_when_drift20_gt10"] = 100 * (hi.r1 > 0).mean()
out["mean_r1_when_drift20_le10_pct"] = 100 * lo.r1.mean()
out["pct_up_when_drift20_le10"] = 100 * (lo.r1 > 0).mean()

# ---------------- recovery context ----------------
y = mu.loc["2026-01-01":]
hi_d = y.idxmax()
lo_d = y.loc[hi_d:].idxmin()
out["mu_2026_high"] = y.max(); out["mu_2026_high_date"] = str(hi_d.date())
out["mu_july_low"] = y.loc[hi_d:].min(); out["mu_july_low_date"] = str(lo_d.date())
out["mu_pct_below_high"] = 100 * (mu.iloc[p] / y.max() - 1)
out["mu_pct_above_low"] = 100 * (mu.iloc[p] / y.loc[hi_d:].min() - 1)

# ---------------- valuation ----------------
# older non-GAAP EPS (2017-2019) from press-release headline bullets (Tier 1 text)
eps_old = {}
for f in sorted((ROOT / "data" / "pr").glob("201*.txt")):
    t = f.read_text().replace("\n", " ")
    m = re.search(r"Non-GAAP net income of \$[\d.]+ (?:billion|million)\s*,?\s*or \$([\d.]+) per diluted share", t)
    if m:
        eps_old[pd.Timestamp(f.stem)] = float(m.group(1))
eps = pd.concat([pd.Series(eps_old), ga.set_index("report_date").eps_act.dropna()]).sort_index()
eps = eps[~eps.index.duplicated()]
# realised next-4Q EPS known at each report date (perfect foresight) -> P/E at report close
rows = []
dates = list(eps.index)
for i, d in enumerate(dates):
    if i + 4 >= len(dates):
        break
    ntm = eps.iloc[i + 1: i + 5].sum()
    q = mu.index.get_indexer([d])[0]
    rows.append(dict(date=d.date(), px=mu.iloc[q], ntm_eps_realised=ntm, pe_ntm_realised=mu.iloc[q] / ntm if ntm > 0 else np.nan,
                     ttm_eps=eps.iloc[max(0, i - 3): i + 1].sum()))
pe = pd.DataFrame(rows)
pe.to_csv(ROOT / "data" / "pe_history.csv", index=False)
out["fy27_consensus_eps"] = 156.53          # 24/7 Wall St 23/09/2026 citing consensus (Tier 3, cross-checked vs BofA/Wells ranges)
out["pe_fy27_cons_at_2409"] = mu.iloc[p] / 156.53
out["pe_fy27_wells_166"] = mu.iloc[p] / 166.0
out["pe_normalized_gs_62"] = mu.iloc[p] / 62.0
# peak-cycle multiples: P/E on realised NTM EPS at the quarter where NTM EPS peaked in each cycle
pe_valid = pe.dropna()
for lab, a, b in [("2018_cycle", "2017-06-01", "2019-06-30"), ("2021_22_cycle", "2020-06-01", "2022-12-31")]:
    seg = pe_valid[(pd.to_datetime(pe_valid.date) >= a) & (pd.to_datetime(pe_valid.date) <= b)]
    if len(seg):
        k = seg.ntm_eps_realised.idxmax()
        out[f"peak_{lab}_date"] = str(seg.loc[k, "date"])
        out[f"peak_{lab}_pe_on_peak_ntm_eps"] = seg.loc[k, "pe_ntm_realised"]
        out[f"peak_{lab}_min_pe_in_cycle"] = seg.pe_ntm_realised.min()
for m in [4, 5, 6, 8, 10, 12]:
    out[f"eps_required_at_{m}x"] = mu.iloc[p] / m

# ---------------- 14-week normalisation ----------------
fq3, fq4g, fq1c = 41.456, 50.0, 56.7
out["fq3_per_week_bn"] = fq3 / 13
out["fq4_guide_per_week_bn"] = fq4g / 14
out["fq4_guide_qoq_headline_pct"] = 100 * (fq4g / fq3 - 1)
out["fq4_guide_qoq_per_week_pct"] = 100 * ((fq4g / 14) / (fq3 / 13) - 1)
out["extra_week_contribution_pp"] = 100 * (14 / 13 - 1)
for fq4 in [50.5, 52.0, 53.0]:
    out[f"fq1_cons56.7_vs_fq4_{fq4}_headline_pct"] = 100 * (fq1c / fq4 - 1)
    out[f"fq1_cons56.7_vs_fq4_{fq4}_per_week_pct"] = 100 * ((fq1c / 13) / (fq4 / 14) - 1)
    out[f"fq1_flat_per_week_rev_if_fq4_{fq4}"] = fq4 / 14 * 13

s = pd.Series(out)
s.to_csv(ROOT / "data" / "setup_summary.csv", header=["value"])
pd.set_option("display.width", 200)
print(s.to_string())
print("\nP/E on realised next-4Q EPS at each print:\n", pe.round(2).to_string())
