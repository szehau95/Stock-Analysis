# Bahrain GP (Sepang) — Polymarket "Driver Winner" edge analysis

Race: 04/10/2026, Sepang International Circuit, lights out 15:00 MYT (07:00 UTC), 56 laps (assumed, 2017 distance).
Market snapshot: CLOB/Gamma pulled 04/10/2026 ~13:12 MYT (CLOB timestamp 1791090743279). Prices will have moved since.
Analysis only. No trades placed, no wallet touched.

## Verdict: **PASS**

No position clears **edge ≥ 4 pp after fees using the conservative bound of the 90% interval**, which is the sizing rule you set.
Only one position clears 4 pp on the *point estimate*: Russell YES (+4.7 pp). It fails once the model is blended with two independent market priors (≈ +2.0 pp).

## 1. Verdict table

Cost = ask + taker fee, where the fee is `0.05·p·(1−p)` per share (Polymarket Sports schedule). Quarter-Kelly f = 0.25·(p−c)/(1−c). The "cons." column uses the lower bound of the interval (for a NO position, 1 − the upper bound).

| Position | Ask | All-in cost | My P (90% int.) | Edge | ROI | ¼-Kelly pt | ¼-Kelly cons. |
|---|---|---|---|---|---|---|---|
| VER YES | 0.620 | 0.6318 | 56.2% (29.9–76.8) | −7.0 pp | −11.0% | 0 | 0 |
| **VER NO** | 0.390 | 0.4019 | 43.8% (23.2–70.1) | +3.6 pp | +9.0% | 1.50% | 0 |
| ANT YES | 0.210 | 0.2183 | 16.6% (0.5–51.9) | −5.2 pp | −23.8% | 0 | 0 |
| **ANT NO** | 0.800 | 0.8080 | 83.4% (48.1–99.5) | +2.6 pp | +3.2% | 3.35% | 0 |
| HAM YES | 0.100 | 0.1045 | 8.3% (0.3–30.5) | −2.2 pp | −20.6% | 0 | 0 |
| **RUS YES** | 0.033 | 0.0346 | 8.1% (0.5–26.2) | **+4.7 pp** | **+135%** | 1.21% | **0** |
| HAD YES | 0.023 | 0.0241 | 6.0% (0.0–27.1) | +3.6 pp | +147% | 0.91% | 0 |
| LEC YES | 0.035 | 0.0367 | 3.5% (0.0–11.9) | −0.1 pp | −3.9% | 0 | 0 |
| NOR YES | 0.029 | 0.0304 | 1.1% (0.0–3.9) | −1.9 pp | −64% | 0 | 0 |
| PIA YES | 0.012 | 0.0126 | 0.13% (0.0–0.5) | −1.1 pp | −89% | 0 | 0 |
| PIA / NOR / HAM NO | 0.992 / 0.98 / 0.905 | — | — | +0.6 / +0.8 / +0.8 pp | <1% | — | below threshold |

Worked arithmetic:
- RUS YES: cost = 0.033 + 0.05×0.033×0.967 = 0.0346. Edge = 0.0813 − 0.0346 = +4.67 pp. ROI = 0.0813/0.0346 − 1 = +135%. ¼-Kelly = 0.25×(0.0467/0.9654) = 1.21%. Lower bound 0.5% < 3.46% → 0.
- VER NO: NO ask = 1 − YES bid 0.61 = 0.39. Cost = 0.39 + 0.05×0.39×0.61 = 0.4019. P(NO) = 1 − 0.5621 = 0.4379. Edge = +3.6 pp, below 4 pp.

**Best watch-list candidate if you drop the lower-bound rule:** Russell YES.
- Limit: 3.3¢. Best ask is 3.3¢ for 305 shares; filling $200 walks the book to a 3.93¢ VWAP, so only about $50 fills near the top.
- Highest entry that keeps the 4 pp edge: **3.9¢**.
- No longer +EV above **7.7¢** on the model alone, or above **~5.2¢** on the 50/50 model–bookmaker blend (fair ≈ 5.5%).
- Size: at most 1.2% of bankroll.
- Exit liquidity is poor: the best bid is 2¢ × 100 shares.

## 2. Market data (Gamma + CLOB)

Event id 1119552, slug `f1-bahrain-grand-prix-winner-2026-10-04`, negRisk = true.
- Event volume $154,844. 24h volume $134,208.
- The "Other" outcome market is listed as **inactive**.
- Fees: Polymarket Sports taker feeRate 0.05 on `C·p·(1−p)`. Makers pay nothing. The Gamma fields `takerBaseFee=1000` and `makerBaseFee=1000` don't match the docs; I used the docs.

| Driver | Bid | Ask | Last | 24h vol | $50 VWAP / all-in | $200 | $1000 |
|---|---|---|---|---|---|---|---|
| VER YES | .61 | .62 (10 sh) | .62 | $29,873 | .6287 / .6404 | .6297 / .6413 | .6299 / .6416 |
| VER NO | .38 | .39 | — | — | .3920 / .4039 | .3980 / .4100 | .4096 / .4216 |
| ANT | .20 | .21 | .21 | $16,186 | .2100 / .2183 | .2148 / .2232 | .2189 / .2275 |
| HAM | .095 | .10 | .10 | $12,548 | .1000 / .1045 | .1000 / .1045 | beyond shown depth |
| LEC | .03 | .035 | .03 | $22,289 | .0350 / .0367 | .0352 / .0369 | beyond shown depth |
| RUS | .02 | .033 | .028 | $5,990 | .0362 / .0379 | .0393 / .0412 | beyond shown depth |
| NOR | .02 | .029 | .03 | $5,350 | .0298 / .0312 | .0340 / .0357 | beyond shown depth |
| HAD | .013 | .023 | .01 | $39,191 | .0230 / .0241 | .0267 / .0280 | beyond shown depth |
| PIA | .008 | .012 | .009 | $2,591 | .0185 / .0194 | .0203 / .0213 | beyond shown depth |
| 14 others | none / ≤.001 | .001–.01 | — | <$500 each | — | — | — |

"Beyond shown depth" means the six ask levels I pulled weren't enough to fill $1000. The book is likely deeper.

- **Overround:** the YES best asks of the 8 contenders sum to **1.062**. Including the 1¢ and 0.1¢ placeholder asks on the other 15 drivers, the total is ≈1.176. The best bids of the 8 contenders sum to 0.996.
- **Implied probability (mid):** VER 61.5, ANT 20.5, HAM 9.75, LEC 3.25, RUS 2.65, NOR 2.45, HAD 1.8, PIA 1.0.

### Resolution rules → payout impact
- The market resolves to whoever is P1 in the **FIA Final Classification**. Time penalties included in that classification count.
- **DSQ or changes after the Final Classification is published are ignored.** A scrutineering DSQ that lands before publication does count.
- **Red flag, not resumed:** the FIA classifies at the lap before suspension, and that leader wins the market. This favours whoever leads when the storm hits. If no green-flag lap is completed, no classification exists. The rules don't spell this case out; most likely it is treated as a cancellation and resolves to "Other".
- **Cancelled, or rescheduled after 11/10/2026 → "Other".** Every driver YES then pays 0 and every NO pays $1. That is a small tail bonus for NO positions.
- **A driver not listed** (for example a reserve driver) winning → "Other".

## 3. Race fundamentals

**Grid** (RaceFans grid page, penalties applied):

| Pos | Driver | Pos | Driver | Pos | Driver |
|---|---|---|---|---|---|
| 1 | VER (1:35.130) | 2 | HAM +0.298 | 3 | ANT +0.501 |
| 4 | LEC +0.536 | 5 | NOR | 6 | PIA |
| 7 | RUS +0.741 | 8 | HAD (qualified P3, 5-place PU drop) | 9 | GAS |
| 10 | BOR | 11 | LAW | 12 | ALO |

COL takes 5 + 10 places. LIN takes 30 places (PU).
*Conflict:* F1.com's summary mentions a Lawson PU back-of-grid drop, while RaceFans lists Lindblad. This doesn't affect the winner market.

**Season form** (after Baku):
- Standings: ANT 302 pts (8 wins), RUS 236, HAM 199, NOR 186, LEC 179, VER 163, HAD 86.
- Russell won Baku; Verstappen was P2 and Hadjar P3.
- Sepang is VER's first pole of 2026.

**This weekend:**
- FP1: VER P1.
- FP2 long runs, adjusted for compound and fuel (motorsport.com): **VER 0, RUS +0.19, LEC +0.32, NOR +0.43, PIA +0.78 s/lap**. ANT and HAM had no clean published run.
- FP3: ANT P1, 0.278s ahead of VER (the-race.com). Mercedes says its upgrade hurt low-speed corners on Friday and was recovered overnight.
- Tyre deg is ~0.3 s/lap average on C3/C4 with track temps in the mid-50s °C, so a two-stop race is likely. Nobody ran the hard tyre on Friday.

**Weather** (Open-Meteo, Sepang 2.76N 101.74E, MYT):

| Model | 14:00 | 15:00 | 16:00 | 17:00 |
|---|---|---|---|---|
| ECMWF IFS | 84% / 0.1mm | 90% / 0.4 | 94% / 0.4 | 94% / 0.4 |
| GFS | 71% / 0.3 | 83% / 0.3 | 92% / 0.0 | 97% / 0.0 |
| ICON | 58% / 0.5 (showers) | 75% / 0.3 | 70% / 0.0 | 53% / 0.0 |

- CAPE is 2,000–2,850 J/kg, which means convective storms are possible.
- BBC: 55% chance of thundery showers at 15:00.
- Every session so far this weekend has been dry.
- Rain is likely but forecast amounts are small. **Scenario weights: dry 40% / mixed 45% / wet 15%.** These are judgement calls, drawn per batch from a Dirichlet distribution.

**Safety car, pit loss, starts, reliability, team orders** — all **assumptions**, not verified with data:
- SC/VSC probability: 45% dry / 65% mixed / 85% wet.
- Pit loss: 21.5 s green, 11 s under SC, 13 s under VSC.
- Ferrari launch advantage: −0.05 s.
- Grid calibrated so pole leads lap 1 76% of the time.
- Race DNF rates: VER 7% and HAD 8% (Red Bull-Ford PU in its first year; HAD already over the PU element limit), Mercedes 4%, Ferrari 5%.
- No team orders modelled. Mercedes could favour ANT, who leads the title by 66 points; that hurts RUS.

## 4. Model

[`race_mc.py`](race_mc.py) is a lap-by-lap Monte Carlo. Each simulated race includes:
- grid gap and start shock
- lap-1 incidents
- pace, tyre deg and lap noise
- overtaking friction
- two-stop strategy windows
- SC/VSC: gaps compress and stops in the window are pulled forward
- rain windows: forced inter/slick stops, wet-skill deltas, and red flags in heavy rain
- DNF hazard

The uncertainty has two layers:
- **Epistemic:** the true pace offsets, the rain mix and the SC rate, drawn 300 times.
- **Aleatory:** race-day randomness, 400 races per draw.

The 90% interval is the 5th–95th percentile across the 300 draws. Two seeds × 120k = **240,000 simulated races**.

| Driver | P(win) seed 7 / seed 8 | Pooled | Dry | Mixed | Wet |
|---|---|---|---|---|---|
| VER | 56.8 / 55.6 | **56.2%** | 61.5 | 55.4 | 45.1 |
| ANT | 16.4 / 16.9 | **16.6%** | 17.3 | 16.5 | 15.3 |
| HAM | 8.5 / 8.1 | **8.3%** | 6.8 | 8.7 | 11.5 |
| RUS | 7.7 / 8.6 | **8.1%** | 6.5 | 8.4 | 11.7 |
| HAD | 5.5 / 6.4 | **6.0%** | 5.4 | 6.2 | 7.0 |
| LEC | 3.8 / 3.2 | **3.5%** | 2.3 | 3.8 | 6.1 |
| NOR | 1.1 / 1.1 | **1.1%** | 0.5 | 1.1 | 2.9 |

**Sensitivity** (20k sims, common seed; reference VER 60.4 / ANT 14.8 / HAM 7.4):

| Change | VER | ANT | HAM |
|---|---|---|---|
| VER pace ±0.10 s/lap | 72.6 / 44.2 (±14 pp) | 10.2 / 20.1 | 5.1 / 10.5 |
| ANT pace −0.10 / +0.10 | 53.8 / 64.3 | 25.0 / 8.0 | 6.5 / 8.1 |
| HAM pace −0.10 | 56.3 | 13.7 | 14.2 (+7 pp) |
| All dry | 65.4 | 15.6 | 5.9 |
| Heavy-wet mix (20/45/35) | 56.6 | 14.6 | 8.4 |
| VER DNF 3% / 12% | 63.9 / 56.1 | 13.8 / 16.0 | 6.7 / 8.2 |
| Overtaking harder / easier | 61.3 / 59.3 | ≈ | ≈ |

**Ranking:** the VER–ANT pace gap matters most, ahead of rain and VER reliability. Overtaking difficulty, deg level and SC rate each move results by less than 2 pp.

**External prior.** Oddschecker best prices: VER 1/2, ANT 7/2, HAM 7/1, LEC 14/1, HAD 16/1, RUS 18/1, NOR 20/1, PIA 33/1. The implied probabilities sum to 1.269. Power de-vig (k = 1.203) gives:

| | VER | ANT | HAM | LEC | HAD | RUS | NOR | PIA |
|---|---|---|---|---|---|---|---|---|
| Book (power) | 61.4 | 16.4 | 8.2 | 3.8 | 3.3 | 2.9 | 2.6 | 1.4 |
| Polymarket mid | 61.5 | 20.5 | 9.75 | 3.25 | 1.8 | 2.65 | 2.45 | 1.0 |
| Model | 56.2 | 16.6 | 8.3 | 3.5 | 6.0 | 8.1 | 1.1 | 0.13 |

**Where the model disagrees with Polymarket, and why:**
- **VER (−5 pp):** the model applies a 7% DNF hazard, 60% non-dry weather (VER wins 45% in wet sims), and wide uncertainty on Mercedes' pace after FP3. The bookmakers agree with Polymarket here, so I give the model less weight on this one.
- **ANT (−4 pp):** the model and bookmakers agree (16.6 vs 16.4). **Polymarket looks rich on Antonelli**, plausibly from championship-leader and fan flow. This is the most robust disagreement, but it is only +2.6 pp after fees.
- **RUS (+5.5 pp) and HAD (+4 pp):** this comes from a single FP2 long run (RUS) and an assumed race pace (HAD). The model also ignores team orders. Both markets put RUS at about 3%, so I treat this as model risk, not edge.

## 5. Risks, live plan, confidence

**Top 3 risks to the Russell watch-list idea:**
1. **The FP2 long run doesn't hold on Sunday.** Mercedes changed its setup overnight, and one session is a thin sample. If RUS's race pace is +0.27 rather than +0.17, his P(win) halves to ~3%, which is the market price.
2. **Team orders.** If Mercedes protects ANT's title lead and RUS runs behind him, the main ways for RUS to win shrink.
3. **Liquidity.** The best bid is 2¢ × 100 shares, so you can't hedge cheaply in-play; this is effectively hold to settlement.

**Exit or hedge triggers:**
- RUS isn't top-4 after the first stops with no SC.
- Dry race and RUS more than 8 s off the lead at lap 30.

**Live-race plan.** Lap-1 conditional probabilities from the model:

| Lap-1 state | Model P(win) |
|---|---|
| VER leads (76% of sims) | 59.3% |
| VER P2 | 51.6% |
| VER P3 | 46.3% |
| HAM leads (19% of sims) | 13.0% |
| ANT leads | 31% |

Triggers:
- **Clean start, VER leads:** expect VER YES to reprice to ~70%+. The model says 59%, so the NO side would show more than 4 pp of edge. Treat that as a signal to re-check pace, not an automatic entry.
- **HAM leads after T1:** the market will likely bid HAM well above the model's 13%. **HAM NO** becomes the candidate.
- **SC/VSC:** VER falls to 53.5% vs 61.7% without one. Cars that haven't stopped gain a cheaper stop. A SC in laps 12–20 helps anyone running long; a SC in laps 30–40 helps whoever is on the alternate strategy.
- **Rain onset** (watch the radar from ~14:30): wet sims give VER 45% and the longshot field more. If rain lands mid-race, the inter-tyre call lap decides the race, so stay flat unless the price runs 8 pp or more past these numbers.
- **Pit sequence:** with ~0.3 s/lap deg the undercut is strong. If Mercedes undercuts VER and comes out ahead, reprice ANT/RUS up about 10–15 pp in the model.
- **ANT YES bid ≥ 21.5¢ before the race:** ANT NO reaches 4 pp of edge on the model and the bookmaker blend (NO cost ≤ 0.794). This is the cleanest conditional entry.

**Confidence:** high that PASS is right; low to moderate in the model's absolute numbers.

**Three facts I could not verify:**
1. **Antonelli's and Hamilton's long-run race pace.** Not in any published FP2 analysis I could reach. This is the second-largest sensitivity.
2. **Live bookmaker odds.** The Oddschecker page parsed only partially; the top 8 looked coherent but the longshots were garbled. bet365 returned 403. The Racing Post table is dated before qualifying. So the external prior is approximate and has no exact timestamp.
3. **Reliability, team orders and history.** I couldn't verify Red Bull-Ford PU reliability or VER's 2026 DNF record, Mercedes' team-orders policy, Sepang SC/VSC history, or 2026 start-performance stats. All of these are modelled assumptions.

## Sources
- Polymarket Gamma API event 1119552; CLOB `/book` for each token; fee docs: https://docs.polymarket.com/trading/fees
- Grid and penalties: https://www.racefans.net/2026/10/03/2026-bahrain-grand-prix-in-malaysia-grid/
- Qualifying: https://www.formula1.com/en/latest/article/verstappen-seizes-first-pole-position-of-the-season-in-qualifying-for-bahrain-gp-in-malaysia.3BW0zzYBLhG54bsQoNKFvP
- Long runs: https://www.motorsport.com/f1/news/f1-bahrain-gp-long-runs-max-verstappen-the-favourite-in-malaysia/10861062/
- FP3: https://www.the-race.com/formula-1/mercedes-fights-back-in-final-sepang-f1-practice/
- Standings: https://www.racefans.net/2026/09/26/2026-azerbaijan-grand-prix-race-result-and-championship-points/
- Weather: Open-Meteo forecast API; https://www.crash.net/f1/news/1105911/1/it-going-rain-f1-bahrain-gp-malaysia-full-weather-forecast
- Relocation and start time: https://en.wikipedia.org/wiki/2026_Bahrain_Grand_Prix ; https://www.news.gp/en/fia-confirms-start-time-for-relocated-bahrain-grand-prix
- Odds: https://www.oddschecker.com/motorsport/formula-1 ; https://racingpost.com/sport/motor-sports-tips/formula-1-tips/bahrain-grand-prix-in-malaysia-betting-tips-odds-and-predictions-aYOkn3V8RxMY

Reproduce: `pip install numpy && python3 sens.py && python3 edge.py` (~4 min). Outputs are in `model_output.txt` and `edge_output.txt`.
