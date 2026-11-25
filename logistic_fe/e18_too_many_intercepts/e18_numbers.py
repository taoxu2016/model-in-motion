"""Model in Motion · The Logistic Fixed-Effect Model · Episode 18: Too many intercepts.

Every number the episode shows or says is computed here, checked, and written to e18_numbers.json.
Scenes and narration read e18_numbers.json; nothing numeric is typed into scene code or the script.

One experiment (blueprint appendix, M18): 4,000 patients, one risk factor x ~ N(0, 1), a true coefficient of 0.5, and
provider intercepts drawn from N(-0.5, 1). The same recipe is run with the patients grouped into providers of 2, 5, 10,
25 and 100, 400 times each, and fitted two ways: jointly, with one intercept per provider (the series' model), and
conditionally on each provider's total (which removes the intercepts).

    python e18_numbers.py        # from this folder: prints the ledger, runs every check, writes e18_numbers.json
"""
from __future__ import annotations

import inspect
import json
import logging
import sys
import warnings
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.special import expit

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.crowd import BETA as CROWD_BETA  # noqa: E402
from mim.crowd import joint_fit, simulate  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
import pprof_py.data.preparation as prep  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]
BETA, TOTAL, SIZES, REPS, SEED = 0.5, 4000, (2, 5, 10, 25, 100), 400, 2026


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def world(rng, size):
    """One world: 4,000 patients in providers of one size. Returns the risk factor and the outcomes, a row per provider."""
    m = TOTAL // size
    g = rng.normal(-0.5, 1.0, m)
    x = rng.normal(size=(m, size))
    return x, (rng.random((m, size)) < expit(g[:, None] + BETA * x)).astype(float)


def joint(x, y, tol=1e-11):
    """The joint fit: one intercept per provider and one shared coefficient, by Newton steps through the fold (Episode 8).

    Providers whose patients all had the same outcome have no finite intercept and tell the fit nothing about the
    coefficient (Episode 10), so they are set aside. Returns the coefficient, its standard error, how many providers
    were set aside, and the fitted intercepts of the rest."""
    s = y.sum(1)
    keep = (s > 0) & (s < y.shape[1])
    x, y = x[keep], y[keep]
    g, b = np.log(y.mean(1) / (1 - y.mean(1))), 0.0
    for _ in range(200):
        p = expit(g[:, None] + b * x)
        w, r = p * (1 - p), y - p
        Ug, V, B = r.sum(1), w.sum(1), (w * x).sum(1)
        S = float((w * x * x).sum() - (B * B / V).sum())
        db = float(((r * x).sum() - (B * Ug / V).sum()) / S)
        dg = (Ug - B * db) / V
        b, g = b + db, g + dg
        if max(abs(db), float(np.max(np.abs(dg)))) < tol:
            break
    p = expit(g[:, None] + b * x)
    w = p * (1 - p)
    V, B = w.sum(1), (w * x).sum(1)
    return b, 1.0 / np.sqrt(float((w * x * x).sum() - (B * B / V).sum())), int((~keep).sum()), g, keep


def conditional(x, y):
    """The conditional fit: given how many of a provider's patients had the event, which ones were they? No intercepts appear."""
    k, (m, n), rows = y.sum(1).astype(int), x.shape, np.arange(x.shape[0])
    sxy = float((x * y).sum())

    def nll(b):
        w = np.exp(b * x)
        e = np.zeros((m, n + 1)); e[:, 0] = 1.0                                   # e[:, k]: the sum, over every way to pick k patients, of the product of their weights
        for j in range(n):
            e[:, 1:j + 2] = e[:, 1:j + 2] + e[:, :j + 1] * w[:, j:j + 1]
        return -(b * sxy - float(np.log(e[rows, k]).sum()))

    return float(minimize_scalar(nll, bounds=(-3.0, 5.0), method="bounded", options={"xatol": 1e-9}).x)


# ----------------------------------------------------------------------------- 1. the experiment
RES, FIRST = {}, {}
for size in SIZES:
    rng = np.random.default_rng([SEED, size])
    bj, se, bc, alike = [], [], [], []
    for rep in range(REPS):
        x, y = world(rng, size)
        b, s, d, g, keep = joint(x, y)
        bj.append(b); se.append(s); alike.append(d); bc.append(conditional(x, y))
        if rep == 0:
            FIRST[size] = {"x": x, "y": y, "beta": b, "se": s, "alike": d, "gamma": g, "keep": keep, "conditional": bc[0]}
    bj, se, bc = np.array(bj), np.array(se), np.array(bc)
    RES[size] = {"ratio": float(bj.mean() / BETA), "ratio_se": float(bj.std(ddof=1) / np.sqrt(REPS) / BETA), "sd": float(bj.std(ddof=1)), "se": float(se.mean()), "coverage": float(np.mean(np.abs(bj - BETA) <= 1.959964 * se)),
                 "conditional": float(bc.mean() / BETA), "conditional_se": float(bc.std(ddof=1) / np.sqrt(REPS) / BETA), "alike": float(np.mean(alike)), "providers": TOTAL // size,
                 "intervals": [[float(a), float(s_)] for a, s_ in zip(bj[:40], se[:40])], "fits": bj.tolist()}

# ----------------------------------------------------------------------------- 2. two thousand pairs (S01, S03)
P = FIRST[2]
check("the world on screen: 2,000 providers of 2 patients, a true coefficient of 0.5", P["x"].shape == (2000, 2) and BETA == 0.5)
check("its joint fit returns 0.92: nearly twice the truth", round(P["beta"], 2) == 0.92, f"{P['beta']:.4f}")
check("over 400 such worlds the fit averages 1.01: twice the truth (blueprint: 2.00 times)", round(RES[2]["ratio"] * BETA, 2) == 1.01 and round(RES[2]["ratio"], 1) == 2.0, f"{RES[2]['ratio'] * BETA:.4f}; ratio {RES[2]['ratio']:.3f} +- {RES[2]['ratio_se']:.3f}")
check("in 1,224 of its 2,000 pairs both patients had the same outcome (on average over worlds, 1,190: blueprint)", P["alike"] == 1224 and round(RES[2]["alike"], -1) == 1190, f"average {RES[2]['alike']:.0f}")
xd, yd = P["x"][P["keep"]], P["y"][P["keep"]]
check("in each of the other 776 pairs the fitted intercept sits exactly midway: minus the coefficient times the pair's average risk factor", len(xd) == 776 and float(np.max(np.abs(P["gamma"] + P["beta"] * xd.mean(1)))) < 1e-8)
pd_ = expit(P["gamma"][:, None] + P["beta"] * xd)
check("so the two fitted chances in such a pair add up to exactly one", float(np.max(np.abs(pd_.sum(1) - 1.0))) < 1e-9)
check("for pairs the joint coefficient is exactly twice the conditional one: 0.9229 against 0.4614", abs(P["beta"] / P["conditional"] - 2.0) < 1e-5 and round(P["conditional"], 4) == 0.4614, f"{P['beta']:.5f}, {P['conditional']:.5f}")

# ----------------------------------------------------------------------------- 3. how large must a provider be? (S04)
ratios = [RES[s]["ratio"] for s in SIZES]
check("regrouped into providers of 5, 10, 25 and 100, the coefficient comes out 26%, 12%, 5% and 1% too steep (blueprint: 24%, 12%, 6%, 1%)",
      [round(100 * (r - 1)) for r in ratios[1:]] == [26, 12, 5, 1], str(fl(ratios)) + " +- " + str(fl([RES[s]["ratio_se"] for s in SIZES])))
excess = [(RES[s]["ratio"] - 1) * s for s in SIZES[1:]]
check("from 5 patients up, the excess is a little over 1 divided by the provider's size: between 1.0 and 1.4, 1.2 on average", all(1.0 < e < 1.4 for e in excess) and round(float(np.mean(excess)), 1) == 1.2, str(fl(excess, 2)))
check("providers whose patients all share one outcome, on average: 1,189 of 2,000 pairs; 163 of 800 fives; 27 of 400 tens; 2 of 160; none of 40", [round(RES[s]["alike"]) for s in SIZES] == [1189, 163, 27, 2, 0], str(fl([RES[s]["alike"] for s in SIZES], 1)))

more = []                                                                         # five times as many providers of the same size: 20,000 patients in fives
rng = np.random.default_rng([SEED, 5, 5])
for _ in range(100):
    m5 = 4000
    g5, x5 = rng.normal(-0.5, 1.0, m5), rng.normal(size=(m5, 5))
    more.append(joint(x5, (rng.random((m5, 5)) < expit(g5[:, None] + BETA * x5)).astype(float))[0])
more_ratio = float(np.mean(more)) / BETA
check("adding providers does not help: 4,000 providers of 5 come out 27% too steep, against 26% for 800 of them", round(100 * (more_ratio - 1)) == 27 and abs(more_ratio - RES[5]["ratio"]) < 0.02,
      f"{more_ratio:.4f} +- {np.std(more, ddof=1) / 10 / BETA:.4f}")
check("single worlds of pairs scatter by about 0.11 around that average", round(RES[2]["sd"], 2) == 0.11, f"{RES[2]['sd']:.4f}")

# ----------------------------------------------------------------------------- 4. no warning (S05)
ses, cover = [RES[s]["se"] for s in SIZES], [RES[s]["coverage"] for s in SIZES]
check("the standard error stays between 0.04 and 0.08 at every size (blueprint)", fl(ses, 2) == [0.08, 0.05, 0.04, 0.04, 0.04], str(fl(ses)))
check("95% intervals hold the truth in none of the worlds of pairs, about a quarter with fives (26%), 71% with tens, and about 90% and 93% above (blueprint: 0%, 32%, 72%, 85%, 97%)",
      cover[0] == 0.0 and [round(100 * c) for c in cover[1:3]] == [26, 71] and 0.89 < cover[3] < 0.92 and round(100 * cover[4]) == 93, str(fl(cover)))

# ----------------------------------------------------------------------------- 5. the conditional fit (S06)
cond = [RES[s]["conditional"] for s in SIZES]
check("the conditional fit is within 1% of the truth at every size (blueprint: 0.99 to 1.02)", all(abs(c - 1.0) < 0.01 for c in cond), str(fl(cond)) + " +- " + str(fl([RES[s]["conditional_se"] for s in SIZES])))

# ----------------------------------------------------------------------------- 6. in practice (S07)
W = FIRST[10]                                                                     # a world of tens: large enough to pass the package's cutoff, small enough to hold providers with one outcome only
df = pd.DataFrame({"prov": np.repeat(np.arange(W["x"].shape[0]), 10), "x": W["x"].ravel(), "y": W["y"].ravel()})
PK = LogisticFixedEffectModel(cutoff=9).fit(df, y_var="y", x_vars=["x"], provider_var="prov")   # the default cutoff of 10 would set aside every provider of ten
pk_beta = float(np.asarray(PK.coefficients_["beta"]).ravel()[0])
check("the bias belongs to the method, not the program: pprof_py's fit of one world of tens, holding its 22 one-outcome providers at a wall, gives the same coefficient to five decimals (0.58803)",
      abs(pk_beta - W["beta"]) < 1e-5 and W["alike"] == 22 and round(pk_beta, 5) == 0.58803, f"{pk_beta:.5f} against {W['beta']:.5f}; {W['alike']} of 400 providers had one outcome only")
check("pprof_py keeps a provider only if it has more than its cutoff of 10 patients: 10 or fewer are set aside by default (as Episode 10 said)",
      inspect.signature(LogisticFixedEffectModel.__init__).parameters["cutoff"].default == 10 and '"prov_size"] > self.cutoff' in inspect.getsource(prep))
r1 = []
for j in range(50):
    r1.append(float(joint_fit(simulate(seed=4000 + 10 * j))["beta"][0] / CROWD_BETA[0]))
crowd_ratio, crowd_se = float(np.mean(r1)), float(np.std(r1, ddof=1) / np.sqrt(50))
check("in the series' crowd, 20 to 500 patients a provider, the first coefficient comes out 1% too steep over fifty redraws", round(100 * (crowd_ratio - 1)) == 1 and crowd_ratio - 1 > 2 * crowd_se,
      f"{crowd_ratio:.4f} +- {crowd_se:.4f}")
rng = np.random.default_rng([SEED, 0])
lin = []
for _ in range(100):
    g, x = rng.normal(-0.5, 1.0, 2000), rng.normal(size=(2000, 2))
    yl = g[:, None] + BETA * x + rng.normal(size=(2000, 2))
    xc, yc = x - x.mean(1, keepdims=True), yl - yl.mean(1, keepdims=True)
    lin.append(float((xc * yc).sum() / (xc * xc).sum()))
check("a straight-line model with one intercept per pair has no such bias: 1.00 times the truth", round(float(np.mean(lin)) / BETA, 2) == 1.00, f"{np.mean(lin) / BETA:.4f}")

show = np.where(P["keep"])[0][:3]
pairs = [{"x": fl(P["x"][i], 2), "y": [int(v) for v in P["y"][i]], "gamma": float(-P["beta"] * P["x"][i].mean()), "p": fl(expit(-P["beta"] * P["x"][i].mean() + P["beta"] * P["x"][i]), 3)} for i in show]
OUT = {
    "episode": 18, "title": "Too Many Intercepts", "beta": BETA, "patients": TOTAL, "sizes": list(SIZES), "reps": REPS,
    "pairs": {"providers": 2000, "beta": P["beta"], "conditional": P["conditional"], "alike": P["alike"], "discordant": int(P["keep"].sum()), "average": RES[2]["ratio"] * BETA, "average_alike": RES[2]["alike"],
              "examples": pairs, "outcomes": [[int(v) for v in row] for row in P["y"][:400]], "fits": fl(RES[2]["fits"], 4)},
    "sweep": {str(s): {k: RES[s][k] for k in ("ratio", "ratio_se", "se", "coverage", "conditional", "alike", "providers", "intervals")} for s in SIZES},
    "excess_times_size": float(np.mean(excess)), "more_providers": {"count": 4000, "base": TOTAL // 5, "ratio": more_ratio},
    "practice": {"cutoff": 10, "crowd_ratio": crowd_ratio, "package_beta": pk_beta, "own_beta": W["beta"], "package_world_alike": W["alike"], "linear_ratio": float(np.mean(lin)) / BETA},
}

if __name__ == "__main__":
    for s in SIZES:
        r = RES[s]
        print(f"size {s:3d}  joint {r['ratio']:.3f} +- {r['ratio_se']:.3f}   SE {r['se']:.3f}   coverage {r['coverage']:.3f}   conditional {r['conditional']:.3f} +- {r['conditional_se']:.3f}   all alike {r['alike']:.0f} of {r['providers']}")
    print(f"pairs      first world: joint {P['beta']:.4f}, conditional {P['conditional']:.4f}, alike {P['alike']}")
    print(f"practice   crowd {crowd_ratio:.4f} +- {crowd_se:.4f}; package {pk_beta:.5f} against {W['beta']:.5f}; linear {np.mean(lin) / BETA:.4f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e18_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
