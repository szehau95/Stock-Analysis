#!/usr/bin/env bash
# Reproduce the full analysis (network needed for fetch steps). AS_OF = 30/09/2026.
set -euo pipefail
cd "$(dirname "$0")"
pip install -q pandas numpy scipy statsmodels yfinance lxml beautifulsoup4 requests tabulate
python3 src/fetch_prices.py            # Yahoo OHLCV/dividends/splits (T3)
python3 src/fetch_mgs.py               # BNM FMIP month-end MGS yields (T1)
python3 src/fetch_mgs_daily.py         # BNM FMIP daily MGS yields 2025-26 (T1)
python3 src/fetch_fin.py               # Yahoo FY financials + consensus (T3)
python3 src/parse_ks.py                # Bursa quarterly filings via klsescreener (requires data/raw/ks_*.html)
python3 src/build_panel.py             # point-in-time panel + core-earnings adjustments
python3 src/m1_price_forensics.py      # Module 1
python3 src/m2_attribution.py          # Module 2 quant support
python3 src/m34_fund_valuation.py      # Modules 3-4
python3 src/m5_analogs.py              # Module 5
python3 src/m6_scenarios.py            # Module 6
python3 src/m7_levels.py               # Module 7 support
python3 src/make_tables.py && python3 src/assemble_report.py
