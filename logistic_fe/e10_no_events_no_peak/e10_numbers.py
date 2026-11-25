"""Model in Motion · The Logistic Fixed-Effect Model · Episode 10: No events, no peak.

Every number the episode shows or says is computed here, checked, and written to e10_numbers.json.
Scenes and narration read e10_numbers.json; nothing numeric is typed into scene code or the script.
Most of this episode is about what the fitting software prints, so most checks run pprof_py itself.

    python e10_numbers.py        # from this folder: prints the ledger, runs every check, writes e10_numbers.json
"""
from __future__ import annotations

import json
import logging
import sys
import warnings
from math import ceil, log
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit, rows  # noqa: E402

warnings.simplefilter("ignore")
logging.disable(logging.CRITICAL)
import pandas as pd  # noqa: E402
from pprof_py import LogisticFixedEffectModel  # noqa: E402

ALL = list(CAST)
PROV, X01, Y = rows(ALL)
CHECKS: list[tuple[str, bool, str]] = []
fl = lambda a, k=3: [round(float(v), k) for v in a]


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


g_fit, beta, cov4, ll_fit = fit()                      # the four clinics that have a finite fit
E8 = json.loads((HERE.parent / "e08_the_arrow_matrix" / "e08_numbers.json").read_text())
E9 = json.loads((HERE.parent / "e09_how_sure_are_we" / "e09_numbers.json").read_text())
four = np.array([g_fit[k] for k in FINITE])
n_elm = CAST["Elm"][0] + CAST["Elm"][2]
g0 = float(logit(Y.mean()))                            # the plain guess every slider starts from


def frame(cast=CAST):
    names = list(cast)
    prov, x, y = rows(names) if cast is CAST else _rows(cast)
    return pd.DataFrame({"clinic": np.array(names)[prov], "x": x, "y": y})


def _rows(cast):
    prov, x, y = [], [], []
    for i, (n0, e0, n1, e1) in enumerate(cast.values()):
        for n, e, hi in ((n0, e0, 0.0), (n1, e1, 1.0)):
            prov += [i] * n; x += [hi] * n; y += [1.0] * e + [0.0] * (n - e)
    return np.array(prov), np.array(x), np.array(y)


def run(df=None, algorithm="Serbin", **fit_kw):
    """One pprof_py fit of the cast. Returns the model with its effects keyed by clinic."""
    m = LogisticFixedEffectModel(algorithm=algorithm).fit(frame() if df is None else df, y_var="y", x_vars=["x"], provider_var="clinic", **fit_kw)
    m.g = dict(zip([str(v) for v in m.provider_ids_], np.ravel(m.coefficients_["gamma"]).astype(float)))
    m.b = float(np.ravel(m.coefficients_["beta"])[0])
    return m


# ----------------------------------------------------------------------------- 1. a hill with no top (S03)
check("Elm: 11 patients, all lower-risk, no readmissions", CAST["Elm"] == (11, 0, 0, 0) or list(CAST["Elm"]) == [11, 0, 0, 0])
elm_ll = lambda g: -n_elm * float(np.log1p(np.exp(g)))                         # Elm's own height: every patient lower-risk, none readmitted
ref = float(np.median(np.append(four, -50.0)))                                 # the middle clinic of five, wherever below Birch Elm's slider sits
check("the middle clinic is Cedar, at -1.52, wherever Elm's slider stopped", abs(ref - g_fit["Cedar"]) < 1e-12 and round(ref, 2) == -1.52
      and all(abs(float(np.median(np.append(four, v))) - ref) < 1e-12 for v in (-5.24, -6.25, -7.25, -11.52)))
hill_at = {"reference": elm_ll(ref), "-3": elm_ll(-3.0), "-6.25": elm_ll(-6.25), "-11.5": elm_ll(-11.5)}
check("Elm's hill reads -2.17 at the reference, -0.53 at -3, -0.02 at -6.25 and -0.0001 at -11.5 (blueprint has -2.18 for the first)",
      (round(hill_at["reference"], 2), round(hill_at["-3"], 2), round(hill_at["-6.25"], 2), round(hill_at["-11.5"], 4)) == (-2.17, -0.53, -0.02, -0.0001),
      f"{hill_at['reference']:.4f}, {hill_at['-3']:.4f}, {hill_at['-6.25']:.4f}, {hill_at['-11.5']:.6f}")
grid = np.linspace(3.0, -25.0, 561)
heights = np.array([elm_ll(g) for g in grid])
check("it rises at every step down the slider and never reaches its ceiling of zero", np.all(np.diff(heights) > 0) and heights.max() < 0.0)
expected = lambda g: n_elm * float(expit(g))
check("the meter: expected is above observed at every slider position (4.49 at the plain guess, 1.97 at the reference, 0.02 at -6.25)",
      all(expected(g) > 0 for g in grid) and (round(expected(g0), 2), round(expected(ref), 2), round(expected(-6.25), 2)) == (4.49, 1.97, 0.02),
      f"{expected(g0):.3f}, {expected(ref):.3f}, {expected(-6.25):.4f}")

# ----------------------------------------------------------------------------- 2. where the slider stops (S04)
elm_path = [p["gamma"][4] for p in E8["joint"]["path"]]                        # Episode 8's joint path
steps = np.diff(elm_path)
check("stepping together, Elm's slider goes -2.06, -3.19, -4.23, -5.24, -6.25", fl(elm_path[1:6], 2) == [-2.06, -3.19, -4.23, -5.24, -6.25], str(fl(elm_path[:6])))
check("each step is exactly -1 / (1 - p): about one unit once p is small", np.allclose(steps[:5], [-1.0 / (1.0 - expit(g)) for g in elm_path[:5]], atol=1e-9)
      and all(abs(s + 1.0) < 0.14 for s in steps[1:5]), str(fl(steps[:5])))
S = run()
B = run(algorithm="Ban")
check("pprof_py, stepping together: 5 steps, Elm printed at -6.25", S.algorithm.iter == 5 and round(S.g["Elm"], 2) == -6.25, f"{S.g['Elm']:.4f}")
check("pprof_py, taking turns: 21 rounds, Elm printed at -11.52, which is the middle clinic's value minus 10", B.algorithm.iter == 21 and round(B.g["Elm"], 2) == -11.52
      and abs(B.g["Elm"] - (float(np.median(list(B.g.values()))) - 10.0)) < 1e-9, f"{B.g['Elm']:.4f}")
import inspect  # noqa: E402
rule = inspect.getsource(type(B.algorithm))
check("taking turns waits for the sliders as well as the dial (its loop runs while either is still moving)", "max(self.gamma_crit, self.beta_crit) > self.tol" in rule)
B_free = run(algorithm="Ban", bound=1000.0)
check("so without the wall it does not finish: it is still running at the software's limit of 10,000 rounds", B_free.algorithm.iter == 10000 and B_free.g["Elm"] < -50.0,
      f"{B_free.algorithm.iter} rounds, slider at {B_free.g['Elm']:.2f}")
no_elm = LogisticFixedEffectModel(algorithm="Ban").fit(frame()[frame()["clinic"] != "Elm"], y_var="y", x_vars=["x"], provider_var="clinic")
check("with the wall it takes 21 rounds, exactly as many as the four other clinics need on their own", int(no_elm.algorithm.iter) == 21 and B.algorithm.iter == 21)
check("stepping together stops on the dial alone: at its last step Elm's slider is still moving a full unit", abs(steps[4] + 1.0) < 0.01 and S.algorithm.iter == 5, f"{steps[4]:.4f}")
loose, tight = run(tol=1e-4), run(tol=1e-10)
check("the stopping rule matters: looser (1e-4) prints -5.24 after 4 steps, tighter (1e-10) prints -7.25 after 6 (blueprint)",
      (round(loose.g["Elm"], 2), loose.algorithm.iter, round(tight.g["Elm"], 2), tight.algorithm.iter) == (-5.24, 4, -7.25, 6), f"{loose.g['Elm']:.4f}, {tight.g['Elm']:.4f}")
runs = {"together": S, "turns": B, "looser": loose, "tighter": tight}
worst = max(max(abs(m.b - beta), *[abs(m.g[k] - g_fit[k]) for k in FINITE]) for m in runs.values())
check("nothing else is harmed: the dial and the other four sliders match the four-clinic fit in all four runs (within 0.00002)", worst < 2e-5, f"largest difference {worst:.1e}")

# ----------------------------------------------------------------------------- 3. what breaks (S05)
wald_S, wald_B = S.test(test_method="wald").loc["Elm"], B.test(test_method="wald").loc["Elm"]
check("Elm's printed interval after stepping together: -19.7 to +7.2 (Episode 9)", (round(float(wald_S["ci_lower"]), 1), round(float(wald_S["ci_upper"]), 1)) == (-19.7, 7.2))
check("after taking turns its standard error is in the nineties and the interval hundreds wide", 90 < float(wald_B["se"]) < 100 and float(wald_B["ci_upper"] - wald_B["ci_lower"]) > 300,
      f"SE {float(wald_B['se']):.1f}; {float(wald_B['ci_lower']):.0f} to {float(wald_B['ci_upper']):.0f}")
sizes = np.array([CAST[k][0] + CAST[k][2] for k in ALL], dtype=float)
mean_ref = {name: float(np.average([m.g[k] for k in ALL], weights=sizes)) for name, m in (("together", S), ("turns", B))}
check("a size-weighted average of the gammas: -1.75 after one routine, -2.31 after the other (blueprint: -1.751, -2.314)",
      (round(mean_ref["together"], 2), round(mean_ref["turns"], 2)) == (-1.75, -2.31), f"{mean_ref['together']:.4f}, {mean_ref['turns']:.4f}")
ratio = {}
for name, m in (("together", S), ("turns", B)):
    t = m.calculate_standardized_measures(stdz="indirect", reference="mean")["indirect"].set_index("provider_id")
    ratio[name] = {k: float(t.loc[k, "indirect_ratio"]) for k in FINITE}
    own = {k: (CAST[k][1] + CAST[k][3]) / float(np.sum(expit(mean_ref[name] + beta * X01[PROV == i]))) for i, k in enumerate(FINITE)}
    check(f"against that average ({name}), pprof_py's observed-to-expected ratios match a direct calculation", all(abs(own[k] - ratio[name][k]) < 2e-4 for k in FINITE))
check("Alder's readmissions against that reference: 1.87 times expected, or 2.76 times (the other three: 0.97, 1.12, 1.63 or 1.30, 1.55, 2.26)",
      fl([ratio["together"][k] for k in FINITE], 2) == [1.87, 0.97, 1.12, 1.63] and fl([ratio["turns"][k] for k in FINITE], 2) == [2.76, 1.3, 1.55, 2.26])
direct = {}
for name, m in (("together", S), ("turns", B)):
    d = m.calculate_standardized_measures(stdz="direct")["direct"].set_index("provider_id")
    direct[name] = float(d.loc["Elm", "direct_rate"])
    check(f"Elm's direct rate ({name}) is the cast's average probability under Elm's printed slider", abs(direct[name] - 100 * float(np.mean(expit(m.g["Elm"] + m.b * X01)))) < 1e-6)
check("Elm's direct rate: 0.74% or 0.004% (blueprint)", (round(direct["together"], 2), round(direct["turns"], 3)) == (0.74, 0.004), f"{direct['together']:.4f}, {direct['turns']:.5f}")

# ----------------------------------------------------------------------------- 4. what survives (S06)
med = {name: float(np.median([m.g[k] for k in ALL])) for name, m in (("together", S), ("turns", B))}
check("the middle clinic's value is -1.52 after either routine", round(med["together"], 2) == -1.52 and abs(med["together"] - med["turns"]) < 2e-5)
ind = {name: m.calculate_standardized_measures(stdz="indirect")["indirect"].set_index("provider_id") for name, m in (("together", S), ("turns", B))}
e_ref = n_elm * float(expit(ref))
check("at that reference Elm's 11 patients would expect 1.97 readmissions; it had none (pprof_py agrees after either routine)",
      round(e_ref, 2) == 1.97 and all(abs(float(t.loc["Elm", "expected"]) - e_ref) < 1e-4 and float(t.loc["Elm", "observed"]) == 0 for t in ind.values()), f"{e_ref:.4f}")
check("and the other four ratios are the same after either routine: 1.62, 0.88, 1.00, 1.46",
      all(fl([float(t.loc[k, "indirect_ratio"]) for k in FINITE], 2) == [1.62, 0.88, 1.0, 1.46] for t in ind.values()))
stay = 1.0 - float(expit(ref))
p_none = stay ** n_elm
exact = {name: m.test(test_method="poibin_exact").loc["Elm"] for name, m in (("together", S), ("turns", B))}
check("each such patient has an 82% chance of no readmission; all eleven, 11% (0.821 to the 11th = 0.114)", round(stay, 3) == 0.821 and round(p_none, 3) == 0.114, f"{stay:.4f}, {p_none:.4f}")
check("pprof_py's exact test gives that same 0.114 after either routine, and does not flag Elm", all(abs(float(r["p_value"]) - p_none) < 5e-6 and int(r["flag"]) == 0 for r in exact.values()),
      f"{float(exact['together']['p_value']):.6f}, {float(exact['turns']['p_value']):.6f}")
p30 = stay ** 30
check("thirty such patients with none: 0.0027, about 3 chances in 1,000 (blueprint)", round(p30, 4) == 0.0027)
first = ceil(log(0.05) / log(stay))
check("sixteen is the first count at which no readmissions falls below 5%", first == 16 and stay ** 15 > 0.05 > stay ** 16, f"{stay ** 15:.4f}, {stay ** 16:.4f}")
ci = S.calculate_confidence_intervals(option="SM", stdz="indirect", measure="ratio", test_method="exact")["indirect_ratio"].set_index("provider_id").loc["Elm"]
p_up = 1.0 - 0.05 ** (1.0 / n_elm)                                              # mid-p: half the chance of none equals 2.5%
check("the exact interval for Elm's ratio runs from 0 to 1.33 (blueprint), and follows from the count alone",
      (round(float(ci["ci_ratio_lower"]), 2), round(float(ci["ci_ratio_upper"]), 2)) == (0.0, 1.33) and abs(n_elm * p_up / e_ref - float(ci["ci_ratio_upper"])) < 2e-3,
      f"{float(ci['ci_ratio_upper']):.4f}; by hand {n_elm * p_up / e_ref:.4f}")

# ----------------------------------------------------------------------------- 5. two footnotes (S07)
mirror_cast = dict(CAST); mirror_cast["Elm"] = (11, 11, 0, 0)
Mi = run(frame(mirror_cast), algorithm="Ban")
check("the mirror image: with all 11 readmitted, taking turns runs Elm to the upper wall, the middle clinic's value plus 10",
      abs(Mi.g["Elm"] - (float(np.median(list(Mi.g.values()))) + 10.0)) < 1e-9 and Mi.g["Elm"] > 8, f"{Mi.g['Elm']:.3f}")
fen_cast = dict(CAST); fen_cast["Fen"] = (5, 1, 3, 2)
F = run(frame(fen_cast))
check("Fen, 8 patients (5 lower-risk with 1 readmission, 3 higher-risk with 2), never enters the fit; the dial is unchanged",
      "Fen" not in F.g and list(F.g) == ALL and abs(F.b - S.b) < 1e-9, f"kept {list(F.g)}")
ten_cast = dict(CAST); ten_cast["Elm"] = (10, 0, 0, 0)
T = run(frame(ten_cast))
check("the screen keeps providers with more than 10 records: Elm with 10 would have been dropped, with 11 it stays", "Elm" not in T.g and "Elm" in S.g)
F_in = run(frame(fen_cast), cutoff=0)
check("for the record: with Fen let in, the dial would read 2.0 to 2.2", "Fen" in F_in.g and 2.0 < F_in.b < 2.2, f"{F_in.b:.4f}")

OUT = {
    "episode": 10, "title": "No Events, No Peak", "clinics": ALL, "elm": {"patients": n_elm, "readmissions": 0},
    "reference": ref, "start": g0, "fit": {"beta": beta, "gamma": g_fit},
    "hill": {"at": hill_at, "curve": [[float(g), float(h)] for g, h in zip(grid[::4], heights[::4])]},
    "meter": {"start": expected(g0), "reference": expected(ref), "at_printed": expected(-6.25)},
    "march": {"path": [float(v) for v in elm_path[:6]], "steps": fl(steps[:5], 4)},
    "printed": {"together": S.g["Elm"], "turns": B.g["Elm"], "looser": loose.g["Elm"], "tighter": tight.g["Elm"], "turns_without_wall": B_free.g["Elm"], "rounds_without_wall": int(B_free.algorithm.iter),
                "steps": {"together": int(S.algorithm.iter), "turns": int(B.algorithm.iter), "looser": int(loose.algorithm.iter), "tighter": int(tight.algorithm.iter)}, "wall": ref - 10.0},
    "breaks": {"interval": [float(wald_S["ci_lower"]), float(wald_S["ci_upper"])], "interval_turns": [float(wald_B["ci_lower"]), float(wald_B["ci_upper"])],
               "mean_reference": mean_ref, "ratio": ratio, "direct_rate": direct},
    "survives": {"median": med["together"], "expected": e_ref, "stay": stay, "p_none": p_none, "p_thirty": p30, "first_flag": first,
                 "ratio_upper": float(ci["ci_ratio_upper"]), "ratios": {k: float(ind["together"].loc[k, "indirect_ratio"]) for k in FINITE},
                 "curve": [[n, stay ** n] for n in range(1, 41)]},
    "footnotes": {"mirror": Mi.g["Elm"], "fen": {"patients": 8, "cast": [5, 1, 3, 2]}, "cutoff": 10, "beta_with_fen": F_in.b},
}

if __name__ == "__main__":
    print("hill      ", {k: round(v, 4) for k, v in hill_at.items()})
    print("printed   ", {k: round(float(v), 3) for k, v in OUT["printed"].items() if not isinstance(v, dict)}, OUT["printed"]["steps"])
    print("mean ref  ", {k: round(v, 3) for k, v in mean_ref.items()}, "| Alder's ratio", round(ratio["together"]["Alder"], 3), round(ratio["turns"]["Alder"], 3))
    print("direct    ", {k: round(v, 5) for k, v in direct.items()})
    print(f"survives   median {med['together']:.4f}; expected {e_ref:.4f}; stay {stay:.4f}; none {p_none:.4f}; thirty {p30:.5f}; first below 5%: {first}; ratio up to {float(ci['ci_ratio_upper']):.3f}")
    print(f"footnotes  mirror {Mi.g['Elm']:.3f}; with Fen the dial would read {F_in.b:.4f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e10_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
