# ACEL monthly-roll optimiser

Screens counters for worst-of ACEL/FCN structures (12M, monthly observation, memory KO,
European KI) and ranks them by the chance of knocking out at observation #1, following the
ACEL Monthly-Roll master prompt. The current run screens the US lines in the Lombard Odier
research list of 17.09.2026 for a 01/10/2026 fixing. The write-up is in
[`output/report.md`](output/report.md).

## Run

```bash
pip install -r acel/requirements.txt
cd acel
python3 iv12m.py            # 12M ATM vols from data/iv12m_quotes.csv -> data/iv12m.csv
python3 engine.py --td 2026-10-01   # ~3 min on 4 cores; writes output/*.csv
python3 report.py           # output/report.md
```

`engine.py --help` lists the options (fixing date, path counts, MU month-1 vol, workers).

## Inputs (`data/`)

| File | Contents | Source |
|---|---|---|
| `snapshots_raw.jsonl` | last, change, 13W/26W/52W high-low, 30D ATM IV, HV30, IV percentiles | IBKR `get_price_snapshot`, 25/09/2026 pre-market |
| `closes/*.txt`, `dates_1y.txt` | 1Y daily closes to 24/09/2026 | IBKR `get_price_history` |
| `iv12m_quotes.csv` | Sep-2027 ATM call/put bid-ask at the 24/09 close | IBKR option chains |
| `universe.json` | Bloomberg ticker, LO rating/PT/upside, dividend yield, next print | LO list, company releases, data vendors |
| `ledger.json` | May–Sep 2026 trade ledger; the 24/09 USD fill is the coupon calibration point | master prompt |

To refresh, re-pull those five inputs and re-run the three scripts.

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
- Coupons: the note is priced at par less an all-in take calibrated to the 24/09 USD fill
  (MU + SNDK + SKHY 95/70/70 at 16.20%). "Roll pricing" is that take less 2.5 pts of UF. Coupons
  are indicative, for ranking and desk requests only.

## Outputs (`output/`)

| File | Contents |
|---|---|
| `report.md` | ranked table, top-3 verdicts, fee/vol economics, desk lines, pre-filled releases |
| `ranking_top.csv` | best structure per finalist basket (200k paths) |
| `finalists_all_structures.csv` | every grid structure for the finalist baskets |
| `grid_all_structures.csv.gz` | full screen (50k paths) |
| `single_name_screen.csv`, `name_scorecard.csv` | per-counter metrics and verdicts |
| `calibration.json` | all-in take and cross-checks against the September fills |
| `benchmarks.csv` | recent house structures re-run for the same fixing |
| `strike_levers_top5.csv`, `tradeoff_top1.csv`, `frontier.csv` | coupon trade-offs |
