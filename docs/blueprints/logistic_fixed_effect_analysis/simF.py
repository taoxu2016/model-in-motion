import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
from scipy.stats import norm
from crowd import *
from pprof_py.inference import EmpiricalNull
np.set_printoptions(precision=3, suppress=True, linewidth=170)
D = design(); n = D["n"]; planted = np.r_[D["pos"], D["neg"]]; other = np.setdiff1d(np.arange(M), planted)
small = n < 50; large = n >= 200; mid = ~small & ~large
c = norm.ppf(0.975)
print("== M19: the tau knob (same patients, same random numbers, provider differences scaled by tau)")
for tau in (0.0, 0.1, 0.2, 0.3):
    df, gamma = outcomes(D, tau); f = fit(df)
    r = f.test(test_method="poibin_exact"); z = r.z_raw.to_numpy(float); fl = r.flag.to_numpy().astype(float)
    se = np.sqrt(np.ravel(f.variances_["gamma_case_mix"]))
    pred = 2 * norm.sf(c / np.sqrt(1 + tau ** 2 / se ** 2))
    rs = f.test(test_method="score").flag.to_numpy().astype(float)
    line = (f"tau={tau}: flagged (exact) {int((fl != 0).sum())}/200 = {(fl != 0).mean():.3f}; non-planted {int((fl[other] != 0).sum())}/194 = {(fl[other] != 0).mean():.3f}; "
            f"n<50 {(fl[other][small[other]] != 0).mean():.3f}, mid {(fl[other][mid[other]] != 0).mean():.3f}, n>=200 {(fl[other][large[other]] != 0).mean():.3f}; "
            f"SD of z (non-planted) {z[other].std():.2f}; formula-predicted rate {pred[other].mean():.3f} (n>=200: {pred[other][large[other]].mean():.3f}); score flags {int((rs != 0).sum())}")
    print(line)
    for ng in (3,):
        re = f.test(test_method="poibin_exact", null_model=EmpiricalNull.fitter(size=f.provider_sizes_, n_groups=ng))
        fe = re.flag.to_numpy().astype(float)
        grp = re.groupby("null_group")[["null_mean", "null_sd"]].first()
        print(f"     empirical null ({ng} size groups): flagged {int((fe != 0).sum())}/200; non-planted {int((fe[other] != 0).sum())}; planted flags {fe[planted]} (theoretical: {fl[planted]}); null sd by group {grp.null_sd.round(2).to_numpy()} mean {grp.null_mean.round(2).to_numpy()}")
    re1 = f.test(test_method="poibin_exact", null_model=EmpiricalNull.fitter()); fe1 = re1.flag.to_numpy().astype(float)
    print(f"     empirical null (one group): flagged {int((fe1 != 0).sum())}; null sd {re1.null_sd.iloc[0]:.2f} mean {re1.null_mean.iloc[0]:.2f}; planted {fe1[planted]}")
print("group sizes: n<50", small.sum(), "mid", mid.sum(), "n>=200", large.sum(), "; planted sizes", n[planted])
print("example: SE 0.1, tau 0.3 -> SD of z", np.sqrt(1 + 0.3 ** 2 / 0.1 ** 2).round(2), "; SE 0.5 ->", np.sqrt(1 + 0.3 ** 2 / 0.5 ** 2).round(2), "; flag prob", (2 * norm.sf(c / np.sqrt(1 + 9))).round(3), (2 * norm.sf(c / np.sqrt(1 + 0.36))).round(3))
# funnel widened under the empirical null at tau = 0.3
df, gamma = outcomes(D, 0.3); f = fit(df)
fl0 = f.funnel_limits(); fl1 = f.funnel_limits(null_model=EmpiricalNull.fitter(size=f.provider_sizes_, n_groups=3))
p0, p1 = fl0.providers, fl1.providers
print("tau=0.3 funnel (score test): outside theoretical limits", int((p0.flag != 0).sum()), "; outside empirical limits", int((p1.flag.fillna(0) != 0).sum()))
for k in (planted[2], planted[5]):
    print("  provider size", n[k], "precision", p0.precision.iloc[k].round(1), "theoretical limits", p0.lower.iloc[k].round(3), p0.upper.iloc[k].round(3), "empirical limits", p1.lower.iloc[k].round(3), p1.upper.iloc[k].round(3), "O/E", p0.estimate.iloc[k].round(3))
print(fl1.test.groupby("null_group")[["null_mean", "null_sd"]].first().round(3))
# 20 replicate crowds at tau=0.3, no planted: average flag rates theoretical vs empirical
acc = {"th": [], "em": []}
for rep in range(20):
    dfr, _ = outcomes(D, 0.3, seed_y=20_000 + rep, plant=None) if False else outcomes(D, 0.3, seed_y=20_000 + rep)
    fr = fit(dfr)
    a = fr.test(test_method="poibin_exact").flag.to_numpy().astype(float); b = fr.test(test_method="poibin_exact", null_model=EmpiricalNull.fitter(size=fr.provider_sizes_, n_groups=3)).flag.to_numpy().astype(float)
    acc["th"].append((a[other] != 0).mean()); acc["em"].append((b[other] != 0).mean())
print("20 replicates at tau=0.3: mean flag rate among non-planted: theoretical", np.mean(acc["th"]).round(3), "empirical", np.mean(acc["em"]).round(3))
