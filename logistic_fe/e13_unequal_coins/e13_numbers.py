"""Model in Motion · The Logistic Fixed-Effect Model · Episode 13: Unequal coins.

Every number the episode shows or says is computed here, checked, and written to e13_numbers.json.
Scenes and narration read e13_numbers.json; nothing numeric is typed into scene code or the script.

    python e13_numbers.py        # from this folder: prints the ledger, runs every check, writes e13_numbers.json
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from math import comb
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, coin_pmf, expit, fit, mid_p, rows  # noqa: E402
from mim.crowd import joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

ALL = list(CAST)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
SEED, ROUNDS = 2026, 2000


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta, cov4, ll_fit = fit()
E11 = json.loads((HERE.parent / "e11_swap_the_curve" / "e11_numbers.json").read_text())
ref = E11["reference"]["gamma"]
N0 = {k: CAST[k][0] for k in ALL}; N1 = {k: CAST[k][2] for k in ALL}
OBS = {k: CAST[k][1] + CAST[k][3] for k in ALL}
SIZE = {k: N0[k] + N1[k] for k in ALL}
coins = lambda k, g=ref: np.array([float(expit(g))] * N0[k] + [float(expit(g + beta))] * N1[k])       # one coin per patient, at level g
expected = lambda k, g=ref: float(coins(k, g).sum())
PMF = {k: coin_pmf(coins(k)) for k in ALL}

# ----------------------------------------------------------------------------- 1. the question (S01)
check("Alder: 13 readmissions where the reference expects 8 (8.02)", OBS["Alder"] == 13 and round(expected("Alder"), 2) == 8.02)
raw = {k: OBS[k] / SIZE[k] for k in ALL}
check("Dune: 12 patients, 7 readmissions against 4.8 expected, the highest raw rate in the cast (58%)", (SIZE["Dune"], OBS["Dune"]) == (12, 7) and round(expected("Dune"), 2) == 4.8
      and max(raw, key=raw.get) == "Dune" and round(100 * raw["Dune"]) == 58)

# ----------------------------------------------------------------------------- 2. twelve coins (S03)
p_lo, p_hi = float(expit(ref)), float(expit(ref + beta))
check("at the reference a lower-risk patient's coin comes up 18% of the time and a higher-risk patient's 62%; Dune has six of each",
      (round(100 * p_lo), round(100 * p_hi), N0["Dune"], N1["Dune"]) == (18, 62, 6, 6))
flips = np.random.default_rng(SEED).random((ROUNDS, SIZE["Dune"])) < coins("Dune")
tally = flips.sum(axis=1)
check("the first three rounds of the seeded flips give 3, 5 and 3 readmissions", tally[:3].tolist() == [3, 5, 3], str(tally[:6].tolist()))
check("after two thousand rounds the counts average 4.8 and 13% of them are 7 or more", round(float(tally.mean()), 1) == 4.8 and round(100 * float(np.mean(tally >= 7))) == 13,
      f"mean {tally.mean():.3f}; share at 7 or more {np.mean(tally >= 7):.4f}")
stages = {n: np.bincount(tally[:n], minlength=13).tolist() for n in (20, 200, ROUNDS)}

# ----------------------------------------------------------------------------- 3. no need to flip (S04)
dune = PMF["Dune"]
BLUEPRINT_DUNE = [0.0009, 0.0101, 0.0489, 0.1342, 0.2305, 0.2575, 0.1895, 0.0920, 0.0294, 0.0061, 0.0008, 0.0001, 0.0000]
check("built one coin at a time, Dune's pile matches the blueprint's table to four decimals", np.allclose(dune, BLUEPRINT_DUNE, atol=6e-5))
partial = [coin_pmf(coins("Dune")[:k]).tolist() for k in range(SIZE["Dune"] + 1)]
check("each coin splits every bar: the part that stays is one minus its chance, the part that moves right is its chance",
      all(np.allclose(np.array(partial[k + 1]), np.append(np.array(partial[k]) * (1 - coins("Dune")[k]), 0.0) + np.insert(np.array(partial[k]) * coins("Dune")[k], 0, 0.0)) for k in range(12)))
flat = np.zeros(13)
for mask in range(1 << 12):                                                      # every one of the 4,096 ways twelve coins can land
    bits = np.array([(mask >> j) & 1 for j in range(12)])
    flat[bits.sum()] += float(np.prod(np.where(bits == 1, coins("Dune"), 1 - coins("Dune"))))
check("and it agrees with adding up all 4,096 ways twelve coins can land", np.allclose(flat, dune, atol=1e-12))
check("the pile is centred on 4.8 with variance 2.29", abs(float(np.arange(13) @ dune) - 4.8) < 1e-9 and round(float(((np.arange(13) - 4.8) ** 2) @ dune), 2) == 2.29)
check("the chance of exactly 5 is 26%, of 6 19%, of 7 9%, and of 8 or more 4% (blueprint)",
      [round(100 * v) for v in (dune[5], dune[6], dune[7], dune[8:].sum())] == [26, 19, 9, 4], str(fl([dune[5], dune[6], dune[7], dune[8:].sum()], 4)))
check("two thousand flips come close to it: every bar within 2.5 points", np.max(np.abs(np.array(stages[ROUNDS]) / ROUNDS - dune)) < 0.025,
      f"largest gap {np.max(np.abs(np.array(stages[ROUNDS]) / ROUNDS - dune)):.4f}")

# ----------------------------------------------------------------------------- 4. how surprising is seven? (S05)
o = OBS["Dune"]
tail, beyond, half = float(dune[o:].sum()), float(dune[o + 1:].sum()), 0.5 * float(dune[o])
p_dune = mid_p(dune, o)
check("the chance of 7 or more is 13% (0.128)", round(tail, 3) == 0.128)
check("half of the bar at 7 plus everything beyond is 8% (0.046 + 0.036 = 0.082); doubled, 16% (0.165) (blueprint)",
      (round(half, 3), round(beyond, 3), round(half + beyond, 3), round(p_dune, 3)) == (0.046, 0.036, 0.082, 0.165) and round(100 * p_dune) == 16, f"{p_dune:.4f}")
check("about one time in six: not flagged at 5%", abs(1 / p_dune - 6) < 0.1 and p_dune > 0.05, f"1 in {1 / p_dune:.2f}")

# ----------------------------------------------------------------------------- 5. Alder's thirty coins (S06)
alder = PMF["Alder"]
p_val = {k: mid_p(PMF[k], OBS[k]) for k in ALL}
check("Alder: thirty coins, 24 at 18% and 6 at 62%, a pile centred on 8", (SIZE["Alder"], N0["Alder"], N1["Alder"]) == (30, 24, 6) and round(float(np.arange(31) @ alder), 2) == 8.02)
check("the chance of 13 or more is two and a half percent (0.025) and the p-value is 3.5% (0.035): flagged (blueprint)",
      round(float(alder[13:].sum()), 3) in (0.025, 0.026) and abs(float(alder[13:].sum()) - 0.0255) < 1e-4 and round(p_val["Alder"], 3) == 0.035 and p_val["Alder"] < 0.05, f"{alder[13:].sum():.4f}, {p_val['Alder']:.4f}")
check("the others: Birch 45%, Cedar 99%, Elm 11% (blueprint: 0.45, 0.99, 0.114)", [round(100 * p_val[k]) for k in ("Birch", "Cedar", "Elm")] == [45, 99, 11],
      str(fl([p_val[k] for k in ALL], 4)))
check("Elm's p-value is its whole bar at zero", abs(p_val["Elm"] - float(PMF["Elm"][0])) < 1e-12 and round(float(PMF["Elm"][0]), 3) == 0.114)
check("only Alder is flagged; the clinic with the highest raw rate, Dune, is not", [k for k in ALL if p_val[k] < 0.05] == ["Alder"])
PK = LogisticFixedEffectModel().fit(pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y}), y_var="y", x_vars=["x"], provider_var="clinic")
tests = PK.test(test_method="poibin_exact")
check("pprof_py's exact test gives the same five p-values and the same single flag", all(abs(float(tests.loc[k, "p_value"]) - p_val[k]) < 2e-5 for k in ALL)
      and [k for k in ALL if int(tests.loc[k, "flag"]) != 0] == ["Alder"], str(fl([float(tests.loc[k, "p_value"]) for k in ALL], 4)))

# ----------------------------------------------------------------------------- 6. why unequal matters (S07)
def equal(k):
    n, p = SIZE[k], expected(k) / SIZE[k]
    return np.array([comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(n + 1)])


var = lambda f: float(((np.arange(len(f)) - float(np.arange(len(f)) @ f)) ** 2) @ f)
eq = {k: equal(k) for k in ("Dune", "Alder")}
check("identical coins with the same average spread wider: variance 2.88 against 2.29 for Dune (blueprint), 5.88 against 4.94 for Alder",
      (round(var(eq["Dune"]), 2), round(var(dune), 2), round(var(eq["Alder"]), 2), round(var(alder), 2)) == (2.88, 2.29, 5.88, 4.94))
p_equal = {k: mid_p(eq[k], OBS[k]) for k in eq}
check("with identical coins Alder's p-value rises from 3.5% to 5.2% and it is no longer flagged; Dune's goes from 16% to 22%",
      round(100 * p_equal["Alder"], 1) == 5.2 and p_equal["Alder"] > 0.05 and round(100 * p_equal["Dune"]) == 22, f"{p_equal['Alder']:.4f}, {p_equal['Dune']:.4f}")
check("the identical coin for Alder comes up 27% of the time", round(100 * expected("Alder") / 30) == 27)

# ----------------------------------------------------------------------------- 7. turn the test inside out (S08)
def one_sided(k, g, upper):
    f = coin_pmf(coins(k, g)); o_ = OBS[k]
    return float(f[o_ + 1:].sum() + 0.5 * f[o_]) if upper else float(f[:o_].sum() + 0.5 * f[o_])


def solve(k, upper, lo=-12.0, hi=8.0):
    """The gamma at which the observed count sits exactly on the edge of a 2.5% tail."""
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        v = one_sided(k, mid, upper)
        lo, hi = (mid, hi) if (v < 0.025) == upper else (lo, mid)
    return 0.5 * (lo + hi)


interval = {k: (solve(k, True) if OBS[k] > 0 else float("-inf"), solve(k, False)) for k in ALL}
check("Alder's 13 sits on the edge of the tail at gamma = -1.46 and at +0.13: its exact 95% interval (blueprint)", (round(interval["Alder"][0], 2), round(interval["Alder"][1], 2)) == (-1.46, 0.13),
      f"{interval['Alder'][0]:.4f}, {interval['Alder'][1]:.4f}")
check("at both ends of that interval the p-value is exactly 5%", all(abs(mid_p(coin_pmf(coins("Alder", g)), 13) - 0.05) < 1e-9 for g in interval["Alder"]))
check("the reference, -1.52, lies just outside Alder's interval and inside the other four: the same verdicts as the flags",
      ref < interval["Alder"][0] and all(interval[k][0] < ref < interval[k][1] for k in ("Birch", "Cedar", "Dune", "Elm")) and round(ref, 2) == -1.52)
check("pprof_py's exact intervals for gamma agree", all(abs(float(tests.loc[k, "ci_upper"]) - interval[k][1]) < 2e-3 for k in ALL)
      and all(abs(float(tests.loc[k, "ci_lower"]) - interval[k][0]) < 2e-3 for k in FINITE) and float(tests.loc["Elm", "ci_lower"]) == float("-inf"))
ratio_iv = {k: ((expected(k, interval[k][0]) / expected(k)) if OBS[k] > 0 else 0.0, expected(k, interval[k][1]) / expected(k)) for k in ALL}
check("carried through Episode 11's curve: Alder's ratio between 1.04 and 2.26, Dune's between 0.82 and 2.04, Elm's between 0 and 1.33 (blueprint)",
      fl(ratio_iv["Alder"], 2) == [1.04, 2.26] and fl(ratio_iv["Dune"], 2) == [0.82, 2.04] and fl(ratio_iv["Elm"], 2) == [0.0, 1.33], str({k: fl(v) for k, v in ratio_iv.items()}))
ci = PK.calculate_confidence_intervals(option="SM", stdz="indirect", measure="ratio", test_method="exact")["indirect_ratio"].set_index("provider_id")
check("pprof_py's exact intervals for the ratios agree", all(abs(float(ci.loc[k, "ci_ratio_lower"]) - ratio_iv[k][0]) < 2e-3 and abs(float(ci.loc[k, "ci_ratio_upper"]) - ratio_iv[k][1]) < 2e-3 for k in ALL))
check("Episode 11's shortcut interval for Alder was 1.02 to 2.31: close, not the same", fl(E11["link"]["ratio_interval"], 2) == [1.02, 2.31])
slide = [float(v) for v in np.linspace(ref, interval["Alder"][1], 61)]
p_slide = [mid_p(coin_pmf(coins("Alder", g)), 13) for g in slide]
check("as gamma slides from the reference up to Alder's own value the p-value climbs to 1, then falls back to 5% at the far end",
      abs(max(p_slide) - 1.0) < 0.02 and abs(slide[int(np.argmax(p_slide))] - g_fit["Alder"]) < 0.06 and abs(p_slide[-1] - 0.05) < 1e-9, f"peak {max(p_slide):.3f} at {slide[int(np.argmax(p_slide))]:.3f}")

# ----------------------------------------------------------------------------- 8. what the p-value promises (S09)
CROWDS = 50
flagged, small_flagged, small_n, n_tests = 0, 0, 0, 0
for j in range(CROWDS):                                                           # level crowds: every provider truly at the same level, no planted outliers
    c = simulate(seed=3000 + 10 * j, tau=0.0, plant=0.0)
    F = joint_fit(c, max_iter=30)
    g0 = float(np.median(F["gamma"]))
    p0 = expit(g0 + F["X"] @ F["beta"])
    obs = np.bincount(F["prov"], weights=F["y"], minlength=len(F["gamma"])).astype(int)
    starts = np.concatenate([[0], np.cumsum(c["n"])])
    for i in range(len(obs)):
        pv = mid_p(coin_pmf(p0[starts[i]:starts[i + 1]]), int(obs[i]))
        hit = pv < 0.05
        flagged += hit; n_tests += 1
        if c["n"][i] < 50:
            small_flagged += hit; small_n += 1
rate, small_rate = flagged / n_tests, small_flagged / small_n
check("in fifty simulated crowds where every provider truly equals the reference, the test flags about 5% of 10,000 (blueprint: 4.99% of 20,000)",
      n_tests == 10000 and 0.044 < rate < 0.056, f"{100 * rate:.2f}%")
check("among providers with fewer than 50 patients it flags a little under 5% (blueprint: 4.6%)", 0.035 < small_rate < 0.056, f"{100 * small_rate:.2f}% of {small_n}")

OUT = {
    "episode": 13, "title": "Unequal Coins", "clinics": ALL, "reference": {"gamma": ref, "p_low": p_lo, "p_high": p_hi}, "fit": {"beta": beta, "gamma": g_fit},
    "cast": {k: {"low": N0[k], "high": N1[k], "observed": OBS[k], "size": SIZE[k], "expected": expected(k), "raw": raw[k]} for k in ALL},
    "sim": {"seed": SEED, "rounds": ROUNDS, "first": [[bool(v) for v in row] for row in flips[:3]], "first_counts": tally[:3].tolist(), "stages": {str(k): v for k, v in stages.items()},
            "mean": float(tally.mean()), "tail": float(np.mean(tally >= 7))},
    "pmf": {k: PMF[k].tolist() for k in ALL}, "partial": partial, "equal": {k: eq[k].tolist() for k in eq},
    "dune": {"tail": tail, "beyond": beyond, "half": half, "one_sided": half + beyond, "p": p_dune, "variance": var(dune), "variance_equal": var(eq["Dune"])},
    "alder": {"tail": float(alder[13:].sum()), "p": p_val["Alder"], "p_equal": p_equal["Alder"], "variance": var(alder), "variance_equal": var(eq["Alder"]), "equal_chance": expected("Alder") / 30},
    "p_value": p_val, "p_equal": p_equal, "flagged": [k for k in ALL if p_val[k] < 0.05],
    "interval": {k: [None if not np.isfinite(interval[k][0]) else interval[k][0], interval[k][1]] for k in ALL}, "ratio_interval": {k: list(ratio_iv[k]) for k in ALL},
    "shortcut_interval": E11["link"]["ratio_interval"], "ratio": E11["ratio"], "slide": {"gamma": slide, "p": p_slide},
    "calibration": {"crowds": CROWDS, "tests": n_tests, "rate": rate, "small_rate": small_rate, "small_tests": small_n},
}

if __name__ == "__main__":
    print("Dune pile     ", fl(dune, 4))
    print(f"Dune           tail {tail:.4f}; half bar {half:.4f} + beyond {beyond:.4f} = {half + beyond:.4f}; p {p_dune:.4f}; equal coins p {p_equal['Dune']:.4f}")
    print(f"Alder          tail {alder[13:].sum():.4f}; p {p_val['Alder']:.4f}; equal coins p {p_equal['Alder']:.4f}; variances {var(alder):.3f} and {var(eq['Alder']):.3f}")
    print("p-values      ", {k: round(v, 4) for k, v in p_val.items()})
    print("gamma interval", {k: [None if not np.isfinite(a) else round(a, 3), round(b, 3)] for k, (a, b) in interval.items()})
    print("ratio interval", {k: fl(v) for k, v in ratio_iv.items()})
    print(f"flips          first three {tally[:3].tolist()}; mean {tally.mean():.3f}; 7 or more {np.mean(tally >= 7):.4f}")
    print(f"calibration    {100 * rate:.2f}% of {n_tests}; under 50 patients {100 * small_rate:.2f}% of {small_n}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e13_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
