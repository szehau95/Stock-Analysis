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

*Correction to the interim Module 1 shown in chat:* HLBANK and AMBANK are **not** stale. HLB's 4QFY26 (June quarter) was released on 27/08/2026 and AMBANK's 1QFY27 (June quarter) on 18/08/2026. The ADV figures shown earlier were one-day volumes; the table above uses 63-session averages.

---

## Module 2 — Fundamentals (T4Q, latest quarter, NTM consensus)

NTM EPS blends the current- and next-fiscal-year consensus by time remaining (Yahoo, T3, 14/10/2026). The NTM dividend yield is NTM EPS × the T4Q payout. Core ROE is core T4Q EPS over average book value, using the panel's documented one-off adjustments.

**HLBANK core basis.** Share of associates, mainly the 17.8% Bank of Chengdu (BOCD) stake, was RM1,380m of FY26 PAT of RM4,531m (30%). Stripping it from both earnings *and* equity (carrying value RM10.35b, T3) gives a **core ROE of 10.2% vs 11.2% headline**. The stake is then valued at market (BOCD CNY19.25 × 4.238b shares × 17.8% × CNYMYR 0.6097 = RM8.85b, RM4.32/share). That is RM1.5b below carrying value, which is a latent impairment risk of about RM0.73/share.

| Bank | P/B | P/B 5Y mean (±1SD) | P/B z (5Y) | P/TBV | P/E T4Q core | P/E NTM | EY NTM | DY T4Q | DY NTM |
|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 1.29 | 1.28 (1.19–1.37) | +0.14 | 1.39 | 11.5 | 10.9 | 9.2% | 6.4% | 6.8% |
| PBBANK | 1.48 | 1.59 (1.46–1.72) | -0.84 | 1.56 | 12.4 | 11.8 | 8.5% | 4.8% | 5.1% |
| CIMB | 1.15 | 1.05 (0.90–1.20) | +0.70 | 1.30 | 10.3 | 9.6 | 10.4% | 6.3% | 6.7% |
| HLBANK † | 1.05 | 1.20 (1.09–1.32) | -1.29 | 1.11 | 9.7 | 9.2 | 10.8% | 5.1% | 5.4% |
| RHBBANK | 0.94 | 0.88 (0.78–0.97) | +0.61 | 1.04 | 9.2 | 8.9 | 11.3% | 6.8% | 7.1% |
| AMBANK | 0.97 | 0.81 (0.69–0.94) | +1.26 | 0.99 | 9.9 | 9.4 | 10.7% | 5.6% | 5.9% |

| Bank | Core ROE T4Q (headline basis) | Core ROE ranked | Latest Q ann. | Last 4Q ROE path (%) | 4Q slope /qtr | NIM | CIR | Loan growth y/y | CASA | FY+1 EPS rev. 3M |
|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 11.2% | = | 11.7% | 11.2 → 11.5 → 10.8 → 11.7 | +0.08pp | 2.1% (10.0bp y/y) | 49.1% | 2.7% | 41.5% | -0.6% |
| PBBANK | 12.2% | = | 12.1% | 12.6 → 12.7 → 11.8 → 12.1 | -0.25pp | 2.08% (UNVERIFIED y/y) | 35.1% | 5.9% | UNVERIFIED | -0.4% |
| CIMB | 11.2% | = | 11.2% | 11.8 → 10.9 → 11.0 → 11.2 | -0.19pp | 2.04% (UNVERIFIED y/y) | 45.2% | UNVERIFIED | 42.6% | -1.6% |
| HLBANK † | 11.2% | 10.2% | 12.1% | 11.2 → 11.9 → 10.3 → 12.1 | +0.13pp | 1.84% (-6.0bp y/y) | 37.6% | 7.7% | 34.7% | -0.3% |
| RHBBANK | 10.3% | = | 9.6% | 10.8 → 10.7 → 10.2 → 9.6 | -0.40pp | 1.86% (-2.0bp y/y) | 46.8% | 7.0% | 27.6% | -1.1% |
| AMBANK | 10.0% | = | 9.7% | 10.3 → 10.0 → 9.7 → 9.7 | -0.21pp | 1.93% (-8.0bp y/y) | 43.4% | 7.0% | 32.5% | +0.0% |

| Bank | GIL | Stage 2 | Credit cost | LLC (basis) | CET1 | TCR | LCR | Payout T4Q | CET1 >13% (RM bn, est.) | Payout vs CET1 |
|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 1.35% | UNVERIFIED | 20bp | 103.1% (basis not stated) | 14.92% (pro forma ~14.1% post-Etiqa) | 18.68% | 130% | 74% | 6.5 | ok |
| PBBANK | 0.54% | UNVERIFIED | UNVERIFIED | 138.9% (basis not stated) | 13.9% | 16.5% | UNVERIFIED | 60% | 2.9 | ok |
| CIMB | 1.6% | UNVERIFIED | 34bp | UNVERIFIED (n/a) | 14.0% | UNVERIFIED | UNVERIFIED | 65% | 4.4 | ok |
| HLBANK † | 0.57% | UNVERIFIED | 4bp | 244.1% (incl. regulatory reserve (79.5% excl.)) | 12.9% | 16.2% | 127.0% | 50% | -0.2 | WATCH: CET1 below 13% ref |
| RHBBANK | 1.47% | UNVERIFIED | 13bp | 115.4% (incl. regulatory reserve) | 14.8% | 17.1% | 138.3% | 63% | 3.8 | ok |
| AMBANK | 1.62% | UNVERIFIED | 19bp | 102.5% (incl. regulatory reserve) | 14.82% | 17.31% | 143.9% | 55% | 2.1 | ok |

| Bank | FY guidance (mgmt) | YTD vs guidance | NIM per 25bp OPR cut (bp) | KPI tier |
|---|---|---|---|---|
| MAYBANK | FY26: ROE>=11.8%, loans 4-5%, NIM 2.05-2.10%, NCC ~20bps, CIR ~49% | ROE behind (11.6 vs >=11.8); NIM/NCC/CIR on track; loans behind (2.7 vs 4-5) | 2-3 (sector avg; ~70% variable-rate) | T2 |
| PBBANK | FY26: loans 4-5%, credit cost single-digit bps | Loans ahead (5.9 annualised vs 4-5); NIM -3bp QoQ to 2.08% (lowest since 2020) | 3-4 (Maybank IB 2025) | T2 |
| CIMB | FY26: ROE 11.0-11.5%, CIR <47%, credit cost 25-35bps, CET1 >=14.0%, NIM flat to -10bps (revised, T3) | ROE on track (11.2); CIR ahead (45.2); credit cost at top of range (34 1H ann.; 38 in 2Q); CET1 at floor (14.0) | UNVERIFIED (sector 2-4) | T1 |
| HLBANK † | FY26 loans 6-7% (Kenanga 28/05/2026); FY27 targets not disclosed | FY26 loans ahead (7.7 vs 6-7); FY27 UNVERIFIED | UNVERIFIED (sector 2-4) | T1 |
| RHBBANK | FY26: credit cost 13-14bps, loans 5-6% | Credit cost on track (13 vs 13-14); loans ahead (7.0 YoY) | 3-4 (Maybank IB 2025) | T1 |
| AMBANK | FY27 numeric targets not disclosed; FY26 ROE ~10% | ROE behind FY26 run-rate (9.7 vs ~10) | UNVERIFIED (sector 2-4) | T1 |

*Stage 2 loans, non-interest-income share and ROA could not be verified at T1/T2 for the set and are marked UNVERIFIED. The quality score therefore uses GIL alone in its asset-quality slot, consistently for all six. The "CET1 > 13%" figure uses an RWA proxy of 0.55 × total assets and is an estimate. MAYBANK's CET1 buffer uses the pro forma ~14.1% after the RM4.83b Etiqa buyout.*

**Reads**
- **The ROE trajectory splits the group.** MAYBANK (latest quarter 11.7%) and HLB (12.1% headline) are improving. RHB (10.8 → 9.6% over three quarters) and AMBANK (10.3 → 9.7%) are fading. For RHB this matters most: MBSB Research flags a likely miss of its PROGRESS27 target (≥12% ROE by 2027).
- **Funding is the pressure point.** PBB's NIM is at its lowest since 2020 (2.08%, −3bp q/q). AMBANK's CASA fell 10% YTD and its NIM is down 8bp y/y. RHB has the lowest CASA in the group (27.6%).
- **Capital.** RHB (14.8%) and AMBANK (14.82%) have the widest CET1 buffers. HLB, at 12.9%, is below the 13% reference, which is why HLB is flagged in the payout check.

---

## Module 3 — Valuation

**3.1–3.2 Justified P/B and mispricing.** Justified P/B = (core ROE − g)/(COE − g), and fair value = justified P/B × BVPS (plus the BOCD stake at market for HLB). The base case is the one specified in the variables block. The four stress columns change one assumption at a time: a uniform β of 1, the latest quarter's annualised ROE instead of T4Q, both together, and g/COE shifts.

| Bank | β raw / Blume | COE | Core ROE | Justified P/B | Actual P/B (core) | BVPS (core) | Fair value | Mispricing | … at β=1 | … on latest-Q ROE | … latest-Q ROE & β=1 | FV g=3% / 5% | FV COE +50bp / −50bp | Implied COE | Implied ERP |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 0.82 / 0.88 | 9.1% | 11.2% | 1.41 | 1.29 | 7.69 | 10.86 | +9.0% | -4.8% | +17.2% | +2.4% | 10.34 / 11.63 | 9.89 / 12.04 | 9.5% | 6.5% |
| PBBANK | 1.13 / 1.08 | 10.3% | 12.2% | 1.29 | 1.48 | 3.17 | 4.09 | -12.9% | -5.4% | -13.7% | -6.2% | 3.97 / 4.27 | 3.79 / 4.44 | 9.5% | 5.2% |
| CIMB | 1.42 / 1.28 | 11.5% | 11.2% | 0.95 | 1.15 | 6.50 | 6.19 | -17.4% | +6.5% | -17.5% | +6.4% | 6.23 / 6.15 | 5.81 / 6.63 | 10.2% | 5.0% |
| HLBANK † | 0.90 / 0.93 | 9.4% | 10.2% | 1.15 | 1.12 | 15.33 | 21.94 | +2.1% | -3.4% | +2.1% | -3.4% | 21.58 / 22.45 | 20.45 / 23.72 | 9.6% | 6.2% |
| RHBBANK | 0.81 / 0.87 | 9.1% | 10.3% | 1.25 | 0.94 | 7.81 | 9.72 | +33.1% | +15.5% | +18.7% | +3.0% | 9.40 / 10.19 | 8.85 / 10.78 | 10.7% | 7.9% |
| AMBANK | 1.15 / 1.10 | 10.4% | 10.0% | 0.93 | 0.97 | 6.48 | 6.05 | -3.5% | +6.6% | -9.1% | +0.4% | 6.11 / 5.97 | 5.61 / 6.56 | 10.2% | 5.8% |

**3.3 Cross-sectional P/B vs core ROE.** Across the nine listed banks: **P/B = −0.28 + 13.15 × ROE, R² 0.89** (slope s.e. 1.77). On the core six alone: P/B = −1.37 + 23.3 × ROE, R² 0.86. A negative residual means the bank is cheap relative to its ROE.

| Bank | Set | Core ROE | P/B (core) | Fitted P/B | Residual (9-bank fit) | Residual (core-6 fit) | Read |
|---|---|---|---|---|---|---|---|
| ALLIANCE | context | 10.0% | 0.89 | 1.03 | -13.8% | – | cheap |
| RHBBANK | core | 10.3% | 0.94 | 1.07 | -12.6% | -9.3% | cheap |
| BIMB | context | 7.0% | 0.56 | 0.63 | -10.7% | – | cheap |
| AMBANK | core | 10.0% | 0.97 | 1.03 | -6.3% | +0.3% | cheap |
| CIMB | core | 11.2% | 1.15 | 1.18 | -2.6% | -6.4% | on line |
| HLBANK † | core | 10.2% | 1.12 | 1.06 | +5.3% | +9.9% | rich |
| MAYBANK | core | 11.2% | 1.29 | 1.19 | +9.1% | +4.6% | rich |
| PBBANK | core | 12.2% | 1.48 | 1.32 | +12.5% | +0.9% | rich |
| AFFIN | context | 4.4% | 0.41 | 0.29 | +38.5% | – | rich |

**3.4–3.6 History, dividends and consensus.** P/B z-scores against each bank's own 5-year history are in the Module 2 valuation table.

| Bank | DY NTM | Spread vs MGS10 3.83% | Payout | Cons. TP median | # analysts | Buy/Hold/Sell | Our FV | FV vs cons. | >15% gap |
|---|---|---|---|---|---|---|---|---|---|
| MAYBANK | 6.8% | +3.0pp | 74% | 11.54 | 18 | 9/8/0 | 10.86 | -5.9% | no |
| PBBANK | 5.1% | +1.2pp | 60% | 5.54 | 18 | 10/7/0 | 4.09 | -26.1% | YES |
| CIMB | 6.7% | +2.9pp | 65% | 8.90 | 16 | 13/4/1 | 6.19 | -30.4% | YES |
| HLBANK † | 5.4% | +1.6pp | 50% | 26.07 | 14 | 12/3/0 | 21.94 | -15.9% | YES |
| RHBBANK | 7.1% | +3.2pp | 63% | 8.73 | 15 | 6/9/0 | 9.72 | +11.3% | no |
| AMBANK | 5.9% | +2.0pp | 55% | 7.72 | 15 | 12/4/0 | 6.05 | -21.7% | YES |

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

| Bank | Core ROE | ROE slope | CASA | CIR | GIL | LLC | CET1 vs 13% | ROE (30) | Trend (10) | CASA (15) | CIR (10) | GIL (15) | LLC (10) | CET1 (10) | Quality |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| PBBANK | 12.2% | -0.25pp | UNVERIFIED | 35.1% | 0.54% | 138.9% | +0.90pp | 100 | 20 | 50 | 100 | 100 | 75 | 20 | **74.0** |
| MAYBANK | 11.2% | +0.08pp | 41.5% | 49.1% | 1.35% | 103.1% | +1.09pp | 80 | 80 | 75 | 0 | 60 | 25 | 60 | **60.8** |
| CIMB | 11.2% | -0.19pp | 42.6% | 45.2% | 1.6% | UNVERIFIED | +1.00pp | 60 | 60 | 100 | 40 | 20 | 50 | 40 | **55.0** |
| HLBANK † | 10.2% | +0.13pp | 34.7% | 37.6% | 0.57% | 244.1% | -0.10pp | 20 | 100 | 50 | 80 | 80 | 100 | 0 | **53.5** |
| RHBBANK | 10.3% | -0.40pp | 27.6% | 46.8% | 1.47% | 115.4% | +1.80pp | 40 | 0 | 0 | 20 | 40 | 50 | 80 | **33.0** |
| AMBANK | 10.0% | -0.21pp | 32.5% | 43.4% | 1.62% | 102.5% | +1.82pp | 0 | 40 | 25 | 60 | 0 | 0 | 100 | **23.8** |

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

| Bank | Close | 20DMA | 50DMA | 200DMA | 40W | 50/200 cross (date) | 40W slope 4w | Regime | RSI D | RSI W | MACD D / W (vs signal, hist) | ADX (lead) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.30 | 7.57 | 8.05 | 7.98 | 8.04 | golden (25/09/25) | +0.4% | Range | 32 | 33 | ↓+ / ↓− | 54 (−DI) |
| HLBANK † | 21.48 | 22.04 | 22.11 | 21.78 | 21.82 | golden (02/09/26) | +0.3% | Range | 41 | 48 | ↓+ / ↓− | 25 (−DI) |
| MAYBANK | 9.96 | 10.02 | 10.19 | 10.59 | 10.65 | death (28/08/26) | +0.2% | Range | 44 | 37 | ↓+ / ↓+ | 17 (+DI) |
| CIMB | 7.50 | 7.67 | 7.72 | 7.64 | 7.62 | golden (03/09/26) | -0.1% | Downtrend | 44 | 42 | ↓+ / ↓− | 19 (−DI) |
| PBBANK | 4.70 | 4.72 | 4.88 | 4.73 | 4.75 | golden (07/10/25) | +0.9% | Range | 45 | 41 | ↓+ / ↓− | 31 (−DI) |
| AMBANK | 6.27 | 6.45 | 6.81 | 6.41 | 6.43 | golden (27/08/25) | +0.5% | Range | 37 | 40 | ↓+ / ↓− | 35 (−DI) |

*MACD key: ↑/↓ = MACD above/below its signal line; +/− = histogram rising/falling over 3 bars. The regime is classed on the weekly trend: Uptrend needs the weekly close above a rising 40-week MA plus price above the 200-DMA with the 50-DMA above the 200-DMA. Downtrend needs the weekly close below a falling 40-week MA plus price below the 200-DMA. Anything else is Range. On the unadjusted chart, RHB's 50/200 crossed down on 08/10/2026. Adjusted, the 50-DMA (8.05) is still just above the 200-DMA (7.98) and closing fast.*

| Bank | 3M vs KLCI | 6M vs KLCI | 3M vs sector | 6M vs sector | RS line in 52W range | RS 52W extreme | From 52W high | OBV 20d | CMF 20d |
|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | -6.9% | -5.7% | -8.0% | -7.6% | 53% | no | -16.8% | down | -0.08 |
| HLBANK † | +6.1% | +5.0% | +5.0% | +3.1% | 62% | no | -12.6% | down | -0.29 |
| MAYBANK | -1.8% | -5.0% | -2.9% | -6.9% | 44% | no | -15.0% | down | -0.49 |
| CIMB | +4.4% | +6.0% | +3.3% | +4.1% | 70% | no | -11.8% | down | -0.06 |
| PBBANK | +2.0% | +6.4% | +0.9% | +4.5% | 82% | no | -9.2% | down | -0.24 |
| AMBANK | +1.0% | +9.0% | -0.1% | +7.1% | 58% | no | -14.9% | down | -0.26 |

| Bank | Entry zone | Stop (basis) | Immediate hurdle | T1 | T2 | Upside T1 | Downside | R:R | R:R to hurdle | Flip trigger (weekly close >) | Post-flip stop / T1 / T2 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.21–7.33 | 7.06 (2xATR) | – | 7.84 | 8.13 | +7.3% | -3.3% | 2.20 | 2.20 | 8.04 | 7.86 / 8.24 / 8.77 |
| HLBANK † | 21.20–21.59 | 20.66 (structure) | 21.86 | 23.41 | 24.58 | +9.0% | -3.8% | 2.36 | 0.46 | 21.82 | 21.19 / 23.41 / 24.58 |
| MAYBANK | 9.87–9.99 | 9.73 (2xATR) | – | 10.19 | 10.63 | +2.3% | -2.3% | 1.00 | 1.00 | 10.65 | 10.48 / 11.02 / 11.71 |
| CIMB | 7.39–7.54 | 7.26 (structure) | 7.62 | 7.93 | 8.51 | +5.7% | -3.2% | 1.77 | 0.50 | 7.64 | 7.42 / 7.93 / 8.51 |
| PBBANK | 4.65–4.72 | 4.55 (2xATR) | 4.75 | 4.87 | 5.04 | +3.6% | -3.2% | 1.11 | 0.36 | 4.75 | 4.64 / 4.87 / 5.04 |
| AMBANK | 6.24–6.30 | 6.00 (2xATR) | – | 6.50 | 6.81 | +3.7% | -4.3% | 0.85 | 0.85 | 6.43 | 6.22 / 6.81 / 7.37 |

| Bank | Trend (35) | RS (25) | Momentum (20) | R:R (20) | Penalty | Tech score | … conservative T1 |
|---|---|---|---|---|---|---|---|
| RHBBANK | 30 | 15 | 8 | 73 | −0 | **30.3** | 30.3 |
| HLBANK † | 40 | 74 | 31 | 79 | −0 | **54.4** | 41.7 |
| MAYBANK | 15 | 29 | 30 | 33 | −0 | **25.3** | 25.3 |
| CIMB | 30 | 72 | 35 | 59 | −0 | **47.3** | 38.8 |
| PBBANK | 30 | 67 | 27 | 37 | −0 | **40.1** | 35.1 |
| AMBANK | 30 | 71 | 21 | 28 | −0 | **38.3** | 38.3 |

*Technical score weights: trend regime 35, relative strength vs KLCI and sector (3M/6M) 25, momentum (daily and weekly RSI/MACD, ADX direction) 20, R:R 20. Penalties apply for daily RSI > 75 or price > 2 ATR above the 20-DMA; none triggered. The "conservative T1" column re-scores with the immediate hurdle as T1.*

**Reads**
- **All six trade below their 200-DMA.** None has a relative-strength line at a 52-week high, and OBV is falling on all six over 20 days. The sector is in a correction, not a trend.
- **HLB has the best relative strength:** +6.1% vs KLCI over 3M and +5.0% vs the sector, on a golden cross dated 02/09/2026. Its R:R of 2.4 assumes it reclaims the RM21.8–22.1 band (200-DMA, 40-week line and 20/50-DMA). Measured to that band, the R:R is only 0.46.
- **RHB has the weakest tape:** ADX 54 with −DI in control, RSI 32, and −6.9% vs KLCI over 3M. The R:R of 2.2 is real (there is no heavy hurdle before RM7.84), but it is a counter-trend trade with no structural support until RM6.61–6.63.
- **MAYBANK's tape is broken:** death cross on 28/08/2026, −5.0% vs KLCI over 6M, and R:R of 1.0. It is also the largest KLCI weight ahead of the KLCI-50 dilution.

---

## Module 6 — Composite, quadrant and sensitivity

| Bank | Mispricing (40) | P/B–ROE resid. (30) | P/B z 5Y (15) | DY NTM (15) | Value score | … with β=1 COE |
|---|---|---|---|---|---|---|
| RHBBANK | 100 | 100 | 40 | 100 | **91** | 91 |
| HLBANK † | 60 | 40 | 100 | 20 | **54** | 46 |
| MAYBANK | 80 | 20 | 60 | 80 | **59** | 35 |
| CIMB | 0 | 60 | 20 | 60 | **30** | 54 |
| PBBANK | 20 | 0 | 80 | 0 | **20** | 12 |
| AMBANK | 40 | 80 | 0 | 40 | **46** | 62 |

| Bank | Value | Quality | Tech | Composite 40/30/30 | Rank | Rank 60/20/20 | Rank 20/30/50 | Rank (β=1) | Quadrant | Quadrant (β=1) | Quadrant (cons. T1) | Checks |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 91 | 33 | 30 | **55.4** | 1 | 1 | 4 | 1 | VALUE TRAP WATCH | VALUE TRAP WATCH | VALUE TRAP WATCH | 3/4 |
| HLBANK † | 54 | 54 | 54 | **54.0** | 2 | 2 | 1 | 3 | ACTIONABLE BUY | MOMENTUM HOLD | VALUE TRAP WATCH | 2/4 |
| MAYBANK | 59 | 61 | 25 | **49.4** | 3 | 3 | 5 | 5 | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | 2/4 |
| CIMB | 30 | 55 | 47 | **42.7** | 4 | 5 | 3 | 2 | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | 3/4 |
| PBBANK | 20 | 74 | 40 | **42.2** | 5 | 6 | 2 | 6 | AVOID / UNDERWEIGHT | AVOID / UNDERWEIGHT | AVOID / UNDERWEIGHT | 3/4 |
| AMBANK | 46 | 24 | 38 | **37.0** | 6 | 4 | 6 | 4 | AVOID / UNDERWEIGHT | VALUE TRAP WATCH | AVOID / UNDERWEIGHT | 2/4 |

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

| Bank | Price | Mkt cap RMbn | P/B (core) | Fair P/B | Mispricing | Core ROE | FY+1 yld | CET1 | GIL | Trend | RSI | Upside T1 | Stop | R:R | V / Q / T / Composite | Quadrant | Lean | Confidence |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| RHBBANK | 7.30 | 31.9 | 0.94 | 1.25 | +33% | 10.3% | 7.1% | 14.8% | 1.47% | Range | 32 | +7.3% | 7.06 | 2.2 | 91 / 33 / 30 / **55.4** | VALUE TRAP WATCH | **Overweight** | Medium |
| HLBANK † | 21.48 | 44.0 | 1.12 | 1.15 | +2% | 10.2% | 5.4% | 12.9% | 0.57% | Range | 41 | +9.0% | 20.66 | 2.4 | 54 / 54 / 54 / **54.0** | ACTIONABLE BUY | **Overweight** | Low |
| MAYBANK | 9.96 | 120.5 | 1.29 | 1.41 | +9% | 11.2% | 6.8% | 14.92% | 1.35% | Range | 44 | +2.3% | 9.73 | 1.0 | 59 / 61 / 25 / **49.4** | VALUE TRAP WATCH | **Neutral** | Low |
| CIMB | 7.50 | 80.7 | 1.15 | 0.95 | -17% | 11.2% | 6.7% | 14.0% | 1.6% | Downtrend | 44 | +5.7% | 7.26 | 1.8 | 30 / 55 / 47 / **42.7** | AVOID / UNDERWEIGHT | **Neutral** | Medium |
| PBBANK | 4.70 | 91.2 | 1.48 | 1.29 | -13% | 12.2% | 5.1% | 13.9% | 0.54% | Range | 45 | +3.6% | 4.55 | 1.1 | 20 / 74 / 40 / **42.2** | AVOID / UNDERWEIGHT | **Underweight** | Medium |
| AMBANK | 6.27 | 20.8 | 0.97 | 0.93 | -3% | 10.0% | 5.9% | 14.82% | 1.62% | Range | 37 | +3.7% | 6.00 | 0.9 | 46 / 24 / 38 / **37.0** | AVOID / UNDERWEIGHT | **Underweight** | Low |

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
