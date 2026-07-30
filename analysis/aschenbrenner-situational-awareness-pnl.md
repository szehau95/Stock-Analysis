# Situational Awareness LP — Net P&L Analysis (Sept 2024 – July 2026)

**Subject:** Leopold Aschenbrenner's Situational Awareness LP
**Question:** What is the net P&L over the past ~2 years, and was the fund still profitable after the July 2026 forced liquidation?
**Analysis date:** 30 July 2026 (mid-session; July not yet closed)
**Short answer:** Yes — decisively profitable on a time-weighted basis. The July collapse was severe but mathematically could not undo the 2025–H1 2026 compounding.

---

## 1. Headline conclusion

| Measure | Result |
|---|---|
| Cumulative net return, launch → 30 Jun 2026 | **≈ +1,517%** (16.2x) |
| Estimated cumulative net return after July 2026 | **≈ +600% to +900%** (7x–10x) |
| July 2026 drawdown needed to erase *all* gains since launch | **−93.8%** |
| Verdict | Still very profitable; but gains are unevenly distributed across investors |

A dollar invested at the September 2024 launch was worth roughly **$16.20** on 30 June 2026 and is worth roughly **$7–$10** today. The fund gave back over half its life-to-date gains in four weeks and still sits on a ~7–10x.

---

## 2. Reconstructed return chain (time-weighted, net of fees)

No audited track record is public. The chain below is built from reported figures and cross-validates internally.

| Period | Net return | Cumulative | Source basis |
|---|---|---|---|
| Sep–Dec 2024 (stub) | ≈ 0% (inferred residual) | 1.00x | back-solved, see check below |
| FY 2025 | **+200%** | 3.00x | reported ~200% for 2025 |
| 2026 through May | +270% YTD | 11.10x | reported "up roughly 270% through the first five months" |
| 2026 through June | **+439%** YTD | **16.17x** | 24 July investor letter (via FT) |
| July 2026 (MTD) | **−47% to −56% (est.)** | **7.2x–8.6x** | AUM-implied, see §4 |

**Internal consistency check.** 2025 (+200%) compounded with 2026-through-May (+270%) gives exactly **11.10x = +1,010%**, which matches the independently reported ">1,000% net of fees since launch." That agreement is only possible if the Sep–Dec 2024 stub period was approximately flat — so the chain hangs together and the 2024 stub is not a hidden source of return.

**June 2026 alone was roughly +46%** (5.39 / 3.70 − 1), i.e. the fund made nearly half its money again in the final month before the top. This matters for §5: capital that arrived in June bought in at the highest NAV in the fund's history.

---

## 3. What actually happened in July — three losing legs at once

This is the analytically interesting part. The fund was not simply "long AI and the market fell." Using the 30 June 13F positions and actual July price action (IBKR daily bars; 1 July open as month-start reference):

| Position | 13F role | 1 Jul | 29 Jul | 30 Jul | MTD @ 29 Jul | MTD @ 30 Jul | Effect on fund |
|---|---|---|---|---|---|---|---|
| Nebius (NBIS) | long | 240.27 | 148.22 | 190.28 | **−38.3%** | −20.8% | loss |
| SanDisk (SNDK) | long | 2085.17 | 1015.89 | 1249.67 | **−51.3%** | −40.1% | loss |
| Micron (MU) | long | 1082.01 | 739.00 | 853.04 | **−31.7%** | −21.2% | loss |
| CoreWeave (CRWV) | long | 88.90 | 60.82 | 74.78 | **−31.6%** | −15.9% | loss |
| SK Hynix | long (not in 13F) | — | — | — | sharp decline | — | loss |
| Adobe (ADBE) | short | 209.43 | 263.43 | 246.83 | **+25.8%** | +17.9% | **loss** |
| Nvidia (NVDA) | put, $1.57bn | 293.49 | 338.19 | 331.63 | **+15.2%** | +13.0% | **loss** |
| VanEck Semis (SMH) | put, $2.04bn | 634.25 | 504.22 | 535.51 | −20.5% | −15.6% | gain |
| Oracle (ORCL) | put, $1.07bn | 144.49 | 117.74 | 124.89 | −18.5% | −13.6% | gain |

The July rout was **not a broad AI selloff — it was a violent rotation inside AI.** Nvidia rose 13% and Adobe rose 18% while memory and neocloud names fell 16–40%. Situational Awareness was positioned on the wrong side of all three axes simultaneously:

1. **Long the crushed cohort** — memory (SanDisk, Micron, SK Hynix) and neoclouds (Nebius, CoreWeave), the names that had run up the most and unwound hardest.
2. **Short the cohort that rallied** — software, with Adobe up ~18–26% against them.
3. **Long puts on names that went up** — the $1.57bn Nvidia put line lost as Nvidia rallied 13%.

The SMH and Oracle put lines did work, which is likely why the damage, though severe, was not total. But the hedges were pointed at large-cap semis and AI-software capex, not at the memory/neocloud complex that actually broke — so the put book hedged the wrong tail.

**Leverage did the rest.** Reported gross leverage was ~4x. A 4x-levered book losing ~12–14% at the position level maps to roughly a 50% NAV loss, which is consistent with the AUM path in §4. Prime brokers (Bank of America, Goldman Sachs, JPMorgan) pressed for margin, and the entire public book — long and short, ~two-thirds of total investments — was sold to Citadel in effectively a single transaction.

**Note on the 30 July bounce.** Every long name rallied 15–28% on 30 July (Nebius +28%, SanDisk +23%, CoreWeave +23%, Micron +15%). Press figures citing "down more than 35% this month" reflect the 29 July trough. If the book was liquidated into the 28–29 July lows, the fund crystallised losses roughly 15–25 percentage points worse than month-end marks would have shown — the liquidation timing itself was expensive.

---

## 4. Sizing the July drawdown

The exact drawdown has **not been disclosed.** The available anchors are AUM figures, and they conflict:

| Anchor | Figure |
|---|---|
| Peak, start of July 2026 | ~$45bn |
| "Valued at" before the rout | ~$24bn |
| Current AUM (post-rout reporting) | ~$20bn |

Taking $45bn as the July starting point:

- $45bn → $24bn = **−46.7%**
- $45bn → $20bn = **−55.6%**

These are AUM moves, not clean NAV returns — they may blend performance with forced deleveraging, redemptions, and possibly gross-vs-net exposure definitions. The $45bn figure in particular may reflect peak gross assets rather than equity NAV. Treat **−47% to −56%** as the best available estimate of the July NAV hit, with real uncertainty around it.

### Sensitivity: cumulative return since launch vs. July outcome

| July 2026 | Cumulative multiple | Cumulative net return | $1 at launch |
|---|---|---|---|
| −10% | 14.55x | +1,355% | $14.55 |
| −20% | 12.94x | +1,194% | $12.94 |
| −30% | 11.32x | +1,032% | $11.32 |
| −40% | 9.70x | +870% | $9.70 |
| **−47%** | **8.62x** | **+762%** | **$8.62** |
| −50% | 8.08x | +708% | $8.08 |
| **−56%** | **7.18x** | **+618%** | **$7.18** |
| −70% | 4.85x | +385% | $4.85 |
| −80% | 3.23x | +223% | $3.23 |
| **−93.8%** | **1.00x** | **0%** | **$1.00** |

**The result is robust.** Even an implausible −80% July leaves the fund up more than 3x since launch. The fund would have had to lose **93.8%** in a single month to give back everything — and it did not come close.

---

## 5. The critical caveat: time-weighted ≠ what investors actually made

The +600–900% figure is the **return of the fund**, not the return of the average dollar in it. These diverge more here than in almost any fund I can think of, and the gap is the real story.

AUM went from **$225m at launch to ~$45bn at the start of July 2026** — a ~200x increase, while performance alone accounts for only ~16x. That arithmetic is unavoidable: **the overwhelming majority of the capital arrived after the overwhelming majority of the compounding had already happened.**

Consequences:

- **Founding investors** (the Collisons, Daniel Gross, Nat Friedman) rode the full 16x and are up enormously even after July.
- **Investors who subscribed in H1 2026** — the period when the fund was scaling hardest and Jane Street came in — bought into a NAV that had already risen 439% YTD, with June alone up ~46%. A −47% to −56% July puts most of that cohort **underwater on their investment**, in some cases badly.
- **Aggregate dollar P&L is still positive**, and comfortably so. For the fund to have lost money in aggregate, cumulative net subscriptions would have to exceed today's ~$20bn NAV; starting from $225m and compounding 16x, that is not plausible. But aggregate profit is far smaller relative to capital deployed than the +618–762% headline suggests.
- **Fee asymmetry.** Performance fees on a +439% first half were earned on gains that have since substantially reversed. Absent a clawback, the manager banked incentive fees on paper profits that late investors never realised, and those investors now sit below a high-water mark.

So the honest framing: **the fund was highly profitable; a large fraction of its investors were not.**

---

## 6. The part nobody is marking: the private book

Post-liquidation the portfolio is **entirely private**, and this is where the answer gets stronger, not weaker.

The retained private book includes an **Anthropic stake reportedly acquired near a $60bn valuation.** Anthropic's May 2026 Series H closed at **$965bn post-money** ($65bn raised; run-rate revenue reported above $47bn).

That is roughly a **16x mark on the Anthropic position alone** — and unlike the public book, it was not sold into the July lows. Private marks lag and are not liquid, so this is not cash in hand, and a sustained AI derating would eventually flow through to private valuations. But as of today the surviving portfolio carries a very large unrealised gain that the public-market carnage did not touch.

This changes the character of the situation: the July event looks less like a fund blowing up and more like a **forced deleveraging of the liquid sleeve to meet margin, leaving the illiquid sleeve — the better-performing one — intact.** Aschenbrenner has invited investors to commit fresh capital from 1 August, framing the drawdown as an entry point.

---

## 7. Bottom line

1. **Was it profitable over the past two years? Yes, emphatically.** Roughly **+600% to +900% net since the September 2024 launch**, even after the July liquidation — down from ~+1,517% at the 30 June peak.
2. **The liquidation was severe but not existential.** An estimated −47% to −56% month. It would have taken −93.8% to erase the track record.
3. **The loss mechanism was concentration plus leverage, not a directional AI call gone wrong.** Long memory/neocloud, short software, and long Nvidia puts all lost simultaneously in a rotation *within* AI. 4x leverage converted a low-double-digit position-level loss into a ~50% NAV loss and triggered the margin-driven sale to Citadel.
4. **Forced selling into the 28–29 July trough was itself costly** — names rebounded 15–28% on 30 July, the day after.
5. **The headline return badly overstates investor experience.** With AUM up ~200x against 16x of performance, most capital missed most of the gains, and the H1 2026 cohort is likely underwater.
6. **The surviving private book is the strongest remaining asset** — an Anthropic stake entered near $60bn against a $965bn May 2026 round.

### Principal uncertainties

- The July drawdown is **estimated from conflicting AUM figures** ($45bn / $24bn / $20bn), not disclosed. It is the single largest unknown, though the conclusion holds across the entire plausible range.
- 13F data shows **notional value only** — it does not distinguish long from short option positions, disclose strikes or expiries, or cover foreign listings (SK Hynix), swaps, or short stock. The put lines are treated here as long puts, consistent with press descriptions of the fund's hedging, but this is an inference.
- The 2025 (+200%) and 2024 (~0%) figures are **press-reported and back-solved**, not audited. One source cited a 2025 return of +2,065%, which is inconsistent with the ">1,000% since launch" figure and is treated as an error.
- Private marks are **not liquidity**. The Anthropic gain is unrealised and reflects a May 2026 round struck before the July rout.

---

## Sources

- [Seeking Alpha — Aschenbrenner's hedge fund unwinds public bets amid AI market rout](https://seekingalpha.com/news/4621752-leopold-aschenbrenners-hedge-fund-unwinds-public-bets-amid-ai-market-rout)
- [CNBC — Aschenbrenner forced to unwind all public stock positions after steep losses](https://www.cnbc.com/2026/07/30/leopold-aschenbrenners-hedge-fund-is-facing-steep-ai-losses.html)
- [Yahoo Finance / CNBC — Situational Awareness sells public equities book](https://finance.yahoo.com/markets/stocks/articles/situational-awareness-sells-public-equities-140824582.html)
- [Bloomberg — Situational Awareness unwinding trades, report says](https://www.bloomberg.com/news/articles/2026-07-30/aschenbrenner-hedge-fund-situational-awareness-seeks-capital-after-loss-ft-says)
- [Hedgeweek — Situational Awareness seeks fresh capital after tech sell-off](https://www.hedgeweek.com/situational-awareness-seeks-fresh-capital-after-tech-sell-off/)
- [Hedgeweek — Situational Awareness soars past $20bn](https://www.hedgeweek.com/situational-awareness-soars-past-20bn/)
- [Disruption Banking — Can Situational Awareness raise capital after its 439% H1 gain?](https://www.disruptionbanking.com/2026/07/30/can-the-situational-awareness-hedge-fund-raise-capital-after-its-439-h1-gain/)
- [Insider Monkey — Situational Awareness LP 13F holdings](https://www.insidermonkey.com/hedge-fund/situational+awareness+lp/1581/)
- [Crypto Briefing — Situational Awareness dumps entire public stock portfolio](https://cryptobriefing.com/situational-awareness-hedge-fund-liquidates-portfolio/)
- [Anthropic — Series H at $965bn post-money](https://www.anthropic.com/news/series-h)
- [CNBC — Anthropic tops OpenAI, nears $1tn valuation](https://www.cnbc.com/2026/05/28/anthropic-open-ai-startup-value.html)
- Price data: Interactive Brokers daily OHLCV bars, 1–30 July 2026
