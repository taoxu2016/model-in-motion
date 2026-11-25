import numpy as np, pandas as pd, warnings, logging
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit, logit
from scipy.linalg import cho_factor, cho_solve
from cast import CAST, build
np.set_printoptions(precision=4, suppress=True, linewidth=170)
d = build().sort_values("clinic").reset_index(drop=True)
names = list(CAST)
idx = d.clinic.map({k: i for i, k in enumerate(names)}).to_numpy(); X = d[["x"]].to_numpy(float); y = d.y.to_numpy(float)
m = 5
def ll(g, b): 
    lin = g[idx] + X @ b; return np.sum(y * lin - np.logaddexp(0, lin))
def serbin(tol=1e-8, bound=10.0, max_iter=10000, verbose=True, X=X):
    ybar = y.mean(); g = np.full(m, logit(ybar)); b = np.zeros(X.shape[1]); crit = np.inf; it = 0; s, t = 0.01, 0.6
    if verbose: print("start gamma", g[0], "beta", b, "ll", ll(g, b))
    while it <= max_iter and crit >= tol:
        it += 1
        p = expit(g[idx] + X @ b); q = np.maximum(p * (1 - p), 1e-20); r = y - p
        Ug = np.bincount(idx, weights=r, minlength=m); Ub = X.T @ r
        Dinv = 1 / np.bincount(idx, weights=q, minlength=m)
        qX = q[:, None] * X; Bt = np.vstack([np.bincount(idx, weights=qX[:, c], minlength=m) for c in range(X.shape[1])])  # p x m
        A = X.T @ qX
        J1 = Bt * Dinv; S = A - J1 @ Bt.T; c = cho_factor(S); J2 = cho_solve(c, J1); sU = cho_solve(c, Ub)
        dg = Dinv * Ug + J2.T @ (J1 @ Ug - Ub); db = sU - J2 @ Ug
        v = 1.0; l0 = ll(g, b); dl = ll(g + v * dg, b + v * db) - l0; lam = np.r_[Ug, Ub] @ np.r_[dg, db]
        nb = 0
        while dl < s * v * lam and not (0.0 < s * v * lam <= 1e-12 * (1 + abs(l0))):
            v *= t; nb += 1; dl = ll(g + v * dg, b + v * db) - l0
        if verbose and it == 1:
            print("   iter1 scores: U_gamma", Ug, "U_beta", Ub, "D", 1 / Dinv, "B", Bt, "A", A, "S", S)
            print("   iter1 steps : d_gamma", dg, "d_beta", db)
        g = g + v * dg; med = np.median(g); g = np.clip(g, med - bound, med + bound)
        bn = b + v * db; crit = np.max(np.abs(b - bn)); b = bn
        if verbose: print(f"iter {it}: v={v:.3f} backtracks={nb} beta={b} gamma={g} ll={ll(g, b):.5f} crit={crit:.2e}")
    return g, b, it
g, b, it = serbin()
print("final", g, b, it)
for tol in (1e-4, 1e-5, 1e-6, 1e-8, 1e-10, 1e-12):
    g2, b2, it2 = serbin(tol=tol, verbose=False); print("tol", tol, "iters", it2, "Elm gamma", g2[4], "beta", b2)
print("\nElm's own log-likelihood term: -11*log(1+exp(g))")
for gg in (-1.52, -2, -3, -4, -6.25, -8, -11.52, -20): print(gg, round(-11 * np.logaddexp(0, gg), 5))
# BAN replicate (centred), following pprof_py
def ban(center=True, shift=0.0, tol=1e-8, bound=10.0, max_iter=100000, verbose=False):
    Xs = X + shift; xbar = Xs.mean(0) if center else np.zeros(Xs.shape[1]); Xc = Xs - xbar
    def llc(g, b): 
        lin = g[idx] + Xc @ b; return np.sum(y * lin - np.logaddexp(0, lin))
    g = np.full(m, logit(y.mean())); b = np.zeros(1); gc = bc = np.inf; it = 0; s, t = 0.01, 0.6; path = [(g.copy(), b.copy())]
    while it < max_iter and max(gc, bc) > tol:
        it += 1; g_old = g.copy()
        p = expit(g[idx] + Xc @ b); q = np.maximum(p * (1 - p), 1e-20); r = y - p
        Ug = np.bincount(idx, weights=r, minlength=m); Ig = np.bincount(idx, weights=q, minlength=m); dg = Ug / Ig
        v = 1.0; l0 = llc(g, b); lam = Ug @ dg
        while not (llc(g + v * dg, b) - l0 >= s * v * lam or (0.0 < s * v * lam <= 1e-12 * (1 + abs(l0)))): v *= t
        g = g + v * dg; med = np.median(g); g = np.clip(g, med - bound, med + bound); gc = np.max(np.abs(g - g_old))
        p = expit(g[idx] + Xc @ b); q = np.maximum(p * (1 - p), 1e-20); r = y - p
        Ub = Xc.T @ r; Ib = Xc.T @ (q[:, None] * Xc); db = np.linalg.solve(Ib, Ub)
        v = 1.0; l0 = llc(g, b); lam = Ub @ db
        while not (llc(g, b + v * db) - l0 >= s * v * lam or (0.0 < s * v * lam <= 1e-12 * (1 + abs(l0)))): v *= t
        bn = b + v * db; bc = np.max(np.abs(b - bn)); b = bn; path.append((g.copy(), b.copy()))
        if verbose and it <= 6: print(f"  BAN iter {it}: beta={b} gamma={g - xbar @ b}")
    return g - xbar @ b, b, it, path
gB, bB, itB, path = ban(verbose=True); print("BAN centred: iters", itB, "beta", bB, "gamma", gB)
for sh in (0.0, 5.0, 50.0):
    gU, bU, itU, _ = ban(center=False, shift=sh, max_iter=200000); print(f"BAN uncentred, x shifted by {sh}: iters", itU, "beta", bU)
from pprof_py import LogisticFixedEffectModel
mb = LogisticFixedEffectModel(algorithm="Ban").fit(build(), y_var="y", x_vars=["x"], provider_var="clinic")
gb = np.ravel(mb.coefficients_["gamma"]); print("pprof BAN gamma", gb, "iters", mb.algorithm.iter, "weighted mean reference", np.average(gb, weights=mb.provider_sizes_))
ms = LogisticFixedEffectModel().fit(build(), y_var="y", x_vars=["x"], provider_var="clinic")
gs = np.ravel(ms.coefficients_["gamma"]); print("pprof SerBIN gamma", gs, "weighted mean reference", np.average(gs, weights=ms.provider_sizes_), "medians", np.median(gs), np.median(gb))
print("BAN direct rate Elm:", mb.calculate_standardized_measures(stdz="direct")["direct"].round(5).to_string())
