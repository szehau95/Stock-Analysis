# ACEL monthly-roll screen: Lombard Odier research list (17.09.2026)

Fixing assumed **01/10/2026** (first clean date after MU reports on 30/09 after the close), obs #1 **02/11/2026**. Market data: IBKR, closes of 24 Sep 2026. Model: correlated-GBM Monte Carlo, 50,000 paths per structure over 680 baskets (12,002 structures), finalists re-run at 200,000 paths. Coupons are model estimates for ranking and quote requests, not quotes.

## Bottom line

- **Best counters from the three lists right now: ARM and DELL** as the engine (highest usable vol, prints after obs #1, KI headroom to the 13-week low), with DDOG, PDD or AVGO as the third name (then BABA, ORCL, PANW, NVDA, DIS). ARM is in 52 and DELL in 22 of the 64 baskets that clear every hard filter at a ≥9% roll-priced coupon.
- **Top structure: ARM + DELL + DDOG, KO 80 / Strike 60 / KI 60**: P(KO @ obs #1) 71.6%, P(KO by obs #3) 82.9%, P(loss) 9.7%, but an average loss of 49% when it does lose.
- **The catch is coupon, not KO.** No structure in the universe clears your hard filters *and* your regime coupon targets (0 of 12,002). At the all-in cost implied by the 24/09 fill (5.84% of notional), roll-friendly structures price at roughly **−2% to +2% p.a.**; with 2.5 pts less UF they reach **~9–12% p.a.** Each 1% of UF costs ~4% p.a. of coupon on a note expected to live ~3 months.
- **Why your structures drifted from KO 80–85 to 95–100 (Jul→Sep):** the July/August fills (KO 80–85, KI 50–60, ~20%) only reconcile with the September fee level if memory vols were ~20–30 points higher than today, which fits July's realized swings. Memory IVs now sit at their 2nd–21st 52-week percentile, so holding 15–17% forced KO and KI up. That is what the September trades did.
- **The current memory basket fails the framework on every hard filter.** MU+SNDK+SKHY 95/70/70: P(KO @ obs #1) 43.9%, P(loss) 22.9% (E[loss | loss] 48%); SK hynix (27/10) and Sandisk (~30/10) report inside obs #1, and KI 70 sits above the 13-week-low limit (SNDK 51%, SKHY 60%, MU 61%).

## 1. Counters in the lists, screened

US lines only (ACEL chassis). Not modelled: Sell-rated names (SpaceX, Enphase, First Solar, Nike); names without a US line (Samsung, Tencent, Xiaomi, BYD and the European and Swiss names); small caps (Mirion, On, Service Corp); low-vol defensives (Verizon, AT&T, McDonald's, Home Depot); and names outside the house style (IBM, Spotify, Booking, Pinterest, TKO, Aptiv, Trimble, Logitech, Nokia, STMicro, SAP, Baidu, Ferrari).

| Counter | LO | LO PT upside | IV 30D | IV 12M | IV pct 52w | vs 52W hi | KI cap (13W) | vs 20D MA | Next print | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ARM UW | H | -18% | 67% | 73% | 60% | -32% | 64% | 15% | 04/11 (e) | Tier 1 engine (52 baskets, best #1) |
| DELL UN | B | 12% | 60% | 68% | 51% | -10% | 60% | 2% | 24/11 (e) | Tier 1 engine (22 baskets, best #1) |
| DDOG UW | H | -4% | 57% | 63% | 51% | -12% | 71% | 11% | 05/11 (e) | Tier 1 third leg (20 baskets, best #1) |
| MU UW | H | 11% | 61% | 62% | 21% | -14% | 61% | 10% | 30/09 (c) | Tier 2 engine (17 baskets, best #5) |
| PANW UW | H | -8% | 51% | 57% | 69% | -2% | 67% | 8% | 12/11 (e) | Tier 2 third leg (13 baskets, best #7) |
| ORCL UN | H | 4% | 49% | 56% | 20% | -56% | 74% | -7% | 14/12 (e) | Tier 2 third leg (11 baskets, best #5) |
| AMAT UW | H | 10% | 54% | 56% | 51% | -36% | 78% | 5% | 12/11 (e) | Tier 2 third leg (10 baskets, best #14) |
| AVGO UW | B | 43% | 35% | 44% | 2% | -29% | 86% | -2% | 10/12 (e) | Tier 1 third leg (4 baskets, best #3) |
| NVDA UW | SB | 16% | 30% | 39% | 1% | -5% | 76% | 1% | 18/11 (e) | Tier 2 third leg (5 baskets, best #20) |
| PDD UW | B | 41% | 30% | 40% | 16% | -44% | 83% | -3% | 18/11 (e) | Tier 1 third leg (3 baskets, best #2) |
| DIS UN | SB | 36% | 24% | 29% | 29% | -9% | 79% | -0% | 12/11 (e) | Tier 3 third leg (3 baskets, best #19) |
| BABA UN | B | 95% | 38% | 44% | 14% | -43% | 76% | -1% | 19/11 (e) | Tier 2 third leg (10 baskets, best #4) |
| ADBE UW | H | -2% | 38% | 45% | 30% | -34% | 74% | -9% | 10/12 (e) | Tier 2 third leg (7 baskets, best #8) |
| AMD UW | H | -24% | 52% | 58% | 22% | -2% | 61% | 21% | 03/11 (c) | Avoid: strong-day fix, px 24% above LO PT |
| CRM UN | B | 26% | 39% | 45% | 28% | -11% | 57% | -4% | 02/12 (e) | Exclude now: 13W-low rule caps KI at 57% |
| PLTR UW | H | -12% | 47% | 58% | 25% | -7% | 51% | 8% | 09/11 (c) | Exclude now: 13W-low rule caps KI at 51% |
| ANET UN | H | 7% | 46% | 46% | 17% | -3% | 68% | 5% | 02/11 (e) | Exclude: est. print on the obs #1 date |
| SKHY UW | H | -3% | 56% | 63% | 2% | -7% | 60% | 4% | 27/10 (e) | Exclude: prints before obs #1 |
| STX UW | H | 1% | 69% | 69% | 37% | -21% | 69% | n/a | 27/10 (e) | Exclude: prints before obs #1 |
| GOOGL UW | B | 31% | 31% | 36% | 42% | -16% | 83% | 0% | 27/10 (e) | Exclude: prints before obs #1 |
| AMZN UW | SB | 28% | 31% | 36% | 38% | -13% | 82% | -2% | 29/10 (e) | Exclude: prints before obs #1 |
| MSFT UW | SB | 23% | 26% | 26% | 31% | -10% | 64% | n/a | 27/10 (e) | Exclude: prints before obs #1 |
| META UW | B | -10% | 41% | 41% | 71% | -0% | 61% | n/a | 28/10 (e) | Exclude: prints before obs #1 |
| AAPL UW | B | 3% | 23% | 23% | 24% | -3% | 73% | n/a | 29/10 (e) | Exclude: prints before obs #1 |
| TSLA UW | H | 2% | 44% | 44% | 33% | -24% | 71% | n/a | 21/10 (e) | Exclude: prints before obs #1 |
| NFLX UW | B | 46% | 44% | 44% | 86% | -43% | 82% | n/a | 15/10 (e) | Exclude: prints before obs #1 |
| TSM UN | SB | 20% | 33% | 33% | 8% | -6% | 74% | n/a | 15/10 (e) | Exclude: prints before obs #1 |
| ASML UW | B | 21% | 46% | 46% | 47% | -14% | 80% | n/a | 14/10 (e) | Exclude: prints before obs #1 |
| INTC UW | H | -22% | 67% | 67% | 50% | -11% | 58% | n/a | 22/10 (e) | Exclude: prints before obs #1 |
| NOW UN | SB | 31% | 56% | 56% | 66% | -28% | 59% | n/a | 21/10 (e) | Exclude: prints before obs #1 |

*KI cap (13W)* = 90% of the 13-week low ÷ spot, the highest KI that clears your 13-week-low hard filter. (c) confirmed date, (e) vendor estimate or prior-year pattern. LO PT upside is recomputed at the 24/09 close (foreign-listed lines keep the list's 17/09 figure). *Baskets* = filter-passing baskets containing the name; *best #* = its best position in the ranked table below; *engine* = 30D IV ≥ 58%.

## 2. Ranked structures

Hard filters applied: no print inside obs #1, P(KO @ obs #1) ≥ 55%, P(loss) ≤ 12%, every KI at least 10% below its 13-week low. Minimum coupon: 9% p.a. at roll pricing (the lowest target in your sweet-spot table). Grid: KO 80–95, Strike = KI 50–80, inside your rules of thumb (KO ≤ 100 − 0.5·σ₁ₘ, KI ≤ e^(−0.75σ)). Ranked on memory KO; simultaneous KO shown after the slash.

| # | Basket | KO/Str/KI | CPN roll / 24-09 cost | P(KO@1) | P(KO≤3) mem/sim | E[life] m | P(loss) | E[loss\|loss] | Client EV | CPN/IV | Score | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ARM + DELL + DDOG | 80/60/60 | 9.4% / -2.1% | 71.6% | 83%/80% | 2.6/3.0 | 9.7%/14% | 49% | -2.7% | 0.15 | 0.589 | low corr (avg rho 0.24); px > LO PT (ARM/DDOG); earnings <=3d after obs #1 (ARM/DDOG) |
| 2 | ARM + DELL + PDD | 83/60/60 | 9.2% / -2.0% | 70.7% | 82%/80% | 2.7/3.0 | 10.0%/13% | 48% | -2.7% | 0.18 | 0.585 | low corr (avg rho 0.25); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 3 | AVGO + ARM + DELL | 83/60/60 | 9.1% / -2.0% | 70.7% | 82%/80% | 2.7/3.0 | 10.0%/13% | 48% | -2.7% | 0.17 | 0.583 | low corr (avg rho 0.43); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 4 | ARM + DELL + BABA | 83/60/60 | 10.0% / -0.7% | 69.0% | 81%/78% | 2.8/3.2 | 10.6%/14% | 47% | -2.7% | 0.18 | 0.566 | low corr (avg rho 0.26); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 5 | MU + ARM + ORCL | 83/60/60 | 9.5% / -1.4% | 69.5% | 81%/79% | 2.8/3.1 | 10.4%/14% | 47% | -2.7% | 0.16 | 0.565 | low corr (avg rho 0.41); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 6 | ARM + DELL | 85/60/60 | 11.3% / 1.3% | 66.3% | 79%/77% | 3.0/3.2 | 11.5%/14% | 47% | -2.6% | 0.18 | 0.563 | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 7 | ARM + ORCL + PANW | 83/60/60 | 9.2% / -1.6% | 68.6% | 81%/78% | 2.8/3.2 | 10.5%/14% | 46% | -2.7% | 0.16 | 0.560 | low corr (avg rho 0.32); px > LO PT (ARM/PANW); earnings <=3d after obs #1 (ARM) |
| 8 | ARM + DELL + ADBE | 83/60/60 | 10.0% / -0.6% | 68.0% | 81%/77% | 2.9/3.3 | 10.8%/15% | 47% | -2.6% | 0.18 | 0.559 | low corr (avg rho 0.11); px > LO PT (ARM/ADBE); earnings <=3d after obs #1 (ARM) |
| 9 | MU + ARM + PDD | 85/60/60 | 9.2% / -1.4% | 68.0% | 80%/78% | 2.9/3.2 | 10.7%/14% | 46% | -2.6% | 0.17 | 0.558 | low corr (avg rho 0.30); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 10 | MU + AVGO + ARM | 85/60/60 | 9.2% / -1.3% | 68.3% | 80%/78% | 2.9/3.2 | 10.7%/13% | 46% | -2.6% | 0.17 | 0.558 | overlaps live 18/06,04/09; px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 11 | ARM + DDOG + BABA | 83/60/60 | 9.3% / -1.3% | 67.8% | 81%/77% | 2.9/3.3 | 10.6%/15% | 46% | -2.6% | 0.17 | 0.557 | low corr (avg rho 0.19); px > LO PT (ARM/DDOG); earnings <=3d after obs #1 (ARM/DDOG) |
| 12 | ARM + ADBE + DDOG | 83/60/60 | 9.1% / -1.5% | 67.4% | 81%/77% | 2.9/3.3 | 10.6%/15% | 46% | -2.6% | 0.17 | 0.554 | low corr (avg rho 0.11); px > LO PT (ARM/ADBE/DDOG); earnings <=3d after obs #1 (ARM/DDOG) |
| 13 | ARM + DDOG | 85/60/60 | 10.6% / 0.7% | 64.5% | 78%/76% | 3.1/3.4 | 11.7%/15% | 46% | -2.6% | 0.17 | 0.548 | px > LO PT (ARM/DDOG); earnings <=3d after obs #1 (ARM/DDOG) |
| 14 | MU + AMAT + ARM | 85/55/55 | 9.2% / -0.6% | 65.4% | 78%/76% | 3.1/3.4 | 11.5%/14% | 43% | -2.6% | 0.15 | 0.548 | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 15 | AMAT + ARM + PANW | 83/60/60 | 9.5% / -0.9% | 67.5% | 80%/77% | 2.9/3.3 | 10.9%/15% | 45% | -2.6% | 0.17 | 0.547 | low corr (avg rho 0.28); px > LO PT (ARM/PANW); earnings <=3d after obs #1 (ARM) |

- **CPN roll** = model coupon at an all-in take of 3.34% (the 24/09 fill's 5.84% less 2.5 pts of UF). **24-09 cost** = same structure at the 24/09 fill's all-in cost.
- **Client EV** (CPN × E[life]/12 − P(loss) × E[loss | loss]) comes out near −2.6% for every row. In a model where coupons and probabilities share one risk-neutral measure, it collapses to roughly minus the all-in fee plus a little funding, so it measures fee drag, not structure quality. At the 24/09 cost it is about −5% per roll.
- Penalties (−0.03 each): strong-day fix, avg ρ < 0.5 on 3 names, IV percentile > 90, ≥2 names shared with a live ledger basket. *px > LO PT* and *earnings ≤3d after obs #1* are shown but not penalised. Every row is below your regime coupon target and most have CPN/IV < 0.20, so those two flags are left out.

Internal only (UF 1.0% under roll pricing):

| # | Basket | Fee velocity p.a. | Net-of-UF yield p.a. | UF > 1-mth CPN and P(KO@1) > 70% | +CPN per 1% UF cut |
|---|---|---|---|---|---|
| 1 | ARM + DELL + DDOG | 4.5% | 4.9% | FLAG | 4.6% |
| 2 | ARM + DELL + PDD | 4.4% | 4.8% | FLAG | 4.5% |
| 3 | AVGO + ARM + DELL | 4.4% | 4.7% | FLAG | 4.5% |
| 4 | ARM + DELL + BABA | 4.2% | 5.8% |  | 4.3% |
| 5 | MU + ARM + ORCL | 4.3% | 5.2% |  | 4.3% |
| 6 | ARM + DELL | 4.0% | 7.4% |  | 4.0% |
| 7 | ARM + ORCL + PANW | 4.2% | 4.9% |  | 4.3% |
| 8 | ARM + DELL + ADBE | 4.2% | 5.8% |  | 4.2% |

## 3. Top 3 verdicts

1. **ARM + DELL + DDOG 80/60/60**: P(KO@1) 71.6%, P(loss) 9.7%, ~9% at roll pricing. **Rolls:** KO 80 sits 1.3 monthly σ below spot and memory KO locks each name as it clears. **Breaks:** ARM (LO Hold, PT $250 = 82% of spot, just above its $245 KO) de-rating into obs #1, or an ARM/DDOG print landing before 02/11 (both estimated 04–05/11).
2. **ARM + DELL + PDD 83/60/60**: P(KO@1) 70.7%, P(loss) 10.0%, ~9% at roll pricing. **Rolls:** same ARM + DELL engine, with PDD (LO Buy, +41% to PT) as a near-uncorrelated third leg. **Breaks:** an ARM-led AI-hardware sell-off in October; PDD adds China headline risk.
3. **AVGO + ARM + DELL 83/60/60**: P(KO@1) 70.7%, P(loss) 10.0%, ~9% at roll pricing. **Rolls:** AVGO (LO Buy, +43% to PT) is the quality anchor and the best-correlated third leg (avg ρ 0.43), which helps the worst-of KO. **Breaks:** an AI-complex sell-off into the mega-cap prints of 27–29/10, which fall inside obs #1.

Best-coupon alternative: **ARM + DELL 85/60/60** (two names): P(KO@1) 66.3%, P(loss) 11.5%, ~11% at roll pricing.
If you want no ARM exposure: **ORCL + PANW + DDOG 85/65/65** (P(KO@1) 67.2%, P(loss) 11.3%, ~10%); **MU + DELL + DDOG 83/60/60** (P(KO@1) 66.4%, P(loss) 11.3%, ~10%).

## 4. Why the coupons are thin: fee load and vol regime

The model prices each note at par less an all-in issuer take, calibrated to the 24/09 USD fill (MU + SNDK + SKHY 95/70/70 at 16.20%), which implies **5.84% of notional** (UF plus the issuer's margin plus model error). The other September fills imply a similar take:

| Fill | Basket | KO/Str/KI | Desk CPN | Implied all-in take | P(KO@1) | P(loss) |
|---|---|---|---|---|---|---|
| 04/09 MYR | MU + AVGO | 100/75/55 | 12.50% | 4.46% | 31.7% | 17.8% |
| 09/09 MYR | MU + SNDK + SKHY | 90/80/70 | 15.00% | 5.98% | 55.0% | 18.0% |
| 11/09 USD | NVDA + AMZN + GOOGL | 100/80/80 | 10.10% | 5.17% | 20.7% | 30.1% |
| 22/09 MYR | MU + SNDK + SKHY | 95/72.4/70 | 15.00% | 6.71% | 43.0% | 23.7% |
| 24/09 AUD | MU + SNDK + SKHY | 100/70/60 | 17.00% | 6.34% | 31.9% | 26.3% |

MYR and AUD fills are run on USD rates (no quanto adjustment), so read their implied take as ±1 pt. The term structure matters: 30-day IVs for NVDA, AVGO, PDD and PLTR sit 9–11 vol points under their 12-month IVs, so the model uses 30D IV for month 1 (your obs #1 odds) and the 12M-implied forward vol for months 2–12. With flat 30D vols the NVDA + AMZN + GOOGL fill read 4.1 pts too low; with the term structure it reads within 1.3 pts.

A fixed take hits short-life notes hardest. For the top structure the coupon annuity is 0.218, so each 1% of fee is worth 4.6% p.a. of coupon:

**ARM + DELL + DDOG**, same basket, different structures:

| KO/Str/KI | P(KO@1) | P(KO≤3) | E[life] m | P(loss) | E[loss\|loss] | CPN @24/09 cost | CPN @roll | Hard filters |
|---|---|---|---|---|---|---|---|---|
| 80/60/60 | 71.5% | 83% | 2.7 | 9.8% | 49% | -2.0% | 9.5% | pass |
| 85/60/60 | 56.2% | 72% | 3.7 | 16.0% | 48% | 8.5% | 16.7% | P(loss) > 12% |
| 90/60/60 | 40.3% | 59% | 4.9 | 23.4% | 46% | 14.7% | 20.9% | P(KO@1) < 55%; P(loss) > 12% |
| 95/60/60 | 26.5% | 46% | 6.2 | 31.1% | 45% | 18.3% | 23.2% | P(KO@1) < 55%; P(loss) > 12% |
| 95/70/60 | 26.5% | 46% | 6.2 | 31.1% | 52% | 23.0% | 27.9% | P(KO@1) < 55%; P(loss) > 12% |
| 100/70/60 | 15.9% | 34% | 7.4 | 38.4% | 51% | 25.4% | 29.5% | P(KO@1) < 55%; P(loss) > 12% |

At the September cost this basket pays 8.5% at KO 85 (P(KO@1) 56%, P(loss) 16%) and 14.7% at KO 90 (P(KO@1) 40%, P(loss) 23%). Getting to 12–16% means breaking your P(KO@1) and P(loss) filters: today, coupon and monthly KO pull against each other.

The July–August fills (KO 80–85, KI 50–60, ~20%) only reprice at a September-like all-in take if memory vols were 20–30 points higher than today, which matches July's daily moves in MU and SNDK:

| Fill | Basket | KO/Str/KI | Desk CPN | take @ vol +0 | take @ vol +10 | take @ vol +20 | take @ vol +30 |
|---|---|---|---|---|---|---|---|
| 08/07 MYR | MU + SNDK + WDC | 85/50/50 | 20.22% | 0.1% | 1.7% | 3.6% | 5.7% |
| 15/07 MYR | MU + SNDK + WDC | 80/60/60 | 19.66% | 0.7% | 2.2% | 3.9% | 5.8% |
| 13/08 USD | MU + SNDK + WDC | 83/60/60 | 20.00% | 1.1% | 2.8% | 4.7% | 6.8% |
| 21/08 USD | MU + SNDK + SKHY | 85/65/65 | 18.60% | 2.0% | 3.8% | 5.8% | 8.0% |

Your recent and live house structures, re-run for a 01/10 fixing (caps off):

| Basket | KO/Str/KI | CPN @24/09 cost | P(KO@1) | P(KO≤3) | P(loss) | E[loss\|loss] | Fails | Prints in obs #1 |
|---|---|---|---|---|---|---|---|---|
| MU + SNDK + SKHY | 95/70/70 | 15.6% | 43.9% | 61% | 22.9% | 48% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | SNDK 2026-10-30, SKHY 2026-10-27 |
| MU + SNDK + SKHY | 100/70/60 | 17.7% | 32.1% | 51% | 25.8% | 50% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | SNDK 2026-10-30, SKHY 2026-10-27 |
| MU + SNDK + SKHY | 85/60/60 | -0.7% | 69.0% | 80% | 10.9% | 46% | KI within 10% of 13W low | SNDK 2026-10-30, SKHY 2026-10-27 |
| NVDA + AMZN + GOOGL | 100/80/80 | 8.7% | 20.8% | 43% | 29.9% | 30% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | AMZN 2026-10-29, GOOGL 2026-10-27 |
| MU + AVGO | 100/75/55 | 9.0% | 31.8% | 53% | 17.2% | 50% | P(KO@1) < 55%; P(loss) > 12% | none |
| MU + AVGO | 90/60/60 | -7.5% | 66.8% | 80% | 9.1% | 37% | none | none |

Vol regime: 52-week IV percentiles are SKHY 2%, NVDA 1%, AVGO 2%, SNDK 6%, MU 21%. Selling vol (which is what the client does in an ACEL) pays little until it re-rates, typically after a sell-off or into earnings, and your earnings filter rules out the second.

## 5. Coupon lever that keeps P(loss): strike above KI

A strike above the KI leaves P(loss) unchanged (the KI still sets the loss event) but raises the loss once it happens. You have used it before (04/09 75/55, 09/09 80/70).

| Basket | KO/Str/KI | CPN @roll | CPN @24/09 | P(KO@1) | P(loss) | E[loss\|loss] |
|---|---|---|---|---|---|---|
| ARM + DELL + DDOG | 80/60/60 | 9.4% | -2.1% | 71.6% | 9.7% | 49% |
| ARM + DELL + DDOG | 80/65/60 | 11.1% | -0.4% | 71.6% | 9.7% | 53% |
| ARM + DELL + DDOG | 80/70/60 | 12.5% | 1.0% | 71.6% | 9.7% | 57% |
| ARM + DELL + PDD | 83/60/60 | 9.2% | -2.0% | 70.7% | 10.0% | 48% |
| ARM + DELL + PDD | 83/65/60 | 10.9% | -0.2% | 70.7% | 10.0% | 52% |
| ARM + DELL + PDD | 83/70/60 | 12.4% | 1.2% | 70.7% | 10.0% | 55% |
| AVGO + ARM + DELL | 83/60/60 | 9.1% | -2.0% | 70.7% | 10.0% | 48% |
| AVGO + ARM + DELL | 83/65/60 | 10.8% | -0.3% | 70.7% | 10.0% | 52% |
| AVGO + ARM + DELL | 83/70/60 | 12.3% | 1.2% | 70.7% | 10.0% | 55% |

## 6. Desk request lines (Florence)

```
USD 12M ARM UW + DELL UN + DDOG UW | Strike 60 | KO 80 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN + DDOG UW | Strike 70 | KO 80 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN + PDD UW | Strike 60 | KO 83 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN + PDD UW | Strike 70 | KO 83 | KI 60 | CPN ?
USD 12M AVGO UW + ARM UW + DELL UN | Strike 60 | KO 83 | KI 60 | CPN ?
USD 12M AVGO UW + ARM UW + DELL UN | Strike 70 | KO 83 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN | Strike 60 | KO 85 | KI 60 | CPN ?
USD 12M ORCL UN + PANW UW + DDOG UW | Strike 65 | KO 85 | KI 65 | CPN ?
```

- Ask for each line at your standard UF and at UF 1.0%. The model expects roughly −2% to +1% and 9–12.5% respectively, with the strike-70 variants ~3 pts higher.
- Memory KO, monthly obs, European KI, closing prices. Preferred fixing 01/10, after MU's 30/09 print has moved the AI-hardware complex. Obs #1 then lands 02/11, 2–3 days before ARM's and DDOG's estimated prints: get both dates confirmed first, and if either lands on or before 02/11, fix by 29/09 instead.
- Re-check the 20-day-MA strong-day test on the fixing morning.

## 7. Release drafts: pre-filled, waiting on the quote

```
🇺🇸 *Private Tranche ACEL*

*ARM UW + DELL UN + DDOG UW*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 80%
Strike: 60%
KI: 60%

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $245.07
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Dell Technologies C (DELL UN)
Current Price: $536.02
52-Week High: $595.51
Indicative KO Price: $428.82
Indicative Strike Price: $321.61
Indicative KI Price: $321.61

Datadog Inc (DDOG UW)
Current Price: $256.92
52-Week High: $292.72
Indicative KO Price: $205.54
Indicative Strike Price: $154.15
Indicative KI Price: $154.15

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 01 Oct 2026.
```

```
🇺🇸 *Private Tranche ACEL*

*ARM UW + DELL UN + PDD UW*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 83%
Strike: 60%
KI: 60%

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $254.26
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Dell Technologies C (DELL UN)
Current Price: $536.02
52-Week High: $595.51
Indicative KO Price: $444.90
Indicative Strike Price: $321.61
Indicative KI Price: $321.61

PDD Holdings ADR (PDD UW)
Current Price: $78.20
52-Week High: $139.41
Indicative KO Price: $64.91
Indicative Strike Price: $46.92
Indicative KI Price: $46.92

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 01 Oct 2026.
```

```
🇺🇸 *Private Tranche ACEL*

*AVGO UW + ARM UW + DELL UN*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 83%
Strike: 60%
KI: 60%

Broadcom Inc (AVGO UW)
Current Price: $350.36
52-Week High: $494.23
Indicative KO Price: $290.80
Indicative Strike Price: $210.22
Indicative KI Price: $210.22

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $254.26
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Dell Technologies C (DELL UN)
Current Price: $536.02
52-Week High: $595.51
Indicative KO Price: $444.90
Indicative Strike Price: $321.61
Indicative KI Price: $321.61

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 01 Oct 2026.
```

Do not send until Florence's coupon is approved. Update the trade date if you fix on 29/09.

## Method and assumptions

- Spot = 24/09 close; 52W high = max(live, IBKR 52W high); 13W low from IBKR. Correlations from 1Y daily log returns (SKHY since its July listing). Risk-neutral drift, r = 3.5%, LO dividend yields.
- Vol: 30D ATM IV in month 1, forward vol from ~12M ATM option IV (Sep-2027 expiry, 24/09 mids) in months 2–12, and a +5 vol-pt bump phasing in between 100% and the KI level. MU month 1 uses 53.1%: its 30D IV less the ±8.9% move implied by the 02/10 straddle.
- Loss at maturity if no KO and worst-of < KI: 1 − WO/Strike. KO modes: memory per stock (ranked) and simultaneous (shown after the slash).
- Roll Score = 0.45·P(KO@1) + 0.25·P(KO≤3) + 0.20·(1 − P(loss)/0.12) + 0.10·min(CPN/IV ÷ 0.30, 1) − 0.03 per penalty, with CPN at roll pricing and IV = basket average 30D IV.
- Earnings dates: MU 30/09 and AMD 03/11 confirmed; the rest are vendor estimates. ANET is estimated for 02/11, obs #1 itself, and treated as a fail until confirmed.
- All probabilities are risk-neutral. With a positive equity risk premium, P(KO) would be modestly higher and P(loss) modestly lower. The ranking would barely move.

