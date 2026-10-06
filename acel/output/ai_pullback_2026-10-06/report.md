# AI pull-back screen: ACEL counters off their highs, for a 15% coupon

Fixing **08/10/2026**, obs #1 **09/11/2026**. Market data: IBKR, 06/10/2026 pre-market snapshot (spot, 30D ATM IV, HV30, 52-week and 13-week ranges), daily closes to 05/10/2026, Sep-2027 ATM option mids for the 12M vol of the priced names. Coupons use the desk calibration of 28/09/2026 (issuer spread 3.06% + UF, pricing correlations floored at 0.6). 63 baskets of 1–3 names from 7 counters, 4,986 structures at 50,000 paths. Finalists and desk lines re-run at 200,000 paths. Coupons are model estimates for quote requests, not quotes. Desk terms means UF 4%, the basis of the 28/09 quotes.

## Bottom line

- **Top 5 counters: ORCL, ARM, AMAT, AVGO, BIDU.** ORCL (−55%) is the anchor: the deepest correction on the list, 52% IV, and no print until ~14/12/2026. ARM (−33%, 72% IV) funds the coupon. AMAT is ARM's most correlated partner (ρ 0.53), but it is only 26% off its high and 15% above its 20-day average, so fixing now locks in a high strike. AVGO (−26%, LO Buy) adds KO odds at the lowest vol of the seven priced. BIDU (−47%) edges BABA (−41%, LO Buy) on correlation to the US names. ADBE is 34% off its high, but it has traded against the semis (ρ −0.36 to AMAT), which works against you in a worst-of.
- **A 15% coupon at desk terms needs ARM in the basket.** 7 AI names on the lists are ≥30% off their 52-week highs: ORCL (−55%), BIDU (−47%), WDC (−45%), BABA (−41%), ADBE (−34%), IBM (−33%), ARM (−33%). WDC, IBM, ARM print before obs #1, which leaves ORCL, BIDU, BABA, ADBE. These four were priced with ARM, AMAT and AVGO (both −26%). ARM (30D IV 72%) is what funds 15% at UF 4%: all 9 baskets that get there contain it. Without ARM the ceiling at desk terms is **12.6%**, at KO 100.
- **Best at desk terms: ORCL + ARM + AMAT, KO 95 / Strike 75 / KI 65, ~15.2%.** P(KO@1) 32.3%, P(KO by obs #3) 51%, P(KO ever) 68%. P(loss) 28.1%, with an average loss of 50% when it happens. This is a 12-month coupon trade, not a monthly roll. It misses the P(KO@1) and P(loss) filters, and ARM reports on 04/11/2026, five days before obs #1.
- **Lower UF buys KO odds.** At UF 2% the same basket pays 15.9% at KO 90, with P(KO@1) 46.7%. At UF 1% it pays 16.8% at KO 88, with P(KO@1) 53.0%. On these notes (expected life 4.5–6.7 months), each 1% of UF is worth 1.9–2.9 pts of coupon.
- **ARM's print adds little coupon, so a post-print fixing is a real option.** Its weeklies price a ±11% move on 04/11/2026. Taking that out of month 1 costs only 0.4–1.1 pts of coupon across the six desk lines (line 1: 14.5% instead of 15.2%), because the coupon comes from ARM's 68% vol over the whole year. A fixing around 06/11/2026 (obs #1 07/12/2026) has ARM, ORCL and AVGO all clear of prints; AMAT, BIDU and BABA are not (they report 12/11–24/11). At today's levels, ORCL + ARM + AVGO 100/75/65 would price ~15.9% at desk terms then, but the coupon re-sets off wherever ARM trades after the print.
- **Memory: your instinct holds on the numbers.** MU (−16%), SKHY (−5%) and SNDK (−28%) are not 30% off their highs. SKHY, SNDK and WDC (−45%) report before obs #1.
- **Nothing at ≥15% passes every hard filter.** A true monthly roll on these names (P(KO@1) ≥ 55%, P(loss) ≤ 12%, no print before obs #1) pays at most 6.8% at UF 1% (ORCL 95/80/70).

## 1. IV screen: every AI name on the lists

Sorted by distance from the 52-week high. 30D IV is IBKR's ATM implied vol. For the 7 priced names, 12M IV is from Sep-2027 ATM mids of 06/10/2026. Other names use the 24/09/2026 marks, and '—' means no long-dated quote was pulled. IV pct is where today's 30D IV sits in its 1-year range. Obs #1 is 09/11/2026.

| Counter | Theme | LO | Off 52W high | 30D IV | 12M IV | HV30 | IV pct | Next print | Before obs #1 | Screen |
|---|---|---|---|---|---|---|---|---|---|---|
| ORCL | AI cloud | H | −55% | 52% | 56% | 60% | 32% | 14/12/2026 est. | no | **priced** |
| BIDU | China AI | H | −47% | 37% | 43% | 36% | 5% | 18/11/2026 est. | no | **priced** |
| WDC | Storage | n/r | −45% | 61% | — | 70% | 3% | 29/10/2026 est. | yes | ≥30% off, prints first |
| BABA | China AI cloud | B | −41% | 38% | 44% | 30% | 18% | 24/11/2026 est. | no | **priced** |
| ADBE | AI software | H | −34% | 38% | 45% | 42% | 29% | 09/12/2026 est. | no | **priced** |
| IBM | AI software | H | −33% | 43% | — | 33% | 77% | 20/10/2026 est. | yes | ≥30% off, prints first |
| ARM | AI semis | H | −33% | 72% | 68% | 73% | 69% | 04/11/2026 confirmed | yes | **priced** |
| NOW | AI software | SB | −28% | 59% | — | 52% | 75% | 28/10/2026 est. | yes | 25–30% off, prints first |
| SNDK | Memory | n/r | −28% | 62% | 73% | 65% | 0% | 30/10/2026 est. | yes | 25–30% off, prints first |
| AMAT | AI semi equipment | H | −26% | 51% | 56% | 47% | 38% | 12/11/2026 est. | no | **priced** |
| AVGO | AI semis | B | −26% | 36% | 44% | 34% | 6% | 09/12/2026 company | no | **priced** |
| STX | Storage | H | −24% | 68% | — | 78% | 31% | 27/10/2026 est. | yes | <25% off |
| SAP | AI software | B | −24% | 45% | — | 34% | 76% | 21/10/2026 est. | yes | <25% off |
| TSLA | Autonomy / robotics | H | −24% | 43% | — | 38% | 34% | 21/10/2026 est. | yes | outside AI theme |
| INTC | AI semis | H | −19% | 66% | — | 63% | 49% | 22/10/2026 est. | yes | <25% off |
| MRVL | AI semis | n/r | −18% | 61% | 68% | 66% | 34% | 01/12/2026 est. | no | <25% off |
| MU | Memory | H | −16% | 45% | 62% | 51% | 0% | 30/09/2026 (reported) | no | <25% off |
| GOOGL | Hyperscaler | B | −15% | 39% | 36% | 27% | 86% | 27/10/2026 est. | yes | <25% off |
| CRM | AI software | B | −14% | 38% | 45% | 57% | 23% | 02/12/2026 est. | no | <25% off |
| AMZN | Hyperscaler | SB | −12% | 43% | 36% | 25% | 91% | 29/10/2026 est. | yes | <25% off |
| PLTR | AI software | H | −8% | 53% | 58% | 42% | 59% | 09/11/2026 confirmed | yes | <25% off |
| DELL | AI hardware | B | −7% | 55% | 68% | 67% | 37% | 24/11/2026 est. | no | <25% off |
| ASML | AI semi equipment | B | −6% | 44% | — | 38% | 34% | 14/10/2026 est. | yes | <25% off |
| DDOG | AI software | H | −5% | 67% | 63% | 55% | 77% | 05/11/2026 est. | yes | <25% off |
| SKHY | Memory | H | −5% | 55% | 63% | 57% | 0% | 27/10/2026 est. | yes | <25% off |
| META | Hyperscaler | B | −4% | 45% | — | 43% | 86% | 28/10/2026 est. | yes | <25% off |
| MSFT | Hyperscaler | SB | −4% | 35% | — | 26% | 82% | 27/10/2026 est. | yes | <25% off |
| AAPL | Devices | B | −4% | 26% | — | 23% | 56% | 29/10/2026 est. | yes | outside AI theme |
| ANET | AI networking | H | −2% | 50% | — | 41% | 35% | 02/11/2026 est. | yes | <25% off |
| AMD | AI semis | H | −2% | 48% | 58% | 49% | 7% | 03/11/2026 confirmed | yes | <25% off |
| TSM | AI semis | SB | −1% | 32% | — | 28% | 6% | 15/10/2026 est. | yes | <25% off |
| NVDA | AI semis | SB | 0% | 29% | 39% | 36% | 0% | 18/11/2026 est. | no | <25% off |
| PANW | Security software | H | 0% | 48% | 57% | 57% | 59% | 12/11/2026 est. | no | outside AI theme |

- **Where the vol is:** ARM 72%, STX 68%, DDOG 67%, INTC 66%, SNDK 62%, WDC 61%, MRVL 61%, NOW 59%. All but MRVL report before obs #1, and only ARM and WDC are ≥30% off their highs. The highest-vol ≥30% name with a clean obs #1 is ORCL at 52%.
- **The other clean ≥30% names sit at 37%–38% IV** (ADBE 38%, BABA 38%, BIDU 37%). That is well short of what 15% needs at KO 95 with the strike above KI. BIDU's and AVGO's IV is near the bottom of their 1-year ranges (5% and 6% percentile): cheap vol, so they add little coupon.
- **ARM's 30D IV (72%) includes the 04/11/2026 print.** Without it, ARM's vol is ~64% (section 5). NOW (−28%, LO Strong Buy, 59% IV) and IBM (−33%) also price prints that land before obs #1.

## 2. Top 5 counters

Ranked on the best P(KO @ obs #1) each name reaches inside a basket that pays at least 15%. The basket can differ by UF, and the best basket at desk terms is the same for the top three.

| # | Counter | Off 52W high | 30D / 12M IV | Next print | Best P(KO@1), CPN ≥15%: UF 4% · 2% · 1% | Best basket at desk terms | LO |
|---|---|---|---|---|---|---|---|
| 1 | ORCL | −55% | 52% / 56% | 14/12/2026 est. | 32% · 47% · 54% | ORCL + ARM + AMAT | H (+1% to PT) |
| 2 | ARM | −33% | 72% / 68% | 04/11/2026 confirmed | 32% · 47% · 56% | ORCL + ARM + AMAT | H (−17% to PT) |
| 3 | AMAT | −26% | 51% / 56% | 12/11/2026 est. | 32% · 47% · 56% | ORCL + ARM + AMAT | H (−5% to PT) |
| 4 | AVGO | −26% | 36% / 44% | 09/12/2026 company | 24% · 44% · 53% | ARM + AMAT + AVGO | B (+37% to PT) |
| 5 | BIDU | −47% | 37% / 43% | 18/11/2026 est. | 20% · 42% · 50% | BIDU + ARM + AMAT | H (+20% to PT) |
|  | *BABA* | −41% | 38% / 44% | 24/11/2026 est. | 19% · 42% · 49% | BABA + ARM + AMAT | B (+95% to PT) |
|  | *ADBE* | −34% | 38% / 45% | 09/12/2026 est. | 15% · 38% · 45% | ORCL + ADBE + ARM | H (−2% to PT) |

1. **ORCL**: 55% off its high, the deepest correction on the list. 52% / 56% IV, and the 13-week low allows a KI up to 72%. Next print ~14/12/2026, well after obs #1. It is in the best basket at UF 4% and 2%, and in the second-best at UF 1%. LO Hold, at its PT.
2. **ARM**: 33% off its high, with the highest IV on the list (72% / 68%). It funds the coupon: every basket that reaches 15% at desk terms contains it. It fails your earnings rule: confirmed print 04/11/2026 after the close, five days before obs #1, priced at ±11%. The print is worth only 0.4–1.1 pts of coupon, so a post-print fixing loses little (section 5). The 13-week low (219.39) caps KI at 65. LO Hold, and 21% above its 250 PT.
3. **AMAT**: 26% off its high, short of your 30% line. 51% / 56% IV, and the best correlation on the list to ARM (0.53) and AVGO (0.54). It prints ~12/11/2026, three days after obs #1. Strong-day flag: 15% above its 20-day average after a rally from 474 on 24/09/2026, so fixing now locks in a high strike. LO Hold, above its 520 PT.
4. **AVGO**: 26% off its high, also short of 30%. The lowest IV of the group (36% / 44%) but the best house view (LO Buy, +37% to the 500 PT), and it moves with ARM and AMAT (ρ 0.51 / 0.54). It buys KO odds and costs coupon. Next print 09/12/2026 (company plan).
5. **BIDU**: 47% off its high, 37% / 43% IV, sitting 4% above its 13-week low. Correlation to ORCL/ARM/AMAT is 0.28/0.34/0.30, against BABA's 0.20/0.28/0.18, which is why it edges BABA on KO odds. **BABA** (−41%, LO Buy) is the swap if you want the house view behind the fifth name, since the numbers are within 1–2 pts. BIDU's 12M vol comes off a wide market.

**On a strict 30% line**, AMAT and AVGO drop out and BABA and ADBE come in. ADBE is the wrong partner. Over the past year it traded as the 'AI loser' side of the trade (ρ −0.36 to AMAT, −0.10 to ARM), so in a worst-of it works as a hedge against the semis, which is the opposite of what an ACEL needs. Its best P(KO@1) at ≥15% is the lowest of the seven.

1-year correlations of daily returns, priced names:

|  | ORCL | BIDU | BABA | ADBE | ARM | AMAT | AVGO |
|---|---|---|---|---|---|---|---|
| ORCL | 1.00 | 0.28 | 0.20 | 0.20 | 0.42 | 0.28 | 0.44 |
| BIDU | 0.28 | 1.00 | 0.59 | 0.01 | 0.34 | 0.30 | 0.35 |
| BABA | 0.20 | 0.59 | 1.00 | 0.00 | 0.28 | 0.18 | 0.28 |
| ADBE | 0.20 | 0.01 | 0.00 | 1.00 | −0.10 | −0.36 | −0.09 |
| ARM | 0.42 | 0.34 | 0.28 | −0.10 | 1.00 | 0.53 | 0.51 |
| AMAT | 0.28 | 0.30 | 0.18 | −0.36 | 0.53 | 1.00 | 0.54 |
| AVGO | 0.44 | 0.35 | 0.28 | −0.09 | 0.51 | 0.54 | 1.00 |

## 3. Baskets that clear 15%

For each basket, the structure with the highest P(KO @ obs #1) that pays at least 15%. KO grid 85–100, KI 50–70 (capped at 90% of every name's 13-week low), strike at KI, KI+5 or KI+10. Probabilities on historical correlations, memory KO. *Misses* are the master prompt's hard filters.

### At desk terms (UF 4%): 9 baskets, all with ARM

| # | Basket | KO/Str/KI | CPN | P(KO@1) | P(KO≤3) | P(KO ever) | E[life] m | P(loss) | E[loss\|loss] | avg ρ | Misses | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ORCL + ARM + AMAT | 95/75/65 | 15.2% | 32.3% | 51% | 68% | 5.7 | 28.1% | 50% | 0.41 | print, P(KO@1), P(loss) | AMAT −26% off high; KO > 91.6 rule; KI > 64.5 rule; strong day (AMAT); avg ρ < 0.5 |
| 2 | ARM + AMAT + AVGO | 100/75/65 | 16.1% | 23.7% | 43% | 62% | 6.5 | 31.0% | 47% | 0.53 | print, P(KO@1), P(loss) | AMAT −26%, AVGO −26% off high; KO > 92.4 rule; strong day (AMAT) |
| 3 | ORCL + ARM + AVGO | 100/75/65 | 16.4% | 21.8% | 41% | 60% | 6.7 | 32.8% | 47% | 0.46 | print, P(KO@1), P(loss) | AVGO −26% off high; KO > 92.3 rule; avg ρ < 0.5 |
| 4 | BIDU + ARM + AMAT | 100/75/65 | 16.0% | 20.3% | 39% | 60% | 6.9 | 33.0% | 47% | 0.39 | print, P(KO@1), P(loss) | AMAT −26% off high; KO > 92.3 rule; strong day (AMAT); avg ρ < 0.5 |
| 5 | ORCL + BIDU + ARM | 100/75/65 | 16.2% | 19.0% | 38% | 59% | 7.0 | 34.3% | 47% | 0.35 | print, P(KO@1), P(loss) | KO > 92.2 rule; avg ρ < 0.5 |
| 6 | BABA + ARM + AMAT | 100/75/65 | 16.3% | 18.7% | 38% | 58% | 7.0 | 34.3% | 47% | 0.33 | print, P(KO@1), P(loss) | AMAT −26% off high; KO > 92.2 rule; strong day (AMAT); avg ρ < 0.5 |
| 7 | ORCL + BABA + ARM | 100/75/65 | 16.5% | 17.8% | 36% | 57% | 7.2 | 35.5% | 47% | 0.30 | print, P(KO@1), P(loss) | KO > 92.2 rule; avg ρ < 0.5 |
| 8 | ORCL + ADBE + ARM | 100/75/65 | 16.4% | 14.9% | 34% | 56% | 7.4 | 36.7% | 47% | 0.17 | print, P(KO@1), P(loss) | KO > 92.2 rule; avg ρ < 0.5 |
| 9 | ADBE + ARM + AMAT | 100/75/65 | 16.2% | 11.7% | 31% | 55% | 7.6 | 36.9% | 46% | 0.02 | print, P(KO@1), P(loss) | AMAT −26% off high; KO > 92.2 rule; strong day (AMAT); avg ρ < 0.5 |

### With a lower UF

UF 2%:

| # | Basket | KO/Str/KI | CPN | P(KO@1) | P(KO≤3) | P(KO ever) | E[life] m | P(loss) | E[loss\|loss] | avg ρ | Misses | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ORCL + ARM + AMAT | 90/75/65 | 15.9% | 46.7% | 64% | 77% | 4.5 | 20.8% | 51% | 0.41 | print, P(KO@1), P(loss) | AMAT −26% off high; KI > 64.5 rule; strong day (AMAT); avg ρ < 0.5 |
| 2 | ORCL + ARM + AVGO | 92/75/65 | 15.4% | 44.4% | 62% | 76% | 4.6 | 21.2% | 50% | 0.46 | print, P(KO@1), P(loss) | AVGO −26% off high; avg ρ < 0.5 |
| 3 | ARM + AMAT | 95/75/65 | 15.9% | 43.2% | 61% | 76% | 4.7 | 21.0% | 50% | 0.53 | print, P(KO@1), P(loss) | AMAT −26% off high; KO > 91.1 rule; KI > 63.0 rule; strong day (AMAT) |
| 4 | BABA + ARM + AMAT | 92/75/65 | 15.5% | 42.1% | 60% | 75% | 4.8 | 22.0% | 49% | 0.33 | print, P(KO@1), P(loss) | AMAT −26% off high; strong day (AMAT); avg ρ < 0.5 |
| 5 | ORCL + BIDU + ARM | 92/75/65 | 15.5% | 41.8% | 60% | 75% | 4.8 | 22.2% | 49% | 0.35 | print, P(KO@1), P(loss) | avg ρ < 0.5 |
| 6 | ORCL + ARM | 95/75/65 | 16.2% | 40.9% | 59% | 74% | 4.9 | 22.2% | 50% | 0.42 | print, P(KO@1), P(loss) | KO > 91.0 rule; KI > 62.7 rule |
| 7 | ORCL + BABA + ARM | 92/75/65 | 15.8% | 40.6% | 59% | 74% | 4.9 | 22.8% | 49% | 0.30 | print, P(KO@1), P(loss) | avg ρ < 0.5 |
| 8 | ORCL + ADBE + ARM | 92/75/65 | 15.7% | 38.0% | 58% | 74% | 5.1 | 23.5% | 49% | 0.17 | print, P(KO@1), P(loss) | avg ρ < 0.5 |

UF 1%:

| # | Basket | KO/Str/KI | CPN | P(KO@1) | P(KO≤3) | P(KO ever) | E[life] m | P(loss) | E[loss\|loss] | avg ρ | Misses | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | ARM + AMAT | 90/75/65 | 14.7% | 56.3% | 71% | 83% | 3.7 | 15.5% | 51% | 0.53 | print, P(loss) | AMAT −26% off high; KI > 63.0 rule; strong day (AMAT) |
| 2 | ORCL + ARM | 90/75/65 | 15.1% | 54.3% | 70% | 82% | 3.9 | 16.5% | 51% | 0.42 | print, P(KO@1), P(loss) | KI > 62.7 rule |
| 3 | ORCL + ARM + AMAT | 88/75/65 | 16.8% | 53.0% | 69% | 81% | 4.0 | 17.9% | 52% | 0.41 | print, P(KO@1), P(loss) | AMAT −26% off high; KI > 64.5 rule; strong day (AMAT); avg ρ < 0.5 |
| 4 | ARM + AMAT + AVGO | 90/75/65 | 16.2% | 52.8% | 69% | 81% | 4.0 | 17.4% | 50% | 0.53 | print, P(KO@1), P(loss) | AMAT −26%, AVGO −26% off high; strong day (AMAT) |
| 5 | ORCL + ARM + AVGO | 90/75/65 | 16.5% | 50.8% | 67% | 80% | 4.1 | 18.3% | 50% | 0.46 | print, P(KO@1), P(loss) | AVGO −26% off high; avg ρ < 0.5 |
| 6 | BIDU + ARM + AMAT | 90/75/65 | 16.2% | 50.2% | 67% | 80% | 4.2 | 18.3% | 50% | 0.39 | print, P(KO@1), P(loss) | AMAT −26% off high; strong day (AMAT); avg ρ < 0.5 |
| 7 | BABA + ARM + AMAT | 90/75/65 | 16.5% | 49.0% | 66% | 79% | 4.3 | 18.9% | 50% | 0.33 | print, P(KO@1), P(loss) | AMAT −26% off high; strong day (AMAT); avg ρ < 0.5 |
| 8 | ORCL + BIDU + ARM | 90/75/65 | 16.6% | 48.5% | 65% | 79% | 4.3 | 19.2% | 50% | 0.35 | print, P(KO@1), P(loss) | avg ρ < 0.5 |

Re-run on fresh paths, a few UF 1% lines land just under 15% (e.g. ARM + AMAT 90/75/65 at 14.7%). Treat them as ~15%.

### Without ARM (no print before obs #1)

The best coupons at desk terms, and the best KO odds at ≥15% with a lower UF:

| Basket | KO/Str/KI | CPN UF 4% | CPN UF 2% | CPN UF 1% | P(KO@1) | P(KO≤3) | P(KO ever) | P(loss) | E[loss\|loss] | avg ρ | Flags |
|---|---|---|---|---|---|---|---|---|---|---|---|
| ORCL + BABA + ADBE | 100/80/70 | 12.6% | 16.6% | 18.6% | 14.4% | 34% | 58% | 35.7% | 42% | 0.13 | KO > 93.8 rule; avg ρ < 0.5 |
| ORCL + BABA + AMAT | 100/75/65 | 12.6% | 16.5% | 18.5% | 16.2% | 35% | 58% | 34.3% | 43% | 0.22 | AMAT −26% off high; KO > 93.2 rule; strong day (AMAT); avg ρ < 0.5 |
| ORCL + ADBE + AMAT | 100/75/65 | 12.5% | 16.4% | 18.4% | 11.9% | 32% | 56% | 35.5% | 43% | 0.04 | AMAT −26% off high; KO > 93.2 rule; strong day (AMAT); avg ρ < 0.5 |
| ORCL + AMAT + AVGO | 100/75/65 | 12.4% | 16.4% | 18.3% | 21.2% | 41% | 62% | 30.8% | 44% | 0.42 | AMAT −26%, AVGO −26% off high; KO > 93.3 rule; strong day (AMAT); avg ρ < 0.5 |
| ORCL + BIDU + BABA | 100/80/70 | 12.3% | 16.3% | 18.3% | 19.8% | 40% | 61% | 32.2% | 43% | 0.35 | KO > 93.9 rule; avg ρ < 0.5 |
| ORCL + BIDU + AVGO | 100/80/70 | 12.0% | 16.0% | 18.0% | 19.9% | 40% | 62% | 31.7% | 42% | 0.36 | AVGO −26% off high; KO > 94.0 rule; avg ρ < 0.5 |
| ORCL + AMAT + AVGO | 95/75/65 | 8.3% | 13.3% | 15.8% | 36.3% | 56% | 73% | 23.0% | 45% | 0.42 | AMAT −26%, AVGO −26% off high; KO > 93.3 rule; strong day (AMAT); avg ρ < 0.5 |
| ORCL + BABA + AVGO | 95/80/70 | 7.6% | 12.8% | 15.4% | 35.7% | 56% | 73% | 23.5% | 44% | 0.31 | AVGO −26% off high; KO > 93.9 rule; avg ρ < 0.5 |
| ORCL + BIDU + BABA | 95/80/70 | 7.5% | 12.8% | 15.4% | 36.5% | 56% | 73% | 23.2% | 44% | 0.35 | KO > 93.9 rule; avg ρ < 0.5 |

Without ARM, 15% needs UF 2% or less and KO 95–100, and P(KO@1) tops out around 36%. The ARM baskets above do better on every count except the print.

## 4. Top 3 verdicts

1. **ORCL + ARM + AMAT 95/75/65 at desk terms, ~15.2%.** P(KO@1) 32.3%, P(KO≤3) 51%, P(loss) 28.1%. **Rolls:** ORCL has already de-rated 55% and does not report until mid-December. AMAT is ARM's most correlated partner (0.53), which keeps the worst-of closer to a single stock. **Breaks:** ARM's 04/11/2026 print (±11%) lands five days before obs #1. AMAT is being fixed after a 15% run above its 20-day average. With the strike at 75 above the KI of 65, a breach costs at least 13%. Without the strike lever (95/65/65) the coupon is 10.9%.
2. **ORCL + ARM + AMAT 90/75/65 at UF 2%, ~15.9%.** The best KO odds at 15%: P(KO@1) 46.7%, P(KO≤3) 64%, P(KO ever) 77%, P(loss) 20.8%. **Rolls:** KO 90 sits 0.6 monthly σ below spot instead of 0.3 at KO 95. **Needs:** UF at 2% instead of 4%. At desk terms the same line prices ~10.0%. The breaks are the same as line 1.
3. **ARM + AMAT 95/75/65 at UF 2%, ~15.9%** (your pair). P(KO@1) 43.2%, P(loss) 21.0%. **Rolls:** two names, so one fewer way to miss, and the two move together (ρ 0.53). **Breaks:** both legs are AI semis: if the trade unwinds, nothing in the basket diversifies it. At desk terms the pair reaches 14.0% only at KO 100 (P(KO@1) 31.1%).

If ARM's print before obs #1 is a deal-breaker, wait for it rather than drop ARM. The clean-calendar basket available now (ORCL + AMAT + AVGO) prices ~12.4% at desk terms at KO 100, with P(KO@1) 21.2%. ORCL + ARM + AVGO after the print (section 5) gives up only ~0.4 pts against today's line 3.

## 5. ARM's print: what it adds, and the window after it

ARM's weekly options: the 30/10 expiry (before the print) trades at 63.9% IV and the 06/11 expiry (after it) at 74.3%. The difference prices a one-day move of ±11.2% on 04/11/2026. The table re-runs each ARM line with month-1 vol at 64%, the ex-print level, at today's spot and with everything else unchanged.

| Line | Basket | KO/Str/KI | UF | CPN now | CPN ex-print | P(KO@1) now | P(KO@1) ex-print | P(loss) now | P(loss) ex-print |
|---|---|---|---|---|---|---|---|---|---|
| 1 | ORCL + ARM + AMAT | 95/75/65 | 4% | 15.2% | 14.5% | 32.3% | 32.9% | 28.1% | 27.3% |
| 2 | ARM + AMAT | 100/75/65 | 4% | 14.0% | 13.4% | 31.1% | 31.4% | 26.3% | 25.5% |
| 3 | ORCL + ARM + AVGO | 100/75/65 | 4% | 16.4% | 15.9% | 21.8% | 22.0% | 32.8% | 32.1% |
| 4 | ORCL + ARM + AMAT | 90/75/65 | 2% | 15.9% | 14.7% | 46.7% | 48.1% | 20.8% | 19.7% |
| 5 | ARM + AMAT | 95/75/65 | 2% | 15.9% | 14.9% | 43.2% | 44.2% | 21.0% | 20.0% |
| 6 | ORCL + ARM + AVGO | 92/75/65 | 2% | 15.4% | 14.4% | 44.4% | 45.7% | 21.2% | 20.0% |

- Taking the print out of month 1 costs 0.4–1.1 pts of coupon and raises P(KO@1) by only 0.2–1.4 pts. Month-1 vol mostly drives obs #1. The coupon depends on vol over the note's expected 4–7-month life, which is ARM's 68% 12-month vol, and the print barely moves that.
- In the model the print is just extra month-1 variance. In practice it is a gap: obs #1 becomes a bet on the print's direction, which is what your earnings rule guards against. The numbers say keeping the rule costs little.
- **Calendar.** ARM (04/11/2026) and AMAT (~12/11/2026) report eight days apart, so any fixing between now and mid-November carries one of them into obs #1. The first clean ARM window is a fixing around 06/11/2026 (obs #1 07/12/2026). ORCL, ADBE, ARM, AVGO are clear then, while BIDU, BABA, AMAT report before that obs #1. So the post-print trade is ORCL + ARM + AVGO: lines 3 and 6 re-struck after the print, at roughly the ex-print coupons above, from wherever the stocks are then.

## 6. Desk request lines (Florence)

```
Assuming TD 8/10 - UF 4%
USD 12M ORCL UN + ARM UW + AMAT UW | Strike 75 | KO 95 | KI 65 | CPN ?
USD 12M ARM UW + AMAT UW | Strike 75 | KO 100 | KI 65 | CPN ?
USD 12M ORCL UN + ARM UW + AVGO UW | Strike 75 | KO 100 | KI 65 | CPN ?
```

- Model expectation at UF 4% (±1.5 pts): ORCL + ARM + AMAT 95/75/65: ~15% (P(KO@1) 32%, P(loss) 28%); ARM + AMAT 100/75/65: ~14% (P(KO@1) 31%, P(loss) 26%); ORCL + ARM + AVGO 100/75/65: ~16% (P(KO@1) 22%, P(loss) 33%).

```
Assuming TD 8/10 - UF 2%
USD 12M ORCL UN + ARM UW + AMAT UW | Strike 75 | KO 90 | KI 65 | CPN ?
USD 12M ARM UW + AMAT UW | Strike 75 | KO 95 | KI 65 | CPN ?
USD 12M ORCL UN + ARM UW + AVGO UW | Strike 75 | KO 92 | KI 65 | CPN ?
```

- Model expectation at UF 2% (±1.5 pts): ORCL + ARM + AMAT 90/75/65: ~16% (P(KO@1) 47%, P(loss) 21%); ARM + AMAT 95/75/65: ~16% (P(KO@1) 43%, P(loss) 21%); ORCL + ARM + AVGO 92/75/65: ~15% (P(KO@1) 44%, P(loss) 21%).

- ARM reports 04/11/2026 after the close (confirmed), five days before obs #1 on 09/11/2026. Every line fails the earnings rule on ARM, and none passes P(KO@1) ≥ 55% or P(loss) ≤ 12%. To keep the rule, re-request lines 3 and 6 for a fixing after the print (around 06/11/2026).
- AMAT reports ~12/11/2026 (estimate), three days after obs #1. Strong-day fix on AMAT: re-check the 20-day-MA test on the fixing morning.
- KO 95–100 sits above the KO ≤ 100 − 0.5·σ₁ₘ rule of thumb on the UF 4% lines. KI 65 is 1–2 pts above the e^(−0.75σ) rule on the ARM + AMAT lines. KI 65 is the most the 13-week-low rule allows with ARM in the basket.
- Memory KO, monthly obs, European KI, closing prices.
- No release drafts: releases follow approved quotes only.

## 7. Earnings calendar

| Counter | Next print | Detail | Before obs #1 (09/11/2026) | Source |
|---|---|---|---|---|
| IBM | 20/10/2026 est. | est | yes | vendor estimate |
| NOW | 28/10/2026 est. | est | yes | [link](https://www.tipranks.com/stocks/now/earnings) |
| WDC | 29/10/2026 est. | est | yes | vendor estimate |
| SNDK | 30/10/2026 est. | est window 30/10-09/11 | yes | vendor estimate |
| ARM | 04/11/2026 confirmed | confirmed amc (company release) | yes | [link](https://newsroom.arm.com/news/arm-announces-earnings-release-date-for-second-quarter-fiscal-year-ending-2027) |
| AMAT | 12/11/2026 est. | est (quarter ends 25/10) | no | [link](https://www.tipranks.com/stocks/amat/earnings) |
| BIDU | 18/11/2026 est. | est 17-24/11 | no | [link](https://www.tipranks.com/stocks/bidu/earnings) |
| BABA | 24/11/2026 est. | est, unconfirmed (24/11-01/12) | no | [link](https://www.tipranks.com/stocks/baba/earnings) |
| ADBE | 09/12/2026 est. | est | no | [link](https://www.tipranks.com/stocks/adbe/earnings) |
| AVGO | 09/12/2026 company | company plan, amc | no | [link](https://investors.broadcom.com/news-releases/news-release-details/broadcom-inc-announces-third-quarter-fiscal-year-2026-financial) |
| ORCL | 14/12/2026 est. | est 10-14/12 | no | [link](https://www.tipranks.com/stocks/orcl/earnings) |

## Method and assumptions

- Spot is the 06/10/2026 IBKR snapshot (pre-market, so the prior close for most names). The 52-week high and 13-week low come from IBKR. Correlations use 1-year daily log returns to 05/10/2026. Drift is risk-neutral at r = 3.5%, with LO dividend yields.
- Vol: 30D ATM IV in month 1 (it includes ARM's print), forward vol from the Sep-2027 ATM IV in months 2–12, and a +5 vol-pt skew bump phasing in between 100% and the KI level.
- Coupons: par less an all-in take of issuer spread 3.06% + UF. Pricing paths use historical correlations floored at 0.6. Both are fitted to the desk's 28/09/2026 quotes, ±1.1 pts. Coupon at another UF = coupon + ΔUF / annuity. P(KO), E[life] and P(loss) run on historical correlations with the same seed.
- Loss at maturity if there is no KO and the worst-of ends below KI: 1 − WO/Strike. KO is memory per stock.
- Universe: the 33 tech and AI-related names on the attached LO lists (Comm Services, IT, Consumer Discretionary of 17/09/2026 and IT of 04/08/2026). Priced: AI names ≥25% off their 52-week high with no print before obs #1, plus ARM and AMAT (ORCL, BIDU, BABA, ADBE, ARM, AMAT, AVGO). Every 1–3-name basket was priced.
- Hard rules enforced: KI ≤ 90% of each name's 13-week low. Reported, not enforced: prints before obs #1, the 30% line, and the KO/KI rules of thumb. Enforcing them leaves nothing at 15%.
- None of the baskets shares two names with a ledger trade, so the live-overlap flag does not apply, whichever tranches have knocked out.
- All probabilities are risk-neutral. With a positive equity risk premium, P(KO) would be modestly higher and P(loss) modestly lower.
- ARM ex-print vol: the 305 strike's call/put mids on the 30/10 and 06/11 weeklies at 09:39 UTC 06/10/2026. Move = √((σ₂² − σ₁²)·T₂), with month-1 vol set to σ₁.
