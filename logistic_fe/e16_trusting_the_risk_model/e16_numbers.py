"""Model in Motion · The Logistic Fixed-Effect Model · Episode 16: Trusting the risk model.

Every number the episode shows or says is computed here, checked, and written to e16_numbers.json.
Scenes and narration read e16_numbers.json; nothing numeric is typed into scene code or the script.

Three experiments on the series' crowd (seed 2026), all with the crowd's own patients and its own luck:
  A. the crowd as it is: a risk model of the right form;
  B. the same crowd with a bend added to the truth, 0.3 (x1^2 - 1) on the log-odds, fitted without it and then with it;
  C. the same crowd with its largest provider given a slope of 1.6 instead of 0.8, and an intercept 0.35 lower.

    python e16_numbers.py        # from this folder: prints the ledger, runs every check, writes e16_numbers.json
"""
from __future__ import annotations

import inspect
import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.stats import rankdata

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import coin_pmf, expit, mid_p  # noqa: E402
from mim.crowd import BETA, fit_fixed_effects, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pprof_py.data.preparation as prep  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
SEED, BEND, STEEP, LOWER = 2026, 0.3, 1.6, 0.35


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


c = simulate(seed=SEED)
prov, x1, x2, n = c["prov"], c["x1"], c["x2"], c["n"]
N, M = len(prov), len(n)
luck = np.random.default_rng(SEED + 1).random(N)                                 # the crowd's own uniform draws: one per patient
truth = c["gamma"][prov] + BETA[0] * x1 + BETA[1] * x2
X2, X3 = np.column_stack([x1, x2]), np.column_stack([x1, x2, x1 ** 2])
starts = np.concatenate([[0], np.cumsum(n)])
check("the crowd's outcomes are its own luck applied to its own truth", np.array_equal((luck < expit(truth)).astype(int), c["y"]))


def fitted(X, y):
    g, b, _ = fit_fixed_effects(X, y, prov)
    return g, b, expit(g[prov] + X @ b)


def by_tenths(p, y):
    """Patients in order of predicted risk, cut into ten equal groups: observed, expected and spread for each."""
    groups = np.array_split(np.argsort(p, kind="stable"), 10)
    return [{"n": int(len(g)), "O": float(y[g].sum()), "E": float(p[g].sum()), "V": float((p[g] * (1 - p[g])).sum()), "ratio": float(y[g].sum() / p[g].sum()),
             "z": float((y[g].sum() - p[g].sum()) / np.sqrt((p[g] * (1 - p[g])).sum()))} for g in groups]


def auc(p, y):
    """The chance that a readmitted patient was given a higher predicted risk than one who was not (ties count half)."""
    r, n1 = rankdata(p), float(y.sum())
    return float((r[y == 1].sum() - n1 * (n1 + 1) / 2) / (n1 * (len(y) - n1)))


def meters(p, y):
    return float(np.max(np.abs(np.bincount(prov, weights=y - p, minlength=M))))


def exact_flags(g, b, X, y):
    p0 = expit(float(np.median(g)) + X @ b)
    obs = np.bincount(prov, weights=y, minlength=M)
    flags = np.array([mid_p(coin_pmf(p0[starts[i]:starts[i + 1]]), int(obs[i])) < 0.05 for i in range(M)])
    return flags, obs / np.bincount(prov, weights=p0, minlength=M)


# ----------------------------------------------------------------------------- A. the crowd as it is (S01, S03, S06)
yA = c["y"].astype(float)
gA, bA, pA = fitted(X2, yA)
tA = by_tenths(pA, yA)
check("the crowd: 28,848 patients in 200 providers", (N, M) == (28848, 200))
check("every provider's meter is level: observed equals expected to twelve decimals", meters(pA, yA) < 1e-12, f"largest gap {meters(pA, yA):.1e}")
check("cut by risk into ten groups of 2,884 or 2,885 patients", sorted({t["n"] for t in tA}) == [2884, 2885])
check("for the crowd as it is, observed over expected runs from 0.95 to 1.05 across the tenths (blueprint: 0.955 to 1.048)",
      (round(min(t["ratio"] for t in tA), 2), round(max(t["ratio"] for t in tA), 2)) == (0.95, 1.05), str(fl([t["ratio"] for t in tA])))
check("each tenth is within what luck allows: none is more than 1.96 spreads from level", max(abs(t["z"]) for t in tA) < 1.96, f"largest {max(abs(t['z']) for t in tA):.2f}")

# ----------------------------------------------------------------------------- B. a model that is wrong (S01, S04, S05, S06)
yB = (luck < expit(truth + BEND * (x1 ** 2 - 1))).astype(float)
gL, bL, pL = fitted(X2, yB)                                                       # fitted with a straight line
gQ, bQ, pQ = fitted(X3, yB)                                                       # fitted with the bend
tL, tQ = by_tenths(pL, yB), by_tenths(pQ, yB)
check("the second crowd's provider meters are level too, under the wrong model", meters(pL, yB) < 1e-12, f"largest gap {meters(pL, yB):.1e}")
check("in its lowest-risk tenth the model expects 136 readmissions and there are 339: two and a half times as many (blueprint: 2.47)",
      (round(tL[0]["E"]), round(tL[0]["O"])) == (136, 339) and round(tL[0]["ratio"], 1) == 2.5, f"{tL[0]['O']:.0f} against {tL[0]['E']:.1f}, ratio {tL[0]['ratio']:.3f}")
mid = [t["ratio"] for t in tL[4:7]]
check("in the middle tenths there are more than a fifth fewer than expected: ratios 0.77 to 0.79 (blueprint: 0.79)", fl(sorted(mid), 2) == [0.77, 0.78, 0.79] and max(mid) < 0.8, str(fl(mid)))
check("the straight-line fit puts 0.85 on the first risk factor; with the bend the fit recovers 0.81 and 0.32 for the square (truth 0.8 and 0.3)",
      round(float(bL[0]), 2) == 0.85 and (round(float(bQ[0]), 2), round(float(bQ[2]), 2)) == (0.81, 0.32), f"{fl(bL)}; {fl(bQ)}")
check("give the model the bend and the tenths settle: 0.92 to 1.08 (blueprint: 0.95 to 1.05)", (round(min(t["ratio"] for t in tQ), 2), round(max(t["ratio"] for t in tQ), 2)) == (0.92, 1.08),
      str(fl([t["ratio"] for t in tQ])))
check("after the fix the furthest tenth is 2.2 spreads from level, and only one is past 1.96; before it, the lowest-risk tenth was 18 spreads out",
      round(max(abs(t["z"]) for t in tQ), 1) == 2.2 and sum(abs(t["z"]) > 1.96 for t in tQ) == 1 and round(tL[0]["z"]) == 18,
      f"after: largest {max(abs(t['z']) for t in tQ):.2f}; before: {tL[0]['z']:.1f}")
fL, rL = exact_flags(gL, bL, X2, yB)
fQ, rQ = exact_flags(gQ, bQ, X3, yB)
changed = int((fL != fQ).sum())
check("between the two fits 16 of the 200 providers change their flag (blueprint, on its own draws: 17)", changed == 16, f"{int(fL.sum())} flagged with the line, {int(fQ.sum())} with the bend")
mean_x = np.bincount(prov, weights=x1, minlength=M) / n
unusual = np.zeros(M, dtype=bool)
unusual[np.argsort(-np.abs(mean_x - x1.mean()))[:M // 5]] = True
excess = float(np.mean(rL[unusual] / rQ[unusual]))
check("the fifth of providers with the most unusual case mix had ratios 16% too high under the wrong model (blueprint: 13%); the rest, 1% too low",
      round(100 * (excess - 1)) == 16 and round(100 * (float(np.mean(rL[~unusual] / rQ[~unusual])) - 1)) == -1, f"{excess:.3f}, {np.mean(rL[~unusual] / rQ[~unusual]):.3f}")

# ----------------------------------------------------------------------------- the AUC (S06)
aL, aQ, aA = auc(pL, yB), auc(pQ, yB), auc(pA, yA)
check("the AUC is 0.74 for the wrong model and 0.76 for the corrected one (blueprint: 0.739 and 0.755)", (round(aL, 2), round(aQ, 2)) == (0.74, 0.76), f"{aL:.4f}, {aQ:.4f}")
rng = np.random.default_rng(16)
ev, no = np.where(yB == 1)[0], np.where(yB == 0)[0]
pick_ev, pick_no = rng.choice(ev, 200000), rng.choice(no, 200000)
pairs = (pL[pick_ev] > pL[pick_no]).mean()
sample = [[float(pL[a]), float(pL[b])] for a, b in zip(pick_ev[:4], pick_no[:4])]           # four pairs to show in full
thousand = [bool(v) for v in (pL[pick_ev[:1000]] > pL[pick_no[:1000]])]                    # and the first thousand, as right or wrong
check("of the first thousand of those pairs, 738 have the readmitted patient ranked higher; of the first four, three", sum(thousand) == 738 and sum(thousand[:4]) == 3)
check("that is the chance that a readmitted patient was given the higher risk: 200,000 random pairs agree to two decimals", abs(float(pairs) - aL) < 0.005, f"{pairs:.4f}")


def plain(X, y):
    Z = np.column_stack([np.ones(len(y)), X]); b = np.zeros(Z.shape[1])
    for _ in range(50):
        p = expit(Z @ b); step = np.linalg.solve(Z.T @ (Z * (p * (1 - p))[:, None]), Z.T @ (y - p)); b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    return expit(Z @ b)


a_plain = auc(plain(X2, yA), yA)
check("for the crowd as it is, the AUC is 0.72 without the provider terms and 0.74 with them (blueprint: 0.717 and 0.739)", (round(a_plain, 2), round(aA, 2)) == (0.72, 0.74), f"{a_plain:.4f}, {aA:.4f}")
a_rule = auc(X2 @ bA, yA)                                                        # the fitted rule's own ranking of patients, with every provider term left out
check("rank patients by the fitted risk rule alone and the AUC is still 0.72: the gain to 0.74 comes from knowing the provider, not from a better rule",
      round(a_rule, 2) == 0.72 and abs(a_rule - a_plain) < 0.002, f"{a_rule:.4f}")

# ----------------------------------------------------------------------------- C. one slope for all (S07)
big = int(np.argmax(n))
idx = np.arange(starts[big], starts[big + 1])
yC = yA.copy()
yC[idx] = (luck[idx] < expit(c["gamma"][big] - LOWER + STEEP * x1[idx] + BETA[1] * x2[idx])).astype(float)
gC, bC, pC = fitted(X2, yC)
order = idx[np.argsort(pC[idx], kind="stable")]
low, high = order[:len(idx) // 2], order[len(idx) // 2:]
half = lambda g: (float(yC[g].sum()), float(pC[g].sum()))
check("the largest provider has 484 patients; in this experiment its risk climbs twice as steeply as the shared rule (1.6 against 0.8)", int(n[big]) == 484 and STEEP == 2 * BETA[0] and big not in c["planted_high"] + c["planted_low"])
check("its total balances: 143 observed, 143.0 expected (blueprint, on its own draws: 135)", (yC[idx].sum(), round(float(pC[idx].sum()), 1)) == (143.0, 143.0))
check("but its lower-risk half shows 18 against 41, and its higher-risk half 125 against 102 (blueprint: 18 against 29.2, 117 against 105.8)",
      (half(low)[0], round(half(low)[1]), half(high)[0], round(half(high)[1])) == (18.0, 41, 125.0, 102), f"{half(low)[0]:.0f} against {half(low)[1]:.1f}; {half(high)[0]:.0f} against {half(high)[1]:.1f}")
check("the shared rule itself hardly moves: one provider in 200 cannot bend it", abs(float(bC[0]) - float(bA[0])) < 0.02, f"{bC[0]:.4f} against {bA[0]:.4f}")

# ----------------------------------------------------------------------------- what the software checks first (S08)
src = inspect.getsource(prep).lower()
sig = inspect.signature(LogisticFixedEffectModel.__init__).parameters
check("pprof_py's preparation step checks for missing values, for covariates with zero variance, for correlated pairs (above 0.9) and for variance inflation (above 10)",
      all(k in src for k in ("missing values", "zero variance", "correlation", "variance inflation")) and sig["threshold_cor"].default == 0.9 and sig["threshold_vif"].default == 10)

grid = np.linspace(-3.0, 3.0, 61)
shift = float(np.mean(BETA[0] * x1 + BEND * (x1 ** 2 - 1) - bL[0] * x1))          # so that the fitted line and the true curve agree on average over the patients
OUT = {
    "episode": 16, "title": "Trusting the Risk Model", "patients": N, "providers": M, "tenth_size": tA[0]["n"],
    "meters": {"as_is": meters(pA, yA), "wrong": meters(pL, yB)},
    "tenths": {"as_is": tA, "line": tL, "bend": tQ},
    "bend": {"extra": BEND, "beta_line": fl(bL, 4), "beta_bend": fl(bQ, 4), "grid": grid.tolist(), "true": (BETA[0] * grid + BEND * (grid ** 2 - 1)).tolist(), "line": (float(bL[0]) * grid + shift).tolist()},
    "cost": {"changed": changed, "flag_line": int(fL.sum()), "flag_bend": int(fQ.sum()), "excess": excess, "rest": float(np.mean(rL[~unusual] / rQ[~unusual])),
             "ratio_line": fl(rL, 4), "ratio_bend": fl(rQ, 4), "unusual": [bool(v) for v in unusual], "flip": [bool(v) for v in fL != fQ]},
    "auc": {"wrong": aL, "fixed": aQ, "plain": a_plain, "rule_alone": a_rule, "with_providers": aA, "pairs": sample, "thousand": thousand, "thousand_right": int(sum(thousand))},
    "slope": {"patients": int(n[big]), "steep": STEEP, "shared": float(bC[0]), "true_gamma": float(c["gamma"][big] - LOWER), "fitted_gamma": float(gC[big]),
              "total": [float(yC[idx].sum()), float(pC[idx].sum())], "low": list(half(low)), "high": list(half(high))},
}

if __name__ == "__main__":
    print("as it is  ", fl([t["ratio"] for t in tA]), " largest z", round(max(abs(t["z"]) for t in tA), 2))
    print("the line  ", fl([t["ratio"] for t in tL]), f" lowest tenth {tL[0]['O']:.0f} against {tL[0]['E']:.1f}")
    print("the bend  ", fl([t["ratio"] for t in tQ]), " largest z", round(max(abs(t["z"]) for t in tQ), 2))
    print(f"cost       {changed} flags change ({int(fL.sum())} and {int(fQ.sum())}); unusual fifth {excess:.3f}, rest {np.mean(rL[~unusual] / rQ[~unusual]):.3f}")
    print(f"AUC        wrong {aL:.4f}, fixed {aQ:.4f}; as it is: plain {a_plain:.4f}, with providers {aA:.4f}")
    print(f"slope      total {yC[idx].sum():.0f} against {pC[idx].sum():.1f}; low {half(low)[0]:.0f} against {half(low)[1]:.1f}; high {half(high)[0]:.0f} against {half(high)[1]:.1f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e16_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
