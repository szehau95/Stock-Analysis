#!/usr/bin/env bash
# Rebuild the 14/10/2026 Value x TA screen. Fetchers hit live endpoints; skip them to reproduce from the saved snapshot.
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${FETCH:-0}" == "1" ]]; then
  python3 fetch_px.py && python3 fetch_cons.py && python3 fetch_bs.py && python3 fetch_mgs.py
fi
python3 m14_fundamentals.py
python3 m5_technicals.py
python3 m6_composite.py
python3 make_tables.py
python3 assemble.py
