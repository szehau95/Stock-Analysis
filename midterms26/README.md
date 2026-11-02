# midterms26 — Post-midterm playbook (2026) working dir
Run order (from this folder):
1. `python3 src/fetch_yahoo.py data/raw/yahoo "^GSPC|SPX" ...`   long daily histories -> CSV (see out/PRE report coverage map)
2. `python3 src/fetch_odds.py`            Kalshi + Polymarket live contracts + daily history
3. `python3 src/m2_base_rate.py SPX`      M2 event study, controls, robustness   -> out/m2_*
4. `python3 src/m2_extra.py`              NDX/RUT/SOX, buckets, cycle overlay, drawdowns, realised event moves
5. `python3 src/m7_options.py`            CBOE delayed chains -> event / weekly / 3M implied moves
6. `python3 src/m0_m7_odds.py`            M0 baseline + odds-beta
7. `python3 src/m9_books.py`              Senate seat MC (S5), personal book, client FCN Monte Carlo
8. `python3 src/m3_colleague_and_tables.py`  colleague-claim test, Table 1 probs, Table 8 aggregation
Report: out/PRE_02-11-2026.md
Live inputs pulled via MCP (not scripts): IBKR account (saved to data/raw/ibkr_live_*.json), ACEL Live Book (data/raw/acel/), TradingView quotes/calendars.
