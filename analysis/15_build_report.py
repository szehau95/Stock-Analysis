"""
15_build_report.py — fills report_template.md placeholders with tables rendered from the CSV outputs
(data/report_tables.md from 14_report_tables.py, and data/source_log.csv) -> ../MU_earnings_report.md
"""
import pathlib, re
import pandas as pd

ROOT = pathlib.Path(__file__).resolve().parent
REPO = ROOT.parent
tpl = (ROOT / "report_template.md").read_text()
blocks = {}
cur = None
for line in (ROOT / "data" / "report_tables.md").read_text().splitlines():
    m = re.match(r"^## (T_\w+)$", line)
    if m:
        cur = m.group(1); blocks[cur] = []
    elif cur:
        blocks[cur].append(line)
for k, v in blocks.items():
    tpl = tpl.replace(f"<<{k}>>", "\n".join(v).strip())
src = pd.read_csv(ROOT / "data" / "source_log.csv")
src["source"] = [f"[{s}]({u})" if str(u).startswith("http") else f"{s} ({u})" for s, u in zip(src.source, src.url)]
tpl = tpl.replace("<<SOURCE_LOG>>", src[["figure", "value", "source", "tier", "date"]].apply(lambda c: c.map(lambda v: v.replace("|", "\\|") if isinstance(v, str) else v)).to_markdown(index=False))
left = re.findall(r"<<\w+>>", tpl)
assert not left, left
(REPO / "MU_earnings_report.md").write_text(tpl)
print("written", len(tpl), "chars")
