"""Model in Motion · The Logistic Fixed-Effect Model · Episode 14: Three Shortcuts (when can a faster test replace the exact one?).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode14.py S03_Bell      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e14_numbers.json, written by e14_numbers.py; none is typed here.
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
from mim.piles import Hist, tail_colors  # noqa: E402

N = json.loads((ROOT / "e14_numbers.json").read_text())
CASTD, PMF, AL, P, Z, FLIP, TRAP, CAL, IV = (N[k] for k in ("cast", "pmf", "alder", "p", "z", "flip", "trap", "calibration", "interval"))
REF, BETA, G = N["reference"], N["fit"]["beta"], N["fit"]["gamma"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.55                                           # centre of the side column beside a histogram
NAMES = {"exact": "exact", "bell": "bell curve", "ruler": "ruler", "flip": "flipping"}


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def prob(g):
    return 1.0 / (1.0 + float(np.exp(-g)))


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.1, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def bell_icon(color=PAPER, w=1.6, h=0.9):
    return ParametricFunction(lambda t: np.array([w * t, h * np.exp(-9.0 * t * t), 0.0]), t_range=[-0.5, 0.5, 0.01], color=color, stroke_width=4)


def ruler_icon(color=PAPER, w=1.6):
    return VGroup(Line([-w / 2, 0, 0], [w / 2, 0, 0], stroke_width=3.5, color=color), *[Line([v, -0.13, 0], [v, 0.13, 0], stroke_width=3, color=color) for v in np.linspace(-w / 2, w / 2, 5)])


def flip_icon(color=PAPER):
    return VGroup(*[(Dot(radius=0.08, color=color) if k in (0, 3, 4, 7, 8) else Circle(radius=0.08, stroke_color=color, stroke_width=2)) for k in range(12)]).arrange_in_grid(cols=4, buff=0.14)


def tag(text, color=PAPER):
    t = pill(text, 20)
    t[0].set_stroke(color, width=2.5)
    return t


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        o = CASTD["Alder"]["observed"]
        H = Hist(-5.6, 1.6, -2.2, 1.6, 18, 0.2)
        axis, bars = H.axis(every=2), H.bars(PMF["Alder"], colors=tail_colors(o, 18, ALDER))
        mark = H.marker(o, "Alder's 13", ALDER, H.y0 + H.H(PMF["Alder"][o]))
        exact = VGroup(side("exact, coin by coin", size=19, color=PAPER), big(f"p = {P['exact']['Alder']:.3f}", size=40, color=ACCENT)).arrange(DOWN, buff=0.15).move_to([SX, 0.9, 0])
        work = side("and a fair amount of work", size=18).move_to([SX, -0.2, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(axis), FadeIn(bars), FadeIn(mark), run_time=1.2)
            seg.wait_until(seg.word(0, "and read its p-value"))
            self.play(FadeIn(exact), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(work), run_time=0.6)

        xs = (-4.4, 0.0, 4.4)
        cards = VGroup(*[card(3.6, 2.3).move_to([x, 1.0, 0]) for x in xs])
        icons = VGroup(bell_icon().move_to([xs[0], 1.0, 0]), ruler_icon().move_to([xs[1], 1.0, 0]), flip_icon().move_to([xs[2], 1.0, 0]))
        names = VGroup(*[txt(s, 22, PAPER, weight=SEMIBOLD).move_to([x, -0.5, 0]) for s, x in zip(("a bell curve", "a ruler", "flipping"), xs)])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(axis, bars, mark, exact, work)), run_time=0.6)
            for k, cue in enumerate(("a bell curve", "a ruler", "and brute-force")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(cards[k]), FadeIn(icons[k]), FadeIn(names[k]), run_time=0.6)

        slots = VGroup(*[big("?", size=44, color=MUTED).move_to([x, -1.45, 0]) for x in xs])
        ask = big("which side of 5%?", size=28, color=ACCENT).move_to([0, -2.55, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(LaggedStart(*[FadeIn(s_) for s_ in slots], lag_ratio=0.2), run_time=0.9)
            seg.wait_until(seg.word(0, "Will all three land"))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 14, "Three Shortcuts", "when can a faster test replace the exact one?")


# =================================================================================== S03
class S03_Bell(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(1, "One: a bell curve")
        o, mean, sd = CASTD["Alder"]["observed"], AL["expected"], AL["sd"]
        H = Hist(-5.6, 1.6, -2.2, 1.9, 18, 0.2)
        axis, bars = H.axis(every=2), H.bars(PMF["Alder"], opacity=0.45)
        bell = H.bell(mean, sd)
        top = H.y0 + H.H(H.density(mean, mean, sd))
        centre = VGroup(DashedLine([H.X(mean), H.y0, 0], [H.X(mean), top + 0.1, 0], dash_length=0.08, stroke_width=2.5, color=ACCENT), big(f"{mean:.2f}", size=22, color=ACCENT).move_to([H.X(mean), top + 0.38, 0]))
        ys = H.y0 + H.H(H.density(mean + sd, mean, sd))
        spread = VGroup(DoubleArrow([H.X(mean), ys, 0], [H.X(mean + sd), ys, 0], buff=0, stroke_width=3.5, color=PAPER, tip_length=0.13).set_z_index(6), big(f"{sd:.2f}", size=20, color=PAPER).move_to([H.X(mean + sd / 2), ys + 0.25, 0]).set_z_index(6))
        same = VGroup(side("the same centre", size=18, color=PAPER), side("the same spread", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX, 1.4, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag_), FadeIn(axis), FadeIn(bars), run_time=1.0)
            self.play(Create(bell), FadeIn(same), run_time=1.4)
            seg.wait_until(seg.word(1, "centred on 8.02"))
            self.play(FadeIn(centre), run_time=0.6)
            seg.wait_until(seg.word(1, "with a standard deviation"))
            self.play(FadeIn(spread), run_time=0.6)

        mark = H.marker(o, "Alder's 13", ALDER, H.y0 + H.H(PMF["Alder"][o]))
        mirror = 2 * mean - o
        tails = VGroup(H.bell_area(mean, sd, o, 18.5, opacity=0.95), H.bell_area(mean, sd, -0.5, mirror, opacity=0.95))
        out = VGroup(VGroup(big(f"{AL['above']:.2f}", size=26), side("above the centre", size=17, color=PAPER)).arrange(RIGHT, buff=0.25),
                     VGroup(big(f"{Z['bell']['Alder']:.2f}", size=34, color=ACCENT), side("spreads out", size=17, color=PAPER)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.22).move_to([SX, 0.95, 0])
        both = VGroup(side("the two tails beyond", size=17, color=PAPER), big(pct(P["bell"]["Alder"], 1), size=40, color=ACCENT)).arrange(DOWN, buff=0.1).move_to([SX, -0.75, 0])
        with self.nar("s3_2") as seg:
            self.play(FadeOut(same), FadeIn(mark), FadeIn(out[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "Divide by the spread"))
            self.play(FadeIn(out[1]), run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(tails), FadeIn(both), run_time=0.9)

        formula = MathTex(rf"\frac{{{o} - {mean:.2f}}}{{{sd:.2f}}}", "=", f"{Z['bell']['Alder']:.2f}", font_size=44, color=PAPER)
        formula[2].set_color(ACCENT)
        name = VGroup(tag("the score test"), fit_width(formula, 4.4), fit_width(side("observed minus expected, in standard units", size=16, color=PAPER), 4.5)).arrange(DOWN, buff=0.28).move_to([SX, 0.2, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(out, both)), FadeIn(name[0], scale=0.9), run_time=0.8)
            seg.wait_until(seg.word(0, "It needs just three numbers"))
            self.play(Write(name[1]), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(name[2]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Ruler(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(2, "Two: a ruler on the gamma axis")
        R = Ruler(0.55, -2.5, 0.3, x0=-5.0, x1=4.0, ticks=[-2.5, -2, -1.5, -1, -0.5, 0], labels={v: minus(v, 1) for v in (-2.5, -2, -1.5, -1, -0.5, 0)}, title="log-odds")
        ga, se = G["Alder"], AL["se"]
        ref = VGroup(Line(R.P(REF, -0.02), R.P(REF, 1.0), stroke_width=4, color=CEDAR), VGroup(txt("the reference", 18, CEDAR, weight=SEMIBOLD), big(minus(REF), size=22, color=CEDAR)).arrange(DOWN, buff=0.06).move_to(R.P(REF, 1.5)))
        alder = VGroup(Dot(R.P(ga), radius=0.14, color=ALDER).set_z_index(5), VGroup(txt("Alder", 18, ALDER, weight=SEMIBOLD), big(minus(ga), size=22, color=ALDER)).arrange(DOWN, buff=0.06).move_to(R.P(ga, 1.5)))
        gap = VGroup(DoubleArrow(R.P(REF, 0.55), R.P(ga, 0.55), buff=0, stroke_width=4, color=PAPER, tip_length=0.15), big(f"{AL['gap']:.2f}", size=26, color=PAPER).move_to(R.P((REF + ga) / 2, 0.85)))
        whisk = VGroup(Line(R.P(ga - se), R.P(ga + se), stroke_width=7, color=ALDER), *[Line(R.P(v, -0.14), R.P(v, 0.14), stroke_width=4, color=ALDER) for v in (ga - se, ga + se)]).set_z_index(4)
        whisk_l = VGroup(side("its standard error, from Episode 9", size=16, color=PAPER), big(f"{se:.2f}", size=24, color=ALDER)).arrange(RIGHT, buff=0.25).move_to(R.P(ga, -1.0) + RIGHT * 0.9)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag_), FadeIn(R.g), FadeIn(ref), FadeIn(alder), run_time=1.3)
            seg.wait_until(seg.word(1, "sits 0.87 above"))
            self.play(GrowFromCenter(gap[0]), FadeIn(gap[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "a standard error of"))
            self.play(Create(whisk), FadeIn(whisk_l), run_time=0.9)

        steps = VGroup(*[VGroup(Line(R.P(REF + k * se, -0.95), R.P(REF + (k + 1) * se, -0.95), stroke_width=6, color=ACCENT if k % 2 == 0 else PAPER),
                                txt(str(k + 1), 18, ACCENT if k % 2 == 0 else PAPER, weight=SEMIBOLD).move_to(R.P(REF + (k + 0.5) * se, -1.25))) for k in range(2)],
                       side("standard errors, counted off from the reference", size=15).move_to(R.P(REF, -1.25) + LEFT * 2.45))
        division = MathTex(rf"{AL['gap']:.2f} \div {se:.2f}", "=", f"{Z['ruler']['Alder']:.2f}", font_size=40, color=PAPER)
        division[2].set_color(ACCENT)
        result = VGroup(VGroup(division, side("standard errors", size=17, color=PAPER)).arrange(RIGHT, buff=0.3), VGroup(side("p-value", size=18, color=PAPER), big(pct(P["ruler"]["Alder"], 1), size=36, color=ACCENT)).arrange(RIGHT, buff=0.3),
                        tag("the Wald test")).arrange(RIGHT, buff=0.8).move_to([0, -2.25, 0])
        result = fit_width(result, 12.4).move_to([0, -2.25, 0])
        with self.nar("s4_2", gap=0.8) as seg:
            self.play(FadeOut(whisk_l), LaggedStart(*[FadeIn(s_) for s_ in steps], lag_ratio=0.4), run_time=1.0)
            self.play(FadeIn(result[0]), run_time=0.7)
            seg.wait_until(seg.word(0, "and a p-value of"))
            self.play(FadeIn(result[1]), run_time=0.6)
            seg.wait_until(seg.word(0, "That is the Wald test"))
            self.play(FadeIn(result[2], scale=0.9), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Flip(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(3, "Three: just flip")
        o = CASTD["Alder"]["observed"]
        ps = [prob(REF)] * CASTD["Alder"]["low"] + [prob(REF + BETA)] * CASTD["Alder"]["high"]
        row = VGroup(*[risk_chip(p, r=0.125, color=ALDER).move_to([-5.45 + 0.3 * k, 2.55, 0]) for k, p in enumerate(ps)])
        H = Hist(-5.6, 1.6, -2.2, 1.35, 18, 0.2)
        axis = H.axis(every=2)
        exact = H.bars(PMF["Alder"], color=PAPER, outline=True).set_z_index(4)
        freq = {n: np.array(FLIP["stages"][str(n)]) / n for n in (100, 1000, FLIP["draws"])}
        bars = H.bars(freq[100], color=ALDER, opacity=0.85)
        counter = side("100 rounds", size=19, color=PAPER).move_to([SX, 1.75, 0])
        legend = VGroup(VGroup(Rectangle(width=0.3, height=0.2, stroke_width=0, fill_color=ALDER, fill_opacity=0.85), side("flipped", size=15, color=PAPER)).arrange(RIGHT, buff=0.12),
                        VGroup(Rectangle(width=0.3, height=0.2, stroke_color=PAPER, stroke_width=2), side("exact", size=15, color=PAPER)).arrange(RIGHT, buff=0.12)).arrange(RIGHT, buff=0.5).move_to([SX, 1.2, 0])
        mark = H.marker(o, "13", ALDER, H.y0 + H.H(0.035))
        pval = VGroup(side("this run's p-value", size=18, color=PAPER), big(pct(P["flip"], 1), size=44, color=ACCENT)).arrange(DOWN, buff=0.1).move_to([SX, 0.05, 0])
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag_), FadeIn(row), FadeIn(axis), FadeIn(exact), FadeIn(legend), run_time=1.3)
            seg.wait_until(seg.word(0, "Flip Alder's thirty coins"))
            self.play(FadeIn(bars), FadeIn(counter), run_time=0.7)
            for n, lab in ((1000, "1,000 rounds"), (FLIP["draws"], f"{FLIP['draws']:,} rounds")):
                self.play(Transform(bars, H.bars(freq[n], color=ALDER, opacity=0.85)), Transform(counter, side(lab, size=19, color=PAPER).move_to([SX, 1.75, 0])), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(mark), FadeIn(pval), run_time=0.8)

        floor = VGroup(side("nothing rarer than", size=17, color=PAPER), big(f"1 in {FLIP['draws']:,}", size=26, color=PAPER), side("can be reported", size=17, color=PAPER)).arrange(DOWN, buff=0.08).move_to([SX, -1.2, 0])
        boot = tag("the software calls it a bootstrap")
        boot = fit_width(boot, 4.5).move_to([SX, -2.35, 0])
        with self.nar("s5_2", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "But with ten thousand rounds"))
            self.play(FadeIn(floor), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(boot, scale=0.9), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Board(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(4, "The scoreboard")
        cx = {"exact": -2.3, "bell": 0.5, "ruler": 3.1, "flip": 5.6}
        heads = VGroup(*[txt(NAMES[k], 20, PAPER, weight=SEMIBOLD).move_to([cx[k], 2.45, 0]) for k in cx])
        row_l = VGroup(txt("Alder", 22, ALDER, weight=SEMIBOLD), side("p-value", size=16)).arrange(RIGHT, buff=0.2).move_to([-6.3, 1.7, 0], aligned_edge=LEFT)
        pv = {"exact": P["exact"]["Alder"], "bell": P["bell"]["Alder"], "ruler": P["ruler"]["Alder"], "flip": P["flip"]}
        cells = {k: big(pct(pv[k], 1), size=34, color=ACCENT).move_to([cx[k], 1.7, 0]) for k in cx}
        under = side("all below 5%: Alder is flagged, four times over", size=19, color=PAPER).move_to([0.6, 1.0, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag_), FadeIn(heads), FadeIn(row_l), run_time=1.0)
            for k, cue in (("exact", "3.5% exact"), ("bell", "2.5% by the bell curve"), ("ruler", "4.4% by the ruler"), ("flip", "3.8% by flipping")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(cells[k], scale=0.9), run_time=0.45)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(under), run_time=0.7)

        unit = side("distance from the reference, in standard units", size=17).move_to([0.4, 0.25, 0])
        ys = {n: -0.45 - 0.62 * k for k, n in enumerate(("Alder", "Birch", "Dune", "Elm"))}
        table = {}
        for n, y in ys.items():
            table[n] = VGroup(txt(n, 21, COL[n], weight=SEMIBOLD).move_to([-6.3, y, 0], aligned_edge=LEFT), *[big(minus(Z[k][n]), size=26, color=PAPER).move_to([cx[k], y, 0]) for k in ("exact", "bell", "ruler")])
        wrong = box_around(table["Elm"][3], ALERT)
        why = side("measured from a gamma that does not exist", size=17, color=ALERT).move_to([cx["ruler"] + 0.4, ys["Elm"] - 0.55, 0])
        with self.nar("s6_2", gap=0.8) as seg:
            self.play(FadeIn(unit), *[FadeIn(table[n]) for n in ("Alder", "Birch", "Dune")], run_time=1.0)
            self.play(FadeIn(table["Elm"]), run_time=0.6)
            seg.wait_until(seg.word(1, "The ruler says only"))
            self.play(Create(wrong), run_time=0.7)
            seg.wait_until(seg.word(1, "It is measuring"))
            self.play(FadeIn(why), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Fail(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(5, "Where they fail")

        def se_row(label, se, z, color, y):
            f = MathTex(rf"{AL['gap']:.2f} \div {se}", "=", z, font_size=40, color=PAPER)
            f[2].set_color(color)
            return VGroup(VGroup(*[side(s, size=18, color=PAPER) for s in label]).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([-6.2, y, 0], aligned_edge=LEFT), big(se, size=34, color=color).move_to([0.6, y, 0]), f.move_to([4.1, y, 0]))

        heads = VGroup(side("which standard error?", size=20, color=ACCENT).move_to([-6.2, 2.3, 0], aligned_edge=LEFT), side("standard error", 0.6, 2.3, 16), side("the ruler's reading", 4.1, 2.3, 16))
        bad = se_row(["the textbook one, with the risk factor", f"recorded {TRAP['shift']} units higher"], f"{TRAP['se']:.0f}", f"{TRAP['z']:.2f}", ALERT, 1.2)
        good = se_row(["taken at the average case mix,", "however the factor is recorded"], f"{AL['se']:.2f}", f"{TRAP['z_case_mix']:.2f}", GOOD, -0.2)
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag_), FadeIn(heads), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(bad[0]), run_time=0.7)
            seg.wait_until(seg.word(1, "becomes 38"))
            self.play(FadeIn(bad[1]), run_time=0.5)
            seg.wait_until(seg.word(1, "The test collapses"))
            self.play(FadeIn(bad[2]), run_time=0.6)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(good), run_time=0.9)

        e = CASTD["Elm"]
        x0, x1, y0, y1, lo, hi, p_max = -5.2, 1.6, -2.1, 1.7, -3.5, 8.5, 0.34
        step = (x1 - x0) / (hi - lo)
        X = lambda v: x0 + step * (v - lo)
        Hh = lambda p: (y1 - y0) * p / p_max
        dens = lambda v: Hist.density(v, e["expected"], e["sd"])
        axis = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), *[txt(str(k).replace("-", "\u2212"), 15, MUTED if k >= 0 else ALERT).move_to([X(k), y0 - 0.25, 0]) for k in range(-3, 9)],
                      side("readmissions", size=16).move_to([(x0 + x1) / 2, y0 - 0.58, 0]))
        bars = VGroup(*[Rectangle(width=step * 0.8, height=max(Hh(PMF["Elm"][k]), 0.004), stroke_width=0, fill_color=ELM, fill_opacity=0.6).move_to([X(k), y0 + max(Hh(PMF["Elm"][k]), 0.004) / 2, 0]) for k in range(0, 9)])
        bell = ParametricFunction(lambda v: np.array([X(v), y0 + Hh(dens(v)), 0.0]), t_range=[lo, hi, 0.05], color=ACCENT, stroke_width=4).set_z_index(5)
        spill = Polygon(*[np.array([X(v), y0 + Hh(dens(v)), 0.0]) for v in np.linspace(lo, 0.0, 30)], np.array([X(0.0), y0, 0.0]), np.array([X(lo), y0, 0.0]), stroke_width=0, fill_color=ALERT, fill_opacity=0.6).set_z_index(4)
        zero = DashedLine([X(0.0), y0, 0], [X(0.0), y1, 0], dash_length=0.08, stroke_width=2, color=MUTED)
        notes = VGroup(VGroup(txt("Elm", 24, ELM, weight=SEMIBOLD), side(f"expects {e['expected']:.2f} readmissions", size=18, color=PAPER)).arrange(RIGHT, buff=0.25),
                       VGroup(big(pct(N["elm"]["below_zero"]), size=40, color=ALERT), side("of the bell curve lies below zero", size=17, color=PAPER)).arrange(DOWN, buff=0.1)).arrange(DOWN, buff=0.6)
        notes = fit_width(notes, 4.5).move_to([SX, 0.2, 0])
        with self.nar("s7_2") as seg:
            self.play(FadeOut(VGroup(heads, bad, good)), run_time=0.6)
            self.play(FadeIn(axis), FadeIn(bars), FadeIn(notes[0]), run_time=1.0)
            seg.wait_until(seg.word(0, "and a bell curve centred"))
            self.play(Create(bell), FadeIn(zero), run_time=1.0)
            self.play(FadeIn(spill), FadeIn(notes[1]), run_time=0.8)

        U, bx = 1.25, -2.6
        rows = VGroup()
        for k, (key, y) in enumerate((("exact", 1.2), ("bell", 0.3), ("ruler", -0.6))):
            v = CAL["small_rate"][key]
            b = Rectangle(width=U * 100 * v, height=0.42, stroke_width=0, fill_color=PAPER if key != "ruler" else ALERT, fill_opacity=0.9).move_to([bx + U * 100 * v / 2, y, 0])
            rows.add(VGroup(txt(NAMES[key], 20, PAPER, weight=SEMIBOLD).next_to(b, LEFT, buff=0.3), b, big(pct(v, 1), size=28, color=PAPER if key != "ruler" else ALERT).move_to([bx + U * 5 + 0.95, y, 0])))
        five = VGroup(DashedLine([bx + U * 5, 1.75, 0], [bx + U * 5, -1.15, 0], dash_length=0.1, stroke_width=2.5, color=ACCENT), side("the 5% promised", size=16, color=ACCENT).move_to([bx + U * 5, 2.05, 0]))
        who = VGroup(side(f"{CAL['small_tests']:,} providers with fewer than 50 patients,", size=18, color=PAPER), side("every one truly equal to the reference: how many are flagged?", size=18, color=PAPER)).arrange(DOWN, buff=0.08).move_to([0, -2.0, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(axis, bars, bell, spill, zero, notes)), run_time=0.6)
            self.play(FadeIn(who), FadeIn(five), run_time=0.9)
            for k, cue in enumerate(("the exact test flags", "the bell curve 4.9%", "and the ruler only")):
                seg.wait_until(seg.word(0, cue))
                self.play(GrowFromEdge(rows[k][1], LEFT), FadeIn(rows[k][0]), FadeIn(rows[k][2]), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Choose(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(6, "Which one, when")
        AX = lambda r: -3.4 + 2.9 * r
        y_ax = -1.7
        axis = VGroup(Line([AX(0), y_ax, 0], [AX(2.5), y_ax, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([AX(v), y_ax, 0], [AX(v), y_ax - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([AX(v), y_ax - 0.3, 0])) for v in (0, 0.5, 1, 1.5, 2, 2.5)],
                      side("Alder's ratio: observed, over expected at the reference", size=16).move_to([AX(1.25), y_ax - 0.64, 0]))
        one = VGroup(DashedLine([AX(1), y_ax, 0], [AX(1), 1.9, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), txt("the reference", 16, CEDAR, weight=SEMIBOLD).move_to([AX(1), 2.15, 0]))
        rows = {}
        for k, key in enumerate(("exact", "bell", "ruler")):
            y, (a, b) = 1.25 - 0.95 * k, IV[key]
            bar = VGroup(Line([AX(a), y, 0], [AX(b), y, 0], stroke_width=6, color=ALDER), *[Line([AX(v), y - 0.13, 0], [AX(v), y + 0.13, 0], stroke_width=4, color=ALDER) for v in (a, b)], Dot([AX(N["ratio"]), y, 0], radius=0.11, color=PAPER).set_z_index(5))
            rows[key] = VGroup(txt(NAMES[key], 20, PAPER, weight=SEMIBOLD).move_to([-6.2, y, 0], aligned_edge=LEFT), bar, big(f"{a:.2f} to {b:.2f}", size=24, color=ALDER).move_to([5.4, y, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag_), FadeIn(axis), FadeIn(one), run_time=1.1)
            for key, cue in (("exact", "1.04 to 2.26"), ("bell", "1.07 to 2.25"), ("ruler", "1.02 to 2.31")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(rows[key]), run_time=0.6)

        uses = [("exact", "the exact test", ["for flags:", "the software's default"], None), ("bell", "the bell curve", ["when you need a formula:", "smooth limits, next time"], bell_icon(w=1.0, h=0.5)),
                ("ruler", "the ruler", ["for anything built", "on gamma itself"], ruler_icon(w=1.0)), ("flip", "flipping", ["as a check", "on the others"], flip_icon().scale(0.6))]
        cards = VGroup()
        for k, (key, name, lines, icon) in enumerate(uses):
            c = card(3.0, 3.3).move_to([-4.8 + 3.2 * k, 0.1, 0])
            pic = icon if icon is not None else Hist(-0.6, 0.6, 0.0, 0.5, 12, 0.3).bars(N["pmf"]["Dune"])
            cards.add(VGroup(c, pic.move_to(c.get_center() + UP * 0.95), txt(name, 20, ACCENT, weight=SEMIBOLD).move_to(c.get_center() + UP * 0.1), VGroup(*[txt(s, 17, PAPER) for s in lines]).arrange(DOWN, buff=0.08).move_to(c.get_center() + DOWN * 0.8)))
        cards = VGroup(*[VGroup(c[0], c[1], c[2], fit_width(c[3], 2.7)) for c in cards])
        with self.nar("s8_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(axis, one, *rows.values())), run_time=0.6)
            for k, (s_, cue) in enumerate(((0, "The exact test for flags"), (1, None), (2, None), (2, "And flipping"))):
                seg.wait_until(seg.word(s_, cue) if cue else seg.s(s_))
                self.play(FadeIn(cards[k], shift=UP * 0.1), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag_ = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        m = Hist(-0.9, 0.9, 0.0, 0.8, 18, 0.2)
        icon1 = VGroup(m.bars(PMF["Alder"], opacity=0.45), m.bell(AL["expected"], AL["sd"], width=3))
        gap = VGroup(ruler_icon(w=1.8), Dot([-0.45, 0, 0], radius=0.08, color=CEDAR), Dot([0.45, 0, 0], radius=0.08, color=ALDER), DoubleArrow([-0.45, 0.3, 0], [0.45, 0.3, 0], buff=0, stroke_width=3, color=ACCENT, tip_length=0.1))
        icons = [icon1, gap, flip_icon()]
        caps = [["The bell curve: a normal curve", "with the pile's centre and spread"], ["The ruler: the gap between", "sliders, in standard errors"], ["Flipping: the pile rebuilt by", "brute force. On small clinics", "the three can part ways"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.95, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag_), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        five = VGroup(*[VGroup(Dot(radius=0.16, color=COL[n]), txt("flagged" if N["p"]["exact"][n] < 0.05 else "not", 13, ALERT if N["p"]["exact"][n] < 0.05 else MUTED)).arrange(DOWN, buff=0.1) for n in ORDER]).arrange(RIGHT, buff=0.35).move_to([-4.2, 0.9, 0])
        five_l = side("five verdicts", size=18, color=PAPER).next_to(five, DOWN, buff=0.25)
        many = VGroup(*[Dot(radius=0.045, color=PAPER).set_opacity(0.75) for _ in range(200)]).arrange_in_grid(cols=20, buff=0.1).move_to([0.9, 0.6, 0])
        many_l = side("two hundred? seven thousand?", size=18, color=ACCENT).next_to(many, DOWN, buff=0.25)
        nxt = VGroup(txt("Next:", 26, MUTED), big("the funnel", size=34)).arrange(DOWN, buff=0.2).move_to([5.1, 0.6, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(five), FadeIn(five_l), run_time=0.9)
            seg.wait_until(seg.word(0, "What about two hundred"))
            self.play(FadeIn(many, lag_ratio=0.01), FadeIn(many_l), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_3", 15, "The Funnel")
