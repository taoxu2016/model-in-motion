"""Model in Motion · Logistic Fixed-Effect · Episode 4: preview stills for the script review.

Three key frames, drawn from e04_numbers.json so the pictures cannot disagree with the checked numbers.
These are matplotlib sketches in the series palette, not Manim renders: they show what each frame claims,
where things collide, and what needs a design decision before animation.

    python e04_numbers.py && python preview_stills.py      # writes stills/e04_frame_*.png
"""
from __future__ import annotations

import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrowPatch

HERE = Path(__file__).resolve().parent
N = json.loads((HERE / "e04_numbers.json").read_text())
OUT = HERE / "stills"
OUT.mkdir(exist_ok=True)

# series palette (episode/common.py of Episodes 1-3)
INK, INK_2, PAPER, MUTED, FAINT = "#0E1621", "#16212F", "#F3EEE4", "#8C9AAB", "#33445A"
HUE = {"Alder": "#E69F00", "Birch": "#56B4E9", "Cedar": "#AEB9C6", "Dune": "#CC79A7", "Elm": "#3CC59A"}
ACCENT, ALERT = "#F0E442", "#E8705A"
SANS, DISPLAY, SERIF = "Inter", "Inter Display", "Lora"
plt.rcParams.update({"font.family": SANS, "text.color": PAPER, "axes.edgecolor": FAINT, "figure.facecolor": INK,
                     "axes.facecolor": INK, "savefig.facecolor": INK, "mathtext.fontset": "cm"})

expit = lambda z: 1 / (1 + np.exp(-z))
logit = lambda p: np.log(p / (1 - p))
FIN = ["Alder", "Birch", "Cedar", "Dune"]
DODGE = {"Alder": -0.05, "Dune": 0.05, "Birch": -0.075, "Cedar": 0.06, "Elm": 0.0}   # Alder's and Dune's dots coincide exactly
obs, fit, pooled, beta = N["observed"], N["fit"]["clinics"], N["pooled"], N["fit"]["beta"]
Y0, Y1 = -3.45, 2.45


def panel(title, aside):
    fig = plt.figure(figsize=(16, 9), dpi=100)
    ax = fig.add_axes([0.075, 0.13, 0.635, 0.70])
    ax.set_xlim(-1.0, 1.55); ax.set_ylim(Y0, Y1)
    for s in ("top", "bottom"):
        ax.spines[s].set_visible(False)
    ax.spines["left"].set_color(MUTED); ax.spines["right"].set_color(MUTED)
    ax.set_yticks([-3, -2, -1, 0, 1, 2]); ax.set_yticklabels(["−3", "−2", "−1", "0", "+1", "+2"], color=MUTED, fontsize=15)
    ax.tick_params(axis="y", colors=MUTED, length=5)
    ax.set_ylabel("log-odds", color=MUTED, fontsize=15, labelpad=10)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["lower-risk patients", "higher-risk patients"], color=PAPER, fontsize=17)
    ax.tick_params(axis="x", length=0, pad=14)
    ax.axhline(0, color=FAINT, lw=1, zorder=0)
    for x in (0, 1):
        ax.axvline(x, color=FAINT, lw=1, zorder=0)
    r = ax.twinx(); r.set_ylim(Y0, Y1)
    probs = [0.05, 0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90]
    r.set_yticks([logit(p) for p in probs]); r.set_yticklabels([f"{round(100 * p)}%" for p in probs], color=PAPER, fontsize=15)
    r.tick_params(axis="y", colors=MUTED, length=5)
    for s in ("top", "bottom"):
        r.spines[s].set_visible(False)
    r.spines["left"].set_color(MUTED); r.spines["right"].set_color(MUTED)
    r.set_ylabel("probability of readmission", color=MUTED, fontsize=15, labelpad=12)
    fig.text(0.075, 0.925, title, fontsize=30, family=DISPLAY, weight="semibold", color=PAPER)
    fig.text(0.075, 0.875, aside, fontsize=18, family=SERIF, style="italic", color=MUTED)
    fig.text(0.985, 0.025, "preview still · drawn from e04_numbers.json · not a final render", fontsize=11, color=FAINT, ha="right")
    return fig, ax


def dots(ax, alpha=1.0, ring=False):
    for k in FIN:
        for x, key, n in ((0, "logodds_low", obs[k]["n_low"]), (1, "logodds_high", obs[k]["n_high"])):
            ax.scatter([x + DODGE[k]], [obs[k][key]], s=26 * n, color=HUE[k], alpha=alpha, zorder=5,
                       edgecolors=INK if not ring else PAPER, linewidths=1.5)


def elm_marker(ax, text="Elm · 0 of 11 readmitted\nno finite position"):
    y = Y0 + 0.36
    ax.scatter([0], [y], s=26 * obs["Elm"]["n_low"], facecolors="none", edgecolors=HUE["Elm"], hatch="////", linewidths=1.8, zorder=5)
    ax.add_patch(FancyArrowPatch((0, y - 0.13), (0, Y0 + 0.02), arrowstyle="-|>", mutation_scale=16, color=HUE["Elm"], lw=2, zorder=6))
    ax.text(0.10, y - 0.02, text, color=HUE["Elm"], fontsize=14, va="center", linespacing=1.35)


def legend_sizes(fig):
    fig.text(0.815, 0.30, "dot area = number of patients", fontsize=13, color=MUTED)
    lax = fig.add_axes([0.815, 0.18, 0.165, 0.10]); lax.axis("off"); lax.set_xlim(0, 3); lax.set_ylim(0, 1)
    for x, n in ((0.35, 6), (1.3, 12), (2.4, 24)):
        lax.scatter([x], [0.62], s=26 * n, color=MUTED, edgecolors=INK)
        lax.text(x, 0.02, str(n), color=MUTED, fontsize=12, ha="center")


def names(fig, ys, extra=None):
    for k, y in ys.items():
        fig.text(0.815, y, "●", color=HUE[k], fontsize=17, va="center")
        fig.text(0.837, y, k + (f"   {extra[k]}" if extra and k in extra else ""), color=PAPER, fontsize=16, va="center")


# ------------------------------------------------------------------ frame A: the cold open (S01)
fig, ax = panel("One line for everyone", "the pooled standard from Episode 3, with the clinics put back")
a, b = pooled["start"], pooled["start"] + pooled["step"]
ax.plot([-0.3, 1.3], [a - 0.3 * pooled["step"], b + 0.3 * pooled["step"]], color=MUTED, lw=3, ls=(0, (6, 4)), zorder=3)
ax.scatter([0, 1], [a, b], s=150, facecolors=INK, edgecolors=MUTED, linewidths=2.5, zorder=4)
ax.text(1.33, b + 0.3 * pooled["step"] + 0.05, "pooled\nstandard", color=MUTED, fontsize=14, va="center", linespacing=1.2)
ax.text(-0.33, a - 0.3 * pooled["step"] - 0.02, f"{round(100 * pooled['rate_low'])}% → {round(100 * pooled['rate_high'])}%", color=MUTED, fontsize=14, va="center", ha="right")
for k in FIN:                                           # the misses
    for x, key, line in ((0, "logodds_low", a), (1, "logodds_high", b)):
        ax.plot([x + DODGE[k]] * 2, [line, obs[k][key]], color=HUE[k], lw=2, alpha=0.75, zorder=2)
dots(ax)
elm_marker(ax, "Elm · 0 of 11 readmitted\noff the bottom of the chart")
names(fig, {"Alder": 0.70, "Dune": 0.655, "Birch": 0.59, "Cedar": 0.545}, {"Alder": "above", "Dune": "above", "Birch": "below", "Cedar": "below"})
fig.text(0.815, 0.745, "against the pooled line,\nat both ends", fontsize=13, color=MUTED, linespacing=1.35, va="bottom")
legend_sizes(fig)
fig.savefig(OUT / "e04_frame_A_cold_open.png"); plt.close(fig)

# ------------------------------------------------------------------ frame B: the fitted lines (S05)
fig, ax = panel("Where the lines land", "one shared step, one intercept per clinic · dots are what happened, lines are the model")
xs = np.array([-0.32, 1.32])
for k in FIN:
    ax.plot(xs, fit[k]["gamma"] + beta * xs, color=HUE[k], lw=3.2, zorder=3, solid_capstyle="round")
dots(ax, alpha=0.9)
# the shared step, drawn on Birch's line (the lowest, so it stays clear of the others)
gB = fit["Birch"]["gamma"]
ax.plot([0, 1], [gB, gB], color=ACCENT, lw=1.6, ls=(0, (3, 3)), zorder=4)
ax.add_patch(FancyArrowPatch((1, gB), (1, gB + beta), arrowstyle="-|>", mutation_scale=18, color=ACCENT, lw=2.6, zorder=6))
ax.text(1.04, gB + 0.42, f"β = {beta:.2f}\nodds × {N['fit']['odds_ratio']:.1f}", color=ACCENT, fontsize=16, va="center", weight="semibold", linespacing=1.3)
# gamma labels at the left end; Alder and Dune are 0.07 apart, so their labels are spread and joined by leaders
lab = {"Dune": fit["Dune"]["gamma"] - 0.32 * beta + 0.30, "Alder": fit["Alder"]["gamma"] - 0.32 * beta - 0.22,
       "Cedar": fit["Cedar"]["gamma"] - 0.32 * beta + 0.12, "Birch": fit["Birch"]["gamma"] - 0.32 * beta - 0.16}
for k in FIN:
    y_end = fit[k]["gamma"] - 0.32 * beta
    ax.plot([-0.335, -0.36], [y_end, lab[k]], color=HUE[k], lw=1.2, zorder=3)
    ax.text(-0.37, lab[k], f"{k}  γ = {fit[k]['gamma']:.2f}".replace("-", "−"), color=HUE[k], fontsize=15, va="center", ha="right", weight="semibold")
# Elm's line leaving the panel
gE = -4.35                                              # any value will do: Elm's line has the shared tilt and keeps sinking
xe = np.array([(Y0 - gE) / beta, 1.32])
ax.plot(xe, gE + beta * xe, color=HUE["Elm"], lw=3.2, alpha=0.55, ls=(0, (2, 2)), zorder=2)
for xa_ in (1.08, 1.26):
    ya_ = gE + beta * xa_
    ax.add_patch(FancyArrowPatch((xa_, ya_ - 0.10), (xa_, ya_ - 0.62), arrowstyle="-|>", mutation_scale=14, color=HUE["Elm"], lw=1.8, alpha=0.8, zorder=2))
elm_marker(ax, "Elm · 0 of 11 readmitted\nits line keeps sinking: no finite γ")
names(fig, {"Dune": 0.70, "Alder": 0.655, "Cedar": 0.61, "Birch": 0.565},
      {k: f"{round(100 * fit[k]['p_low'])}% → {round(100 * fit[k]['p_high'])}%" for k in FIN})
fig.text(0.815, 0.745, "the model's probabilities", fontsize=13, color=MUTED)
fig.text(0.815, 0.47, "103 patients:\nrough estimates", fontsize=14, color=MUTED, family=SERIF, style="italic", linespacing=1.4)
legend_sizes(fig)
fig.savefig(OUT / "e04_frame_B_fitted_lines.png"); plt.close(fig)

# ------------------------------------------------------------------ frame C: the same model on the probability ruler (S05)
fig = plt.figure(figsize=(16, 9), dpi=100)
ax = fig.add_axes([0.10, 0.15, 0.66, 0.68])
s = np.linspace(-3.6, 5.6, 600)
ax.set_xlim(s[0], s[-1]); ax.set_ylim(-0.03, 1.03)
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.spines["left"].set_color(MUTED); ax.spines["bottom"].set_color(MUTED)
ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(["0%", "25%", "50%", "75%", "100%"], color=PAPER, fontsize=15)
ax.tick_params(colors=MUTED, length=5)
ax.set_ylabel("probability of readmission", color=MUTED, fontsize=15, labelpad=10)
ax.set_xticks([0, beta]); ax.set_xticklabels(["lower-risk\npatients", "higher-risk\npatients"], color=PAPER, fontsize=16)
ax.set_xlabel("risk score: the steps added on the log-odds ruler", color=MUTED, fontsize=14, labelpad=12)
for x in (0, beta):
    ax.axvline(x, color=FAINT, lw=1.2, zorder=0)
ax.axhline(0.5, color=FAINT, lw=1, zorder=0)
for k in FIN:
    ax.plot(s, expit(fit[k]["gamma"] + s), color=HUE[k], lw=3.2, zorder=3)
    ax.scatter([0, beta], [fit[k]["p_low"], fit[k]["p_high"]], s=130, color=HUE[k], edgecolors=INK, linewidths=1.5, zorder=5)
for k, dx, ha in (("Birch", 0.16, "left"), ("Alder", -0.16, "right")):
    for x, p in ((0, fit[k]["p_low"]), (beta, fit[k]["p_high"])):
        ax.text(x + dx, p + (-0.045 if k == "Birch" else 0.045), f"{round(100 * p)}%", color=HUE[k], fontsize=17, weight="semibold", ha=ha, va="center")
# the sideways slide between Birch's and Alder's curves, read where both cross 50%
xa, xb = -fit["Alder"]["gamma"], -fit["Birch"]["gamma"]
ax.add_patch(FancyArrowPatch((xa, 0.5), (xb, 0.5), arrowstyle="<|-|>", mutation_scale=15, color=PAPER, lw=1.8, zorder=6))
ax.text(xb + 0.75, 0.43, "same shape,\nslid sideways", color=PAPER, fontsize=14, ha="left", va="center", family=SERIF, style="italic", linespacing=1.25)
ax.plot([xb + 0.08, xb + 0.68], [0.492, 0.445], color=PAPER, lw=1.0, zorder=6)
fig.text(0.10, 0.925, "One shape, slid sideways", fontsize=30, family=DISPLAY, weight="semibold", color=PAPER)
fig.text(0.10, 0.875, "the parallel lines of the last frame, redrawn on the probability ruler", fontsize=18, family=SERIF, style="italic", color=MUTED)
names(fig, {"Dune": 0.70, "Alder": 0.655, "Cedar": 0.61, "Birch": 0.565},
      {k: f"{round(100 * fit[k]['p_low'])}% → {round(100 * fit[k]['p_high'])}%" for k in FIN})
fig.text(0.815, 0.745, "the model's probabilities", fontsize=13, color=MUTED)
fig.text(0.815, 0.40, "Only the two marked positions\nhold patients in the cast. The rest\nof each curve is the model's shape.", fontsize=13, color=MUTED, family=SERIF, style="italic", linespacing=1.45)
fig.text(0.985, 0.025, "preview still · drawn from e04_numbers.json · not a final render", fontsize=11, color=FAINT, ha="right")
fig.savefig(OUT / "e04_frame_C_probability.png"); plt.close(fig)
print("wrote", sorted(p.name for p in OUT.glob("*.png")))
