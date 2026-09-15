# Why AMAT Lags, and Why DELL & ARM Popped — 15 Sep 2026

**Snapshot context:** watchlist captured ~10:02 ET, Tue 15 Sep 2026 — roughly 30 minutes into the
session, one day after a violent AI-driven selloff. All prices below from IBKR; news sourced as cited.

---

## 0. The headline finding

**Two of the three premises in the question don't survive contact with the data.**

The single-day percentage column in a watchlist is the noisiest possible lens on relative
performance. Widen the window and the ranking inverts:

| | Sep 14 (1d) | Sep 15 (1d) | 2-day | 3-month | From Jun peak | From 52w high | YTD |
|---|---|---|---|---|---|---|---|
| **AMAT** | −7.07% | −0.23% | −7.28% | −31.41% | −41.46% | −42.78% | **+65.1%** |
| **ASML** | −7.25% | +1.13% | −6.20% | −17.45% | −19.93% | −20.35% | +49.4% |
| **LRCX** | −8.29% | −1.05% | −9.25% | −30.44% | −37.55% | −38.28% | n/a |
| **KLAC** | −6.39% | −0.54% | −6.90% | −35.21% | −44.26% | −45.29% | n/a |
| **ARM** | −9.74% | +3.66% | −6.43% | **−43.62%** | −45.27% | −45.27% | +126.7% |
| **DELL** | −5.82% | +4.87% | −1.23% | **+36.83%** | +36.83% | −1.30% | **+348.5%** |

Three conclusions fall straight out:

1. **AMAT is not lagging "its peers."** It is lagging *ASML specifically*. Against its actual
   closest comparables — Lam Research and KLA — AMAT is mid-pack: better than KLAC (−35.2% over
   3 months), roughly level with LRCX (−30.4%). **ASML is the outlier on the upside, not AMAT on
   the downside.** And YTD, AMAT (+65%) is *beating* ASML (+49%).
2. **ARM is not "doing well."** It is the **worst 3-month performer in the entire group**, down
   43.6%. Tuesday's +5.6% is a bounce off a −9.7% crash day, inside a −45% drawdown. On Sep 14
   ARM fell harder than any semicap name on the list.
3. **Only DELL is genuinely outperforming** — and it is doing so on every timeframe, at an
   all-time high, +348% YTD. That one is real.

So the honest restatement of the question is:

> *Why has ASML decoupled upward from the rest of semicap over three months, why is DELL
> re-rating on fundamentals, and why does ARM whipsaw ±10% a day?*

Those are three different questions with three different answers.

---

## 1. What actually happened on 14–15 September

Monday 14 Sep was a genuine macro event, not stock-specific noise:

- **The AI-slowdown statement.** Leaders at OpenAI, Anthropic and xAI — plus Microsoft's Mustafa
  Suleyman ("We have to keep developing… We just have to do it with a little bit more caution and
  care") — endorsed slowing frontier-model development so safety work can keep pace. Markets read
  this as a direct threat to the AI capex line that has driven the entire 2026 rally.
- **Result:** SMH −4.75%, NVDA −3.36%, AVGO −4.77%, AMD −4.40%, MU −5.25%, INTC −5.59%. The
  Philadelphia semi gauge fell 5.9%. Nasdaq 100 −0.8%, S&P 500 −0.5%.
- **Compounding it:** the **US 10-year yield breached 5.00% for the first time since 2023**, with
  oil spiking. Your own screenshot shows the aftermath — US10Y 5.008%, US30Y 5.377%, both still
  rising; BTC −2.14%, ETH −2.50%, IGV −1.06%. That is not a risk-on tape.

Tuesday 15 Sep was a partial, selective rebound. Critically, **the rebound was not broad** — the
Nasdaq was still −0.12% on your screen while DELL and ARM were +5–6%. That tells you these were
*idiosyncratic* moves, not beta.

**Why this matters for AMAT specifically:** on the actual down day, **ASML fell *more* than AMAT**
(−7.25% vs −7.07%). AMAT's "underperformance" in your screenshot is entirely a Tuesday-morning
rebound-participation gap of ~1.1 percentage points — statistically indistinguishable from noise
30 minutes into a session. The real AMAT story is the three-month chart, not the last two bars.

---

## 2. AMAT: the real problem is *what kind* of semicap it is

AMAT has fallen from **$723 (30 Jun) to $423** — a 41% drawdown — despite a genuinely strong
fiscal Q3 2026 reported 13 Aug:

- Record revenue **$9.115B, +25% YoY**; non-GAAP EPS **$3.50, +41% YoY** (beat $3.39)
- Record operating income $3.08B (33.7% margin), GAAP gross margin 50.3%
- Q4 guide **$10.25B ±$0.5B**, EPS $4.02 ±$0.20 — above consensus

**A record quarter and an above-consensus guide could not stop the stock.** That is the definition
of a de-rating: the market is not disputing the earnings, it is repricing the multiple. Four
reasons:

### 2.1 China is a structural shrinkage, not a cyclical dip
- China was **28% of Q3 revenue ($2.506B)**, down from 35% a year earlier.
- The Sept 2025 BIS rule expansion drives a **~$600M revenue headwind in fiscal 2026**.
- AMAT booked a **$253M settlement with BIS** over an export-controls compliance matter.
- **Domestic substitution is the bigger threat.** China's six major domestic equipment vendors grew
  combined sales from **$748M (2020) to $7.608B (2025)** — a 10x in five years. CXMT, a major AMAT
  customer, now sources an estimated **40–50% of production equipment domestically**. China's 50%
  domestic-equipment mandate makes this policy, not preference.
- Export controls exclude AMAT from China's *leading edge* (logic ≤16/14nm, DRAM ≤18nm) — so the
  China revenue that remains is precisely the mature-node business that domestic vendors are best
  positioned to take.

**The asymmetry with ASML is the whole point:** ASML's EUV is a physical monopoly no Chinese vendor
can replicate this decade. AMAT's deposition/etch/CMP tools have credible domestic substitutes
*today*. Same export regime, completely different competitive consequence.

### 2.2 AMAT is under-indexed to where the AI money actually goes
Q3 Semiconductor Systems mix: **Foundry/Logic 67%, DRAM 26%, Flash 7%**. AMAT's franchise is
broad — materials engineering across many steps — which historically meant diversification, but in
an AI capex cycle means **dilution**. The incremental AI dollar goes disproportionately to:
- **EUV lithography** (ASML, monopoly)
- **Etch/deposition for 3D architectures and HBM** (Lam's sweet spot — LRCX raised its CY26 WFE
  view to the **low-$150B** range from $135–140B, and claims >36% of that opportunity)
- **Process control/inspection** (KLA)

Third-party share work shows **AMAT and Tokyo Electron lost share within their served markets in
2025, while Lam, KLA, ASML and ASMI gained.** AMAT was roughly flat YoY over Q3'24→Q3'25 while KLA
grew double digits and Lam and ASMI grew near 40%. AMAT is answering — it guides process
diagnostics & control to grow **>50% in CY2026** and is launching new optical inspection products —
but that is an attack on KLA's turf, i.e. a share-gain story that has yet to show up in the P&L.

### 2.3 Long-duration cash flows got hit twice on 14 September
This is the mechanism that links AMAT's fall to DELL's resilience.

Semicap equipment revenue is a **derivative of fab construction 2–4 years out**. When AI lab leaders
say "slow down," the thing that is impaired is not 2026 shipments — it is the **2028–2029 fab
buildout** that today's multiple capitalises. Simultaneously, the **10-year going through 5%**
raises the discount rate on exactly those distant cash flows. Long-duration equity got hit from
both ends on the same day.

DELL, by contrast, has a **signed $95B backlog** — contracted, near-term, already-priced revenue.
A philosophical statement about model-training cadence does very little to a purchase order that
ships next quarter.

> **AMAT is a bet on 2029. DELL is a bet on next quarter. The market spent 14 September
> repricing 2029.**

### 2.4 Valuation offered no cushion at the top
AMAT ran **~98–108% YTD into August** before the drawdown. It entered the derating priced for
perfection. The multiples have now largely converged and arguably inverted the quality ranking:
**AMAT forward P/E ~24.3 vs ASML ~28.1** (7 Sep). ASML holds a ~24% premium to the semiconductor
industry median (22.65); AMAT just 7.3%. Note also that AMAT's consensus target (~$658) now sits
~55% above spot — the sell side has *not* re-rated with the tape, which usually means a wave of
target cuts is pending. Bernstein has already cut (to $210 from $220, split-adjusted basis), and
Deutsche Bank slashed sector targets while retaining Buys on three picks.

### 2.5 So why did ASML hold up?
ASML's 3-month drawdown is half AMAT's for concrete reasons:
- Raised FY26 revenue guidance from **€36–40B to €43–45B**, gross margin 54–56%
- Plans to lift **low-NA EUV output ~30%**, from ~65 units (2026) to **78–80 (2027)**; studying a
  further 30% for 2028 — i.e. management publicly committing capacity to 2027–28 demand
- **Intel is running High-NA EUV in production on 18A**; High-NA projected at ~25% of EUV revenue
  by 2028
- Demand commentary points to AI logic + DRAM and installed-base upgrades

The thesis that has taken hold: **EUV capacity, not GPU supply, is the binding constraint on AI
silicon.** A monopoly on the bottleneck is the highest-quality position in the entire supply chain,
and it is structurally insulated from Chinese substitution in a way AMAT's portfolio is not.

**But note the caveat:** ASML is *not* immune. It fell 7.25% on Monday — more than AMAT. Its
outperformance is a slower bleed, not a different direction.

---

## 3. DELL: the only genuine outperformer, and it is fundamental

DELL at **$565.69** sits ~0.4% off its all-time high, **+348.5% YTD**, +36.8% in three months. Not
a bounce — a re-rating. Three catalysts stacked inside eleven trading days:

### 3.1 Q2 FY2027 earnings (1 Sep) — blowout, +15.8% next day on 24.4M shares (~8x normal volume)
- Revenue **$47.0B, +58% YoY** — record
- Non-GAAP EPS **$7.04, +203% YoY** (GAAP-adjusted variants reported ~$6.34/+273%)
- **ISG revenue $31.8B, +89%**; AI server revenue $16.4B
- **$60.9B of AI orders booked in the quarter**; **$95B AI backlog** at period end
- FY guidance raised by **$25B** to **~$192B** for FY ending Jan 2027

### 3.2 The margin bear case was killed, not merely deferred
This is the single most underrated element. The standing short thesis on DELL was always: *AI
servers are low-margin box-assembly around NVIDIA silicon; volume growth destroys mix.* The quarter
refuted it outright:

- **ISG operating margin 8.8% → 15.0% YoY** (+620bps), and **10.5% → 15.0% sequentially**
- **Company gross margin 18.3% → 20.9%**; operating margin **6.0% → 11.5%**
- Achieved *while* AI-optimised servers were **more than half of ISG revenue**

Margin expanding *through* the AI mix shift is the opposite of the bear case. That forces a genuine
multiple re-rate, not just an estimate raise — which is precisely why the move has persisted rather
than faded.

### 3.3 Oracle validated the demand externally (11 Sep, +11.98%)
Oracle reiterated **FY27 capex of $90–95B** against a **$664B backlog**, and CFO Hilary Maxson
**named Dell and HPE specifically** as recipients for AI racks, cooling and networking. HPE +11% to
$61.49; SMCI +7%. Both DELL and HPE posted their largest single-session gain of the year.

This matters more than an internal guide: it is a *customer* confirming the spend. It converts
Dell's backlog from a company claim into a triangulated one.

### 3.4 Mechanical and sentiment support
- **S&P 100 inclusion** (announced for 21 Sep) — forced index buying, and a signalling upgrade
- Street targets repriced to **$600–650** (BofA, Bernstein, Evercore ISI, Raymond James); RBC
  initiated Outperform
- Momentum/quant flows follow 52-week-high breakouts

### 3.5 Why DELL beat its *own* peers on the day
Note SMCI was only **+1.12%** vs DELL +5.88% in your screenshot. Within AI servers the market is
discriminating by counterparty quality: Dell has investment-grade credit, Tier-1 enterprise
relationships, and financing capacity to carry a $95B backlog's working capital. That balance-sheet
capacity *is* the moat in a business where the bottleneck is who can fund the inventory. Dell and
HPE trade as the quality tier; SMCI does not.

### 3.6 The honest risk
Dell captures a modest slice of the value stack — NVIDIA runs ~75% gross margin on the silicon
inside each PowerEdge. Dell's ~21% gross margin is structurally capped, and the whole thesis rests
on **pricing discipline as component costs rise** (memory in particular is inflating). At +348%
YTD, a single quarter of backlog conversion at lower margin would hurt badly. The cash-conversion
cycle on a $95B backlog is the number to watch, not the backlog headline.

---

## 4. ARM: not strength — a high-beta bounce inside a −45% drawdown

This is where the screenshot misleads most severely.

| Date | Close | Move |
|---|---|---|
| 18 Jun 2026 | $439.46 (52w high $452.70) | peak |
| 3 Aug 2026 | $239.06 | trough ~$219.39 intraday |
| 11 Sep 2026 | $264.79 | |
| 14 Sep 2026 | $239.01 | **−9.74%** |
| 15 Sep 2026 | ~$252 | **+5.6%** (your screenshot) |

**ARM is down 43.6% over three months — the worst in the group, worse than AMAT.** The +5.63% is
a dead-cat bounce, and it is large *because* the prior day's fall was large. Why the crash from
June:

### 4.1 Valuation was extraordinary even by AI standards
- **~100x NTM earnings**
- **~39x NTM EV/revenue vs a peer-group mean near 10x**

At 39x sales the stock is not discounting a business, it is discounting a narrative. Narratives
have no valuation floor — which is why "AI leaders call for slowdown" produced a −9.7% day in ARM
versus −3.4% in NVIDIA. **Duration risk in equity form.**

### 4.2 The fundamental crack: royalty growth was cut
CFO Jason Child conceded Arm has "seen some incremental slowdown versus what was expected at the
beginning of the year," with FY royalty growth now **"closer to the high teens" versus ~20%**
guided earlier — **because higher memory prices are denting smartphone unit sales.**

This is the underappreciated link: **the memory shortage driving DRAM pricing (which helps AMAT's
26% DRAM mix and Lam's etch/dep) is simultaneously raising smartphone BOM costs and suppressing
handset volumes — which is where Arm's royalty base actually lives.** The same AI cycle that lifts
semicap is squeezing Arm's core. HSBC downgraded to Hold on 14 July citing TSMC 3nm capacity
bottlenecks and a valuation pricing in years of growth.

### 4.3 The structural overhang: SoftBank
- SoftBank holds **~86–88%** of ARM; **public float is only ~13.35%**
- SoftBank has pledged **~72% of its ARM equity against an $8.5B margin loan**

A thin float amplifies moves in both directions — it is the direct mechanical reason ARM prints
−9.7% and +5.6% on consecutive days. The margin loan adds reflexivity: ARM weakness pressures
SoftBank (down 36% in the period; ARM's contribution to SoftBank NAV fell ¥14tn from the June
peak), and a forced-liquidation scenario against a 13% float is the tail risk that keeps a
structural discount in the name.

### 4.4 What the Tuesday bounce actually was
Real but second-order news existed — Piper Sandler initiated Overweight (9 Sep) on server CPU
design wins; the **Neoverse CSS N4** launched 8 Sep; new Arm Compute Subsystem for Mobile, neural
Mali GPU architectures and the C2 CPU cluster were unveiled at developer events; ~$2B AI CPU
pipeline commentary. But none of that is a 5.6% event on its own. **A 13%-float, 100x-earnings,
heavily-shorted stock that fell 9.7% yesterday bounces 5.6% today largely on mechanics** — short
covering, options gamma, and dip-buying into a name 45% off its high.

---

## 5. The unifying framework

The AI trade split into two tiers in 2026, and 14 September was the day the market priced the split
violently:

| | **Short-duration / contracted** | **Long-duration / capitalised** |
|---|---|---|
| Examples | DELL, HPE | AMAT, LRCX, KLAC, ARM |
| Revenue basis | Signed backlog ($95B) | Fab capex 2–4 years out; royalty streams |
| Sensitivity to "AI slowdown" rhetoric | Low — POs already signed | **Severe** — impairs terminal value |
| Sensitivity to 10Y through 5% | Low | **Severe** — discount rate on distant cash flows |
| 3-month result | **+36.8%** | **−17% to −44%** |

Within the long-duration tier, a second filter decides survival: **is your moat replicable by a
subsidised Chinese competitor?**

- **ASML** — no. EUV is a physical monopoly. Drawdown only −17.5%.
- **AMAT** — partially. Dep/etch/CMP have credible domestic substitutes today, 28% China exposure
  and falling, $600M sanctioned headwind. Drawdown −31.4%.
- **KLAC / LRCX** — in between, −35.2% / −30.4%.
- **ARM** — different axis entirely: no China problem, but a 100x multiple, a royalty base in
  *smartphones* (not AI), and an 86% owner with the stock pledged. Drawdown −43.6%.

**Your screenshot caught the exact moment the tiers were re-sorting — and a one-day column cannot
show you a re-sorting.**

---

## 6. What would actually change each thesis

**AMAT — watch for:**
- Q4 FY26 print vs the $10.25B ±$0.5B guide, and the **first FY2027 WFE framing**
- China as % of revenue: does it stabilise near 28% or keep sliding toward 20%?
- Whether the **>50% CY26 growth in process diagnostics & control** materialises — that is the
  stated share-gain offset, and it is the bull case
- Sell-side target cuts toward spot (consensus ~$658 vs $423 is unsustainable; expect resets)
- Any further BIS rule expansion — the tail risk is another $600M-scale headwind

**DELL — watch for:**
- **Backlog → revenue conversion at margin.** ISG operating margin holding ≥15% is the whole thesis
- Cash conversion cycle / working capital drag on a $95B backlog
- Memory cost pass-through — can pricing discipline survive DRAM inflation?
- Whether Oracle's $90–95B capex is actually spent on schedule

**ARM — watch for:**
- **Royalty growth**: does "high teens" hold, or slip further on smartphone weakness?
- Any change to SoftBank's margin-loan position or float
- Neoverse/server CPU design wins converting to disclosed royalty revenue — the only thing that
  justifies re-rating off a smartphone base onto an AI base
- The multiple: at ~100x NTM, ARM needs the AI datacentre story to become financially visible, not
  just architecturally real

---

## 7. Direct answers

**Q: Why is AMAT lagging its peers?**
On the day, it isn't — that's a ~1pp rebound-participation gap, noise. Over three months it is
down 31% while ASML is down 17%, and that gap is real and structural: AMAT carries 28% China
revenue under a $600M sanctions headwind against domestic competitors that 10x'd in five years,
its 67/26/7 foundry-DRAM-flash mix under-indexes the EUV and HBM steps where AI capex concentrates,
it lost served-market share in 2025 while Lam/KLA/ASML gained, and its cash flows sit far enough
out that both the "AI slowdown" headline and a 5% 10-year hit it twice. Against its *true* peers
LRCX (−30.4%) and KLAC (−35.2%), AMAT is mid-pack. **ASML is the outlier, not AMAT.**

**Q: Why is DELL doing so well?**
Real fundamentals: $47B revenue +58%, $60.9B of AI orders in one quarter, a $95B backlog, guidance
raised $25B — and critically, **ISG margins expanded 620bps *while* AI servers exceeded half of
segment revenue**, destroying the margin-dilution short thesis. Oracle then externally validated
demand by naming Dell in its $90–95B capex plan, and S&P 100 inclusion added mechanical flows.
Short-duration contracted revenue is exactly what you want to own when the market is questioning
AI capex *duration*.

**Q: Why is ARM doing so well?**
**It isn't.** ARM is the worst performer in your entire watchlist over three months (−43.6%),
45% below its June high, and it fell 9.7% the day before your screenshot. Tuesday's +5.6% is a
mechanical bounce in a thin-float (13.35%), ~100x-earnings, heavily-shorted stock — amplified by
short covering and gamma, not driven by news. The underlying trend is down: royalty growth cut from
~20% to "high teens" as memory prices suppress smartphone volumes, a valuation at 39x EV/sales
versus a peer mean of 10x, and SoftBank's 72% equity pledge against an $8.5B margin loan sitting
over a tiny float.

---

*Analysis only — not investment advice. Prices intraday 15 Sep 2026 and will have moved.*
