# ALPHABET Q2 2026 FORM 10-Q — CAPEX BENEFICIARY & ROI ANALYSIS

**Source: Alphabet Inc. Form 10-Q, quarterly period ended June 30, 2026 (PRIMARY).**
Companion to `GOOG_Q2_2026_earnings_event_read.md` (built off the 8-K/Ex-99.1).
The 10-Q supersedes that note where they conflict — see §6 Corrections.
Analysis date: 2026-07-26.

---

## BLUF (5 lines)

1. **The real capex number is not $195–205B — it is $811B.** Alphabet discloses $811.0B of
   material purchase commitments and other contractual obligations, of which $707.0B is
   fixed/guaranteed, "the significant majority" being long-term supply agreements for
   technical-infrastructure production capacity. The annual capex guide is the cash-out
   slice; the commitment book is the forward order book to suppliers.
2. **Alphabet has changed funding regime.** It raised ~$101B of external capital in H1 2026
   ($51.8B notes + $20.5B common + $10.0B Berkshire private placement + $19.0B 6.25%
   mandatory convertible preferred), and authorized a $40B ATM. A company that used to
   fund everything from FCF and buy back stock is now issuing equity *and* preferred.
3. **Quality-of-earnings correction:** the $99.0B equity gain is attributed by management to
   **SpaceX and a private company** — *not* "largely Anthropic" as widely reported. Split:
   $77.4B unrealized on non-marketable (measurement alternative) + $21.4B unrealized on
   marketable/other + $0.3B realized.
4. **Beneficiary hierarchy is now contractually visible:** Broadcom (TPU design, locked to
   2031) > TSMC (fabs every TPU) > Celestica (TPU server assembly) > HBM/memory > power &
   electrical (the true bottleneck — energy take-or-pay running to **2054**).
5. **Best risk-adjusted share-price ROI: BROADCOM (AVGO), 70% confidence** — the widest gap
   between contracted revenue certainty and an undemanding multiple (~20–24x fwd vs ~30–34x
   semis median). Highest torque but higher risk: Celestica. The crowded, already-repriced
   trades are MU (+241% YTD) and Vertiv (52x fwd) — own them, don't chase them.

---

## §1 — WHAT THE 10-Q REVEALS THAT THE PRESS RELEASE DID NOT

| Disclosure | Figure | Why it matters |
|---|---|---|
| Purchase commitments & other contractual obligations | **$811.0B** ($200.7B short-term) | The forward supplier order book. ~4x the annual capex guide. |
| Fixed/guaranteed commitments | **$707.0B** | "Significant majority" = long-term supply agreements to *secure future production capacity*. Suppliers have visibility, not hope. |
| Leases not yet commenced | **$85.2B** | Data centers, commencing 2026–2031, terms 1–26 yrs. Off the balance sheet today. |
| Assets not yet in service | $78.6B → **$122.8B** (+56% in 6M) | $122.8B of capex already spent that earns **zero revenue and zero depreciation** yet. |
| Accrued purchases of PP&E | $8.9B → **$16.2B** (+82%) | Orders accelerating *faster* than the cash capex line shows. |
| Energy service agreements | terms to **2054**, take-or-pay | Alphabet is locking power for 28 years. Energy is the binding constraint. |
| Backstop guarantees | **$7.6B** | Alphabet guaranteeing *counterparties'* procurement of long-lead power equipment. It is underwriting its suppliers' supply chain. |
| TPU merchant sales | began Q2 2026 | "Agreements to supply TPU systems to customers who require or provide on-premises infrastructure… significant majority to be recognized in **2027**." |
| External capital raised H1 | **~$101.3B** | See §2. |
| Revenue backlog | $519.5B ($513.9B Cloud) | >50% to be recognized within 24 months. |

**The single most important line in the filing** (Note 10): commitments of $707.0B are
*fixed or guaranteed*. That is not a spending aspiration subject to a capex-guide revision —
it is a contractual liability. For suppliers, this is the difference between a demand
forecast and a signed order.

### Segment detail (Q2 2026 vs Q2 2025, $M — 10-Q revenue-by-type table)

| Line | Q2'25 | Q2'26 | YoY |
|---|---|---|---|
| Google Search & other | 54,190 | 63,271 | +16.8% |
| YouTube ads | 9,796 | 11,055 | +12.9% |
| **Google Network** | 7,354 | **7,303** | **−0.7%** ← quietly shrinking |
| Google subs/platforms/devices | 11,203 | 12,911 | +15.2% |
| Google Services total | 82,543 | 94,540 | +14.5% |
| **Google Cloud** | 13,624 | **24,768** | **+81.8%** |
| Other Bets | 373 | 382 | +2.4% |
| **Total revenues** | 96,428 | **119,796** | **+24.2%** |

Note the depreciation trajectory: H1 depreciation $13.6B vs $9.5B (+43%) — and that is
*before* the $122.8B of not-yet-in-service assets begins depreciating. This is the
mechanical earnings headwind building for 2027–28.

---

## §2 — THE FUNDING REGIME CHANGE (the underrated story)

| Instrument | Date | Net proceeds |
|---|---|---|
| Senior unsecured notes (USD) | H1 2026 | $20.0B |
| Senior unsecured notes (GBP/CHF/EUR/CAD/JPY) | H1 2026 | $31.8B |
| Common stock offering (29M Class A @ $355.1982; 29M Class C @ $351.8018) | Jun 4, 2026 | $20.5B |
| Private placement to **Berkshire Hathaway** affiliate (14M A + 14M C) | Jun 4, 2026 | $10.0B |
| **6.25% Mandatory Convertible Preferred** (Series A + B, 19M shares) | Jun 5, 2026 | $19.0B |
| ATM program authorized (unused) | Jun 1, 2026 | up to $40.0B |
| **Total raised H1 2026** | | **~$101.3B** |

Long-term debt carrying value: $98.2B. Proceeds explicitly earmarked for "capital
expenditures to scale AI infrastructure and global compute."

**Read-through:** Alphabet is diluting shareholders and paying a 6.25% preferred coupon to
fund compute. That is either (a) the highest-conviction capital-allocation signal in
mega-cap tech, or (b) evidence the buildout has outgrown internal cash generation. It is
genuinely both. For *suppliers*, it is unambiguously bullish: the customer has pre-funded
the order book and is no longer FCF-constrained. For *GOOG equity holders*, it caps near-term
upside — share count is rising, and the preferred sits ahead of common.

---

## §3 — BENEFICIARY MAP

The 10-Q does not name suppliers. Tiering below combines 10-Q commitment structure
(primary) with public supply-chain reporting (secondary, labelled).

### TIER 1 — Contracted silicon (highest certainty)

| Company | Role | Evidence |
|---|---|---|
| **Broadcom (AVGO)** | Designs Ironwood + TPU 8t training chip; **agreement reported to run through 2031** | Google's lead ASIC partner; longest-dated contractual lock in the chain |
| **TSMC (TSM)** | Manufactures **every** Google TPU; Ironwood on N3P, 8th-gen at 2nm | Sole foundry — no second source |
| **MediaTek** (2454.TW) | Designs TPU 8i inference chip + cost-optimized variants | Taiwan-listed; limited US access |
| **Marvell (MRVL)** | *In talks* as third design partner (memory processing unit + inference TPU) | **Optionality — not yet contracted** |

### TIER 2 — Systems, assembly, memory

| Company | Role | Note |
|---|---|---|
| **Celestica (CLS)** | Primary **TPU server assembly** partner | Highest revenue torque to TPU units; thin EMS margins; concentration risk |
| **Micron (MU)** / SK Hynix / Samsung | HBM + DDR5 | MU 2026 HBM **sold out** under fixed-price contracts; ~21% HBM share |
| Optics/interconnect (COHR, LITE, FN, CRDO, ALAB) | Scale-up/scale-out fabric | Real but fragmented exposure |

### TIER 3 — Power, electrical, thermal (**the actual bottleneck**)

The $707B commitment base includes energy take-or-pay to **2054**, plus $7.6B of backstop
guarantees for *long-lead power equipment*. Alphabet is not short chips — it is short
**electrons and grid hardware**.

| Company | Role | Positioning |
|---|---|---|
| **GE Vernova (GEV)** | Gas turbines, grid equipment | $176B backlog; 22% rev growth Q2'26; missed EPS on tariffs |
| **Eaton (ETN)** | Switchgear, electrical distribution | Electrical backlog **+48% YoY**, record $19.6B |
| **Vertiv (VRT)** | Power/thermal management | ~28% organic growth, ~$13.5B rev 2026 — but **52x fwd, beta 2.03** |
| Quanta (PWR), Comfort Systems (FIX), EMCOR (EME) | Build/electrical contracting | Record backlogs; labor-constrained |
| IPPs — Constellation (CEG), Vistra (VST), NextEra (NEE) | PPA counterparties | Direct counterparties to 28-yr take-or-pay |

### TIER 4 — Second derivative (WFE)

**AMAT, LRCX, KLA, ASML** — benefit only *after* TSMC/Micron convert demand into fab
capacity. Real, but one step removed and lagged by 2–4 quarters. **This is where the
user's existing AMAT position sits** — genuine exposure, slower transmission.

### TIER 5 — STRUCTURALLY THREATENED

**Nvidia (NVDA).** Per the 10-Q, Google has begun recognizing revenue from selling **TPU
systems to external, on-premises customers**, with the majority landing in 2027. Google is
converting from Nvidia customer to Nvidia *competitor* in merchant AI silicon. This is a
primary-sourced competitive disclosure, not analyst speculation, and it is the most
underpriced negative in this filing.

**Arm (ARM)** — modest positive (Axion server CPUs), but TPU-centric spend is custom-ASIC
heavy, not Arm-royalty heavy. The user's ARM position gets the weakest read-through of the
book.

---

## §4 — SHARE-PRICE ROI RANKING

Framework: **ROI ≈ (revenue delta ÷ base) × margin quality × contract certainty ×
valuation headroom.** The biggest beneficiary is rarely the best return — what matters is
the gap between contracted reality and what the multiple already assumes.

*These are probabilistic leans on an uncertain future, not guarantees. Confidence % and
invalidation levels are stated so each call can be falsified.*

| Rank | Name | Thesis in one line | Certainty | Valuation headroom | Conf. |
|---|---|---|---|---|---|
| **1** | **AVGO** | Contracted to 2031, ~20–24x fwd vs ~30–34x semis median — certainty is not priced | HIGH | HIGH | **70%** |
| **2** | **GEV / ETN** | Energy is the true constraint; 28-yr take-or-pay + $7.6B equipment backstops; ETN ~30–32x with +48% backlog | HIGH | MEDIUM | **62%** |
| **3** | **CLS** | Purest TPU-unit torque, small base, +24% YTD | MED-HIGH | LOW (~40x) | **55%** |
| **4** | **MRVL** | Third-design-partner optionality unpriced — binary | LOW | HIGH | **45%** |
| **5** | **TSM** | Sole foundry, but Google is one of many customers — diluted | HIGH | MEDIUM | **58%** |
| **6** | **MU** *(held)* | Sold-out HBM is real; +241% YTD and $1.21T cap mean it is now a *cycle* bet | HIGH | **LOW** | **50%** |
| **7** | **AMAT** *(held)* | Second-derivative, lagged | MEDIUM | MEDIUM | **52%** |
| **8** | **VRT** | Best growth, worst entry — 52x fwd, beta 2.03 | HIGH | **VERY LOW** | **40%** |
| — | **NVDA** | Structural headwind from Google TPU merchant entry | — | — | negative lean |

### Top pick — **BROADCOM (AVGO)** | Confidence 70%

The only name where a *multi-year contractual lock* (through 2031) coexists with a
*below-peer multiple* (~20–24x fwd vs ~30–34x semis median). Google's $707B guaranteed
commitment book converts directly into AVGO custom-ASIC revenue with visibility almost no
other supplier has. AVGO is +10% YTD — it has materially lagged the AI complex, so the
expectations bar is low relative to the contracted reality.
**Invalidation:** evidence Google is shifting Ironwood-class *training* silicon share to
MediaTek/Marvell, or AVGO custom-ASIC growth guidance decelerating below ~30% YoY.

### Highest torque — **CELESTICA (CLS)** | Confidence 55%
Primary TPU-server assembler: TPU unit growth flows to a far smaller revenue base than
AVGO's. But EMS margins are thin, ~40x is a full multiple for an assembler, and single-customer
concentration cuts both ways. Position it as a **high-beta satellite, not a core holding.**
**Invalidation:** loss of primary-assembler status, or gross margin compression below ~10%.

### The honest warning — **MICRON (MU)** *(currently held)*
MU is a genuine beneficiary: 2026 HBM sold out on fixed-price contracts, ~21% share, and a
direct Anthropic memory supply agreement (~16 contracts, ~$22B upfront commitments). But:
**+241% YTD, all-time high $1,213.37 on 2026-06-25, now ~$984 after a ~22% drawdown, $1.21T
market cap.** The much-cited ~6x forward P/E is **peak-cycle optics, not cheapness** — a
trough multiple on peak earnings is the classic late-cycle memory signature. Memory is
still a cyclical, and fixed-price contracts that protect you on the way up also cap you when
spot rolls.
**Verdict: HOLD, do not add at these levels.** This is not a sell call — the fundamentals
have not broken, and per the anti-churn discipline a strong GOOG print is not an exit
trigger. It is a *sizing* caution.

### Avoid chasing — **VERTIV (VRT)**
Best operational exposure in Tier 3, worst risk/reward at 52x forward with beta 2.03. Any
wobble in the capex narrative lands on that multiple first and hardest.

---

## §5 — IMPLICATIONS FOR THE EXISTING BOOK (MU, AMAT, ARM, SOXX, SOXL, QQQ)

*** ANTI-CHURN GUARDRAIL (portfolio-reallocation-discipline) ***
Nothing below is an automatic trim/exit trigger. Any action must clear the fundamentals-first
bar standalone — never to "fund" a new idea.

| Holding | Read from this 10-Q | Action lean |
|---|---|---|
| **MU** | Strongest direct read (HBM sold out; Anthropic supply deal) — but already repriced +241% YTD | **Hold, don't add.** Cycle risk now exceeds thesis gap. |
| **AMAT** | Positive but lagged — WFE benefits only after TSMC/MU add capacity | **Hold.** |
| **ARM** | Weakest read-through — spend is custom-ASIC, not Arm-royalty heavy | **Hold**; lowest-conviction name in the book vs this thesis. |
| **SOXX** | Broad basket capture of the $707B commitment book | **Hold** — the cleanest low-maintenance expression. |
| **SOXL** | **3x leveraged.** Semis complex is at elevated multiples with MU already −22% from ATH. Leveraged decay in choppy tape is a structural cost, not a risk you're paid for. | **Flag: size discipline.** The genuine risk in this book. |
| **QQQ** | Index-level; GOOG dilution (share count up) is a small drag | **Hold.** |

**The one gap worth noting:** the book is heavily weighted to *silicon* (MU, AMAT, ARM,
SOXX, SOXL) and has **zero exposure to the power/electrical bottleneck** — which this
filing identifies as the binding constraint (28-year energy take-or-pay, $7.6B equipment
backstops). If capital is ever deployed to a new name, GEV/ETN diversifies a real,
currently-unhedged concentration. Sizing that is a Module 6 exercise and is **not run here**
— it runs only on request.

---

## §6 — CORRECTIONS TO THE PRIOR (8-K-BASED) NOTE

| Item | Prior note said | 10-Q says | Status |
|---|---|---|---|
| Equity gain attribution | "largely the Anthropic stake markup" | "primarily related to unrealized gains… from **SpaceX and a private company**" (MD&A) | **CORRECTED** — press framing was incomplete; SpaceX is named first and Anthropic is never named in the filing. |
| Gain composition | flagged as unresolved | $77.4B unrealized non-marketable (measurement alternative) + $21.4B unrealized marketable/other + $0.3B realized = **$99.031B** | **RESOLVED** |
| Realized vs unrealized | "deferred to the 10-Q" | Realized only **$278M** — 99.7% unrealized | **RESOLVED** — confirms the paper-gain thesis emphatically. |
| Secondary "$37.7B non-marketable" figure | flagged as non-reconciling | Actual measurement-alternative unrealized = **$77.4B** | **DISCARDED** — secondary figure was wrong. |
| Core EPS bridge | ~$2.62 | Unchanged in direction; full $99.0B still the correct amount to back out | **STANDS** |
| Cloud backlog | $514B | $513.9B Cloud / $519.5B total | **CONFIRMED** |

Also newly disclosed and absent from the prior note: EC Android fine of **$5.2B** paid July
2026 (previously accrued); **$2.1B** PriceRunner/Klarna legal charge ($1.5B in G&A, $581M in
OI&E); headcount 198,933.

---

## §7 — SOURCING

**PRIMARY:** Alphabet Inc. Form 10-Q, period ended 2026-06-30 (user-supplied PDF, 65pp) —
all commitment, capex, PP&E, funding, segment, equity-gain, backlog and TPU-merchant figures.
Alphabet 8-K Ex-99.1 (2026-07-22) for the prior note. Alphabet Q1 2026 8-K for comparatives.

**SECONDARY (labelled — supply chain, valuation, price action):**
- TPU supply chain (Broadcom→2031, MediaTek TPU 8i, TSMC N3P/2nm, Celestica assembly,
  Marvell in talks): Tom's Hardware, TheNextWeb, SemiAnalysis, Jon Peddie Research.
- Valuations: GuruFocus, StockAnalysis (AVGO ~20–24x fwd; MU fwd 6–10x, trailing ~19x;
  VRT ~52x; ETN ~30–32x).
- Price action: MU +241% YTD, ATH $1,213.37 (2026-06-25), ~$984 current, $1.21T cap;
  AVGO +10% YTD / +40% 52wk; CLS +24% YTD.
- Backlogs: GEV $176B; ETN electrical $19.6B (+48%); VRT ~$13.5B 2026 revenue.

**Caveats:** supplier identities are secondary-sourced — the 10-Q names no vendor. Forward
P/E figures vary by provider depending on EPS basis (acute for MU given cycle earnings, and
for GOOG given the equity-gain distortion); ranges are shown rather than false precision.
Share-price ROI rankings are probabilistic judgments about an uncertain future, expressed
with confidence levels and invalidation triggers so they can be falsified — not forecasts
of fact, and not personalized investment advice.
