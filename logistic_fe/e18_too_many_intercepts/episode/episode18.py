"""Model in Motion · The Logistic Fixed-Effect Model · Episode 18: Too Many Intercepts (when one intercept per provider bends the shared rule).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode18.py S04_Sweep      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e18_numbers.json, written by e18_numbers.py; none is typed here. The joint fit is drawn in the
alert red wherever it is wrong, the truth in the cedar grey, and the conditional fit in green.
All content stays above y = -3.0, clear of the captions.
"""
from __future__ import annotations

import sys
from pathlib import Path

import os  # noqa: E402

os.environ["MIM_EPISODE"] = str(Path(__file__).resolve().parents[1])   # this episode's folder
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))           # the repository root, for the shared mim package
from mim.common import *  # noqa: E402,F403
from mim.kit import *  # noqa: E402,F403
from mim.lines import *  # noqa: E402,F403
from mim.boards import *  # noqa: E402,F403
from mim.funnel import Funnel  # noqa: E402

N = json.loads((ROOT / "e18_numbers.json").read_text())
PAIRS, SWEEP, PRACTICE, TRUE, SIZES = N["pairs"], N["sweep"], N["practice"], N["beta"], N["sizes"]
SX = 4.5                                            # centre of the side column
JOINT, TRUTH, COND = ALERT, CEDAR, GOOD


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def prob(v):
    return 1.0 / (1.0 + float(np.exp(-v)))


def marker(color=PAPER, h=0.3):
    """An intercept: a short upright stroke with a bead on it."""
    return VGroup(Line(DOWN * h / 2, UP * h / 2, stroke_width=3, color=color), Dot(radius=0.06, color=color))


def pair_field(cy=0.0, cols=40):
    """The first four hundred pairs of the world on screen: two dots a pair, filled where the patient was readmitted."""
    g = VGroup()
    for a, b in PAIRS["outcomes"]:
        g.add(VGroup(*[Dot(radius=0.05, color=PAPER) if v else Circle(radius=0.05, stroke_color=PAPER, stroke_width=1.6) for v in (a, b)]).arrange(RIGHT, buff=0.03))
    return g.arrange_in_grid(cols=cols, buff=(0.085, 0.2)).move_to([0, cy, 0])


class Scale:
    """A flat scale for the shared rule's coefficient."""

    def __init__(self, x0=-5.4, x1=5.4, lo=0.0, hi=1.5, y=-0.6):
        self.x0, self.x1, self.lo, self.hi, self.y = x0, x1, lo, hi, y

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (v - self.lo) / (self.hi - self.lo)

    def axis(self, ticks=(0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5)):
        return VGroup(Line([self.x0, self.y, 0], [self.x1, self.y, 0], stroke_width=3, color=MUTED), *[VGroup(Line([self.X(v), self.y, 0], [self.X(v), self.y - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([self.X(v), self.y - 0.3, 0])) for v in ticks],
                      side("the shared rule's coefficient", size=16).move_to([0, self.y - 0.65, 0]))

    def flag(self, v, label, color, up=1.0):
        return VGroup(Line([self.X(v), self.y, 0], [self.X(v), self.y + up, 0], stroke_width=4, color=color), big(label, size=22, color=color).move_to([self.X(v), self.y + up + 0.28, 0]))


class SizeChart:
    """The fitted rule over the true one, against provider size (log scale)."""

    def __init__(self, x0=-5.4, x1=1.0, y0=-2.0, y1=2.1, lo=0.9, hi=2.1):
        self.x0, self.x1, self.y0, self.y1, self.lo, self.hi = x0, x1, y0, y1, lo, hi

    def X(self, n):
        return self.x0 + (self.x1 - self.x0) * (np.log(n) - np.log(1.6)) / (np.log(130.0) - np.log(1.6))

    def Y(self, r):
        return self.y0 + (self.y1 - self.y0) * (r - self.lo) / (self.hi - self.lo)

    def frame(self):
        g = VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], stroke_width=3, color=MUTED), Line([self.x0, self.y0, 0], [self.x0, self.y1, 0], stroke_width=3, color=MUTED))
        g.add(*[VGroup(Line([self.X(n), self.y0, 0], [self.X(n), self.y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(n), 15, MUTED).move_to([self.X(n), self.y0 - 0.28, 0])) for n in SIZES])
        g.add(*[VGroup(Line([self.x0 - 0.1, self.Y(v), 0], [self.x0, self.Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:.2f}", 14, MUTED).move_to([self.x0 - 0.42, self.Y(v), 0])) for v in (1.0, 1.25, 1.5, 1.75, 2.0)])
        g.add(DashedLine([self.x0, self.Y(1.0), 0], [self.x1, self.Y(1.0), 0], dash_length=0.1, stroke_width=2.5, color=TRUTH), side("the truth", size=14, color=TRUTH).move_to([self.x1 - 0.5, self.Y(1.0) - 0.2, 0]))
        g.add(side("patients in each provider", size=15).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.6, 0]), side("the fitted rule, as a multiple of the true one", size=15).move_to([self.x0, self.y1 + 0.26, 0], aligned_edge=LEFT))
        return g

    def points(self, key, color, labels=True, dy=0.3):
        g = VGroup()
        for n in SIZES:
            r = SWEEP[str(n)][key]
            d = VGroup(Dot([self.X(n), self.Y(r), 0], radius=0.1, color=color).set_z_index(5))
            if labels:
                d.add(txt(f"{r:.2f}", 17, color, weight=SEMIBOLD).move_to([self.X(n) + 0.5, self.Y(r), 0] if n == SIZES[0] else [self.X(n) + 0.05, self.Y(r) + dy, 0]))
            g.add(d)
        return g


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        one = VGroup(marker(ACCENT), VGroup(chip(PAPER, True, 0.2), chip(PAPER, False, 0.2)).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.2).move_to([0, 0.6, 0])
        one_l = side("one provider: its own intercept, and two patients", size=18, color=PAPER).next_to(one, DOWN, buff=0.35)
        field = pair_field(0.35)
        count = VGroup(big(f"{PAIRS['providers']:,} providers", size=28), side(f"{N['patients']:,} patients; the first 400 pairs are shown", size=16)).arrange(DOWN, buff=0.08).move_to([0, 2.6, 0])
        share = side("an intercept for every pair, and one risk rule shared by all", size=18, color=PAPER).move_to([0, -2.2, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(one), FadeIn(one_l), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(VGroup(one, one_l)), run_time=0.5)
            self.play(FadeIn(field, lag_ratio=0.002), FadeIn(count), run_time=1.6)
            seg.wait_until(seg.word(1, "Each pair has its own intercept"))
            self.play(FadeIn(share), run_time=0.7)

        Sc = Scale()
        axis = Sc.axis()
        truth = Sc.flag(TRUE, f"the truth: {TRUE}", TRUTH)
        ask = big("what should the fit return?", size=28, color=ACCENT).move_to([0, 2.2, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(field, count, share)), run_time=0.6)
            self.play(FadeIn(axis), run_time=0.8)
            seg.wait_until(seg.word(0, "a coefficient of"))
            self.play(FadeIn(truth), run_time=0.7)
            seg.wait_until(seg.s(1) + 1.6)
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.8)

        fit = Sc.flag(PAIRS["beta"], f"the fit: {PAIRS['beta']:.2f}", JOINT)
        fits = np.array(PAIRS["fits"])
        edges = np.arange(0.6, 1.5001, 0.05)
        counts = np.histogram(fits, bins=edges)[0]
        pile = VGroup(*[Rectangle(width=(Sc.X(0.05) - Sc.X(0.0)) * 0.9, height=1.5 * n / counts.max(), stroke_width=0, fill_color=JOINT, fill_opacity=0.55).move_to([Sc.X(e + 0.025), Sc.y + 0.75 * n / counts.max(), 0]) for e, n in zip(edges[:-1], counts) if n > 0])
        mean = VGroup(Line([Sc.X(PAIRS["average"]), Sc.y, 0], [Sc.X(PAIRS["average"]), Sc.y + 2.0, 0], stroke_width=4, color=JOINT), big(f"{N['reps']} worlds: {PAIRS['average']:.2f} on average", size=22, color=JOINT).move_to([Sc.X(PAIRS["average"]) + 0.4, Sc.y + 2.3, 0]))
        twice = side("twice the truth: not bad luck, and not a bug", size=18, color=PAPER).move_to([0, -2.2, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeOut(ask), FadeIn(fit), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(fit[1]), FadeIn(pile, lag_ratio=0.05), run_time=1.3)
            seg.wait_until(seg.word(1, "The average is"))
            self.play(FadeIn(mean), run_time=0.7)
            seg.wait_until(seg.word(1, "This is not bad luck"))
            self.play(FadeIn(twice), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 18, "Too Many Intercepts", "when one intercept per provider bends the shared rule")


# =================================================================================== S03
class S03_Why(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Where the bias comes from")
        field = pair_field(0.3)
        same = [k for k, (a, b) in enumerate(PAIRS["outcomes"]) if a == b]
        alike = VGroup(big(f"{PAIRS['alike']:,} of {PAIRS['providers']:,}", size=28, color=MUTED), side("both patients, the same outcome", size=16, color=PAPER)).arrange(DOWN, buff=0.08).move_to([-3.2, -2.3, 0])
        mixed = VGroup(big(f"{PAIRS['discordant']}", size=28, color=ACCENT), side("one readmitted, one not", size=16, color=PAPER)).arrange(DOWN, buff=0.08).move_to([3.2, -2.3, 0])
        wall = side("their intercepts run to the wall: nothing to say about the rule", size=16).move_to([0, 2.6, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(field, lag_ratio=0.002), run_time=1.5)
            seg.wait_until(seg.word(0, "both patients had the same outcome") - 1.2)
            self.play(*[field[k].animate.set_opacity(0.2) for k in same], FadeIn(alike), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(wall), run_time=0.7)
            seg.wait_until(seg.e(1) - 0.2)
            self.play(FadeIn(mixed), run_time=0.6)

        ex = PAIRS["examples"][1]                                              # a mixed pair whose readmitted patient has the higher risk factor
        x0, x1, y0, y1 = -5.4, 0.8, -1.9, 1.9
        X = lambda v: x0 + (x1 - x0) * (v + 3.0) / 6.0
        Y = lambda p: y0 + (y1 - y0) * p
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 15, MUTED).move_to([X(v), y0 - 0.28, 0])) for v in (-3, -2, -1, 0, 1, 2, 3)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(pct(v), 15, MUTED).move_to([x0 - 0.45, Y(v), 0])) for v in (0, 0.5, 1.0)],
                      DashedLine([x0, Y(0.5), 0], [x1, Y(0.5), 0], dash_length=0.08, stroke_width=1.5, color=MUTED), side("the risk factor", size=15).move_to([(x0 + x1) / 2, y0 - 0.6, 0]), side("fitted chance of readmission", size=15).move_to([x0, y1 + 0.26, 0], aligned_edge=LEFT))
        curve = ParametricFunction(lambda v: np.array([X(v), Y(prob(ex["gamma"] + PAIRS["beta"] * v)), 0.0]), t_range=[-3, 3, 0.05], color=ACCENT, stroke_width=4).set_z_index(3)
        mid = float(np.mean(ex["x"]))
        people = VGroup()
        for xv, yv, pv in zip(ex["x"], ex["y"], ex["p"]):
            people.add(VGroup(chip(PAPER, bool(yv), 0.16).move_to([X(xv), y0 + 0.3, 0]), DashedLine([X(xv), y0 + 0.5, 0], [X(xv), Y(pv), 0], dash_length=0.06, stroke_width=2, color=PAPER), Dot([X(xv), Y(pv), 0], radius=0.09, color=PAPER).set_z_index(5),
                              txt(pct(pv, 1), 18, PAPER, weight=SEMIBOLD).move_to([X(xv) + (0.62 if xv > mid else -0.62), Y(pv) + 0.05, 0])))
        centre = VGroup(Line([X(mid), y0, 0], [X(mid), Y(0.5), 0], stroke_width=3, color=ACCENT), Dot([X(mid), Y(0.5), 0], radius=0.08, color=ACCENT).set_z_index(5))
        told = VGroup(side("a pair with one readmission", size=17, color=PAPER), side("its own intercept is free to go anywhere", size=16), big("it settles exactly midway", size=22, color=ACCENT), side(f"the two fitted chances: {pct(ex['p'][0], 1)} and {pct(ex['p'][1], 1)}", size=16, color=PAPER),
                      side("they add up to exactly one", size=16, color=ACCENT)).arrange(DOWN, buff=0.16)
        told = fit_width(told, 4.7).move_to([SX - 0.2, 0.3, 0])
        with self.nar("s3_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(axes), *[FadeIn(p[0]) for p in people], FadeIn(told[0]), run_time=1.1)
            seg.wait_until(seg.word(0, "Here the intercept is free"))
            self.play(Create(curve), FadeIn(told[1]), run_time=1.2)
            seg.wait_until(seg.word(0, "and it settles exactly midway"))
            self.play(FadeIn(centre), *[FadeIn(VGroup(p[1], p[2], p[3])) for p in people], FadeIn(VGroup(*told[2:])), run_time=1.0)

        rows = VGroup(*[VGroup(VGroup(chip(PAPER, bool(e["y"][0]), 0.12), chip(PAPER, bool(e["y"][1]), 0.12)).arrange(RIGHT, buff=0.1), txt(f"{pct(e['p'][0], 1)}  +  {pct(e['p'][1], 1)}  =  {pct(sum(e['p']))}", 20, PAPER)).arrange(RIGHT, buff=0.5) for e in PAIRS["examples"]]).arrange(DOWN, buff=0.28)
        rows_g = VGroup(side("three pairs, each fitted by its own intercept", size=16), rows, side("too good: tuned to two patients and nobody else", size=17, color=ACCENT)).arrange(DOWN, buff=0.3).move_to([-3.0, 0.5, 0])
        two = VGroup(VGroup(side("the joint fit", size=17, color=PAPER), big(f"{PAIRS['beta']:.4f}", size=28, color=JOINT)).arrange(RIGHT, buff=0.3), VGroup(side("asking only which of the two", size=17, color=PAPER), big(f"{PAIRS['conditional']:.4f}", size=28, color=COND)).arrange(RIGHT, buff=0.3),
                     VGroup(side("the ratio", size=17, color=PAPER), big("exactly 2", size=28, color=ACCENT)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.3, aligned_edge=RIGHT).move_to([3.4, 0.5, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(rows_g[0]), FadeIn(rows_g[1]), run_time=1.0)
            seg.wait_until(seg.word(0, "The intercept has been tuned"))
            self.play(FadeIn(rows_g[2]), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(two[0]), FadeIn(two[1]), run_time=0.9)
            seg.wait_until(seg.word(1, "For pairs the sum is exact"))
            self.play(FadeIn(two[2]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Sweep(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "How large must a provider be?")
        C = SizeChart()
        frame, pts = C.frame(), C.points("ratio", JOINT)
        regroup = VGroup(side(f"the same {N['patients']:,} patients", size=17, color=PAPER), *[side(f"{SWEEP[str(n)]['providers']:,} providers of {n}", size=16) for n in SIZES]).arrange(DOWN, buff=0.12).move_to([SX, 1.2, 0])
        steep = VGroup(side("too steep by", size=16, color=PAPER), big("  ".join(pct(SWEEP[str(n)]["ratio"] - 1) for n in SIZES[1:]), size=26, color=JOINT)).arrange(DOWN, buff=0.1).move_to([SX, -1.0, 0])
        self.play(FadeIn(tag), FadeIn(frame), FadeIn(pts[0]), run_time=1.1)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(regroup), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[FadeIn(p) for p in pts[1:]], lag_ratio=0.5), FadeIn(steep), run_time=3.0)

        c = N["excess_times_size"]
        law = ParametricFunction(lambda t: np.array([C.X(np.exp(t)), C.Y(min(1 + c / np.exp(t), C.hi)), 0.0]), t_range=[np.log(4.0), np.log(125.0), 0.03], color=JOINT, stroke_width=3).set_stroke(opacity=0.7)
        law_l = VGroup(side("the excess:", size=16, color=PAPER), big(f"about {c:.1f} over the provider's size", size=20, color=JOINT)).arrange(DOWN, buff=0.08).move_to([C.X(20), C.Y(1.55), 0])
        mp = N["more_providers"]
        more = VGroup(side(f"{mp['count']:,} providers of 5 instead of {mp['base']}:", size=16, color=PAPER), big(f"still {pct(mp['ratio'] - 1)} too steep", size=22, color=JOINT), side("more intercepts, and no more information for each", size=15, color=ACCENT)).arrange(DOWN, buff=0.1)
        more = fit_width(more, 4.7).move_to([SX, 0.2, 0])
        with self.nar("s4_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(regroup, steep)), Create(law), FadeIn(law_l), run_time=1.2)
            seg.wait_until(seg.word(0, "It does not shrink"))
            self.play(FadeIn(more[0]), FadeIn(more[1]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(more[2]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_NoWarning(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "No warning")
        y0, y1, lo, hi = -2.2, 2.0, 0.2, 1.6
        Y = lambda v: y0 + (y1 - y0) * (min(max(v, lo), hi) - lo) / (hi - lo)
        cols = {2: (-5.6, -2.4), 5: (-1.6, 1.6), 100: (2.4, 5.6)}
        names = {2: "pairs", 5: "providers of 5", 100: "providers of 100"}
        axis = VGroup(Line([-6.2, y0, 0], [-6.2, y1, 0], stroke_width=3, color=MUTED), *[VGroup(Line([-6.3, Y(v), 0], [-6.2, Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 14, MUTED).move_to([-6.55, Y(v), 0])) for v in (0.25, 0.5, 0.75, 1.0, 1.25, 1.5)],
                      DashedLine([-6.2, Y(TRUE), 0], [5.9, Y(TRUE), 0], dash_length=0.1, stroke_width=2.5, color=TRUTH), side("the truth", size=14, color=TRUTH).move_to([6.35, Y(TRUE), 0]))
        panels = {}
        for n, (a, b) in cols.items():
            ivs = SWEEP[str(n)]["intervals"]
            xs = np.linspace(a + 0.1, b - 0.1, len(ivs))
            bars = VGroup()
            for x, (est, se) in zip(xs, ivs):
                ok = abs(est - TRUE) <= 1.959964 * se
                bars.add(VGroup(Line([x, Y(est - 1.959964 * se), 0], [x, Y(est + 1.959964 * se), 0], stroke_width=2.6, color=GOOD if ok else JOINT), Dot([x, Y(est), 0], radius=0.03, color=PAPER)))
            head = VGroup(txt(names[n], 19, PAPER, weight=SEMIBOLD), side(f"standard error {SWEEP[str(n)]['se']:.2f}", size=15)).arrange(DOWN, buff=0.06).move_to([(a + b) / 2, 2.6, 0])
            foot = VGroup(side("holding the truth", size=15, color=PAPER), big(pct(SWEEP[str(n)]["coverage"]) if SWEEP[str(n)]["coverage"] > 0 else "never", size=24, color=ACCENT)).arrange(RIGHT, buff=0.2).move_to([(a + b) / 2, -2.7, 0])
            panels[n] = VGroup(bars, head, foot)
        note = side("forty 95% intervals at each size, one for each simulated world", size=15).move_to([0, 3.25, 0])
        self.play(FadeIn(tag), FadeIn(axis), run_time=1.0)
        with self.nar("s5_1", gap=0.8) as seg:
            self.play(*[FadeIn(panels[n][1]) for n in cols], FadeIn(note), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(*[FadeIn(panels[n][0], lag_ratio=0.02) for n in cols], run_time=1.6)
            seg.wait_until(seg.word(1, "With providers of 5"))
            self.play(FadeIn(panels[5][2]), FadeIn(panels[100][2]), run_time=0.8)
            seg.wait_until(seg.word(1, "With pairs, never"))
            self.play(FadeIn(panels[2][2]), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Remedy(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "A remedy that deletes the intercepts")
        chips = VGroup(*[chip(PAPER, k in (1, 3), 0.24) for k in range(5)]).arrange(RIGHT, buff=0.28)
        icpt = marker(ACCENT, 0.4)
        prov = VGroup(icpt, chips).arrange(DOWN, buff=0.3).move_to([-2.6, 0.9, 0])
        icpt_l = side("its intercept", size=15, color=ACCENT).next_to(icpt, RIGHT, buff=0.2)
        given = VGroup(side("taken as given:", size=17, color=PAPER), big("two readmissions", size=24)).arrange(DOWN, buff=0.08).move_to([-2.6, -0.6, 0])
        which = VGroup(side("the only question left:", size=17, color=PAPER), big("which two?", size=28, color=ACCENT)).arrange(DOWN, buff=0.08).move_to([-2.6, -1.9, 0])
        cancel = VGroup(Line(icpt.get_corner(DL) + LEFT * 0.12 + DOWN * 0.05, icpt.get_corner(UR) + RIGHT * 0.12 + UP * 0.05, stroke_width=5, color=ALERT), side("it cancels", size=16, color=ALERT).next_to(icpt, LEFT, buff=0.35))
        cox = VGroup(card(4.6, 2.3), VGroup(txt("the same move as the Cox model", 18, PAPER, weight=SEMIBOLD), side("given that someone failed now: who?", size=16, color=PAPER), big("who, not when", size=24, color=ACCENT)).arrange(DOWN, buff=0.16)).move_to([SX - 0.3, 0.2, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(prov), FadeIn(icpt_l), run_time=1.1)
            seg.wait_until(seg.word(0, "take the number of"))
            self.play(FadeIn(given), run_time=0.7)
            seg.wait_until(seg.word(0, "and ask only which"))
            self.play(FadeIn(which), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(Create(cancel[0]), FadeIn(cancel[1]), icpt_l.animate.set_opacity(0.4), run_time=0.9)
            seg.wait_until(seg.word(1, "It is the same move"))
            self.play(FadeIn(cox), run_time=0.9)

        C = SizeChart()
        frame, joint, cond = C.frame(), C.points("ratio", JOINT), C.points("conditional", COND, labels=False)
        flat = Line([C.X(2), C.Y(1.0), 0], [C.X(100), C.Y(1.0), 0], stroke_width=4, color=COND).set_z_index(4)
        key = VGroup(VGroup(Dot(radius=0.09, color=JOINT), side("the joint fit", size=16, color=PAPER)).arrange(RIGHT, buff=0.15), VGroup(Dot(radius=0.09, color=COND), side("the conditional fit", size=16, color=PAPER)).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([SX, 2.2, 0])
        lo, hi = min(SWEEP[str(n)]["conditional"] for n in SIZES), max(SWEEP[str(n)]["conditional"] for n in SIZES)
        right = VGroup(big("within 1% of the truth", size=24, color=COND), side(f"at every size: {lo:.3f} to {hi:.3f}", size=16, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX, 0.8, 0])
        empty = VGroup(side("the intercepts it returns:", size=16, color=PAPER), VGroup(*[DashedVMobject(RoundedRectangle(width=0.5, height=0.5, corner_radius=0.08, stroke_color=MUTED, stroke_width=2), num_dashes=12) for _ in range(5)]).arrange(RIGHT, buff=0.15), big("none: it cannot profile", size=22, color=ALERT)).arrange(DOWN, buff=0.16)
        empty.move_to([SX, -1.2, 0])
        with self.nar("s6_2", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(frame), FadeIn(joint), FadeIn(key[0]), run_time=1.0)
            self.play(Create(flat), FadeIn(cond), FadeIn(key[1]), FadeIn(right), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(empty[0]), FadeIn(empty[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "It returns no intercepts"))
            self.play(FadeIn(empty[2]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Practice(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "In practice")
        x0, x1, ya = -5.8, 5.8, -0.6
        X = lambda n: x0 + (x1 - x0) * (np.log(n) - np.log(2.0)) / (np.log(600.0) - np.log(2.0))
        axis = VGroup(Line([x0, ya, 0], [x1, ya, 0], stroke_width=3, color=MUTED), *[VGroup(Line([X(n), ya, 0], [X(n), ya - 0.1, 0], stroke_width=2, color=MUTED), txt(str(n), 15, MUTED).move_to([X(n), ya - 0.3, 0])) for n in (2, 5, 10, 25, 50, 100, 200, 500)],
                      side("patients in each provider", size=16).move_to([0, ya - 0.7, 0]))

        def mark(n, label, color, up):
            return VGroup(Line([X(n), ya, 0], [X(n), ya + up, 0], stroke_width=4, color=color), big(label, size=20, color=color).move_to([X(n), ya + up + 0.28, 0]))

        m25 = mark(25, f"about {pct(SWEEP['25']['ratio'] - 1)} too steep", JOINT, 1.6)
        m100 = mark(100, f"about {pct(SWEEP['100']['ratio'] - 1)}", JOINT, 1.0)
        cut = PRACTICE["cutoff"]
        aside = VGroup(Rectangle(width=X(cut) - x0, height=0.5, stroke_width=0, fill_color=MUTED, fill_opacity=0.3).move_to([(x0 + X(cut)) / 2, ya + 0.25, 0]), side(f"{cut} patients or fewer: set aside by the software", size=15, color=PAPER).move_to([(x0 + X(cut)) / 2 + 0.6, ya + 0.75, 0]))
        crowd = VGroup(Rectangle(width=X(500) - X(20), height=0.34, stroke_width=0, fill_color=ACCENT, fill_opacity=0.35).move_to([(X(20) + X(500)) / 2, ya - 1.3, 0]),
                       side(f"our crowd, 20 to 500 patients a provider: about {pct(PRACTICE['crowd_ratio'] - 1)} too steep", size=16, color=ACCENT).move_to([(X(20) + X(500)) / 2, ya - 1.75, 0]))
        keep = side("we keep the joint fit, and keep an eye on provider size", size=18, color=PAPER).move_to([0, 2.5, 0])
        self.play(FadeIn(tag), FadeIn(axis), run_time=1.0)
        with self.nar("s7_1") as seg:
            self.play(FadeIn(keep), run_time=0.8)
            seg.wait_until(seg.word(0, "At 25 patients"))
            self.play(FadeIn(m25), run_time=0.7)
            seg.wait_until(seg.word(0, "at 100"))
            self.play(FadeIn(m100), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(aside), run_time=0.8)
            seg.wait_until(seg.word(1, "And in our crowd"))
            self.play(FadeIn(crowd), run_time=0.8)

        note = VGroup(card(8.6, 1.9), VGroup(txt("a property of the method, not of a program", 20, ACCENT, weight=SEMIBOLD), side(f"pprof_py and this episode's own fit, on one world of tens: {PRACTICE['package_beta']:.5f} and {PRACTICE['own_beta']:.5f}", size=16, color=PAPER)).arrange(DOWN, buff=0.18)).move_to([0, 0.2, 0])
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            seg.wait_until(seg.word(0, "This is a property of the method"))
            self.play(FadeIn(note), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(marker(ACCENT, 0.36), VGroup(chip(PAPER, True, 0.13), chip(PAPER, False, 0.13)).arrange(RIGHT, buff=0.12)).arrange(DOWN, buff=0.14)
        ax = VGroup(Line([-0.8, -0.4, 0], [0.9, -0.4, 0], stroke_width=2.5, color=MUTED), DashedLine([-0.8, -0.2, 0], [0.9, -0.2, 0], dash_length=0.06, stroke_width=2, color=TRUTH))
        icon2 = VGroup(ax, VMobject(color=JOINT, stroke_width=4).set_points_smoothly([np.array([-0.75 + 1.6 * t, -0.2 + 0.75 / (1 + 9 * t), 0.0]) for t in np.linspace(0, 1, 20)]))
        icon3 = VGroup(marker(MUTED, 0.36), Line(LEFT * 0.25 + DOWN * 0.25, RIGHT * 0.25 + UP * 0.25, stroke_width=5, color=ALERT)).set_z_index(3)
        icons = [icon1, icon2, icon3]
        caps = [["Each intercept is fitted to its", "own few patients, and", "overfits them a little"], ["The shared rule comes out too", "steep: by a little more than one", "over the provider's size"], ["Conditioning removes the bias,", "and the intercepts with it"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 1.0, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        E15 = json.loads((ROOT.parent / "e15_the_funnel" / "e15_numbers.json").read_text())["differ"]
        F = Funnel(x0=-5.8, x1=0.2, y0=-1.9, y1=2.0, p_lo=1.5, p_hi=350.0, ticks=(5, 20, 50, 100, 200, 300))
        fun = VGroup(F.axes(x_label="precision", y_label="ratio"), F.edges(), *[F.dot(d["precision"], d["ratio"], ACCENT if (d["out"] and not d["planted"]) else PAPER, 0.045, 0.85) for d in E15["dots"]])
        q = VGroup(side(f"Episode 15: {E15['outside']} of 194 outside the funnel", size=17, color=PAPER), big("are they all outliers?", size=26, color=ACCENT)).arrange(DOWN, buff=0.12).move_to([3.8, 1.2, 0])
        nxt = VGroup(txt("Next, the last episode:", 22, MUTED), big("wider than chance", size=34)).arrange(DOWN, buff=0.2).move_to([3.8, -0.9, 0])
        with self.nar("s8_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(fun), run_time=1.1)
            seg.wait_until(seg.word(0, "When a quarter of the providers"))
            self.play(FadeIn(q), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s8_3", 19, "Wider than Chance")
