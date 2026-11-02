"""M1/M9 PRE: Senate seat-count Monte Carlo (S5 proxy), personal-book election-week risk, client worst-of FCN Monte Carlo.
Inputs: Kalshi state odds, IBKR live snapshot, ACEL Live Book, CBOE implied vols, Yahoo histories. All maths here."""
import json, sys, re, numpy as np, pandas as pd
sys.path.insert(0, 'src'); from common import load
from scipy.stats import norm
OUT = __import__('pathlib').Path('out'); rng = np.random.default_rng(20261103)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40); pd.set_option('display.max_rows', 300)
USDMYR = 4.0695
# ======================= 1. Senate seat-count MC =======================
ks = json.load(open('data/raw/odds/kalshi_senate_states.json'))
pD = {}
for st, (tk, mk) in ks.items():
    tot = sum(v for v in mk.values() if v)
    dem = {'AK': 'Democratic party', 'ME': 'Troy Jackson', 'NC': 'Roy Cooper', 'TX': 'James Talarico', 'IA': 'Josh Turek', 'KS': 'Adam Hamilton', 'MI': 'Abdul El-Sayed',
           'MN': 'Peggy Flanagan', 'NH': 'Chris Pappas', 'GA': 'Jon Ossoff', 'SC': 'Annie Andrews', 'MS': 'Scott Colom', 'MT': 'Seth Bodnar', 'NE': None, 'AL': 'Everett Wess',
           'AR': 'Hallie Shoffner', 'CO': 'John Hickenlooper', 'DE': 'Chris Coons', 'ID': 'David Roth', 'IL': 'Juliana Stratton', 'LA': 'Charles Booker', 'MA': 'Ed Markey',
           'NJ': 'Cory Booker', 'NM': 'Ben Ray Luján', 'OK': 'N’Kiyla Thomas', 'OR': 'Jeff Merkley', 'RI': 'Jack Reed', 'SD': 'Julian Beaudion', 'TN': 'Marquita Bradshaw',
           'VA': 'Mark Warner', 'WV': 'Rachel Fetty Anderson', 'WY': 'James Byrd'}[st]
    pD[st] = (mk.get(dem, 0) or 0) / tot if dem else 0.0   # NE: Osborn (I) pledged no caucus -> not counted as D for control
pD.update({'OH': 0.71, 'FL': 0.14, 'KY': 0.03})  # Kalshi/PM OH-S Brown 0.70-0.725; FL-S Nixon 0.14; KY no market found -> 0.03 assumed
D_NOT_UP = 34
states = sorted(pD); p = np.array([pD[s] for s in states]); z = norm.ppf(np.clip(p, 1e-4, 1 - 1e-4))
sen = {}
for rho in (0.0, 0.3, 0.5):
    N = 200000; g = rng.standard_normal((N, 1)); e = rng.standard_normal((N, len(p)))
    win = (np.sqrt(rho) * g + np.sqrt(1 - rho) * e) < z  # marginal P(win)=p
    seats = D_NOT_UP + win.sum(1); ctrl = seats >= 51
    piv = {}
    for s in ('AK', 'ME'):
        i = states.index(s); piv[s] = ((seats == 51) & win[:, i]) | ((seats == 50) & ~win[:, i])
    late = piv['AK'] | piv['ME']
    sen[rho] = dict(E_seats=seats.mean(), P_D51=ctrl.mean(), P_50=(seats == 50).mean(), P_51=(seats == 51).mean(), P_pivot_AK_or_ME=late.mean())
    print(f"Senate MC rho={rho}: E[D seats] {seats.mean():.1f} | P(D>=51) {ctrl.mean():.3f} | P(50) {(seats == 50).mean():.3f} P(51) {(seats == 51).mean():.3f} | P(control pivots on AK or ME RCV count) {late.mean():.3f}")
order = sorted(states, key=lambda s: -abs(0.5 - pD[s]) * -1)
print('Closest races (D prob):', {s: round(pD[s], 3) for s in sorted(states, key=lambda s: abs(pD[s] - 0.5))[:10]})
# ======================= 2. Personal book =======================
L = json.load(open('data/raw/ibkr_live_20261102.json')); nlv = L['nlv_usd']
mv = pd.read_csv(OUT / 'm7_implied_moves.csv').set_index('sym')
iren = pd.read_csv('data/raw/cboe/IREN.csv.gz', parse_dates=['exp']); c22 = iren[(iren.exp == '2027-01-15') & (iren.cp == 'C') & (iren.k == 22)].iloc[0]
rows = []
for q in L['positions']:
    w = q['mv'] / nlv; under = q['under']
    if q['sym'] == 'IREN 15JAN27 22C':
        S = mv.loc['IREN', 'spot']; dl = c22.delta; notional = q['qty'] * 100 * dl * S
        wk = mv.loc['IREN', 'wk_move_0611']; risk = notional * wk; iv3 = mv.loc['IREN', 'iv_3m']; eff = notional
    elif under is None:
        risk, wk, eff, iv3 = 0.0, np.nan, 0.0, np.nan
    else:
        lev = q['lev']; wk = mv.loc[under, 'wk_move_0611'] * lev; eff = q['mv'] * lev; risk = q['mv'] * wk; iv3 = mv.loc[under, 'iv_3m']
    decay1m = decay3m = np.nan
    if q.get('lev') and q['lev'] > 1:
        Lv = q['lev']; s2 = mv.loc[under, 'iv_3m'] ** 2
        decay1m = np.exp(-(Lv * Lv - Lv) / 2 * s2 * (1 / 12)) - 1; decay3m = np.exp(-(Lv * Lv - Lv) / 2 * s2 * 0.25) - 1
    rows.append(dict(pos=q['sym'], mv_usd=q['mv'], mv_myr=q['mv'] * USDMYR, pct_nlv=w, eff_exposure_usd=eff, eff_x_nlv=eff / nlv, wk_implied_move=wk,
                     event_risk_usd=risk, event_risk_myr=risk * USDMYR, unreal_pct=(q['px'] / q['avg'] - 1) if q['avg'] else np.nan,
                     vol_drag_1m=decay1m, vol_drag_3m=decay3m, flag='CONCENTRATION' if w > 0.10 else ''))
P = pd.DataFrame(rows); P.to_csv(OUT / 'm9_personal.csv', index=False)
print(f"\nPERSONAL (IBKR live 02/11 17:23 MYT; NLV US${nlv:,.0f} = RM{nlv * USDMYR:,.0f}; cash US${L['cash_usd']:,.0f} = {L['cash_usd'] / nlv:.2%} NLV; USD/MYR {USDMYR})")
print(P.to_string(index=False, float_format=lambda v: f'{v:,.4f}'))
print(f"Book effective semis exposure {P.eff_exposure_usd.sum():,.0f} USD = {P.eff_exposure_usd.sum() / nlv:.2f}x NLV | election-week expected abs move (sum, ~perfect corr) US${P.event_risk_usd.sum():,.0f} = RM{P.event_risk_usd.sum() * USDMYR:,.0f} = {P.event_risk_usd.sum() / nlv:.1%} NLV")
for nm, shock in [('2018 replay (SPX -14.7%, 06/11-24/12/2018)', -0.1467), ('1987 replay (SPX -33.5% peak-trough 25/08-19/10/1987)', -0.335)]:
    beta_semis = 2.0; loss = sum(min(r.eff_exposure_usd, 1e12) * max(beta_semis * shock, -0.95) for r in P.itertuples() if r.eff_exposure_usd > 0)
    print(f"   stress {nm}: semis beta 2.0 -> book P&L US${loss:,.0f} ({loss / nlv:.0%} NLV; linear, ignores daily-reset path effects)")
# ======================= 3. Client book Monte Carlo =======================
lb = pd.read_csv('data/clean/livebook.csv', dtype=str).fillna('')
num = lambda x: float(re.sub(r'[^0-9.\-]', '', x)) if re.sub(r'[^0-9.\-]', '', x) not in ('', '-', '.') else np.nan
pct = lambda x: num(x) / 100
live = lb[lb.Status == 'Live']; legs = live[live.Ticker != '']; cl = live[live.Ticker == '']
YMAP = {'AMAT UW': 'AMAT', 'INTC UW': 'INTC', 'ARM UW': 'ARM', 'AVGO UW': 'AVGO', 'NVDA UW': 'NVDA', 'MU UW': 'MU', 'SNDK UW': 'SNDK', 'SKHY UW': 'SKHY', 'MRVL UW': 'MRVL',
        'GOOGL UW': 'GOOGL', 'AMZN UW': 'AMZN', 'ASML UW': 'ASML', 'AMD UW': 'AMD', 'WDC UW': 'WDC', 'QCOM UW': 'QCOM', 'MSFT UW': 'MSFT', '3690 HK': 'HK3690',
        '9618 HK': 'HK9618', '9988 HK': 'HK9988', '9888 HK': 'HK9888', '2382 HK': 'HK2382', '1810 HK': 'HK1810', 'WBC AT': 'WBC', 'CBA AT': 'CBA'}
IVPROXY = {'HK9988': ('BABA', 1.0), 'HK9618': ('JD', 1.0), 'HK9888': ('BIDU', 1.0)}
spx = load('SPX'); spxr = np.log(spx).diff()
def series(t): return load(YMAP[t])
info = {}
for t in legs.Ticker.unique():
    s = series(t); lr = np.log(s).diff().dropna(); a = YMAP[t]
    if a in mv.index and not np.isnan(mv.loc[a, 'iv_3m']): iv, src = mv.loc[a, 'iv_3m'], 'CBOE 3M ATM'
    elif a in IVPROXY: iv, src = mv.loc[IVPROXY[a][0], 'iv_3m'], f'CBOE 3M ATM of US ADR {IVPROXY[a][0]}'
    else: iv, src = lr[-63:].std() * np.sqrt(252) * 1.1, 'realised 63d x1.1 (no listed options)'
    if t.endswith('UW'):
        x = pd.concat([lr, spxr], axis=1, join='inner').dropna()[-252:]; b = np.cov(x.iloc[:, 0], x.iloc[:, 1])[0, 1] / x.iloc[:, 1].var()
    else:
        wk = pd.concat([np.log(s).resample('W-FRI').last().diff(), np.log(spx).resample('W-FRI').last().diff()], axis=1).dropna()[-104:]
        b = np.cov(wk.iloc[:, 0], wk.iloc[:, 1])[0, 1] / wk.iloc[:, 1].var()
    info[t] = dict(iv=iv, iv_src=src, beta=b, beta_adj=0.67 * b + 0.33, last=s.iloc[-1], last_date=s.index[-1].date(),
                   wk_move=(mv.loc[a, 'wk_move_0611'] if a in mv.index else (mv.loc[IVPROXY[a][0], 'wk_move_0611'] if a in IVPROXY else iv * np.sqrt(5 / 252) * 0.8)))
INFO = pd.DataFrame(info).T; INFO.to_csv(OUT / 'm9_underlying_inputs.csv')
print('\nUnderlying inputs (vol, beta to SPX, election-week move):'); print(INFO.to_string(float_format=lambda v: f'{v:.4f}' if isinstance(v, float) else v))
SCN = {'bear': np.log(0.80), 'base': np.log(1.06), 'bull': np.log(1.15)}  # 12M SPX log drift; underlying drift = beta_adj x this
US_HOL = ['2026-11-26', '2026-12-25', '2027-01-01', '2027-01-18', '2027-02-15', '2027-03-26', '2027-05-31', '2027-06-18', '2027-07-05', '2027-09-06', '2027-11-25']
def tdays(d0, d1): return max(np.busday_count(d0, d1, holidays=US_HOL), 0)
def monthly_obs(nxt, fv):
    out = []; d = nxt; k = 0
    while d <= fv:
        out.append(d); k += 1; d = (nxt + pd.DateOffset(months=k))
        while d.weekday() >= 5: d += pd.Timedelta(days=1)
    if out[-1] != fv: out.append(fv)
    return out
NPATH = 20000; deal_rows = []; leg_rows = []
for deal, g in legs.groupby('Deal'):
    g = g.reset_index(drop=True); c = cl[cl.Deal == deal]
    prin_myr = c.Principal_MYR.map(num).sum(); clients = '; '.join(f"{r.Client.title()} ({r.Ccy} {r.Principal})" for r in c.itertuples())
    KO, KI, STK = pct(g.KO[0]), pct(g.KI[0]), pct(g.Strike[0])
    nxt, fv = pd.to_datetime(g.NextKO[0], format='%d-%b-%y'), pd.to_datetime(g.FinalVal[0], format='%d-%b-%y')
    tick = list(g.Ticker); init = np.array([num(x) for x in g.InitPx]); reg0 = np.array(['Registered' in x for x in g.KOStatus])
    S0 = np.array([info[t]['last'] for t in tick]); d0 = max(info[t]['last_date'] for t in tick)
    obs = monthly_obs(nxt, fv); T = np.array([tdays(np.datetime64(d0), np.datetime64(o.date())) for o in obs]) / 252.0
    sig = np.array([info[t]['iv'] for t in tick]); bet = np.array([info[t]['beta_adj'] for t in tick])
    lr = pd.concat([np.log(series(t)).diff().rename(t) for t in tick], axis=1).dropna()[-252:]
    C = lr.corr().values if len(lr) > 40 else np.full((len(tick), len(tick)), 0.6) + 0.4 * np.eye(len(tick))
    for i, t in enumerate(tick):
        kipx, kopx = init[i] * KI, init[i] * KO
        d_ki = 1 - kipx / S0[i]; m3 = sig[i] * 0.5; wk = info[t]['wk_move']
        flag = 'RED' if d_ki <= 1.0 * m3 else ('AMBER' if d_ki <= 1.5 * m3 else 'GREEN')
        leg_rows.append(dict(deal=deal, ccy=g.Ccy[0], ticker=t, pct_init=S0[i] / init[i], ki_pct=KI, ki_dist=d_ki, ko_dist=kopx / S0[i] - 1, registered=reg0[i],
                             wk_move=wk, ki_dist_x_wk=d_ki / wk if wk else np.nan, move3m_1sd=m3, ki_dist_x_3m=d_ki / m3, flag=flag, next_obs=nxt.date(), fv=fv.date(), prin_myr=prin_myr))
    res = {}
    for cname, Cm in (('hist', C), ('stress', 0.7 * C + 0.3 * np.eye(len(tick)))):
        w_, V = np.linalg.eigh(Cm); Cm = (V * np.clip(w_, 1e-6, None)) @ V.T; Lc = np.linalg.cholesky(Cm)
        for sname, mu_spx in SCN.items():
            mu = bet * mu_spx; dT = np.diff(np.r_[0.0, T])
            Z = rng.standard_normal((NPATH, len(T), len(tick))) @ Lc.T
            lnS = np.log(S0 / init) + np.cumsum(mu * dT[:, None] + sig * np.sqrt(dT)[:, None] * Z, axis=1)  # log perf vs initial
            perf = np.exp(lnS); reg = np.repeat(reg0[None, :], NPATH, 0); alive = np.ones(NPATH, bool); ko_first = np.zeros(NPATH, bool)
            for k in range(len(T)):
                reg = reg | (perf[:, k, :] >= KO); ko_now = alive & reg.all(1)
                if k == 0: ko_first = ko_now.copy()
                alive &= ~ko_now
            worst = perf[:, -1, :].min(1); ki = alive & (worst < KI); loss = np.where(ki, np.clip(1 - worst / STK, 0, 1), 0)
            res[(cname, sname)] = dict(p_ko_next=ko_first.mean(), p_ko_life=1 - alive.mean(), p_ki=ki.mean(), el=loss.mean(), lgd=(loss[ki].mean() if ki.any() else 0))
    worst_now = (S0 / init).min()
    deal_rows.append(dict(deal=deal, ccy=g.Ccy[0], legs='/'.join(t.split()[0] for t in tick), worst_now=worst_now, KI=KI, KO=KO, strike=STK, next_obs=nxt.date(), fv=fv.date(),
                          days_to_fv=(fv - pd.Timestamp('2026-11-02')).days, prin_myr=prin_myr, n_clients=len(c), clients=clients,
                          p_ko_next=res[('hist', 'base')]['p_ko_next'], p_ki_bear=max(res[('hist', 'bear')]['p_ki'], res[('stress', 'bear')]['p_ki']),
                          p_ki_base=res[('hist', 'base')]['p_ki'], p_ki_bull=res[('hist', 'bull')]['p_ki'], p_ki_base_stress=res[('stress', 'base')]['p_ki'],
                          el_bear_myr=prin_myr * max(res[('hist', 'bear')]['el'], res[('stress', 'bear')]['el']), el_base_myr=prin_myr * res[('hist', 'base')]['el'],
                          lgd_base=res[('hist', 'base')]['lgd'], avg_corr=(C.sum() - len(tick)) / max(len(tick) * (len(tick) - 1), 1)))
D = pd.DataFrame(deal_rows).sort_values('p_ki_bear', ascending=False); D.to_csv(OUT / 'm9_client_deals.csv', index=False)
LG = pd.DataFrame(leg_rows); LG.to_csv(OUT / 'm9_client_legs.csv', index=False)
print(f"\nCLIENT BOOK: {len(D)} live deals, principal RM{D.prin_myr.sum():,.0f} (MYR eq) | MC {NPATH} paths, GBM at monthly obs, memory KO, European KI at FV, physical at strike")
print(D.drop(columns=['clients']).to_string(index=False, float_format=lambda v: f'{v:,.3f}'))
print('\nLeg flags (rule: KI dist <= 1.0x 3M 1sd move RED, <= 1.5x AMBER):', LG.flag.value_counts().to_dict(), '| deals with >=1 RED leg:', LG[LG.flag == 'RED'].deal.nunique())
print(LG.sort_values('ki_dist')[['deal', 'ticker', 'pct_init', 'ki_pct', 'ki_dist', 'wk_move', 'ki_dist_x_wk', 'move3m_1sd', 'ki_dist_x_3m', 'flag', 'fv']].to_string(index=False, float_format=lambda v: f'{v:.3f}'))
print(f"\nExpected loss (MYR): bear RM{D.el_bear_myr.sum():,.0f} | base RM{D.el_base_myr.sum():,.0f} on RM{D.prin_myr.sum():,.0f} principal")
# historical stress replay (instantaneous, beta-scaled) -> count deals whose worst-of would sit below KI
for nm, shock in [('2018 post-midterm path SPX -14.7%', -0.1467), ('1987 crash SPX -33.5%', -0.335)]:
    below = 0; rm = 0
    for deal, g in legs.groupby('Deal'):
        g = g.reset_index(drop=True); KI = pct(g.KI[0]); init = np.array([num(x) for x in g.InitPx])
        S1 = np.array([info[t]['last'] * np.exp(info[t]['beta_adj'] * np.log(1 + shock)) for t in g.Ticker])
        if (S1 / init).min() < KI: below += 1; rm += D.set_index('deal').loc[deal, 'prin_myr']
    print(f"Stress {nm}, beta-scaled: {below}/{len(D)} deals with worst-of below KI (RM{rm:,.0f}) vs {int((D.worst_now < D.KI).sum())} today")
print('Senate MC summary saved.'); json.dump({str(k): v for k, v in sen.items()}, open(OUT / 'm1_senate_mc.json', 'w'), default=float)
