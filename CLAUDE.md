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
- Leveraged ETFs (SOXL and similar) are off the table as recovery vehicles —
  volatility decay means a 3x fund does not regain its high when the
  underlying index regains its own. This has been demonstrated with live
  numbers and should not be re-proposed.
