"""
01_edgar_history.py
Tier-1 pull: every Micron earnings 8-K (Item 2.02) from SEC EDGAR (CIK 0000723125).
Downloads Exhibit 99.1 press releases to analysis/data/pr/ as plain text and writes
analysis/data/earnings_dates.csv (filing date + acceptance timestamp, all after US close).
"""
import json, re, html, time, pathlib, requests
import pandas as pd

UA = {"User-Agent": "Stock-Analysis research limszehau95@gmail.com"}
ROOT = pathlib.Path(__file__).resolve().parent
DATA = ROOT / "data"
PR = DATA / "pr"
PR.mkdir(parents=True, exist_ok=True)

sub = json.load(open(DATA / "edgar_submissions.json"))
r = sub["filings"]["recent"]
rows = []
for i in range(len(r["form"])):
    if r["form"][i] == "8-K" and "2.02" in r["items"][i]:
        rows.append(dict(filing_date=r["filingDate"][i], accession=r["accessionNumber"][i],
                         acceptance=r["acceptanceDateTime"][i]))
ed = pd.DataFrame(rows).sort_values("filing_date")
ed = ed[ed.filing_date >= "2017-09-01"].reset_index(drop=True)


def to_text(raw: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>|</p>|</tr>|</div>", "\n", t, flags=re.I)
    t = re.sub(r"</td>", " | ", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t).replace("\xa0", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n\s*\n+", "\n", t)
    return t


docs = []
for _, row in ed.iterrows():
    out = PR / f"{row.filing_date}.txt"
    if out.exists() and out.stat().st_size > 0:
        docs.append(out.name)
        continue
    acc = row.accession.replace("-", "")
    idx = requests.get(f"https://www.sec.gov/Archives/edgar/data/723125/{acc}/index.json", headers=UA).json()
    names = [it["name"] for it in idx["directory"]["item"]]
    # 2020+: single ex-99.1; 2017-19: 'exhibit991-pressrel.htm' plus a separate 'guidance.htm'
    cands = [n for n in names if re.search(r"ex[a-z]*-?99|pressrel|earningsrele|guidance", n, re.I) and n.endswith(".htm")]
    if not cands:
        cands = [n for n in names if n.endswith(".htm")]
    parts = []
    for c in sorted(cands, key=lambda n: "guidance" in n.lower()):
        raw = requests.get(f"https://www.sec.gov/Archives/edgar/data/723125/{acc}/{c}", headers=UA).text
        t = to_text(raw)
        if re.search(r"revenue|guidance", t, re.I):
            parts.append(t)
        time.sleep(0.15)
    txt = "\n".join(parts)
    out.write_text(txt)
    docs.append(out.name)
    time.sleep(0.2)

ed["pr_file"] = docs
ed.to_csv(DATA / "earnings_dates.csv", index=False)
print(ed.to_string())
