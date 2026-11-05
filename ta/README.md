# ta/: Technical Analysis engine (screenshot-free)

`ta_engine.py` is a Claude Code rebuild of the project doc `claude/ta-engine.py`, which Claude Code
cannot reach. It follows the TA master prompt (v2 and the chart-only v2.1: M1–M9, plus the M10
log row and `score_call`). Every level, plan and R/R in a brief comes from this file's output,
not from a chart image.

## Run

Chart-only (v2.1). No account inputs; every plan prints risk per share instead of a size:

```bash
cd ta
python3 ta_engine.py data/MU.json --asof 2026-11-04 \
  --bench data/QQQ.json data/SPX.json data/SOX.json \
  --earnings 2026-12-16 --earnings-status ESTIMATED --json /tmp/out.json
```

`--asof` drops a forming bar, so signals run on completed closes only. `--warmup` adds older closes
so EMA200 converges on a short window (used for 1810). `python3 ta_engine.py --help` also lists the
v2 options: sizing (`--nlv`, `--risk`, `--max-name`), book overlay (`--book`) and the FCN/ELN
knock-in check (`--acel-*`). Those are runtime arguments only and are never written into this folder.

## Data (`data/`)

TradingView `get-ohlcv` dumps (1D, `format=columns`) with the response's summary block. The engine
asserts count, high, low, last close, first open, first/last timestamp, total volume and OHLC
consistency, and stops on any mismatch (re-pull rather than trade on a copy error).

| File | Contents |
|---|---|
| `MU.json` | NASDAQ:MU, 05/03/2025–04/11/2026 |
| `1810.json` | HKEX:1810, 05/03/2025–05/11/2026 (last bar forming at pull time) |
| `1810_warmup.json` | closes 01/06/2023–04/03/2025, used only to converge EMA200 (unwarmed EMA200 reads +0.41 too high on 04/11/2026) |
| `1810_weekly_check.json` | TradingView 1W bars; cross-check of the daily file (86 complete weeks match exactly) |
| `QQQ.json`, `SPX.json`, `SOX.json` | US benchmarks for 20D/60D relative strength |
| `HSTECH.json`, `HSI.json` | Hong Kong benchmarks |

## Indicator conventions (TradingView defaults)

EMA 9/21/20/50/200, SMA 200, Bollinger 20/2 (population stdev), RSI 14 (Wilder `ta.rma`) + SMA 9,
ATR 14 (`ta.rma` of true range), OBV + EMA 13, 20D volume SMA, anchored VWAP on hlc3.

## Calibration against the validation log

The master prompt's log records the project-doc engine on MU, 17/07/2026: RSI 44.36, RSI SMA9 46.47,
ATR 85.56, SMA200 483.30, EMA9 937.21, EMA21 971.26, EMA50 899.97, BB 816.57 / 1,025.52 / 1,234.47.
The completed 17/07 bar closed at 848.95. Every moving-average gap implies the same intraday
print, 891.02 (the bar's range was 804.00–903.96). With that print this engine matches all ten
values within 0.005. Its 17/07 fade plan also reproduces the log's: zone 950.00–991.10, T1 818.67
(log 816.57), T2 750 (log 750).

## Where the rebuild had to pick an interpretation

- **Tactical Fib:** last swing ≥ 3× ATR on a zigzag whose reversals are ≥ 3× ATR, so a minor
  pullback inside a leg does not restart it.
- **Targets:** T1 must be a zone with n ≥ 2 (round numbers 0.5), or the cycle high/low or 52W
  high/low. T2 is the next zone of any strength beyond T1. For support longs, fades and live
  setups, targets start beyond the AT-PRICE band: the trade has to travel back through the
  current congestion. This is what reproduces the 17/07 fade.
- **Breakout ladder:** T1 is the next uncleared zone above the trigger. A trigger that lands inside
  that zone scores R/R 0.
- **Divergence:** OBV is checked for regular divergence only. A hidden RSI divergence is marked VOID
  once price closes beyond its first pivot. A pending RSI divergence under 2 points is reported as
  PENDING-MARGINAL.
- **Live setups:** require an AT-PRICE zone (within 0.5× ATR of the close) with n ≥ 3.
- **v2.1 holder note:** TRIM on a confirmed bearish RSI + OBV divergence, or on a close below EMA50
  and the cycle-high AVWAP on ≥ 1.5× volume. Otherwise HOLD while closes stay above the first
  support zone. Pullback and bounce longs are capped at M confidence.

Numbers can still differ in detail from the original engine. Treat a first run on a new ticker as
a rebuild check.
