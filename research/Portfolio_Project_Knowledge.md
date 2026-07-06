# Investment Portfolio — Project Knowledge
*Snapshot as of 2026-07-06. Upload this file to a new Claude.ai Project as Project Knowledge to carry this context forward without re-explaining it each session.*

## How to use this doc
Paste this whole file into a claude.ai Project's "Project knowledge" (Settings → Knowledge → Add). Optionally also paste the "Standing Rules" section into the Project's custom instructions field. Then any chat in that Project starts with full context: the account state, the discipline rules earned the hard way, and the open decisions. Update this file periodically (ask Claude Code to regenerate it) since live prices/positions will drift.

---

## 1. The one thing that matters most: the RM60K lesson

In late June 2026 this portfolio ran ~1.5x effective leverage through three 2x-daily-reset leveraged ETFs (MUU on Micron, RAM on a memory-sector basket, WDCX on Western Digital) sized at ~95% of NAV with ~$16 in cash, into a memory-sector correction. The account drew down ~33% in days and margin cushion nearly evaporated. The user manually cut all leveraged positions, crystallizing a real loss (quoted as "RM60K" / painful).

**Root cause, precisely diagnosed:** 2x daily-reset ETFs compound leverage *every day*. In a sustained trend this is a tailwind (a full-year backtest showed 100% MUU returning +3,025% vs. MU's own +698% over MU's best 12 months ever). In a choppy/reversing market the same mechanism is a wrecking ball — the fund is forced to buy high and sell low on every rebalance, and volatility decay compounds against the holder even if the underlying is flat. The account was rebuilt levered at a volatility peak, drawing the exact opposite tail from the backtest's favorable path.

**Standing rules that came out of this (do not relitigate these casually):**
1. **No leveraged/daily-reset ETFs held overnight.** Ever. If a leveraged product is used, it's a same-day trading tool, not a holding.
2. **Max ~12% per single name, max ~40% per theme.** (MU was trimmed back to this cap on 2026-07-06.)
3. **Every position gets a written invalidation level (closing-price basis) at entry.** For MU the working level has been the $1,020 / $854–882 shelf structure (see §3).
4. **Maintain a real cash reserve (~9–10% combined), and keep it in the account where it can actually be deployed** — a Moomoo cash pile can't buy an IBKR dip.
5. **Judge performance against contributed capital, not against the peak.** Anchoring to the all-time-high balance is what turns a manageable trim into a ride to the bottom.
6. **Don't chase "highest ROI" as the explicit goal after a loss.** That instinct is how one bad drawdown becomes two.

---

## 2. Current holdings (live as of 2026-07-06, intraday)

### IBKR (net liquidation ≈ $35,600, leverage 0.99x, no margin risk)
| Position | Qty | Mkt Value | Unrl. P/L | Weight |
|---|---|---|---|---|
| MU | 5 | ~$4,995 | +$104 | ~14% (target: trim to ~12% via other means, ASML trim below addresses cash not MU) |
| NVDA | 25 | ~$4,893 | +$48 | ~14% |
| MSFT | 12 | ~$4,628 | −$60 | ~13% |
| ASML | 2 (pending sell 1) | ~$3,694 | +$186 | ~10% → ~5% after trim |
| PLTR | 25 | ~$3,306 | +$37 | ~9% |
| AMAT | 5 | ~$2,992 | +$24 | ~8% |
| META | 5 | ~$2,948 | +$18 | ~8% |
| MRVL | 8 | ~$2,035 | +$97 | ~6% |
| VRT | 6 | ~$1,957 | +$143 | ~5% |
| ARM | 5 | ~$1,635 | +$73 | ~5% |
| IBIT | 52 | ~$1,839 | −$51 | ~5% |
| HK dust ("45757 @VALUE") | 3000 | ~$489 (~$62 net of FX) | −$1,242 | negligible — untradeable stub on IBKR's VALUE pseudo-exchange, cannot be sold via normal order routing; leave alone or contact IBKR support to clear |
| Cash | — | ~$371 | — | ~1% (thin — see open action below) |

**⚠️ Open/pending order:** A **SELL 1 ASML, LIMIT $1,850, DAY** instruction is staged (id #100) but **not yet submitted** by the user in the IBKR app as of this snapshot — still shows 2 shares held. Purpose: raise ~$1,850 of real dry powder in IBKR specifically (Moomoo cash can't be deployed there). Check on resume whether this filled, expired, or needs re-staging at a new price.

### Moomoo (post-trim, ~$5,998 total)
| Position | Qty | Mkt Value | Unrl. P/L |
|---|---|---|---|
| WDC (Western Digital) | 4 | $2,385 | +$238 (+11.1%) |
| MU | 0 (trimmed to zero here 2026-07-06) | — | — |
| Cash | — | $3,614 | — |

### Combined book (~$41,500 total, both accounts)
- Themes: ~60% semiconductors (compute/memory/equipment spread across NVDA/MU/ASML/AMAT/MRVL/ARM), ~26% AI software/platforms (MSFT/PLTR/META), ~5% infra (VRT), ~4% crypto (IBIT), ~10% cash.
- **This is unlevered, diversified, and structurally sound** — a completely different (and much healthier) book than the pre-crisis leveraged-memory concentration.

---

## 3. Micron (MU) — standing thesis, as last analyzed

**Fundamental (12-month direction): BUY.** Q3 FY26 revenue $41.46B (+346% YoY), 84.6% gross margin, $24.4B net cash, HBM sold out through CY2026 with ~$100B in customer agreements, HBM share ~21% (#2 behind SK Hynix ~62%, ahead of Samsung ~17%). 12-month PT ~$1,500 (range $1,250–1,650). Invalidation triggers (none fired as of last check): two consecutive months of falling DRAM/HBM contract prices; sequential gross-margin contraction in guidance; HBM4 qualification delay or NVIDIA allocation falling below ~15%.

**Technical structure (daily):** Key shelf/confluence zone **$1,020–1,029** (EMA21 + 0.382 Fib), tested and defended multiple times late June/early July with a reversal off intraday lows near $1,024–1,046. Deeper structural floor **$854–882** (EMA50 + 0.618 Fib + prior swing low) — this is the level that matters if $1,020 fails on a closing basis. ATH $1,255 (2026-06-25, post-earnings). A DRAM-industry antitrust class action (filed ~2026-06-25, naming Samsung/SK Hynix/Micron) is a live overhang — thesis-relevant if it escalates toward DOJ involvement (attacks the supply-discipline mechanism the bull case depends on), not yet a fundamental trigger.

**Sector context:** SK Hynix and Samsung earnings (~Jul 7-8 prelim, Samsung; late July, SK Hynix) are the next scheduled catalysts — record profits expected on the AI memory supercycle. Watch whether the market *buys* or *sells* those prints as the read on whether the correction is over.

**Political/optics footnote:** Micron announced a $250M "Trump Accounts" contribution (~2026-07-01/02) amid presidential praise — financially immaterial (~0.2% of annualized FCF) but plausibly relevant as goodwill positioning given the pending antitrust matter and CHIPS Act exposure. Categorized as low-materiality unless it converts into an actual contract/stake/regulatory action (an Intel-stake-style precedent exists in this environment).

---

## 4. Backtest findings (1-year, MU-related leverage strategies)

Full interactive tearsheet was built and published as an artifact during this session (log-scale equity curves, risk/return scatter, full scorecard) — not reproduced here in detail, but the key numbers:

| Strategy | 1-yr return | Volatility | Max drawdown | Sharpe |
|---|---|---|---|---|
| 100% MU (unlevered) | +697.7% | 75.8% | −30.3% | **3.09 (best risk-adjusted)** |
| 80% MUU / 5% puts / 15% cash | +1,266.9% | 112.2% | −38.3% | 2.87 |
| 100% MUU (2x, unhedged) | **+3,024.6% (best return)** | 150.8% | **−52.9% (worst)** | 3.02 |
| 90% MUU / 10% puts | +1,128.3% | 117.1% | −38.7% | 2.70 |
| SOXX / QQQ / SPY (benchmarks) | +133% / +28% / +19% | 41 / 18 / 13% | −16 / −12 / −9% | 2.16 / 1.21 / 1.11 |

**Key conclusions:**
- Put overlays (Black-Scholes modeled, not real historical option quotes — flagged explicitly) reduce drawdown but are **Sharpe-negative** in this data; they're behavioral insurance (making a drawdown holdable), not a return enhancer.
- There is **no MUU/cash/put mix that matches MU's own Sharpe/drawdown profile while beating its return** — MU and MUU sit on roughly the same risk/return line; blending them (e.g., 70/30 or 60/40 MU/MUU) moves you along that line for ~1.7–2.3x the return at MU's own Sharpe, but drawdown necessarily deepens (~-38% to -40%) — you cannot have MU's drawdown AND MUU's return.
- The entire backtest window is MU's best-ever 12 months (near-straight-line 8x). This is a **favorable-path artifact, not a forecast** — forward returns will very likely be lower and drawdowns at least as deep. Explicitly flagged in the tearsheet as survivorship/path bias.
- **Practical takeaway carried forward:** if more MU-linked leverage is ever considered again, a MU-core + MUU-satellite blend (~60-70/30-40) with a pre-committed rebalance rule (trim the satellite after big run-ups, hold the core through chop) is the version that's actually survivable — not a standing 100% MUU position sized off a backtest.

---

## 5. Open items to check on resuming this thread
1. Did the staged ASML sell (1 share, limit $1,850) fill, expire unsubmitted, or get cancelled?
2. Where does MU sit relative to $1,020 (near-term) and $854–882 (structural)? Has it closed below either on a daily basis?
3. What happened at Samsung's July 7-8 preliminary earnings and SK Hynix's late-July report — bought or sold?
4. Any escalation in the DRAM antitrust suit (DOJ involvement would be thesis-relevant)?
5. Has the HK dust stub been cleared (contact IBKR) or is it still sitting there?
6. Reconfirm current cash levels in both accounts — the ~9-10% combined cash target should be checked periodically, not just once.

---

## 6. Tooling note (context for whoever continues this)
This analysis was produced in Claude Code with live Interactive Brokers MCP tool access (real account positions, order staging, live/historical price data via IBKR) plus web search for news/earnings context. A plain Claude.ai chat/Project **cannot** pull live brokerage data or place orders — it can only reason over whatever is pasted in or uploaded as Project Knowledge/files. For anything requiring a live portfolio check, fresh price data, or order execution, that still needs to happen in an environment with brokerage tool access (this Claude Code environment, or equivalent). This document is a point-in-time snapshot, not a live feed — treat prices/positions here as stale the moment new information arrives.
