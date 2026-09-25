"""
12_book.py — Module 8: personal book exposure to the MU print (IBKR positions pulled 25/09/2026).
  * print-day beta of each holding to MU's 1-day reaction (last 16 prints, close t0 -> close t+1)
  * MU-event-beta-weighted exposure, cash vs 6-8% floor, concentration
  * book P&L distribution on print day = sum(value_i * beta_i * MU_move) using the Module-5 MC draws,
    before and after the proposed pre-earnings trim (MU 6 -> 4 shares)
Writes data/book_exposure.csv and data/book_pnl.csv
"""
import pathlib
import numpy as np
import pandas as pd
import yfinance as yf
from mc_core import simulate

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
pos = pd.read_csv(ROOT / "data" / "ibkr_positions_20260925.csv")
acct = pd.read_json(ROOT / "data" / "ibkr_account_20260925.json", typ="series")
NLV, CASH = float(acct["net_liquidation"]), float(acct["total_cash_value"])
ev = pd.read_csv(REPO / "hist_moves.csv", parse_dates=["report_date"]).tail(16)

tick = ["MU", "AMAT", "SOXX", "JEPQ", "QCOM", "AVGO", "LRCX", "VRT", "BE"]
px = yf.download(tick, start="2022-01-01", auto_adjust=True, progress=False)["Close"]
px.to_csv(ROOT / "data" / "book_prices.csv")
rows = []
for t in tick:
    r = []
    for d in ev.report_date:
        s = px[t].dropna()
        p = s.index.get_indexer([d])[0]
        m = px["MU"].dropna()
        q = m.index.get_indexer([d])[0]
        if p >= 0 and p + 1 < len(s) and q >= 0:
            r.append((m.iloc[q + 1] / m.iloc[q] - 1, s.iloc[p + 1] / s.iloc[p] - 1))
    r = np.array(r)
    beta = 1.0 if t == "MU" else np.polyfit(r[:, 0], r[:, 1], 1)[0]
    corr = 1.0 if t == "MU" else np.corrcoef(r[:, 0], r[:, 1])[0, 1]
    rows.append(dict(symbol=t, n_prints=len(r), beta_to_MU_print=beta, corr=corr))
betas = pd.DataFrame(rows).set_index("symbol")

bk = pos.set_index("symbol")[["quantity", "market_price", "market_value_usd"]].copy()
bk = bk.join(betas, how="left")
bk.loc["45757.HK", ["beta_to_MU_print", "corr"]] = 0.0
bk["weight_pct_nlv"] = 100 * bk.market_value_usd / NLV
bk["mu_beta_exposure_usd"] = bk.market_value_usd * bk.beta_to_MU_print
bk["semis_ai_hw"] = bk.index.isin(["MU", "AMAT", "SOXX", "QCOM", "AVGO", "LRCX"])
bk["ai_infra_power"] = bk.index.isin(["VRT", "BE"])
bk.round(4).to_csv(ROOT / "data" / "book_exposure.csv")

# ---- print-day P&L distribution ----
df, _ = simulate(N=100_000)
mv = df.move.to_numpy() / 100
def pnl(book):
    return np.outer(mv, (book.market_value_usd * book.beta_to_MU_print).to_numpy()).sum(axis=1)
base = pnl(bk)
trim = bk.copy()
trim.loc["MU", "market_value_usd"] = 4 * 1094.45
trim.loc["MU", "quantity"] = 4
p_trim = pnl(trim)
cash_after = CASH + 2 * 1094.45
out = pd.Series({
    "NLV": NLV, "cash": CASH, "cash_pct_nlv": 100 * CASH / NLV, "cash_floor_pct": "6-8",
    "semis_ai_hw_pct_nlv": bk.loc[bk.semis_ai_hw, "weight_pct_nlv"].sum(),
    "semis_plus_ai_infra_pct_nlv": bk.loc[bk.semis_ai_hw | bk.ai_infra_power, "weight_pct_nlv"].sum(),
    "largest_position": bk.weight_pct_nlv.idxmax(), "largest_weight_pct": bk.weight_pct_nlv.max(),
    "mu_direct_pct_nlv": bk.loc["MU", "weight_pct_nlv"],
    "mu_beta_exposure_usd": bk.mu_beta_exposure_usd.sum(),
    "mu_beta_exposure_pct_nlv": 100 * bk.mu_beta_exposure_usd.sum() / NLV,
    "book_pnl_per_1pct_MU_usd": bk.mu_beta_exposure_usd.sum() / 100,
    "E_book_pnl_usd": base.mean(), "E_book_pnl_pct_nlv": 100 * base.mean() / NLV,
    "p05_book_pnl_usd": np.percentile(base, 5), "p05_book_pnl_pct_nlv": 100 * np.percentile(base, 5) / NLV,
    "p95_book_pnl_usd": np.percentile(base, 95),
    "after_trim_mu_pct_nlv": 100 * 4 * 1094.45 / NLV,
    "after_trim_cash_usd": cash_after, "after_trim_cash_pct_nlv": 100 * cash_after / NLV,
    "after_trim_mu_beta_exposure_usd": (trim.market_value_usd * trim.beta_to_MU_print).sum(),
    "after_trim_E_book_pnl_usd": p_trim.mean(), "after_trim_p05_book_pnl_usd": np.percentile(p_trim, 5),
    "after_trim_p95_book_pnl_usd": np.percentile(p_trim, 95),
})
out.to_csv(ROOT / "data" / "book_pnl.csv", header=["value"])
pd.set_option("display.width", 200)
print(bk[["quantity", "market_value_usd", "weight_pct_nlv", "beta_to_MU_print", "corr", "mu_beta_exposure_usd"]].round(2).to_string())
print(); print(out.to_string())
