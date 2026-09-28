# ACEL monthly-roll optimiser

Screens counters for worst-of ACEL/FCN structures (12M, monthly observation, memory KO,
European KI) and ranks them by the chance of knocking out at observation #1, following the
ACEL Monthly-Roll master prompt. The current run screens the US lines in the Lombard Odier
research list of 17.09.2026 for a 02/10/2026 fixing, with coupons calibrated to the desk's
28/09/2026 quotes. The write-up is in
[`output/report.md`](output/report.md).

## Run

```bash
pip install -r acel/requirements.txt
cd acel
python3 iv12m.py            # 12M ATM vols from data/iv12m_quotes.csv -> data/iv12m.csv
python3 engine.py --td 2026-10-02   # ~6 min on 4 cores; writes output/*.csv
python3 report.py           # output/report.md
```

`engine.py --help` lists the options (fixing date, path counts, MU month-1 vol, pricing-correlation
floor, workers).

## Inputs (`data/`)

| File | Contents | Source |
|---|---|---|
| `snapshots_raw.jsonl` | last, change, 13W/26W/52W high-low, 30D ATM IV, HV30, IV percentiles | IBKR `get_price_snapshot`, 25/09/2026 pre-market |
| `closes/*.txt`, `dates_1y.txt` | 1Y daily closes to 24/09/2026 | IBKR `get_price_history` |
| `iv12m_quotes.csv` | Sep-2027 ATM call/put bid-ask at the 24/09 close | IBKR option chains |
| `universe.json` | Bloomberg ticker, LO rating/PT/upside, dividend yield, next print | LO list, company releases, data vendors |
| `ledger.json` | May–Sep 2026 trade ledger; September fills are cross-checks | master prompt |
| `desk_quotes.json` | desk quotes of 28/09/2026 (TD 02/10, KO 95, UF 4%): the coupon calibration set | desk chat |

To refresh, re-pull those inputs (and add the latest desk quotes) and re-run the three scripts.

## Model

- Correlated GBM on monthly steps, risk-neutral drift (r = 3.5%), correlations from 1Y daily log returns.
- Vol: 30D ATM IV for month 1 (drives P(KO @ obs #1)), forward vol implied by the ~12M ATM IV for
  months 2–12, and a +5 vol-pt skew bump that phases in between 100% and the KI level.
- Both KO modes (memory per stock, simultaneous). They agree at obs #1.
- Hard filters: no print between fixing and obs #1, P(KO@1) ≥ 55%, P(loss) ≤ 12%, KI ≤ 90% of
  the 13-week low. Grid limited to the prompt's rules of thumb (KO ≤ 100 − 0.5·σ₁ₘ, KI ≤ e^(−0.75σ)).
- Roll Score = 0.45·P(KO@1) + 0.25·P(KO≤3) + 0.20·(1 − P(loss)/0.12) + 0.10·min(CPN/IV ÷ 0.30, 1),
  less 0.03 per penalty (strong-day fix, avg ρ < 0.5 on 3 names, IV percentile > 90, overlap with a
  live basket).
- Coupons: the note is priced at par less an all-in take (issuer spread + UF). Pricing paths use
  historical correlations floored at 0.6, since the desk marks worst-of correlation well above
  realized on low-correlation tech baskets; probabilities stay on historical correlations. The
  floor and the spread (~3.1% ex-UF) are fitted to the desk's 28/09 quotes (±1.1 pts). Coupons are
  shown at UF 1% (ranking) and UF 4% (the desk's basis), indicative only.
- Ranking: when nothing passes every hard filter at ≥9% (the case on 28/09), structures reaching 9%
  at UF 1% with the earnings and 13-week-low rules intact are ranked, with the missed filter shown.

## Outputs (`output/`)

| File | Contents |
|---|---|
| `report.md` | ranked table, top-3 verdicts, fee/vol economics, desk lines, pre-filled releases |
| `ranking_top.csv` | best structure per finalist basket (200k paths) |
| `finalists_all_structures.csv` | every grid structure for the finalist baskets |
| `grid_all_structures.csv.gz` | full screen (50k paths) |
| `single_name_screen.csv`, `name_scorecard.csv` | per-counter metrics and verdicts |
| `calibration.json` | fitted spread and correlation floor, quote-by-quote fit, September fills' implied UF |
| `strict_pass_top.csv` | best coupon per basket among structures passing every hard filter |
| `benchmarks.csv` | recent house structures re-run for the same fixing |
| `strike_levers_top5.csv`, `tradeoff_top1.csv`, `frontier.csv` | coupon trade-offs |
