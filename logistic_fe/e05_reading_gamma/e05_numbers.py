"""Model in Motion · The Logistic Fixed-Effect Model · Episode 5: Reading gamma.

Every number the episode shows or says is computed here, checked, and written to e05_numbers.json.
Scenes and narration read e05_numbers.json; nothing numeric is typed into scene code or the script.

    python e05_numbers.py        # from this folder: prints the ledger, runs every check, writes e05_numbers.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit  # noqa: E402

CHECKS: list[tuple[str, bool, str]] = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


odds = lambda p: p / (1 - p)

# ----------------------------------------------------------------------------- 1. the fit (as in Episode 4)
g, beta, cov, loglik = fit()
P = {k: (float(expit(g[k])), float(expit(g[k] + beta))) for k in FINITE}       # the model's probabilities: (lower-risk, higher-risk)
E4 = json.loads((HERE.parent / "e04_one_intercept_per_provider" / "e04_numbers.json").read_text())
check("same fit as Episode 4's numbers file (beta and the four gammas)",
      abs(beta - E4["fit"]["beta"]) < 1e-9 and all(abs(g[k] - E4["fit"]["clinics"][k]["gamma"]) < 1e-9 for k in FINITE),
      f"beta {beta:.4f}; " + ", ".join(f"{k} {g[k]:.4f}" for k in FINITE))
check("the cast here is the cast Episode 4 used",
      all(E4["observed"][k]["n_low"] == CAST[k][0] and E4["observed"][k]["events_low"] == CAST[k][1]
          and E4["observed"][k]["n_high"] == CAST[k][2] and E4["observed"][k]["events_high"] == CAST[k][3] for k in CAST))

# ----------------------------------------------------------------------------- 2. the gap (S01)
gap = g["Alder"] - g["Cedar"]
OR = float(np.exp(gap))
check("Alder's line sits 0.87 above Cedar's: an odds ratio of 2.4 (blueprint: 0.871 and 2.39)", abs(gap - 0.8708) < 5e-5 and abs(OR - 2.389) < 5e-4,
      f"{gap:.4f}, {OR:.4f}")
check("the gap is the same at both risk levels", abs((logit(P["Alder"][1]) - logit(P["Cedar"][1])) - gap) < 1e-12)

# ----------------------------------------------------------------------------- 3. three readings (S03)
raw = {k: (CAST[k][1] + CAST[k][3], CAST[k][0] + CAST[k][2]) for k in ("Alder", "Cedar")}
raw_rate = {k: raw[k][0] / raw[k][1] for k in raw}
check("reading one fails: 13 of 30 against 8 of 20 is 43% against 40%, a ratio of 1.08",
      raw["Alder"] == (13, 30) and raw["Cedar"] == (8, 20) and (round(100 * raw_rate["Alder"]), round(100 * raw_rate["Cedar"])) == (43, 40)
      and abs(raw_rate["Alder"] / raw_rate["Cedar"] - 1.083) < 5e-4, f"{raw_rate['Alder'] / raw_rate['Cedar']:.3f}")
rr = [P["Alder"][k] / P["Cedar"][k] for k in (0, 1)]
check("reading two fails: 18% to 34% is 1.9 times, 62% to 80% is 1.3 times",
      [round(100 * P["Cedar"][k]) for k in (0, 1)] == [18, 62] and [round(100 * P["Alder"][k]) for k in (0, 1)] == [34, 80]
      and [round(v, 1) for v in rr] == [1.9, 1.3], f"{rr[0]:.3f}, {rr[1]:.3f}")
impossible = OR * P["Cedar"][1]
check("reading two is impossible for the higher-risk patient: 2.4 times 62% is nearly 150%", 1.45 < impossible < 1.50, f"{100 * impossible:.1f}%")
od = {k: (float(odds(P[k][0])), float(odds(P[k][1]))) for k in ("Alder", "Cedar")}
check("reading three holds: odds 0.22 to 0.52 and 1.64 to 3.91, each 2.4 times",
      [round(od["Cedar"][0], 2), round(od["Alder"][0], 2), round(od["Cedar"][1], 2), round(od["Alder"][1], 2)] == [0.22, 0.52, 1.64, 3.91]
      and all(abs(od["Alder"][k] / od["Cedar"][k] - OR) < 1e-9 for k in (0, 1)),
      f"{od['Cedar'][0]:.4f} -> {od['Alder'][0]:.4f}; {od['Cedar'][1]:.4f} -> {od['Alder'][1]:.4f}")

# the alternative test of reading one offered in the script doc: Alder's own 30 patients at Cedar's level
alt_e = CAST["Alder"][0] * P["Cedar"][0] + CAST["Alder"][2] * P["Cedar"][1]
check("alternative for reading one: Alder's 30 patients would have 8.0 readmissions at Cedar's level against 13, a ratio of 1.6",
      abs(alt_e - 8.02) < 5e-3 and round(raw["Alder"][0] / alt_e, 1) == 1.6, f"{alt_e:.3f}, ratio {raw['Alder'][0] / alt_e:.3f}")

# ----------------------------------------------------------------------------- 4. one odds ratio, many effects (S04)
stops = [0.05, P["Cedar"][0], 0.50, P["Cedar"][1], 0.90]            # Cedar's probability for the patient
slide = []
for q in stops:
    a = float(expit(logit(q) + gap))
    slide.append({"cedar": float(q), "alder": a, "difference": a - q, "ratio": a / q, "s": float(logit(q) - g["Cedar"])})
check("slide: 5, 18, 50, 62, 90 percent at Cedar become 11, 34, 70, 80, 96 at Alder (blueprint)",
      [round(100 * r["cedar"]) for r in slide] == [5, 18, 50, 62, 90] and [round(100 * r["alder"]) for r in slide] == [11, 34, 70, 80, 96],
      str([round(100 * r["alder"], 1) for r in slide]))
check("slide: differences of 6, 16, 20, 18 and 6 points, each equal to the difference of the rounded pair",
      [round(100 * r["difference"]) for r in slide] == [6, 16, 20, 18, 6]
      and all(round(100 * r["difference"]) == round(100 * r["alder"]) - round(100 * r["cedar"]) for r in slide),
      str([round(100 * r["difference"], 2) for r in slide]))
check("slide: the ratio of probabilities falls from 2.2 to 1.06", [round(slide[0]["ratio"], 1), round(slide[-1]["ratio"], 2)] == [2.2, 1.06]
      and all(a["ratio"] > b["ratio"] for a, b in zip(slide, slide[1:])), str([round(r["ratio"], 2) for r in slide]))
q_star = float(expit(-gap / 2))
biggest = float(expit(gap / 2) - q_star)
check("the difference is largest in the middle (21 points, from 39% to 61%) and smaller at every stop",
      abs(biggest - 0.214) < 1e-3 and all(r["difference"] <= biggest + 1e-12 for r in slide), f"{100 * biggest:.1f} points at {100 * q_star:.1f}%")
rare = float(expit(logit(0.01) + gap) / 0.01)
check("only for rare events does the ratio of probabilities come close to the odds ratio (2.36 at 1%)", abs(rare - 2.36) < 5e-3 and rare < OR,
      f"{rare:.3f} against {OR:.3f}")

# ----------------------------------------------------------------------------- 5. gammas move, gaps don't (S05)
zero = {}
for label, shift in (("lower", 0.0), ("higher", 1.0), ("halfway", 0.5)):
    gz, bz, _, llz = fit(shift=shift)                                    # a real refit with the risk factor recoded
    zero[label] = {"shift": shift, "gamma": gz, "beta": bz, "loglik": llz,
                   "p": {k: (float(expit(gz[k] + bz * (0 - shift))), float(expit(gz[k] + bz * (1 - shift)))) for k in FINITE}}
check("recoding: with higher-risk as zero every gamma rises by 2.02 (the whole step)",
      all(abs(zero["higher"]["gamma"][k] - g[k] - beta) < 1e-9 for k in FINITE) and round(beta, 2) == 2.02)
check("recoding: with zero halfway every gamma rises by 1.01 (blueprint: 1.008)",
      all(abs(zero["halfway"]["gamma"][k] - g[k] - beta / 2) < 1e-9 for k in FINITE) and round(beta / 2, 3) == 1.008 and round(beta / 2, 2) == 1.01)
check("recoding changes neither beta, nor any probability, nor the fit",
      all(abs(z["beta"] - beta) < 1e-9 and abs(z["loglik"] - loglik) < 1e-9 and all(abs(z["p"][k][j] - P[k][j]) < 1e-9 for k in FINITE for j in (0, 1))
          for z in zero.values()))
check("recoding leaves every gap where it was: Alder minus Cedar is 0.87 each time",
      all(abs((z["gamma"]["Alder"] - z["gamma"]["Cedar"]) - gap) < 1e-9 for z in zero.values()))

# ----------------------------------------------------------------------------- 6. a warning about averages (S06)
n_low, n_high = sum(v[0] for v in CAST.values()), sum(v[2] for v in CAST.values())
avg = {k: (n_low * P[k][0] + n_high * P[k][1]) / (n_low + n_high) for k in ("Alder", "Cedar")}
gap_avg = float(logit(avg["Alder"]) - logit(avg["Cedar"]))
check("all 103 patients: 57 lower-risk and 46 higher-risk", (n_low, n_high) == (57, 46))
check("averages: 38% at Cedar's level and 55% at Alder's (blueprint: 37.6% and 54.5%)",
      abs(avg["Cedar"] - 0.3764) < 5e-5 and abs(avg["Alder"] - 0.5453) < 5e-5 and (round(100 * avg["Cedar"]), round(100 * avg["Alder"])) == (38, 55),
      f"{100 * avg['Cedar']:.2f}%, {100 * avg['Alder']:.2f}%")
check("averages: the two rates are 0.69 apart on the log-odds ruler, not 0.87 (blueprint: 0.686); an odds ratio of 2.0",
      abs(gap_avg - 0.6867) < 5e-4 and round(gap_avg, 2) == 0.69 and round(float(np.exp(gap_avg)), 1) == 2.0, f"{gap_avg:.4f}, odds ratio {np.exp(gap_avg):.3f}")
rng = np.random.default_rng(5)
worst = 0.0
for _ in range(20000):                                                   # any mix of patients, any gap: the averaged gap is never the larger
    k = int(rng.integers(2, 6))
    w = rng.dirichlet(np.ones(k)); base = rng.normal(0, 2, k); d = abs(rng.normal(0, 1.5)) + 1e-3
    worst = max(worst, float(logit(w @ expit(base + d)) - logit(w @ expit(base))) - d)
check("the gap between two averages is never larger than the gap for each patient (20,000 random mixes)", worst <= 1e-12, f"largest excess {worst:.1e}")
same = float(logit(expit(-0.5 + gap)) - logit(expit(-0.5)))
check("and it is equal only when every patient has the same risk", abs(same - gap) < 1e-12)

# ----------------------------------------------------------------------------- 7. spoken forms
check("spoken roundings: 0.87, 2.4, 2.02, 1.01, 0.69, 38%, 55%",
      (round(gap, 2), round(OR, 1), round(beta, 2), round(beta / 2, 2), round(gap_avg, 2)) == (0.87, 2.4, 2.02, 1.01, 0.69))

OUT = {
    "episode": 5, "title": "Reading gamma",
    "fit": {"beta": beta, "odds_ratio_beta": float(np.exp(beta)), "gamma": g, "p": P},
    "gap": {"alder_minus_cedar": gap, "odds_ratio": OR},
    "reading_one": {"alder": [raw["Alder"][0], raw["Alder"][1], raw_rate["Alder"]], "cedar": [raw["Cedar"][0], raw["Cedar"][1], raw_rate["Cedar"]],
                    "ratio": raw_rate["Alder"] / raw_rate["Cedar"]},
    "reading_two": {"ratio_low": rr[0], "ratio_high": rr[1], "impossible": impossible},
    "reading_three": {"cedar_odds": list(od["Cedar"]), "alder_odds": list(od["Alder"])},
    "slide": slide, "largest_difference": {"cedar": q_star, "alder": float(expit(gap / 2)), "difference": biggest}, "rare_ratio": rare,
    "zero": {k: {"shift_in_gamma": zero[k]["gamma"]["Alder"] - g["Alder"], "gamma": zero[k]["gamma"]} for k in zero},
    "averages": {"n_low": n_low, "n_high": n_high, "cedar_rate": avg["Cedar"], "alder_rate": avg["Alder"], "gap": gap_avg, "odds_ratio": float(np.exp(gap_avg))},
    "patients": n_low + n_high,
}

if __name__ == "__main__":
    print(f"gap Alder - Cedar {gap:.4f}  odds ratio {OR:.3f}")
    print("reading one   raw rates", f"{100 * raw_rate['Alder']:.1f}% vs {100 * raw_rate['Cedar']:.1f}%  ratio {raw_rate['Alder'] / raw_rate['Cedar']:.3f}")
    print("reading two   ratios of probabilities", f"{rr[0]:.3f} (lower-risk), {rr[1]:.3f} (higher-risk); 2.4 x 62% = {100 * impossible:.0f}%")
    print("reading three odds", f"{od['Cedar'][0]:.3f} -> {od['Alder'][0]:.3f}, {od['Cedar'][1]:.3f} -> {od['Alder'][1]:.3f}")
    print(f"{'at Cedar':>9s}{'at Alder':>10s}{'difference':>12s}{'ratio':>8s}")
    for r in slide:
        print(f"{100 * r['cedar']:8.1f}%{100 * r['alder']:9.1f}%{100 * r['difference']:10.1f} pt{r['ratio']:8.2f}")
    print("zero at higher-risk: gammas +", f"{beta:.4f}", "  halfway: +", f"{beta / 2:.4f}")
    print(f"averages: {100 * avg['Cedar']:.2f}% and {100 * avg['Alder']:.2f}%; gap {gap_avg:.4f} (odds ratio {np.exp(gap_avg):.3f}) against {gap:.4f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e05_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
