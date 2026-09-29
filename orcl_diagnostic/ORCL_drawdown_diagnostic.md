ORCL DRAWDOWN DIAGNOSTIC
========================

VARIABLES
  TICKER          = ORCL
  AS_OF_DATE      = 29/09/2026 (last close 28/09/2026)
  LOOKBACK_START  = 10/09/2025 (closing high $328.33); secondary window 08/09/2026 (local high $162.52)
  LOOKBACK_LABEL  = "since 52w closing high" + "recent leg since 8 Sep 2026"
  PEER_SET        = MSFT, AMZN, GOOGL, CRWV, NVDA, AVGO, SMH, IGV
  BENCHMARKS      = SPX (^GSPC), NDX (^NDX)
  LAST_EARNINGS   = Q1 FY27, released 10/09/2026 after close (8-K filed 10/09/2026; 10-Q filed 11/09/2026) — verified on EDGAR
  HOLDING_CONTEXT = N (IBKR live positions 29/09/2026: no ORCL)
  DECISION_NEEDED = Whether to initiate (Add from zero) / No action

Data: daily closes from Yahoo chart API, cross-checked against IBKR get_price_history (last 5 closes identical:
149.20 / 144.56 / 139.54 / 137.10 / 132.60). All arithmetic in scripts in this folder:
  fetch.py, m0.py, m3_attribution.py, m1_m4_m5.py, m6_event_alloc.py, m7_overlay.py

----------------------------------------------------------------------------------------------------
MODULE 0 — PREMISE VALIDATION
----------------------------------------------------------------------------------------------------
Premise is TRUE. ORCL closed $132.60 on 28/09/2026, -59.6% from its 10/09/2025 closing high of $328.33
(the post-Q1 FY26 +36% day). The cycle low was $114.99 on 24/07/2026 (-65.0%); the stock rebounded +41% to $162.52
on 08/09/2026 and has since fallen -18.4% in 14 sessions. 1D -3.3% | 1W -10.7% | 1M -12.7% | 3M -10.3% | YTD -32.0%
(YE25 $194.91). Over the same YTD window SPX +12.2%, NDX +19.9%, SMH +66.6%, NVDA +23.0%, CRWV +18.8%, IGV -0.2%.

Shape of the moves:
  (a) Gap events: the long drawdown is dominated by earnings/financing gaps. 10 Dec 2025 -10.8%, 11 Jun 2026 -8.5%,
      and the 22–26 Jun 2026 week (10-K plus ATM prospectus) -19%.
  (b) Grind: the recent leg is mostly a grind. Six down days of -1.7% to -3.7% between 14 and 28 Sep, with no single gap
      larger than -5.9%.
  (c) Intraday reversal: on 11 Sep 2026 (the Q1 FY27 reaction) the stock opened +7.5% and closed -1.7% (-8.6% open-to-close).
      The market sold the beat.
Scope is the share price, so Module 8 (OCI outages) was not run.

----------------------------------------------------------------------------------------------------
MODULE 1 — EVENT TIMELINE (close-to-close; Peers = equal-weight of the 8-name peer set)
----------------------------------------------------------------------------------------------------
Date        Event [source tier]                                                        ORCL    SPX    Peers  ORCL-Peers
2025-09-10  Q1 FY26 (9 Sep AMC), RPO $455B -> all-time closing high [T1 IR]             +35.95  +0.30  +3.74  +32.2
2025-10-17  Day after AI World FY30 targets ($225B rev, 30-40% OCI GM) [T2 Yahoo/Barron's]  -6.93  +0.53  -0.48   -6.5
2025-12-11  Q2 FY26: rev/cloud miss; FY26 capex guide +$15B to ~$50B [T2 Investing/Sherwood] -10.83 +0.21  -0.90   -9.9
2026-02-02  Announces $45-50B CY26 debt+equity raise incl. ATM [T2 CNBC 2 Feb]            -2.75  +0.54  -0.71   -2.0
2026-02-05  Week -15.8%: CDS elevated, OpenAI exposure, UBS/RBC PT cuts [T2 Yahoo/Fool]    -6.95  -1.23  -3.14   -3.8
2026-03-11  Q3 FY26 "best quarter in 15 yrs"; TTM FCF -$24.7B [T2 Fortune 10 Mar]         +9.18  -0.08  +1.30   +7.9
2026-05-29  Wedbush PT $275; $30B US govt cloud deal [T3 lead -> T2 Fool]                 +10.84 +0.22  +1.70   +9.1
2026-06-05  AVGO AI guide disappoints; Hold downgrade 2 Jun [T2 Yahoo/StockStory]         -9.59  -2.64  -5.16   -4.4
2026-06-11  Q4 FY26: FY27 capex $90-95B gross/$70B net, $40B raise incl $20B ATM [T1 8-K 10 Jun; T2 CNBC] -8.53 +1.75 +1.51 -10.0
2026-06-22  10-K: $260B uncommenced DC leases, headcount -13% [T1 10-K]                    -5.00  -0.37  -3.08   -1.9
2026-06-23  ATM prospectus 424B5 / ATM amendment [T1 EDGAR]; worst week since 2001 [T2 CNBC 26 Jun] -5.66 -1.44 -2.23 -3.4
2026-07-09  S&P cuts to BBB-/stable; OpenAI named key credit risk [T1 S&P, via T2 heise/Yahoo]  +2.65 +0.81 +0.88 +1.8
2026-07-24  Cycle low $114.99                                                               -4.21  +0.05  -2.15   -2.1
2026-07-30  Gemini on OCI; MSFT Azure >$100B run-rate (29 Jul) [T2 Fool 7 Aug]             +8.34  +1.66  +6.91   +1.4
2026-09-01  Global bond selloff, UST30Y near 20y high [T2 Fool 1 Sep]                      -5.23  -0.71  -1.89   -3.3
2026-09-10  Q1 FY27 day-of (release AMC) [T1 8-K]                                          -5.38  -0.58  -1.48   -3.9
2026-09-11  Q1 FY27 reaction: beat/raise, RPO $664B, FCF -$5.4B [T1 8-K/10-Q]             -1.74  +0.86  +0.79   -2.5
2026-09-14  Ellison cancels 10b5-1 sale (PR 12 Sep, 8-K 14 Sep) [T1]; AI-regulation + Fed-hike fears [T2 Fool] -3.65 -0.48 -1.33 -2.3
2026-09-17  Relief bounce                                                                   +5.19  +1.14  +1.15   +4.0
2026-09-23  No discrete catalyst                                                            -3.11  -0.75  -1.15   -2.0
2026-09-24  Bloomberg: force-majeure notice to Blue Owl on Project Jupiter (NM); CDS record ~227bp [T2 Bloomberg/CNBC/DCD; CDS level T3 SA] -3.47 -0.02 +0.23 -3.7
2026-09-25  Follow-through                                                                  -1.75  +0.51  +0.28   -2.0
2026-09-28  Reports of new layoff round (T3 only, not verified in T1/T2)                   -3.28  -0.77  -0.85   -2.4

Date conflict adjudicated: erp.today (T3) gives Q1 FY27 as 11 Sep. The EDGAR 8-K was filed 10 Sep and SpotGamma/the
call transcript put the release at 10 Sep AMC. Adopted: 10 Sep release, 11 Sep reaction.
Quote conflict adjudicated: MLQ (T3) has 11 Jun "fell 9.3% to $182.64". The official close is $184.10 (-8.5%); the $182.64 is
likely an intraday print. Close used.

----------------------------------------------------------------------------------------------------
MODULE 2 — CAUSE HYPOTHESES
----------------------------------------------------------------------------------------------------
 1 Capex & FCF stress ............ CONFIRMED. Q1 FY27 capex $28.5B = 147% of revenue; FCF -$5.4B; TTM FCF -$28.7B.
                                   Headline OCF (+184%) includes $11.4B of customer prepayments with a significant
                                   financing component. FCF excluding them was -$16.8B in one quarter. FY27 capex $90-95B gross /
                                   <=$70B net (T1 10-Q, call).
 2 Balance sheet / credit ........ CONFIRMED. Debt $125.3B, net $88.3B; +$34.6B on-BS op leases; +$288B uncommenced
                                   DC leases (+$28B QoQ; 0.72x market cap). S&P BBB- (one notch above HY), Moody's Baa2
                                   negative. 5y CDS record ~227bp on 24 Sep vs IG index ~53bp (T3 SA, consistent with T2
                                   Yahoo "200bp"). Equity is trading as a credit story. Interest coverage is NOT deteriorating yet:
                                   GAAP EBIT/interest 4.7x vs 4.6x a year ago.
 3 Customer concentration ........ CONFIRMED (as a priced risk; no realized default). ~half of RPO is tied to OpenAI
                                   (S&P via T2; erp.today). The 10-Q gives no customer %, and the 10-K says "no single customer >=10% of revenue"
                                   (true today, not for backlog). No renegotiation signal found.
 4 RPO quality ................... PARTIAL. Only 13% of $664B ($86B) converts in 12 months. $75B+ is prepaid/BYO-hardware
                                   (better quality). Conversion depends on capacity delivery (see 6).
 5 Margin compression ............ PARTIAL. Cloud & software segment margin 54.5% vs 59.6% a year ago (-5.1pp); depreciation +134%.
                                   Non-GAAP op margin held at 42%. Mgmt guides gross margin to "flatten" after the ramp.
 6 Execution / delivery .......... CONFIRMED (new, recent). Q1 delivered 850MW and Abilene is 75% done (positive). On 10 Sep
                                   mgmt called New Mexico "on track". On 24 Sep a force-majeure notice on the same site was reported (gas
                                   pipeline slipped to 1 Feb 2027; hell-or-high-water lease). This is a credibility gap. Mgmt says there is no FY27 impact.
 7 Guidance / expectations reset . PARTIAL. No guide-down: FY27 revenue raised to >=$90B, EPS $8.10. The 11 Sep reaction
                                   (-1.7% vs ±11.5% implied) shows the print was not the shock. The reset happened at Q2 FY26 (Dec) and
                                   Q4 FY26 (Jun) on capex/funding, not on demand.
 8 Positioning unwind ............ PARTIAL. The ~29% "post-hype unwind" of the +36% Sep-2025 spike is a positioning effect.
                                   Pre-print call skew (SpotGamma) was followed by a sold gap. Short interest is low (~1.5-2.8% of float, T3). The
                                   13F data is too thin to judge (T3).
 9 Sector / regime rotation ...... PARTIAL (minor). Beta-adjusted, the AI-infra basket ex-market explains 9-26% of the full
                                   drawdown and 0-41% of the recent leg (depending on beta window). NDX was a TAILWIND in both windows.
10 Legacy software pressure ...... PARTIAL. IGV ex-market explains 22-35% of the full drawdown. Software revenue -3%.
11 Macro / rates ................. PARTIAL (minor). UST10Y rose 4.03% -> 5.24% since the peak and 4.81 -> 5.24 in the recent leg. The rate
                                   coefficient beyond NDX beta is small (-0.05% per +10bp). 1 Sep was a rates day (-5.2%).
12 Index / flow effects .......... CONFIRMED (supply). The $20B ATM was fully used in Jun-Aug: 141M shares, +5.0% share count
                                   in one quarter, ~6.9% of ADV, average price $141.20 vs quarter VWAP ~$153. No buyback offset.

----------------------------------------------------------------------------------------------------
MODULE 3 — RETURN ATTRIBUTION (log-return factor model: NDX + AI-infra[CRWV,NVDA,AVGO,SMH] ex-mkt + IGV ex-mkt)
----------------------------------------------------------------------------------------------------
Window                                   ORCL     NDX    AI-infra  IGV    | market  AI-infra  software  IDIOSYNCRATIC
A. Peak 10-Sep-25 -> 28-Sep-26 (pre β)   -59.2%  +27.0%  +15.7%   -6.0%  |  -33%     +9%      +35%       +88%
A. same, in-window β                                                      |  -38%    +24%      +25%       +89%
A. same, CRWV as sector factor                                            |  -38%    +26%      +22%       +90%
B. Jun-1 high -> 28-Sep                  -46.4%   -0.8%  -14.9%   -2.1%  |   +2%    +17%       +2%       +79%
C. Sep-8 high -> 28-Sep (pre β)          -18.4%   +2.6%   -3.7%   +2.7%  |  -18%    +41%       -3%       +80%
C. same, in-window β                                                      |  -22%     -2%       +1%      +122%
(negative % = factor offset the drawdown; R² of daily fit 0.47-0.57)

Conclusion: 80-90% of the drawdown is ORCL-specific in every specification. The market rose while ORCL fell.

Top-5 worst days, full window (residual = idiosyncratic):
  2025-12-11  -10.8%  resid -10.6  Q2 FY26 capex raise + revenue miss
  2026-06-05   -9.6%  resid  -3.3  AVGO spillover (mostly sector: AI-infra -7.6%)
  2026-06-11   -8.5%  resid  -8.8  Q4 FY26 capex $90-95B + $40B raise (NDX +3.3% that day)
  2026-02-05   -7.0%  resid  -1.5  CDS/OpenAI week (largely sector-driven that day)
  2025-10-17   -6.9%  resid  -6.0  sell-the-news after FY30 targets
Top-5 worst days, recent leg:
  2026-09-10  -5.4%  resid -3.8  pre-print risk-off
  2026-09-14  -3.7%  resid -1.8  AI-regulation/Fed fears; AI basket -4.9%
  2026-09-24  -3.5%  resid -3.7  Project Jupiter force majeure; CDS record (peers +0.2%)
  2026-09-28  -3.3%  resid -1.5  layoff reports; NDX -1.1%
  2026-09-23  -3.1%  resid -1.5  no discrete catalyst

Recent-leg bucket split (share of idiosyncratic): earnings window 18% | 14-22 Sep 18% | Jupiter/CDS/layoffs 23-28 Sep 64%.

Earnings realized vs implied:
  Dec-25 -10.8% (implied n/a) | Mar-26 +9.2% | Jun-26 -8.5% vs ±12% implied | Sep-26 -1.7% vs ±11.5% implied (SpotGamma, T2/T3)
  The Sep print came in well inside implied, so the recent weakness is NOT an earnings shock.

Rolling 20D correlation, latest: 0.63 to AI-infra basket, 0.64 to NDX, 0.49 to CRWV (range over 12m 0.4-0.8). ORCL still
co-moves daily with the AI trade, but its drift is its own.

Full-window idiosyncratic residual allocated to event days (m6_event_alloc.py):
  Capex/FCF/funding & dilution (12 days) ............ ~51% of total drawdown
  Post-hype unwind of Sep-2025 spike (Sep-Oct 25) ... ~29%
  Credit/counterparty/execution (11 days) ........... ~18%
  May-Jun 2026 squeeze (net positive) ............... ~-10%
  Residual non-event grind .......................... ~0%

----------------------------------------------------------------------------------------------------
MODULE 4 — FUNDAMENTAL QUALITY SCORECARD (Q1 FY27 vs Q1 FY26 unless noted; T1 8-K/10-Q)
----------------------------------------------------------------------------------------------------
Metric                              Latest            Prior             Trend   RAG
Revenue growth                      +30% ($19.3B)     $14.9B yr-ago     up      G
OCI (IaaS) growth                   +121% ($7.4B)     FY26 +93%         up      G
Software (license/support)          -3% ($5.5B)       n/v               down    A
Non-GAAP op margin                  42%               ~42% (mgmt: flat) flat    G
Cloud&software segment margin       54.5%             59.6%             down    A
GAAP vs non-GAAP                    GAAP EPS $1.56 / NG $1.92; SBC $1.13B (5.8% rev); restructuring $94M (plan
                                    raised to $2.8B). FY26 GAAP included a $2.7B Ampere gain (one-off).       A
Capex                               $28.5B (147% rev) $8.5B             up      R
OCF                                 $23.1B            $8.1B             up*     A  (*$11.4B customer prepayments)
FCF / FCF ex-prepay                 -$5.4B / -$16.8B  -$0.4B            down    R
TTM FCF                             -$28.7B           FY26 -$23.7B      down    R
Gross debt / net debt               $125.3B / $88.3B  ~$85B LTD 1y ago  up      R
Uncommenced DC leases               $288B             $260B (May-26)    up      R
EBIT / interest                     4.7x              4.6x              flat    A
Interest expense                    $1.43B (+55%)     $0.92B            up      A
Credit rating                       BBB- (S&P) / Baa2 neg (Moody's)    BBB     down    R
RPO / next-12m                      $664B / $86B (13%) $638B / 12% (May) up     G
RPO concentration                   ~50% OpenAI (T2)  —                 —       R
Share count                         3,024M            2,880M (May-26)   +5.0%   R
Guidance vs consensus               FY27 rev >=$90B (raised), EPS $8.10; Q2 rev +30-34%; capex unchanged  G
Valuation                           16.4x FY27 NG EPS at $132.60        compressed

Read: the operating business is Green/Amber and the funding stack is Red. This is a financing-model problem, not a demand problem.

----------------------------------------------------------------------------------------------------
MODULE 5 — MARKET-IMPLIED READ
----------------------------------------------------------------------------------------------------
Options (IBKR, 29/09/2026 snapshot): ATM IV 51.8% vs 30D HV 57.9% (20D realized 52.1%); IV 52w percentile 0.32.
  Nov-20 skew is flat to slightly call-rich: 110P 52.5% | 120P 51.8% | 130P 52.1% | 135C 52.2% | 145C 52.8% | 155C 54.6%.
  Largest nearby OI is the 120P (12.1k). Put/call volume today is 0.38, below average. No crash hedging and no capitulation premium.
Credit: 5y CDS at a record ~227bp (24 Sep, T3 Seeking Alpha; T2 Yahoo cites ~200bp), about 4x the IG index. On 24 Sep CDS
  widened while CRWV rose +3.7%, so credit is leading equity and the move is ORCL-specific.
Ownership: short interest is low (1.5-2.8% of float, T3), so a squeeze is not the setup and shorts are not driving this.
  The Q2-26 13F data is inconclusive (T3 only).
Sell-side: consensus is still Buy (~32 analysts, T3). Barclays OW, PT $252 (Sep). Scotiabank cut to $215 before the print; Wedbush
  cut $275 -> $240 (T3 aggregations; not individually verified at T1/T2).

Agreement / divergence: fundamentals and credit AGREE that funding and counterparty risk is the issue. Options DIVERGE:
  they show no stress premium, and IV sits below realized. Sell-side DIVERGES and stays bullish on backlog. The credit market is
  the most informed signal here, and it points down.

----------------------------------------------------------------------------------------------------
MODULE 6 — VERDICT
----------------------------------------------------------------------------------------------------
VERDICT: D — Mixed. About 65% B (thesis intact, expectations and financing-cost reset) and about 35% A-risk (funding and
         counterparty impairment building but not realized). It is not C: market and sector explain only 10-20%.
LEAN: No action (do not initiate). CONFIDENCE: 65% (diagnosis confidence ~75%)
TOP 3 CAUSES (ranked, % of the -59.6% drawdown, log basis):
  1. Capex/FCF/funding & dilution: ~50% (confidence: high)
  2. Unwind of the Sep-2025 +36% spike / positioning: ~30% (medium)
  3. Credit, counterparty & execution (CDS, S&P BBB-, OpenAI ~50% of RPO, Jupiter force majeure): ~18% (high), and
     it is 64% of the idiosyncratic move in the last two weeks
  Sector (software, AI-infra ex-mkt) adds ~30-45%, and a rising market offsets ~-35%.
WHAT WOULD CHANGE MY MIND:
  To Add: CDS back below ~150bp with equity stable; Q2 FY27 net capex tracking <=$70B/yr with no new equity program;
          disclosure that non-OpenAI RPO is >50% and growing; Jupiter power resolved or the force majeure withdrawn.
  To A (thesis-breaking): Moody's downgrade to Baa3 or S&P outlook to negative (junk risk); any OpenAI contract
          delay or renegotiation; a new ATM or equity raise beyond the $20B; force majeure spreading to another site
          (e.g., Wisconsin); an FY27 revenue guide cut.
NEXT CATALYSTS:
  09/10/2026 — Dividend record date (non-event; Oct 23 payment)
  14/11/2026 — Q3-CY26 13F filing deadline (institutional positioning read)
  18/11/2026 — Annual Meeting, virtual (DEF 14A filed 25/09/2026, T1)
  ~mid-Dec 2026 — Q2 FY27 earnings (date not yet set by Oracle IR; last year 10/12/2025)
  01/02/2027 — Energy Transfer pipeline in-service target for Project Jupiter power
  Unscheduled — Moody's review; any new 424B5 (equity/debt) on EDGAR; OpenAI financing headlines
Observable triggers: CDS 5y (227bp record); $114.99 cycle low; $120 put-OI cluster; EDGAR 424B5/8-K filings.

----------------------------------------------------------------------------------------------------
MODULE 7 — PORTFOLIO OVERLAY (formally N/A: no ORCL held; run for the "Add" question)
----------------------------------------------------------------------------------------------------
Live IBKR (29/09/2026): NLV $42,160; cash $313 (0.74% of NLV). 98.4% of NLV is semis/AI-infra (AMAT 30.9%, SOXX 15.8%,
MU 14.9%, ARM 8.7%, QCOM 6.7%, AVGO 6.6%, LRCX 5.9%, VRT 5.8%, BE 3.1%). ORCL correlation to the book: 0.40 (1y), 0.53 (60d).
Any ORCL entry would need a trim to fund it (no cash buffer). That trim would add the same AI-capex factor the book already
holds 9 times over, with a credit tail on top. Funding an entry would require running the portfolio-reallocation-discipline
skill first. No trim is proposed here.

----------------------------------------------------------------------------------------------------
SOURCES
----------------------------------------------------------------------------------------------------
T1: Oracle Q1 FY27 8-K ex99.1 (10/09/2026) https://www.sec.gov/Archives/edgar/data/0001341439/000119312526387905/orcl-ex99_1.htm
T1: Oracle 10-Q Q1 FY27 (11/09/2026) https://www.sec.gov/Archives/edgar/data/0001341439/000119312526389274/orcl-20260831.htm
T1: Oracle 10-K FY26 (22/06/2026) https://www.sec.gov/Archives/edgar/data/0001341439/000119312526277521/orcl-20260531.htm
T1: Oracle 8-K Ellison 10b5-1 cancellation (14/09/2026) https://www.sec.gov/Archives/edgar/data/1341439/000119312526389753/d20034dex991.htm
T1: Oracle DEF 14A (25/09/2026) https://www.sec.gov/Archives/edgar/data/1341439/000119312526402816/0001193125-26-402816-index.htm
T1: Form 144s 16/09 & 22/09/2026 (RSU vesting sales, $1.5M and $0.4M, immaterial)
T1: S&P "Oracle Corp. Downgraded To 'BBB-/A-3'" https://www.spglobal.com/ratings/en/regulatory/article/-/view/sourceId/101695609 (403; content via T2)
T2: Bloomberg 24/09/2026 https://www.bloomberg.com/news/articles/2026-09-24/oracle-cites-force-majeure-to-shield-itself-on-controversial-data-center
T2: CNBC 24/09/2026 https://www.cnbc.com/2026/09/24/oracle-data-center-force-majeure.html
T2: DCD https://www.datacenterdynamics.com/en/news/oracle-issues-force-majeure-notice-to-blue-owl-following-series-of-setbacks-at-project-jupiter-data-center-campus-report/
T2: CNBC 11/06/2026 https://www.cnbc.com/2026/06/11/oracle-shares-tumble-11percent-on-increased-capital-raise-cash-concerns.html
T2: CNBC 26/06/2026 https://www.cnbc.com/2026/06/26/oracle-stock-ends-worst-week-since-2001-as-investors-dwell-on-finances.html
T2: CNBC 10/09/2026 options preview https://www.cnbc.com/2026/09/10/oracle-options-are-doing-something-curious-heading-into-earnings.html
T2: Motley Fool Q1 FY27 transcript https://www.fool.com/earnings/call-transcripts/2026/09/11/oracle-orcl-q1-2027-earnings-call-transcript/
T2: Motley Fool 01/09/2026 https://www.fool.com/investing/2026/09/01/why-is-oracle-stock-down-today/
T2: Yahoo/Motley Fool 14/09/2026 https://finance.yahoo.com/markets/stocks/articles/why-oracle-stock-fell-quickly-153800455.html
T2: Motley Fool 07/08/2026 https://www.fool.com/investing/2026/08/07/oracle-surges-whats-driving-the-sudden-rally/
T2: Investing.com Q2 FY26 https://www.investing.com/news/earnings/oracle-slumps-in-afterhours-trading-as-q2-revenue-miss-estimates-on-software-drag-4401847
T2/T3: SpotGamma implied move https://spotgamma.com/oracle-earnings-preview-ai-backlog-options-implied-move/
T3 (lead only): Seeking Alpha CDS record https://seekingalpha.com/news/4646794-oracle-credit-default-swaps-hit-new-record-high-as-ai-debt-worries-mount
T3: erp.today, 247wallst, timothysykes, cryptonomist, tradingkey, mlq.ai, marketbeat (leads; key facts re-verified above where marked)
Market data: IBKR (snapshot, history, option chain, positions); Yahoo chart API (daily closes, cross-checked with IBKR)
