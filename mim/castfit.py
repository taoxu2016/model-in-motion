"""Model in Motion: the five-clinic cast and its fixed-effect fit, for number files (numpy only, no Manim).

The cast is the blueprint's running example; mim.common.CLINICS holds the same counts for drawing.
"""
import numpy as np

# clinic -> (lower-risk patients, of whom readmitted, higher-risk patients, of whom readmitted)
CAST = {"Alder": (24, 8, 6, 5), "Birch": (6, 1, 24, 13), "Cedar": (10, 2, 10, 6), "Dune": (6, 2, 6, 5), "Elm": (11, 0, 0, 0)}
FINITE = ["Alder", "Birch", "Cedar", "Dune"]          # clinics whose intercept has a finite estimate


def expit(z):
    return 1.0 / (1.0 + np.exp(-z))


def logit(p):
    return np.log(p / (1.0 - p))


def rows(names=FINITE):
    """Patient-level arrays: clinic index, x (1 = higher-risk), y (1 = readmitted)."""
    g, x, y = [], [], []
    for i, k in enumerate(names):
        n0, e0, n1, e1 = CAST[k]
        for xx, n, e in ((0, n0, e0), (1, n1, e1)):
            g += [i] * n
            x += [xx] * n
            y += [1] * e + [0] * (n - e)
    return np.array(g), np.array(x, float), np.array(y, float)


def fit(names=FINITE, shift=0.0, tol=1e-13, maxit=100):
    """Joint maximum likelihood for logit(p_ij) = gamma_i + beta (x_ij - shift), by Newton-Raphson.

    `shift` moves the zero of the risk factor: 0 codes lower-risk as zero, 1 codes higher-risk as zero.
    Returns ({clinic: gamma}, beta, covariance matrix, log-likelihood).
    """
    g, x, y = rows(names)
    m = len(names)
    Z = np.zeros((len(y), m + 1))
    Z[np.arange(len(y)), g] = 1.0
    Z[:, m] = x - shift
    th = np.zeros(m + 1)
    th[:m] = logit(y.mean())
    for _ in range(maxit):
        p = expit(Z @ th)
        info = Z.T @ (Z * (p * (1 - p))[:, None])
        step = np.linalg.solve(info, Z.T @ (y - p))
        th = th + step
        if np.max(np.abs(step)) < tol:
            break
    p = expit(Z @ th)
    return dict(zip(names, th[:m].tolist())), float(th[m]), np.linalg.inv(info), float(np.sum(y * np.log(p) + (1 - y) * np.log(1 - p)))


def coin_pmf(ps):
    """Distribution of the number of heads among coins with chances `ps`, built exactly, one coin at a time (Episode 13)."""
    f = np.zeros(len(ps) + 1)
    f[0] = 1.0
    for k, p in enumerate(ps):
        f[1:k + 2] = f[1:k + 2] * (1.0 - p) + f[0:k + 1] * p      # each bar splits: tails stays, heads moves one step right
        f[0] *= 1.0 - p
    return f


def mid_p(f, observed):
    """Two-sided mid-p for an observed count: twice the smaller tail, counting half of the bar at the count itself."""
    up = float(f[observed + 1:].sum() + 0.5 * f[observed])
    down = float(f[:observed].sum() + 0.5 * f[observed])
    return 2.0 * min(up, down)
