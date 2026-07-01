# AI Supercycle Quality Screen — Underwriting & Basket Construction
**As-of:** 2026-07-01 (live IBKR pricing, intraday) · **Capital frame:** $60,000 nominal · **Capital source:** SOURCED FROM EXISTING PORTFOLIO
**Desk register:** JPMAM-style thematic growth · **Account NAV:** $51,120.58

> **Framework note.** The `portfolio-reallocation-discipline` and `goldman-technical-strategist` skills referenced in the mandate are not installed in this environment; both frameworks are applied *inline as specified in the prompt*. All prices/volumes are live IBKR snapshots at run time; technicals are computed from IBKR daily bars through the 2026-06-30 close; fundamentals are date-anchored to primary releases (see Section D). Figures that could not be traced to a live/primary source are flagged **[verify]**.

---

## Executive summary — the real problem is the book you already own

The mandate assumed incremental AI exposure of MU/AVGO/NVDA/MSFT/META. **The live account holds none of those as equities.** It holds two **2x daily-reset leveraged ETFs on memory**:

| Holding | Instrument | Mkt value | % NAV | Avg cost | Unrl P&L | Annualized vol |
|---|---|---|---|---|---|---|
| **MUU** | Direxion Daily MU Bull **2X** (2x Micron) | $27,694 | 54.2% | $1,047.31 | **−$584** | **235%** |
| **RAM** | Roundhill T-REX **2X** Long DRAM Daily | $18,769 | 36.7% | $26.25 | **−$2,201** | **222%** |
| IBIT | iShares Bitcoin Trust | $1,740 | 3.4% | $36.34 | −$150 | — |
| 45757 (HK) | Chinese real-estate microcap | $489 | 1.0% | — | −$1,242 | — |
| Cash | — | $16 | 0.0% | — | — | — |

**~91% of the account is a 2x-leveraged, single-sub-theme (memory) bet** — on a beta-adjusted basis ≈ **$92,900 of memory exposure on a $51,121 account**. These are *daily-reset* products: structurally unsuitable as core buy-and-hold holdings (volatility decay/path dependency), and both are currently **at a loss** despite Micron's run — the holder bought near the top, so there is no embedded-gain tax friction protecting the position.

Under the reallocation discipline, **MUU and RAM fail a standalone risk review on their own merits** (instrument structure + 91% concentration + embedded 2x leverage on a cyclical) — *not* because the new basket needs funding. That independent failure is what frees capital. The screen below then deploys into names that **diversify away from memory**, which — combined with a market that has rotated hard — is the binding constraint on the whole exercise.

**Verdict: 3 names clear every gate (NVDA, ANET, VRT). A padded 6–10 name basket is not available at today's prices without violating the no-chase rule — so we ship the smaller, higher-conviction basket and hold dry powder.**

---

## SECTION A — Basket Summary Table (first tranche)

Weights shown as % of the $60,000 nominal frame (the prompt's caps: 15% single / 35% sub-theme = $9,000 / $21,000). Dollar sizes are the *actual* deployment sourced from the reallocation.

| Ticker | Sub-theme | Wt %(of $60k) | $ Alloc | Shares | Entry Zone | Stop (close) | R/R → T1 |
|---|---|---|---|---|---|---|---|
| **NVDA** | Compute / silicon (GPU) | 15.0% | $9,000 | 45 | **191–200** (0.618 fib+EMA200 → 0.5 fib) | 187 | ~2.5:1 (T1 220) |
| **ANET** | Networking / interconnect | 13.75% | $8,250 | 50 | **162–165** (EMA20+0.236 fib) — *wait for tag* | 156 | ~1.9:1 (T1 178) |
| **VRT** | Power & cooling infra | 11.25% | $6,750 | 21 | **318–328** (EMA20+0.236 fib) | 300 | ~2.4:1 (T1 376) |

- **Total deployed (basket):** $24,000 (≈47% of NAV) · **first-tranche ~60%, reserve ~40%** for the deeper fib/EMA tag or an invalidation-reclaim.
- **Cash buffer / dry powder retained:** target ~$3,000 formal buffer (within 5–8%), plus staged-tranche reserve and add-capital for the WAIT list (AVGO first in line).
- **Max single-name weight achieved:** 15.0% (NVDA, at cap). **Max sub-theme weight:** 15.0% — *no intra-basket sub-theme cluster* (compute / networking / power each carry one name).
- **Combined AI-theme concentration after trades:** residual memory (~$9–12k) + NVDA + ANET + VRT ≈ **$33–36k = ~65–70% of NAV** (higher on a beta-adjusted basis because the memory residual is 2x-levered). **This is still high** — but it is now spread across **four** sub-themes (memory / compute / networking / power) versus **one** leveraged sub-theme today. That de-clustering, not the gross theme weight, is the win. It is also why we deliberately *do not* deploy the full freed amount.

---

## Reallocation plan (Workstream 7 — the capital source)

Independent standalone review outcomes:

| Holding | Standalone verdict | Action |
|---|---|---|
| **MUU / RAM** (2x memory) | **Fail** — daily-reset leverage is not a core holding; 91% single-sub-theme concentration; both at a loss (no gain-lock rationale) | **Trim to a de-levered residual** (~$9–12k, ~18–23% NAV). *Ideally swap the residual 2x → 1x/unlevered MU or a semi ETF in a separate step.* |
| **IBIT** | Not AI-supercycle; small loss; non-core to this mandate | **Exit** — funds basket, harvests a small loss |
| **45757 (HK RE)** | Dead money, −72% vs cost, off-theme, illiquid | **Exit** (or leave as a rounding-error stub) |

**Freed capital ≈ $37.5k (ETF trim) + $2.2k (IBIT/HK) + $16 cash ≈ $39.7k.** Of this, **~$24k is responsibly deployable** into the three qualifying names at compliant sizes; **the ~$14–16k remainder stays in cash by design** — a feature of cutting a dangerously leveraged position, not a failure to deploy. Per the mandate: *"If insufficient capital is sourced, reduce the new basket, don't manufacture exits"* — the inverse also holds: when few names clear the bar, **don't over-trim to fund a basket you can't build.**

> No trim above is justified *because the basket needs funding.* Each is justified because the holding independently fails its own review. That is the discipline.

---

## SECTION B — Per-Name Briefs

### 1) NVDA — NVIDIA · Compute/silicon · **BUY (into weakness)**
**Underwrite.** The single highest-quality asset in the theme. Q1 FY2027 (qtr ended 4/26/26, reported 5/20/26): record revenue **$81.6B (+85% y/y)**, Data Center **$75.2B (+92%)**; Q2 guide **$91B** vs ~$86.8B consensus — a beat-and-raise *with China datacenter compute excluded from guidance*. FY2026 revenue $215.9B (+65%). ROIC ≫ WACC by a wide margin, ~70s% gross margin, prodigious FCF, net cash. **Moat:** CUDA software lock-in + full-stack scale (switching cost + ecosystem), not "it has AI in the name." **Valuation:** notably *de-rated* — stock +6% YTD while earnings +85%, i.e., multiple compression — the most attractive quality/price combination in the group. **Overlap check:** compute/logic is a *different* sub-theme from the account's memory book; genuinely additive. **Policy risk:** the largest single-name China/export-control exposure in the basket (already partly de-risked by excluding China from guidance).

**Technical (six-point, computed):**
- **Trend phase:** primary uptrend, *intermediate pullback* — price $198.28 below EMA20 (204.2)/EMA50 (204.9) but above SMA100 (196.6) and rising EMA200 (191.5).
- **Fib:** retraced the 165.17→235.74 up-swing to between the **0.5 (200.45)** and **0.618 (192.13)**.
- **EMA+Fib confluence:** **0.618 fib 192.13 ≈ EMA200 191.48** → high-quality support shelf 191–193; entry zone **191–200**.
- **RSI(14):** 45.2 — neutral, not oversold (room without being washed out).
- **OBV/volume:** decline off the 236 high came on *lighter* volume than the prior advance — constructive (distribution not confirmed). *[qualitative, volume-trend]*
- **ATR(14):** 7.09 (3.6% of price) — lowest-vol name → largest weight. Stop **187** (below EMA200 & 1.5×ATR, closing basis). **T1 220** (0.236 fib/prior shelf), **T2 236**. R/R ≈ **2.5:1** mid-zone.

### 2) ANET — Arista Networks · Networking/interconnect · **BUY (wait for the tag)**
**Underwrite.** The Ethernet back-end winner of the AI build-out. Q1 2026 revenue **$2.709B (+35.1% y/y)**; FY2026 guide raised to **$11.5B (+27.7%)**; AI-networking target raised to **~$3.5B**; customer base = the cloud titans (MSFT, META, GOOGL, ORCL). ~60%+ gross margin, net cash, strong FCF, ROIC ≫ WACC. **Moat:** EOS software stack + merchant-silicon systems → deep switching costs at hyperscale. **Valuation:** premium but PEG-reasonable given 28%+ growth and margin durability. **Overlap check:** networking systems — distinct driver from memory; diversifies the book.

**Technical (computed):**
- **Trend phase:** established uptrend — $169.14 above EMA20 (162.9)/EMA50 (157.8)/SMA100 (148.1)/EMA200 (142.5), full bullish stack.
- **Fib:** only ~5% off the 177.73 high; 116.13→177.73 swing → **0.236 = 163.19**.
- **EMA+Fib confluence:** **0.236 fib 163.19 ≈ EMA20 162.90** → entry zone **162–165**. *Price is at 169 now — this is a WAIT-for-pullback, do not chase.*
- **RSI(14):** 56.3 — healthy, mid-range.
- **OBV/volume:** advance to highs on firm volume; OBV confirming trend. *[qualitative]*
- **ATR(14):** 8.77 (5.2%). Stop **156** (EMA50/1.5×ATR). **T1 178** (prior high). R/R ≈ **1.9:1** from 163–164 (fails the 1.5 test if chased at 169 — hence the limit entry).

### 3) VRT — Vertiv · Power & cooling infrastructure · **BUY**
**Underwrite.** The purest diversifier from a semiconductor-heavy book. Q1 2026: sales **$2.65B (+30%, +23% organic)**, Americas +44%; **orders +252% y/y**, **backlog $15.0B (+109%)**, **book-to-bill 2.9x**; adj. operating margin **20.8% (+430bps)**; **FY guide raised to ~30% organic / ~51% EPS growth**. Positive net revisions, expanding margins, deleveraging on FCF. **Moat:** scale + installed base in data-center thermal/power management, with switching costs on integrated systems. **Valuation:** the richest of the three (EV/EBITDA full **[verify vs 3-yr band]**) — but a 2.9x book-to-bill and 252% order growth are a genuine offsetting acceleration, so it survives the price-discipline gate. **Overlap check:** electrical/thermal infra — *uncorrelated to memory demand cyclicality*; the single best diversifier here.

**Technical (computed):**
- **Trend phase:** strong uptrend — $333.17 above EMA20 (318.4)/EMA50 (312.6)/SMA100 (290.9)/EMA200 (246.9).
- **Fib:** shallow pullback (~11%) from the 376.23 high; 149.83→376.23 swing → **0.236 = 322.80**.
- **EMA+Fib confluence:** **0.236 fib 322.80 ≈ EMA20 318.39** → entry zone **318–328** (price 333 sits just above; scale in on a tag).
- **RSI(14):** 54.8 — mid-range, room to run.
- **OBV/volume:** uptrend on rising participation; pullback on lighter tape. *[qualitative]*
- **ATR(14):** 21.47 (**6.4% — highest vol in the basket**) → smallest weight. Stop **300** (1.5×ATR, closing basis). **T1 376** (prior high). R/R ≈ **2.4:1** from ~322.

---

## SECTION C — Names Screened Out (the discipline record)

| Ticker | Sub-theme | Gate failed | Note |
|---|---|---|---|
| **AVGO** | Compute/silicon (custom ASIC) | **Portfolio overlap** | Passes quality, valuation *and* technicals (pullback to 0.618 fib 365 / SMA100 372; R/R ~1.7:1). Excluded *only* to avoid stacking a second large semiconductor beta on top of NVDA + the memory residual. **#1 on the add list.** |
| **AMD** | Compute/silicon | **Technical R/R + overlap** | +169% YTD, sitting at all-time high ($577). No-chase; poor R/R to any T1. |
| **GEV** | Power & grid | **Technical R/R + lumpiness** | At all-time high ($1,170); a single share is too lumpy for this account size. |
| **PANW** | Cybersecurity | **Technical R/R** | At all-time high ($341, +85% YTD). No confluence entry. |
| **CRWD** | Cybersecurity | **Technical R/R + lumpiness** | Near ATH ($762). No pullback structure. |
| **CEG** | Power (nuclear) | **Technical (trend)** | −29% YTD, near 52-wk low; primary downtrend/falling knife — not a confirmed base. |
| **MSFT** | Hyperscale/cloud | **Technical (trend)** | Quality/valuation attractive (−22% YTD, near 52-wk low) **but** in a primary downtrend below the 200-day. **WATCH** for a reclaim of ~$400/50-day. |
| **PLTR** | Applied AI/software | **Technical (trend) + valuation** | −34% YTD, downtrend near 52-wk low; multiple still rich. |
| **CRDO** | Networking/interconnect | **Volatility/entry** | Near 52-wk high with **~123% annualized vol**; vol-adjusted size would be negligible and the spread is wide — uninvestable at this account size today. |
| **IBIT** (held) | — (non-AI) | **Off-theme** | Recommend exit to fund basket (small loss). |
| **MUU / RAM** (held) | Memory (2x-levered) | **Reallocation target** | See reallocation plan — trim to a de-levered residual. |

---

## SECTION D — Explicit Assumptions & Data Recency

- **Prices / volume / volatility / 52-wk stats:** live IBKR snapshots pulled **2026-07-01 intraday** (e.g., NVDA $198.28, AVGO $376.44, VRT $333.17, ANET $169.14; MUU $1,025.70, RAM $23.54, IBIT $33.44). Not cached.
- **Technical stack (EMA20/50, SMA100, EMA200, RSI14, ATR14, swing/Fib):** computed from **IBKR daily OHLC bars, 2025-07-02 → 2026-06-30 close** (Wilder smoothing for RSI/ATR). OBV/volume reads are **qualitative volume-trend observations**, not a computed 13-period eOBV — flagged as such.
- **Fundamentals (date-anchored):** NVDA Q1 FY2027 release **2026-05-20**; VRT Q1 2026 release (~Apr 2026); ANET Q1 2026 release (~May 2026) — via primary/company sources listed below.
- **[verify] / not independently sourced this run:** precise ROIC−WACC spreads, EV/EBITDA vs each name's own 3-yr band, and full trailing-90-day consensus revision series (S&P Global / EDGAR line items were not pulled). Quality/valuation verdicts use the date-anchored releases above plus the desk's priors — **verify against the latest 10-Q and current consensus before execution.** Where sources conflict, that is surfaced, not averaged.
- **Account data:** IBKR positions/summary/allocation, live 2026-07-01. Buying power $3,408, cash $16 — the $60k nominal frame is **not fundable as new cash**; hence the reallocation-sourced construction.
- **FX/tax (factual, not advice):** basket is USD-denominated (no incremental FX hedge by default); US-source dividends to a non-US holder are typically subject to statutory withholding — confirm actual treatment with a tax advisor. The residual HK holding carries HKD FX and China policy exposure.
- **Portfolio-shock note:** NVDA (direct China/export-control exposure) and the memory residual would draw down *together* under a single export-control action or a hyperscaler capex guide-down — the two largest AI-beta exposures are correlated to the same macro shock. This is the explicit reason the basket is sized restrained and material cash is retained.

**Sources:** [NVIDIA Q1 FY27 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000051/q1fy27pr.htm) · [NVIDIA newsroom Q4/FY26](https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026) · [Vertiv Q1 2026 release](https://www.prnewswire.com/news-releases/vertiv-reports-strong-first-quarter-with-diluted-eps-growth-of-136-adjusted-diluted-eps-growth-of-83-raises-full-year-guidance-302750110.html) · [Vertiv Q1 2026 8-K (SEC)](https://www.sec.gov/Archives/edgar/data/0001674101/000167410126000006/exhibit991vrt02112026.htm) · [Arista Q1 2026 results](https://infotechlead.com/networking/arista-networks-q1-2026-revenue-surges-35-as-ai-networking-cloud-titans-and-enterprise-demand-drive-growth-95620)

---

## DECISIVENESS

1. Every basket name carries an explicit **BUY** with a stated entry zone, stop, and T1 — no "accumulate" hand-waving. NVDA is a buy into 191–200; **ANET requires patience for the 162–165 tag (do not chase at 169)**; VRT scales in on a tag of 318–328.
2. Fewer than MAX_POSITIONS names cleared every gate. We **ship three**, not a padded six, and retain dry powder — consistent with the mandate.
3. The single most important action is **not the new basket** — it is **de-levering the 91% memory concentration** that independently fails its own review. Do that first; deploy the diversifiers second; keep the rest in cash.

*Research and portfolio-construction framework, not personalized investment advice — final capital deployment remains Emmanuel's.*
