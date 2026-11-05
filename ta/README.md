# ta/: Technical Analysis v2 engine (screenshot-free)

`ta_engine.py` is a Claude Code rebuild of the project doc `claude/ta-engine.py`, which Claude Code
cannot reach. It follows the TA v2 master prompt (M1–M9, plus the M10 log row and `score_call`).
Every level, plan, R/R and size in a brief comes from this file's output, not from a chart image.

## Run

```bash
cd ta
python3 ta_engine.py data/1810.json --warmup data/1810_warmup.json --asof 2026-11-04 \
  --nlv <NLV_USD> --risk 0.5 --max-name 6 --fx <USDMYR> --ccy HKD --usd-local <USDHKD> --lot 200 \
  --bench data/HSTECH.json data/HSI.json data/QQQ.json \
  --earnings 2026-11-24 --earnings-status CONFIRMED --implied-move 10.5 --implied-exp 2026-11-27 \
  --json /tmp/out.json
```

`--asof` drops a forming bar, so signals run on completed closes only. `python3 ta_engine.py --help`
lists the book overlay (`--book`), FCN/ELN knock-in check (`--acel-*`) and live-print options.
Account and client inputs are runtime arguments only. They are never written into this folder.

## Data (`data/`)

TradingView `get-ohlcv` dumps (1D, `format=columns`) with the response's summary block. The engine
asserts count, high, low, last close, first open, first/last timestamp, total volume and OHLC
consistency, and stops on any mismatch (re-pull rather than trade on a copy error).

| File | Contents |
|---|---|
| `1810.json` | HKEX:1810, 05/03/2025–05/11/2026 (last bar forming at pull time) |
| `1810_warmup.json` | closes 01/06/2023–04/03/2025, used only to converge EMA200 (unwarmed EMA200 reads +0.41 too high on 04/11/2026) |
| `1810_weekly_check.json` | TradingView 1W bars; cross-check of the daily file (86 complete weeks match exactly) |
| `HSTECH.json`, `HSI.json`, `QQQ.json` | benchmarks for 20D/60D relative strength (indices carry no volume) |

## Indicator conventions (TradingView defaults)

EMA 9/21/20/50/200, SMA 200, Bollinger 20/2 (population stdev), RSI 14 (Wilder `ta.rma`) + SMA 9,
ATR 14 (`ta.rma` of true range), OBV + EMA 13, 20D volume SMA, anchored VWAP on hlc3.
RSI and ATR were cross-checked against an independent EWM formula (identical at 04/11/2026).

## Where the rebuild had to pick an interpretation

- **Tactical Fib:** last swing ≥ 3× ATR on a zigzag whose reversals are ≥ 3× ATR, so a minor
  pullback inside a leg does not restart it.
- **Targets:** a zone must have n ≥ 2 (round numbers 0.5), or be the cycle high/low or 52W high/low.
- **Breakout ladder:** T1 is the next uncleared zone. A trigger that lands inside that zone scores R/R 0.
- **Divergence:** OBV is checked for regular divergence only. A hidden RSI divergence is marked VOID
  once price closes beyond its first pivot.
- **Live setups:** require an AT-PRICE zone (within 0.5× ATR of the close) with n ≥ 3.

Numbers can differ in detail from the original project-doc engine. Treat a first run on a new
ticker as a rebuild check.
