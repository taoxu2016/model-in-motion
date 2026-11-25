"""Model in Motion · The Logistic Fixed-Effect Model · Episode 6: Fitting by balance.

Every number the episode shows or says is computed here, checked, and written to e06_numbers.json.
Scenes and narration read e06_numbers.json; nothing numeric is typed into scene code or the script.

    python e06_numbers.py        # from this folder: prints the ledger, runs every check, writes e06_numbers.json
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))
from mim.castfit import CAST, FINITE, expit, fit, logit  # noqa: E402

ALL = list(CAST)
CHECKS: list[tuple[str, bool, str]] = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def expected(name, gamma, beta):
    n0, _, n1, _ = CAST[name]
    return float(n0 * expit(gamma) + n1 * expit(gamma + beta))


def observed(name):
    return CAST[name][1] + CAST[name][3]


def loglik_clinic(name, gamma, beta):
    n0, e0, n1, e1 = CAST[name]
    t = 0.0
    for n, e, eta in ((n0, e0, gamma), (n1, e1, gamma + beta)):
        if n:
            p = float(expit(eta))
            t += e * np.log(p) + (n - e) * np.log(1 - p)
    return float(t)


def loglik(gammas, beta):
    return sum(loglik_clinic(k, gammas[k], beta) for k in gammas)


def u_beta(gammas, beta):
    """The dial's meter: observed minus expected readmissions among higher-risk patients."""
    return sum(CAST[k][3] - CAST[k][2] * float(expit(gammas[k] + beta)) for k in gammas)


# ----------------------------------------------------------------------------- 1. the plain guess (pprof_py's starting point)
N_PAT = sum(v[0] + v[2] for v in CAST.values())
N_EV = sum(v[1] + v[3] for v in CAST.values())
rate0 = N_EV / N_PAT
g0 = float(logit(rate0))
start_g = {k: g0 for k in ALL}
ll0 = loglik(start_g, 0.0)
like0 = float(np.exp(ll0))
expo = int(np.floor(np.log10(like0)))
mant = like0 / 10.0 ** expo
U0 = {k: observed(k) - expected(k, g0, 0.0) for k in ALL}
E0 = {k: expected(k, g0, 0.0) for k in ALL}
obs_high = sum(v[3] for v in CAST.values())
n_high = sum(v[2] for v in CAST.values())
ub0 = u_beta(start_g, 0.0)
check("the plain guess: 42 of 103, 41% for everyone; gamma -0.373 (blueprint)", (N_EV, N_PAT) == (42, 103) and round(100 * rate0) == 41 and abs(g0 + 0.373) < 5e-4,
      f"{100 * rate0:.2f}%, {g0:.4f}")
check("its height is -69.63 (blueprint), spoken as minus 69.6", abs(ll0 + 69.63) < 5e-3 and round(ll0, 1) == -69.6, f"{ll0:.3f}")
check("the likelihood is about 6 x 10^-31: a decimal point followed by thirty zeros", expo == -31 and round(mant) == 6, f"{mant:.2f}e{expo}")
check("the product has 42 factors of 0.41 and 61 of 0.59", abs(N_EV * np.log(rate0) + (N_PAT - N_EV) * np.log(1 - rate0) - ll0) < 1e-9
      and (round(rate0, 2), round(1 - rate0, 2)) == (0.41, 0.59))
check("meters at the plain guess: +0.77, +1.77, -0.16, +2.11, -4.49 (blueprint)",
      [round(U0[k], 2) for k in ALL] == [0.77, 1.77, -0.16, 2.11, -4.49], str([round(U0[k], 2) for k in ALL]))
check("spoken: Dune expected 4.9 and saw 7; Birch 12.2 and 14; Elm 4.5 and none",
      (round(E0["Dune"], 1), observed("Dune"), round(E0["Birch"], 1), observed("Birch"), round(E0["Elm"], 1), observed("Elm")) == (4.9, 7, 12.2, 14, 4.5, 0))
check("the dial's meter at the plain guess: 29 observed, 18.76 expected, +10.24 (blueprint); 'fewer than 19'",
      obs_high == 29 and n_high == 46 and abs(ub0 - 10.24) < 5e-3 and abs((obs_high - ub0) - 18.76) < 5e-3 and obs_high - ub0 < 19, f"{ub0:.3f}")

# the slope really is observed minus expected: a numerical derivative of the height
h = 1e-6
num = {k: (loglik({**start_g, k: g0 + h}, 0.0) - loglik({**start_g, k: g0 - h}, 0.0)) / (2 * h) for k in ALL}
check("the slope of the height in each gamma equals that clinic's observed minus expected (numerical derivative)",
      all(abs(num[k] - U0[k]) < 1e-5 for k in ALL))
numb = (loglik(start_g, h) - loglik(start_g, -h)) / (2 * h)
check("the slope of the height in beta equals the dial's meter (numerical derivative)", abs(numb - ub0) < 1e-5)

# ----------------------------------------------------------------------------- 2. one slider: Dune (S05)
gD = float(logit(observed("Dune") / (CAST["Dune"][0] + CAST["Dune"][2])))        # with beta = 0, Dune levels at its own rate
gain = loglik({**start_g, "Dune": gD}, 0.0) - ll0
gOver = 1.2
uOver = observed("Dune") - expected("Dune", gOver, 0.0)
fall = loglik({**start_g, "Dune": gOver}, 0.0) - loglik({**start_g, "Dune": gD}, 0.0)
others = max(abs((observed(k) - expected(k, g0, 0.0)) - U0[k]) for k in ALL if k != "Dune")
check("Dune's slider alone levels Dune's meter at +0.34 and lifts the height by 0.75; no other meter moves",
      abs(observed("Dune") - expected("Dune", gD, 0.0)) < 1e-12 and round(gD, 2) == 0.34 and round(gain, 2) == 0.75 and others == 0.0, f"{gD:.4f}, {gain:.4f}")
ub_dune = u_beta({**start_g, "Dune": gD}, 0.0)
check("Dune's slider does move the dial's meter, from +10.24 to +9.19: Dune has higher-risk patients", round(ub_dune, 2) == 9.19 and CAST["Dune"][2] > 0, f"{ub_dune:.3f}")
check("pushed further (to +1.2) Dune's meter tips the other way and the height falls", uOver < -2 and fall < -0.9, f"O - E {uOver:.2f}, height {fall:.2f}")

# ----------------------------------------------------------------------------- 3. the dial alone (S05)
lo_, hi_ = 0.0, 5.0
for _ in range(200):
    mid = (lo_ + hi_) / 2
    lo_, hi_ = (mid, hi_) if u_beta(start_g, mid) > 0 else (lo_, mid)
bD = (lo_ + hi_) / 2
UD = {k: observed(k) - expected(k, g0, bD) for k in ALL}
check("the dial alone levels its own meter at 0.91", abs(u_beta(start_g, bD)) < 1e-9 and round(bD, 2) == 0.91, f"{bD:.4f}")
check("turning the dial shifts every clinic that has higher-risk patients, and leaves Elm where it was",
      all(abs(UD[k] - U0[k]) > 0.5 for k in FINITE) and abs(UD["Elm"] - U0["Elm"]) < 1e-12 and CAST["Elm"][2] == 0,
      str({k: round(UD[k], 2) for k in ALL}))

# ----------------------------------------------------------------------------- 4. level everything (S06)
g, beta, cov, ll_fit = fit()
E_fit = {k: expected(k, g[k], beta) for k in FINITE}
check("at the fit the dial reads 2.02 and the four sliders are where Episode 4 found them",
      round(beta, 2) == 2.02 and [round(g[k], 2) for k in FINITE] == [-0.65, -1.82, -1.52, -0.58])
check("at the fit expected equals observed in each of the four clinics: 13, 14, 8 and 7",
      [observed(k) for k in FINITE] == [13, 14, 8, 7] and all(abs(E_fit[k] - observed(k)) < 1e-9 for k in FINITE))
check("and the dial's meter is level: 29 higher-risk readmissions expected", abs(u_beta(g, beta)) < 1e-9)
check("the height at the fit is -55.59 (blueprint), with Elm's slider run all the way down", abs(ll_fit + 55.59) < 5e-3 and round(ll_fit, 1) == -55.6, f"{ll_fit:.3f}")
split = (CAST["Alder"][0] * float(expit(g["Alder"])), CAST["Alder"][2] * float(expit(g["Alder"] + beta)))
check("the balance holds for totals, not groups: Alder expects 8.2 and 4.8 where it saw 8 and 5",
      (round(split[0], 1), round(split[1], 1)) == (8.2, 4.8) and abs(sum(split) - 13) < 1e-9 and (CAST["Alder"][1], CAST["Alder"][3]) == (8, 5), f"{split[0]:.3f}, {split[1]:.3f}")
elm = [{"gamma": v, "expected": expected("Elm", v, beta), "height_term": loglik_clinic("Elm", v, beta)} for v in (-2.0, -4.0, -6.0, -8.0)]
check("Elm never levels: expected stays above 0 and each step down gains less height",
      all(e["expected"] > 0 for e in elm) and all(b["height_term"] > a["height_term"] for a, b in zip(elm, elm[1:]))
      and all((c["height_term"] - b["height_term"]) < (b["height_term"] - a["height_term"]) for a, b, c in zip(elm, elm[1:], elm[2:])),
      str([round(e["height_term"], 3) for e in elm]))
check("with Elm at -8 the total height is within 0.01 of -55.59", abs(ll_fit + elm[-1]["height_term"] + 55.59) < 0.01)

# ----------------------------------------------------------------------------- 5. the hill (S07)
def profile(bv):
    """For a fixed dial position, level the four clinics (bisection on each gamma) and return the height."""
    t = 0.0
    for k in FINITE:
        a, b_ = -20.0, 20.0
        for _ in range(200):
            m = (a + b_) / 2
            a, b_ = (m, b_) if observed(k) - expected(k, m, bv) > 0 else (a, m)
        t += loglik_clinic(k, (a + b_) / 2, bv)
    return t


grid = [round(0.1 * i, 1) for i in range(0, 41)]
prof = [(bv, profile(bv)) for bv in grid]
peak_b = max(prof, key=lambda r: r[1])[0]
pooled_step = float(logit(29 / 46) - logit(13 / 57))
p_pool, p_peak, p_zero = profile(pooled_step), profile(beta), profile(0.0)
check("the hill's top is at the fitted dial position, 2.02, at the fitted height", peak_b == 2.0 and abs(p_peak - ll_fit) < 1e-9
      and all(p_peak >= v for _, v in prof), f"grid peak {peak_b}, height {p_peak:.3f}")
check("the pooled step, 1.75, sits a little way down the left side (0.1 below the top)", abs(pooled_step - 1.753) < 5e-4 and 0.05 < p_peak - p_pool < 0.2,
      f"{p_pool:.3f}, {p_peak - p_pool:.3f} below")
check("the hill has one top: it rises to the peak and falls after it", all(b_[1] > a[1] for a, b_ in zip(prof[:21], prof[1:21])) and all(b_[1] < a[1] for a, b_ in zip(prof[21:], prof[22:])))

OUT = {
    "episode": 6, "title": "Fitting by Balance", "patients": N_PAT, "events": N_EV,
    "start": {"gamma": g0, "rate": rate0, "loglik": ll0, "likelihood_mantissa": mant, "likelihood_exponent": expo,
              "expected": E0, "o_minus_e": U0, "u_beta": ub0, "observed_high": obs_high, "expected_high": obs_high - ub0, "n_high": n_high},
    "dune": {"level_gamma": gD, "gain": gain, "u_beta_after": ub_dune, "overshoot_gamma": gOver, "overshoot_o_minus_e": uOver, "fall": fall},
    "dial": {"beta": bD, "o_minus_e": UD},
    "fit": {"beta": beta, "gamma": g, "loglik": ll_fit, "observed": {k: observed(k) for k in ALL}, "alder_split": list(split)},
    "elm": elm,
    "hill": {"profile": prof, "peak_beta": beta, "peak": p_peak, "pooled_beta": pooled_step, "pooled": p_pool, "at_zero": p_zero},
}

if __name__ == "__main__":
    print(f"plain guess: rate {100 * rate0:.2f}%, gamma {g0:.4f}, height {ll0:.3f}, likelihood {mant:.2f}e{expo}")
    print("meters:", {k: round(U0[k], 2) for k in ALL}, " dial:", round(ub0, 2))
    print(f"Dune alone: levels at {gD:.4f}, height +{gain:.3f}; at {gOver}: O - E {uOver:.2f}, height {fall:.2f}")
    print(f"dial alone: levels at {bD:.4f}; meters then", {k: round(UD[k], 2) for k in ALL})
    print(f"fit: beta {beta:.4f}, height {ll_fit:.3f}; Alder split {split[0]:.2f} + {split[1]:.2f}")
    print(f"hill: top {p_peak:.3f} at {beta:.3f}; pooled {pooled_step:.3f} -> {p_pool:.3f}; at zero {p_zero:.3f}")
    print()
    bad = 0
    for name, ok, detail in CHECKS:
        bad += not ok
        print(("PASS  " if ok else "FAIL  ") + name + (f"   [{detail}]" if detail else ""))
    print(f"\n{len(CHECKS) - bad} of {len(CHECKS)} checks pass")
    (HERE / "e06_numbers.json").write_text(json.dumps(OUT, indent=1))
    raise SystemExit(1 if bad else 0)
