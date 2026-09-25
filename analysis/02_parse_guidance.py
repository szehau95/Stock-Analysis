"""
02_parse_guidance.py
Parse each Tier-1 press release (analysis/data/pr/*.txt) for:
  actual revenue ($M), non-GAAP GM %, non-GAAP diluted EPS  (the quarter just reported)
  next-quarter non-GAAP guidance: revenue mid & half-range, GM mid, EPS mid & half-range
Writes analysis/data/guide_vs_actual.csv  (one row per fiscal quarter, guide from prior release)
"""
import re, pathlib
import numpy as np
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
PR = ROOT / "data" / "pr"
ed = pd.read_csv(ROOT / "data" / "earnings_dates.csv")


def num(s):
    return float(s.replace(",", ""))


def money_to_m(val, unit):
    v = num(val)
    return v * 1000 if unit.lower().startswith("b") else v


def parse(t: str) -> dict:
    out = {}
    flat = t.replace("\n", " / ")
    # ---------- actuals ----------
    m = re.search(r"Quarterly Financial Results.*?Revenue\s*\|\s*\$\s*\|\s*([\d,]+)", flat)
    if m:
        out["rev_act_m"] = num(m.group(1))
    # non-GAAP EPS from reconciliation (negative values are parenthesised)
    m = re.search(r"Non-GAAP diluted earnings (?:\(loss\) )?per share\s*/?\s*\|\s*\$\s*\|\s*(\()?([\d.]+)", flat)
    if m:
        out["eps_act"] = num(m.group(2)) * (-1 if m.group(1) else 1)
    # non-GAAP gross margin %: reconciliation "Non-GAAP gross margin | $ | X" / revenue
    m = re.search(r"Non-GAAP gross margin\s*/?\s*\|\s*\$\s*\|\s*(\()?([\d,]+)", flat)
    if m and "rev_act_m" in out:
        out["gm_act"] = round(100 * num(m.group(2)) * (-1 if m.group(1) else 1) / out["rev_act_m"], 2)
    # ---------- guidance ----------
    bo = flat.find("Business Outlook")
    g = flat[bo: bo + 2500] if bo >= 0 else ""
    # revenue: "$50.0 billion ± $1.0 billion" / "$7.60 billion ± $200 million" / "$4.6 billion - $5.2 billion"
    rrow = re.search(r"Revenue\s*/?\s*\|(.*?)(?:Gross margin)", g)
    if rrow:
        vals = re.findall(r"\$\s*([\d.,]+)\s*(billion|million)\s*±\s*\$\s*([\d.,]+)\s*(billion|million)", rrow.group(1))
        rng = re.findall(r"\$\s*([\d.,]+)\s*(billion|million)\s*[-–]\s*\$\s*([\d.,]+)\s*(billion|million)", rrow.group(1))
        if vals:
            v = vals[-1]
            out["rev_guide_mid_m"] = money_to_m(v[0], v[1])
            out["rev_guide_hr_m"] = money_to_m(v[2], v[3])
        elif rng:
            v = rng[-1]
            lo, hi = money_to_m(v[0], v[1]), money_to_m(v[2], v[3])
            out["rev_guide_mid_m"], out["rev_guide_hr_m"] = (lo + hi) / 2, (hi - lo) / 2
    grow = re.search(r"Gross margin\s*/?\s*\|(.*?)(?:Operating expenses)", g)
    if grow:
        vals = re.findall(r"(\()?([\d.]+)\s*%\)?\s*(?:±\s*([\d.]+)\s*%)?", grow.group(1))
        vals = [v for v in vals if v[1]]
        # keep only midpoints (entries followed by ± or 'Approximately X%'); last one is the non-GAAP column
        mids = [v for v in vals if v[2]] or vals
        if mids:
            v = mids[-1]
            out["gm_guide_mid"] = num(v[1]) * (-1 if v[0] else 1)
            out["gm_guide_hr"] = num(v[2]) if v[2] else np.nan
    erow = re.search(r"Diluted earnings (?:\(loss\) )?per share\s*/?\s*\|(.*?)(?:Further)", g)
    if erow:
        vals = re.findall(r"(\()?\$\s*([\d.]+)\)?\s*±\s*\$\s*([\d.]+)", erow.group(1))
        if vals:
            v = vals[-1]
            out["eps_guide_mid"] = num(v[1]) * (-1 if v[0] else 1)
            out["eps_guide_hr"] = num(v[2])
    return out


rows = []
for _, r in ed.iterrows():
    f = PR / r.pr_file
    t = f.read_text() if f.exists() else ""
    if not t:
        continue
    d = parse(t)
    d["report_date"] = r.filing_date
    rows.append(d)

df = pd.DataFrame(rows).sort_values("report_date").reset_index(drop=True)
# guide issued at report t applies to quarter reported at t+1
for c in ["rev_guide_mid_m", "rev_guide_hr_m", "gm_guide_mid", "gm_guide_hr", "eps_guide_mid", "eps_guide_hr"]:
    df["prev_" + c] = df[c].shift(1)
df["rev_vs_guide_mid_pct"] = 100 * (df.rev_act_m / df.prev_rev_guide_mid_m - 1)
df["rev_vs_guide_top"] = df.rev_act_m > (df.prev_rev_guide_mid_m + df.prev_rev_guide_hr_m)
df["eps_vs_guide_mid_pct"] = 100 * (df.eps_act / df.prev_eps_guide_mid - 1)
df["gm_vs_guide_bp"] = 100 * (df.gm_act - df.prev_gm_guide_mid)
df["next_guide_qoq_pct"] = 100 * (df.rev_guide_mid_m / df.rev_act_m - 1)
df.to_csv(ROOT / "data" / "guide_vs_actual.csv", index=False)
pd.set_option("display.width", 250)
print(df[["report_date", "rev_act_m", "gm_act", "eps_act", "prev_rev_guide_mid_m", "prev_eps_guide_mid",
          "rev_vs_guide_mid_pct", "eps_vs_guide_mid_pct", "gm_vs_guide_bp", "rev_guide_mid_m", "rev_guide_hr_m",
          "gm_guide_mid", "eps_guide_mid", "next_guide_qoq_pct"]].round(2).to_string())
