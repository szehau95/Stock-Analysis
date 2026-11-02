"""Pull live Kalshi + Polymarket midterm contracts (Tier 1 market data) and daily price history. Saves raw JSON; prints a compact table."""
import json, time, urllib.request, urllib.parse, pathlib, datetime as dt
OUT = pathlib.Path('data/raw/odds'); OUT.mkdir(parents=True, exist_ok=True)
def get(url, tries=4):
    for a in range(tries):
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=60))
        except Exception as e:
            err = e; time.sleep(2 ** (a + 1))
    raise err
K = "https://api.elections.kalshi.com/trade-api/v2"
now = dt.datetime.now(dt.timezone.utc)
print("pulled", now.strftime("%Y-%m-%d %H:%M UTC"), "=", (now + dt.timedelta(hours=8)).strftime("%d/%m/%Y %H:%M MYT"))
kal = {}
for s in ["CONTROLH", "CONTROLS", "KXBALANCEPOWERCOMBO", "KXDSENATESEATS", "KXDHOUSESEATS"]:
    js = get(f"{K}/events?series_ticker={s}&with_nested_markets=true&status=open&limit=50")
    kal[s] = js
    for ev in js.get("events", []):
        print(f"\nKALSHI {s} | {ev['event_ticker']} | {ev.get('title')}")
        for m in ev.get("markets", []):
            yb, ya, lp = m.get("yes_bid"), m.get("yes_ask"), m.get("last_price")
            yb = m.get("yes_bid_dollars", yb); ya = m.get("yes_ask_dollars", ya); lp = m.get("last_price_dollars", lp)
            print(f"   {m['ticker']:<34} {str(m.get('yes_sub_title') or m.get('subtitle') or ''):<42} bid {yb} ask {ya} last {lp} vol {m.get('volume')} oi {m.get('open_interest')}")
json.dump(kal, open(OUT / "kalshi_live.json", "w"))
pm = {}
for slug in ["balance-of-power-2026-midterms", "which-party-will-win-the-house-in-2026", "which-party-will-win-the-senate-in-2026"]:
    js = get("https://gamma-api.polymarket.com/events?slug=" + slug)
    pm[slug] = js
    for ev in js:
        print(f"\nPOLYMARKET {slug} | vol {float(ev.get('volume') or 0):,.0f} | liq {float(ev.get('liquidity') or 0):,.0f}")
        for m in ev.get("markets", []):
            if m.get("closed"): continue
            op = json.loads(m.get("outcomePrices") or "[]"); oc = json.loads(m.get("outcomes") or "[]")
            print(f"   {m.get('groupItemTitle') or m.get('question'):<48} {dict(zip(oc, op))} bid {m.get('bestBid')} ask {m.get('bestAsk')} last {m.get('lastTradePrice')} vol {float(m.get('volume') or 0):,.0f}")
json.dump(pm, open(OUT / "polymarket_live.json", "w"))
# daily history (Polymarket CLOB) for each open market's YES token
hist = {}
for slug, js in pm.items():
    for ev in js:
        for m in ev.get("markets", []):
            if m.get("closed"): continue
            tok = json.loads(m.get("clobTokenIds") or "[]")
            if not tok: continue
            name = f"{slug}::{m.get('groupItemTitle') or m.get('question')}"
            h = get(f"https://clob.polymarket.com/prices-history?market={tok[0]}&interval=max&fidelity=1440")
            hist[name] = h.get("history", [])
json.dump(hist, open(OUT / "polymarket_history.json", "w"))
print("\nPM history series:", {k.split('::')[1]: len(v) for k, v in hist.items()})
