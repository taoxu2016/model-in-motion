"""Model in Motion: the simulated crowd of providers (blueprint appendix, seed 2026).

numpy and scipy only, so number files can import it without Manim.
"""
import numpy as np
from scipy.special import expit

BETA, G0, RHO, SD_MU, M = np.array([0.8, 0.5]), -1.5, -0.6, 0.6, 200


def simulate(seed=2026, tau=0.3, plant=0.8, rho=RHO):
    """The series' crowd of 200 providers. Returns provider-level and patient-level arrays.

    The random draws are in the order Episode 1 used, so the same seed gives the same crowd.
    rho is the link between a provider's effect and its case mix; rho=0 breaks it (Episode 17), using the same draws."""
    rng = np.random.default_rng(seed)
    n = np.round(np.exp(rng.uniform(np.log(20), np.log(500), M))).astype(int)
    mu = rng.normal(0, SD_MU, M)
    eps = rng.normal(size=M)
    u = rho * mu / SD_MU + np.sqrt(1 - rho ** 2) * eps
    prov = np.repeat(np.arange(M), n)
    x1 = rng.normal(mu[prov], 1.0)
    x2 = rng.binomial(1, 0.3, prov.size).astype(float)
    order = np.argsort(n, kind="stable")
    pos = [order[int(q * (M - 1))] for q in (0.15, 0.50, 0.85)]
    neg = [order[int(q * (M - 1)) + 1] for q in (0.15, 0.50, 0.85)]
    rng_y = np.random.default_rng(seed + 1)
    gamma = G0 + tau * u
    gamma[pos] = G0 + plant
    gamma[neg] = G0 - plant
    y = (rng_y.random(prov.size) < expit(gamma[prov] + BETA[0] * x1 + BETA[1] * x2)).astype(int)
    raw = np.bincount(prov, weights=y) / n
    return {"n": n, "mu": mu, "gamma": gamma, "raw": raw, "prov": prov, "x1": x1, "x2": x2, "y": y, "u": u,
            "planted_high": pos, "planted_low": neg}


def fit_fixed_effects(X, y, prov, tol=1e-10, max_iter=100):
    """Fixed-effect logistic fit for any set of covariates, by joint Newton steps through the fold (Episode 8).

    One intercept per provider and one coefficient per column of X. Returns (gamma, beta, steps)."""
    X, y = np.asarray(X, dtype=float), np.asarray(y, dtype=float)
    m, k = int(prov.max()) + 1, X.shape[1]
    g, b = np.full(m, float(np.log(y.mean() / (1.0 - y.mean())))), np.zeros(k)
    for steps in range(1, max_iter + 1):
        p = expit(g[prov] + X @ b)
        w, r = p * (1.0 - p), y - p
        U, V = np.bincount(prov, weights=r, minlength=m), np.bincount(prov, weights=w, minlength=m)
        B = np.column_stack([np.bincount(prov, weights=w * X[:, j], minlength=m) for j in range(k)])
        S = X.T @ (X * w[:, None]) - B.T @ (B / V[:, None])
        db = np.linalg.solve(S, X.T @ r - B.T @ (U / V))
        dg = (U - B @ db) / V
        g, b = g + dg, b + db
        if max(np.max(np.abs(db)), np.max(np.abs(dg))) < tol:
            break
    return g, b, steps


def joint_fit(c, tol=1e-10, max_iter=100):
    """Fixed-effect logistic fit of a simulated crowd on its two risk factors.

    Returns the provider effects, the two coefficients and the patient-level arrays later episodes reuse."""
    X, y, prov = np.column_stack([c["x1"], c["x2"]]), c["y"].astype(float), c["prov"]
    g, b, steps = fit_fixed_effects(X, y, prov, tol=tol, max_iter=max_iter)
    return {"gamma": g, "beta": b, "X": X, "y": y, "prov": prov, "steps": steps}


def case_mix_se(fit):
    """Standard error of each provider effect at the average case mix (Episode 9): its own part plus its share of the coefficients'."""
    g, b, X, prov = fit["gamma"], fit["beta"], fit["X"], fit["prov"]
    m = len(g)
    p = expit(g[prov] + X @ b)
    w = p * (1.0 - p)
    V = np.bincount(prov, weights=w, minlength=m)
    B = np.column_stack([np.bincount(prov, weights=w * X[:, k], minlength=m) for k in range(X.shape[1])])
    S = X.T @ (X * w[:, None]) - B.T @ (B / V[:, None])
    dev = B / V[:, None] - X.mean(axis=0)
    return np.sqrt(1.0 / V + np.einsum("ij,jk,ik->i", dev, np.linalg.inv(S), dev))
