"""Model in Motion · The Logistic Fixed-Effect Model · Episode 14: Three shortcuts.

Every number the episode shows or says is computed here, checked, and written to e14_numbers.json.
Scenes and narration read e14_numbers.json; nothing numeric is typed into scene code or the script.

    python e14_numbers.py        # from this folder: prints the ledger, runs every check, writes e14_numbers.json
"""
from __future__ import annotations

import inspect
import json
import logging
import sys
import warnings
from math import erfc, sqrt
from pathlib import Path
from statistics import NormalDist

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, coin_pmf, expit, fit, mid_p, rows  # noqa: E402
from mim.crowd import case_mix_se, joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

ALL = list(CAST)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
two_sided = lambda z: erfc(abs(z) / sqrt(2.0))                                   # both tails of a bell curve beyond z
SEED, DRAWS = 2026, 10000


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta, cov4, ll_fit = fit()
E9 = json.loads((HERE.parent / "e09_how_sure_are_we" / "e09_numbers.json").read_text())
E10 = json.loads((HERE.parent / "e10_no_events_no_peak" / "e10_numbers.json").read_text())
E11 = json.loads((HERE.parent / "e11_swap_the_curve" / "e11_numbers.json").read_text())
E13 = json.loads((HERE.parent / "e13_unequal_coins" / "e13_numbers.json").read_text())
ref = E11["reference"]["gamma"]
gam = {**g_fit, "Elm": E10["printed"]["together"]}
N0 = {k: CAST[k][0] for k in ALL}; N1 = {k: CAST[k][2] for k in ALL}
OBS = {k: CAST[k][1] + CAST[k][3] for k in ALL}
coins = lambda k, g=ref: np.array([float(expit(g))] * N0[k] + [float(expit(g + beta))] * N1[k])
E = {k: float(coins(k).sum()) for k in ALL}
V = {k: float((coins(k) * (1 - coins(k))).sum()) for k in ALL}
PK = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")

# ----------------------------------------------------------------------------- 1. where we left off (S01)
p_exact = dict(E13["p_value"])
check("last time's exact p-value for Alder: 3.5%", round(100 * p_exact["Alder"], 1) == 3.5)

import time  # noqa: E402
_t = time.perf_counter()
_big = coin_pmf(np.random.default_rng(1).uniform(0.05, 0.6, 5000))
check("for the record: the exact pile is not slow; for a provider of 5,000 patients it takes well under a second", time.perf_counter() - _t < 1.0 and abs(float(_big.sum()) - 1.0) < 1e-9,
      f"{time.perf_counter() - _t:.3f} s")

# ----------------------------------------------------------------------------- 2. one: a bell curve (S03)
sd = {k: sqrt(V[k]) for k in ALL}
z_score = {k: (OBS[k] - E[k]) / sd[k] for k in ALL}
p_score = {k: two_sided(z_score[k]) for k in ALL}
check("Alder's pile is centred on 8.02 with a standard deviation of 2.22 (blueprint)", (round(E["Alder"], 2), round(sd["Alder"], 2)) == (8.02, 2.22))
check("its 13 is 4.98 above the centre: 2.24 standard deviations, and the bell curve's two tails hold 2.5% (blueprint)",
      (round(OBS["Alder"] - E["Alder"], 2), round(z_score["Alder"], 2), round(100 * p_score["Alder"], 1)) == (4.98, 2.24, 2.5), f"{z_score['Alder']:.4f}, {p_score['Alder']:.4f}")
check("the bell curve has the pile's own centre and spread", abs(float(np.arange(31) @ np.array(E13["pmf"]["Alder"])) - E["Alder"]) < 1e-9 and abs(E13["alder"]["variance"] - V["Alder"]) < 1e-9)
t_score = PK.test(test_method="score")
check("pprof_py's score test gives the same z and p for all five", all(abs(float(t_score.loc[k, "z_raw"]) - z_score[k]) < 1e-3 and abs(float(t_score.loc[k, "p_value"]) - p_score[k]) < 1e-3 for k in ALL),
      str(fl([float(t_score.loc[k, "z_raw"]) for k in ALL])))

# ----------------------------------------------------------------------------- 3. two: a ruler on the gamma axis (S04)
se = dict(zip(ALL, E9["share"]["avg_se"]))                                          # Episode 9's standard errors at the average case mix
gap = {k: gam[k] - ref for k in ALL}
z_wald = {k: gap[k] / se[k] for k in ALL}
p_wald = {k: two_sided(z_wald[k]) for k in ALL}
check("Alder's gamma sits 0.87 above the reference with a standard error of 0.43 (blueprint: 0.871 and 0.432)", (round(gap["Alder"], 2), round(se["Alder"], 2)) == (0.87, 0.43)
      and abs(gap["Alder"] - 0.871) < 5e-4 and abs(se["Alder"] - 0.432) < 5e-4)
check("that is 2.02 standard errors and a p-value of 4.4% (blueprint)", (round(z_wald["Alder"], 2), round(100 * p_wald["Alder"], 1)) == (2.02, 4.4) and round(0.87 / 0.43, 2) == 2.02,
      f"{z_wald['Alder']:.4f}, {p_wald['Alder']:.4f}")
t_wald = PK.test(test_method="wald")
check("pprof_py's Wald test gives the same z and p for all five", all(abs(float(t_wald.loc[k, "z_raw"]) - z_wald[k]) < 1e-3 and abs(float(t_wald.loc[k, "p_value"]) - p_wald[k]) < 1e-3 for k in ALL),
      str(fl([float(t_wald.loc[k, "z_raw"]) for k in ALL])))

# ----------------------------------------------------------------------------- 4. three: just flip (S05)
flips = np.random.default_rng(SEED).random((DRAWS, len(coins("Alder")))) < coins("Alder")
tally = flips.sum(axis=1)
stages = {n: np.bincount(tally[:n], minlength=31).tolist() for n in (100, 1000, DRAWS)}
p_boot = mid_p(np.array(stages[DRAWS]) / DRAWS, OBS["Alder"])
check("ten thousand rounds of Alder's thirty coins (series seed) give a p-value of 3.8%", round(100 * p_boot, 1) == 3.8 and abs(p_boot - p_exact["Alder"]) < 0.006, f"{p_boot:.4f}")
check("the flipped pile is within 1 point of the exact one at every count", np.max(np.abs(np.array(stages[DRAWS]) / DRAWS - np.array(E13["pmf"]["Alder"]))) < 0.01,
      f"largest gap {np.max(np.abs(np.array(stages[DRAWS]) / DRAWS - np.array(E13['pmf']['Alder']))):.4f}")
check("with ten thousand rounds the smallest p-value it can report, short of zero, is 1 in 10,000", abs(2 * 0.5 / DRAWS - 1e-4) < 1e-15)
t_boot = PK.test(test_method="bootstrap_exact", n_resample=DRAWS, seed=SEED)
check("pprof_py's own bootstrap, with its own random draws, lands within half a point of the exact 3.5% and flags only Alder (blueprint's run: 3.9%)",
      abs(float(t_boot.loc["Alder", "p_value"]) - p_exact["Alder"]) < 0.005 and [k for k in ALL if int(t_boot.loc[k, "flag"]) != 0] == ["Alder"], f"{float(t_boot.loc['Alder', 'p_value']):.4f}")

# ----------------------------------------------------------------------------- 5. the scoreboard (S06)
inv = NormalDist().inv_cdf
z_exact = {k: float(np.sign(OBS[k] - E[k]) * inv(1 - p_exact[k] / 2)) for k in ALL}
check("z by exact, bell curve and ruler: Alder 2.11, 2.24, 2.02; Birch -0.76, -0.77, -0.64; Dune 1.39, 1.45, 1.43; Elm -1.58, -1.55, -0.69 (blueprint)",
      [fl([z_exact[k], z_score[k], z_wald[k]], 2) for k in ("Alder", "Birch", "Dune", "Elm")] == [[2.11, 2.24, 2.02], [-0.76, -0.77, -0.64], [1.39, 1.45, 1.43], [-1.58, -1.55, -0.69]])
flags = {"exact": [k for k in ALL if p_exact[k] < 0.05], "bell": [k for k in ALL if p_score[k] < 0.05], "ruler": [k for k in ALL if p_wald[k] < 0.05]}
check("all four ways put Alder below 5%, and the three tests flag no one else", all(v == ["Alder"] for v in flags.values()) and p_boot < 0.05, str({k: fl([p_exact[k], p_score[k], p_wald[k]], 3) for k in ALL}))
w_fit = lambda g: float(sum(N0["Elm"] * expit(g) * (1 - expit(g)) for _ in range(1)))
elm_turns = E10["printed"]["turns"]
z_elm_turns = (elm_turns - ref) / sqrt(1.0 / w_fit(elm_turns) + (0.0 - E9["share"]["xbar"]) ** 2 / E9["dial"]["S"])
check("for Elm the ruler reads -0.7 where the other two read about -1.5; after the other fitting routine it would read -0.1",
      round(z_wald["Elm"], 1) == -0.7 and round(z_exact["Elm"], 1) == -1.6 and round(z_score["Elm"], 1) == -1.5 and round(z_elm_turns, 1) == -0.1, f"{z_wald['Elm']:.3f}, {z_elm_turns:.3f}")

# ----------------------------------------------------------------------------- 6. where they fail (S07)
def textbook_se(shift):
    """Standard error of Alder's gamma read at zero when the risk factor is recorded `shift` units higher (Episode 9)."""
    x = X01 + shift
    g_all = np.array([gam[k] - shift * beta for k in ALL])
    p = expit(g_all[PROV] + x * beta); w = p * (1 - p)
    Vf = np.bincount(PROV, weights=w, minlength=5); Bf = np.bincount(PROV, weights=w * x, minlength=5)
    S = float((x * x) @ w) - float((Bf * Bf / Vf).sum())
    return float(np.sqrt(1.0 / Vf[0] + (Bf[0] / Vf[0]) ** 2 / S))


se65 = textbook_se(65.0)
check("recorded 65 units higher, the textbook standard error of Alder's gamma becomes 38 and the test collapses to 0.02 (blueprint)",
      round(se65) == 38 and round(gap["Alder"] / se65, 2) == 0.02 and abs(textbook_se(0.0) - E9["share"]["text_se"][0]) < 1e-6, f"{se65:.2f}, {gap['Alder'] / se65:.4f}")
check("with the standard error at the average case mix it stays 2.02, however the factor is recorded (Episode 9)", round(z_wald["Alder"], 2) == 2.02)
below = NormalDist(E["Elm"], sd["Elm"]).cdf(0.0)
check("Elm expects fewer than two readmissions (1.97); a bell curve centred there puts 6% of itself below zero", E["Elm"] < 2 and round(E["Elm"], 2) == 1.97 and round(100 * below) == 6, f"{below:.4f}")
CROWDS = 50
hits = {m: [0, 0] for m in ("exact", "bell", "ruler")}                                # flagged overall, flagged among providers under 50 patients
n_tests, n_small = 0, 0
for j in range(CROWDS):                                                            # the same fifty level crowds as Episode 13
    c = simulate(seed=3000 + 10 * j, tau=0.0, plant=0.0)
    F = joint_fit(c, max_iter=30)
    g0 = float(np.median(F["gamma"]))
    p0 = expit(g0 + F["X"] @ F["beta"])
    m = len(F["gamma"])
    obs = np.bincount(F["prov"], weights=F["y"], minlength=m)
    e0, v0 = np.bincount(F["prov"], weights=p0, minlength=m), np.bincount(F["prov"], weights=p0 * (1 - p0), minlength=m)
    flag_bell = np.abs((obs - e0) / np.sqrt(v0)) > 1.959964
    flag_ruler = np.abs((F["gamma"] - g0) / case_mix_se(F)) > 1.959964
    starts = np.concatenate([[0], np.cumsum(c["n"])])
    flag_exact = np.array([mid_p(coin_pmf(p0[starts[i]:starts[i + 1]]), int(obs[i])) < 0.05 for i in range(m)])
    small = c["n"] < 50
    for name, f in (("exact", flag_exact), ("bell", flag_bell), ("ruler", flag_ruler)):
        hits[name][0] += int(f.sum()); hits[name][1] += int(f[small].sum())
    n_tests += m; n_small += int(small.sum())
rate = {k: v[0] / n_tests for k, v in hits.items()}
small_rate = {k: v[1] / n_small for k, v in hits.items()}
check("the exact test's rates match Episode 13's run of the same fifty crowds", abs(rate["exact"] - E13["calibration"]["rate"]) < 1e-12 and abs(small_rate["exact"] - E13["calibration"]["small_rate"]) < 1e-12)
check("among level-crowd providers under 50 patients: exact 4.7%, bell curve 4.9%, ruler 4.0% (blueprint's larger run: 4.6%, 4.7%, 4.0%)",
      (round(100 * small_rate["exact"], 1), round(100 * small_rate["bell"], 1), round(100 * small_rate["ruler"], 1)) == (4.7, 4.9, 4.0),
      f"{100 * small_rate['exact']:.2f}, {100 * small_rate['bell']:.2f}, {100 * small_rate['ruler']:.2f} of {n_small}")
check("over all 10,000 tests the three flag 4.8%, 4.9% and 4.5% (blueprint's larger run: 4.99%, 5.00%, 4.67%)",
      (round(100 * rate["exact"], 1), round(100 * rate["bell"], 1), round(100 * rate["ruler"], 1)) == (4.8, 4.9, 4.5), str({k: round(100 * v, 2) for k, v in rate.items()}))
check("the ruler flags the fewest small providers", small_rate["ruler"] < min(small_rate["exact"], small_rate["bell"]))

# ----------------------------------------------------------------------------- 7. which one, when (S08)
expected = lambda g: float(coins("Alder", g).sum())
spread = lambda g: sqrt(float((coins("Alder", g) * (1 - coins("Alder", g))).sum()))


def score_edge(target, lo=-8.0, hi=8.0):
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if (OBS["Alder"] - expected(mid)) / spread(mid) > target else (lo, mid)
    return 0.5 * (lo + hi)


iv_score = (expected(score_edge(1.959964)) / E["Alder"], expected(score_edge(-1.959964)) / E["Alder"])
iv = {"exact": E13["ratio_interval"]["Alder"], "bell": list(iv_score), "ruler": E11["link"]["ratio_interval"]}
check("each test turns inside out into an interval for Alder's ratio: 1.04 to 2.26, 1.07 to 2.25, 1.02 to 2.31 (blueprint)",
      [fl(iv[k], 2) for k in ("exact", "bell", "ruler")] == [[1.04, 2.26], [1.07, 2.25], [1.02, 2.31]], str({k: fl(v) for k, v in iv.items()}))
ci_score = PK.calculate_confidence_intervals(option="SM", stdz="indirect", measure="ratio", test_method="score")["indirect_ratio"].set_index("provider_id").loc["Alder"]
check("pprof_py's score interval for Alder's ratio agrees", abs(float(ci_score["ci_ratio_lower"]) - iv_score[0]) < 2e-3 and abs(float(ci_score["ci_ratio_upper"]) - iv_score[1]) < 2e-3,
      f"{float(ci_score['ci_ratio_lower']):.4f}, {float(ci_score['ci_ratio_upper']):.4f}")
check("the exact test is pprof_py's default for flags", inspect.signature(LogisticFixedEffectModel.test).parameters["test_method"].default == "poibin_exact")

OUT = {
    "episode": 14, "title": "Three Shortcuts", "clinics": ALL, "reference": ref, "fit": {"beta": beta, "gamma": g_fit},
    "cast": {k: {"low": N0[k], "high": N1[k], "observed": OBS[k], "expected": E[k], "sd": sd[k]} for k in ALL},
    "pmf": {k: E13["pmf"][k] for k in ALL},
    "alder": {"expected": E["Alder"], "sd": sd["Alder"], "above": OBS["Alder"] - E["Alder"], "gap": gap["Alder"], "se": se["Alder"]},
    "p": {"exact": p_exact, "bell": p_score, "ruler": p_wald, "flip": p_boot}, "z": {"exact": z_exact, "bell": z_score, "ruler": z_wald},
    "flip": {"seed": SEED, "draws": DRAWS, "stages": {str(k): v for k, v in stages.items()}, "resolution": 1.0 / DRAWS, "package": float(t_boot.loc["Alder", "p_value"])},
    "elm": {"z_other_routine": z_elm_turns, "below_zero": below},
    "trap": {"shift": 65, "se": se65, "z": gap["Alder"] / se65, "z_case_mix": z_wald["Alder"]},
    "calibration": {"crowds": CROWDS, "tests": n_tests, "small_tests": n_small, "rate": rate, "small_rate": small_rate},
    "interval": iv, "ratio": E11["ratio"]["Alder"],
}

if __name__ == "__main__":
    print("z  exact", fl([z_exact[k] for k in ALL])); print("z  bell ", fl([z_score[k] for k in ALL])); print("z  ruler", fl([z_wald[k] for k in ALL]))
    print("p  exact", fl([p_exact[k] for k in ALL], 4)); print("p  bell ", fl([p_score[k] for k in ALL], 4)); print("p  ruler", fl([p_wald[k] for k in ALL], 4))
    print(f"flip      {p_boot:.4f} from {DRAWS} rounds; package {float(t_boot.loc['Alder', 'p_value']):.4f}")
    print(f"trap      SE {se65:.2f}, z {gap['Alder'] / se65:.4f}; Elm's ruler z after the other routine {z_elm_turns:.3f}; bell curve below zero {below:.4f}")
    print("rates    ", {k: round(100 * v, 2) for k, v in rate.items()}, " under 50:", {k: round(100 * v, 2) for k, v in small_rate.items()}, f"({n_small} providers)")
    print("intervals", {k: fl(v) for k, v in iv.items()})
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e14_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
