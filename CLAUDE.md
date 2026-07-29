# Analysis Context — Standing Instructions

> NOTE: This repository is PUBLIC. Do not commit account values, position
> sizes, net worth figures, broker identifiers, or personal tax status to
> this file. Portfolio specifics stay in the session, not in git.

## Dead Positions — Exclude From All Analysis Forever

### 45757 — CHINA EVERGRANDE GROUP (HKD)

- **STATUS: PERMANENTLY UNRECOVERABLE.** Delisted / suspended; quoted price
  is stale and will not recover.
- **User instruction (Jul 2026): "forget abt it forever".**
- Treat its value as ZERO in all recovery math, allocation percentages,
  portfolio ceilings, and reallocation proposals.
- Do not surface it again as an actionable position.

## Analytical Framework In Use

- Master Prompt: Fundamental (Part A) + Technical (Part B) + Synthesis (Part C).
- Technical work follows the `goldman-technical-strategist` framework:
  one decisive verdict word (BUY / SELL / TRIM / WAIT). Risk/reward must beat
  1.5:1 to Target 1, or the verdict is WAIT. No hedging.
- **Never invent indicator values.** EMA / RSI / OBV / ATR / Fibonacci levels
  must be read off a supplied chart screenshot. If no chart is provided, say a
  chart is required rather than estimating.
- Sourcing: primary sources only (SEC filings, company IR, Reuters, Bloomberg,
  CNBC, WSJ, FT). State "data unavailable" rather than estimating a missing
  metric. Flag conflicting sources against the primary filing rather than
  averaging them away. Always state the as-of date of key figures.
- Reallocation proposals MUST run through the `portfolio-reallocation-discipline`
  skill. Fundamentals first; needing capital for a new entry is never a valid
  reason to exit or aggressively trim a quality position.

## Standing Preferences

- Deliver analysis in copy-pasteable code-block format.
- Long-term holder; comfortable holding through drawdowns.
## Leveraged ETFs (SOXL / TQQQ) — Refined Position

Two distinct cases. Do not collapse them.

- **As a RECOVERY vehicle (buy and hold through a drawdown): NO.**
  Daily-reset decay means a 3x fund does not regain its own high when the
  underlying index regains its high. Demonstrated with live numbers; do not
  re-propose.
- **As a TACTICAL entry AFTER a confirmed reversal: permitted.** In a smooth
  sustained uptrend, daily compounding delivers ABOVE the stated multiple
  (2023: SOXX ~+65%, SOXL +227%). Entry regime is the whole edge.

Entry discipline when this is on the table:
- Signal is the **200-day SMA of the UNDERLYING** (SOXX for SOXL, QQQ for
  TQQQ), not of the leveraged fund. Compute it from actual daily bars —
  never estimate it.
- Preferred trigger: underlying washes to/through its 200-day, then closes
  back above it for 3+ consecutive sessions.
- Hard exit: underlying closes below its 200-day. That is a regime flip to
  cash, not a dip to buy.
- Size as a defined satellite sleeve (10-15% ceiling), never a core position.
  A 3x fund large enough to hit a return target is also large enough to
  restart the account.
