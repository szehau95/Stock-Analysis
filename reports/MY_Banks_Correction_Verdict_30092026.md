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

| name                                 | 52w high (date)      |   Current | Px DD   | TR DD   | TR DD (USD)   | Ex-div share of px DD   | YTD px   | YTD TR   | 1m     | 3m     | vs KLCI since high   | Leg1 TR (trough)   | Leg2 TR (from)   |
|:-------------------------------------|:---------------------|----------:|:--------|:--------|:--------------|:------------------------|:---------|:---------|:-------|:-------|:---------------------|:-------------------|:-----------------|
| MAYBANK                              | 12.38 (24/02/2026)   |     10.04 | -18.9%  | -14.0%  | -18.0%        | 26%                     | -4.2%    | +1.6%    | -6.0%  | -6.5%  | -13.3%               | -13.4% (03/06)     | -7.6% (17/07)    |
| PBBANK                               | 5.28 (04/08/2026)    |      4.7  | -11.0%  | -9.1%   | -8.7%         | 18%                     | +3.5%    | +8.4%    | -5.1%  | -2.9%  | -6.6%                | n/a                | -9.1% (04/08)    |
| CIMB                                 | 8.95 (27/01/2026)    |      7.8  | -12.8%  | -8.3%   | -10.9%        | 35%                     | -5.5%    | -0.5%    | -2.0%  | +4.7%  | -6.4%                | -17.5% (03/06)     | -2.4% (28/09)    |
| HLBANK                               | 25.80 (30/01/2026)   |     23.36 | -9.5%   | -8.2%   | -11.7%        | 13%                     | +5.5%    | +6.9%    | -0.6%  | +9.5%  | -4.6%                | -18.0% (29/05)     | -2.2% (03/09)    |
| RHBBANK                              | 8.88 (10/08/2026)    |      7.53 | -15.2%  | -13.6%  | -13.4%        | 11%                     | -2.3%    | +3.7%    | -13.2% | -8.5%  | -10.7%               | n/a                | -13.6% (10/08)   |
| AMBANK                               | 7.37 (12/08/2026)    |      6.46 | -12.3%  | -12.3%  | -12.1%        | 0%                      | -0.6%    | +2.8%    | -6.4%  | +0.9%  | -7.5%                | n/a                | -12.3% (12/08)   |
| BIMB                                 | 2.54 (12/02/2026)    |      2.05 | -19.3%  | -17.8%  | -21.1%        | 8%                      | -10.5%   | -8.8%    | -2.4%  | -1.4%  | -13.9%               | -16.6% (02/07)     | -6.0% (05/08)    |
| ALLIANCE                             | 5.53 (14/01/2026)    |      4.69 | -15.2%  | -13.4%  | -13.9%        | 12%                     | -7.1%    | -5.2%    | -4.7%  | -1.1%  | -12.0%               | -18.3% (13/04)     | -6.9% (03/09)    |
| AFFIN                                | 2.78 (12/02/2026)    |      2.01 | -27.7%  | -25.2%  | -28.2%        | 9%                      | -14.5%   | -11.5%   | -2.0%  | -10.7% | -22.3%               | -17.0% (09/07)     | -11.5% (16/07)   |
| BANK COMPOSITE (cap-wtd)             | 5.02 (11/02/2026)    |      4.47 | -10.9%  | -6.7%   | -10.4%        | 38%                     | -1.1%    | +3.5%    | -4.8%  | -1.3%  | -5.2%                | -9.4% (03/06)      | -4.6% (05/08)    |
| FBM KLCI                             | 1771.25 (27/01/2026) |   1656.43 | -6.5%   | -6.5%   | -9.1%         | n/a                     | -1.4%    | -1.4%    | -4.0%  | -0.5%  | +0.0%                | -6.5% (01/07)      | -5.3% (26/08)    |
| KLCI ex-banks (algebraic, FS wt 40%) | 1.12 (06/05/2026)    |      1.04 | -6.8%   | -6.8%   | -9.6%         | n/a                     | -1.8%    | -1.8%    | -3.5%  | -0.0%  | -1.1%                | -7.1% (02/07)      | -4.9% (26/08)    |
| Non-bank KLCI basket (EW, 12 names)  | 2.48 (26/08/2026)    |      2.39 | -3.4%   | -3.4%   | -4.4%         | n/a                     | +9.3%    | +9.3%    | -2.4%  | +6.2%  | +1.8%                | n/a                | -3.4% (26/08)    |

*Leg 1 = 52w high to the trough before 15/07/2026. Leg 2 = the Jul–Sep high to 30/09/2026 (TR basis). A blank Leg 1 means the 52w high itself was printed in August, so the bank's whole correction is the Aug–Sep leg.*

**Findings**
- **Ex-dividend mechanics.** 38% of the composite's price drawdown is dividends (MAYBANK 26%, CIMB 35%, PBBANK 18%). In total-return terms, only AFFIN, BIMB, ALLIANCE and CIMB are negative YTD.
- **Two distinct legs.**
  - *Leg 1 (Feb→early Jun: Iran war/oil, soft 1Q26, EM outflows, MYR −3.5%).* It hit MAYBANK, CIMB, HLB, BIMB, ALLIANCE and AFFIN. CIMB and HLB have since recovered 14% off their lows.
  - *Leg 2 (Aug→Sep: global yield spike, financials outflows, KLCI-50 announcement, 2Q results).* It hit PBBANK, RHB and AMMB, which printed **new 52w highs in August** and are now down 9–14% TR.
- **The sector trails KLCI by 5.2pp since its high.** A 12-name non-bank KLCI basket is **+9.3% YTD vs banks −1.1%**, which is rotation, not a market-wide collapse.

### 2.2 Ex-dividend events in the window and drawdown pattern

| name     | Ex-div in window (DD/MM/YYYY:RM)   |   Days TR<=-2% | Top-5 days / max TR DD   | Pattern      |
|:---------|:-----------------------------------|---------------:|:-------------------------|:-------------|
| MAYBANK  | 12/03/2026:0.330; 23/09/2026:0.310 |              7 | 91%                      | event-driven |
| PBBANK   | 10/09/2026:0.105                   |              1 | 79%                      | event-driven |
| CIMB     | 16/03/2026:0.203; 15/09/2026:0.197 |              8 | 93%                      | event-driven |
| HLBANK   | 13/03/2026:0.300                   |              9 | 69%                      | event-driven |
| RHBBANK  | 14/09/2026:0.150                   |              3 | 96%                      | event-driven |
| AMBANK   | nan                                |              4 | 87%                      | event-driven |
| BIMB     | 12/03/2026:0.044                   |              6 | 62%                      | event-driven |
| ALLIANCE | 11/06/2026:0.097                   |             11 | 99%                      | event-driven |
| AFFIN    | 11/05/2026:0.085                   |              7 | 51%                      | mixed        |

The pattern is **event-concentrated**: the top-5 dividend-neutral down days deliver 51–99% of each bank's max TR drawdown, but gap-downs are rare (≤2 days of >2% gap per bank). It reads as orderly selling into a handful of catalyst days rather than a capitulation.

### 2.3 Five largest down days per bank (dividend-neutral TR returns), tagged to catalysts

| bank     | date       | TR day   | Gap at open   | Vol vs 60d   | catalyst                                                                                      |
|:---------|:-----------|:---------|:--------------|:-------------|:----------------------------------------------------------------------------------------------|
| MAYBANK  | 28/05/2026 | -4.0%    | +0.0%         | 1.8x         | 1Q26 results: Maybank/CIMB soft, PBB flat; ME-conflict provision fears; own results window    |
| MAYBANK  | 26/02/2026 | -2.9%    | +0.2%         | 3.8x         | own results window                                                                            |
| MAYBANK  | 09/03/2026 | -2.6%    | -0.7%         | 1.5x         | Iran war escalation: KLCI -2.55% (steepest 2026 fall pre-Sep)                                 |
| MAYBANK  | 30/03/2026 | -2.3%    | -0.5%         | 0.8x         | no specific catalyst identified (market/flow)                                                 |
| MAYBANK  | 24/03/2026 | -2.2%    | +0.7%         | 1.4x         | no specific catalyst identified (market/flow)                                                 |
| PBBANK   | 27/08/2026 | -2.9%    | +0.2%         | 2.0x         | Maybank/HLB 2Q results; Maybank DRP; own results window                                       |
| PBBANK   | 29/09/2026 | -1.5%    | -0.2%         | 0.9x         | KLCI -1.56% to 9-month low: oil + bond yields at multi-year highs                             |
| PBBANK   | 11/09/2026 | -1.0%    | +0.0%         | 0.8x         | MGS10Y peaks 4.18% (HLIB)                                                                     |
| PBBANK   | 15/09/2026 | -1.0%    | +0.0%         | 1.0x         | no specific catalyst identified (market/flow)                                                 |
| PBBANK   | 28/08/2026 | -1.0%    | +0.2%         | 2.4x         | RHB/CIMB 2Q results                                                                           |
| CIMB     | 27/02/2026 | -5.0%    | -0.2%         | 2.7x         | FY25 results window (Maybank/CIMB 26-27/02); own results window                               |
| CIMB     | 03/06/2026 | -3.7%    | -1.9%         | 3.3x         | foreign-outflow phase: RM2.53b net sold in w/e 29/05 (MSCI May SAIR effective 29/05)          |
| CIMB     | 28/01/2026 | -3.4%    | -0.1%         | 2.3x         | no specific catalyst identified (market/flow)                                                 |
| CIMB     | 30/03/2026 | -2.9%    | -0.8%         | 1.7x         | no specific catalyst identified (market/flow)                                                 |
| CIMB     | 29/09/2026 | -2.6%    | -0.1%         | 1.3x         | KLCI -1.56% to 9-month low: oil + bond yields at multi-year highs                             |
| HLBANK   | 28/05/2026 | -3.3%    | +0.9%         | 2.3x         | 1Q26 results: Maybank/CIMB soft, PBB flat; ME-conflict provision fears                        |
| HLBANK   | 03/02/2026 | -3.2%    | -0.2%         | 2.1x         | no specific catalyst identified (market/flow)                                                 |
| HLBANK   | 18/09/2026 | -2.4%    | +0.0%         | 2.0x         | FS foreign outflow -RM309.7m in w/e 18/09 despite market net inflow (MBSB)                    |
| HLBANK   | 27/02/2026 | -2.3%    | +0.0%         | 1.0x         | FY25 results window (Maybank/CIMB 26-27/02); own results window                               |
| HLBANK   | 13/02/2026 | -2.3%    | -0.4%         | 0.7x         | no specific catalyst identified (market/flow)                                                 |
| RHBBANK  | 01/09/2026 | -3.9%    | -2.1%         | 5.4x         | 1st session after 2Q results + Merdeka: FS foreign outflow -RM462.9m in shortened week (MBSB) |
| RHBBANK  | 29/09/2026 | -3.8%    | +0.1%         | 1.5x         | KLCI -1.56% to 9-month low: oil + bond yields at multi-year highs                             |
| RHBBANK  | 11/09/2026 | -2.8%    | +0.0%         | 1.7x         | MGS10Y peaks 4.18% (HLIB)                                                                     |
| RHBBANK  | 11/08/2026 | -1.7%    | +0.0%         | 0.6x         | no specific catalyst identified (market/flow)                                                 |
| RHBBANK  | 09/09/2026 | -1.6%    | +0.0%         | 2.5x         | no specific catalyst identified (market/flow)                                                 |
| AMBANK   | 11/09/2026 | -3.2%    | -0.6%         | 0.7x         | MGS10Y peaks 4.18% (HLIB)                                                                     |
| AMBANK   | 29/09/2026 | -2.4%    | -0.3%         | 0.7x         | KLCI -1.56% to 9-month low: oil + bond yields at multi-year highs                             |
| AMBANK   | 01/09/2026 | -2.2%    | -1.4%         | 1.5x         | 1st session after 2Q results + Merdeka: FS foreign outflow -RM462.9m in shortened week (MBSB) |
| AMBANK   | 17/08/2026 | -2.0%    | -0.5%         | 1.0x         | own results window                                                                            |
| AMBANK   | 19/08/2026 | -1.8%    | -0.1%         | 2.0x         | AMMB 1QFY27 results (18/08); FS outflow w/e 21/08; own results window                         |
| BIMB     | 16/02/2026 | -2.8%    | -0.4%         | 0.5x         | no specific catalyst identified (market/flow)                                                 |
| BIMB     | 03/06/2026 | -2.7%    | +0.0%         | 3.2x         | foreign-outflow phase: RM2.53b net sold in w/e 29/05 (MSCI May SAIR effective 29/05)          |
| BIMB     | 22/05/2026 | -2.6%    | +0.0%         | 1.8x         | no specific catalyst identified (market/flow)                                                 |
| BIMB     | 02/03/2026 | -2.4%    | -2.4%         | 1.1x         | US/Israel strikes on Iran (28/02) — first trading day; Brent spike                            |
| BIMB     | 18/09/2026 | -2.4%    | +0.0%         | 2.9x         | FS foreign outflow -RM309.7m in w/e 18/09 despite market net inflow (MBSB)                    |
| ALLIANCE | 20/01/2026 | -5.4%    | -1.3%         | 1.7x         | no specific catalyst identified (market/flow)                                                 |
| ALLIANCE | 02/04/2026 | -4.2%    | +0.0%         | 2.5x         | no specific catalyst identified (market/flow)                                                 |
| ALLIANCE | 16/02/2026 | -4.2%    | +0.0%         | 0.7x         | no specific catalyst identified (market/flow)                                                 |
| ALLIANCE | 09/03/2026 | -3.3%    | -1.0%         | 2.7x         | Iran war escalation: KLCI -2.55% (steepest 2026 fall pre-Sep)                                 |
| ALLIANCE | 24/03/2026 | -2.6%    | -0.2%         | 2.2x         | no specific catalyst identified (market/flow)                                                 |
| AFFIN    | 19/08/2026 | -3.7%    | +0.0%         | 3.7x         | AMMB 1QFY27 results (18/08); FS outflow w/e 21/08                                             |
| AFFIN    | 24/03/2026 | -3.4%    | -0.4%         | 0.9x         | no specific catalyst identified (market/flow)                                                 |
| AFFIN    | 18/08/2026 | -2.7%    | +0.0%         | 5.5x         | Affin 2Q26 results (14/08, profit -11%) digestion; FS outflow w/e 21/08                       |
| AFFIN    | 08/06/2026 | -2.5%    | +0.0%         | 1.5x         | no specific catalyst identified (market/flow)                                                 |
| AFFIN    | 02/03/2026 | -2.2%    | -2.2%         | 1.3x         | US/Israel strikes on Iran (28/02) — first trading day; Brent spike                            |

### 2.4 Peer check: is it Malaysia-specific? (local-currency px; USD TR)

| name   | 52w high   | Px DD   | TR DD (USD)   | YTD px (LCY)   | YTD TR (USD)   | 3m     |
|:-------|:-----------|:--------|:--------------|:---------------|:---------------|:-------|
| DBS    | 04/09/2026 | -1.0%   | -1.8%         | +38.2%         | +44.4%         | +17.2% |
| OCBC   | 04/09/2026 | -0.8%   | -1.6%         | +62.0%         | +69.7%         | +27.6% |
| UOB    | 15/07/2026 | -4.2%   | -1.1%         | +22.8%         | +28.6%         | +7.4%  |
| BBCA   | 05/11/2025 | -29.9%  | -30.6%        | -24.5%         | -25.5%         | +8.9%  |
| BBRI   | 03/11/2025 | -21.8%  | -19.6%        | -13.7%         | -13.7%         | +17.5% |
| BMRI   | 24/02/2026 | -24.7%  | -21.6%        | -20.6%         | -15.9%         | +3.8%  |
| KBANK  | 21/09/2026 | -8.9%   | -9.3%         | +20.8%         | +22.5%         | +0.9%  |
| BBL    | 16/07/2026 | -8.1%   | -7.1%         | +10.0%         | +10.1%         | -3.1%  |

**Ruling:** this is a **Malaysia-plus-EM-flow event, not a regional bank sell-off**.
- Singapore banks are at or near highs (DBS +44%, OCBC +70% YTD in USD) and Thai banks are up 10–22%.
- Only Indonesia is worse (−14% to −25% YTD in USD, IDR 17,860). That feeds Maybank Indonesia and CIMB Niaga through translation.
- KLCI ex-banks is −1.8% YTD vs the bank composite −1.1% on price. The sharper gap is against the rotation basket (+9.3%).

---

## 3. Causal decomposition (Module 2)

### 3.1 Quantitative anchors

**(a) Price decomposition from each bank's 52w high: ΔlnP = ΔlnEPS(core TTM) + ΔlnP/E; ΔlnP = ΔlnBV + ΔlnP/B.**

| bank     | From (52w high)   | Price chg   | TR chg   | EPS(core TTM) effect   | P/E effect   | BV effect   | P/B effect   | Dividend effect   | DY-MGS spread now   | 1y ago   | at 52w high   |
|:---------|:------------------|:------------|:---------|:-----------------------|:-------------|:------------|:-------------|:------------------|:--------------------|:---------|:--------------|
| MAYBANK  | 24/02/2026        | -18.9%      | -14.0%   | +0.9%                  | -21.8%       | +0.3%       | -21.2%       | +5.9%             | +2.28pp             | +2.81pp  | +1.48pp       |
| PBBANK   | 04/08/2026        | -11.0%      | -9.1%    | +0.9%                  | -12.5%       | +3.4%       | -15.0%       | +2.1%             | +0.70pp             | +1.52pp  | +0.53pp       |
| CIMB     | 27/01/2026        | -12.8%      | -8.3%    | +1.0%                  | -14.8%       | -0.5%       | -13.3%       | +5.1%             | +1.94pp             | +1.97pp  | +1.73pp       |
| HLBANK   | 30/01/2026        | -9.5%       | -8.2%    | +5.8%                  | -15.8%       | +7.0%       | -16.9%       | +1.3%             | +0.11pp             | +0.01pp  | +0.22pp       |
| RHBBANK  | 10/08/2026        | -15.2%      | -13.6%   | +0.1%                  | -16.6%       | +2.9%       | -19.4%       | +1.9%             | +2.55pp             | +3.07pp  | +1.90pp       |
| AMBANK   | 12/08/2026        | -12.3%      | -12.3%   | +0.1%                  | -13.3%       | -0.9%       | -12.3%       | +0.0%             | +1.33pp             | +1.90pp  | +1.01pp       |
| BIMB     | 12/02/2026        | -19.3%      | -17.8%   | +0.7%                  | -22.1%       | +1.1%       | -22.6%       | +1.9%             | +2.96pp             | +3.15pp  | +2.01pp       |
| ALLIANCE | 14/01/2026        | -15.2%      | -13.4%   | +2.1%                  | -18.6%       | +3.2%       | -19.6%       | +2.1%             | -0.02pp             | +0.88pp  | -0.10pp       |
| AFFIN    | 12/02/2026        | -27.7%      | -25.2%   | -3.6%                  | -28.8%       | +1.7%       | -34.1%       | +3.4%             | +0.15pp             | -3.45pp  | -3.55pp       |

→ **Multiple-only de-rating.** EPS (core TTM) *rose* 0.1–5.8% at 8 of 9 banks between the high and today; AFFIN (−3.6%) is the exception. The dividend-yield-minus-MGS spread is *narrower than a year ago* at 7 of 9 banks, because MGS rose 64bp YoY (3.45% on 30/09/2025 → 4.09%, T1). It is wider than at the Feb peak, because prices fell further than yields rose.

**(b) Weekly factor model** (bank composite TR on the non-bank equity basket, ΔMGS10Y [BNM daily, T1], ΔUST10Y, MYR, Brent; estimated 01/2025–07/2026; n = 79, R² = 0.33; HC1 SE). Coefficients: non-bank β 0.38 (t 4.9); ΔMGS +0.10%/bp (t 2.8, **positive**, which reflects the 2025 NIM-relief channel); ΔUST −0.03%/bp (t −1.8); MYR 0.70 (t 2.6); Brent ~0.

|                      | Leg1 11/02->03/06/2026   | Leg2 05/08->30/09/2026   | Since peak 11/02->30/09   | YTD                |
|:---------------------|:-------------------------|:-------------------------|:--------------------------|:-------------------|
| weeks                | 17                       | 8                        | 34                        | 39                 |
| actual_bank_tr       | -5.2%                    | -3.7%                    | -5.0%                     | +4.2%              |
| contrib_r_nonbank    | +3.7%                    | +0.2%                    | +4.6%                     | +3.8%              |
| contrib_d_mgs        | +0.1%                    | +3.6%                    | +5.2%                     | +5.7%              |
| contrib_d_ust        | -0.9%                    | -1.7%                    | -3.0%                     | -3.1%              |
| contrib_r_myr        | -1.2%                    | +0.2%                    | -2.4%                     | -0.6%              |
| contrib_r_brent      | +0.4%                    | +0.2%                    | +0.5%                     | +0.6%              |
| alpha_drift          | +1.6%                    | +0.8%                    | +3.2%                     | +3.7%              |
| residual_unexplained | -9.1%                    | -7.0%                    | -13.1%                    | -6.1%              |
| mgs_move_bps         | 0.9999999999999593       | 36.99999999999995        | 52.99999999999999         | 58.99999999999994  |
| ust_move_bps         | 32.999992370605426       | 59.50002670288085        | 104.90002632141108        | 106.80003166198728 |
| brent_move           | +36.8%                   | +14.8%                   | +41.0%                    | +57.9%             |
| nonbank_move         | +10.0%                   | +0.5%                    | +12.2%                    | +10.0%             |

→ Macro factors do **not** explain the fall.
- The only negative contributions are UST (−3.0pp since the peak) and MYR (−2.4pp, concentrated in leg 1).
- The **sector-specific residual is −9.1pp in leg 1 and −7.0pp in leg 2**. That is the footprint of flows and rotation, the KLCI-50 reweight, earnings-visibility concerns and the Maybank capital event.
- The domestic-yield channel works through MTM/NOII visibility and relative yield. It is not captured by a simple beta.

**(c) Local institutions: net substantial-shareholder transactions** (Bursa filings via klsescreener transcription; RM m at current price). This covers holders ≥5% only, so it understates total activity.

| bank     |   ('EPF', '2026YTD') |   ('EPF', 'Aug-Sep26') |   ('EPF', 'Feb-Jun26') |   ('KWAP', '2026YTD') |   ('KWAP', 'Aug-Sep26') |   ('KWAP', 'Feb-Jun26') |   ('PNB/ASNB', '2026YTD') |   ('PNB/ASNB', 'Aug-Sep26') |   ('PNB/ASNB', 'Feb-Jun26') |
|:---------|---------------------:|-----------------------:|-----------------------:|----------------------:|------------------------:|------------------------:|--------------------------:|----------------------------:|----------------------------:|
| AFFIN    |                    0 |                      0 |                      0 |                     0 |                       0 |                       0 |                         0 |                           0 |                           0 |
| ALLIANCE |                  181 |                    -56 |                    311 |                     0 |                       0 |                       0 |                         0 |                           0 |                           0 |
| AMBANK   |                  450 |                    471 |                    334 |                     0 |                       0 |                       0 |                         0 |                           0 |                           0 |
| BIMB     |                  -19 |                     -1 |                    -20 |                     0 |                       0 |                       0 |                        -8 |                           0 |                          -8 |
| CIMB     |                  457 |                    423 |                   -823 |                  -511 |                    -389 |                       8 |                         0 |                           0 |                           0 |
| HLBANK   |                 -213 |                     -4 |                   -412 |                     0 |                       0 |                       0 |                         0 |                           0 |                           0 |
| MAYBANK  |                  802 |                   -838 |                   1324 |                  -328 |                     -57 |                      27 |                       664 |                          40 |                         979 |
| PBBANK   |                -1871 |                   -241 |                  -1410 |                   829 |                      85 |                     724 |                         0 |                           0 |                           0 |
| RHBBANK  |                 -810 |                    580 |                  -1094 |                  -137 |                       0 |                    -142 |                         0 |                           0 |                           0 |

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

| bank     |   Rank |   Score | Core ROE   | 10y avg   |   ROE z(10y) | ΔROE 4Q   | EPS g YoY   | NIM   | NIM YoY   | CASA   | CIR   | CC (bp)   | GIL   | LLC   | CET1   | Loans YoY   |   DPS TTM (RM) | Payout   | DY   | Cons FY0 rev 90d   |   Rev breadth 30d | Core vs rep (FY)   | KPI coverage   |
|:---------|-------:|--------:|:-----------|:----------|-------------:|:----------|:------------|:------|:----------|:-------|:------|:----------|:------|:------|:-------|:------------|---------------:|:---------|:-----|:-------------------|------------------:|:-------------------|:---------------|
| MAYBANK  |      1 |    0.73 | 11.2%      | 10.4%     |         0.96 | +32bp     | +1.6%       | 2.10% | +10bp     | 41.1%  | 49.9% | 8         | 1.34% | 103%  | 15.0%  | 2.7%        |          0.64  | 73.9%    | 6.4% | -0.7%              |              0.05 | +0.4%              | 100%           |
| PBBANK   |      2 |    0.65 | 12.2%      | 13.4%     |        -0.78 | -39bp     | +1.3%       | n/a   | n/a       | n/a    | 35.1% | n/a       | 0.54% | 139%  | 13.9%  | 5.9%        |          0.225 | 59.6%    | 4.8% | -1.4%              |             -0.25 | +0.5%              | 67%            |
| HLBANK   |      3 |    0.63 | 11.2%      | 11.0%     |         0.25 | +2bp      | +6.0%       | 1.84% | n/a       | 34.7%  | 37.6% | n/a       | 0.57% | 80%   | 12.9%  | 7.7%        |          0.98  | 44.3%    | 4.2% | +0.1%              |              0.32 | -0.1%              | 67%            |
| RHBBANK  |      4 |    0.63 | 10.3%      | 9.3%      |         0.94 | +40bp     | +7.8%       | 1.86% | -2bp      | n/a    | n/a   | 14        | n/a   | n/a   | n/a    | n/a         |          0.5   | 62.8%    | 6.6% | -1.9%              |             -0.29 | -0.7%              | 33%            |
| AMBANK   |      5 |    0.57 | 10.0%      | 8.8%      |         0.95 | +7bp      | +4.3%       | 1.93% | -8bp      | n/a    | 43.4% | 19        | 1.62% | n/a   | n/a    | 7.0%        |          0.35  | 55.0%    | 5.4% | -1.1%              |              0    | -0.0%              | 67%            |
| CIMB     |      6 |    0.54 | 11.2%      | 8.9%      |         0.95 | +12bp     | +1.5%       | 2.04% | n/a       | n/a    | 45.2% | 38        | 1.60% | n/a   | 14.0%  | n/a         |          0.47  | 64.6%    | 6.0% | -1.8%              |             -0.4  | +1.1%              | 67%            |
| ALLIANCE |      7 |    0.51 | 10.0%      | 9.4%      |         0.44 | -34bp     | +1.8%       | 2.26% | n/a       | n/a    | 47.4% | 0         | n/a   | n/a   | n/a    | 9.5%        |          0.191 | 37.6%    | 4.1% | +1.8%              |              0.23 | +1.3%              | 33%            |
| BIMB     |      8 |    0.43 | 6.3%       | 10.7%     |        -1.32 | -21bp     | +0.4%       | n/a   | n/a       | n/a    | n/a   | n/a       | n/a   | n/a   | n/a    | n/a         |          0.144 | 58.6%    | 7.0% | -2.2%              |             -0.29 | -9.1%              | 0%             |
| AFFIN    |      9 |    0.31 | 4.4%       | 5.1%      |        -0.51 | -38bp     | -3.7%       | 1.52% | +3bp      | n/a    | 63.0% | n/a       | n/a   | n/a   | n/a    | 13.6%       |          0.085 | 40.4%    | 4.2% | -7.0%              |             -0.89 | +2.3%              | 33%            |

*KPI sources: MAYBANK 1Q26 release (T1) + The Edge 27/08/2026 (T2); CIMB 2Q26 release (T1); HLB FY26 release 27/08/2026 (T1); Alliance 1QFY27 release (T1); PBB The Edge 26/08/2026; RHB The Edge/Star 28/08/2026; AMMB Star 18/08/2026; AFFIN Star 14/08/2026 (T2). Consensus: Yahoo (T3). ROE, EPS, DPS and payout are computed from Bursa quarterly filings (klsescreener transcription, T3 of T1).*

| bank     | Core ROE TTM % (oldest -> latest, 12Q)                      |
|:---------|:------------------------------------------------------------|
| MAYBANK  | 10.7 10.4 10.7 10.5 10.9 10.7 11.0 10.9 11.3 11.2 11.4 11.2 |
| PBBANK   | 13.5 12.7 12.4 12.3 12.8 12.7 13.0 12.6 12.6 12.3 12.5 12.2 |
| HLBANK   | 11.8 11.6 11.6 11.8 12.1 11.7 11.3 11.2 11.3 11.0 11.1 11.2 |
| RHBBANK  | 10.6 9.4 9.0 8.8 9.3 9.8 9.8 9.9 10.1 10.1 10.6 10.3        |
| AMBANK   | 9.7 9.9 9.9 10.3 10.5 10.0 10.0 9.9 10.0 10.2 9.9 10.0      |
| CIMB     | 10.3 10.7 10.9 11.0 11.3 11.2 11.4 11.0 11.3 11.3 11.3 11.2 |
| ALLIANCE | 9.6 9.5 9.9 10.3 10.1 10.2 10.1 10.3 10.2 10.2 9.8 10.0     |
| BIMB     | 7.5 7.6 7.7 7.6 7.3 7.6 7.5 7.2 7.0 7.1 6.9 7.0             |
| AFFIN    | 4.8 3.7 3.3 3.3 3.7 4.5 4.5 4.8 4.7 4.6 4.5 4.4             |

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

| bank     |   P/B |   10y mean |   z(10y) |   %ile 10y |   %ile 15y |   %ile 20y | ROE 07-15   | ROE 16-26   |   P/B 07-15 |   P/B 16-26 | P/E core   |   P/E z(10y) | DY   | DY-MGS   |   spread %ile 20y |   spread %ile 10y |
|:---------|------:|-----------:|---------:|-----------:|-----------:|-----------:|:------------|:------------|------------:|------------:|:-----------|-------------:|:-----|:---------|------------------:|------------------:|
| MAYBANK  |  1.31 |       1.27 |     0.25 |         64 |         45 |         37 | 14.9%       | 10.5%       |        1.85 |        1.28 | 11.6x      |        -0.83 | 6.4% | +2.28pp  |                46 |                40 |
| PBBANK   |  1.48 |       1.81 |    -0.91 |         17 |         12 |          9 | 23.5%       | 13.6%       |        3.1  |        1.84 | 12.4x      |        -0.76 | 4.8% | +0.70pp  |                68 |                69 |
| CIMB     |  1.2  |       1    |     1    |         81 |         62 |         47 | 14.7%       | 8.8%        |        2.03 |        1    | 10.7x      |        -0.37 | 6.0% | +1.94pp  |                83 |                68 |
| HLBANK   |  1.15 |       1.3  |    -0.79 |         26 |         17 |         13 | 15.6%       | 11.0%       |        1.76 |        1.3  | 10.6x      |        -0.84 | 4.2% | +0.11pp  |                78 |                79 |
| RHBBANK  |  0.96 |       0.87 |     0.97 |         86 |         66 |         51 | 12.9%       | 9.2%        |        1.3  |        0.87 | 9.5x       |        -0.06 | 6.6% | +2.55pp  |                81 |                63 |
| AMBANK   |  1    |       0.75 |     1.73 |         94 |         70 |         55 | 12.5%       | 8.8%        |        1.54 |        0.76 | 10.2x      |         1.04 | 5.4% | +1.33pp  |                85 |                73 |
| BIMB     |  0.57 |       0.87 |    -1.47 |          0 |          0 |          2 | 13.3%       | 11.0%       |        1.11 |        0.9  | 8.3x       |        -0.25 | 7.0% | +2.96pp  |                84 |                77 |
| ALLIANCE |  0.91 |       0.91 |     0.03 |         53 |         35 |         27 | 12.0%       | 9.5%        |        1.6  |        0.93 | 9.2x       |        -0.39 | 4.1% | -0.02pp  |                57 |                36 |
| AFFIN    |  0.41 |       0.48 |    -0.73 |         26 |         18 |         14 | 8.5%        | 5.1%        |        0.76 |        0.48 | 9.5x       |        -0.2  | 4.2% | +0.15pp  |                71 |                72 |

**The ROE reset is visible in the data.** Average core ROE fell from ~15% (2007–15) to ~10.5% (2016–26) at MAYBANK, from 23.5% to 13.6% at PBBANK, and from 14.7% to 8.8% at CIMB. P/Bs reset with it. **20y percentiles are therefore a false anchor.** On the relevant post-reset 10y bands:
- **Cheap:** PBBANK (17th percentile), HLB (26th), AFFIN (26th), BIMB (0th, a record low).
- **Mid:** ALLIANCE (53rd), MAYBANK (64th).
- **Expensive vs own history:** CIMB (81st), RHB (86th), AMMB (94th).

### 5.2 The core test: cheap after ROE, or cheap because ROE is lower?

| bank     | Core ROE   |   TS fair P/B (ROE) |   Resid (SD) |   R² | g    |   β (Blume) | COE=MGS+β·6%   |   Gordon P/B | Actual/Gordon   | Implied COE   | Implied ERP   |   ERP %ile 20y |   ERP %ile 10y | ROE implied @fair COE   |   XS fair P/B |   XS resid |
|:---------|:-----------|--------------------:|-------------:|-----:|:-----|------------:|:---------------|-------------:|:----------------|:--------------|:--------------|---------------:|---------------:|:------------------------|--------------:|-----------:|
| MAYBANK  | 11.2%      |                1.38 |        -0.37 | 0.72 | 2.9% |        0.87 | 9.3%           |         1.3  | +0.5%           | 9.3%          | 6.0%          |             38 |             55 | 11.2%                   |          1.19 |       0.11 |
| PBBANK   | 12.2%      |                1.69 |        -0.68 | 0.82 | 4.9% |        1.06 | 10.5%          |         1.31 | +13.5%          | 9.8%          | 5.4%          |             29 |             37 | 13.2%                   |          1.32 |       0.16 |
| CIMB     | 11.2%      |                1.44 |        -0.65 | 0.66 | 4.0% |        1.26 | 11.7%          |         0.94 | +28.1%          | 10.0%         | 4.7%          |             55 |             57 | 13.2%                   |          1.19 |       0.01 |
| HLBANK   | 11.2%      |                1.34 |        -0.87 | 0.5  | 5.0% |        0.88 | 9.4%           |         1.41 | -18.8%          | 10.4%         | 7.1%          |             37 |             57 | 10.0%                   |          1.19 |      -0.05 |
| RHBBANK  | 10.3%      |                1.02 |        -0.24 | 0.4  | 3.8% |        0.83 | 9.1%           |         1.24 | -21.9%          | 10.5%         | 7.8%          |             37 |             48 | 8.9%                    |          1.08 |      -0.11 |
| AMBANK   | 10.0%      |                1.05 |        -0.19 | 0.58 | 4.5% |        1.1  | 10.7%          |         0.89 | +11.5%          | 10.0%         | 5.4%          |             43 |             40 | 10.6%                   |          1.04 |      -0.04 |
| BIMB     | 7.0%       |                0.69 |        -0.46 | 0.38 | 2.9% |        0.69 | 8.3%           |         0.76 | -24.6%          | 10.0%         | 8.5%          |             20 |             31 | 5.9%                    |          0.64 |      -0.07 |
| ALLIANCE | 10.0%      |                1.2  |        -0.79 | 0.19 | 5.0% |        0.71 | 8.3%           |         1.5  | -39.2%          | 10.5%         | 9.0%          |             54 |             50 | 8.0%                    |          1.04 |      -0.12 |
| AFFIN    | 4.4%       |                0.46 |        -0.43 | 0.64 | 2.6% |        1    | 10.1%          |         0.24 | +74.1%          | 6.9%          | 2.8%          |             19 |             35 | 5.7%                    |          0.3  |       0.11 |

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

| Peak       | Trough     | Trigger                                                              | Type                        | Pk-Tr   |   Days | P/B@tr   | ROE@tr   | DY@tr   | MGS@tr   | EPS pk->tr   | EPS tr->+12m   | +3m    | +6m    | +12m   | +36m    | Hit -6.7% on   | +12m from hit   | +36m from hit   | Further DD after hit   |
|:-----------|:-----------|:---------------------------------------------------------------------|:----------------------------|:--------|-------:|:---------|:---------|:--------|:---------|:-------------|:---------------|:-------|:-------|:-------|:--------|:---------------|:----------------|:----------------|:-----------------------|
| 29/03/2000 | 18/04/2001 | Dot-com bust / post-AFC bank merger overhang / 9-11                  | n/a (pre-fundamentals data) | -45.7%  |    385 | n/a      | n/a      | n/a     | n/a      | n/a          | +0.0%          | +23.2% | +20.4% | +65.8% | +113.0% | 17/04/2000     | -37.8%          | -19.3%          | -38.8%                 |
| 23/04/2002 | 03/12/2002 | 2002-03 global bear market / Iraq war / SARS                         | n/a (pre-fundamentals data) | -25.7%  |    224 | n/a      | n/a      | n/a     | n/a      | n/a          | +1.9%          | +5.7%  | +15.0% | +45.7% | +89.6%  | 30/05/2002     | -7.7%           | +44.4%          | -20.0%                 |
| 22/03/2004 | 17/05/2004 | 2004-05 rate-hike cycle (Fed), post-GE11 consolidation               | Multiple-only derating      | -16.1%  |     56 | 1.77     | 14.5%    | 4.6%    | n/a      | +7.3%        | +0.8%          | +6.4%  | +18.2% | +22.0% | +111.4% | 14/04/2004     | +10.5%          | +82.3%          | -9.3%                  |
| 14/01/2008 | 10/03/2008 | GFC + GE12 'political tsunami' (08/03/2008)                          | ROE reset (structural)      | -18.1%  |     56 | 2.01     | 21.0%    | 7.3%    | 3.7%     | +2.5%        | -3.9%          | +3.7%  | -0.4%  | -24.4% | +77.2%  | 21/01/2008     | -29.8%          | +59.2%          | -11.2%                 |
| 19/02/2008 | 16/03/2009 | GFC + GE12 'political tsunami' (08/03/2008)                          | ROE reset (structural)      | -38.0%  |    391 | 1.33     | 16.6%    | 7.1%    | 4.1%     | -4.5%        | +2.9%          | +39.4% | +63.7% | +96.8% | +166.8% | 04/03/2008     | -26.7%          | +64.1%          | -32.5%                 |
| 08/07/2011 | 26/09/2011 | Euro sovereign crisis II / US downgrade                              | Multiple-only derating      | -18.4%  |     80 | 1.97     | 17.6%    | 5.6%    | 3.6%     | +3.4%        | +14.4%         | +11.8% | +20.4% | +23.9% | +54.6%  | 25/08/2011     | +11.2%          | +35.9%          | -12.5%                 |
| 08/09/2014 | 24/08/2015 | Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era) | ROE reset (structural)      | -19.2%  |    350 | 1.42     | 12.9%    | 4.3%    | 4.1%     | -9.4%        | -5.1%          | +3.8%  | +3.7%  | +7.5%  | +46.1%  | 16/10/2014     | -6.0%           | +14.4%          | -13.3%                 |
| 07/04/2015 | 21/01/2016 | Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era) | ROE reset (structural)      | -17.9%  |    289 | 1.34     | 11.9%    | 4.0%    | 4.2%     | -8.7%        | -0.6%          | +14.5% | +6.6%  | +14.5% | +50.7%  | 29/06/2015     | -6.0%           | +21.8%          | -11.9%                 |
| 27/02/2019 | 19/03/2020 | COVID-19 + 200bp OPR cuts + moratorium                               | EPS-revision-led            | -35.5%  |    386 | 0.85     | 10.4%    | 7.6%    | 2.8%     | -1.1%        | -34.6%         | +20.2% | +13.7% | +46.6% | +71.1%  | 24/07/2019     | -14.7%          | +19.6%          | -30.6%                 |

*Type rule: ROE reset = ROE down ≥2.5pp at +24m with no EPS recovery; EPS-led = EPS −5% or worse peak-to-trough or over the next 12m; otherwise multiple-only. "Hit −6.7%" = first date the episode reached today's composite depth. Fundamentals start 2003.*

### 6.2 Which episode does today resemble on fundamentals, not price? (≥8% episodes since 2008, standardised distance)

| Peak       | Trough     | Trigger                                                              | DD     | ROE vs 5y   | P/B vs 5y   | EPS pk->tr   | ΔMGS   | ΔUST   | Brent   | EPS +12m   | Fwd +12m   | Fwd +36m   |   Distance |
|:-----------|:-----------|:---------------------------------------------------------------------|:-------|:------------|:------------|:-------------|:-------|:-------|:--------|:-----------|:-----------|:-----------|-----------:|
| 11/02/2026 | 03/06/2026 | 2026 Iran war/oil shock + global yield spike + KLCI-50 reweight      | -9.4%  | +71bp       | +5.3%       | +1.2%        | +6bp   | +32bp  | +40.9%  | +0.9%      | n/a        | n/a        |       1.56 |
| 24/07/2013 | 28/08/2013 | Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era) | -9.1%  | -43bp       | -5.4%       | -0.3%        | +55bp  | +19bp  | +8.8%   | +1.7%      | +13.3%     | -1.5%      |       1.84 |
| 26/02/2025 | 09/04/2025 | 2025 US tariff shock / OPR cut (07/2025)                             | -11.4% | +113bp      | -4.2%       | +0.9%        | -4bp   | +15bp  | -9.7%   | +2.8%      | +24.6%     | n/a        |       2.48 |
| 19/04/2018 | 06/07/2018 | GE14 (09/05/2018) + 2018 EM/trade-war sell-off                       | -12.4% | -169bp      | -12.3%      | +1.8%        | +26bp  | -8bp   | +4.5%   | +2.6%      | +7.9%      | +6.2%      |       2.61 |
| 24/11/2022 | 02/06/2023 | Cukai Makmur (Budget 2022) + Fed hikes / foreign outflows            | -8.3%  | +131bp      | -11.9%      | +10.2%       | -67bp  | -2bp   | -10.9%  | +2.1%      | +23.9%     | +59.9%     |       3.79 |
| 08/07/2011 | 26/09/2011 | Euro sovereign crisis II / US downgrade                              | -18.4% | +75bp       | -9.1%       | +3.4%        | -30bp  | -111bp | -12.1%  | +14.4%     | +23.9%     | +54.6%     |       4.14 |
| 08/09/2014 | 16/12/2014 | Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era) | -14.9% | -237bp      | -25.2%      | -1.9%        | -6bp   | -40bp  | -40.3%  | -12.2%     | -2.1%      | +27.4%     |       4.35 |
| 07/04/2015 | 21/01/2016 | Taper tantrum -> oil crash / 1MDB / ringgit collapse (ROE reset era) | -17.9% | -417bp      | -32.9%      | -8.7%        | +29bp  | +13bp  | -50.5%  | -0.6%      | +14.5%     | +50.7%     |       5.16 |
| 27/02/2019 | 19/03/2020 | COVID-19 + 200bp OPR cuts + moratorium                               | -35.5% | -97bp       | -41.0%      | -1.1%        | -124bp | -157bp | -57.1%  | -34.6%     | +46.6%     | +71.1%     |       6.8  |

**Closest match: the 2013 taper tantrum** (distance 1.84, excluding 2026's own leg 1):
- **Same shock and starting point.** MGS +55bp (now +59bp), ROE at its 5y average, P/B near its 5y mean, EPS intact.
- **Outcome.** A −9% drawdown, then **+13% at 12m but −1.5% at 36m**, because it was followed by the 2014–16 oil/1MDB/ringgit **ROE reset**.

Next closest are 2025 (tariff shock: +25% at 12m) and 2018 (GE14/EM: +8% at 12m, +6% at 36m). Today is a *multiple-only de-rating*, historically the strongest entry type. The analog shows the risk is not the next 12m but whether ROE (near the top of its 10y range) holds.

### 6.3 Base rates: entering at today's drawdown depth (first crossing of the current TR depth from the rolling 52w high; re-armed after half-recovery)

| series    | Current TR depth   |   n events | Hit 12m   | Median 12m   | Worst 12m   | Median 36m   | Hit 36m   | Median further DD (12m)   | Worst further DD   |
|:----------|:-------------------|-----------:|:----------|:-------------|:------------|:-------------|:----------|:--------------------------|:-------------------|
| COMPOSITE | -6.7%              |         25 | 72%       | +10.5%       | -29.8%      | +44.8%       | 91%       | -4.8%                     | -34.6%             |
| MAYBANK   | -14.0%             |         11 | 73%       | +6.7%        | -42.3%      | +41.3%       | 91%       | -2.9%                     | -42.3%             |
| PBBANK    | -9.1%              |         25 | 84%       | +15.1%       | -27.4%      | +46.6%       | 100%      | -2.3%                     | -41.4%             |
| CIMB      | -8.3%              |         29 | 62%       | +13.2%       | -41.0%      | +34.0%       | 75%       | -5.9%                     | -50.5%             |
| HLBANK    | -8.2%              |         24 | 83%       | +7.4%        | -29.2%      | +25.2%       | 100%      | -4.9%                     | -36.7%             |
| RHBBANK   | -13.6%             |         15 | 47%       | -10.0%       | -53.1%      | +34.8%       | 80%       | -22.2%                    | -62.5%             |
| AMBANK    | -12.3%             |         19 | 47%       | -0.1%        | -78.3%      | +20.1%       | 67%       | -16.7%                    | -83.3%             |
| BIMB      | -17.8%             |          9 | 89%       | +34.0%       | -30.5%      | +36.0%       | 89%       | -4.4%                     | -32.9%             |
| ALLIANCE  | -13.4%             |         22 | 64%       | +9.5%        | -43.7%      | +30.1%       | 71%       | -6.8%                     | -55.8%             |
| AFFIN     | -25.2%             |         11 | 45%       | -2.3%        | -49.2%      | +51.5%       | 80%       | -17.9%                    | -59.6%             |

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

| bank     | Prob B/Ba/Be   | Bull TR   |   Bull P/B | Base TR   | Bear TR   |   Bear P/B | Bear ROE   | E[TR] MYR   | E[TR] USD   |   Up/Down |   Break-even P/B | Div cover (bear)   |   12m-fwd EPS (cons) |   Base DPS |
|:---------|:---------------|:----------|-----------:|:----------|:----------|-----------:|:-----------|:------------|:------------|----------:|-----------------:|:-------------------|---------------------:|-----------:|
| MAYBANK  | 25/50/25       | +16.0%    |       1.38 | +9.6%     | -13.9%    |       1.03 | 9.7%       | +5.4%       | +5.2%       |      1.16 |             1.18 | 1.13x              |                0.915 |      0.662 |
| PBBANK   | 25/55/20       | +25.5%    |       1.69 | +10.0%    | -17.5%    |       1.11 | 10.6%      | +8.4%       | +8.5%       |      1.46 |             1.34 | 1.46x              |                0.4   |      0.233 |
| CIMB     | 20/50/30       | +32.1%    |       1.44 | +10.5%    | -33.3%    |       0.71 | 9.8%       | +1.7%       | +1.5%       |      0.96 |             1.08 | 1.30x              |                0.781 |      0.494 |
| HLBANK   | 30/50/20       | +29.3%    |       1.34 | +10.6%    | -7.8%     |       0.96 | 9.5%       | +12.5%      | +12.8%      |      3.75 |             1.03 | 1.95x              |                2.332 |      1.013 |
| RHBBANK  | 20/50/30       | +17.2%    |       1.02 | +10.6%    | -12.0%    |       0.77 | 8.4%       | +5.1%       | +4.5%       |      1.43 |             0.87 | 1.31x              |                0.825 |      0.508 |
| AMBANK   | 20/45/35       | +16.5%    |       1.05 | +10.2%    | -36.9%    |       0.56 | 8.4%       | -5.0%       | -5.4%       |      0.45 |             0.9  | 1.52x              |                0.672 |      0.362 |
| BIMB     | 20/45/35       | +45.8%    |       0.77 | +9.3%     | -25.1%    |       0.39 | 4.1%       | +4.6%       | +4.1%       |      1.83 |             0.52 | 1.09x              |                0.236 |      0.136 |
| ALLIANCE | 25/50/25       | +45.0%    |       1.2  | +10.3%    | -18.4%    |       0.68 | 7.9%       | +11.8%      | +11.9%      |      2.45 |             0.82 | 2.17x              |                0.521 |      0.192 |
| AFFIN    | 15/45/40       | +19.3%    |       0.46 | +7.4%     | -35.3%    |       0.24 | 3.1%       | -7.9%       | -8.7%       |      0.55 |             0.38 | 1.65x              |                0.232 |      0.092 |

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

| bank     |   Base EPS |   Stress EPS | EPS hit   | Stress ROE   |   PAT hit (RM b) | Div cover   | DPS cut   | CET1 now   |   CET1 Δ (1y, bp) |
|:---------|-----------:|-------------:|:----------|:-------------|-----------------:|:------------|:----------|:-----------|------------------:|
| MAYBANK  |      0.897 |        0.597 | -33.4%    | 7.8%         |             3.62 | 0.90x       | -18.9%    | 14.96%     |               -36 |
| PBBANK   |      0.392 |        0.29  | -26.1%    | 9.1%         |             1.98 | 1.24x       | +0.0%     | 13.90%     |               -64 |
| CIMB     |      0.765 |        0.517 | -32.5%    | 7.9%         |             2.69 | 1.05x       | -5.9%     | 14.00%     |               -55 |
| HLBANK   |      2.285 |        1.67  | -26.9%    | 8.2%         |             1.26 | 1.65x       | +0.0%     | 12.90%     |               -70 |
| RHBBANK  |      0.809 |        0.523 | -35.4%    | 6.7%         |             1.25 | 1.03x       | -7.4%     | n/a        |               -55 |
| AMBANK   |      0.659 |        0.439 | -33.3%    | 6.8%         |             0.73 | 1.21x       | +0.0%     | n/a        |               -64 |
| BIMB     |      0.231 |        0.066 | -71.6%    | 1.8%         |             0.38 | 0.48x       | -56.4%    | n/a        |               -35 |
| ALLIANCE |      0.511 |        0.322 | -36.9%    | 6.3%         |             0.33 | 1.68x       | +0.0%     | 12.40%     |               -64 |
| AFFIN    |      0.227 |        0.077 | -66.3%    | 1.6%         |             0.4  | 0.83x       | -25.0%    | n/a        |               -49 |

**Read-across**
- **Dividend cover under full stress** stays >1× everywhere except **MAYBANK (0.90×: DPS −19%)**, **BIMB (0.48×)** and **AFFIN (0.83×)**. MAYBANK's 6.4% yield is the most stress-sensitive of the majors because its payout is ~74%.
- **CET1 absorbs a stress year with a 35–70bp hit.**
- **MAYBANK capital.** Post-Etiqa CET1 is ~14.1% (14.96% − 83bp, assuming the full RM4.83b is deducted against RWA ≈ RM580b), and ~13.8% after a stress year. That is above any plausible 12.5–13% management floor.

### 7.2 Price references from the bands (secondary to fundamental triggers)

| bank     |    Px |   BVPS |   @10y mean |   @-0.5SD |   @-1SD |   @-1.5SD |   @ROE-fair |   @Gordon | 1y vol   |
|:---------|------:|-------:|------------:|----------:|--------:|----------:|------------:|----------:|:---------|
| MAYBANK  | 10.04 |   7.69 |        9.79 |      9.27 |    8.76 |      8.25 |       10.61 |      9.99 | 15.7%    |
| PBBANK   |  4.7  |   3.17 |        5.72 |      5.16 |    4.6  |      4.04 |        5.37 |      4.14 | 17.5%    |
| CIMB     |  7.8  |   6.5  |        6.53 |      5.89 |    5.25 |      4.61 |        9.37 |      6.09 | 20.6%    |
| HLBANK   | 23.36 |  20.38 |       26.56 |     24.53 |   22.51 |     20.48 |       27.34 |     28.76 | 20.1%    |
| RHBBANK  |  7.53 |   7.81 |        6.82 |      6.45 |    6.09 |      5.72 |        7.97 |      9.64 | 17.7%    |
| AMBANK   |  6.46 |   6.48 |        4.86 |      4.4  |    3.94 |      3.48 |        6.82 |      5.79 | 17.8%    |
| BIMB     |  2.05 |   3.59 |        3.14 |      2.77 |    2.4  |      2.03 |        2.47 |      2.72 | 17.3%    |
| ALLIANCE |  4.69 |   5.14 |        4.65 |      4.11 |    3.57 |      3.02 |        6.19 |      7.72 | 20.7%    |
| AFFIN    |  2.01 |   4.88 |        2.32 |      2.11 |    1.89 |      1.68 |        2.24 |      1.15 | 16.9%    |

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

| bank    | qdate      | type      | reason                                                            |   eps_reported_sen |   eps_core_sen |
|:--------|:-----------|:----------|:------------------------------------------------------------------|-------------------:|---------------:|
| MAYBANK | 2009-06-30 | one-off   | BII goodwill impairment (one-off, RM1.9b-class)                   |             -17.62 |          13.25 |
| CIMB    | 2018-06-30 | one-off   | Gain on disposal of 50% CIMB Securities International (CITIC Sec) |              21.29 |          12.12 |
| CIMB    | 2021-03-31 | re-spread | quarterly mis-allocation; FY total kept                           |              24.76 |          10.72 |
| CIMB    | 2021-06-30 | re-spread | quarterly mis-allocation; FY total kept                           |              10.8  |          10.72 |
| CIMB    | 2021-09-30 | re-spread | quarterly mis-allocation; FY total kept                           |              -1.07 |          10.72 |
| CIMB    | 2021-12-31 | re-spread | quarterly mis-allocation; FY total kept                           |               8.37 |          10.72 |
| HLBANK  | 2013-03-31 | one-off   | Source transcription error (EPS=0.00)                             |               0    |          28.12 |
| AMBANK  | 2007-03-31 | one-off   | 4QFY07 exceptional impairment/loss                                |             -25.69 |           5.36 |
| AMBANK  | 2021-03-31 | one-off   | 1MDB global settlement RM2.83b (4QFY21)                           |            -156    |           9.23 |
| AFFIN   | 2022-09-30 | one-off   | Gain on disposal of Affin Hwang Asset Management stake            |              38.41 |           6.29 |

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
