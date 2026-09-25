"""
08_beat_probability.py — Module 2c: beat probabilities (Monte Carlo; assumptions in mc_core.PARAMS)
Writes data/beat_probabilities.csv and data/mc_draws_sample.csv
"""
import pathlib
import numpy as np
import pandas as pd
from mc_core import simulate, CONS, WHISPER

ROOT = pathlib.Path(__file__).resolve().parent
df, p = simulate()
rev4, eps4, gm4, rev1, gm1, eps1, g = df.rev4, df.eps4, df.gm4, df.rev1, df.gm1, df.eps1, df.g_week
df.drop(columns=["move", "is_tail", "tail_name"]).sample(5_000, random_state=1).to_csv(
    ROOT / "data" / "mc_draws_sample.csv", index=False)

P = {
    "P(FQ4 rev > consensus mean $50.69bn)": (rev4 > CONS["rev4"]).mean(),
    "P(FQ4 rev > high snapshot $51.2bn)": (rev4 > CONS["rev4_hi"]).mean(),
    "P(FQ4 rev > guide high $51.0bn)": (rev4 > 51.0).mean(),
    "P(FQ4 rev > whisper mid $52.75bn)": (rev4 > WHISPER["rev4"]).mean(),
    "P(FQ4 rev < guide mid $50.0bn)": (rev4 < 50.0).mean(),
    "P(FQ4 EPS > consensus $31.34)": (eps4 > CONS["eps4"]).mean(),
    "P(FQ4 EPS > whisper mid $33.25)": (eps4 > WHISPER["eps4"]).mean(),
    "P(FQ4 GM >= consensus 87.0%)": (gm4 >= CONS["gm4"]).mean(),
    "P(FQ1 rev guide mid > consensus $56.7bn)": (rev1 > CONS["rev1"]).mean(),
    "P(FQ1 rev guide mid > whisper mid $58.5bn)": (rev1 > WHISPER["rev1"]).mean(),
    "P(FQ1 GM guide >= consensus 87.5%)": (gm1 >= CONS["gm1"]).mean(),
    "P(FQ1 GM guide >= whisper 88.25%)": (gm1 >= WHISPER["gm1"]).mean(),
    "P(FQ1 EPS guide >= consensus $35.25)": (eps1 >= CONS["eps1"]).mean(),
    "P(FQ1 EPS guide >= whisper $37.25)": (eps1 >= WHISPER["eps1"]).mean(),
    "P(FQ1 guide headline QoQ <= 0%, flat/down)": (rev1 <= rev4).mean(),
    "P(FQ1 guide headline QoQ < +10%)": ((rev1 / rev4 - 1) < 0.10).mean(),
    "P(print beat AND FQ1 rev guide < consensus)": ((rev4 > CONS["rev4"]) & (rev1 < CONS["rev1"])).mean(),
}
E = {
    "E[FQ4 rev $bn]": rev4.mean(), "median FQ4 rev $bn": rev4.median(),
    "p10 FQ4 rev": rev4.quantile(0.10), "p90 FQ4 rev": rev4.quantile(0.90),
    "E[FQ4 rev beat vs consensus %]": 100 * (rev4.mean() / CONS["rev4"] - 1),
    "E[FQ4 rev beat vs consensus $bn]": rev4.mean() - CONS["rev4"],
    "E[FQ4 rev beat vs guide mid %]": 100 * (rev4.mean() / 50.0 - 1),
    "E[FQ4 GM %]": gm4.mean(), "E[FQ4 EPS]": eps4.mean(),
    "E[FQ4 EPS beat vs consensus %]": 100 * (eps4.mean() / CONS["eps4"] - 1),
    "E[FQ1 rev guide $bn]": rev1.mean(), "p10 FQ1 rev guide": rev1.quantile(0.10), "p90 FQ1 rev guide": rev1.quantile(0.90),
    "E[FQ1 guide vs consensus %]": 100 * (rev1.mean() / CONS["rev1"] - 1),
    "E[FQ1 GM guide %]": gm1.mean(), "E[FQ1 EPS guide]": eps1.mean(),
    "E[FQ1 guide headline QoQ %]": 100 * (rev1 / rev4 - 1).mean(),
    "E[FQ1 guide per-week QoQ %]": 100 * g.mean(),
    "E[FQ4 actual headline QoQ % vs FQ3 $41.456bn]": 100 * (rev4.mean() / 41.456 - 1),
    "E[FQ4 actual per-week QoQ %]": 100 * ((rev4.mean() / 14) / (41.456 / 13) - 1),
}
res = pd.concat([pd.Series(P), pd.Series(E)])
res.to_csv(ROOT / "data" / "beat_probabilities.csv", header=["value"])
print("params:", {k: p[k] for k in ["g_mu", "g_sd", "rho", "beat_mix_p", "beat_mu"]})
print(res.round(4).to_string())
g_eps = (50.0 * 0.86 - 1.65 + 0.55) * 0.85 / p["shares"]
print(f"\ncheck: guide-input EPS = {g_eps:.2f} (company guide 31.00)")
