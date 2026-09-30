# Malaysian Banks Correction — Causal Diagnosis & Entry-Point Verdict

**AS_OF_DATE:** 30/09/2026 (prices: Bursa close 30/09/2026; MGS: BNM FMIP 29/09/2026) · **UNIVERSE:** MAYBANK, PBBANK, CIMB, HLBANK, RHBBANK, AMBANK, BIMB, ALLIANCE, AFFIN · **HORIZON:** 12m core / 36m secondary · **PROFILE:** BOTH (PERSONAL sizing uses the connected IBKR account; CLIENT_HLPB suitability in §8) · **CASH_BUFFER_CHECK:** ON
All consequential numbers computed in Python (`src/`); raw/clean data in `data/`, module outputs in `output/`. Tier tags: **T1** primary (BNM, company releases, Bursa filings), **T2** verified secondary (The Edge/Star/NST/Bernama/broker notes with attribution), **T3** aggregator (Yahoo, klsescreener): lead-gen or mechanical price/consensus data only.

---

## 1. Bottom line

1. **The premise is only half right.** The cap-weighted bank composite is −10.9% on price from its 11/02/2026 peak but only **−6.7% on total return**. Ex-dividend mechanics account for 38% of the price fall, and YTD total return is **+3.5%**. The "heavy" correction is concentrated in AFFIN (−25% TR), BIMB (−18%), MAYBANK (−14%), RHB (−14%) and ALLIANCE (−13%).
2. **It is justified, and it is a de-rating, not an earnings event.** ~100% of the price decline is P/E compression; trailing core EPS is flat-to-up at 8 of 9 banks. The drivers are foreign selling of financials plus rotation into utilities, data-centre and construction names, and a global yield/oil risk-premium shock (UST +105bp and MGS +53bp since the peak; Brent +41%).
3. **Adjusted for ROE and a 4.09% MGS, the sector is fairly valued, not cheap.** Sector P/B is 1.23× (54th percentile of the post-2016 regime). Implied ERP is at its 10y median (50th percentile). ROE is at or above its 10y average at Maybank, CIMB, RHB and AMMB. The 20y P/B band is a false anchor because ROE reset structurally in 2015–16.
4. **History favours 12m patience, with a 36m caveat.** The closest fundamental analog is the **2013 taper tantrum** (+55bp MGS, EPS intact): +13% at 12m but −1.5% at 36m, because the 2014–16 ROE reset followed. At today's depth the sector base rate is a 72% 12m hit rate with a +10.5% median.
5. **Lean: SCALE-IN ON TRIGGERS, selectively. Confidence 65%.** The sector's probability-weighted 12m TR is only +5.5% (vs MGS 4.09%), so the call is stock-specific:
   - ACCUMULATE HLBANK now.
   - Scale into PBBANK, MAYBANK and ALLIANCE on the triggers in §8.
   - WAIT on CIMB, RHB and AMBANK (all near the top of their own 10y P/B bands).
   - AVOID AFFIN and BIMB.

---

## 2. Premise validation (Module 1)

### 2.1 Drawdown table (Yahoo prices T3, reconciled to IBKR last price for MAYBANK RM10.04; TR includes dividends at ex-date)

{{M1_TABLE}}

*Leg 1 = 52w high to the trough before 15/07/2026. Leg 2 = the Jul–Sep high to 30/09/2026 (TR basis). A blank Leg 1 means the 52w high itself was printed in August, so the bank's whole correction is the Aug–Sep leg.*

**Findings**
- **Ex-dividend mechanics.** 38% of the composite's price drawdown is dividends (MAYBANK 26%, CIMB 35%, PBBANK 18%). In total-return terms, only AFFIN, BIMB, ALLIANCE and CIMB are negative YTD.
- **Two distinct legs.**
  - *Leg 1 (Feb→early Jun: Iran war/oil, soft 1Q26, EM outflows, MYR −3.5%).* It hit MAYBANK, CIMB, HLB, BIMB, ALLIANCE and AFFIN. CIMB and HLB have since recovered 14% off their lows.
  - *Leg 2 (Aug→Sep: global yield spike, financials outflows, KLCI-50 announcement, 2Q results).* It hit PBBANK, RHB and AMMB, which printed **new 52w highs in August** and are now down 9–14% TR.
- **The sector trails KLCI by 5.2pp since its high.** A 12-name non-bank KLCI basket is **+9.3% YTD vs banks −1.1%**, which is rotation, not a market-wide collapse.

### 2.2 Ex-dividend events in the window and drawdown pattern

{{M1_EXDIV}}

The pattern is **event-concentrated**: the top-5 dividend-neutral down days deliver 51–99% of each bank's max TR drawdown, but gap-downs are rare (≤2 days of >2% gap per bank). It reads as orderly selling into a handful of catalyst days rather than a capitulation.

### 2.3 Five largest down days per bank (dividend-neutral TR returns), tagged to catalysts

{{M1_DOWNDAYS}}

### 2.4 Peer check: is it Malaysia-specific? (local-currency px; USD TR)

{{M1_PEERS}}

**Ruling:** this is a **Malaysia-plus-EM-flow event, not a regional bank sell-off**.
- Singapore banks are at or near highs (DBS +44%, OCBC +70% YTD in USD) and Thai banks are up 10–22%.
- Only Indonesia is worse (−14% to −25% YTD in USD, IDR 17,860). That feeds Maybank Indonesia and CIMB Niaga through translation.
- KLCI ex-banks is −1.8% YTD vs the bank composite −1.1% on price. The sharper gap is against the rotation basket (+9.3%).

---

## 3. Causal decomposition (Module 2)

### 3.1 Quantitative anchors

**(a) Price decomposition from each bank's 52w high: ΔlnP = ΔlnEPS(core TTM) + ΔlnP/E; ΔlnP = ΔlnBV + ΔlnP/B.**

{{M2_DECOMP}}

→ **Multiple-only de-rating.** EPS (core TTM) *rose* 0.1–5.8% at 8 of 9 banks between the high and today; AFFIN (−3.6%) is the exception. The dividend-yield-minus-MGS spread is *narrower than a year ago* at 7 of 9 banks, because MGS rose 64bp YoY (3.45% on 30/09/2025 → 4.09%, T1). It is wider than at the Feb peak, because prices fell further than yields rose.

**(b) Weekly factor model** (bank composite TR on the non-bank equity basket, ΔMGS10Y [BNM daily, T1], ΔUST10Y, MYR, Brent; estimated 01/2025–07/2026; n = 79, R² = 0.33; HC1 SE). Coefficients: non-bank β 0.38 (t 4.9); ΔMGS +0.10%/bp (t 2.8, **positive**, which reflects the 2025 NIM-relief channel); ΔUST −0.03%/bp (t −1.8); MYR 0.70 (t 2.6); Brent ~0.

{{M2_FACTORS}}

→ Macro factors do **not** explain the fall.
- The only negative contributions are UST (−3.0pp since the peak) and MYR (−2.4pp, concentrated in leg 1).
- The **sector-specific residual is −9.1pp in leg 1 and −7.0pp in leg 2**. That is the footprint of flows and rotation, the KLCI-50 reweight, earnings-visibility concerns and the Maybank capital event.
- The domestic-yield channel works through MTM/NOII visibility and relative yield. It is not captured by a simple beta.

**(c) Local institutions: net substantial-shareholder transactions** (Bursa filings via klsescreener transcription; RM m at current price). This covers holders ≥5% only, so it understates total activity.

{{M2_LOCAL}}

→ Local institutions are not providing a floor. EPF cut **PBBANK by ~RM1.9b YTD** and RHB by ~RM0.8b, and trimmed MAYBANK by ~RM0.8b in Aug–Sep. KWAP (+RM0.8b PBBANK) and PNB (+RM0.7b MAYBANK) partly offset.

### 3.2 Driver Attribution Table

Base = composite price decline of −10.9% from 11/02/2026. The "% of decline" column sums to ~100% (38% mechanical dividends + 62% economic de-rating). Allocations within the 62% are analyst estimates anchored on 3.1(a)–(c).

| # | Driver | Cat. | Direction / evidence | Status | Est. % of decline | Persistence | Conf. | Tier |
|---|---|---|---|---|---|---|---|---|
| 14 | Ex-dividend mechanics; post-ex-div selling | B | 38% of composite price DD (MAYBANK 12/03 RM0.33 + 23/09 RM0.31; CIMB 16/03 + 15/09; PBB 10/09; RHB 14/09) | **Confirmed** | **38%** | Transitory (mechanical) | H | T1/T3 |
| 10/13 | Foreign net selling of Financial Services + rotation to utilities/DC/construction/plantation | B | FS the largest weekly outflow in most weeks from w/e 14/08: −RM245.5m (w/e 28/08), −RM462.9m (Merdeka wk), −RM309.7m (w/e 18/09 while market +RM127m), −RM162.5m (w/e 25/09); MAYBANK/AMMB led w/e 14/08 (−RM623.6m). Non-bank basket +12.2% vs banks −5.0% TR since peak; factor residual −9.1pp / −7.0pp | **Confirmed** | **25%** | Cyclical | H | T2 (MBSB via Edge/NST/FocusM) |
| 3/28 | Global yield & risk-premium shock (Fed/UST, oil-inflation) → higher COE | A/D | UST10Y +105bp since 11/02 to 5.26%; Brent $72 → ~$120 → $96 (war from 28/02); factor model UST −3.0pp; implied ERP now at 10y median, meaning P/B fell ≈ in line with rf | **Confirmed** | **12%** | Cyclical | M | T1/T2/T3 |
| 5/20/25 | Middle East conflict → SME/provision fears; soft 1Q26 (MAYBANK 23% of consensus, CIMB dip, PBB flat); small negative revisions | A/C | 28/05 MAYBANK −4.0% (1.8× vol); overlays +RM0.3b to RM2.6b; BNM RM5b SME facility; FY26 cons EPS −0.7% to −1.9% (90d) for majors (HLB +0.1%), BIMB −2.2%, AFFIN −7.0%. **But GIL at record lows** (CIMB 1.6% ATL, PBB 0.54%, HLB 0.57%) | **Partially** | **8%** | Cyclical | M | T1/T2/T3 |
| 2 | MGS 10Y spike / DY-spread compression / FVOCI MTM | A | MGS 3.45% (30/09/25) → 4.09% (29/09/26), peak 4.18% on 11/09; DY-MGS spread narrower YoY at 7/9 banks; HLIB: a 30bp shock costs ~10% of NOII at AMMB/BIMB and ~4.5% at CIMB; FVOCI BV hit ~1%. In-sample MGS beta is positive, so the effect runs via visibility, not mechanics | **Partially** | **5%** | Cyclical | M | T1/T2 |
| 3/9 | MYR weakness & regional-sub translation (IDR) | A | MYR −3.5% in leg 1 (factor −2.4pp); since recovered (KL USD/MYR ref 4.0792, +0.8% YTD); IDR 17,860; Maybank group loans +2.7% vs Malaysia +5.5% | **Partially** | **4%** | Transitory | M | T1/T3 |
| 11 | FBM KLCI-50 revamp (announced 20/08; 50% 21/12/2026, 100% 21/06/2027; FS weight 42.8% → 36.8%) | B | Timing matches leg 2; largest dilution MAYBANK/PBB/CIMB; flow size not quantifiable (no passive AUM data) | **Partially** | **4%** | Transitory (supply overhang to 06/2027) | M | T2 |
| 21/22 | Maybank Etiqa buyout (RM4.83b, 03/08) → CET1 drag, DRP for 2026 | C | CET1 −0.8pp by our arithmetic (RM4.83b / RWA ≈ RM580b) vs "~2pp" (broker via The Edge); DRP 5 sen of 31 sen; MAYBANK leg 2 −7.6% TR | **Partially** (Maybank-specific) | **2%** | Transitory | M | T2/analyst |
| 16/23 | NIM compression / deposit competition / digital banks | C | Mixed: MAYBANK +10bp YoY (2.10%), AFFIN +3bp, RHB −2bp, AMMB −8bp, CIMB −4bp QoQ, PBB NII −0.2% YoY; GXBank 12m FD 3.85% vs MAYBANK 3.55%; sector median NIM 2.08% vs 2.09% | **Partially** | **2%** | Cyclical (structural for PBB) | M | T1/T2 |
| 12 | Local institutions (EPF/KWAP/PNB) | B | EPF −RM1.9b PBBANK YTD; aggregate ≈ −RM0.5b; local institutions −RM368m w/e 18/09 | **Confirmed** (partial data) | in 25% | Cyclical | M | T1 via T3 |
| 18 | Non-interest income quality (treasury-propped 1H26) | C | Treasury/markets income >20% growth at CIMB/PBB/ABMB/HLB; "core lending did not drive the result"; AMMB NII growth from investment securities (Kenanga) | **Confirmed** | in 8%/5% | Cyclical | M | T2 |
| 15 | Broker rating / TP actions | B | HLIB 30/09: CIMB, RHB, AMMB → Hold; PBB → Buy (top pick). Consensus TP mean still above price (MAYBANK RM11.86, CIMB RM8.89) | **Partially** | in 25% | Transitory | M | T2/T3 |
| 24 | Guidance slippage | C | MAYBANK 1H26 ROE 11.6% vs 11.8% target; PBB flagged downside risks (1Q); RHB guided ROE up | **Partially** | <1% | Cyclical | M | T2 |
| 1 | OPR path | A | Held 2.75% at every 2026 MPC (22/01, 05/03, 07/05, 09/07, 03/09); no cut priced; supportive for NIM | **Not supported** | 0% | — | H | T1 |
| 4 | Domestic growth / household debt | A | 1H26 GDP +5.7%; 2026F raised to ~5% | **Not supported** | 0% | — | H | T1 |
| 6 | Inflation / subsidy rationalisation → retail AQ | A | CPI 1.8% (Jan–Jul); no GIL evidence; consumer-banking PBT −0.4% (median) | **Unverified** | 0% | Watch | L | T1/T2 |
| 7 | Budget 2027 (09/10/2026) levy/SRR/Basel changes | A | No bank-levy proposal found; Pre-Budget Statement 18/08 | **Unverified** | 0% | Event risk | L | T2 |
| 8 | Property/construction cycle | A | Construction/property names leading the market; no AQ signal | **Not supported** | 0% | — | M | T3 |
| 17 | Loan growth | C | Healthy: HLB +7.7%, AMMB +7%, ABMB +9.5%, AFFIN +13.6%, PBB +5.9% ann. | **Not supported** (positive) | 0% | — | H | T1/T2 |
| 19 | Opex / CIR | C | Stable or improving (MAYBANK opex −5.3% YoY; AFFIN CIR 63% from 68.9%) | **Not supported** | 0% | — | H | T1/T2 |
| 26 | Regulatory / legal / one-offs | C | None identified in 2026 | **Not supported** | 0% | — | M | — |
| 27 | De-rating decomposition | D | ~100% multiple; EPS +0.1% to +5.8% | **Confirmed** (framing) | (= the 62%) | — | H | computed |
| + | Jan–Feb 2026 rally round-trip | — | Composite YTD price only −1.1%; KLCI peaked 27/01 | **Confirmed** (context) | — | — | H | T3 |
| 15b | Short interest | B | Not available (Bursa site blocked from this environment) | **Unverified** | — | — | — | — |

**Verdict on the dominant three drivers.**
1. **Flows and rotation (~25% of the price decline, ~40% of the economic part).** Foreigners have used Malaysian financials as the funding leg for a rotation into utilities, data-centre, construction and plantation beneficiaries. EPF is trimming PBBANK and RHB, and the KLCI-50 revamp adds a benchmark-weight overhang to 06/2027.
2. **The global rate/oil risk-premium shock (~12% + 5% via MGS/MTM).** UST +105bp and MGS +53bp since the peak lifted the market's required return. The P/B compression is almost exactly what the risk-free move implies, which is why implied ERP sits at its 10y median.
3. **Earnings-visibility erosion (~8%).** This is not an earnings collapse. Core lending earnings are soft, 1H profits were propped by treasury income that the Q3 MGS spike will partly reverse (MTM), and Middle East provisioning risk drives overlays. Revisions are only −1% to −2%.

Stripping the 38% of dividend mechanics leaves a **multiple-only de-rating on intact EPS**. Two of the three drivers (flows, global rates) are watch items under the anti-churn rule, not fundamental impairments.

---

## 4. Fundamentals scorecard (Module 3)

**Scorecard weights** (declared in `src/m34_fund_valuation.py`, adjustable): core ROE 20%, ROE trend 10%, EPS growth 10%, revisions 10%, NIM trend 10%, asset quality (GIL + LLC) 10%, credit cost 5%, CET1 10%, CIR 5%, dividend sustainability (payout closest to 55%) 10%. Scores are percentile ranks within the universe; missing KPIs score neutral (0.5), and coverage is shown.

{{M3_SCORE}}

*KPI sources: MAYBANK 1Q26 release (T1) + The Edge 27/08/2026 (T2); CIMB 2Q26 release (T1); HLB FY26 release 27/08/2026 (T1); Alliance 1QFY27 release (T1); PBB The Edge 26/08/2026; RHB The Edge/Star 28/08/2026; AMMB Star 18/08/2026; AFFIN Star 14/08/2026 (T2). Consensus: Yahoo (T3). ROE, EPS, DPS and payout are computed from Bursa quarterly filings (klsescreener transcription, T3 of T1).*

{{M3_ROE12Q}}

**Read-across**
- **MAYBANK ranks #1 on fundamentals.** ROE is ~1 SD above its 10y average (z +0.97), NIM is up 10bp YoY, and CET1 of 14.96% leaves room for the Etiqa deduction. Its weakness is valuation (§5), not fundamentals.
- **PBBANK is the only large bank with ROE drifting lower over 12 quarters** (13.5% → 12.2%, z −0.79). Breadth is also negative (0 up / 10 down on FY26).
- **HLB has the best momentum.** EPS +6.0%, revision breadth +0.32, CIR 37.6%, GIL 0.57%. Its caveats are the lowest CET1 among the majors (12.9%) and LLC of 79.5% (244% including the regulatory reserve).
- **CIMB, RHB and AMMB carry ROE ~1pp above their 10y averages (z ≈ +0.95).** That is near-peak profitability, not trough.
- **BIMB fails the >3% core-vs-reported check.** FY25 normalized income is 9.1% below reported, so core ROE is ~6.3% vs the 7.0% headline. ROE z −1.3.
- **AFFIN is the weakest franchise.** ROE 4.4%, profit −11%, CIR 63%, consensus −7% over 90d.

---

## 5. Valuation vs history (Module 4)

### 5.1 Bands (monthly, point-in-time BVPS and ROE mapped by announcement date; BIMB from 2009)

{{M4_BANDS}}

**The ROE reset is visible in the data.** Average core ROE fell from ~15% (2007–15) to ~10.5% (2016–26) at MAYBANK, from 23.5% to 13.6% at PBBANK, and from 14.7% to 8.8% at CIMB. P/Bs reset with it. **20y percentiles are therefore a false anchor.** On the relevant post-reset 10y bands:
- **Cheap:** PBBANK (17th percentile), HLB (26th), AFFIN (26th), BIMB (0th, a record low).
- **Mid:** ALLIANCE (53rd), MAYBANK (64th).
- **Expensive vs own history:** CIMB (81st), RHB (86th), AMMB (94th).

### 5.2 The core test: cheap after ROE, or cheap because ROE is lower?

{{M4_REGR}}

*TS = each bank's own monthly P/B-on-core-ROE regression. Gordon: P/B = (ROE−g)/(COE−g), with g = ROE×(1−payout) bounded 2–5%, COE = MGS10Y 4.09% + β_Blume × 6.0% ERP, β from 3y weekly vs KLCI. XS = today's cross-section across the 9 banks: P/B = −0.27 + 13.1×ROE (R² 0.91).*

**Result**
1. **Below the ROE line at every bank, but only modestly.** Sector residual is −0.54 SD. Largest discounts: HLB −0.87 SD, PBB −0.68, CIMB −0.65. Smallest: AMMB −0.19, RHB −0.24, MAYBANK −0.37.
2. **After adjusting for rates, value disappears.** Implied ERP sits at the **37th–57th percentile of the 10y history for every major**, and the sector is at the 50th. The MGS move has absorbed the de-rating.
3. **Gordon at COE = MGS + β×6%:**
   - Cheap: HLB (fair 1.41× vs 1.15×) and RHB (1.24× vs 0.97×).
   - Fair: MAYBANK (1.30× vs 1.31×).
   - Rich: PBB (1.31× vs 1.48×), CIMB (0.94× vs 1.20×, driven by its 1.26 beta) and AMMB (0.89× vs 1.00×).
   - With β = 1 for all, every major lands within ±13% of fair.
4. **Cross-sectionally:** cheapest for their ROE are ALLIANCE (−0.12), RHB (−0.11), BIMB and HLB. Richest are PBBANK (+0.16) and MAYBANK (+0.11), a quality premium.
5. **The MGS-augmented TS regression is rejected as causal.** Its MGS coefficient is positive because MGS and P/B co-trended down over 2007–2021.

**Sector relative (bank vs KLCI P/B) is a data gap.** A KLCI P/B history was not retrievable (Bursa blocked). The proxy is relative performance, where banks trail KLCI by 5.2pp since the high and the non-bank basket by ~13pp YTD.

---

## 6. Historical analogs (Module 5)

### 6.1 Every bank-sector drawdown ≥15% from its rolling 52w high since 2000 (cap-weighted composite TR)

{{M5_EPISODES}}

*Type rule: ROE reset = ROE down ≥2.5pp at +24m with no EPS recovery; EPS-led = EPS −5% or worse peak-to-trough or over the next 12m; otherwise multiple-only. "Hit −6.7%" = first date the episode reached today's composite depth. Fundamentals start 2003.*

### 6.2 Which episode does today resemble on fundamentals, not price? (≥8% episodes since 2008, standardised distance)

{{M5_SIMILARITY}}

**Closest match: the 2013 taper tantrum** (distance 1.84, excluding 2026's own leg 1):
- **Same shock and starting point.** MGS +55bp (now +59bp), ROE at its 5y average, P/B near its 5y mean, EPS intact.
- **Outcome.** A −9% drawdown, then **+13% at 12m but −1.5% at 36m**, because it was followed by the 2014–16 oil/1MDB/ringgit **ROE reset**.

Next closest are 2025 (tariff shock: +25% at 12m) and 2018 (GE14/EM: +8% at 12m, +6% at 36m). Today is a *multiple-only de-rating*, historically the strongest entry type. The analog shows the risk is not the next 12m but whether ROE (near the top of its 10y range) holds.

### 6.3 Base rates: entering at today's drawdown depth (first crossing of the current TR depth from the rolling 52w high; re-armed after half-recovery)

{{M5_BASERATES}}

*A valuation-conditioned sample (sector P/B within ±10% of 1.23× and ROE within ±1.5pp of 11.1%; 1,044 overlapping days, 2016–25) gives an 83% 12m hit rate, +10.4% median, and −2.7% at the 10th percentile.*

**Read:** the quality names at today's depth have strong base rates (PBB 84% / +15%, HLB 83% / +7%, MAYBANK 73% / +7%). **RHB and AMMB historically kept falling** from similar depths (47% hit rates; median further drawdown −22% and −17%). AFFIN is a coin-flip with a −18% median further drawdown.

---

## 7. Forward scenarios (Module 6): 12m, MYR and USD

Declared in `src/m6_scenarios.py`:
- **EPS base:** 12m-forward EPS is the FY-weighted consensus (T3); DPS = TTM payout (bounded 30–90%) × EPS.
- **Bull:** EPS ×1.03; P/B moves to max(10y −0.5SD, ROE-fair TS P/B); MYR +3%.
- **Base:** EPS ×0.98; P/B unchanged.
- **Bear:** +25bp credit cost, −5bp NIM, −5% fees. P/B goes to the midpoint of 10y −1.5SD and Gordon at bear ROE with COE +50bp, floored at 85% of the 20y minimum. MYR −5%.
- **Balance-sheet proxies (flagged):** loans = max(Yahoo net loans, 0.65×TA), HLB RM226.3b reported; IEA = 0.9×TA; fees = 15% of revenue; RWA = 0.55×TA.

{{M6_SCEN}}

**Probability rationale**
- **HLB (30/50/20):** positive revisions, lowest bear P/B gap, EPS +6%.
- **PBB (25/55/20):** quality floor, offset by an ROE drift and negative breadth.
- **MAYBANK (25/50/25):** fairly priced, 6.4% yield, capital known.
- **CIMB (20/50/30):** top of its 10y band, highest β and credit cost, IDR exposure.
- **RHB (20/50/30):** top of its band, weak base rates.
- **AMMB (20/45/35):** 94th-percentile P/B, NIM −8bp, highest MTM sensitivity.
- **BIMB (20/45/35):** ROE falling, core below reported.
- **ALLIANCE (25/50/25):** momentum vs a credit cost at an unsustainable 0.3bp.
- **AFFIN (15/45/40):** ROE 4.4%, −7% revisions.

**Sector (cap-weighted):** bull +23.9% / base +10.1% / bear −19.4% → **E[TR] +5.5% MYR (+5.4% USD)**.

### 7.1 Full stress (+50bp credit cost, −10bp NIM, −10% fees; one year; dividends capped at 90% of stress EPS)

{{M6_STRESS}}

**Read-across**
- **Dividend cover under full stress** stays >1× everywhere except **MAYBANK (0.90×: DPS −19%)**, **BIMB (0.48×)** and **AFFIN (0.83×)**. MAYBANK's 6.4% yield is the most stress-sensitive of the majors because its payout is ~74%.
- **CET1 absorbs a stress year with a 35–70bp hit.**
- **MAYBANK capital.** Post-Etiqa CET1 is ~14.1% (14.96% − 83bp, assuming the full RM4.83b is deducted against RWA ≈ RM580b), and ~13.8% after a stress year. That is above any plausible 12.5–13% management floor.

### 7.2 Price references from the bands (secondary to fundamental triggers)

{{M7_LEVELS}}

---

## 8. Verdict & execution plan (Module 7)

### 8.1 Sector

| | Verdict |
|---|---|
| **Fundamentals verdict** | **Sound but peak-ish.** EPS intact, asset quality at record highs, capital ample. ROE is at its 10y high, so earnings upside is limited and the 2013 → 2014–16 template is the tail risk. |
| **Timing verdict** | **Not yet.** Flows are still negative (FS outflows most weeks since mid-Aug; KLCI-50 overhang to 06/2027). 3Q26 results (late Nov) will carry the Q3 MGS MTM hit. MGS 4.09% keeps the hurdle high. |
| **Sector call** | **SCALE-IN ON TRIGGERS, selectively. Confidence 65%.** E[TR] +5.5% ≈ MGS + 1.4pp is not enough to own the whole sector. Own the names where valuation or revisions do the work. |

### 8.2 Bank-by-bank

| Bank | Verdict | Conf. | Single most important reason | Fundamentals vs timing |
|---|---|---|---|---|
| **HLBANK** | **ACCUMULATE NOW** (T1), T2/T3 on triggers | 65% | Only major that is cheap on every lens (10y P/B 26th percentile, −0.87 SD vs ROE line, Gordon 1.41× vs 1.15×) **with positive revision breadth** (7 up / 2 down) and the smallest bear case (−7.8%) | Fundamentals: strong. Timing: acceptable now. The 80 sen final goes ex ~early/mid-Oct (FY25 precedent 08/10/2025). |
| **PBBANK** | **SCALE-IN ON TRIGGERS** (small T1) | 60% | Cheap vs its own 10y band (17th percentile) with the best asset quality (GIL 0.54%, LLC 139%) — **but ROE is drifting down and EPF sold ~RM1.9b** | Fundamentals: high quality, slowly eroding NIM. Timing: wait for NIM stabilisation. |
| **MAYBANK** | **SCALE-IN ON TRIGGERS** (T1 yield carry) | 55% | 6.4% yield (+2.3pp over MGS), fair on Gordon, EPS intact, but **P/B at the 64th percentile of its 10y band** and 2026 DRP caps dividend upside | Fundamentals: #1 scorecard. Timing: KLCI-50 dilution and Etiqa capital clarity pending. |
| **ALLIANCE** | **SCALE-IN ON TRIGGERS** (half T1) | 55% | Cheapest vs ROE cross-sectionally (−0.12), profit +25%, loans +9.5%, positive revisions (7/1), E[TR] +11.8% | Fundamentals: momentum. Risk: credit cost 0.3bp must normalise. Timing: 2QFY27 results (late Nov). |
| **CIMB** | **WAIT** | 60% | P/B at the **81st percentile of its 10y band**, 28% above Gordon; highest credit cost (38bp) and β; revision breadth −0.40 | Trigger: P/B ≤1.05× (~RM6.85) *or* 3Q26 NIM up QoQ with credit cost ≤35bp. |
| **RHBBANK** | **WAIT** | 55% | P/B at the 86th percentile of its 10y band; history at this depth is poor (47% hit, −22% median further drawdown); HLIB → Hold | Trigger: P/B ≤0.87× (10y mean, ~RM6.80) *or* FY26 ROE ≥10.5% reaffirmed at 3Q. |
| **AMBANK** | **WAIT** (verging on AVOID) | 60% | **P/B at the 94th percentile of its 10y band (z +1.7)**, NIM −8bp YoY, NII growth reliant on investment securities, highest MTM sensitivity (~10% of NOII per 30bp) | Trigger: P/B ≤0.85× (~RM5.50) *or* NIM ≥2.0% with credit cost ≤20bp. |
| **BIMB** | **AVOID** | 55% | Record-low P/B is a **value trap**: core ROE ~6.3% and falling (z −1.3), core 9% below reported, 7 of 8 analysts Hold | Revisit on two consecutive quarters of core ROE ≥7.5%. |
| **AFFIN** | **AVOID** | 70% | ROE 4.4%, consensus −7% over 90d (0 up / 9 down), profit −11%, E[TR] −7.9% | Revisit on ROE ≥6% with positive revisions. |

**Best pick: HLBANK.** It is the only name where quality, valuation and revision momentum align. The runner-up for higher-beta mandates is ALLIANCE.
**Worst pick: AFFIN,** followed by AMBANK on valuation.
**Quality vs cheapness:** PBB's premium (1.48×) is now *below* its own history but *above* the cross-sectional ROE line, so you are paying for asset quality while ROE drifts. The "discounts" at CIMB, RHB and AMBANK are illusory: each trades near the top of its own post-2016 band on near-peak ROE.

### 8.3 Tranche plan: fundamental triggers first, prices as secondary references

| Tranche | When | Names & size (share of intended sleeve) | Fundamental trigger (must hold) | Price reference (secondary) |
|---|---|---|---|---|
| **T1** | Now (30/09/2026 onwards) | HLB 40% of the HLB allocation; PBB, MAYBANK and ALLIANCE 25–33% each | Valuation (HLB/PBB below the 10y mean; MAYBANK DY −MGS ≥ +2pp), EPS intact, no guidance cut | HLB ≤RM24.5 (−0.5SD); PBB ≤RM5.16 (−0.5SD); MAYBANK ≤RM10.5 (DY −MGS ≥2pp) |
| **T2** | 3Q26 results window (MAYBANK/CIMB/PBB/RHB ~20–28/11/2026; HLB 1QFY27 ~27/11; AMMB/ALLIANCE 2QFY27 ~late Nov) | Add the next third | (a) NIM flat-to-up QoQ; (b) credit cost within guidance, no new overlays; (c) Q3 MTM/treasury hit <10% of NOII; (d) 30d revision breadth ≥0; (e) MAYBANK discloses post-Etiqa CET1 ≥13.5% with DPS policy intact | MAYBANK ≤RM9.3 (−0.5SD); PBB ≤RM4.60 (−1SD); HLB ≤RM22.5 (−1SD) |
| **T3** | After KLCI-50 phase 1 (21/12/2026) and FY26 results (late Feb 2027) | Final third; open CIMB or RHB only if their WAIT triggers hit | Foreign FS flows net positive 4 consecutive weeks **and** (MGS 10Y ≤3.9% **or** consensus FY27 revisions turn up); FY27 ROE guidance ≥ FY26 | CIMB ≤RM6.85; RHB ≤RM6.80 |

**Invalidation triggers (any one → stop adding and reassess)**
- Sector GIL up >20bp QoQ, or credit cost >40bp at any major.
- FY27 ROE guidance cut below 11% (MAYBANK) or 11.5% (HLB).
- A DPS cut or payout below stated policy.
- MAYBANK post-Etiqa CET1 <13%, or HLB CET1 <12.5%.
- MGS 10Y >4.5% sustained (+40bp ≈ −6% to −8% on Gordon P/B).
- Brent >US$120 sustained or renewed Hormuz closure (SME/consumer stress beyond overlays).
- A Budget 2027 bank-specific levy (09/10/2026).

### 8.4 CASH_BUFFER_CHECK (IBKR, read-only snapshot, 30/09/2026) — PERSONAL

**Account snapshot**
- Net liquidation **USD 43,372**; cash **USD 3,852 (8.9%)**; gross position value USD 39,516; leverage 0.91.
- **~91% is in one theme** (US semis/AI hardware: AMAT, MU, SOXX, LRCX, ARM, AVGO, QCOM, VRT, BE), plus a HKD warrant (45757) worth ~USD 62.
- **No Malaysian financials.**

Applying the portfolio-reallocation-discipline rules:
- **No trims to fund this.** Nothing in this analysis establishes fundamental deterioration in the semis book, so no existing holding passes the "standalone sell test". Concentration in one theme is a separate review item, not a funding source.
- **Capital comes from cash above the 6–8% floor only.** Deployable now: **USD 382 (at an 8% floor) to USD 1,250 (at 6%), i.e., RM1.6–5.1k.** That funds T1 only.
- **T1 at the 6% floor:** HLB 100 shares (RM2,336 ≈ USD 573, 1.3% of NLV), plus MAYBANK 100 (RM1,004), plus PBB 200 (RM940), plus ALLIANCE 100 (RM469). Total ≈ RM4.75k ≈ USD 1.16k ≈ 2.7% of NLV, inside the 6% floor.
- **T2/T3 should be funded by new cash inflows,** or deferred if none arrive. Do not manufacture exits.
- **Target sleeve:** 5–8% of NLV in Malaysian banks over time (a "new entry" of 3–5%, rising to a satellite of ≤8%). It diversifies a one-theme book: the banks' weekly β to KLCI is 0.7–1.3, and their dividend income in MYR is single-tier with no Malaysian withholding.
- **Execution:** convert USD→MYR at IBKR (MYR ref 4.0792); trade in board lots of 100; limit orders only (Bursa liquidity is fine for these sizes).
- **Context mismatch flagged:** the skill's documented portfolio (VOO anchor, MSFT/META, ~USD 52k) does not match the connected account. Confirm which account this plan is for before acting.

### 8.5 CLIENT_HLPB (higher capital-protection bar)

- **Suitability:** income-seeking clients with a horizon of ≥3 years only. A 36m horizon matters because the 2013 analog was flat after 3 years.
- **Name choice:** restrict to HLB, PBB and MAYBANK. Avoid AFFIN, BIMB and AMMB.
- **Concentration cap:** Malaysian financials ≤20% of the equity sleeve and ≤7% per bank, *including* existing HLFG/HLB exposure.
- **Preferred route: direct equity for dividend yield** (MAYBANK 6.4%, PBB 4.8%, HLB 4.2%). This gives full upside participation and keeps the dividend stream.
- **ELN overlay (only if the client explicitly wants enhanced carry and accepts share delivery).** Indicative 6m ELN, 92% strike, European, before issuer margin:

| Underlying | Spot | Strike (92%) | Indicative coupon p.a. | If spot at maturity = bear-case 12m price | If −20% at maturity |
|---|---|---|---|---|---|
| MAYBANK | 10.04 | 9.24 | ~6.6% | 7.99 → **−10.2%** on notional (shares delivered at 9.24, MTM loss net of coupon) | 8.03 → **−9.7%** |
| PBBANK | 4.70 | 4.32 | ~7.1% | 3.65 → **−12.1%** | 3.76 → **−9.5%** |
| HLBANK | 23.36 | 21.49 | ~8.2% | 20.52 → **−0.4%** | 18.69 → **−8.9%** |

**ELN verdict: not preferred.**
- The coupon (6.6–8.2% before margin) is only ~0–2pp above the stocks' own dividend yields.
- Upside is surrendered in exactly the scenario (bull +16% to +29%) where the thesis pays.
- The downside is almost the full equity downside.

**KIKO: not recommended.** It carries the same downside as the ELN, while the knock-out also truncates the upside that makes the entry worthwhile. Risk disclosure applies: capital is at risk; share delivery at strike; issuer credit risk; limited secondary liquidity.

---

## 9. Confidence, conflicts, what I don't know (Module 8)

### 9.1 Source conflicts and rulings

| Conflict | Sources | Ruling |
|---|---|---|
| Maybank CET1 impact of the Etiqa buyout: "~2pp" vs our arithmetic | The Edge node/813262, 08/2026, quoting a research house (T2) vs RM4.83b / RWA≈RM580b = −0.83pp | **Arithmetic wins at group level (~−0.8 to −0.9pp → ~14.1%).** The 2pp figure likely refers to bank-entity CET1 (unverified). Resolve with the 3Q26 Pillar 3 disclosure. |
| "Etiqa buyout" vs "Ageas EUR1.1b stake purchase" (seed list treats them as two) | The Star 03/08/2026; Coverager; Bloomberg (T2) | **Same transaction:** RM4.83b for Ageas's 30.95% of Maybank Ageas Holdings (≈ EUR1.1b). Not double-counted. |
| YTD 2026 foreign net outflow: RM7.62b (early Sep) vs RM20.94b (mid-Sep) | Search summaries of MBSB/MIDF coverage (T2, not directly verifiable; MIDF site and BusinessToday blocked) | **Neither used as a number.** The weekly prints (T2) are internally consistent with the lower figure. RM20.94b is likely mis-dated. Flagged as a gap. |
| MGS 10Y level | BNM FMIP 4.09% (29/09) vs press 3.94% (25/09) vs HLIB peak 4.18% (11/09) | **All consistent (different dates).** BNM T1 used for level; HLIB for the peak. |
| Maybank 52w high: seed RM12.42 vs IBKR 12.07 vs Yahoo close 12.38 | IBKR misc_statistics (adjusted), Yahoo raw close | **Yahoo raw close 12.38 (24/02/2026) used.** IBKR's 52w stats are dividend-adjusted; the seed was likely intraday. |
| Maybank 1H26 ROE: 11.6% (Star) vs 12.0% 2Q (Edge) vs 11.2% TTM (computed) | Different bases (1H annualised, quarter, TTM) | TTM core **11.2%** used for all valuation. |
| Yahoo "Net Loan" understates reported loans (HLB 182.8b vs 226.3b reported) | Yahoo (T3) vs HLB release (T1) | Loans modelled as max(Yahoo, 0.65×TA); HLB reported. **Stress EPS sensitivities ±15%.** |

### 9.2 Data gaps and stale inputs
- **KPIs for 12 quarters** (NIM, CASA, GIL, credit cost, CET1) were not systematically retrievable. Bursa, marketscreener and stockanalysis are blocked from this environment.
  - The scorecard uses latest-quarter KPIs. Coverage is 33–67% for RHB, AMMB, ALLIANCE and AFFIN, and 0% for BIMB.
  - Stale items: MAYBANK CET1 (1Q26), ALLIANCE CET1 12.4% (1QFY26).
- **Consensus revisions** come from Yahoo (T3, 7–19 analysts). There was no Bloomberg or S&P access.
- **No KLCI P/B or DY history**, so the sector-relative valuation uses price relatives.
- **Flows:** MIDF/MBSB PDFs are unreachable; weekly prints are from tier-2 press. There is no passive AUM data to size the KLCI-50 flow. Short interest is unavailable.
- **Core earnings, historical:** one-offs were stripped where identified (table below), and the 2022 Cukai Makmur was added back at ×1/0.90 (approximate). COVID-era modification losses and provisions are *not* stripped. The current four quarters needed no adjustment except the BIMB haircut.

{{CORE_ADJ}}

- **Balance-sheet proxies in the stress test** are listed in §7. Treat the stress-EPS sensitivities as ±15%.

### 9.3 Five data points that would flip the verdict

1. **3Q26 NIM and credit cost (late Nov).** A QoQ NIM drop of ≥5bp at PBB or MAYBANK, or credit cost >30bp at a major, flips SCALE-IN → WAIT. If both are benign, T2 goes ahead and the sector call moves to ACCUMULATE.
2. **MAYBANK post-Etiqa CET1 and DPS guidance.** CET1 <13.5% or a payout-policy cut flips MAYBANK → WAIT.
3. **MGS 10Y path.** Above 4.5% sustained, Gordon fair P/B falls 6–8% and the sector moves to WAIT. At or below 3.8%, rates stop being a headwind and the timing verdict moves to supportive.
4. **Consensus revision breadth.** If it turns ≥0 for PBB and CIMB, those names move up to T1/T2. If HLB's breadth turns negative, HLB drops to SCALE-IN.
5. **Budget 2027 (09/10/2026).** Any bank-specific levy (e.g., a Cukai Makmur repeat) is a direct ROE hit of ~1pp. That flips everything to WAIT pending quantification.

### 9.4 Catalyst calendar (DD/MM/YYYY)

| Date | Event | Tier |
|---|---|---|
| ~early–mid 10/2026 | HLBANK final DPS 80 sen ex-date (FY25 precedent 08/10/2025) | T1 (dividend declared 27/08/2026); date estimated |
| 09/10/2026 | Budget 2027 tabled | T2 (Star, Dewan Rakyat calendar) |
| 05/11/2026 | BNM MPC (final 2026 meeting) | T2 (BNM schedule via search) |
| ~12/11/2026; eff. ~30/11/2026 | MSCI Nov-2026 index review (standard calendar; verify) | Estimated |
| ~17–28/11/2026 | 3Q26 results: PBB (~17/11, 2025 precedent), AFFIN (~20/11), MAYBANK (~21/11), ALLIANCE 2QFY27 (~25/11), AMMB 2QFY27 (~26/11), RHB/HLB 1QFY27/CIMB/BIMB (~27–28/11) | Estimated from 2025 announcement dates (T3 of T1) |
| ~10–12/12/2026 | AMMB, ALLIANCE, BIMB, CIMB interim ex-dates (2025 precedent) | Estimated |
| 21/12/2026 | FBM KLCI-50 phase 1 (20 new constituents at 50% weight) | T2 (Star 20/08/2026) |
| late 01/2027 | BNM MPC (first 2027 meeting; 2026 precedent 22/01) | Estimated |
| ~25–28/02/2027 | FY26 results and final DPS (MAYBANK, PBB, CIMB, RHB, BIMB, AFFIN); FY27 ROE targets | Estimated |
| ~11–16/03/2027 | MAYBANK, PBB, CIMB, RHB, HLB ex-dates (2026 precedent) | Estimated |
| 21/06/2027 | FBM KLCI-50 phase 2 (100% weight) | T2 |

---

## 10. Source log

| # | Data point(s) | Tier | Source | Date of data / retrieved |
|---|---|---|---|---|
| 1 | OPR 2.75% and 2026 MPC decisions (22/01, 05/03, 07/05, 03/09) | T1 | BNM Open API `api.bnm.gov.my/public/opr` | 03/09/2026 / 30/09/2026 |
| 2 | MPC statement: 1H26 GDP 5.7%, 2026F ~5%, CPI 1.8% / core 2.0% Jan–Jul, Middle East risk | T1 | bnm.gov.my Monetary Policy Statement 03/09/2026 | 03/09/2026 / 30/09/2026 |
| 3 | MGS 10Y/3Y/5Y/7Y monthly 09/2006–09/2026 and daily 01/2025–09/2026; MGS10Y 4.09% on 29/09/2026; KL USD/MYR ref 4.0792 on 30/09/2026 | T1 | BNM FMIP `financialmarkets.bnm.gov.my/benchmark-yields` | 29/09/2026 / 30/09/2026 |
| 4 | Quarterly EPS, DPS, NTA (BVPS), PATAMI, announcement dates 2002–2Q26; substantial-shareholder filings | T3 of T1 | klsescreener.com transcription of Bursa quarterly reports | 30/09/2026 |
| 5 | Daily OHLCV, dividends, splits (9 banks, KLCI, 8 ASEAN peers, 12 KLCI non-banks, FX, UST10Y, Brent, DXY) | T3 | Yahoo Finance via yfinance | 30/09/2026 |
| 6 | MAYBANK last RM10.04, dividend yield 6.41%, 52w stats (adjusted) | T3 (broker feed, delayed) | IBKR market data | 30/09/2026 |
| 7 | FY financials (TA, net loans, NII, revenue, tax, normalized income); consensus EPS trend, revisions, TPs, recommendations | T3 | Yahoo Finance | 30/09/2026 |
| 8 | Maybank 1Q26: NIM 2.14%, CASA 41.1%, CIR 49.9%, GIL 1.34%, LLC 104.4%, CET1 14.96%, NCC 10bp | T1 | maybank.com news 28/05/2026 | 28/05/2026 / 30/09/2026 |
| 9 | Maybank 2Q26: NP RM2.69b (+2.4%), NIM 2.10% (+10bp YoY), LLC 103.1%, loans +2.7%, DPS 31 sen | T2 | The Edge node/815937; fintechnews.my 04/09/2026 | 27/08/2026 / 30/09/2026 |
| 10 | Maybank 1H26 overlays RM2.6b (+RM0.3b), ROE 11.6% vs 11.8% target, DRP 2026, CGSI TP RM15.20 | T2 | The Star 31/08/2026 | 31/08/2026 |
| 11 | Etiqa: RM4.83b for 30.95% of Maybank Ageas Holdings; "~2pp CET1" (research house); DRP; Kenanga neutral | T2 | The Edge node/813262 & 813072; The Star 03/08/2026 | 08/2026 |
| 12 | CIMB 2Q26: NP RM1.94b, ROE 11.2%, NIM 2.04% (−4bp QoQ), CC 38bp (1H 34bp), GIL 1.6%, CIR 45.2%, CET1 14.0% | T1 | cimb.com newsroom 2Q26 | 08/2026 / 30/09/2026 |
| 13 | PBB 2Q26: NP RM1.82b (+3.7%), NII −0.2%, CIR 35.1%, GIL 0.54%, LLC 138.9%, ROE 12.2%, CET1 13.9%, DPS 10.5 sen | T2 | The Edge node/815772 | 26/08/2026 |
| 14 | HLB FY26: PAT RM4,531m, NIM 1.84%, CASA 34.7%, CIR 37.6%, GIL 0.57%, LIC 79.5% / 244.1%, CET1 12.9%, loans +7.7%, DPS 110 sen, payout 50.4% | T1 | hlb.com.my FY2026 results release | 27/08/2026 |
| 15 | RHB 2Q26: NP RM807m, NIM 1.86% (−2bp), ROE 9.6%, CC guidance 13–14bp, DPS 15 sen; foreign shareholding 22.4% | T2 | The Edge node/816118, node/806528; The Star 28/08/2026 | 06–08/2026 |
| 16 | AMMB 1QFY27: NP RM520m, NIM 1.93% (−8bp), CC 19bp, GIL 1.62%, CIR 43.4%, loans +7% | T2 | The Star 18/08/2026; BusinessToday 19/08/2026 (Kenanga) | 18–19/08/2026 |
| 17 | Alliance 1QFY27: NP RM248.3m (+25%), NIM 2.26%, CIR 47.4%, NCC 0.3bp | T1 | alliancebank.com.my press release | 08/2026 |
| 18 | Affin 2Q26: NP RM127.5m (−11.1%), NIM 1.52% (+3bp), CIR 63%, loans +13.6% | T2 | The Star 14/08/2026; NST | 14/08/2026 |
| 19 | BIMB 2Q26: NP RM139.1m (+9.8%) | T2 | Star/Bernama via search | 27/08/2026 |
| 20 | Sector 1H26: median NP +0.8%, NIM 2.08%, treasury >20% growth at CIMB/PBB/ABMB/HLB; core lending weak | T2 | tabinsights.com | 08/09/2026 |
| 21 | 1Q26 reaction: MAYBANK −4% to RM10.50; 23% of consensus; BNM RM5b SME facility; avg TP RM12.64 | T2 | The Edge node/805238 | 28/05/2026 |
| 22 | HLIB sector note: MGS peak 4.18% (11/09); MTM sensitivities; CIMB/RHB/AMMB → Hold; PBB → Buy | T2 | The Star "Banks face more measured valuation upside" | 30/09/2026 |
| 23 | KLCI 29/09: 1,643.96 (−1.56%), 9-month low; flows foreign −RM142m, local institutions −RM34m, retail +RM176m | T2 | The Star 29/09/2026; Bernama | 29/09/2026 |
| 24 | Weekly foreign flows and FS sector flows (w/e 14/08, 28/08, Merdeka week, 11/09, 18/09, 25/09) | T2 | MBSB Research via The Edge, NST, FocusMalaysia, BusinessToday, TMR (search summaries) | 08–09/2026 |
| 25 | FBM KLCI-50: 30 → 50 constituents; 50% on 21/12/2026, 100% on 21/06/2027; FS weight 42.8% → 36.8% | T2 | The Star 20–21/08/2026; FocusMalaysia | 20/08/2026 |
| 26 | Iran war from 28/02/2026; Brent $72 → ~$120 peak; Hormuz disruption | T2 | CNBC 21/04/2026; IEA OMR 03/2026; World Bank blog | 03–04/2026 |
| 27 | Budget 2027 tabled 09/10/2026; Pre-Budget Statement 18/08/2026 | T2 | The Star 23/07/2026; rates.my | 07–09/2026 |
| 28 | 12m FD: GXBank 3.85%, AEON 3.80%, Maybank/RHB/HLB 3.55% | T3 | Aggregator (ringgitplus/stashaway via search) | 09/2026 |
| 29 | IBKR account snapshot (NLV, cash, positions) | T1 (own account) | IBKR API (read-only) | 30/09/2026 |

*Figures older than one quarter are flagged where used: MAYBANK CET1/CASA/CIR/GIL (1Q26), ALLIANCE CET1 (1QFY26), and Yahoo FY financials (FY25 / FYE Mar-26 / FYE Jun-26).*
