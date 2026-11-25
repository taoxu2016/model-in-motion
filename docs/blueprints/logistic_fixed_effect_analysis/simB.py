import numpy as np, pandas as pd, warnings, logging, time
logging.disable(logging.CRITICAL); warnings.filterwarnings("ignore")
from scipy.special import expit
from scipy.stats import norm
from crowd import *
np.set_printoptions(precision=4, suppress=True, linewidth=160)
D = design(); n = D["n"]; planted = np.r_[D["pos"], D["neg"]]; null = np.setdiff1d(np.arange(M), planted)
print("== level crowd (tau=0, six planted at +-0.8)")
df, gamma = outcomes(D, 0.0); f = fit(df)
print("events", df.y.sum(), "rate", round(df.y.mean(), 4), "beta", np.ravel(f.coefficients_["beta"]).round(4), "gamma0", np.median(np.ravel(f.coefficients_["gamma"])).round(4))
res = {}
for tmeth in ("poibin_exact", "score", "wald"):
    t0 = time.time(); r = f.test(test_method=tmeth); el = time.time() - t0
    fl = r.flag.to_numpy().astype(float); res[tmeth] = r
    print(f"{tmeth:13s}: flagged among 194 null {int((fl[null] != 0).sum())} ({(fl[null] != 0).mean():.3f}); planted + caught {int((fl[D['pos']] == 1).sum())}/3 sizes {n[D['pos']]} flags {fl[D['pos']]}; "
          f"planted - caught {int((fl[D['neg']] == -1).sum())}/3 sizes {n[D['neg']]} flags {fl[D['neg']]}; time {el:.2f}s")
fl = f.funnel_limits(); p = fl.providers
print("funnel precision range", p.precision.min().round(2), p.precision.max().round(2), "; limits at min/max precision:", (1 - 1.96 / np.sqrt(p.precision.min())).round(3), (1 + 1.96 / np.sqrt(p.precision.min())).round(3),
      (1 - 1.96 / np.sqrt(p.precision.max())).round(3), (1 + 1.96 / np.sqrt(p.precision.max())).round(3))
print("planted providers on the funnel:"); print(p.loc[planted, ["observed", "expected", "estimate", "precision", "lower", "upper", "flag"]].round(3).to_string())
print("score-flag vs exact-flag crosstab"); print(pd.crosstab(res["score"].flag.rename("score"), res["poibin_exact"].flag.rename("exact")))
fl2 = f.funnel_limits(levels=(0.95, 0.998)); c = fl2.curves
print("99.8% limits at precision 10, 50:", (1 - norm.ppf(0.999) / np.sqrt(10)).round(3), (1 + norm.ppf(0.999) / np.sqrt(10)).round(3), (1 - norm.ppf(0.999) / np.sqrt(50)).round(3), (1 + norm.ppf(0.999) / np.sqrt(50)).round(3))
print("outside 99.8% limits:", int(((p.estimate > 1 + norm.ppf(0.999) / np.sqrt(p.precision)) | (p.estimate < 1 - norm.ppf(0.999) / np.sqrt(p.precision))).sum()))

print("\n== calibration of the three tests: 100 replicate level crowds without planted outliers (20,000 provider tests)")
rates = {k: [] for k in ("poibin_exact", "score", "wald")}; small = n < 50; large = n >= 200
acc = {k: {"all": [], "small": [], "large": []} for k in rates}
t0 = time.time()
for rep in range(100):
    dfr, _ = outcomes(D, 0.0, seed_y=10_000 + rep, plant=0.0)
    fr = fit(dfr)
    for k in rates:
        flg = fr.test(test_method=k).flag.to_numpy().astype(float) != 0
        acc[k]["all"].append(flg.mean()); acc[k]["small"].append(flg[small].mean()); acc[k]["large"].append(flg[large].mean())
print("time", round(time.time() - t0, 1), "s; small providers (n<50):", small.sum(), "large (n>=200):", large.sum())
for k in acc: print(f"{k:13s} flag rate at nominal 5%: all {np.mean(acc[k]['all']):.4f}, n<50 {np.mean(acc[k]['small']):.4f}, n>=200 {np.mean(acc[k]['large']):.4f}")
