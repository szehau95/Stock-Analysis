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

| Bank | Mispricing v1.0 | v1.1 | Quality v1.0 → v1.1 | Composite v1.0 | Composite v1.1 | Lean v1.0 | Lean v1.1 |  |
|---|---|---|---|---|---|---|---|---|
| RHBBANK | +33% | +32% | 33 → 30 | 55.4 (#1) | 54.4 (#1) | Overweight (Medium) | **Neutral (High)** | was top pick |
| HLBANK † | +2% | +2% | 54 → 54 | 54.0 (#2) | 54.2 (#2) | Overweight (Low) | **Overweight (Medium)** | TOP PICK |
| MAYBANK | +9% | +8% | 61 → 53 | 49.4 (#3) | 47.1 (#3) | Neutral (Low) | **Neutral (Medium)** |  |
| PBBANK | -13% | -13% | 74 → 78 | 42.2 (#5) | 43.5 (#4) | Underweight (Medium) | **Neutral (Low)** |  |
| CIMB | -17% | -18% | 55 → 55 | 42.7 (#4) | 42.8 (#5) | Neutral (Medium) | **Underweight (Low)** |  |
| AMBANK | -3% | -4% | 24 → 29 | 37.0 (#6) | 38.7 (#6) | Underweight (Low) | **Underweight (Low)** |  |

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

| Bank | Code | Latest Q | Q end | Announced | Days to 13/10 | Next results | Close 13/10 (RM) | Mkt cap (RM bn) | 52W H / L | 3M ADV (RM m) | Liquidity |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 1155 | 2Q26 | 30/06/2026 | 27/08/2026 | 47 | late-Nov-2026 (unconfirmed) | 9.96 | 120.5 | 12.42 / 9.78 | 163.0 | Actionable |
| PBBANK | 1295 | 2Q26 | 30/06/2026 | 26/08/2026 | 48 | late-Nov-2026 (unconfirmed) | 4.70 | 91.2 | 5.29 / 4.18 | 112.7 | Actionable |
| CIMB | 1023 | 2Q26 | 30/06/2026 | 28/08/2026 | 46 | late-Nov-2026 (unconfirmed) | 7.50 | 80.7 | 8.95 / 7.19 | 90.0 | Actionable |
| HLBANK † | 5819 | 4QFY26 (FY Jun-26) | 30/06/2026 | 27/08/2026 | 47 | late-Nov-2026 (unconfirmed) | 21.48 | 44.0 | 25.80 / 20.26 | 19.6 | Actionable |
| RHBBANK | 1066 | 2Q26 | 30/06/2026 | 28/08/2026 | 46 | late-Nov-2026 (unconfirmed) | 7.30 | 31.9 | 8.94 / 6.63 | 65.6 | Actionable |
| AMBANK | 1015 | 1QFY27 (FY Mar-27) | 30/06/2026 | 18/08/2026 | 56 | late-Nov-2026 (unconfirmed) | 6.27 | 20.8 | 7.37 / 5.61 | 42.7 | Actionable |

| Bank | Corporate events / distortions (Module 1.4) |
|---|---|
| MAYBANK | Etiqa buyout RM4.83b (CET1 ~-0.8pp pro forma to ~14.1%); 2026 DRP; overlays RM2.6b at 1H26 (+RM0.3b) |
| PBBANK | Capital management initiatives flagged by CGSI; 1H profit missed some estimates |
| CIMB | Loans +1.1% QoQ (constant ccy); GIL all-time low |
| HLBANK † | Associates (mainly 17.8% Bank of Chengdu) = RM1,380m of RM4,531m FY26 PAT; BOCD CBond dilution FY25; DPS 110 sen |
| RHBBANK | Capital management plan due early 2027 (T2); NAV/share RM7.81 |
| AMBANK | CASA -10.0% YTD to RM46.9b (ratio derived 46.9/144.1); CET1 14.40% excl. unaudited Q1 profit |

**Additional events found in the v1.1 sweep:**
- **PBB:** privatising its 73.23%-owned Hong Kong unit PFHL at HK$2.50/share (~RM379m, <1% of equity, about −13bp CET1 at bank level per RHB Research; long-stop 08/03/2027). Brokers call it neutral.
- **CIMB:** reportedly weighing a sale of its Philippine operations (up to USD200m), alongside a plan to return up to RM2b of extra capital by 2027 (T3, aggregator).

### Module 1.5 — Broker-action sweep (last ~60 days)

| Date | Bank | House | Action | Rating / TP | Stated reason | Factor in model | Tier |
|---|---|---|---|---|---|---|---|
| ~07/10/2026 | CIMB | JPMorgan | Downgrade | Underweight | 3Q26 surprises likely skewed negative for quite a few banks; sell-off attributed by dealers to rising long-term yields | treasury_mtm;results_risk | T2 |
| 01/10/2026 | CIMB | MBSB Research | TP cut | RM9.29 → RM9.20 (Buy) | Trim | results_risk | T3 |
| ~07/10/2026 | AMBANK | JPMorgan | Downgrade | Neutral | 3Q26 surprises skewed negative | treasury_mtm;results_risk | T2 |
| 05/10/2026 | RHBBANK | HLIB | Rating/TP | Buy RM9.50 (The Star 02/09/2026) → Hold RM8.00 | Higher MGS yields weigh on 3Q26 trading income/NOII; ROE likely at low end of 10.8-11.0% target | treasury_mtm;results_risk;roe_fade | T2 |
| 11/09/2026 | SECTOR | RHB Research | Sector downgrade | Overweight → Neutral | Valuations; funding pressure; early asset-quality stress | sector | T2 |
| 06/10/2026 | SECTOR | RHB Research | Sensitivity note | – | +100bp yields: sector CET1 -46bp, ~RM8b MTM; top picks AMMB, MAYBANK, HLBANK | treasury_mtm | T2 |
| 01/10/2026 | SECTOR | Affin Hwang IB | Sensitivity note | – | Largest capital-ratio drops MAYBANK, RHB, CIMB; least PBB, HLB (shortest duration) | treasury_mtm | T2 |
| 09/09/2026 | PBBANK | Maybank IB | Maintain | Buy RM5.50 | PFHL privatisation (RM379m) neutral | corporate_event | T2 |

**Reads.** Every recent negative action cites the same driver: rising bond yields hitting trading income and capital (3Q26 surprises "skewed negative"). That is a factor reported numbers do not yet show, and Module 2b now quantifies it. On 07/10 CIMB fell 4.8%, AMBANK 4.5%, RHB 2.4%, PBB 1.7% and MAYBANK 1.0%. HLB's −2.6% that day was its 80-sen ex-dividend date (−3.6% mechanically), so ex-dividend it rose.

---

## Module 2 — Fundamentals (T4Q, latest quarter, NTM consensus)

Book values below are **treasury-adjusted**: June BV, less the after-tax FVOCI mark from 30/06 to 13/10 (Module 2b). HLBANK's core basis strips Bank of Chengdu from earnings *and* equity:
- **ROE:** core 10.2% vs 11.2% headline.
- **Associates' share:** RM1,380m of RM4,531m FY26 PAT.
- **The stake:** carrying value RM10.35b vs market value RM8.85b. It is valued at market (RM4.32/share).

| Bank | P/B | P/B 5Y mean (±1SD) | P/B z (5Y) | P/TBV | P/E T4Q core | P/E NTM | EY NTM | DY T4Q | DY NTM |
|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 1.30 | 1.28 (1.19–1.37) | +0.14 | 1.39 | 11.5 | 10.9 | 9.2% | 6.4% | 6.8% |
| PBBANK | 1.49 | 1.59 (1.46–1.72) | -0.84 | 1.56 | 12.4 | 11.8 | 8.5% | 4.8% | 5.1% |
| CIMB | 1.16 | 1.05 (0.90–1.20) | +0.70 | 1.30 | 10.3 | 9.6 | 10.4% | 6.3% | 6.7% |
| HLBANK † | 1.06 | 1.20 (1.09–1.32) | -1.29 | 1.11 | 9.7 | 9.2 | 10.8% | 5.1% | 5.4% |
| RHBBANK | 0.94 | 0.88 (0.78–0.97) | +0.61 | 1.04 | 9.2 | 8.9 | 11.3% | 6.8% | 7.1% |
| AMBANK | 0.98 | 0.81 (0.69–0.94) | +1.26 | 0.99 | 9.9 | 9.4 | 10.7% | 5.6% | 5.9% |

| Bank | Core ROE T4Q (headline basis) | Core ROE ranked | Latest Q ann. | Last 4Q ROE path (%) | 4Q slope /qtr | NIM | CIR | Loan growth y/y | CASA | FY+1 EPS rev. 3M |
|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 11.2% | = | 11.7% | 11.2 → 11.5 → 10.8 → 11.7 | +0.08pp | 2.1% (10.0bp y/y) | 49.1% | 2.7% | 41.5% | -0.6% |
| PBBANK | 12.2% | = | 12.1% | 12.6 → 12.7 → 11.8 → 12.1 | -0.25pp | 2.08% (UNVERIFIED y/y) | 35.1% | 5.9% | UNVERIFIED | -0.4% |
| CIMB | 11.2% | = | 11.2% | 11.8 → 10.9 → 11.0 → 11.2 | -0.19pp | 2.04% (UNVERIFIED y/y) | 45.2% | UNVERIFIED | 42.6% | -1.6% |
| HLBANK † | 11.2% | 10.2% | 12.1% | 11.2 → 11.9 → 10.3 → 12.1 | +0.13pp | 1.84% (-6.0bp y/y) | 37.6% | 7.7% | 34.7% | -0.3% |
| RHBBANK | 10.3% | = | 9.6% | 10.8 → 10.7 → 10.2 → 9.6 | -0.40pp | 1.86% (-2.0bp y/y) | 46.8% | 7.0% | 27.6% | -1.1% |
| AMBANK | 10.0% | = | 9.7% | 10.3 → 10.0 → 9.7 → 9.7 | -0.21pp | 1.93% (-8.0bp y/y) | 43.4% | 7.0% | 32.5% | +0.0% |

| Bank | GIL | Stage 2 | Credit cost | LLC (basis) | CET1 reported | CET1 adj. (FVOCI to 13/10) | TCR | LCR | Payout T4Q | CET1 >13% (RM bn, T1 RWA) | Payout vs CET1 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 1.35% | UNVERIFIED | 20bp | 103.1% (basis not stated) | 14.92% | 13.69% (incl. Etiqa −1.10pp) | 18.68% | 130% | 74% | 3.0 | ok |
| PBBANK | 0.54% | UNVERIFIED | UNVERIFIED | 138.9% (basis not stated) | 13.9% | 13.84% | 16.5% | UNVERIFIED | 60% | 3.2 | ok |
| CIMB | 1.6% | UNVERIFIED | 34bp | UNVERIFIED (n/a) | 14.0% | 13.88% | UNVERIFIED | UNVERIFIED | 65% | 3.4 | ok |
| HLBANK † | 0.57% | UNVERIFIED | 4bp | 244.1% (incl. regulatory reserve (79.5% excl.)) | 12.9% | 12.84% | 16.2% | 127.0% | 50% | -0.3 | WATCH: CET1 below 13% ref |
| RHBBANK | 1.47% | UNVERIFIED | 13bp | 115.4% (incl. regulatory reserve) | 14.8% | 14.72% | 17.1% | 138.3% | 63% | 3.1 | ok |
| AMBANK | 1.62% | UNVERIFIED | 19bp | 102.5% (incl. regulatory reserve) | 14.82% | 14.75% | 17.31% | 143.9% | 55% | 2.2 | ok |

| Bank | FY guidance (mgmt) | YTD vs guidance | NIM per 25bp OPR cut (bp) | KPI tier |
|---|---|---|---|---|
| MAYBANK | FY26: ROE>=11.8%, loans 4-5%, NIM 2.05-2.10%, NCC ~20bps, CIR ~49% | ROE behind (11.6 vs >=11.8); NIM/NCC/CIR on track; loans behind (2.7 vs 4-5) | 2-3 (sector avg; ~70% variable-rate) | T2 |
| PBBANK | FY26: loans 4-5%, credit cost single-digit bps | Loans ahead (5.9 annualised vs 4-5); NIM -3bp QoQ to 2.08% (lowest since 2020) | 3-4 (Maybank IB 2025) | T2 |
| CIMB | FY26: ROE 11.0-11.5%, CIR <47%, credit cost 25-35bps, CET1 >=14.0%, NIM flat to -10bps (revised, T3) | ROE on track (11.2); CIR ahead (45.2); credit cost at top of range (34 1H ann.; 38 in 2Q); CET1 at floor (14.0) | UNVERIFIED (sector 2-4) | T1 |
| HLBANK † | FY26 loans 6-7% (Kenanga 28/05/2026); FY27 targets not disclosed | FY26 loans ahead (7.7 vs 6-7); FY27 UNVERIFIED | UNVERIFIED (sector 2-4) | T1 |
| RHBBANK | FY26: credit cost 13-14bps, loans 5-6% | Credit cost on track (13 vs 13-14); loans ahead (7.0 YoY) | 3-4 (Maybank IB 2025) | T1 |
| AMBANK | FY27 numeric targets not disclosed; FY26 ROE ~10% | ROE behind FY26 run-rate (9.7 vs ~10) | UNVERIFIED (sector 2-4) | T1 |

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

| Bank | FVOCI debt (RM bn) | Amortised cost (RM bn) | FVTPL (RM bn) | Group RWA (RM bn) | FVOCI reserve (RM bn) | FVOCI / RWA | FVOCI / equity | Effective duration | Duration basis |
|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 57.1 | 31.0 | 7.4 | 177.4 | 0.44 | 32.2% | 1.68× | 3.0y | calibrated sector mean |
| AMBANK | 32.9 | 11.2 | 12.4 | 123.0 | 0.77 | 26.7% | 1.53× | 3.0y | calibrated sector mean |
| MAYBANK | 113.9 | 93.7 | 46.0 | 440.5 | UNVERIFIED (0 assumed) | 25.9% | 1.22× | 2.9y | calibrated (RHB Research) |
| CIMB | 83.7 | 82.2 | 66.7 | 389.8 | UNVERIFIED (0 assumed) | 21.5% | 1.20× | 3.2y | calibrated (RHB Research) |
| HLBANK † | 37.2 | 25.1 | 7.3 | 195.6 | 0.10 | 19.0% | 0.89× | 2.4y | 0.8x calibrated (shortest, T2) |
| PBBANK | 52.5 | 32.0 | 4.0 | 380.0 | UNVERIFIED (0 assumed) | 13.8% | 0.85× | 2.4y | 0.8x calibrated (shortest, T2) |

| Bank | CET1: Q3 (+36bp) | CET1: peak 2026-09-11 (+49bp) | CET1: to 13/10 (+24bp) | BV/share marked to 13/10 | CET1: further +100bp | BV: further +100bp | 3Q26 FVTPL hit, % of 2Q PBT (unhedged max) | … % of FY26e profit |
|---|---|---|---|---|---|---|---|---|
| RHBBANK | −14bp | −23bp | −8bp | −0.073 (0.9%) | **−61bp** | −3.9% | 2.2% | 0.5% |
| MAYBANK | −21bp | −28bp | −14bp | −0.050 (0.6%) | **−57bp** | −2.7% | 4.0% | 1.0% |
| CIMB | −19bp | −26bp | −12bp | −0.045 (0.7%) | **−52bp** | −2.9% | 8.0% | 2.0% |
| HLBANK † | −10bp | −15bp | −6bp | −0.081 (0.4%) | **−32bp** | −1.6% | 1.4% | 0.4% |
| AMBANK | −10bp | −14bp | −7bp | −0.055 (0.9%) | **−28bp** | −3.5% | 5.6% | 1.4% |
| PBBANK | −9bp | −13bp | −6bp | −0.012 (0.4%) | **−26bp** | −1.6% | 0.5% | 0.1% |

**Reads**
- **You were right about RHB and CIMB, and RHB is the extreme case.** RHB has the largest bond book relative to its capital: FVOCI is 32% of RWA and 1.68× equity. Its FVOCI reserve was only RM0.44b at June, down from RM0.68b in December. It is therefore the most exposed to a *further* yield rise: −61bp CET1 and −3.9% book value per +100bp. CIMB is third on CET1 sensitivity (−52bp), has the largest trading book (RM66.7b FVTPL; RM46.3b of it government debt), and carries the biggest 3Q26 trading-income risk (up to ~8% of quarterly PBT, unhedged). MAYBANK (−57bp) completes the exposed trio, matching Affin Hwang's ranking.
- **The damage already done is small.** Half the Q3 spike has reversed. Marked to 13/10, book values are 0.4–0.9% lower and CET1s 6–14bp lower. Even at the 11/09 peak, no bank lost more than 28bp of CET1, and the 3Q26 FVTPL hit is ≤2% of FY profit. That supports HLIB's "foregone upside, not losses" read for RHB.
- **So the factor works through forward risk and news flow, not current value.**
  - **Forward risk:** a Fed in hiking mode, UST at a 24-year high and BNM hike odds mean another +50–100bp is a live scenario. On a +100bp move, RHB loses 2.4× the CET1 that PBB does.
  - **News flow:** 3Q26 will print the Q3 marks and the trading-income dip, and brokers have already downgraded the exposed names.
- **AMBANK is the exception on capital.** Its RM0.77b FVOCI reserve absorbs the mark at 45%, so its CET1 sensitivity is low (−28bp). Its book-value sensitivity is still high (−3.5%), and its FVTPL is the second largest relative to profit, hence JPMorgan's downgrade.

---

## Module 3 — Valuation (on treasury-adjusted book value)

| Bank | β raw / Blume | COE | Core ROE | Justified P/B | Actual P/B (core) | BVPS (core) | Fair value | Mispricing | … at β=1 | … on latest-Q ROE | … latest-Q ROE & β=1 | FV g=3% / 5% | FV COE +50bp / −50bp | Implied COE | Implied ERP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 0.82 / 0.88 | 9.1% | 11.2% | 1.41 | 1.30 | 7.64 | 10.79 | +8.3% | -5.4% | +16.5% | +1.7% | 10.27 / 11.55 | 9.82 / 11.96 | 9.5% | 6.5% |
| PBBANK | 1.13 / 1.08 | 10.3% | 12.2% | 1.29 | 1.49 | 3.16 | 4.08 | -13.3% | -5.7% | -14.1% | -6.6% | 3.95 / 4.25 | 3.78 / 4.43 | 9.5% | 5.2% |
| CIMB | 1.42 / 1.28 | 11.5% | 11.2% | 0.95 | 1.16 | 6.46 | 6.15 | -18.0% | +5.8% | -18.1% | +5.6% | 6.19 / 6.10 | 5.77 / 6.59 | 10.2% | 4.9% |
| HLBANK † | 0.90 / 0.93 | 9.4% | 10.2% | 1.15 | 1.13 | 15.25 | 21.84 | +1.7% | -3.8% | +1.7% | -3.8% | 21.49 / 22.36 | 20.37 / 23.62 | 9.5% | 6.1% |
| RHBBANK | 0.81 / 0.87 | 9.1% | 10.3% | 1.25 | 0.94 | 7.73 | 9.63 | +31.9% | +14.5% | +17.6% | +2.1% | 9.32 / 10.10 | 8.76 / 10.68 | 10.7% | 7.9% |
| AMBANK | 1.15 / 1.10 | 10.4% | 10.0% | 0.93 | 0.98 | 6.42 | 6.00 | -4.3% | +5.7% | -9.9% | -0.4% | 6.06 / 5.92 | 5.57 / 6.50 | 10.2% | 5.7% |

**P/B vs core ROE, nine listed banks:** P/B = −0.29 + 13.26 × ROE, **R² 0.89** (slope s.e. 1.77). Core six only: −1.36 + 23.26 × ROE, R² 0.87.

| Bank | Set | Core ROE | P/B (core) | Fitted P/B | Residual (9-bank fit) | Residual (core-6 fit) | Read |
|---|---|---|---|---|---|---|---|
| ALLIANCE | context | 10.0% | 0.89 | 1.03 | -14.3% | – | cheap |
| RHBBANK | core | 10.3% | 0.94 | 1.08 | -12.3% | -9.1% | cheap |
| BIMB | context | 7.0% | 0.56 | 0.63 | -11.0% | – | cheap |
| AMBANK | core | 10.0% | 0.98 | 1.04 | -6.0% | +0.4% | cheap |
| CIMB | core | 11.2% | 1.16 | 1.19 | -2.5% | -6.3% | on line |
| HLBANK † | core | 10.2% | 1.13 | 1.07 | +5.2% | +9.7% | rich |
| MAYBANK | core | 11.2% | 1.30 | 1.19 | +9.2% | +4.7% | rich |
| PBBANK | core | 12.2% | 1.49 | 1.33 | +12.3% | +0.8% | rich |
| AFFIN | context | 4.4% | 0.41 | 0.29 | +38.9% | – | rich |

| Bank | DY NTM | Spread vs MGS10 3.83% | Payout | Cons. TP median | # analysts | Buy/Hold/Sell | Our FV | FV vs cons. | >15% gap |
|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 6.8% | +3.0pp | 74% | 11.54 | 18 | 9/8/0 | 10.79 | -6.5% | no |
| PBBANK | 5.1% | +1.2pp | 60% | 5.54 | 18 | 10/7/0 | 4.08 | -26.3% | YES |
| CIMB | 6.7% | +2.9pp | 65% | 8.90 | 16 | 13/4/1 | 6.15 | -30.9% | YES |
| HLBANK † | 5.4% | +1.6pp | 50% | 26.07 | 14 | 12/3/0 | 21.84 | -16.2% | YES |
| RHBBANK | 7.1% | +3.2pp | 63% | 8.73 | 15 | 6/9/0 | 9.63 | +10.3% | no |
| AMBANK | 5.9% | +2.0pp | 55% | 7.72 | 15 | 12/4/0 | 6.00 | -22.3% | YES |

**Reads**
- **The bond mark barely moves fair values** (≤1.2 points of mispricing). RHB stays the cheapest bank: +32% to Gordon value, −12% regression residual, 7.1% yield. Its realistic re-rating anchor is the regression-fit price of **RM8.32** (+14%), and Gordon value is RM9.63.
- **But part of RHB's discount is now explained.** Its implied ERP is 7.9%, against 4.9–6.5% for the others. That premium lines up with the highest rate sensitivity, a three-quarter ROE fade, the lowest CASA and a fresh downgrade. On latest-quarter ROE with β=1, it is only +2% cheap.
- **HLB is fairly valued** (+1.7%; −3.8% at β=1) on an ex-Chengdu basis, and **PBB is rich in every specification** (−13%).
- **CIMB's valuation is a beta question.** It is −18% at its own β of 1.28 and +6% at β=1.
- **Consensus gaps over 15%** (PBB, CIMB, HLB, AMBANK) reflect three things: targets are 12-month forward, brokers assume higher forward ROE, and brokers use a flat COE. RHB is the only bank where our fair value sits above the consensus median (+10%). HLIB's new RM8.00 is below it.

---

## Module 4 — Quality score v1.1 (0–100, percentile within the core six; UNVERIFIED inputs score 50)

| Bank | Core ROE | ROE slope | CASA | CIR | GIL | LLC | CET1 adj. vs 13% | CET1 per +100bp | ROE (27) | Trend (9) | CASA (13.5) | CIR (9) | GIL (13.5) | LLC (9) | CET1 (9) | Rate risk (10) | Quality v1.0 wts | Quality v1.1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PBBANK | 12.2% | -0.25pp | UNVERIFIED | 35.1% | 0.54% | 138.9% | +0.84pp | −26bp | 100 | 20 | 50 | 100 | 100 | 75 | 40 | 100 | 76.0 | **78.4** |
| CIMB | 11.2% | -0.19pp | 42.6% | 45.2% | 1.6% | UNVERIFIED | +0.88pp | −52bp | 60 | 60 | 100 | 40 | 20 | 50 | 60 | 40 | 57.0 | **55.3** |
| HLBANK † | 10.2% | +0.13pp | 34.7% | 37.6% | 0.57% | 244.1% | -0.16pp | −32bp | 20 | 100 | 50 | 80 | 80 | 100 | 0 | 60 | 53.5 | **54.2** |
| MAYBANK | 11.2% | +0.08pp | 41.5% | 49.1% | 1.35% | 103.1% | +0.69pp | −57bp | 80 | 80 | 75 | 0 | 60 | 25 | 20 | 20 | 56.8 | **53.1** |
| RHBBANK | 10.3% | -0.40pp | 27.6% | 46.8% | 1.47% | 115.4% | +1.72pp | −61bp | 40 | 0 | 0 | 20 | 40 | 50 | 80 | 0 | 33.0 | **29.7** |
| AMBANK | 10.0% | -0.21pp | 32.5% | 43.4% | 1.62% | 102.5% | +1.75pp | −28bp | 0 | 40 | 25 | 60 | 0 | 0 | 100 | 80 | 23.8 | **29.4** |

*Weights are the prompt's (ROE 30, trend 10, CASA 15, CIR 10, GIL 15, LLC 10, CET1 10) × 0.9, plus **rate risk 10** (CET1 bp per +100bp, inverse). The CET1 buffer uses CET1 marked to 13/10, and MAYBANK's also includes the Etiqa buyout at −1.10pp. The "Quality v1.0 wts" column re-scores on the same v1.1 inputs with the prompt's original weights, to isolate the effect of the new factor. The v1.0 report's quality numbers are in the reconciliation table above. ROE trend is the slope of the last four quarterly annualised core ROEs.*

**Reads.** PBB rises (78): it has the best rate-risk profile on top of the best franchise metrics. RHB (30) and AMBANK (29) sit at the bottom. MAYBANK slips to 53 because the Etiqa correction thins its CET1 buffer to 0.7pp above 13%, and its rate risk is the second highest.

---

## Module 5 — Technical analysis (weekly primary, daily entry; unchanged from v1.0)

Indicators use dividend-adjusted OHLC, because every core bank went ex-dividend in the 3-month window (HLB 80 sen on 07/10; MAYBANK 23/09; CIMB 15/09; RHB 14/09; PBB 10/09).

How the levels are built:
- **Structure:** weekly pivots (3y), daily pivots (±15 sessions), 52-week extremes, high-volume nodes, and the 50/200-DMA and 40-week lines. Levels are clustered within 0.6 ATR.
- **T1:** the first cluster at least 1.5 ATR above price.
- **Stop:** the tighter of (support − 0.25 ATR) and 2 × ATR, never within 1.5 ATR of price.

| Bank | Close | 20DMA | 50DMA | 200DMA | 40W | 50/200 cross (date) | 40W slope 4w | Regime | RSI D | RSI W | MACD D / W (vs signal, hist) | ADX (lead) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.30 | 7.57 | 8.05 | 7.98 | 8.04 | golden (25/09/25) | +0.4% | Range | 32 | 33 | ↓+ / ↓− | 54 (−DI) |
| HLBANK † | 21.48 | 22.04 | 22.11 | 21.78 | 21.82 | golden (02/09/26) | +0.3% | Range | 41 | 48 | ↓+ / ↓− | 25 (−DI) |
| MAYBANK | 9.96 | 10.02 | 10.19 | 10.59 | 10.65 | death (28/08/26) | +0.2% | Range | 44 | 37 | ↓+ / ↓+ | 17 (+DI) |
| PBBANK | 4.70 | 4.72 | 4.88 | 4.73 | 4.75 | golden (07/10/25) | +0.9% | Range | 45 | 41 | ↓+ / ↓− | 31 (−DI) |
| CIMB | 7.50 | 7.67 | 7.72 | 7.64 | 7.62 | golden (03/09/26) | -0.1% | Downtrend | 44 | 42 | ↓+ / ↓− | 19 (−DI) |
| AMBANK | 6.27 | 6.45 | 6.81 | 6.41 | 6.43 | golden (27/08/25) | +0.5% | Range | 37 | 40 | ↓+ / ↓− | 35 (−DI) |

*MACD key: ↑/↓ = MACD above/below its signal line; +/− = histogram rising/falling. Regime: Uptrend needs the weekly close above a rising 40-week MA, plus price above the 200-DMA with the 50-DMA above the 200-DMA. Downtrend needs the weekly close below a falling 40-week MA plus price below the 200-DMA. Anything else is Range.*

| Bank | 3M vs KLCI | 6M vs KLCI | 3M vs sector | 6M vs sector | RS line in 52W range | RS 52W extreme | From 52W high | OBV 20d | CMF 20d |
|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | -6.9% | -5.7% | -8.0% | -7.6% | 53% | no | -16.8% | down | -0.08 |
| HLBANK † | +6.1% | +5.0% | +5.0% | +3.1% | 62% | no | -12.6% | down | -0.29 |
| MAYBANK | -1.8% | -5.0% | -2.9% | -6.9% | 44% | no | -15.0% | down | -0.49 |
| PBBANK | +2.0% | +6.4% | +0.9% | +4.5% | 82% | no | -9.2% | down | -0.24 |
| CIMB | +4.4% | +6.0% | +3.3% | +4.1% | 70% | no | -11.8% | down | -0.06 |
| AMBANK | +1.0% | +9.0% | -0.1% | +7.1% | 58% | no | -14.9% | down | -0.26 |

| Bank | Entry zone | Stop (basis) | Immediate hurdle | T1 | T2 | Upside T1 | Downside | R:R | R:R to hurdle | Flip trigger (weekly close >) | Post-flip stop / T1 / T2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.21–7.33 | 7.06 (2xATR) | – | 7.84 | 8.13 | +7.3% | -3.3% | 2.20 | 2.20 | 8.04 | 7.86 / 8.24 / 8.77 |
| HLBANK † | 21.20–21.59 | 20.66 (structure) | 21.86 | 23.41 | 24.58 | +9.0% | -3.8% | 2.36 | 0.46 | 21.82 | 21.19 / 23.41 / 24.58 |
| MAYBANK | 9.87–9.99 | 9.73 (2xATR) | – | 10.19 | 10.63 | +2.3% | -2.3% | 1.00 | 1.00 | 10.65 | 10.48 / 11.02 / 11.71 |
| PBBANK | 4.65–4.72 | 4.55 (2xATR) | 4.75 | 4.87 | 5.04 | +3.6% | -3.2% | 1.11 | 0.36 | 4.75 | 4.64 / 4.87 / 5.04 |
| CIMB | 7.39–7.54 | 7.26 (structure) | 7.62 | 7.93 | 8.51 | +5.7% | -3.2% | 1.77 | 0.50 | 7.64 | 7.42 / 7.93 / 8.51 |
| AMBANK | 6.24–6.30 | 6.00 (2xATR) | – | 6.50 | 6.81 | +3.7% | -4.3% | 0.85 | 0.85 | 6.43 | 6.22 / 6.81 / 7.37 |

| Bank | Trend (35) | RS (25) | Momentum (20) | R:R (20) | Penalty | Tech score | … conservative T1 |
|---|---|---|---|---|---|---|---|
| RHBBANK | 30 | 15 | 8 | 73 | −0 | **30.3** | 30.3 |
| HLBANK † | 40 | 74 | 31 | 79 | −0 | **54.4** | 41.7 |
| MAYBANK | 15 | 29 | 30 | 33 | −0 | **25.3** | 25.3 |
| PBBANK | 30 | 67 | 27 | 37 | −0 | **40.1** | 35.1 |
| CIMB | 30 | 72 | 35 | 59 | −0 | **47.3** | 38.8 |
| AMBANK | 30 | 71 | 21 | 28 | −0 | **38.3** | 38.3 |

**Reads.** All six trade below their 200-DMA, and OBV is falling on all six. HLB has the best relative strength (+6.1% vs KLCI over 3M) on a golden cross, but must reclaim the RM21.8–22.1 moving-average band. RHB has the weakest tape: ADX 54 with sellers in control, and RS −6.9%. That is consistent with the market pricing exactly the rate-risk and downgrade story above.

---

## Module 6 — Composite, quadrant, sensitivity

| Bank | Mispricing (40) | P/B–ROE resid. (30) | P/B z 5Y (15) | DY NTM (15) | Value score | … with β=1 COE |
|---|---|---|---|---|---|---|
| RHBBANK | 100 | 100 | 40 | 100 | **91** | 91 |
| HLBANK † | 60 | 40 | 100 | 20 | **54** | 46 |
| MAYBANK | 80 | 20 | 60 | 80 | **59** | 35 |
| PBBANK | 20 | 0 | 80 | 0 | **20** | 12 |
| CIMB | 0 | 60 | 20 | 60 | **30** | 62 |
| AMBANK | 40 | 80 | 0 | 40 | **46** | 54 |

| Bank | Value | Quality | Tech | Composite 40/30/30 | Rank | Rank 60/20/20 | Rank 20/30/50 | Rank (β=1) | Quadrant | Quadrant (β=1) | Quadrant (cons. T1) | Negative broker action ≤30d | Lean | Lean under 60/20/20 · 20/30/50 · β=1 · cons. T1 | Confidence (lean stable) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 91 | 30 | 30 | **54.4** | 1 | 1 | 4 | 2 | VALUE TRAP WATCH | VALUE TRAP WATCH | VALUE TRAP WATCH | HLIB Hold RM8.00 | **Neutral** | N / N / N / N | High (4/4) |
| HLBANK † | 54 | 54 | 54 | **54.2** | 2 | 2 | 1 | 3 | ACTIONABLE BUY | MOMENTUM HOLD | VALUE TRAP WATCH | – | **Overweight** | OW / OW / N / OW | Medium (3/4) |
| MAYBANK | 59 | 53 | 25 | **47.1** | 3 | 3 | 5 | 6 | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | – | **Neutral** | N / N / UW / N | Medium (3/4) |
| PBBANK | 20 | 78 | 40 | **43.5** | 4 | 6 | 2 | 5 | AVOID / UNDERWEIGHT | AVOID / UNDERWEIGHT | AVOID / UNDERWEIGHT | – | **Neutral** | UW / N / UW / N | Low (2/4) |
| CIMB | 30 | 55 | 47 | **42.8** | 5 | 5 | 3 | 1 | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | JPMorgan Underweight | **Underweight** | UW / N / N / UW | Low (2/4) |
| AMBANK | 46 | 29 | 38 | **38.7** | 6 | 4 | 6 | 4 | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | JPMorgan Neutral | **Underweight** | N / UW / N / UW | Low (2/4) |

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

| Bank | Price | Mkt cap RMbn | P/B (core) | Fair P/B | Mispricing | Core ROE | FY+1 yld | CET1 adj. | CET1 per +100bp | GIL | Trend | RSI | Upside T1 | Stop | R:R | V / Q / T / Composite | Quadrant | Lean | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.30 | 31.9 | 0.94 | 1.25 | +32% | 10.3% | 7.1% | 14.7% | −61bp | 1.47% | Range | 32 | +7.3% | 7.06 | 2.2 | 91 / 30 / 30 / **54.4** | VALUE TRAP WATCH | **Neutral** | High |
| HLBANK † | 21.48 | 44.0 | 1.13 | 1.15 | +2% | 10.2% | 5.4% | 12.8% | −32bp | 0.57% | Range | 41 | +9.0% | 20.66 | 2.4 | 54 / 54 / 54 / **54.2** | ACTIONABLE BUY | **Overweight** | Medium |
| MAYBANK | 9.96 | 120.5 | 1.30 | 1.41 | +8% | 11.2% | 6.8% | 13.7% | −57bp | 1.35% | Range | 44 | +2.3% | 9.73 | 1.0 | 59 / 53 / 25 / **47.1** | VALUE TRAP WATCH | **Neutral** | Medium |
| PBBANK | 4.70 | 91.2 | 1.49 | 1.29 | -13% | 12.2% | 5.1% | 13.8% | −26bp | 0.54% | Range | 45 | +3.6% | 4.55 | 1.1 | 20 / 78 / 40 / **43.5** | AVOID / UNDERWEIGHT | **Neutral** | Low |
| CIMB | 7.50 | 80.7 | 1.16 | 0.95 | -18% | 11.2% | 6.7% | 13.9% | −52bp | 1.6% | Downtrend | 44 | +5.7% | 7.26 | 1.8 | 30 / 55 / 47 / **42.8** | AVOID / UNDERWEIGHT | **Underweight** | Low |
| AMBANK | 6.27 | 20.8 | 0.98 | 0.93 | -4% | 10.0% | 5.9% | 14.8% | −28bp | 1.62% | Range | 37 | +3.7% | 6.00 | 0.9 | 46 / 29 / 38 / **38.7** | AVOID / UNDERWEIGHT | **Underweight** | Low |

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
