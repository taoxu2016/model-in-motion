"""Model in Motion · The Logistic Fixed-Effect Model · Episode 7: Climbing the hill.

Every number the episode shows or says is computed here, checked, and written to e07_numbers.json.
Scenes and narration read e07_numbers.json; nothing numeric is typed into scene code or the script.

    python e07_numbers.py        # from this folder: prints the ledger, runs every check, writes e07_numbers.json

The alternating fit below follows pprof_py's BanAlgorithm line for line (one Newton step for every gamma, then one
for beta, each with Armijo backtracking s = 0.01, t = 0.6; gammas clamped to the median +- 10; stop when both
blocks move by less than 1e-8), so that its round counts can be checked against the package itself.
"""
from __future__ import annotations

import json
import sys
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit, rows  # noqa: E402

ALL = list(CAST)
CHECKS: list[tuple[str, bool, str]] = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def counts(name, gamma, beta):
    """(observed, expected, wobble V) for one clinic: V is the sum of p(1 - p), the rate at which expected moves with gamma."""
    n0, e0, n1, e1 = CAST[name]
    p0, p1 = float(expit(gamma)), float(expit(gamma + beta))
    return e0 + e1, n0 * p0 + n1 * p1, n0 * p0 * (1 - p0) + n1 * p1 * (1 - p1)


def ll_clinic(name, gamma, beta):
    n0, e0, n1, e1 = CAST[name]
    t = 0.0
    for n, e, eta in ((n0, e0, gamma), (n1, e1, gamma + beta)):
        if n:
            p = min(max(float(expit(eta)), 1e-300), 1 - 1e-16)
            t += e * np.log(p) + (n - e) * np.log(1 - p)
    return float(t)


g, beta_hat, cov, ll_fit = fit()
N_PAT, N_EV = sum(v[0] + v[2] for v in CAST.values()), sum(v[1] + v[3] for v in CAST.values())
g0 = float(logit(N_EV / N_PAT))

# ----------------------------------------------------------------------------- 1. one slider, one step: Dune (S03)
start = g["Cedar"]                                         # Dune starts from Cedar's level, with the dial held at its fitted place
steps, cur = [], start
for _ in range(4):
    O, E, V = counts("Dune", cur, beta_hat)
    steps.append({"gamma": cur, "observed": O, "expected": E, "wobble": V, "tilt": O - E, "step": (O - E) / V, "height": ll_clinic("Dune", cur, beta_hat)})
    cur = cur + (O - E) / V
check("Dune from Cedar's level: observed 7, expected 4.8, wobble 2.29 (blueprint)",
      steps[0]["observed"] == 7 and round(steps[0]["expected"], 1) == 4.8 and round(steps[0]["wobble"], 2) == 2.29, f"{steps[0]['expected']:.3f}, {steps[0]['wobble']:.3f}")
check("first step: 2.2 over 2.29 is 0.96, landing at -0.56 (blueprint: -0.564)",
      round(steps[0]["tilt"], 1) == 2.2 and round(steps[0]["step"], 2) == 0.96 and abs(steps[1]["gamma"] + 0.564) < 5e-4, f"{steps[0]['step']:.4f} -> {steps[1]['gamma']:.4f}")
check("second step: -0.017, landing on -0.580 (blueprint); the third moves less than 0.0001",
      round(steps[1]["step"], 3) == -0.017 and abs(steps[2]["gamma"] - g["Dune"]) < 5e-4 and abs(steps[2]["step"]) < 1e-4, f"{steps[1]['step']:.4f} -> {steps[2]['gamma']:.4f}; then {steps[2]['step']:.1e}")
# the parabola with the same slope and curvature really does peak at the next guess
check("the parabola's slope is the tilt and its curvature is the wobble (numerical derivatives of Dune's height)",
      abs((ll_clinic("Dune", start + 1e-5, beta_hat) - ll_clinic("Dune", start - 1e-5, beta_hat)) / 2e-5 - steps[0]["tilt"]) < 1e-6
      and abs(-(ll_clinic("Dune", start + 1e-4, beta_hat) - 2 * ll_clinic("Dune", start, beta_hat) + ll_clinic("Dune", start - 1e-4, beta_hat)) / 1e-8 - steps[0]["wobble"]) < 1e-3)
pc = (float(expit(start)), float(expit(start + beta_hat)))
wob = {"low": pc[0] * (1 - pc[0]), "high": pc[1] * (1 - pc[1]), "at_half": 0.25, "at_two_percent": 0.02 * 0.98}
check("wobble per patient: 0.15 at 18%, 0.24 at 62%, 0.25 at most (at 50%), 0.02 at 2%",
      (round(wob["low"], 2), round(wob["high"], 2), round(wob["at_two_percent"], 2)) == (0.15, 0.24, 0.02) and (round(100 * pc[0]), round(100 * pc[1])) == (18, 62))

# ----------------------------------------------------------------------------- 2. the alternating fit, as pprof_py's BAN does it
try:
    from pprof_py.algorithms.logistic.fixed_effect import BaseAlgorithm
    below_noise = BaseAlgorithm._below_noise
except Exception:                                                        # pragma: no cover
    below_noise = lambda predicted, loglik: predicted <= 1e-12 * abs(loglik)

PROV, X01, Y = rows(ALL)
M = len(ALL)


def loglik(gam, beta, x):
    eta = gam[PROV] + x * beta
    return float(np.sum(Y * eta - np.logaddexp(0.0, eta)))


def ban(shift=0.0, centre=False, tol=1e-8, max_iter=20000):
    """Alternating Newton updates. `shift` records the risk factor as shift and shift + 1; `centre` subtracts its mean first."""
    x = X01 + shift
    xbar = float(x.mean()) if centre else 0.0
    xc = x - xbar
    gam, beta, it, gcrit, bcrit = np.full(M, g0), 0.0, 0, np.inf, np.inf
    path = [(beta, (gam - xbar * beta).copy())]
    while it < max_iter and max(gcrit, bcrit) > tol:
        it += 1
        old = gam.copy()
        p = expit(gam[PROV] + xc * beta)
        q = np.maximum(p * (1 - p), 1e-20)
        score = np.bincount(PROV, weights=Y - p, minlength=M)
        dg = score / np.bincount(PROV, weights=q, minlength=M)
        v, l0, lam = 1.0, loglik(gam, beta, xc), float(score @ dg)
        while not (loglik(gam + v * dg, beta, xc) - l0 >= 0.01 * v * lam or below_noise(0.01 * v * lam, l0)):
            v *= 0.6
        gam = gam + v * dg
        med = np.median(gam)
        gam = np.clip(gam, med - 10.0, med + 10.0)
        gcrit = float(np.max(np.abs(gam - old)))
        path.append((beta, (gam - xbar * beta).copy()))                 # after the gamma step
        p = expit(gam[PROV] + xc * beta)
        q = np.maximum(p * (1 - p), 1e-20)
        sb, ib = float(xc @ (Y - p)), float((xc * xc) @ q)
        db = sb / ib
        v, l0, lam = 1.0, loglik(gam, beta, xc), sb * db
        while not (loglik(gam, beta + v * db, xc) - l0 >= 0.01 * v * lam or below_noise(0.01 * v * lam, l0)):
            v *= 0.6
        bcrit = abs(v * db)
        beta = beta + v * db
        path.append((beta, (gam - xbar * beta).copy()))                 # after the beta step
    return it, beta, gam - xbar * beta, path


r_plain, b_plain, g_plain, path_plain = ban()
r_cent, b_cent, g_cent, _ = ban(centre=True)
r_five, b_five, g_five, _ = ban(shift=5.0)
r_five_c, _, _, _ = ban(shift=5.0, centre=True)
stops = {"plain": abs(b_plain - beta_hat), "centred": abs(b_cent - beta_hat), "five_higher": abs(b_five - beta_hat)}
check("every alternating route climbs toward the same top and stops a hair short of it: within 0.0003 of beta, worst when the coding is worst",
      max(stops.values()) < 3e-4 and stops["five_higher"] > stops["centred"] and all(abs(g_plain[i] - g[k]) < 1e-3 for i, k in enumerate(FINITE)),
      ", ".join(f"{k} {v:.1e}" for k, v in stops.items()))
check("with the risk factor centred first, as pprof_py does, the cast takes 21 rounds (blueprint)", r_cent == 21, f"{r_cent}")
check("recorded five units higher, plain alternation takes 3,125 rounds (blueprint); centred, still 21", r_five == 3125 and r_five_c == 21, f"{r_five}, {r_five_c}")
p_five = [float(expit(g_five[i] + b_five * (5 + xx))) for i in range(4) for xx in (0, 1)]
p_true = [float(expit(g[k] + beta_hat * xx)) for k in FINITE for xx in (0, 1)]
check("recording the factor five units higher changes no fitted probability (largest difference under 0.001)",
      max(abs(a - b) for a, b in zip(p_five, p_true)) < 1e-3, f"{max(abs(a - b) for a, b in zip(p_five, p_true)):.1e}")
PKG = None
try:
    import logging
    logging.disable(logging.CRITICAL)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        import pandas as pd
        from pprof_py import LogisticFixedEffectModel
        df = pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y})
        PKG = {}
        for alg in ("Ban", "Serbin"):
            mod = LogisticFixedEffectModel(algorithm=alg).fit(df, y_var="y", x_vars=["x"], provider_var="clinic")
            PKG[alg] = {"rounds": int(mod.algorithm.iter), "beta": float(np.ravel(mod.coefficients_["beta"])[0])}
    check("pprof_py itself: its alternating fit takes the same 21 rounds and stops on the same beta as this file's copy of it",
          PKG["Ban"]["rounds"] == r_cent and abs(PKG["Ban"]["beta"] - b_cent) < 1e-9, f"{PKG['Ban']['rounds']} rounds; beta differs by {abs(PKG['Ban']['beta'] - b_cent):.1e}")
    check("pprof_py's joint method reaches the top in 5 steps", PKG["Serbin"]["rounds"] == 5 and abs(PKG["Serbin"]["beta"] - beta_hat) < 1e-6)
except Exception as err:                                                 # pragma: no cover
    check("pprof_py's own round count compared", False, repr(err)[:120])

# the first round, shown on the machine (plain coding)
first = {k: {"observed": counts(k, g0, 0.0)[0], "expected": counts(k, g0, 0.0)[1], "wobble": counts(k, g0, 0.0)[2],
             "step": (counts(k, g0, 0.0)[0] - counts(k, g0, 0.0)[1]) / counts(k, g0, 0.0)[2]} for k in ALL}
check("round one, every clinic at once: steps of +0.11, +0.24, -0.03, +0.73 and -1.69",
      [round(first[k]["step"], 2) for k in ALL] == [0.11, 0.24, -0.03, 0.73, -1.69], str([round(first[k]["step"], 3) for k in ALL]))
check("their wobbles are the blueprint's 7.245, 7.245, 4.830, 2.898, 2.656", [round(first[k]["wobble"], 3) for k in ALL] == [7.245, 7.245, 4.830, 2.898, 2.656])
check("a clinic's step uses only its own patients: the plain path's first gamma step equals these five steps",
      np.allclose(path_plain[1][1] - path_plain[0][1], [first[k]["step"] for k in ALL], atol=1e-12))
rounds_plain = [{"beta_before": path_plain[2 * r][0], "gamma_after": [float(v) for v in path_plain[2 * r + 1][1]], "beta_after": path_plain[2 * r + 2][0]}
                for r in range(min(8, r_plain))]
check("plain alternation crawls: the dial reads 0.68 after one round and only 1.91 after eight; 54 rounds in all",
      round(rounds_plain[0]["beta_after"], 2) == 0.68 and round(rounds_plain[7]["beta_after"], 2) == 1.91 and r_plain == 54,
      str([round(r["beta_after"], 2) for r in rounds_plain]))

# ----------------------------------------------------------------------------- 2b. sliders and dial together (the teaser, S07)
def joint(tol=1e-8, max_iter=50):
    """Newton's step for every gamma and beta at once, solved through the Schur complement."""
    gam, beta, path, schur = np.full(M, g0), 0.0, [], []
    path.append((beta, gam.copy()))
    for it in range(1, max_iter + 1):
        p = expit(gam[PROV] + X01 * beta)
        w, r = p * (1 - p), Y - p
        Ug, Igg = np.bincount(PROV, weights=r, minlength=M), np.bincount(PROV, weights=w, minlength=M)
        Igb = np.bincount(PROV, weights=w * X01, minlength=M)
        S = float((X01 * X01) @ w) - float(Igb @ (Igb / Igg))
        db = (float(X01 @ r) - float(Igb @ (Ug / Igg))) / S
        gam, beta = gam + (Ug - Igb * db) / Igg, beta + db
        path.append((beta, gam.copy()))
        schur.append(S)
        if abs(db) < tol:
            break
    return it, path, schur


j_steps, j_path, j_schur = joint()
check("stepping together: the first joint step takes the dial to 1.81 and Birch to -1.58 (blueprint: 1.8116, -1.5786)",
      abs(j_path[1][0] - 1.8116) < 5e-5 and abs(j_path[1][1][1] + 1.5786) < 5e-5 and abs(j_schur[0] - 4.250) < 5e-4, f"{j_path[1][0]:.4f}, {j_path[1][1][1]:.4f}")
check("stepping together reaches the top in 5 steps, as pprof_py's joint method does",
      j_steps == 5 and abs(j_path[-1][0] - beta_hat) < 1e-9 and (PKG is None or PKG["Serbin"]["rounds"] == j_steps), f"{j_steps}")

# ----------------------------------------------------------------------------- 3. Elm (S05)
elm, cur = [], g0
for _ in range(5):
    p = float(expit(cur))
    cur = cur - 1.0 / (1.0 - p)                                           # (0 - n p) / (n p (1 - p))
    elm.append(cur)
check("Elm steps down by about one unit each round, with no end: -2.06, -3.19, -4.23, -5.24, -6.25 (blueprint)",
      [round(v, 2) for v in elm] == [-2.06, -3.19, -4.23, -5.24, -6.25] and np.allclose([path_plain[2 * r + 1][1][4] for r in range(5)], elm, atol=1e-9))

# ----------------------------------------------------------------------------- 4. the staircase picture (S06): beta against Birch's gamma
def best_height(name, beta):
    a, b = -25.0, 25.0
    for _ in range(120):
        m = (a + b) / 2
        O, E, _ = counts(name, m, beta)
        a, b = (m, b) if O - E > 0 else (a, m)
    return ll_clinic(name, (a + b) / 2, beta)


BG, GG = np.linspace(-0.2, 3.2, 69), np.linspace(-3.3, 0.5, 77)
others = np.array([sum(best_height(k, bv) for k in ("Alder", "Cedar", "Dune")) for bv in BG])
Z = np.array([[ll_clinic("Birch", gv, bv) + others[j] for j, bv in enumerate(BG)] for gv in GG])
levels = [ll_fit - d for d in (12.0, 8.0, 5.0, 2.5, 1.0, 0.25)]
from contourpy import contour_generator  # noqa: E402
cg = contour_generator(x=BG, y=GG, z=Z)
contours = []
for lv in levels:
    for line in cg.lines(lv):
        if len(line) >= 8:
            step_ = max(1, len(line) // 90)
            pts = [[round(float(a), 3), round(float(b), 3)] for a, b in line[::step_]] + [[round(float(line[-1][0]), 3), round(float(line[-1][1]), 3)]]
            contours.append({"below_top": round(ll_fit - lv, 2), "points": pts})
ridge = [[round(float(bv), 3), round(float(GG[np.argmax(Z[:, j])]), 3)] for j, bv in enumerate(BG)]
stair = [[round(float(b_), 4), round(float(gv[1]), 4)] for b_, gv in path_plain[: 2 * min(r_plain, 40) + 1]]
check("the top of the map is the fit: beta 2.02, Birch's gamma -1.82", abs(BG[np.unravel_index(np.argmax(Z), Z.shape)[1]] - beta_hat) < 0.06
      and abs(GG[np.unravel_index(np.argmax(Z), Z.shape)[0]] - g["Birch"]) < 0.06 and abs(Z.max() - ll_fit) < 0.01)
check("the ridge runs diagonally: as the dial goes up, Birch's best gamma comes down", all(b[1] <= a[1] + 1e-9 for a, b in zip(ridge, ridge[1:])) and ridge[0][1] - ridge[-1][1] > 1.5,
      f"from {ridge[0][1]} to {ridge[-1][1]}")
check("the staircase is a staircase: each half-step moves only the gamma or only the dial",
      all((abs(b[0] - a[0]) < 1e-12) != (abs(b[1] - a[1]) < 1e-12) or (abs(b[0] - a[0]) < 1e-9 and abs(b[1] - a[1]) < 1e-9) for a, b in zip(stair, stair[1:])))

HILL = json.loads((HERE.parent / "e06_fitting_by_balance" / "e06_numbers.json").read_text())["hill"]       # Episode 6's hill, for the cold open
check("Episode 6's hill is the same hill: its top is this fit", abs(HILL["peak_beta"] - beta_hat) < 1e-9 and abs(HILL["peak"] - ll_fit) < 1e-9)

OUT = {
    "episode": 7, "title": "Climbing the Hill", "hill": HILL,
    "fit": {"beta": beta_hat, "gamma": g, "loglik": ll_fit}, "start_gamma": g0,
    "dune": {"start": start, "steps": steps, "wobble_per_patient": wob, "p_low": pc[0], "p_high": pc[1]},
    "first_round": first, "rounds_plain": rounds_plain,
    "stops_short_by": stops, "rounds": {"plain": r_plain, "centred": r_cent, "five_higher": r_five, "five_higher_centred": r_five_c, "package": PKG},
    "elm": elm,
    "joint": {"steps": j_steps, "path": [[round(float(b_), 4), round(float(gv[1]), 4)] for b_, gv in j_path]},
    "map": {"contours": contours, "ridge": ridge, "stair": stair, "beta_range": [float(BG[0]), float(BG[-1])], "gamma_range": [float(GG[0]), float(GG[-1])]},
}

if __name__ == "__main__":
    for k, s in enumerate(steps[:3]):
        print(f"Dune step {k + 1}: at {s['gamma']:+.4f}  O {s['observed']}  E {s['expected']:.3f}  V {s['wobble']:.3f}  step {s['step']:+.4f}")
    print("round one steps:", {k: round(first[k]["step"], 3) for k in ALL})
    print(f"rounds: plain {r_plain}, centred {r_cent}, five higher {r_five} (centred {r_five_c}); package {PKG}")
    print("plain path, dial after each round:", [round(r["beta_after"], 3) for r in rounds_plain])
    print("Elm:", [round(v, 2) for v in elm], " contour lines:", len(contours), " stair points:", len(stair))
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e07_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
