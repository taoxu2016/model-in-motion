"""Model in Motion · The Logistic Fixed-Effect Model · Episode 8: The arrow matrix.

Every number the episode shows or says is computed here, checked, and written to e08_numbers.json.
Scenes and narration read e08_numbers.json; nothing numeric is typed into scene code or the script.

    python e08_numbers.py        # from this folder: prints the ledger, runs every check, writes e08_numbers.json
"""
from __future__ import annotations

import json
import sys
import time
import warnings
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit, rows  # noqa: E402

ALL = list(CAST)
M = len(ALL)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta_hat, cov, ll_fit = fit()
g0 = float(logit(Y.mean()))


def arrow(gam, beta, x=X01):
    """The arrow's three parts at a setting: each clinic's own wobble, its tie to the dial, and the dial's own wobble."""
    p = expit(gam[PROV] + x * beta)
    w = p * (1 - p)
    return np.bincount(PROV, weights=w, minlength=M), np.bincount(PROV, weights=w * x, minlength=M), float((x * x) @ w), w


def loglik(gam, beta, x=X01):
    eta = gam[PROV] + x * beta
    return float(np.sum(Y * eta - np.logaddexp(0.0, eta)))


# ----------------------------------------------------------------------------- 1. the table at the fit (S03)
PKG = None
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import logging
    logging.disable(logging.CRITICAL)
    import pandas as pd
    import pprof_py
    from pprof_py import LogisticFixedEffectModel
    df = pd.DataFrame({"clinic": np.array(ALL)[PROV], "x": X01, "y": Y})
    mod = LogisticFixedEffectModel(algorithm="Serbin").fit(df, y_var="y", x_vars=["x"], provider_var="clinic")
    PKG = {"gamma": [float(v) for v in np.ravel(mod.coefficients_["gamma"])], "beta": float(np.ravel(mod.coefficients_["beta"])[0]), "steps": int(mod.algorithm.iter)}
gam_fit = np.array(PKG["gamma"])                       # the package's final state: Elm's slider where its fifth step left it
check("the package's fit: the four gammas and beta of Episode 4, Elm left at -6.25 after 5 steps",
      all(abs(gam_fit[i] - g_fit[k]) < 1e-6 for i, k in enumerate(FINITE)) and abs(PKG["beta"] - beta_hat) < 1e-6 and round(gam_fit[4], 2) == -6.25 and PKG["steps"] == 5)
diag, border, corner, w_fit = arrow(gam_fit, PKG["beta"])
check("diagonal at the fit: 6.38, 6.66, 3.82, 2.31, 0.02 (blueprint)", [round(v, 2) for v in diag] == [6.38, 6.66, 3.82, 2.31, 0.02], str([round(float(v), 3) for v in diag]))
check("border at the fit: 0.97, 5.94, 2.35, 0.93, 0 (blueprint); corner 10.20", [round(v, 2) for v in border] == [0.97, 5.94, 2.35, 0.93, 0.0] and round(corner, 2) == 10.2,
      f"{[round(float(v), 3) for v in border]}, {corner:.3f}")
Z = np.zeros((len(Y), M + 1)); Z[np.arange(len(Y)), PROV] = 1.0; Z[:, M] = X01
FULL = Z.T @ (Z * w_fit[:, None])                       # the whole 6 x 6 table, built the long way from all 103 patients
off = FULL[:M, :M] - np.diag(np.diag(FULL[:M, :M]))
check("built the long way, the 6 x 6 table is exactly the arrow: 20 clinic-to-clinic cells are zero", np.all(off == 0.0) and np.allclose(np.diag(FULL)[:M], diag)
      and np.allclose(FULL[:M, M], border) and abs(FULL[M, M] - corner) < 1e-12)
check("each cell is how much a meter moves when a control moves (numerical derivative of expected counts)",
      all(abs((np.bincount(PROV, weights=expit((gam_fit + 1e-6 * (np.arange(M) == k))[PROV] + X01 * PKG["beta"]), minlength=M)
               - np.bincount(PROV, weights=expit(gam_fit[PROV] + X01 * PKG["beta"]), minlength=M))[i] / 1e-6 - FULL[i, k]) < 1e-5 for i in range(M) for k in range(M)))
check("Birch has 24 higher-risk patients and Elm none", CAST["Birch"][2] == 24 and CAST["Elm"][2] == 0)

# ----------------------------------------------------------------------------- 2. scale (S04)
cells = lambda m, p: (m + p) ** 2
nonzero = lambda m, p: m + 2 * m * p + p * p
check("the crowd's table: 40,804 cells, 1,004 of them not zero (blueprint)", cells(200, 2) == 40804 and nonzero(200, 2) == 1004)
check("a national measure, 7,000 providers and 50 risk factors: almost 50 million cells", cells(7000, 50) == 49702500 and nonzero(7000, 50) / cells(7000, 50) < 0.015,
      f"{cells(7000, 50):,} cells, {100 * nonzero(7000, 50) / cells(7000, 50):.1f}% not zero")

# ----------------------------------------------------------------------------- 3. folding (S05)
fold = border ** 2 / diag
S = corner - float(fold.sum())
check("folding: clinics take away 0.15, 5.30, 1.45, 0.38 and 0; the corner falls from 10.20 to 2.93 (blueprint)",
      [round(v, 2) for v in fold] == [0.15, 5.3, 1.45, 0.38, 0.0] and round(S, 2) == 2.93, f"{[round(float(v), 3) for v in fold]}, S {S:.4f}")
xbar = border / diag                                                     # each clinic's weighted mean of x
within = np.bincount(PROV, weights=w_fit * (X01 - xbar[PROV]) ** 2, minlength=M)
check("what is left is the spread of risk inside each clinic: 0.82, 0.64, 0.90, 0.56 and 0 (blueprint)",
      [round(v, 2) for v in within] == [0.82, 0.64, 0.9, 0.56, 0.0] and abs(within.sum() - S) < 1e-12, str([round(float(v), 3) for v in within]))
check("folding is exact: 1/S is the dial's cell in the inverse of the whole table", abs(np.linalg.inv(FULL)[M, M] - 1.0 / S) < 1e-9)
E4 = json.loads((HERE.parent / "e04_one_intercept_per_provider" / "e04_numbers.json").read_text())
check("1/sqrt(S) is the dial's standard error, the one behind Episode 4's interval (0.58)", abs(1 / np.sqrt(S) - E4["fit"]["se_beta"]) < 1e-9 and round(1 / np.sqrt(S), 2) == 0.58,
      f"{1 / np.sqrt(S):.4f}")
check("ignoring the clinics would overstate what the data say about the dial 3.5 times", round(corner / S, 1) == 3.5, f"{corner / S:.3f}")

# ----------------------------------------------------------------------------- 4. one step, together (S06)
def joint(shift=0.0, tol=1e-8, max_iter=50):
    x = X01 + shift
    gam, beta = np.full(M, g0), 0.0
    path = [{"beta": beta, "gamma": gam.tolist(), "loglik": loglik(gam, beta, x)}]
    first = None
    for it in range(1, max_iter + 1):
        d, b, c, w = arrow(gam, beta, x)
        p = expit(gam[PROV] + x * beta)
        Ug, Ub = np.bincount(PROV, weights=Y - p, minlength=M), float(x @ (Y - p))
        S_ = c - float((b * b / d).sum())
        tilt = Ub - float((b * Ug / d).sum())                          # the dial's tilt, corrected for what the clinics will do
        db = tilt / S_
        dg = (Ug - b * db) / d
        if first is None:
            first = {"corrected_tilt": tilt, "S": S_, "dial_step": db, "gamma_steps": dg.tolist(), "diag": d.tolist(), "border": b.tolist(), "corner": c,
                     "tilts": Ug.tolist(), "dial_tilt": Ub}
        gam, beta = gam + dg, beta + db
        path.append({"beta": beta, "gamma": gam.tolist(), "loglik": loglik(gam, beta, x)})
        if abs(db) < tol:
            break
    return it, path, first


n_steps, path, first = joint()
check("the first joint step: S 4.250 at the plain guess, the dial moves 1.81, the clinics -0.26, -1.21, -0.94, -0.18, -1.69 (blueprint)",
      abs(first["S"] - 4.250) < 5e-4 and round(first["dial_step"], 2) == 1.81 and [round(v, 2) for v in first["gamma_steps"]] == [-0.26, -1.21, -0.94, -0.18, -1.69],
      f"{first['dial_step']:.4f}; {[round(float(v), 3) for v in first['gamma_steps']]}")
d0, b0, c0, w0 = arrow(np.full(M, g0), 0.0)
p0 = expit(np.full(len(Y), g0))
FULL0 = Z.T @ (Z * w0[:, None])
full_step = np.linalg.solve(FULL0, Z.T @ (Y - p0))
check("the folded step is the plain step exactly: solving the whole 6 x 6 system gives the same six numbers",
      np.allclose(full_step[:M], first["gamma_steps"], atol=1e-12) and abs(full_step[M] - first["dial_step"]) < 1e-12)
check("the dial goes 0, 1.81, 2.00, 2.0164 and stops after 5 steps (blueprint); the package agrees",
      [round(path[k]["beta"], 3) for k in range(4)] == [0.0, 1.812, 2.004, 2.016] and round(path[3]["beta"], 4) == 2.0164 and n_steps == 5 and PKG["steps"] == 5)
check("the height goes -69.63, -57.00, -56.03, -55.75 (blueprint)", [round(path[k]["loglik"], 2) for k in range(4)] == [-69.63, -57.0, -56.03, -55.75])
s5, p5, _ = joint(shift=5.0)
s50, p50, _ = joint(shift=50.0)
check("recorded 5 or 50 units higher, the joint path does not change: the same 5 steps and the same dial positions",
      s5 == n_steps and s50 == n_steps and max(abs(a["beta"] - b_["beta"]) for a, b_ in zip(path, p5)) < 1e-9
      and max(abs(a["beta"] - b_["beta"]) for a, b_ in zip(path, p50)) < 1e-6,
      f"largest difference {max(abs(a['beta'] - b_['beta']) for a, b_ in zip(path, p50)):.1e}")
E7 = json.loads((HERE.parent / "e07_climbing_the_hill" / "e07_numbers.json").read_text())
check("Episode 7's counts for taking turns: 54 rounds as recorded, 21 centred, 3,125 five units higher",
      (E7["rounds"]["plain"], E7["rounds"]["centred"], E7["rounds"]["five_higher"]) == (54, 21, 3125))

# ----------------------------------------------------------------------------- 5. what it buys (S07)
rng = np.random.default_rng(2026)
m_big = 2000
n_big = 20 + rng.exponential(80.0, m_big).round().astype(int)
prov_big = np.repeat(np.arange(m_big), n_big)
mu_big = rng.normal(0.0, 0.5, m_big)
x1 = rng.normal(mu_big[prov_big], 1.0)
x2 = (rng.random(len(prov_big)) < 0.3).astype(float)
gam_big = -1.5 + 0.3 * rng.normal(size=m_big) - 0.3 * mu_big
y_big = (rng.random(len(prov_big)) < expit(gam_big[prov_big] + 0.8 * x1 + 0.5 * x2)).astype(float)
big = pd.DataFrame({"prov": prov_big, "x1": x1, "x2": x2, "y": y_big})
times = []
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    for _ in range(3):
        t0 = time.perf_counter()
        mb = LogisticFixedEffectModel(algorithm="Serbin").fit(big, y_var="y", x_vars=["x1", "x2"], provider_var="prov")
        times.append(time.perf_counter() - t0)
fit_seconds = float(np.median(times))
beta_big = np.ravel(mb.coefficients_["beta"]).astype(float)
dense_gb = len(prov_big) * (m_big + 2) * 8 / 1e9
check("the test fit: 2,000 providers and about 200,000 patients, with the planted steps 0.8 and 0.5 recovered",
      m_big == 2000 and 195000 < len(prov_big) < 206000 and abs(beta_big[0] - 0.8) < 0.03 and abs(beta_big[1] - 0.5) < 0.05,
      f"{len(prov_big):,} patients; steps {beta_big[0]:.3f}, {beta_big[1]:.3f}")
check("it fits in less than a second here (median of three runs)", fit_seconds < 1.0, f"{fit_seconds:.2f} s")
check("the same data as a table with a column per provider would fill 3.3 gigabytes", round(dense_gb, 1) == 3.3, f"{dense_gb:.2f} GB")

OUT = {
    "episode": 8, "title": "The Arrow Matrix", "clinics": ALL,
    "table": {"diag": diag.tolist(), "border": border.tolist(), "corner": corner, "elm_gamma": float(gam_fit[4])},
    "scale": {"cast": [cells(M, 1), nonzero(M, 1) - 2], "crowd": [cells(200, 2), nonzero(200, 2)], "national": [cells(7000, 50), nonzero(7000, 50)], "national_side": 7050, "crowd_side": 202},
    "fold": {"terms": fold.tolist(), "S": S, "within": within.tolist(), "overstate": corner / S, "running": (corner - np.cumsum(fold)).tolist()},
    "first": first, "joint": {"steps": n_steps, "path": path}, "start_gamma": g0,
    "turns": {"plain": E7["rounds"]["plain"], "centred": E7["rounds"]["centred"], "five_higher": E7["rounds"]["five_higher"]},
    "cost": {"providers": m_big, "patients": int(len(prov_big)), "seconds": fit_seconds, "dense_gb": dense_gb},
    "fit": {"beta": beta_hat, "gamma": g_fit},
}

if __name__ == "__main__":
    print("diag  ", [round(float(v), 3) for v in diag]); print("border", [round(float(v), 3) for v in border], " corner", round(corner, 3))
    print("fold  ", [round(float(v), 3) for v in fold], " S", round(S, 4), " overstate", round(corner / S, 2))
    print("dial  ", [round(p_["beta"], 4) for p_ in path], " steps", n_steps)
    print(f"cost   {len(prov_big):,} patients, {fit_seconds:.2f} s, dense {dense_gb:.2f} GB")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e08_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
