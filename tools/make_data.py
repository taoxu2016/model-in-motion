"""Build the two small data files the episode needs (both deterministic).

data/crowd.json  the blueprint's simulated crowd of 200 providers (seed 2026, tau = 0.3), reduced to three ranks
                 per provider: by true effect, by raw rate, by case mix; plus the statistics quoted on screen.
data/luck.json   twelve re-deals of the five-clinic cast when every patient has the same chance 42/103.
"""
import json
import sys
from pathlib import Path

import numpy as np
from scipy.special import expit
from scipy.stats import binom, spearmanr, rankdata

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from mim.crowd import M, simulate  # noqa: E402

ROOT = (Path(sys.argv[1]) if len(sys.argv) > 1
        else Path(__file__).resolve().parents[1] / "logistic_fe" / "e01_unfair_comparisons").resolve()


def main():
    c = simulate()
    n, mu, gamma, raw = c["n"], c["mu"], c["gamma"], c["raw"]
    r_true = rankdata(gamma, method="ordinal") - 1          # 0 = truly best (lowest effect)
    r_raw = rankdata(raw, method="ordinal") - 1             # 0 = lowest raw rate
    r_mix = rankdata(mu, method="ordinal") - 1              # 0 = healthiest patients
    rho_true = spearmanr(raw, gamma)[0]
    rho_mix = spearmanr(raw, mu)[0]
    wrong = int(np.sum(r_raw // 40 != r_true // 40))
    wrong_mix = int(np.sum(r_raw // 40 != r_mix // 40))
    print(f"crowd: {M} providers, {n.sum()} patients; rank corr raw~true {rho_true:.3f}, raw~case mix {rho_mix:.3f}; "
          f"wrong fifth {wrong} of {M} (vs case-mix fifth: {wrong_mix})")
    (ROOT / "data" / "crowd.json").write_text(json.dumps({
        "rank_true": r_true.tolist(), "rank_raw": r_raw.tolist(), "rank_mix": r_mix.tolist(),
        "rho_true": round(float(rho_true), 3), "rho_mix": round(float(rho_mix), 3), "wrong_fifth": wrong}))

    sizes = {"Alder": 30, "Birch": 30, "Cedar": 20, "Dune": 12, "Elm": 11}
    p, K = 42 / 103, 12
    theory = {k: (int(binom.ppf(0.025, v, p)), int(binom.ppf(0.975, v, p))) for k, v in sizes.items()}
    best = None
    for seed in range(400):
        rng = np.random.default_rng(seed)
        draws = [[(rng.random(v) < p).tolist() for v in sizes.values()] for _ in range(K)]
        counts = np.array([[sum(c) for c in d] for d in draws])                   # K x 5
        lo, hi = counts.min(0), counts.max(0)
        miss = sum(abs(lo[j] - theory[k][0]) + abs(hi[j] - theory[k][1]) for j, k in enumerate(sizes))
        if best is None or miss < best[0]:
            best = (miss, seed, draws, counts)
    miss, seed, draws, counts = best
    print(f"luck: p = {p:.4f}, seed {seed}, miss {miss}")
    for j, (k, v) in enumerate(sizes.items()):
        print(f"  {k:6s} n={v:2d} theory 95% {theory[k][0]}-{theory[k][1]} of {v} "
              f"({100 * theory[k][0] / v:.0f}%-{100 * theory[k][1] / v:.0f}%), drawn {counts[:, j].tolist()}")
    (ROOT / "data" / "luck.json").write_text(json.dumps({"p": p, "seed": seed, "draws": draws,
                                                          "theory": {k: list(v) for k, v in theory.items()}}))


if __name__ == "__main__":
    main()
