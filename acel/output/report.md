# ACEL monthly-roll screen: Lombard Odier research list (17.09.2026), repriced to the desk

Fixing **02/10/2026** (the desk's assumed trade date), obs #1 **02/11/2026**. Market data: IBKR, closes of 24 Sep 2026. Coupons calibrated to the desk's 28/09/2026 quotes (8 lines, KO 95, UF 4%). Model: correlated-GBM Monte Carlo, 50,000 paths per structure over 680 baskets (12,002 structures), finalists re-run at 200,000 paths. Coupons are model estimates for ranking and quote requests, not quotes.

## Bottom line

- **The first pass overpriced coupons, and the desk's quotes show where.** It took its fee level from the 24/09 fill and priced on historical correlations. On those assumptions the 8 quotes imply an all-in take of 8.1% at UF 4% and fit to only ±1.8 pts. The desk marks correlation well above realized on these low-correlation tech baskets: ARM + DELL + DDOG has a historical average ρ of 0.24. A worst-of put on names marked more correlated is worth less, so the coupon is lower. With pricing correlations floored at 0.6, the quotes fit to ±1.1 pts at an all-in take of **7.1% at UF 4%**, i.e. an issuer spread of **3.1% before UF**. Probabilities stay on historical correlations, which is the conservative side for a worst-of.
- **No structure clears every hard filter at a ≥9% coupon, even at UF 1%.** 8,499 structures pass the filters, and the best of them pays 7.4% at UF 1% (AMD + ARM + DELL 83/60/60). The desk's "KO 80–83 can't get anything of value" matches the model: at UF 4% every KO 80–85 structure prices below zero. Most of that is the UF. On a note expected to live 2–3 months, each 1% of UF costs 4–5.5% p.a. of coupon, so UF 4% takes 17–22 pts off a KO 80–85 coupon.
- **Closest to the framework: ARM + DELL KO 88 / Strike 60 / KI 60**, ~10.7% at UF 1%. P(KO @ obs #1) 58.6%, P(KO by obs #3) 73.6%, P(loss) 14.5%, which misses the 12% filter; average loss 47% when it does lose. Every ≥9% structure in the ranked table misses P(loss) by 1–3 pts. Relaxing that filter to ~15% is the price of a 9–11% monthly-roll coupon today.
- **One open question, which the next quote settles.** The KO 95 quotes fit a 0.6 to 0.8 correlation floor about equally well, but short-life coupons differ: at 0.8 the KO 85–88 lines read 2.5–4 pts higher, enough to reopen a ≥9% roll that passes every filter. This report uses 0.6, the conservative end. The desk's price on the KO 85–88 lines below at UF 1% tells us which.
- **The desk's KO 95 lines are not monthly-roll trades.** P(KO @ obs #1) 27%–40%, P(loss) 22%–31%, and an average loss of 41%–52% when it happens. They are 12-month coupon trades. If you take one, ARM + DELL 95/60/60 at 8.85% has the best KO odds and the lowest P(loss) of the set.
- **Counters:** ARM is the engine, in 90 of the 208 baskets that reach 9% at UF 1% with the earnings and 13-week-low rules intact. DELL is its best partner (68 baskets); ORCL, MU, NVDA, AMAT and AVGO fill the third slot in the top 6.

## 1. The desk's 28/09/2026 quotes against the model

Trade date 02/10/2026, UF 4%, all at KO 95 because the desk could not price KO 80–83 at that UF. Model coupons at the fitted take; probabilities on historical correlations.

| Basket | KO/Str/KI | Desk CPN | Model CPN | Diff | avg ρ | P(KO@1) | P(KO≤3) | E[life] m | P(loss) | E[loss\|loss] | Fails |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ARM + DELL + DDOG | 95/60/60 | 11.39% | 12.50% | +1.11 | 0.24 | 26.6% | 46% | 6.2 | 31.0% | 45% | P(KO@1); P(loss) |
| ARM + DELL + DDOG | 95/70/60 | 15.14% | 16.93% | +1.79 | 0.24 | 26.6% | 46% | 6.2 | 31.0% | 52% | P(KO@1); P(loss) |
| ARM + DELL + PDD | 95/60/60 | 9.73% | 9.23% | -0.50 | 0.25 | 31.5% | 52% | 5.6 | 25.8% | 43% | P(KO@1); P(loss) |
| ARM + DELL + PDD | 95/70/60 | 13.40% | 13.45% | +0.05 | 0.25 | 31.5% | 52% | 5.6 | 25.8% | 51% | P(KO@1); P(loss) |
| AVGO + ARM + DELL | 95/60/60 | 9.64% | 9.67% | +0.03 | 0.43 | 34.3% | 54% | 5.5 | 25.4% | 43% | P(KO@1); P(loss) |
| AVGO + ARM + DELL | 95/70/60 | 13.40% | 13.94% | +0.54 | 0.43 | 34.3% | 54% | 5.5 | 25.4% | 51% | P(KO@1); P(loss) |
| ARM + DELL | 95/60/60 | 8.85% | 7.92% | -0.93 | 0.41 | 40.3% | 59% | 4.9 | 21.9% | 44% | P(KO@1); P(loss) |
| ORCL + PANW + DDOG | 95/65/65 | 10.33% | 8.49% | -1.84 | 0.41 | 34.0% | 53% | 5.5 | 25.9% | 41% | P(KO@1); P(loss) |

The biggest miss is ORCL + PANW + DDOG 95/65/65 (-1.8 pts). One correlation floor cannot match every basket, because the desk's single-name vol and skew marks also differ from the ATM-plus-bump used here. The model also values strike 70 over strike 60 0.5–0.7 pts higher than the desk does.

| Pricing correlation | All-in take @UF 4% | Issuer spread ex-UF | Fit error (RMS, pts) |
|---|---|---|---|
| historical | 8.08% | 4.08% | 1.84 |
| floored at 0.4 | 7.89% | 3.89% | 1.45 |
| floored at 0.5 | 7.55% | 3.55% | 1.26 |
| floored at 0.6 | 7.06% | 3.06% | 1.07 |
| floored at 0.7 | 6.48% | 2.48% | 0.96 |
| floored at 0.8 | 5.79% | 1.79% | 0.90 |

Floors from 0.6 to 0.8 fit about equally well. 0.6 is used because it leaves the larger issuer spread, the conservative choice for short-life notes where the take dominates the coupon. At a 0.8 floor the KO 85–88 coupons below would read 2.5–4 pts higher.

The September fills, repriced on the same basis, and the UF each one implies (your records will say whether these are right):

| Fill | Basket | KO/Str/KI | Desk CPN | Implied all-in take | Implied UF | P(KO@1) | P(loss) |
|---|---|---|---|---|---|---|---|
| 04/09 MYR | MU + AVGO | 100/75/55 | 12.50% | 4.29% | 1.2% | 31.7% | 17.8% |
| 09/09 MYR | MU + SNDK + SKHY | 90/80/70 | 15.00% | 5.98% | 2.9% | 55.0% | 18.0% |
| 11/09 USD | NVDA + AMZN + GOOGL | 100/80/80 | 10.10% | 4.36% | 1.3% | 20.7% | 30.1% |
| 22/09 MYR | MU + SNDK + SKHY | 95/72.4/70 | 15.00% | 6.71% | 3.6% | 43.0% | 23.7% |
| 24/09 AUD | MU + SNDK + SKHY | 100/70/60 | 17.00% | 6.34% | 3.3% | 31.9% | 26.3% |
| 24/09 USD | MU + SNDK + SKHY | 95/70/70 | 16.20% | 5.84% | 2.8% | 43.0% | 23.7% |

MYR and AUD fills are run on USD rates (no quanto adjustment), so read their implied UF as ±1 pt. If any implied UF is far from what you charged, send me the actual UFs and I will refit the spread.

## 2. Counters in the lists, screened

US lines only (ACEL chassis). Not modelled: Sell-rated names (SpaceX, Enphase, First Solar, Nike); names without a US line (Samsung, Tencent, Xiaomi, BYD and the European and Swiss names); small caps (Mirion, On, Service Corp); low-vol defensives (Verizon, AT&T, McDonald's, Home Depot); and names outside the house style (IBM, Spotify, Booking, Pinterest, TKO, Aptiv, Trimble, Logitech, Nokia, STMicro, SAP, Baidu, Ferrari).

| Counter | LO | LO PT upside | IV 30D | IV 12M | IV pct 52w | vs 52W hi | KI cap (13W) | vs 20D MA | Next print | Verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| ARM UW | H | -18% | 67% | 73% | 60% | -32% | 64% | 15% | 04/11 (e) | Tier 1 engine (90 baskets, best #1) |
| DELL UN | B | 12% | 60% | 68% | 51% | -10% | 60% | 2% | 24/11 (e) | Tier 1 engine (68 baskets, best #1) |
| DDOG UW | H | -4% | 57% | 63% | 51% | -12% | 71% | 11% | 05/11 (e) | Tier 1 third leg (71 baskets, best #15) |
| MU UW | H | 11% | 61% | 62% | 21% | -14% | 61% | 10% | 30/09 (c) | Tier 1 engine (40 baskets, best #3) |
| PANW UW | H | -8% | 51% | 57% | 69% | -2% | 67% | 8% | 12/11 (e) | Tier 1 third leg (47 baskets, best #13) |
| ORCL UN | H | 4% | 49% | 56% | 20% | -56% | 74% | -7% | 14/12 (e) | Tier 1 third leg (50 baskets, best #2) |
| AMAT UW | H | 10% | 54% | 56% | 51% | -36% | 78% | 5% | 12/11 (e) | Tier 1 third leg (49 baskets, best #4) |
| AVGO UW | B | 43% | 35% | 44% | 2% | -29% | 86% | -2% | 10/12 (e) | Tier 2 third leg (28 baskets, best #6) |
| NVDA UW | SB | 16% | 30% | 39% | 1% | -5% | 76% | 1% | 18/11 (e) | Tier 1 third leg (24 baskets, best #3) |
| PDD UW | B | 41% | 30% | 40% | 16% | -44% | 83% | -3% | 18/11 (e) | Tier 2 third leg (24 baskets, best #8) |
| DIS UN | SB | 36% | 24% | 29% | 29% | -9% | 79% | -0% | 12/11 (e) | Tier 2 third leg (19 baskets, best #14) |
| BABA UN | B | 95% | 38% | 44% | 14% | -43% | 76% | -1% | 19/11 (e) | Tier 2 third leg (30 baskets, best #23) |
| ADBE UW | H | -2% | 38% | 45% | 30% | -34% | 74% | -9% | 10/12 (e) | Tier 2 third leg (30 baskets, not in top 25) |
| AMD UW | H | -24% | 52% | 58% | 22% | -2% | 61% | 21% | 03/11 (c) | Tier 2 third leg (36 baskets, best #11, strong-day fix) |
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

*KI cap (13W)* = 90% of the 13-week low ÷ spot, the highest KI that clears your 13-week-low hard filter. (c) confirmed date, (e) vendor estimate or prior-year pattern. LO PT upside is recomputed at the 24/09 close (foreign-listed lines keep the list's 17/09 figure). *Baskets* = baskets reaching 9% at UF 1% with the earnings and 13W rules intact; *best #* = the name's best position in the ranked table below; *engine* = 30D IV ≥ 58%.

## 3. Ranked structures

Nothing passes every hard filter at ≥9%, so the table ranks structures that reach **9% p.a. at UF 1%** with the earnings rule (no print before obs #1) and the 13-week-low KI rule intact, ordered by Roll Score. The *Misses* column shows which of the P(KO@1) ≥ 55% and P(loss) ≤ 12% filters each one fails. Grid: KO 80–95, Strike = KI 50–80, inside your rules of thumb (KO ≤ 100 − 0.5·σ₁ₘ, KI ≤ e^(−0.75σ)). Ranked on memory KO; simultaneous KO shown after the slash.

| # | Basket | KO/Str/KI | CPN @UF 1% / 4% | P(KO@1) | P(KO≤3) mem/sim | E[life] m | P(loss) | E[loss\|loss] | Client EV | CPN/IV | Score | Misses | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ARM + DELL | 88/60/60 | 10.7% / -0.1% | 58.6% | 74%/72% | 3.5/3.8 | 14.5%/17% | 47% | -3.6% | 0.17 | 0.462 | P(loss) | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 2 | ARM + DELL + ORCL | 85/60/60 | 10.0% / -1.6% | 61.5% | 75%/73% | 3.4/3.8 | 14.0%/18% | 47% | -3.8% | 0.17 | 0.460 | P(loss) | low corr (avg rho 0.41); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 3 | MU + NVDA + ARM | 88/60/60 | 9.1% / -1.9% | 60.1% | 75%/72% | 3.4/3.8 | 13.7%/17% | 45% | -3.5% | 0.17 | 0.455 | P(loss) | low corr (avg rho 0.46); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 4 | AMAT + ARM + DELL | 85/60/60 | 10.2% / -1.1% | 60.8% | 75%/72% | 3.4/3.8 | 14.2%/18% | 47% | -3.7% | 0.17 | 0.450 | P(loss) | low corr (avg rho 0.43); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 5 | MU + ARM + DELL | 85/60/60 | 10.7% / -0.7% | 60.6% | 75%/72% | 3.4/3.8 | 14.3%/18% | 48% | -3.8% | 0.17 | 0.448 | P(loss) | low corr (avg rho 0.41); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 6 | MU + AVGO + ARM | 88/60/60 | 9.6% / -1.2% | 59.5% | 74%/72% | 3.5/3.8 | 14.1%/17% | 44% | -3.5% | 0.18 | 0.447 | P(loss) | overlaps live 18/06,04/09; px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 7 | AMAT + ARM | 90/60/60 | 9.8% / -0.2% | 56.6% | 72%/70% | 3.7/3.9 | 14.7%/16% | 43% | -3.3% | 0.16 | 0.444 | P(loss) | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 8 | MU + ARM + PDD | 88/60/60 | 9.1% / -1.9% | 58.6% | 74%/70% | 3.5/4.0 | 14.1%/18% | 44% | -3.6% | 0.17 | 0.441 | P(loss) | low corr (avg rho 0.30); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 9 | MU + AMAT + ARM | 88/55/55 | 9.2% / -0.8% | 57.0% | 72%/70% | 3.7/4.0 | 14.8%/17% | 42% | -3.4% | 0.15 | 0.440 | P(loss) | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 10 | MU + ARM | 90/60/60 | 10.8% / 0.6% | 56.2% | 72%/70% | 3.7/3.9 | 15.0%/17% | 45% | -3.4% | 0.17 | 0.438 | P(loss) | px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 11 | AMD + ARM + DELL | 85/60/60 | 10.1% / -1.4% | 62.1% | 76%/73% | 3.3/3.7 | 13.7%/17% | 47% | -3.6% | 0.17 | 0.437 | P(loss) | strong-day fix (AMD); low corr (avg rho 0.48); px > LO PT (AMD/ARM); earnings <=3d after obs #1 (AMD/ARM) |
| 12 | AMD + ARM | 90/60/60 | 9.8% / -0.4% | 58.3% | 73%/72% | 3.6/3.8 | 14.1%/15% | 44% | -3.2% | 0.16 | 0.435 | P(loss) | strong-day fix (AMD); px > LO PT (AMD/ARM); earnings <=3d after obs #1 (AMD/ARM) |
| 13 | ARM + DELL + PANW | 85/60/60 | 10.1% / -1.4% | 59.1% | 74%/70% | 3.5/4.0 | 14.7%/20% | 47% | -4.0% | 0.17 | 0.433 | P(loss) | low corr (avg rho 0.28); px > LO PT (ARM/PANW); earnings <=3d after obs #1 (ARM) |
| 14 | ARM + DELL + DIS | 88/60/60 | 10.8% / 0.1% | 57.1% | 73%/69% | 3.6/4.1 | 15.0%/19% | 46% | -3.6% | 0.21 | 0.430 | P(loss) | low corr (avg rho 0.18); px > LO PT (ARM); earnings <=3d after obs #1 (ARM) |
| 15 | MU + ARM + DDOG | 85/60/60 | 9.6% / -2.0% | 58.5% | 74%/70% | 3.5/4.1 | 14.7%/20% | 46% | -4.0% | 0.15 | 0.424 | P(loss) | low corr (avg rho 0.25); px > LO PT (ARM/DDOG); earnings <=3d after obs #1 (ARM/DDOG) |

- **CPN** at an all-in take of 4.06% (UF 1%) and 7.06% (UF 4%, the desk's basis on 28/09/2026).
- **Client EV** (CPN × E[life]/12 − P(loss) × E[loss | loss]) runs -4.0% to -3.2% per roll. Coupons are priced on the desk's correlation mark and probabilities on historical correlation, so it measures fee drag plus that correlation premium, not structure quality.
- Penalties (−0.03 each): strong-day fix, avg ρ < 0.5 on 3 names, IV percentile > 90, ≥2 names shared with a live ledger basket. *px > LO PT* and *earnings ≤3d after obs #1* are shown but not penalised. Every row is below your regime coupon target and has CPN/IV < 0.20, so those two flags are left out.

**Every hard filter passing (roll-friendly, thin coupon):** best coupon per basket at UF 1%.

| Basket | KO/Str/KI | CPN @UF 1% | CPN @UF 0% | P(KO@1) | P(KO≤3) | E[life] m | P(loss) | E[loss\|loss] | Flags |
|---|---|---|---|---|---|---|---|---|---|
| AMD + ARM + DELL | 83/60/60 | 7.4% | 11.7% | 67.6% | 80% | 3.0 | 11.6% | 48% | strong-day fix (AMD); low corr (avg rho 0.48) |
| ARM + DELL + DIS | 85/60/60 | 7.3% | 11.5% | 65.7% | 79% | 3.0 | 11.7% | 47% | low corr (avg rho 0.18) |
| AMD + ARM | 88/60/60 | 7.0% | 10.9% | 63.6% | 77% | 3.2 | 11.8% | 44% | strong-day fix (AMD) |
| ARM + DELL + ORCL | 83/60/60 | 6.9% | 11.3% | 67.3% | 80% | 3.0 | 11.6% | 48% | low corr (avg rho 0.41) |
| MU + AMD + ARM | 85/55/55 | 6.5% | 10.4% | 65.4% | 78% | 3.1 | 11.7% | 43% | strong-day fix (AMD) |
| ARM + DELL | 85/60/60 | 6.3% | 10.6% | 66.6% | 79% | 3.0 | 11.1% | 47% |  |

Internal only (UF 1%):

| # | Basket | Fee velocity p.a. | Net-of-UF yield p.a. | UF > 1-mth CPN and P(KO@1) > 70% | −CPN per +1% UF | Max UF for 9% |
|---|---|---|---|---|---|---|
| 1 | ARM + DELL | 3.4% | 7.3% |  | 3.6% | 1.47% |
| 2 | ARM + DELL + ORCL | 3.6% | 6.4% |  | 3.9% | 1.26% |
| 3 | MU + NVDA + ARM | 3.5% | 5.6% |  | 3.7% | 1.03% |
| 4 | AMAT + ARM + DELL | 3.5% | 6.7% |  | 3.8% | 1.33% |
| 5 | MU + ARM + DELL | 3.5% | 7.2% |  | 3.8% | 1.45% |
| 6 | MU + AVGO + ARM | 3.4% | 6.2% |  | 3.6% | 1.17% |
| 7 | AMAT + ARM | 3.2% | 6.6% |  | 3.3% | 1.25% |
| 8 | MU + ARM + PDD | 3.4% | 5.7% |  | 3.7% | 1.04% |

## 4. Top 3 verdicts

1. **ARM + DELL 88/60/60**: P(KO@1) 58.6%, P(loss) 14.5%, ~10.7% at UF 1%. **Rolls:** two names, so one fewer way to miss, and memory KO locks DELL (LO Buy, +12% to PT) on its own; KO 88 sits 0.7 monthly σ below spot. **Breaks:** ARM, which trades 23% above LO's $250 PT (below its KO price) and 15% above its 20-day MA, with its print estimated 04/11, two days after obs #1.
2. **ARM + DELL + ORCL 85/60/60**: P(KO@1) 61.5%, P(loss) 14.0%, ~10.0% at UF 1%. **Rolls:** KO 85 is the widest cushion in the top 3 (1.0 monthly σ), and ORCL, 56% below its 52-week high, has already de-rated. **Breaks:** ARM, which trades 23% above LO's $250 PT (below its KO price) and 15% above its 20-day MA, with its print estimated 04/11, two days after obs #1; ORCL (LO Hold) is the lagging leg if AI-capex sentiment turns.
3. **MU + NVDA + ARM 88/60/60**: P(KO@1) 60.1%, P(loss) 13.7%, ~9.1% at UF 1%. **Rolls:** the most correlated of the top 3 (avg ρ 0.46); NVDA (LO Strong Buy, +16% to PT) at ~30% IV damps the worst-of, and MU fixes after its 30/09 print. **Breaks:** the mega-cap prints of 27–29/10 inside obs #1 moving NVDA, or MU giving back its post-print move; ARM, which trades 23% above LO's $250 PT (below its KO price) and 15% above its 20-day MA, with its print estimated 04/11, two days after obs #1.

If you want no ARM exposure: **ORCL + PANW + DDOG 88/65/65** (P(KO@1) 57.0%, P(loss) 15.4%, ~9.7%); **ORCL + DDOG + DIS 90/70/70** (P(KO@1) 54.1%, P(loss) 15.7%, ~9.6%).

## 5. Why the coupons are thin: UF on a short-life note, and the vol regime

A fixed take hits short-life notes hardest. For the top structure the coupon annuity is 0.279 (expected life 3.5 months), so each 1% of UF moves the coupon by 3.6% p.a. Same basket, different structures:

**ARM + DELL**:

| KO/Str/KI | P(KO@1) | P(KO≤3) | E[life] m | P(loss) | E[loss\|loss] | CPN @UF 1% | CPN @UF 2% | CPN @UF 4% | Hard filters |
|---|---|---|---|---|---|---|---|---|---|
| 80/60/60 | 78.3% | 87% | 2.2 | 7.2% | 49% | -1.4% | -7.0% | -18.2% | pass |
| 85/60/60 | 66.5% | 79% | 3.0 | 11.5% | 47% | 7.1% | 2.9% | -5.5% | pass |
| 88/60/60 | 58.6% | 74% | 3.5 | 14.4% | 46% | 10.6% | 7.0% | -0.2% | P(loss) > 12% |
| 90/60/60 | 53.3% | 70% | 3.9 | 16.5% | 46% | 12.5% | 9.2% | 2.7% | P(KO@1) < 55%; P(loss) > 12% |
| 95/60/60 | 40.4% | 59% | 4.9 | 22.0% | 44% | 15.8% | 13.2% | 8.0% | P(KO@1) < 55%; P(loss) > 12% |
| 95/70/60 | 40.4% | 59% | 4.9 | 22.0% | 52% | 19.9% | 17.3% | 12.1% | P(KO@1) < 55%; P(loss) > 12% |

Coupon and monthly KO pull against each other: the KO 95 rows pay the desk-style coupons but knock out at obs #1 less than half the time; the KO 80–85 rows roll but only pay at a low UF.

The July–August fills (KO 80–85, KI 50–60, ~20%) only reprice at a September-like take if memory vols were 20–30 points higher than today, which matches July's daily moves in MU and SNDK:

| Fill | Basket | KO/Str/KI | Desk CPN | take @ vol +0 | take @ vol +10 | take @ vol +20 | take @ vol +30 |
|---|---|---|---|---|---|---|---|
| 08/07 MYR | MU + SNDK + WDC | 85/50/50 | 20.22% | 0.1% | 1.7% | 3.6% | 5.7% |
| 15/07 MYR | MU + SNDK + WDC | 80/60/60 | 19.66% | 0.7% | 2.2% | 3.9% | 5.8% |
| 13/08 USD | MU + SNDK + WDC | 83/60/60 | 20.00% | 1.1% | 2.8% | 4.7% | 6.8% |
| 21/08 USD | MU + SNDK + SKHY | 85/65/65 | 18.60% | 2.0% | 3.8% | 5.8% | 8.0% |

Your recent and live house structures, re-run for a 02/10/2026 fixing (caps off):

| Basket | KO/Str/KI | CPN @UF 4% | CPN @UF 1% | P(KO@1) | P(KO≤3) | P(loss) | E[loss\|loss] | Fails | Prints in obs #1 |
|---|---|---|---|---|---|---|---|---|---|
| MU + SNDK + SKHY | 95/70/70 | 12.4% | 20.1% | 43.9% | 61% | 22.9% | 48% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | SNDK 30/10/2026, SKHY 27/10/2026 |
| MU + SNDK + SKHY | 100/70/60 | 15.1% | 21.5% | 32.1% | 51% | 25.8% | 50% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | SNDK 30/10/2026, SKHY 27/10/2026 |
| MU + SNDK + SKHY | 85/60/60 | -5.8% | 6.8% | 69.0% | 80% | 10.9% | 46% | KI within 10% of 13W low | SNDK 30/10/2026, SKHY 27/10/2026 |
| NVDA + AMZN + GOOGL | 100/80/80 | 4.3% | 10.6% | 20.8% | 43% | 29.9% | 30% | KI within 10% of 13W low; P(KO@1) < 55%; P(loss) > 12% | AMZN 29/10/2026, GOOGL 27/10/2026 |
| MU + AVGO | 100/75/55 | 5.7% | 12.6% | 31.8% | 53% | 17.2% | 50% | P(KO@1) < 55%; P(loss) > 12% | none |
| MU + AVGO | 90/60/60 | -13.4% | -0.5% | 66.8% | 80% | 9.1% | 37% | none | none |

Vol regime: 52-week IV percentiles are SKHY 2%, NVDA 1%, AVGO 2%, SNDK 6%, MU 21%. Selling vol (which is what the client does in an ACEL) pays little until it re-rates, typically after a sell-off or into earnings, and your earnings filter rules out the second.

## 6. Coupon lever that keeps P(loss): strike above KI

A strike above the KI leaves P(loss) unchanged (the KI still sets the loss event) but raises the loss once it happens. The desk prices this lever at ~3.7 pts per 10 strike points on the KO 95 lines; the model reads it ~0.5 pts richer.

| Basket | KO/Str/KI | CPN @UF 1% | CPN @UF 4% | P(KO@1) | P(loss) | E[loss\|loss] |
|---|---|---|---|---|---|---|
| ARM + DELL | 88/60/60 | 10.7% | -0.1% | 58.6% | 14.5% | 47% |
| ARM + DELL | 88/65/60 | 12.6% | 1.8% | 58.6% | 14.5% | 51% |
| ARM + DELL | 88/70/60 | 14.3% | 3.5% | 58.6% | 14.5% | 54% |
| ARM + DELL + ORCL | 85/60/60 | 10.0% | -1.6% | 61.5% | 14.0% | 47% |
| ARM + DELL + ORCL | 85/65/60 | 11.9% | 0.3% | 61.5% | 14.0% | 51% |
| ARM + DELL + ORCL | 85/70/60 | 13.6% | 2.0% | 61.5% | 14.0% | 55% |
| MU + NVDA + ARM | 88/60/60 | 9.1% | -1.9% | 60.1% | 13.7% | 45% |
| MU + NVDA + ARM | 88/65/60 | 11.1% | 0.0% | 60.1% | 13.7% | 49% |
| MU + NVDA + ARM | 88/70/60 | 12.7% | 1.7% | 60.1% | 13.7% | 52% |

## 7. Desk request lines (Florence)

```
Assuming TD 2/10 - UF 1%
USD 12M ARM UW + DELL UN | Strike 60 | KO 88 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN | Strike 70 | KO 88 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN + ORCL UN | Strike 60 | KO 85 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN + ORCL UN | Strike 70 | KO 85 | KI 60 | CPN ?
USD 12M MU UW + NVDA UW + ARM UW | Strike 60 | KO 88 | KI 60 | CPN ?
USD 12M MU UW + NVDA UW + ARM UW | Strike 70 | KO 88 | KI 60 | CPN ?
USD 12M ARM UW + DELL UN | Strike 60 | KO 85 | KI 60 | CPN ?
```

- Model expectation at UF 1% (0.6 correlation floor, ±1.5 pts; 2.5–4 pts higher if the desk marks correlation nearer 0.8): ARM + DELL 88/60/60: ~11% (~7% at UF 2%); ARM + DELL 88/70/60: ~14% (~11% at UF 2%); ARM + DELL + ORCL 85/60/60: ~10% (~6% at UF 2%); ARM + DELL + ORCL 85/70/60: ~14% (~10% at UF 2%); MU + NVDA + ARM 88/60/60: ~9% (~5% at UF 2%); MU + NVDA + ARM 88/70/60: ~13% (~9% at UF 2%); ARM + DELL 85/60/60: ~6% (~2% at UF 2%).
- The last line passes every hard filter (P(KO@1) 67%, P(loss) 11%); it is there to get the desk's price for a true monthly roll.
- Memory KO, monthly obs, European KI, closing prices. Obs #1 lands 02/11, two days before ARM's estimated 04/11 print: get ARM's date confirmed before fixing.
- Re-check the 20-day-MA strong-day test on the fixing morning.

## 8. Release drafts: pre-filled, waiting on the quote

```
🇺🇸 *Private Tranche ACEL*

*ARM UW + DELL UN*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 88%
Strike: 60%
KI: 60%

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $269.58
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Dell Technologies C (DELL UN)
Current Price: $536.02
52-Week High: $595.51
Indicative KO Price: $471.70
Indicative Strike Price: $321.61
Indicative KI Price: $321.61

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 02 Oct 2026.
```

```
🇺🇸 *Private Tranche ACEL*

*ARM UW + DELL UN + ORCL UN*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 85%
Strike: 60%
KI: 60%

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $260.39
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Dell Technologies C (DELL UN)
Current Price: $536.02
52-Week High: $595.51
Indicative KO Price: $455.62
Indicative Strike Price: $321.61
Indicative KI Price: $321.61

Oracle Corp (ORCL UN)
Current Price: $139.54
52-Week High: $320.53
Indicative KO Price: $118.61
Indicative Strike Price: $83.72
Indicative KI Price: $83.72

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 02 Oct 2026.
```

```
🇺🇸 *Private Tranche ACEL*

*MU UW + NVDA UW + ARM UW*

Tenure: 12 months
Currency: USD
Memory KO
Coupon: [desk quote]% p.a.
KO: 88%
Strike: 60%
KI: 60%

Micron Technology Inc (MU UW)
Current Price: $1,080.53
52-Week High: $1,255.00
Indicative KO Price: $950.87
Indicative Strike Price: $648.32
Indicative KI Price: $648.32

NVIDIA Corp (NVDA UW)
Current Price: $224.58
52-Week High: $236.27
Indicative KO Price: $197.63
Indicative Strike Price: $134.75
Indicative KI Price: $134.75

Arm Holdings ADR (ARM UW)
Current Price: $306.34
52-Week High: $452.70
Indicative KO Price: $269.58
Indicative Strike Price: $183.80
Indicative KI Price: $183.80

Indicative prices as of 24 Sep 2026. Official KO, Strike and KI levels to be fixed based on the closing prices on the trade date, 02 Oct 2026.
```

Do not send until the desk's coupon is approved.

## Method and assumptions

- Spot = 24/09 close; 52W high = max(live, IBKR 52W high); 13W low from IBKR. Correlations from 1Y daily log returns (SKHY since its July listing). Risk-neutral drift, r = 3.5%, LO dividend yields.
- Vol: 30D ATM IV in month 1, forward vol from ~12M ATM option IV (Sep-2027 expiry, 24/09 mids) in months 2–12, and a +5 vol-pt bump phasing in between 100% and the KI level. MU month 1 uses 53.1%: its 30D IV less the ±8.9% move implied by the 02/10 straddle.
- Coupons: par less an all-in take (issuer spread 3.06% + UF), pricing paths on historical correlations floored at 0.6. Spread and floor fitted to the desk's 28/09/2026 quotes. P(KO), E[life] and P(loss) run on historical correlations with the same seed.
- Loss at maturity if no KO and worst-of < KI: 1 − WO/Strike. KO modes: memory per stock (ranked) and simultaneous (shown after the slash).
- Roll Score = 0.45·P(KO@1) + 0.25·P(KO≤3) + 0.20·(1 − P(loss)/0.12) + 0.10·min(CPN/IV ÷ 0.30, 1) − 0.03 per penalty, with CPN at UF 1% and IV = basket average 30D IV.
- Earnings dates: MU 30/09 and AMD 03/11 confirmed; the rest are vendor estimates. ANET is estimated for 02/11, obs #1 itself, and treated as a fail until confirmed.
- All probabilities are risk-neutral. With a positive equity risk premium, P(KO) would be modestly higher and P(loss) modestly lower. The ranking would barely move.

