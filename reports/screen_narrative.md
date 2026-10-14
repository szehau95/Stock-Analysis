# Malaysian Banks — Fundamental Value × Technical Upside Screen

**Run date:** 14/10/2026 · **Prices:** close 13/10/2026 (last complete Bursa session; the 14/10 bar was still forming at build time) · **Universe:** core six (Option A: MAYBANK, PBBANK, CIMB, HLBANK, RHBBANK, AMBANK) · **Owner:** Emmanuel Lim Sze Hau · **Not client-facing**

† **HLBANK is an employer-group entity.** It went through the identical framework. Personal dealing is subject to HLB staff trading and blackout rules, so check compliance before acting on any view on HLBANK (HLFG was not screened in this run).

---

## Verdict in one screen

| | Call |
|---|---|
| **Top pick** | **RHBBANK — Overweight.** Medium confidence on the lean; Low confidence on it being *the* pick (it drops to #4 on the technical-tilt re-rank, and it leads HLB by only 1.4 composite points). It is the cheapest bank on every value measure and the yield leader (7.1% NTM). But ROE has faded for three quarters and the chart is broken, so **stage the entry**: a ⅓ starter at RM7.21–7.33 with a stop at RM7.06, and the remaining ⅔ only on a weekly close above RM8.04. |
| **Runner-up** | **HLBANK † — Overweight, Low confidence.** It is the most balanced name (value, quality and technicals all 54) and the only base-case ACTIONABLE BUY. Its value cushion is thin (+2%), and it must reclaim RM21.86. |
| **Avoid** | **AMBANK — Underweight, Low confidence.** It has the weakest quality score (24): CASA −10% YTD, NIM −8bp y/y, the highest GIL and the thinnest coverage, at a P/B 1.3 SD above its 5-year mean. |
| **Value-trap watchlist** | **RHBBANK** (weekly close > RM8.04) and **MAYBANK** (weekly close > RM10.65). CIMB (> RM7.64) is cheap only under a β=1 COE. |
| **Sector** | Fairly valued and technically weak. On latest-quarter ROE with a uniform β, all six banks sit within −6% to +6% of justified value. All six trade below their 200-DMA. Two dated overhangs sit ahead: **late-Nov results** and the **FBM KLCI-50 rebalance on 21/12/2026**, which cuts financials' index weight from ~43% to ~37%. **No name is a clean technical buy on a conservative read, so build positions in stages, not all at once.** |

---

## Variables block (as run)

```
RUN_DATE        = 14/10/2026 (prices: close 13/10/2026)
UNIVERSE        = core six (Option A); BIMB, ALLIANCE, AFFIN used only as P/B–ROE regression context
BENCHMARK       = FBMKLCI (Yahoo ^KLSE). Sector proxy = cap-weighted, dividend-adjusted composite of the core six
                  (the Bursa Financial Services Index is not available in either data feed)
LATEST_QTR      = June-2026 quarter for all six: 2Q26; HLBANK 4QFY26 (FY Jun); AMBANK 1QFY27 (FY Mar)
COE             = MGS10 3.83% (BNM FMIP, 13/10/2026, T1) + β_Blume × 6.0% ERP; β = 3y weekly vs KLCI → 9.1%–11.5% by bank
LT_GROWTH (g)   = 4.0% (sensitivity 3% / 5%)
OPR_CURRENT     = 2.75% (BNM MPS 03/09/2026, T1); next MPC 05/11/2026
TA              = weekly (primary trend, completed weeks to 09/10/2026) + daily (entry); 3–6 month horizon;
                  indicators on dividend-adjusted OHLC
WEIGHTS         = Value 40 · Quality 30 · Technical 30 (sensitivity 60/20/20 and 20/30/50)
OUTPUT          = PLAIN_TEXT; CLIENT_FACING = FALSE
```

---

## Module 1 — Premise validation & data freshness

All six banks last reported the June-2026 quarter, between 18/08 and 28/08/2026. No bank is more than one quarter behind its peers, so the FY misalignment is handled with trailing-four-quarter (T4Q) figures. The next results (3Q26; HLB 1QFY27; AMBANK 2QFY27) are due in late November 2026. Those dates are unconfirmed: aggregator calendars returned nothing and Bursa was unreachable from the build environment. All six clear the RM5m 3M-ADV liquidity floor; HLBANK is the thinnest at RM19.6m.

{{M1_FRESHNESS}}

{{M1_EVENTS}}

*Correction to the interim Module 1 shown in chat:* HLBANK and AMBANK are **not** stale. HLB's 4QFY26 (June quarter) was released on 27/08/2026 and AMBANK's 1QFY27 (June quarter) on 18/08/2026. The ADV figures shown earlier were one-day volumes; the table above uses 63-session averages.

---

## Module 2 — Fundamentals (T4Q, latest quarter, NTM consensus)

NTM EPS blends the current- and next-fiscal-year consensus by time remaining (Yahoo, T3, 14/10/2026). The NTM dividend yield is NTM EPS × the T4Q payout. Core ROE is core T4Q EPS over average book value, using the panel's documented one-off adjustments.

**HLBANK core basis.** Share of associates, mainly the 17.8% Bank of Chengdu (BOCD) stake, was RM1,380m of FY26 PAT of RM4,531m (30%). Stripping it from both earnings *and* equity (carrying value RM10.35b, T3) gives a **core ROE of 10.2% vs 11.2% headline**. The stake is then valued at market (BOCD CNY19.25 × 4.238b shares × 17.8% × CNYMYR 0.6097 = RM8.85b, RM4.32/share). That is RM1.5b below carrying value, which is a latent impairment risk of about RM0.73/share.

{{M2_VALUATION}}

{{M2_PROFIT}}

{{M2_RISK}}

{{M2_TARGETS}}

*Stage 2 loans, non-interest-income share and ROA could not be verified at T1/T2 for the set and are marked UNVERIFIED. The quality score therefore uses GIL alone in its asset-quality slot, consistently for all six. The "CET1 > 13%" figure uses an RWA proxy of 0.55 × total assets and is an estimate. MAYBANK's CET1 buffer uses the pro forma ~14.1% after the RM4.83b Etiqa buyout.*

**Reads**
- **The ROE trajectory splits the group.** MAYBANK (latest quarter 11.7%) and HLB (12.1% headline) are improving. RHB (10.8 → 9.6% over three quarters) and AMBANK (10.3 → 9.7%) are fading. For RHB this matters most: MBSB Research flags a likely miss of its PROGRESS27 target (≥12% ROE by 2027).
- **Funding is the pressure point.** PBB's NIM is at its lowest since 2020 (2.08%, −3bp q/q). AMBANK's CASA fell 10% YTD and its NIM is down 8bp y/y. RHB has the lowest CASA in the group (27.6%).
- **Capital.** RHB (14.8%) and AMBANK (14.82%) have the widest CET1 buffers. HLB, at 12.9%, is below the 13% reference, which is why HLB is flagged in the payout check.

---

## Module 3 — Valuation

**3.1–3.2 Justified P/B and mispricing.** Justified P/B = (core ROE − g)/(COE − g), and fair value = justified P/B × BVPS (plus the BOCD stake at market for HLB). The base case is the one specified in the variables block. The four stress columns change one assumption at a time: a uniform β of 1, the latest quarter's annualised ROE instead of T4Q, both together, and g/COE shifts.

{{M3_JPB}}

**3.3 Cross-sectional P/B vs core ROE.** Across the nine listed banks: **P/B = −0.28 + 13.15 × ROE, R² 0.89** (slope s.e. 1.77). On the core six alone: P/B = −1.37 + 23.3 × ROE, R² 0.86. A negative residual means the bank is cheap relative to its ROE.

{{M3_REG}}

**3.4–3.6 History, dividends and consensus.** P/B z-scores against each bank's own 5-year history are in the Module 2 valuation table.

{{M3_DIV_CONS}}

**Reads**
- **RHB is the only bank that is cheap on all three lenses.** It screens +33% to Gordon fair value, carries the most negative regression residual among the core six (−12.6%), and has the highest yield (7.1%). Its fair value of 1.25× is not a fantasy level: **RHB traded at 1.17× as recently as 10/08/2026** (5-year range 0.74–1.17×). It has de-rated about 20% since, with no adverse disclosure found. The likely drivers are the ROE fade and the capital-management plan slipping to 1Q27 at the earliest; there is no rights issue or M&A (The Star 02/09/2026). **The margin is assumption-sensitive.** It falls to +15.5% at β=1, to +18.7% on latest-quarter ROE, and to +3.0% with both. RHB stays cheapest in three of the four specifications.
- **PBB is rich in every specification:** −13% to Gordon, +12.5% regression residual, and the lowest yield spread (+1.2pp over MGS). You pay 1.48× for the best franchise just as its NIM is at a six-year low.
- **CIMB's valuation is a beta question.** Its 3y β of 1.28 lifts COE to 11.5% and produces −17%; at β=1 it is +6.5%. The regression places it on the line (−2.6%). It is treated as fairly valued.
- **Where our fair value is more than 15% below the consensus median (PBB −26%, CIMB −30%, AMBANK −22%, HLB −16%),** three things explain the gap:
  - Broker targets are 12-month forward, so they embed roughly a year of BV accretion (ROE × retention ≈ 4–5%).
  - Brokers underwrite ROE above T4Q; for example, CGSI has PBB reaching 12.5% by FY28.
  - Our CAPM COE is higher than the 10–11% flat COE brokers typically use for high-β names (CIMB, AMBANK, PBB).

  RHB is the only bank where our fair value sits *above* consensus (+11%, against brokers' RM8.40–9.51 range).
- **Sector level.** Implied COE runs from 9.5% to 10.7% across the six, and implied ERP from 5.0% to 7.9% against the 6.0% assumed. RHB's 7.9% is the highest risk premium in the group. This is consistent with the 30/09 run, where implied ERP sat at its 10-year median. The −26bp MGS rally since 29/09 is already reflected in the COEs used here.

---

## Module 4 — Quality score (0–100, percentile within the core six; UNVERIFIED inputs score 50)

{{M4_QUALITY}}

*"ROE trend" is the slope of the last four quarterly annualised core ROEs. An earlier draft used the change in T4Q ROE over four quarters, which scored RHB's three-quarter fade as the best trend in the group; that was corrected before scoring. HLB's trend uses headline quarterly ROE, because there is no quarterly ex-associate split.*

---

## Module 5 — Technical analysis (weekly primary, daily entry)

Indicators use dividend-adjusted OHLC, because every core bank went ex-dividend inside the 3-month window:
- HLB: 80 sen on 07/10/2026 (−3.6%)
- MAYBANK: 31 sen on 23/09
- CIMB: 19.65 sen on 15/09
- RHB: 15 sen on 14/09
- PBB: 10.5 sen on 10/09

Unadjusted charts overstate the damage. HLB's apparent 33 RSI and "−2.5 ATR below the 20-DMA", for example, were mostly the dividend coming off.

How the levels are built:
- **Structure:** weekly pivots (3y), daily pivots (1y, ±15 sessions), 52-week extremes, high-volume nodes (1y), and the 50/200-DMA and 40-week lines. Levels within 0.6 ATR are clustered.
- **T1:** the first cluster at least 1.5 ATR above price.
- **Stop:** the tighter of (support − 0.25 ATR) and 2 × ATR, never within 1.5 ATR of price.
- **Immediate hurdle:** a heavy cluster (three or more levels) inside 1.5 ATR, which must be reclaimed before T1.

{{M5_TREND}}

*MACD key: ↑/↓ = MACD above/below its signal line; +/− = histogram rising/falling over 3 bars. The regime is classed on the weekly trend: Uptrend needs the weekly close above a rising 40-week MA plus price above the 200-DMA with the 50-DMA above the 200-DMA. Downtrend needs the weekly close below a falling 40-week MA plus price below the 200-DMA. Anything else is Range. On the unadjusted chart, RHB's 50/200 crossed down on 08/10/2026. Adjusted, the 50-DMA (8.05) is still just above the 200-DMA (7.98) and closing fast.*

{{M5_RS}}

{{M5_LEVELS}}

{{M5_SCORE}}

*Technical score weights: trend regime 35, relative strength vs KLCI and sector (3M/6M) 25, momentum (daily and weekly RSI/MACD, ADX direction) 20, R:R 20. Penalties apply for daily RSI > 75 or price > 2 ATR above the 20-DMA; none triggered. The "conservative T1" column re-scores with the immediate hurdle as T1.*

**Reads**
- **All six trade below their 200-DMA.** None has a relative-strength line at a 52-week high, and OBV is falling on all six over 20 days. The sector is in a correction, not a trend.
- **HLB has the best relative strength:** +6.1% vs KLCI over 3M and +5.0% vs the sector, on a golden cross dated 02/09/2026. Its R:R of 2.4 assumes it reclaims the RM21.8–22.1 band (200-DMA, 40-week line and 20/50-DMA). Measured to that band, the R:R is only 0.46.
- **RHB has the weakest tape:** ADX 54 with −DI in control, RSI 32, and −6.9% vs KLCI over 3M. The R:R of 2.2 is real (there is no heavy hurdle before RM7.84), but it is a counter-trend trade with no structural support until RM6.61–6.63.
- **MAYBANK's tape is broken:** death cross on 28/08/2026, −5.0% vs KLCI over 6M, and R:R of 1.0. It is also the largest KLCI weight ahead of the KLCI-50 dilution.

---

## Module 6 — Composite, quadrant and sensitivity

{{M6_VALUE}}

{{M6_COMPOSITE}}

The quadrant map uses Value ≥ 50 = cheap (relative to the core six) and Technical ≥ 50 = constructive (an absolute score).

**Rules and the ruling**
- **Confidence** counts four robustness checks:
  1. Rank within ±1 under 60/20/20.
  2. Rank within ±1 under 20/30/50.
  3. Quadrant unchanged with a β=1 COE.
  4. Quadrant unchanged with the conservative T1.

  4/4 = High, 3/4 = Medium, 2 or fewer = Low.
- **Lean:** Overweight requires a top-2 composite in the ACTIONABLE BUY or VALUE TRAP WATCH quadrant. Underweight requires the AVOID quadrant and a bottom-2 composite. Everything else is Neutral.
- **Does the top pick survive both re-weightings?** **No.** RHB is #1 at 40/30/30 and 60/20/20 and with β=1, but **#4 at 20/30/50**. Per the prompt, the top-pick designation drops one notch, from Medium to **Low**. The Overweight lean stays at Medium (3/4 checks).
- **The conflict and the ruling.** The composite is effectively a tie: RHB 55.4 vs HLB 54.0. The ROE-trend correction alone moved RHB by 3.0 points. I keep the framework's #1:
  - **RHB's value lead is robust in rank** (91 under both COE builds).
  - **HLB's ACTIONABLE BUY status is not robust.** It flips to MOMENTUM HOLD at β=1 and to VALUE TRAP WATCH on the conservative T1, which is why it scores only 2/4.
  - **RHB's expected 12-month total return is materially higher.** To its regression-fit P/B (RM8.36, +15%) plus a 7.1% yield, versus HLB's fair value +2% plus 5.4%.

  The value-trap risk is managed in execution (staged, trigger-gated entry), not by overriding the ranking.

---

## Module 7 — Macro & catalyst overlay

| Date | Catalyst | Direction | Names most affected | vs quant ranking | Tier / source |
|---|---|---|---|---|---|
| 09/10/2026 (done) | **Budget 2027**: SME, housing and investment-led credit support; deficit 3.3% of GDP (from 3.6%); ringgit seen at RM4.07–4.08/USD | + | Sector; SME lenders (RHB, AMBANK) | Supportive, but already in the 12–13/10 bank-led rebound | T2: Malay Mail 12/10, NST, The Star 09/10 |
| 13/10/2026 (done) | **MGS 10Y 3.83%**, −26bp since 29/09; 3Y 3.43% still 68bp above OPR | + for COE / − if it signals cuts | High-P/B names gain most from lower COE (PBB, MAYBANK) | Already in the COE; does not change ranks | T1: BNM FMIP |
| 05/11/2026 | **BNM MPC**: hold at 2.75% expected (14th month; Bank Muamalat, RHB IB see no change into 1H27) | Neutral; a surprise cut is − NIM | PBB, RHB (−3 to −4bp NIM per 25bp, 2025 estimate) | A cut would deepen the PBB Underweight and test RHB's thesis | T1: BNM MPS 03/09; T2: NST, The Sun |
| Late Nov 2026 | **3Q26 / HLB 1QFY27 / AMBANK 2QFY27 results** | ± | RHB (does ROE stop fading?), MAYBANK (post-Etiqa CET1, DRP), PBB (NIM), AMBANK (CASA) | **The key confirmation event for the top pick** | T2: prior-year timing |
| 21/12/2026 and 21/06/2027 | **FBM KLCI expands to 50 names**; financials' weight ~43% → ~37% (HLIB/CIMB simulations); new entrants phased 50/50 | − (passive selling) | Largest KLCI weights: MAYBANK, PBB, CIMB | Reinforces staged entries and the MAYBANK wait | T2: The Star 21/08, BusinessToday 03/04, Kenanga 16/04 |
| 1Q27 at the earliest | **RHB capital-management framework**: 50–60% payout guidance; possible +100bp CET1 uplift from Basel III reforms | + | RHB | **Reinforces the RHB Overweight** (excess CET1 ~RM3.8b est.) | T2: The Star 02/09 (HLIB, MBSB, Kenanga, BIMB) |
| Ongoing | **Foreign flows**: net selling resumed (−RM473m in the week to ~25/09, MBSB Research); local institutions buying | − | High-foreign-ownership names (CIMB, PBB, MAYBANK) | Neutral to ranks; argues for patience | T2: BusinessToday 28/09 |
| Ongoing | Bank-specific | | | | |
| | MAYBANK: Etiqa buyout (CET1 ~−0.8pp pro forma), 2026 DRP dilution, RM2.6b overlays as a buffer | − / + | MAYBANK | Reinforces Neutral until the flip trigger | T2: The Edge, The Star (prior run) |
| | HLB: BOCD at 0.88× book, RM1.5b below carrying value; CNY and China-bank sentiment drive 30% of PAT | − | HLB † | Reinforces Low confidence | T1: HLFG deck; T3: Yahoo |
| | CIMB: FY26 NIM guide cut to flat/−10bp; credit cost at the top of the 25–35bp range | − | CIMB | Reinforces Neutral | T1 release; T3 Quartr |
| | AMBANK: CASA −10% YTD; 2QFY27 interim dividend in November | − / + | AMBANK | Reinforces Underweight | T1: AmBank release |

**Ruling.** The overlay *reinforces* the quant ranking and argues for staging entries over the next 10 weeks rather than buying now:
- The two dated negatives are both still ahead: results in late November and the KLCI-50 rebalance on 21/12.
- The two positives that matter for the top pick are company-specific and slow. RHB's capital plan (1Q27) and a stop in its ROE fade (3Q26 print) are not priced as near-term certainties.
- Nothing in the overlay contradicts a rank. The one swing factor is an unexpected OPR cut on 05/11, which would hurt PBB most and RHB second.

---

## Module 8 — Verdict

### 8.1 Ranked scorecard (all six)

{{M8_SCORECARD}}

*Trend is the weekly-regime label; RSI is daily. Upside, stop and R:R are from the Module 5 levels table. Fair P/B is justified P/B at base COE and g = 4%. HLB's P/B, fair P/B and mispricing are on the ex-associate core basis (headline P/B 1.05×).*

### 8.2 Top pick — RHBBANK (Overweight · lean confidence Medium · top-pick designation Low)

- **Value:**
  - Cheapest bank in the core six. P/B 0.94× vs justified 1.25×, fair value RM9.72 (+33%); +15–19% under single stresses, +3% with both.
  - Most negative P/B–ROE residual among the core six (−12.6%; regression-fit price RM8.36).
  - Highest NTM yield, 7.1% (+3.2pp over MGS).
  - It traded at 1.17× two months ago, and the consensus median of RM8.73 is +20%.
- **Quality, the weak leg:**
  - Weak: 4Q ROE path 10.8 → 9.6%, lowest CASA (27.6%), quality score 33.
  - Offsetting: CET1 14.8% (~RM3.8b above 13%, est.), credit cost on guidance (13bp), loans +7% y/y, CIR improving to 46.8%, LLC 115% including regulatory reserves.
  - Upside catalyst: the 1Q27 capital-management framework (50–60% payout, possible +100bp CET1 from Basel III reforms).
- **Technical:** a counter-trend setup with defined risk. RSI 32, price 2.2 ATR below the 20-DMA. There is no heavy resistance before RM7.84, so the 2.2 R:R is clean, but ADX 54 says the selling has not exhausted.
- **Execution:**
  - **Starter (⅓):** entry zone RM7.21–7.33, stop RM7.06 on a daily close (−3.3%). T1 RM7.84 (+7.3%), T2 RM8.13 (+11.4%).
  - **Add (⅔):** only on a weekly close > RM8.04, the 40-week/200-DMA band. Post-flip stop RM7.86, T1 RM8.24, T2 RM8.77. Value anchors: RM8.36 (regression) and RM9.72 (Gordon).
- **Invalidation:**
  - Daily close < RM7.06: exit the starter. The next structure is RM6.61–6.63, the 52-week-low zone.
  - 3Q26 annualised core ROE < 9.5% (a fourth straight decline) or NIM < 1.80%.
  - A capital plan with no payout uplift or buyback.
  - CET1 < 14%.
  - Any rights issue or M&A disclosure.

### 8.3 Runner-up — HLBANK † (Overweight, Low confidence)

- **For:**
  - The only name with value, quality and technicals all at or above 50 (54/54/54), and the only base-case ACTIONABLE BUY.
  - Best asset quality: GIL 0.57%, LLC 244% including regulatory reserves, credit cost ~4bp.
  - ROE is rising; P/B is −1.3 SD vs its 5-year history.
  - Outperforming the KLCI by +6% over 3M.
  - Levels: entry RM21.20–21.59, stop RM20.66, **reclaim RM21.86 first**, then T1 RM23.41 and T2 RM24.58.
- **Against:**
  - The value cushion is thin: +2% (−3% at β=1) on a 10.2% ex-Chengdu core ROE.
  - CET1 of 12.9% is below the 13% reference.
  - The BOCD stake is marked RM1.5b below carrying value.
  - † Employer-group: check HLB staff dealing and blackout rules before acting, especially into the late-November 1QFY27 results.

### 8.4 Avoid — AMBANK (Underweight, Low confidence)

- **Weakest quality in the set (24/100):**
  - ROE fading (10.3 → 9.7%).
  - NIM −8bp y/y to 1.93%.
  - CASA balances −10% YTD (RM46.9b; a 32.5% mix).
  - Highest GIL (1.62%) and thinnest coverage (102.5% including regulatory reserves).
- **No valuation cushion:**
  - P/B 0.97× is +1.26 SD above its 5-year mean (re-rated from 0.63× in 2023).
  - Fair value −3.5% (−9% on latest-quarter ROE).
  - R:R 0.85.
- Confidence is Low only because a β=1 COE makes it screen cheap (+6.6%). The fundamentals do not support chasing that.

**Also Underweight: PBBANK (Medium confidence).** It is the highest-quality bank (74), but it is rich in every specification: −13% to fair value, a +12.5% regression residual, and a 5.1% yield (+1.2pp over MGS). Its NIM is at a six-year low and it is the most OPR-sensitive. Buy the franchise lower; RM4.09 is our fair value.

### 8.5 Value-trap watchlist (cheap, technically broken)

| Bank | Why cheap | Why broken | Flip-to-buy trigger | Then: stop / T1 / T2 |
|---|---|---|---|---|
| **RHBBANK** (top pick) | Value 91 under both COE builds | ADX 54 (−DI), RS −6.9% 3M, below the 50/200-DMA and 40W | **Weekly close > RM8.04** | 7.86 / 8.24 / 8.77 |
| **MAYBANK** | +9% fair value (+17% on latest-quarter ROE); ROE improving (11.7% latest quarter); quality #2 | Death cross 28/08/2026, RS −5% 6M, R:R 1.0; largest weight into the KLCI-50 rebalance | **Weekly close > RM10.65** | 10.48 / 11.02 / 11.71 |
| *CIMB (conditional)* | Cheap only with a β=1 COE (+6.5%) | Weekly "Downtrend", below the 40W | Weekly close > RM7.64 | 7.42 / 7.93 / 8.51 |

### 8.6 Key risks to the sector call (ranked by probability × impact)

1. **KLCI-50 passive selling into 21/12/2026** (high probability, medium impact). Financials' index weight drops ~6pp. MAYBANK, PBB and CIMB are hit hardest; this is why MAYBANK stays on the watchlist.
2. **NIM squeeze from deposit competition or an OPR cut** (medium-high probability, medium impact). PBB's NIM is at a six-year low, AMBANK is −8bp y/y and RHB has the weakest CASA. The MGS rally hints at easing expectations even though the 3Y still sits above OPR.
3. **Asset-quality mean reversion from Middle East, oil or tariff stress on SMEs** (medium probability, high impact). GILs are at or near record lows (CIMB 1.6% all-time low, PBB 0.54%, HLB 0.57%). Overlays such as MAYBANK's RM2.6b buffer some of it. RHB and AMBANK have the most SME sensitivity.
4. **Persistent foreign outflows or a ringgit reversal** (medium probability, medium impact). Net selling resumed in late September. Budget 2027 and the firmer ringgit are the offset.

### 8.7 Sources

| # | Source | Tier | As of |
|---|---|---|---|
| 1 | BNM Monetary Policy Statement (OPR 2.75% held) — bnm.gov.my | T1 | 03/09/2026 |
| 2 | BNM FMIP benchmark MGS yields (10Y 3.83%, 3Y 3.43%) — financialmarkets.bnm.gov.my | T1 | 13/10/2026 |
| 3 | BNM 2026 MPC schedule (6th meeting 05/11/2026) — via bnm.gov.my MPS 06/11/2025 | T1 | 06/11/2025 |
| 4 | RHB Bank news release, 1H FY2026 (CET1, GIL, LLC, CASA, LCR, loans, NAV) — rhbgroup.com | T1 | 28/08/2026 |
| 5 | Hong Leong Bank FY2026 results release — hlb.com.my | T1 | 27/08/2026 |
| 6 | HLFG FY2026 analyst presentation (HLB P&L incl. associates RM1,380m; BOCD 17.8%; ROE; credit cost) — hlfg.com.my | T1 | 08/2026 |
| 7 | AmBank Group Q1FY27 results release — ambankgroup.com | T1 | 18/08/2026 |
| 8 | CIMB 2Q26 results release (ROE 11.2%, CIR 45.2%, GIL 1.6%, CET1 14.0%) — cimb.com | T1 | 28/08/2026 |
| 9 | Kenanga, Maybank 2Q26 results note (CET1, CASA, GIL, LLC, credit cost, guidance) | T2 | 28/08/2026 |
| 10 | The Asian Banker, Maybank 2Q26; CIMB 2Q26 earnings-call transcript | T2 | 08/2026 |
| 11 | The Edge (node/815772, 815919): PBB 2Q26 NIM 2.08%, CET1 13.9%, LLC 138.9%; HLIB/CGSI views | T2 | 26–27/08/2026 |
| 12 | Malay Mail / The Star: PBB 2Q26 (GIL 0.54%, loans +5.9% annualised) | T2 | 26/08/2026 |
| 13 | The Star, "Capital management plan to bolster RHB Bank" (HLIB, MBSB, BIMB, Kenanga) | T2 | 02/09/2026 |
| 14 | Kenanga RHB 4Q25 note (FY26 credit cost 13–14bp, loans 5–6%) | T2 | 02/03/2026 |
| 15 | TA Research, PBB 1Q26 (loans 4–5%, single-digit credit cost guidance) | T2 | 15/05/2026 |
| 16 | The Star / BusinessToday / Kenanga: FBM KLCI-50 (effective 21/12/2026 and 21/06/2027; financials ~43% → ~37%) | T2 | 03/04–21/08/2026 |
| 17 | Malay Mail, NST, The Star, Bernama: Budget 2027 reactions | T2 | 09–12/10/2026 |
| 18 | NST (OPR hold, 5.7% 1H GDP); The Sun (RHB IB OPR view) | T2 | 09/2026 |
| 19 | BusinessToday (MBSB Research weekly fund flow, −RM473m) | T2 | 28/09/2026 |
| 20 | The Edge via Maybank IB: NIM sensitivity per 25bp OPR cut (2025 vintage) | T2 | 2025 |
| 21 | The Edge node/813262, The Star 03/08 and 31/08/2026: Etiqa buyout, Maybank overlays and DRP (30/09 run source log) | T2 | 08/2026 |
| 22 | Yahoo Finance: OHLCV and dividends to 13/10/2026; consensus EPS, revisions, targets, recommendations (14/10/2026); Jun-26 balance sheets (TBV, HLB associate carrying value) | T3 | 13–14/10/2026 |
| 23 | Yahoo Finance: Bank of Chengdu (601838.SS) price, shares, P/B; CNYMYR | T3 | 13–14/10/2026 |
| 24 | TradingView MY10Y (cross-check of #2); analyst rating split (MAYBANK consensus EPS and targets rejected: USD-denominated figures labelled MYR) | T3 | 14/10/2026 |
| 25 | klsescreener transcription of Bursa quarterly reports (point-in-time panels, core-EPS adjustments) — 30/09 run | T3 → reconciled to T1 headlines | 30/09/2026 |
| 26 | Quartr CIMB 2Q26 summary (revised NIM guidance only) | T3 | 08/2026 |

### 8.8 Data gaps and method notes

- **UNVERIFIED, would change scores if filled:** PBB CASA and credit cost; CIMB LLC and y/y loan growth; Stage 2 for all six; HLB FY27 guidance; 2026-vintage OPR sensitivities. Missing quality inputs score 50 (neutral).
- **Bursa announcements were not reachable** from the build environment. Results dates and figures come from company releases (T1) or press and broker coverage (T2), as tagged.
- **The core-ROE adjustments come from the 30/09 run** (no one-offs fall in this T4Q window). HLB is additionally stripped of associates.
- **The HLB associate carrying value is T3** (Yahoo, Jun-26). The FY26 share of profit is T1.
- Prices are Yahoo closes (T3). They were cross-checked against a TradingView snapshot on 14/10, where intraday differences were ≤ 1%.
- Reproduce with `src/screen/run_screen.sh`. Outputs are in `output/screen/`.
