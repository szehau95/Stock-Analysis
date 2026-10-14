"""Substitute {{TABLE}} placeholders in reports/screen_narrative.md with output/screen/tables.md blocks."""
import re
from common import OUT
blocks = dict(re.findall(r"^## (\S+)\n\n(.*?)(?=^## |\Z)", open(f"{OUT}/tables.md").read(), flags=re.S | re.M))
txt = open("reports/screen_narrative.md").read()
missing = sorted(set(re.findall(r"\{\{(\w+)\}\}", txt)) - set(blocks))
assert not missing, f"missing tables: {missing}"
out = re.sub(r"\{\{(\w+)\}\}", lambda m: blocks[m.group(1)].strip(), txt)
open("reports/MY_Banks_Value_TA_Screen_14102026.md", "w").write(out)
print("report written:", len(out), "chars")
