import numpy as np, pandas as pd, warnings, logging
logging.disable(logging.CRITICAL)
warnings.filterwarnings("ignore")
from scipy.special import expit, logit

# cast: provider -> (n_low, events_low, n_high, events_high)
CAST = {
    "Alder": (24, 8, 6, 5),
    "Birch": (6, 1, 24, 13),
    "Cedar": (10, 2, 10, 6),
    "Dune":  (6, 2, 6, 5),
    "Elm":   (11, 0, 0, 0),
}
def build(cast=CAST):
    rows = []
    for prov, (n0, e0, n1, e1) in cast.items():
        rows += [(prov, 0, 1)] * e0 + [(prov, 0, 0)] * (n0 - e0)
        rows += [(prov, 1, 1)] * e1 + [(prov, 1, 0)] * (n1 - e1)
    return pd.DataFrame(rows, columns=["clinic", "x", "y"])

if __name__ == "__main__":
    d = build()
    print(d.groupby("clinic").agg(n=("y", "size"), events=("y", "sum"), high=("x", "sum")).assign(rate=lambda t: t.events / t.n))
    print("overall", len(d), d.y.sum(), d.y.mean())
    print(d.groupby("x").y.agg(["size", "sum", "mean"]))
    from pprof_py import LogisticFixedEffectModel
    m = LogisticFixedEffectModel().fit(d, y_var="y", x_vars=["x"], provider_var="clinic")
    print("providers", m.provider_ids_, "sizes", m.provider_sizes_)
    print("beta", m.coefficients_["beta"], "gamma", np.ravel(m.coefficients_["gamma"]))
    print("iters", m.algorithm.iter)
    print("var beta", m.variances_["beta"], "se gamma", np.sqrt(np.ravel(m.variances_["gamma"])), "se cm", np.sqrt(np.ravel(m.variances_["gamma_case_mix"])))
    sm = m.calculate_standardized_measures(stdz=["indirect", "direct"])
    print(sm["indirect"].round(4)); print(sm["direct"].round(4))
    for t in ["poibin_exact", "score", "wald"]:
        r = m.test(test_method=t)
        print(t); print(r.round(4).to_string())
