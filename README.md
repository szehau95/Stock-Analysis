# Stock-Analysis

## Malaysian Banks Correction — Causal Diagnosis & Entry-Point Verdict (AS_OF 30/09/2026)

- **Report:** [`reports/MY_Banks_Correction_Verdict_30092026.md`](reports/MY_Banks_Correction_Verdict_30092026.md)
- **Reproduce:** `./run_all.sh` (fetches data, rebuilds all modules, re-renders the report)

| Path | Contents |
|---|---|
| `src/` | Data fetch/parsing, point-in-time panel + core-earnings adjustments, Modules 1-7, table rendering |
| `data/raw/` | Yahoo price files, klsescreener HTML (Bursa quarterly filings), BNM fetch logs |
| `data/clean/` | Quarterly fundamentals (raw + split-rebased), daily panels, BNM MGS (monthly 2006-26, daily 2025-26), KPI table, consensus snapshot |
| `output/` | Module outputs (CSV) and rendered tables |

Assumptions (ERP, g bounds, scorecard weights, scenario probabilities, balance-sheet proxies) are declared at the top of each module file.
