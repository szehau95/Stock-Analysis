---
name: decisive-call-discipline
description: >
  Enforces expected-value discipline and regime-change detection before issuing any
  decisive directional call (BUY / SELL / HOLD / WAIT / AVOID) on a single name, or
  before ranking trade structures (shares vs. options vs. leveraged ETF).
  ALWAYS use this skill whenever: (1) a verdict word — buy, sell, hold, wait, avoid,
  enter, exit, "should I", "worth it", "odds of winning" — is being produced for a
  ticker, (2) a technical brief is about to override or veto a fundamental read,
  (3) a dated catalyst (earnings, guidance, FDA, court date, index rebalance) falls
  inside the proposed holding window, (4) implied volatility, IV rank/percentile, or
  option structure is being used as an argument, (5) a stock is being ranked against
  its 2x/3x leveraged ETF. This skill prevents catalyst-blind WAIT calls and
  stale-chart-level anchoring — a known failure mode logged after the SMCI error of
  August 2026.
---

# Decisive Call Discipline

## Purpose

This skill exists because of a documented error.

On **4 August 2026**, a full fundamental + technical brief on SMCI at $29.63 concluded
**WAIT**. The brief correctly identified the decisive variable, correctly named the bull
case ("above 13% gross margin and $38–45 is reachable"), and then buried it. Eight days
later SMCI printed **$38.15** after guiding FY27 revenue to **$65–72B against $54.4B
consensus**. The missed move was **+27%**.

The forecast was not the failure. **The process was.** The brief contained a +30% branch
and never priced it. Running the expected-value arithmetic on its *own* stated
probabilities returned **+5.5% EV** — WAIT failed its own test and nobody checked.

> **This must never happen again.**

---

## The Core Rule

> **A verdict is not a view — it is an expected-value calculation. If the analysis
> contains a branch worth more than ±25%, that branch must be priced, sized, and shown
> in the verdict. No decisive call ships without the EV arithmetic written out.**

A conditional buried in prose is not analysis. If it moves the stock a quarter, it is
the trade.

---

## Symmetry Clause — read this before anything else

This skill was written after a **missed upside**. It must not become an upside bias.
Every gate below is direction-neutral and fires identically on negative regime changes:
a guide cut of >50%, a pre-announcement below the prior range, a covenant breach, a
withdrawn outlook. A skill that only ever argues for getting long has replaced one
failure mode with a worse one. **If applying these gates produces a bullish conclusion
on four consecutive names, stop and audit for bias.**

---

## The Six Gates

Every decisive call must pass all six. Show the work for each.

### Gate 1 — Regime-Change Test (invalidates chart levels)

Chart structure is a record of the *old* information set. When the information set
changes materially, fib retracements, moving averages, and prior swing highs drawn from
the pre-change range are **historical artifacts, not resistance**.

Mark the technical structure **STALE** if any one of these fires:

| Trigger | Threshold |
|---|---|
| Guidance revised on a key metric | > 50% change (e.g. GM 8.3% → 16% = +93%) |
| Pre-announcement lands outside prior guided range | any breach |
| Backlog / new orders disclosed | > 1.5× TTM revenue |
| Capital raise | > 25% of market cap |
| Issued guide vs. consensus | > 20% above or below |
| Auditor / restatement / delisting status change | any |

**When STALE fires:**
- Targets must be rebuilt from fundamentals (forward EPS × defensible multiple), not
  from the prior price range.
- Moving averages and fib levels may be cited as *observations* but may **not** be used
  as Target 1 in a risk/reward calculation.
- The R/R gate (below) is computed against the fundamental target only.

**Rule: technicals govern entry timing *within* a regime. They never veto a confirmed
regime change.**

### Gate 2 — Two Probability Numbers, Never One

Risk-neutral probability (`N(d2)` from implied vol) embeds **zero drift by construction**
and is mechanically dragged below 50% by high IV. It describes option pricing. It is
**not a forecast** and must never be presented as one.

Required format — both numbers, always:

```
Market-implied (risk-neutral, zero drift): 43%  ← what options are priced at
My estimate (drift assumption: <stated>):  58%  ← the forecast
Gap and why it exists:                     <the edge, or "none — no edge here">
```

If the second number cannot be defended independently of the first, **the first may not
be quoted at all.** "The stock is volatile" is not permitted to masquerade as "the stock
will go down."

### Gate 3 — Mandatory EV Arithmetic (the gate that would have caught SMCI)

If any scenario in the analysis moves the stock **>25%**, the verdict must contain this
table, filled in, before the verdict word:

| Scenario | Probability | Return | Contribution |
|---|---|---|---|
| Bull | __% | +__% | +__% |
| Base | __% | +__% | +__% |
| Bear | __% | −__% | −__% |
| **Expected value** | **100%** | | **±__%** |

Decision rule:

- **EV > +3%** with a dated catalyst inside the window → this is a **position**, not a
  WAIT. Size it per Gate 4.
- **EV between −3% and +3%** → genuinely no edge. WAIT is legitimate; say "no edge"
  explicitly rather than dressing it as caution.
- **EV < −3%** → avoid or short-side structure.

**A WAIT verdict on positive EV is only permissible with a written, specific reason**
(position limit reached, capital committed elsewhere, unquantifiable binary such as a
pending criminal indictment against the entity). "Poor risk/reward to Target 1" is not
such a reason when Target 1 came from a STALE chart.

### Gate 4 — Sizing Schedule, Not Binary Verdict, When a Catalyst Is In-Window

If a dated catalyst falls inside the proposed holding period, the output is a **schedule**,
not BUY/WAIT:

| Tranche | Size | Trigger |
|---|---|---|
| Starter | __% of intended | now |
| Add 1 | __% | catalyst resolves in thesis direction |
| Add 2 | __% | confirmation level reclaimed |
| Abort | — | thesis-invalidating outcome, defined in advance |

Starter size scales with EV and inversely with the implied move. The correct SMCI output
on 4 Aug was *"starter now, add after the guide"* — not WAIT. A binary verdict on a
probabilistic setup discards the available information.

**Also required:** if the catalyst can gap the stock, state plainly that **a stop does not
function through the event**, and size as though the stop does not exist. This part the
SMCI brief got right — keep it.

### Gate 5 — Corporate Actions Are Read as a Set, Not Scored Separately

Financing, backlog disclosure, insider activity, and guidance revisions occurring within
the same quarter are usually **one signal** about what management can see. Scoring them
independently and netting to neutral is the error.

SMCI, June–July 2026, scored separately in the failed brief:

| Read separately (wrong) | Read as a set (correct) |
|---|---|
| $7B raise → dilution, negative | Management is financing a step-change in scale |
| $60B new orders → unconverted, neutral | …that they can already see in the order book… |
| GM 8.3% → 15–17% → possibly one-off | …and that is already showing up in margin |

**The check:** *"If one person knew all of these facts at once, what would they conclude?"*
Ask it before assigning a score to any of them.

Corollary — **a pre-announcement de-risks the quarter, not the guide.** A company does not
pre-announce a doubling of gross margin unless the quarter is dramatically off-consensus.
Never treat a pre-announcement as "the surprise is spent" when the forward guide is still
unreleased and the backlog is large.

### Gate 6 — Match the Instrument Critique to the Actual Holding Period

Volatility-decay math on leveraged ETFs, IV-crush math on long options, and theta
arguments are all **holding-period dependent**. State the horizon before making the
argument, and compute the drag over *that* horizon.

| Horizon | Leveraged ETF drag | Verdict weight |
|---|---|---|
| 1–10 sessions | Small — compute it, don't assume | Decay is a minor factor |
| 2–8 weeks | Material at σ > 60% | Decay is a primary factor |
| > 3 months at σ > 80% | Dominant — (L²−L)/2 × σ² annualized | Disqualifying |

**Logged error:** the SMCI brief ranked a 2x ETF last using multi-week decay math, then
applied it to a six-day catalyst hold. Compounding actual daily closes, the 2x returned
**+36.4%** vs. the stock's +18.7% over that window — drag cost only ~4.5 points. The
general argument was sound; the horizon was mismatched. **Always compute the drag over the
stated horizon rather than citing YTD figures from a different one.**

---

## Anti-Patterns to Prevent

### The SMCI Stale-Level Veto (August 2026)
**What happened:** WAIT issued on R/R of 0.70:1, where Target 1 ($31.60) was a Bollinger
band and Target 2 ($33.00) a 200-day SMA — both drawn from a price range that formed
*before* the pre-announcement that doubled the margin outlook.
**Why it's wrong:** those levels described a company that no longer existed. A $65–72B
revenue guide does not respect a $32.65 SMA.
**The check:** *"Was this level formed before or after the information that changed the
thesis?"* If before, and Gate 1 fired, the level may not anchor the R/R.

### The Buried Branch
**Pattern:** the bull or bear case appears once, in a subordinate clause, then plays no
role in the verdict.
**The check:** grep your own draft for the largest stated move. If it exceeds 25% and does
not appear in the EV table, the brief is incomplete.

### Rigor Theater
**Pattern:** quoting `N(d2)`, IV percentiles, and Greeks with precision, in service of a
conclusion that the math does not actually support. Precision on the inputs is not the
same as validity of the conclusion.
**The check:** for each computed number, state in one line what decision it changes. If it
changes none, cut it.

### Volatility-as-Bearishness
**Pattern:** high IV → low `N(d2)` → "43% odds" → sounds bearish. This is an artifact of
the lognormal distribution, not a directional signal.
**The check:** would this same number appear if the stock were about to double? (Yes.)
Then it is not evidence about direction.

### Horizon-Mismatched Instrument Critique
**Pattern:** long-horizon decay math used to disqualify a short-horizon structure, or vice
versa. See Gate 6.

---

## Required Output Format for Any Decisive Call

Every decisive call must contain, in this order:

1. **Regime status** — STALE or INTACT, with the Gate 1 trigger named if STALE
2. **The decisive variable** — the single number or event that resolves the thesis, and
   the date it is known
3. **Two probability numbers** — market-implied and own estimate, per Gate 2
4. **The EV table** — filled in, per Gate 3, whenever a branch exceeds ±25%
5. **The verdict** — with sizing schedule per Gate 4 if a catalyst is in-window
6. **Invalidation** — the specific observable that makes this call wrong, and by when
7. **Horizon statement** — before any instrument or volatility argument, per Gate 6

---

## Pre-Send Checklist

Run before any verdict word ships:

- [ ] Did any Gate 1 trigger fire? If yes, are targets rebuilt from fundamentals?
- [ ] Is Target 1 in the R/R calculation drawn from a pre-regime-change price range?
- [ ] Is there a stated scenario worth more than ±25%? Is it in the EV table?
- [ ] Does the EV arithmetic actually support the verdict word I am about to write?
- [ ] Am I quoting a risk-neutral probability as if it were a forecast?
- [ ] Is there a dated catalyst inside the holding window? If yes, is the output a
      sizing schedule rather than BUY/WAIT?
- [ ] Have I scored corporate actions separately that should be read as one signal?
- [ ] Have I stated the holding horizon before making any decay/IV/theta argument?
- [ ] If the verdict is WAIT on positive EV, is the specific blocking reason written down?
- [ ] Symmetry check: would these gates produce the mirror-image conclusion on the same
      facts inverted?

---

## Context

- Owner: Emmanuel. IBKR account, USD base. Institutional-PM lens.
- Companion skill: `portfolio-reallocation-discipline` — governs *sizing and capital
  sourcing* once a call is made. This skill governs *the call itself*. Where both apply,
  this skill runs first.
- Sourcing standard unchanged: primary sources (SEC filings, company IR, broker market
  data) over secondary. Label estimates as estimates. Write "data unavailable" rather
  than inferring a number.
- Error log:
  - **April 2026 — MSFT:** capital-math-driven exit escalation.
    See `portfolio-reallocation-discipline`.
  - **August 2026 — SMCI:** catalyst-blind WAIT on positive EV; stale chart levels
    vetoed a confirmed fundamental regime change; horizon-mismatched instrument
    ranking. Missed +27%.
