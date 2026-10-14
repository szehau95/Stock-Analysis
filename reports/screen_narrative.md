# Malaysian Banks — Fundamental Value × Technical Upside Screen (v1.1)

**Run date:** 14/10/2026 · **Prices:** close 13/10/2026 (last complete Bursa session) · **Universe:** core six (MAYBANK, PBBANK, CIMB, HLBANK, RHBBANK, AMBANK) · **Owner:** Emmanuel Lim Sze Hau · **Not client-facing**

**v1.1 adds the securities-book (treasury) factor.** Rising bond yields drove recent broker downgrades of RHB and CIMB, and v1.0 had not modelled that. v1.1 adds:
- each bank's bond-book exposure and its rate sensitivity;
- a sweep of broker rating changes;
- corrections to the OPR framing and to MAYBANK's capital.

The verdict changes. The v1.0 report is kept at `output/screen/v1.0/report_v1.0.md`, and the reconciliation table is below.

† **HLBANK is an employer-group entity.** It went through the identical framework. Personal dealing is subject to HLB staff trading and blackout rules, so check compliance before acting on any view on HLBANK (HLFG was not screened).

---

## Verdict in one screen

| | Call |
|---|---|
| **Top pick** | **HLBANK † — Overweight, Medium confidence** (Low confidence on it being *the* pick, because it is #2 on the 60/20/20 re-rank). It is the only bank scoring at least 50 on value, quality and technicals. Its bond book has the second-lowest rate sensitivity (−32bp CET1 per +100bp). It has no broker downgrade, and it is beating the KLCI by 6% over 3M. Entry: RM21.20–21.59, stop RM20.66. Add on a weekly close above RM21.86; T1 RM23.41, T2 RM24.58. |
| **Runner-up (conditional)** | **RHBBANK — Neutral, High confidence.** It is still the cheapest bank (+32% to fair value, highest yield), but it is no longer the top pick. It has the **highest bond-book rate sensitivity in the group** (FVOCI is 32% of RWA; −61bp CET1 and −3.9% book value per +100bp). HLIB cut it to Hold at RM8.00 on 3Q26 trading income, and its ROE has faded for three quarters. Upgrade to Overweight only after **(a)** the late-November 3Q26 print shows the treasury hit within our estimate and **(b)** a weekly close above RM8.04. |
| **Avoid** | **AMBANK — Underweight, Low confidence.** It has the weakest quality score (29): CASA −10% YTD, NIM −8bp y/y, the highest GIL and the thinnest coverage. JPMorgan cut it to Neutral, and its FVTPL book makes it the second most exposed to a 3Q26 trading-income miss. **CIMB is also Underweight** (JPMorgan cut it to Underweight; it has the largest FVTPL book and −52bp CET1 per +100bp). |
| **Watchlist** | **RHBBANK** (3Q26 print plus a weekly close above RM8.04) and **MAYBANK** (weekly close above RM10.65). MAYBANK carries the second-highest rate sensitivity (−57bp) and its post-Etiqa CET1 is ~13.7% after correction, so it waits too. |
| **Sector** | **Fairly valued, technically weak, and now facing a rising-yield regime.** The Fed hiked on 16/09. UST 10Y reached 5.3%. MGS 10Y spiked 58bp to 4.18% on 11/09 before easing to 3.83%. ANZ and UOB call a BNM hike on 05/11. The *realised* bond-book damage so far is small (≤0.9% of book value, ≤21bp of CET1 at Q3 quarter-end, ≤2% of FY profit). But the *forward* sensitivity differs 2.4× across banks, and that difference is what changes the call. **Favour short-duration books (HLB, PBB). Make bond-heavy books (RHB, MAYBANK, CIMB) earn their entry through the 3Q26 print.** |

---

## What changed from v1.0, and why

{{M0_RECON}}

**Factors v1.0 missed or got wrong, all now in the model:**
1. **Securities-book rate risk** (new Module 2b).
   - FVOCI bond marks now reduce book value and CET1.
   - A 3Q26 FVTPL trading hit is estimated.
   - A +100bp forward sensitivity enters the quality score at 10%, with the prompt's other quality weights scaled by 0.9.
2. **Broker-action sweep** (new Module 1.5).
   - Every rating or target change in the last 60 days is logged with its stated reason and mapped to a modelled factor.
   - A negative action in the last 30 days, whose reason is not yet in reported numbers, blocks an Overweight until the next print.
3. **OPR direction.** v1.0 framed OPR risk as cuts. The market is debating a **hike**. Module 7 is rewritten with two-sided effects: better NIM, but further bond-book losses.
4. **MAYBANK's capital.** v1.0 put the RM4.83b Etiqa buyout at −0.83pp of CET1, using an RWA proxy of ~RM580b. T1 group RWA is **RM440.5b**, so the hit is **−1.10pp**. Pro forma CET1 is ~13.7% after the bond mark, not ~14.1%.
5. **Data source.** Yahoo's "available-for-sale" line combines FVOCI and amortised-cost bonds; this was confirmed against CIMB's, HLB's and AMBANK's T1 statements. All securities and RWA data now come from each bank's own 30/06/2026 statements.
6. **Two method changes, disclosed rather than tuned.**
   - Confidence now measures whether the *lean* survives each alternative specification. v1.0 measured whether the rank moved by more than one place, which flips on noise when six names sit this close.
   - A composite gap under 2 points is a tie, broken on (1) no news-flow flag, (2) lower rate risk, (3) quadrant.

---

## Variables block (as run)

```
RUN_DATE        = 14/10/2026 (prices: close 13/10/2026)
UNIVERSE        = core six; BIMB, ALLIANCE, AFFIN only as P/B–ROE regression context (their BV is not treasury-adjusted)
BENCHMARK       = FBMKLCI. Sector proxy = cap-weighted, dividend-adjusted core-six composite
LATEST_QTR      = June-2026 quarter for all six (2Q26; HLBANK 4QFY26; AMBANK 1QFY27)
COE             = MGS10 3.83% (BNM FMIP, 13/10/2026, T1) + β_Blume × 6.0% ERP (β = 3y weekly vs KLCI) → 9.1%–11.5%
LT_GROWTH (g)   = 4.0% (sensitivity 3% / 5%)
OPR_CURRENT     = 2.75% (BNM MPS 03/09/2026, T1); next MPC 05/11/2026; hike priced as a live risk
TREASURY        = FVOCI marked 30/06 → 13/10 at the average 3/5/7/10Y MGS move (+24bp); duration calibrated to RHB Research
TA              = weekly (completed weeks to 09/10) + daily; 3–6 month horizon; dividend-adjusted OHLC
WEIGHTS         = Value 40 · Quality 30 · Technical 30 (sensitivity 60/20/20, 20/30/50)
QUALITY v1.1    = prompt weights × 0.9 + rate risk 10%
OUTPUT          = PLAIN_TEXT; CLIENT_FACING = FALSE
```

---

## Module 1 — Premise validation & data freshness

All six banks last reported the June-2026 quarter, between 18/08 and 28/08/2026. The next results are due in late November 2026 (unconfirmed). All six clear the RM5m 3M-ADV liquidity floor.

{{M1_FRESHNESS}}

{{M1_EVENTS}}

**Additional events found in the v1.1 sweep:**
- **PBB:** privatising its 73.23%-owned Hong Kong unit PFHL at HK$2.50/share (~RM379m, <1% of equity, about −13bp CET1 at bank level per RHB Research; long-stop 08/03/2027). Brokers call it neutral.
- **CIMB:** reportedly weighing a sale of its Philippine operations (up to USD200m), alongside a plan to return up to RM2b of extra capital by 2027 (T3, aggregator).

### Module 1.5 — Broker-action sweep (last ~60 days)

{{M1_BROKERS}}

**Reads.** Every recent negative action cites the same driver: rising bond yields hitting trading income and capital (3Q26 surprises "skewed negative"). That is a factor reported numbers do not yet show, and Module 2b now quantifies it. On 07/10 CIMB fell 4.8%, AMBANK 4.5%, RHB 2.4%, PBB 1.7% and MAYBANK 1.0%. HLB's −2.6% that day was its 80-sen ex-dividend date (−3.6% mechanically), so ex-dividend it rose.

---

## Module 2 — Fundamentals (T4Q, latest quarter, NTM consensus)

Book values below are **treasury-adjusted**: June BV, less the after-tax FVOCI mark from 30/06 to 13/10 (Module 2b). HLBANK's core basis strips Bank of Chengdu from earnings *and* equity:
- **ROE:** core 10.2% vs 11.2% headline.
- **Associates' share:** RM1,380m of RM4,531m FY26 PAT.
- **The stake:** carrying value RM10.35b vs market value RM8.85b. It is valued at market (RM4.32/share).

{{M2_VALUATION}}

{{M2_PROFIT}}

{{M2_RISK}}

{{M2_TARGETS}}

*Stage 2 loans, non-interest-income share and ROA are UNVERIFIED for the set. The quality score therefore uses GIL alone in its asset-quality slot. "CET1 > 13%" now uses T1 group RWA, not a proxy.*

### Module 2b — Securities book & rate risk (new in v1.1)

**Method:**
1. **Holdings.** FVOCI debt, amortised-cost debt, FVTPL, group RWA and FVOCI reserves come from each bank's 30/06/2026 statements (T1).
2. **Duration.** Effective FVOCI duration is calibrated to RHB Research's group CET1 sensitivities (MAYBANK 57bp, CIMB 52bp per +100bp; T2). That gives **2.9 and 3.2 years**, consistent with BIMB Research's 5–6-year gross duration net of hedges. RHB and AMBANK take the 3.0-year mean. PBB and HLB take 0.8× that, because two brokers rank them shortest; HLB's T1 repricing table agrees, with 80% of FVOCI in the 1–5-year bucket.
3. **Yield moves (BNM, T1), average of 3Y/5Y/7Y/10Y MGS:**
   - Q3 (30/06–30/09): +36.5bp
   - peak (11/09): +49.5bp
   - to 13/10: +24bp
4. **Tax** at 24%.
5. **CET1 follows BNM's capital framework.** Because 55% of cumulative FVOCI *gains* are deducted from CET1, a loss that only erodes a positive reserve costs CET1 45 sen per ringgit; anything beyond the reserve hits in full. Unknown reserves (MAYBANK, PBB, CIMB) are set to zero, which is conservative.
6. **FVTPL.** The 3Q26 FVTPL hit uses government debt (actual for CIMB, 70% of FVTPL otherwise) × 1.5-year duration × the 3Y/5Y Q3 move. It is unhedged, so it is an upper bound.

{{M2B_BOOK}}

{{M2B_IMPACT}}

**Reads**
- **You were right about RHB and CIMB, and RHB is the extreme case.** RHB has the largest bond book relative to its capital: FVOCI is 32% of RWA and 1.68× equity. Its FVOCI reserve was only RM0.44b at June, down from RM0.68b in December. It is therefore the most exposed to a *further* yield rise: −61bp CET1 and −3.9% book value per +100bp. CIMB is third on CET1 sensitivity (−52bp), has the largest trading book (RM66.7b FVTPL; RM46.3b of it government debt), and carries the biggest 3Q26 trading-income risk (up to ~8% of quarterly PBT, unhedged). MAYBANK (−57bp) completes the exposed trio, matching Affin Hwang's ranking.
- **The damage already done is small.** Half the Q3 spike has reversed. Marked to 13/10, book values are 0.4–0.9% lower and CET1s 6–14bp lower. Even at the 11/09 peak, no bank lost more than 28bp of CET1, and the 3Q26 FVTPL hit is ≤2% of FY profit. That supports HLIB's "foregone upside, not losses" read for RHB.
- **So the factor works through forward risk and news flow, not current value.**
  - **Forward risk:** a Fed in hiking mode, UST at a 24-year high and BNM hike odds mean another +50–100bp is a live scenario. On a +100bp move, RHB loses 2.4× the CET1 that PBB does.
  - **News flow:** 3Q26 will print the Q3 marks and the trading-income dip, and brokers have already downgraded the exposed names.
- **AMBANK is the exception on capital.** Its RM0.77b FVOCI reserve absorbs the mark at 45%, so its CET1 sensitivity is low (−28bp). Its book-value sensitivity is still high (−3.5%), and its FVTPL is the second largest relative to profit, hence JPMorgan's downgrade.

---

## Module 3 — Valuation (on treasury-adjusted book value)

{{M3_JPB}}

**P/B vs core ROE, nine listed banks:** P/B = −0.29 + 13.26 × ROE, **R² 0.89** (slope s.e. 1.77). Core six only: −1.36 + 23.26 × ROE, R² 0.87.

{{M3_REG}}

{{M3_DIV_CONS}}

**Reads**
- **The bond mark barely moves fair values** (≤1.2 points of mispricing). RHB stays the cheapest bank: +32% to Gordon value, −12% regression residual, 7.1% yield. Its realistic re-rating anchor is the regression-fit price of **RM8.32** (+14%), and Gordon value is RM9.63.
- **But part of RHB's discount is now explained.** Its implied ERP is 7.9%, against 4.9–6.5% for the others. That premium lines up with the highest rate sensitivity, a three-quarter ROE fade, the lowest CASA and a fresh downgrade. On latest-quarter ROE with β=1, it is only +2% cheap.
- **HLB is fairly valued** (+1.7%; −3.8% at β=1) on an ex-Chengdu basis, and **PBB is rich in every specification** (−13%).
- **CIMB's valuation is a beta question.** It is −18% at its own β of 1.28 and +6% at β=1.
- **Consensus gaps over 15%** (PBB, CIMB, HLB, AMBANK) reflect three things: targets are 12-month forward, brokers assume higher forward ROE, and brokers use a flat COE. RHB is the only bank where our fair value sits above the consensus median (+10%). HLIB's new RM8.00 is below it.

---

## Module 4 — Quality score v1.1 (0–100, percentile within the core six; UNVERIFIED inputs score 50)

{{M4_QUALITY}}

*Weights are the prompt's (ROE 30, trend 10, CASA 15, CIR 10, GIL 15, LLC 10, CET1 10) × 0.9, plus **rate risk 10** (CET1 bp per +100bp, inverse). The CET1 buffer uses CET1 marked to 13/10, and MAYBANK's also includes the Etiqa buyout at −1.10pp. The "Quality v1.0 wts" column re-scores on the same v1.1 inputs with the prompt's original weights, to isolate the effect of the new factor. The v1.0 report's quality numbers are in the reconciliation table above. ROE trend is the slope of the last four quarterly annualised core ROEs.*

**Reads.** PBB rises (78): it has the best rate-risk profile on top of the best franchise metrics. RHB (30) and AMBANK (29) sit at the bottom. MAYBANK slips to 53 because the Etiqa correction thins its CET1 buffer to 0.7pp above 13%, and its rate risk is the second highest.

---

## Module 5 — Technical analysis (weekly primary, daily entry; unchanged from v1.0)

Indicators use dividend-adjusted OHLC, because every core bank went ex-dividend in the 3-month window (HLB 80 sen on 07/10; MAYBANK 23/09; CIMB 15/09; RHB 14/09; PBB 10/09).

How the levels are built:
- **Structure:** weekly pivots (3y), daily pivots (±15 sessions), 52-week extremes, high-volume nodes, and the 50/200-DMA and 40-week lines. Levels are clustered within 0.6 ATR.
- **T1:** the first cluster at least 1.5 ATR above price.
- **Stop:** the tighter of (support − 0.25 ATR) and 2 × ATR, never within 1.5 ATR of price.

{{M5_TREND}}

*MACD key: ↑/↓ = MACD above/below its signal line; +/− = histogram rising/falling. Regime: Uptrend needs the weekly close above a rising 40-week MA, plus price above the 200-DMA with the 50-DMA above the 200-DMA. Downtrend needs the weekly close below a falling 40-week MA plus price below the 200-DMA. Anything else is Range.*

{{M5_RS}}

{{M5_LEVELS}}

{{M5_SCORE}}

**Reads.** All six trade below their 200-DMA, and OBV is falling on all six. HLB has the best relative strength (+6.1% vs KLCI over 3M) on a golden cross, but must reclaim the RM21.8–22.1 moving-average band. RHB has the weakest tape: ADX 54 with sellers in control, and RS −6.9%. That is consistent with the market pricing exactly the rate-risk and downgrade story above.

---

## Module 6 — Composite, quadrant, sensitivity

{{M6_VALUE}}

{{M6_COMPOSITE}}

Quadrant: Value ≥ 50 = cheap (relative to the core six); Technical ≥ 50 = constructive (absolute).

**Rules**
- **Lean:**
  - Overweight needs all three: a top-2 composite, the ACTIONABLE BUY or VALUE TRAP WATCH quadrant, and **no negative broker action in the last 30 days**.
  - Underweight needs both: the AVOID quadrant and a bottom-2 composite.
  - Everything else is Neutral.
- **Confidence:** the share of the four alternative specifications (60/20/20, 20/30/50, β=1 COE, conservative T1) under which the lean is unchanged. 4/4 = High, 3/4 = Medium, 2 or fewer = Low.
- **Top pick:** the highest composite among Overweight-eligible names. A gap under 2 points is a tie, broken on news flow, then rate risk, then quadrant.

**The ruling**
- **Composite: RHB 54.4 vs HLB 54.2, a tie.** HLB wins on every tie-break: no downgrade (RHB has HLIB's), half the rate sensitivity (−32bp vs −61bp), and ACTIONABLE BUY vs VALUE TRAP WATCH. RHB is also blocked from Overweight by the 30-day rule.
- **Does the top pick survive both re-weightings?** **No.** HLB is #1 at 20/30/50 but #2 at 60/20/20, where RHB's value dominates. Per the prompt, the top-pick designation drops one notch, from Medium to **Low**. The Overweight lean on HLB stays at Medium (3/4); it fails only the β=1 specification.

---

## Module 7 — Macro & catalyst overlay

| Date | Catalyst | Direction | Names most affected | vs quant ranking | Tier / source |
|---|---|---|---|---|---|
| 16/09/2026 (done) | **Fed hikes 25bp**, its first hike in 3+ years, and signals another; UST 10Y 5.32–5.35% (24-year high, early October) | − (MTM, foreign flows) | Bond-heavy: RHB, MAYBANK, CIMB | **Drives the v1.1 change**: penalises FVOCI-heavy books | T2: The Star 22/09 and 09/10 |
| 11/09 → 13/10 | **MGS 10Y** 3.60% → 4.18% peak → 3.83%; Q3 average curve move +36.5bp; still +24bp from 30/06 | − realised (small); − forward | As above | Quantified in Module 2b | T1: BNM FMIP |
| 05/11/2026 | **BNM MPC.** ANZ and UOB call **+25bp** ("as early as November"); Bank Muamalat sees normalisation to 3% in 2027; Kenanga contrasts ~70% market odds with under 20% of economists; 3Y MGS 3.43% sits 68bp above OPR | **Two-sided.** A hike lifts NIM (~+2–4bp per 25bp, assuming 2025's cut sensitivities are symmetric; larger for PBB and RHB) but adds bond-book losses | **Best placed: PBB** (NIM-sensitive, least bond risk). Mixed: RHB. MTM-heavy but CASA-rich: MAYBANK, CIMB | Reinforces PBB's upgrade to Neutral and HLB's top pick; keeps RHB on hold | T2: The Edge 17/09 (node/818338); T3: Vocal (Kenanga odds) |
| 09/10/2026 (done) | **Budget 2027**: SME and housing credit support; deficit 3.3% of GDP | + | Sector | In the 12–13/10 rebound | T2: Malay Mail, NST, The Star |
| Late Nov 2026 | **3Q26 results**: first print of the Q3 bond marks and trading-income dip (JPMorgan: "skewed negative") | − near term, then clears the overhang | **CIMB, AMBANK, RHB**, then MAYBANK | **The gating event for RHB's upgrade**; reinforces the CIMB and AMBANK Underweights | T2 |
| 21/12/2026 and 21/06/2027 | **FBM KLCI expands to 50 names**; financials' weight ~43% → ~37% | − (passive selling) | MAYBANK, PBB, CIMB | Reinforces staged entries | T2: The Star 21/08 |
| 1Q27 at the earliest | **RHB capital-management framework** (50–60% payout; possible +100bp CET1 from Basel III reforms) | + | RHB | The upside case once the rate risk clears; excess CET1 ~RM3.1b (T1 RWA) | T2: The Star 02/09 |
| Ongoing | **Bank-specific** | | | | |
| | MAYBANK: Etiqa buyout −1.10pp CET1 (corrected); DRP; overlays RM2.6b | − | MAYBANK | Neutral until the flip trigger | T1 RWA; T2 |
| | HLB: Bank of Chengdu at 0.88× book (RM1.5b below carrying value); CET1 12.8% | − | HLB † | Why it is only Medium confidence | T1, T3 |
| | PBB: PFHL privatisation (RM379m) | ≈ | PBB | Neutral | T2 |

**Ruling.** The overlay now *drives* part of the ranking rather than just timing it:
- A rising-yield regime rewards short-duration, low-FVOCI books (HLB, PBB).
- It also argues against front-running the bond-heavy names (RHB, MAYBANK, CIMB) before 3Q26 shows the damage.
- An OPR hike would be a mixed blessing: better NIM, worse marks. PBB benefits most cleanly.

---

## Module 8 — Verdict

### 8.1 Ranked scorecard

{{M8_SCORECARD}}

*Lean and confidence follow the Module 6 rules. CET1 adj. is marked to 13/10 and, for MAYBANK, includes Etiqa. HLB's P/B, fair P/B and mispricing are on the ex-associate basis (headline P/B 1.06×).*

### 8.2 Top pick — HLBANK † (Overweight · lean confidence Medium · top-pick designation Low)

- **Value: fair, with a historical cushion.**
  - Fair value RM21.84 (+1.7%) on a 10.2% ex-Chengdu core ROE, with the Bank of Chengdu stake at market.
  - P/B is −1.3 SD vs its 5-year history, the cheapest of the six vs its own past.
  - Yield 5.4%.
- **Quality and balance sheet: the right risk profile for this tape.**
  - Second-lowest rate sensitivity: −32bp CET1 and −1.6% book value per +100bp, on a short (1–5-year) FVOCI book.
  - Best asset quality: GIL 0.57%, LLC 244% including regulatory reserves, credit cost ~4bp.
  - ROE trending up; loans +7.7%; CIR 37.6%; no broker downgrade.
- **Technical:**
  - Strongest relative strength: +6.1% vs KLCI over 3M; golden cross 02/09/2026.
  - Price sits just under the RM21.8–22.1 band (200-DMA, 40-week line and 20/50-DMA) after the 80-sen ex-dividend.
  - R:R 2.4 to T1 assumes that band is reclaimed (0.46 measured to the band). That is why execution is staged.
- **Execution:**
  - **Half:** RM21.20–21.59, stop RM20.66 on a daily close (−3.8%).
  - **Rest:** on a weekly close above RM21.86. Post-flip stop RM21.19. T1 RM23.41 (+9.0%), T2 RM24.58.
- **Invalidation:**
  - Daily close below RM20.66.
  - 1QFY27 CET1 below 12.5%, or a payout cut.
  - A Bank of Chengdu impairment above RM1.5b (about RM0.73/share).
  - NIM below 1.80%.
  - † Clear staff dealing and blackout rules first, especially into the late-November 1QFY27 results.

### 8.3 Runner-up (conditional) — RHBBANK (Neutral now · High confidence)

- **For:**
  - Still the cheapest bank on every value lens: +32% to fair value, regression-fit RM8.32, 7.1% yield.
  - CET1 14.7% after the bond mark (~RM3.1b above 13%).
  - Loans +7% y/y; a 1Q27 capital-management catalyst.
  - The discount is real, and the October rally in MGS is already reversing some of the Q3 marks.
- **Against (why not now):**
  - Highest bond-book rate risk in the group: −61bp CET1 and −3.9% book value per +100bp, with only a RM0.44b reserve cushion.
  - HLIB's downgrade to Hold RM8.00 on 3Q26 trading income.
  - Three-quarter ROE fade to 9.6%; lowest CASA (27.6%).
  - The weakest tape of the six.
- **Upgrade to Overweight when both hold:**
  - **(a)** 3Q26 (late November) shows CET1 ≥ 14.5% after the Q3 mark (our estimate is ~14.7%), annualised ROE ≥ 9.5% and no new rating cut.
  - **(b)** A weekly close above RM8.04. Then: stop RM7.86, T1 RM8.24, T2 RM8.77, value anchors RM8.32 and RM9.63.

### 8.4 Avoid — AMBANK (Underweight · Low) — and CIMB (Underweight · Low)

- **AMBANK:**
  - Lowest-quality bank (29): ROE 10.3 → 9.7%, NIM −8bp y/y, CASA −10% YTD, highest GIL (1.62%), thinnest LLC (102.5%).
  - JPMorgan cut it to Neutral.
  - FVTPL is the second largest relative to profit (up to 5.6% of quarterly PBT).
  - P/B is +1.3 SD above its 5-year mean.
  - Its RM0.77b FVOCI reserve protects CET1, not earnings.
- **CIMB:**
  - JPMorgan cut it to Underweight.
  - Largest trading book (RM66.7b FVTPL) and the biggest 3Q26 trading-income risk.
  - −52bp CET1 per +100bp.
  - Valuation only works at β=1.

**PBB moves from Underweight to Neutral (Low confidence).** It is still rich (−13%), but it has the lowest rate risk and the highest quality, and it would gain most cleanly from an OPR hike.

### 8.5 Watchlist (cheap or close, but waiting on a trigger)

| Bank | Why on the list | What blocks it | Trigger | Then: stop / T1 / T2 |
|---|---|---|---|---|
| **RHBBANK** | Value 91, yield 7.1% | Rate risk −61bp; HLIB Hold; ROE fade; tape | **3Q26 print (criteria in 8.3) + weekly close > RM8.04** | 7.86 / 8.24 / 8.77 |
| **MAYBANK** | +8% fair value (+17% on latest-quarter ROE); ROE improving; CASA 41.5% (NIM upside if BNM hikes) | Rate risk −57bp; post-Etiqa CET1 ~13.7%; death cross; KLCI-50 weight | **Weekly close > RM10.65** and post-Etiqa CET1 ≥ 13.5% at 3Q26 | 10.48 / 11.02 / 11.71 |

### 8.6 Key risks to the sector call (ranked by probability × impact)

1. **A further sell-off in bonds and rates** (medium-high probability, medium-high impact). Drivers: Fed hikes, UST above 5.3%, BNM hikes. Each +100bp costs 26–61bp of CET1 and 1.6–3.9% of book value. RHB, MAYBANK and CIMB are most exposed; this is the factor v1.0 missed.
2. **3Q26 trading-income and bond-mark disappointments** (high probability, medium impact; late November). CIMB, AMBANK and RHB are flagged by brokers.
3. **KLCI-50 passive selling into 21/12/2026** (high probability, medium impact). MAYBANK, PBB and CIMB carry the largest weights.
4. **Asset-quality mean reversion on SMEs** (medium probability, high impact). GILs are near record lows. RHB and AMBANK are most SME-sensitive.

### 8.7 Sources

| # | Source | Tier | As of |
|---|---|---|---|
| 1 | BNM Monetary Policy Statement (OPR 2.75%) — bnm.gov.my | T1 | 03/09/2026 |
| 2 | BNM FMIP benchmark MGS yields, daily 2025 → 13/10/2026 (3Y/5Y/7Y/10Y) | T1 | 13/10/2026 |
| 3 | Maybank Group financial statements 2Q FY2026 (FVOCI, FVTPL, amortised cost, group RWA RM440.5b) — maybank.com | T1 | 30/06/2026 |
| 4 | Public Bank condensed interim FS 2Q26 (A8–A10, A30 capital and RWA) — publicbankgroup.com | T1 | 30/06/2026 |
| 5 | CIMB Group FS 30/06/2026 (A9–A12, A28 capital; RWA RM389.7b) — cimb.com | T1 | 30/06/2026 |
| 6 | HLB Annual Report 2026 (audited balance sheet, fair-value reserve note, Total RWA, IRRBB repricing table) — hlb.com.my | T1 | 30/06/2026 |
| 7 | RHB Bank interim FS Q2 2026 (A14–A16, A29 capital incl. FVOCI reserves, RWA) — rhbgroup.com | T1 | 30/06/2026 |
| 8 | AMMB Holdings condensed FS 30/06/2026 (A10–A12, A31 incl. fair-value reserve, RWA) — ambankgroup.com | T1 | 30/06/2026 |
| 9 | Company results releases: RHB 28/08, HLB 27/08, AmBank 18/08, CIMB 28/08/2026; HLFG FY2026 analyst deck | T1 | 08/2026 |
| 10 | RHB Research via BusinessToday: "100bps bond yield rise could cut banks' CET-1 by 46bps" (group sensitivities; AMMB and PBB insulated) | T2 | 06/10/2026 |
| 11 | HLIB via BusinessToday: RHB Hold RM8.00, 3Q26 trading income | T2 | 05/10/2026 |
| 12 | HLIB via The Star: "Rising bond yields pose short-term risk to banks" (MGS path; CIMB sovereign FVTPL RM12.2b; AMMB and BIMB NOII exposure) | T2 | 09/10/2026 |
| 13 | The Edge node/820219 (Affin Hwang IB: duration and capital-ratio rankings) | T2 | 01/10/2026 |
| 14 | JPMorgan CIMB → Underweight, AMMB → Neutral; 07/10 price moves (thefinancialcoconut.com market report; The Star) | T2 | 07/10/2026 |
| 15 | The Edge node/818338 "OPR hike bets rise after Fed move" (ANZ, UOB, Bank Muamalat) | T2 | 17/09/2026 |
| 16 | The Star (BIMB Research: 5–6-year securities duration, mostly FVOCI; Fed hike 16/09) | T2 | 22/09/2026 |
| 17 | The Star 02/09/2026 (RHB capital management; HLIB Buy RM9.50 at the time) | T2 | 02/09/2026 |
| 18 | The Star 08–09/09/2026 (PBB–PFHL privatisation) | T2 | 09/2026 |
| 19 | Kenanga, Maybank 2Q26 note; The Edge PBB 2Q26; Kenanga RHB 4Q25; TA Research PBB 1Q26 | T2 | 03–08/2026 |
| 20 | The Star / BusinessToday / Kenanga: FBM KLCI-50 | T2 | 04–08/2026 |
| 21 | Malay Mail, NST, The Star: Budget 2027 | T2 | 09–12/10/2026 |
| 22 | Vocal.media citing Kenanga (OPR hike odds) | T3 | 09/2026 |
| 23 | Yahoo Finance: prices to 13/10/2026; consensus (14/10/2026); balance sheets used only for P/TBV and HLB associate carrying value | T3 | 13–14/10/2026 |
| 24 | Yahoo Finance: Bank of Chengdu (601838.SS), CNYMYR | T3 | 13–14/10/2026 |
| 25 | klsescreener transcription of Bursa quarterlies (point-in-time panels, core-EPS adjustments; 30/09 run) | T3 → reconciled to T1 | 30/09/2026 |

### 8.8 Data gaps and method notes

- **UNVERIFIED:**
  - FVOCI reserves for MAYBANK, PBB and CIMB (set to zero, which is conservative).
  - The government share of FVTPL outside CIMB (70% assumed).
  - The split between MY sovereign and corporate bonds in each FVOCI book (corporate bonds add credit-spread risk, notably RHB's RM33.6b).
  - Hedge accounting on the bond books.
  - PBB CASA and credit cost; CIMB LLC; Stage 2 for all six; 2026-vintage OPR sensitivities.
- **Duration** is calibrated to two broker data points. A ±0.5-year error changes the +100bp CET1 figures by about ±16%, but not the ranking: RHB's lead comes from FVOCI/RWA (32% vs PBB's 14%), not from duration.
- **Context banks** (BIMB, ALLIANCE, AFFIN) are not treasury-adjusted, because no T1 data was pulled. RHB Research puts BIMB (88bp) and ALLIANCE (62bp) among the most sensitive, so their regression residuals are flattering.
- **Bursa announcements** were unreachable. Company websites supplied the T1 statements.
- **Reproduce:** `src/screen/run_screen.sh`. Outputs are in `output/screen/`; v1.0 is preserved in `output/screen/v1.0/`.
