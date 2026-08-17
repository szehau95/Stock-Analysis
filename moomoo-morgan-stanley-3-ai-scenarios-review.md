# Morgan Stanley's 3 AI Scenarios — Beneficiary Map Review

**Source under review:** moomoo Singapore Instagram carousel (posted 6 Aug 2026), reproducing Morgan Stanley's three AI endgame scenarios. Production date on the graphic: 3 Aug 2026.

**Review date:** 17 August 2026. All prices are live IBKR quotes as of that date. Forward P/E figures are consensus estimates from public sources and vary by methodology — treat them as ±2 turns.

**Nature of this document:** a critique of a published beneficiary map and a relative-value ranking. Not personalised investment advice.

---

## 1. Validating the beneficiary lists

### 1.1 What the map gets right

| Call | Assessment |
|---|---|
| **NVDA in all three, top tier** | Correct, and the strongest structural claim in the deck. Cheaper inference raises token volume faster than it lowers price per token; GPU demand is scenario-invariant. |
| **Power supply chain in all three** | Directionally right. Compute grows in every branch, so electrons are the common denominator. (Constituent selection is a separate problem — see 1.2g.) |
| **MSFT upgraded in Scenario 3; AMZN/GOOGL demoted** | The best non-obvious call on the page. Azure Arc / Azure Local mean Microsoft monetises a shift to on-prem instead of being disintermediated by it. |
| **DELL / HPE / NTAP concentrated in Scenario 3** | Correct mechanism — open weights running locally require someone to sell the local iron. |
| **ZS and NTSK dropping out of Scenario 3** | Internally consistent, and easy to mistake for an error. Cloud-egress inspection matters less when inference stops leaving the building. |
| **Identity security (OKTA, SAIL) across scenarios** | Sound. Agentic AI creates non-human identity sprawl regardless of who trains the model. |

### 1.2 Where it is wrong, incomplete, or internally inconsistent

**a) `P — "Everpure"` is a data error.** There is no US-listed on-premise infrastructure vendor under ticker `P` by that name. In a row with DELL, HPE and NTAP, the intended name is almost certainly **PSTG (Pure Storage)**. Do not act on that tile as printed.

**b) AVGO appears only in Scenario 1.** The largest analytical hole. Broadcom is two distinct AI franchises: custom XPU/ASIC for hyperscalers, and the Ethernet scale-out fabric (Tomahawk/Jericho). Inference-heavy hybrid and open-weight worlds shift spend *toward* cost-optimised custom silicon and Ethernet, not away. Excluding Broadcom from Scenarios 2 and 3 entirely is not defensible.

**c) AMD is absent from all three lists.** AMD is the canonical open-weight beneficiary — ROCm plus the vLLM/SGLang ecosystem, MI-series positioned explicitly on inference TCO, and open models are what actually run well on non-CUDA silicon. Its omission from Scenario 3 is a logic failure. The market disagrees loudly: AMD is **+142.8% YTD**, among the best performers in the whole complex.

**d) META in Scenario 1 only — backwards.** Meta is the Western open-weight champion. Listing MiniMax, Z.AI, Alibaba and Tencent as Scenario 3 model-provider winners while excluding Llama's owner is inconsistent. The steelman ("open weights erode Meta's edge") applies with equal force to the Chinese labs that *are* listed.

**e) "Model providers" as biggest beneficiaries of open-source winning is self-contradictory.** If open weights win, model builders lose pricing power — that *is* the mechanism of the scenario. They gain relevance and share; value accrues to compute, distribution and the application layer. The map confuses being central to the story with capturing the profit.

**f) No foundry and no memory, anywhere.** TSMC is absent from all three scenarios, yet every branch runs on its wafers. Memory (Micron, SK Hynix, Samsung) is absent, yet HBM/DRAM is the binding constraint on 2026 buildouts — CDW's own 2026 guidance cites memory constraints by name. A 2026 beneficiary map without memory omits the tightest link in the chain.

**g) The power basket is populated with second-derivative names and missing the first-order ones.** BE (fuel cells), INIO (gas engines) and SEI (mobile turbines) are genuine on-site power. But **WMB is a midstream gas pipeline operator and LBRT is a frac services company** — gas-supply plays, not on-site power providers. Meanwhile the actual electrical infrastructure winners are nowhere: **VRT** (thermal and power distribution), **ETN**, **GEV**, **PWR**.

**h) The networking treatment is incoherent across scenarios.** Scenario 1 gets optics (COHR, LITE, ANET); Scenario 2 gets enterprise networking (CSCO, FFIV); Scenario 3 gets no network layer at all. If open weights win and enterprises build their own clusters, that is *more* enterprise networking demand. You cannot have decentralised inference over no network.

**i) The SaaS calls are contested and presented as settled.** CRM, WDAY, INTU and NOW as AI beneficiaries is the most debatable claim on the page. The prevailing 2026 market view is that seat-based SaaS is disrupted by agents, not helped. The implicit MS argument — collapsing inference cost relieves COGS and expands margin — is legitimate, but it is a minority position and should be labelled as such.

**j) APPN (Appian) in Scenario 2 "infrastructure software" is a weak inclusion.** Sub-scale low-code BPM, structurally challenged. If the thesis is model routing and orchestration, the credible names are closer to DDOG, MDB, SNOW or PLTR.

**k) No data layer.** RAG and fine-tuning drive Scenarios 2 and 3, so vector and data platforms (SNOW, MDB) belong on the map. They are missing.

**l) DELL is double-counted** — listed under both "Edge Devices" and "On-Premise Infrastructure" in Scenarios 2 and 3, which visually inflates the breadth of those baskets.

**m) No scenario probabilities.** Three unweighted futures are not investable — you cannot size a position without a probability. The underlying MS note does discuss ROI ranges (e.g. ~45% vs ~30% for Alphabet depending on whether Gemini holds frontier); the carousel drops all of it.

---

## 2. Names that benefit under all three scenarios

### 2.1 As the graphic actually lists them

**Tier A — "Biggest Beneficiary" in all three (9 names):**

`NVDA` · `PANW` · `CRWD` · `OKTA` · `BE` · `INIO` · `SEI` · `WMB` · `LBRT`

**Tier B — present in all three but demoted in at least one (6 names):**

| Ticker | S1 | S2 | S3 |
|---|---|---|---|
| MSFT | Other | Biggest | Biggest |
| AMZN | Biggest | Biggest | Other |
| GOOGL | Biggest | Biggest | Other |
| SAIL | Other | Biggest | Biggest |
| CRWV | Other | Other | Other |
| NBIS | Other | Other | Other |

That is 15 names appearing in all three scenarios.

### 2.2 Which of those are genuinely scenario-invariant

Appearing in all three lists is not the same as being architecturally indifferent. Sorting them honestly:

**Genuinely invariant — the demand driver does not depend on who wins:**
- **NVDA** — compute demand rises in every branch.
- **Security complex: PANW, CRWD, OKTA, SAIL** — attack surface and machine-identity sprawl grow regardless of model licensing.
- **On-site power: BE, SEI, INIO** — electrons are needed wherever the inference physically happens.

**Invariant by construction, not by insight:**
- **WMB, LBRT** — these are in all three because natural gas demand is a macro call, not an AI-architecture call. Their presence makes the "wins everywhere" list look more AI-specific than it is.
- **CRWV, NBIS** — rating the neoclouds identically in all three is a hedge, not a call. Their economics diverge sharply: Scenario 1 means tight GPU supply and pricing power; Scenario 3 means commoditised inference and margin compression. Same rating in both is intellectually lazy.

**The honest all-weather list, corrected for the omissions in Part 1:**

> **NVDA, AVGO, TSM** (compute) · **PANW, CRWD, OKTA** (security) · **BE, SEI, VRT** (power)

AVGO, TSM and VRT are not on Moomoo's graphic and should be.

---

## 3. Top 3 conviction picks per scenario, on current price and forward P/E

### 3.1 The framing that matters most

**The market has already paid for Scenario 3.** 2026 year-to-date performance, live as of 17 Aug 2026:

| Scenario 3 / on-prem basket | YTD | | Scenario 1 / hyperscaler basket | YTD |
|---|---|---|---|---|
| DELL | **+297.3%** | | NVDA | +21.1% |
| BE | **+170.7%** | | AVGO | +14.6% |
| HPE | **+147.3%** | | AMZN | +14.6% |
| AMD *(unlisted)* | **+142.8%** | | AAPL | +12.6% |
| PANW | **+108.3%** | | GOOGL | +11.4% |
| NTAP | +95.3% | | CDW | +2.9% |
| CRWD | +84.5% | | MSFT | +2.4% |
| SNX | +73.2% | | PLTR | −2.3% |
| CSCO | +46.5% | | META | **−10.5%** |
| HPQ | +37.5% | | BABA | **−15.0%** |
| INGM | +34.7% | | | |

Buying the decentralisation names today means paying up for a scenario that has already largely happened in the tape. Highest expected ROI comes from names that are cheap **relative to the scenario in which they win** — which inverts the naive reading of the graphic.

---

### 3.2 Scenario 1 — Closed-Source Wins
*Best risk/reward of the three today, precisely because this is the de-rated basket.*

**1. GOOGL — $348.35 · fwd ~17.5x · +11.4% YTD · 14.8% below 52wk high**
The only company that is simultaneously a frontier model owner (Gemini), a hyperscaler (GCP) and a custom silicon owner (TPU). In a closed-source world that vertical stack is the most complete on earth, and it is priced at roughly 17.5x — below the market multiple. MS's own note frames ROI at ~45% if Gemini holds frontier vs ~30% if it is relegated to infrastructure; a 30% downside case is an unusually high floor. Cleanest asymmetry on the board.

**2. AVGO — $395.70 · fwd ~20.3x · +14.6% YTD · 20.1% below 52wk high**
MS names it the standout Scenario 1 beneficiary, and it is 20% off its high at ~20x forward. The forward multiple has compressed hard (63.7x → 32.9x → 20.3x) as earnings caught up to price — the de-rating happened *while* the business compounded. Custom XPU plus Ethernet fabric. Also the name I argue should be in all three scenarios, which makes it a Scenario 1 pick with free optionality on being wrong about the scenario.

**3. META — $590.20 · fwd ~17.2x · −10.5% YTD · 25.2% below 52wk high**
The contrarian pick. The only mega-cap that is actually *down* in 2026, trading below its own five-year average multiple and at a discount to the S&P. In a closed-source world, frontier capability plus owned distribution to 3bn+ users is the highest-ROI configuration that exists, and MS put Meta in Scenario 1 only — exactly the scenario where it is currently cheapest.

*Higher-beta alternative:* COHR at $333.15, 24.3% off its high, for direct optics leverage.

---

### 3.3 Scenario 2 — Hybrid Models Coexist
*The modal outcome. Favour vendor-agnostic picks-and-shovels on low multiples.*

**1. CDW — $139.42 · fwd ~13.3x · +2.9% YTD · 18.0% below 52wk high**
The standout value in the entire deck. Hybrid *is* the CDW business model: vendor-agnostic sale and integration across on-prem, cloud and edge. It is the only name in the graphic that has completely failed to participate in the 2026 AI trade — down ~40% from last July — while being levered to the single most likely scenario, at the lowest forward multiple on the page. The risk is real and is why it is cheap: gross margin compression and memory-cost pass-through. That is a price problem, not a thesis problem.

**2. CSCO — $111.63 · fwd ~23.5x · +46.5% YTD · 14.4% below 52wk high**
In a hybrid world the network is the connective tissue between public cloud, private DC and edge, and Cisco monetises campus/DC networking plus security (it owns Splunk) in one motion. The relative-value argument is direct: **ANET trades at ~46.9x forward for narrower, more concentrated exposure; Cisco is ~23.5x for a broader hybrid footprint.** Half the multiple for more of the scenario.

**3. NVDA — $225.84 · fwd ~22.6x · +21.1% YTD · 4.5% below 52wk high**
Boring and correct. The one name that wins in all three branches, at roughly a market multiple despite the highest-quality earnings stream in the complex. In hybrid it sells into hyperscalers *and* enterprise on-prem through the DGX/OEM channel. The cheapest way to be right without having to pick the architecture.

*Note:* MSFT is the graphic's headline Scenario 2 name and is defensible at +2.4% YTD, but its size caps the ROI that this question is asking about.

---

### 3.4 Scenario 3 — Open-Weight Models Win
*The crowded trade. Be selective and avoid what has already tripled.*

**1. BABA — $124.60 · −15.0% YTD · 35.3% below 52wk high**
The most mispriced Scenario 3 name. If open weights win, the Chinese open-model labs gain the most relevance — and Alibaba is the only one of the four listed model providers that is liquid and accessible to most investors, *and* is simultaneously a hyperscaler (Alibaba Cloud) that monetises the resulting inference. That last point resolves the contradiction flagged in 1.2e: Alibaba captures value through cloud consumption rather than model licensing, so it does not need pricing power in models to win. It is down 15% YTD and 35% off its high while its scenario has been re-rating everywhere else. **Caveat:** China regulatory and geopolitical risk is precisely why it is cheap — size it as a risk position, not a core holding.

**2. INGM — $28.55 · +34.7% YTD · 9.9% below 52wk high**
The least re-rated name in the Scenario 3 distribution bucket — Ingram Micro is +34.7% against TD Synnex's +73.2% for overlapping exposure. Open-weight and on-prem deployment physically reaches enterprises through distribution and VARs; this is that channel, cheaper and less crowded than SNX (which is ~16x forward on FY26 EPS of ~$15.89). Low-margin business — treat it as beta on the channel, not a compounder.

**3. MSFT — $493.84 · +2.4% YTD · 10.4% below 52wk high**
MS's Scenario 3 upgrade of Microsoft is the best call in the deck and the market has not paid for it. Azure Arc and Azure Local make Microsoft the one hyperscaler that *monetises* the on-prem shift rather than being disintermediated by it, and collapsing inference costs expand Copilot gross margin. The stock is up 2.4% YTD — you are getting the Scenario 3 upgrade for free while holding a Scenario 2 leader.

---

### 3.5 Right scenario, wrong entry — what I would not buy for ROI today

| Name | Price | YTD | Problem |
|---|---|---|---|
| **DELL** | $496.35 | +297.3% | Fwd ~25.2x vs ~21.2x hardware median. Thesis fully in the price, and the market still cannot decide if it is a fat-margin vendor or a thin-margin AI integrator — that debate caps the multiple. |
| **BE** | $235.18 | +170.7% | ~47x forward, 33% off its high after a July short report. Fundamentals genuinely strong; price caught the story. Sub-$200 improves risk/reward materially. |
| **HPE** | $59.05 | +147.3% | Re-rated ahead of delivery. |
| **NTAP** | $207.08 | +95.3% | Within 1% of its 52-week high. No margin of safety. |
| **PANW / CRWD** | $383.76 / $216.22 | +108.3% / +84.5% | Correct all-scenario logic, both within 5% of highs. Right names, wrong entry. |
| **ANET** | $200.38 | +52.9% | ~46.9x forward for exposure CSCO offers at ~23.5x. |

---

## 4. Summary

1. **The map is directionally sound but has real holes.** NVDA-everywhere, power-everywhere and the Microsoft Scenario 3 upgrade are good calls. The omissions of **AVGO from Scenarios 2–3, AMD entirely, TSM entirely and memory entirely** are material, the power basket substitutes gas-supply names (WMB, LBRT) for actual electrical infrastructure (VRT, ETN, GEV), Scenario 3 has no network layer, and `P — "Everpure"` is a printing error for PSTG.

2. **Fifteen names appear in all three scenarios**, but only about nine are genuinely architecture-indifferent: NVDA, PANW, CRWD, OKTA, SAIL, BE, SEI, INIO — plus AVGO and TSM, which should be on the list and are not.

3. **The highest-ROI expression is not the Scenario 3 basket.** That trade has already run (DELL +297%, HPE +147%, BE +171%). The de-rated, better-value exposure sits in the Scenario 1 names — GOOGL at ~17.5x, META at ~17.2x and down on the year, AVGO at ~20.3x and 20% off its high — plus CDW at ~13.3x as the cheapest way to own the most likely scenario of the three.
