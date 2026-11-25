"""Model in Motion · The Logistic Fixed-Effect Model · Episode 16: Trusting the Risk Model (the same meter, on new groups).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode16.py S04_Wrong      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e16_numbers.json, written by e16_numbers.py; none is typed here. The meters are the series'
own (mim.meters.Meter): observed on the left, going down when it is the larger.
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
from mim.meters import Meter  # noqa: E402

N = json.loads((ROOT / "e16_numbers.json").read_text())
TENTHS, BEND, COST, AUC, SLOPE = (N[k] for k in ("tenths", "bend", "cost", "auc", "slope"))
SX = 4.4                                            # centre of the side column
TILT = 6.0                                          # meter tilt per unit of (ratio - 1); the angle saturates, the number below carries the value


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def prob(v):
    return 1.0 / (1.0 + float(np.exp(-v)))


def box_around(m, color=PAPER, buff=0.1):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def tiny_meter(color=PAPER, w=0.2):
    """A provider's meter at thumbnail size: a level beam on its pivot."""
    return VGroup(Triangle(fill_color=MUTED, fill_opacity=1, stroke_width=0).scale(0.035), Line(LEFT * w / 2, RIGHT * w / 2, stroke_width=2.5, color=color).shift(UP * 0.055))


def meter_grid(cx, cy=0.25):
    return VGroup(*[tiny_meter() for _ in range(N["providers"])]).arrange_in_grid(cols=20, buff=(0.1, 0.15)).move_to([cx, cy, 0])


XS = [-5.4 + 1.2 * k for k in range(10)]            # where the ten tenths sit, lowest risk on the left


def strip():
    parts = VGroup(*[Rectangle(width=1.14, height=0.28, stroke_width=0, fill_color=ACCENT, fill_opacity=0.14 + 0.085 * k).move_to([XS[k], 2.35, 0]) for k in range(10)])
    return VGroup(parts, side("lowest risk", size=15).move_to([XS[0], 2.75, 0]), side("highest risk", size=15).move_to([XS[9], 2.75, 0]),
                  side(f"all {N['patients']:,} patients, in order of the risk the model gives them", size=16, color=PAPER).move_to([0, 2.75, 0]))


def tenth_meters(tenths, y=1.3, level=False):
    """Ten meters, one for each tenth of predicted risk, each with its observed-over-expected ratio below."""
    meters, labels = VGroup(), VGroup()
    for k, t in enumerate(tenths):
        off = (not level) and abs(t["z"]) > 1.96
        m = Meter(ALERT if off else PAPER, width=0.8)
        m.move_to([XS[k], y, 0])
        m.tilt_to(0.0 if level else TILT * (t["ratio"] - 1.0))
        meters.add(m)
        labels.add(txt(f"{t['ratio']:.2f}", 18, ALERT if off else PAPER, weight=MEDIUM).move_to([XS[k], y - 0.62, 0]))
    return meters, labels


def calibration(tenths, x0=-5.7, x1=-2.4, y0=-2.45, y1=0.15, vmax=2200.0):
    """Observed against expected for the ten groups, around the line where they are equal."""
    X = lambda v: x0 + (x1 - x0) * v / vmax
    Y = lambda v: y0 + (y1 - y0) * v / vmax
    frame = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED), DashedLine([x0, y0, 0], [x1, y1, 0], dash_length=0.08, stroke_width=2, color=MUTED),
                   side("expected", size=14).move_to([(x0 + x1) / 2, y0 - 0.22, 0]), side("observed", size=14).rotate(PI / 2).move_to([x0 - 0.22, (y0 + y1) / 2, 0]))
    dots = VGroup(*[Dot([X(t["E"]), Y(min(t["O"], vmax)), 0], radius=0.07, color=ALERT if abs(t["z"]) > 1.96 else PAPER).set_z_index(4) for t in tenths])
    return frame, dots


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        a, b = meter_grid(-3.45), meter_grid(3.45)
        a_l = VGroup(txt("our crowd", 22, PAPER, weight=SEMIBOLD), side(f"{N['providers']} providers, a meter for each", size=16)).arrange(DOWN, buff=0.08).next_to(a, UP, buff=0.3)
        b_l = VGroup(txt("a second crowd", 22, PAPER, weight=SEMIBOLD), side("fitted the same way", size=16)).arrange(DOWN, buff=0.08).next_to(b, UP, buff=0.3)
        zero = lambda g: side("observed minus expected: zero, for every one", size=16, color=PAPER).next_to(g, DOWN, buff=0.25)
        za, zb = zero(a), zero(b)
        with self.nar("s1_1") as seg:
            seg.wait_until(seg.s(1))
            self.play(FadeIn(a, lag_ratio=0.003), FadeIn(a_l), run_time=1.5)
            seg.wait_until(seg.word(1, "Every meter is level"))
            self.play(FadeIn(za), run_time=0.7)

        ask = big("one of these two models is badly wrong", size=26, color=ACCENT).move_to([0, -2.6, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeIn(b, lag_ratio=0.003), FadeIn(b_l), run_time=1.5)
            seg.wait_until(seg.word(0, "Its two hundred meters"))
            self.play(FadeIn(zb), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.8)

        why = VGroup(big("level by construction", size=30, color=ACCENT), side("a check that every model passes is no check", size=20, color=PAPER)).arrange(DOWN, buff=0.15).move_to([0, -2.3, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(ask, za, zb)), FadeIn(why[0], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(why[1]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 16, "Trusting the Risk Model", "the same meter, on new groups")


# =================================================================================== S03
class S03_Tenths(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Cut by risk")
        st = strip()
        level, _ = tenth_meters(TENTHS["as_is"], level=True)
        each = side(f"ten groups of about {N['tenth_size']:,} patients, each with a meter of its own", size=16).move_to([0, 0.45, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.word(0, "Line up all"))
            self.play(FadeIn(st[3]), FadeIn(st[0], lag_ratio=0.05), FadeIn(st[1]), FadeIn(st[2]), run_time=1.5)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[FadeIn(m) for m in level], lag_ratio=0.06), FadeIn(each), run_time=1.4)

        meters, labels = tenth_meters(TENTHS["as_is"])
        frame, dots = calibration(TENTHS["as_is"])
        lo, hi = min(t["ratio"] for t in TENTHS["as_is"]), max(t["ratio"] for t in TENTHS["as_is"])
        verdict = VGroup(side("observed over expected, across the ten", size=17, color=PAPER), big(f"{lo:.2f} to {hi:.2f}", size=40, color=ACCENT), side("each within what luck allows", size=17, color=PAPER), pill("this model passes", 20)).arrange(DOWN, buff=0.16).move_to([2.6, -1.1, 0])
        with self.nar("s3_2", gap=0.8) as seg:
            self.play(FadeOut(each), Transform(level, meters), FadeIn(labels), run_time=1.2)
            self.play(FadeIn(frame), FadeIn(dots), FadeIn(verdict[0]), FadeIn(verdict[1]), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(verdict[2]), run_time=0.6)
            seg.wait_until(seg.word(1, "This model passes"))
            self.play(FadeIn(verdict[3], scale=0.9), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Wrong(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "A model that is wrong")
        st = strip()
        meters, labels = tenth_meters(TENTHS["line"])
        frame, dots = calibration(TENTHS["line"])
        first = TENTHS["line"][0]
        mid = [t["ratio"] for t in TENTHS["line"][4:7]]
        worst = VGroup(side("the lowest-risk tenth", size=17, color=PAPER), VGroup(big(f"{first['O']:.0f}", size=36, color=ALERT), side("observed, against", size=17, color=PAPER), big(f"{first['E']:.0f}", size=36, color=PAPER), side("expected", size=17, color=PAPER)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.12).move_to([2.7, -0.75, 0])
        middle = VGroup(side("the middle tenths", size=17, color=PAPER), big(f"{min(mid):.2f} to {max(mid):.2f}", size=28, color=ALERT), side("more than a fifth fewer than expected", size=16)).arrange(DOWN, buff=0.1).move_to([2.7, -2.1, 0])
        self.play(FadeIn(tag), FadeIn(st), run_time=1.0)
        with self.nar("s4_1") as seg:
            self.play(LaggedStart(*[FadeIn(m) for m in meters], lag_ratio=0.05), FadeIn(labels), FadeIn(frame), FadeIn(dots), run_time=1.5)
            seg.wait_until(seg.word(0, "the model expected"))
            self.play(Create(box_around(VGroup(meters[0], labels[0]), ALERT)), FadeIn(worst), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(middle), run_time=0.8)

        x0, x1, y0, y1, v_lo, v_hi = -5.2, 1.4, -2.3, 2.2, -3.2, 5.2
        X = lambda v: x0 + (x1 - x0) * (v + 3.0) / 6.0
        Y = lambda v: y0 + (y1 - y0) * (v - v_lo) / (v_hi - v_lo)
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 15, MUTED).move_to([X(v), y0 - 0.28, 0])) for v in (-3, -2, -1, 0, 1, 2, 3)],
                      side("the first risk factor", size=16).move_to([(x0 + x1) / 2, y0 - 0.6, 0]), side("log-odds of readmission", size=16).move_to([x0 + 1.2, y1 + 0.24, 0]))
        curve = VMobject(color=ACCENT, stroke_width=4.5).set_points_smoothly([np.array([X(g), Y(v), 0.0]) for g, v in zip(BEND["grid"], BEND["true"])]).set_z_index(4)
        line = Line([X(BEND["grid"][0]), Y(BEND["line"][0]), 0], [X(BEND["grid"][-1]), Y(BEND["line"][-1]), 0], stroke_width=4, color=PAPER).set_z_index(3)
        gap = VGroup(*[DoubleArrow([X(g), Y(l) + 0.05, 0], [X(g), Y(t) - 0.05, 0], buff=0, stroke_width=3, color=ALERT, tip_length=0.12) for g, l, t in ((BEND["grid"][2], BEND["line"][2], BEND["true"][2]), (BEND["grid"][-3], BEND["line"][-3], BEND["true"][-3]))])
        names = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4.5, color=ACCENT), side("the truth: it bends", size=18, color=PAPER)).arrange(RIGHT, buff=0.2), VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4, color=PAPER), side("the model: a straight line", size=18, color=PAPER)).arrange(RIGHT, buff=0.2),
                       side("at either extreme, more risk than the line allows", size=16, color=ALERT)).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        names = fit_width(names, 4.6).move_to([SX, 0.4, 0])
        with self.nar("s4_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(axes), Create(curve), FadeIn(names[0]), run_time=1.5)
            seg.wait_until(seg.word(0, "patients at either extreme"))
            self.play(FadeIn(gap), FadeIn(names[2]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(Create(line), FadeIn(names[1]), run_time=0.9)

        st2 = strip()
        fixed, fixed_l = tenth_meters(TENTHS["bend"])
        frame2, dots2 = calibration(TENTHS["bend"])
        lo, hi = min(t["ratio"] for t in TENTHS["bend"]), max(t["ratio"] for t in TENTHS["bend"])
        settle = VGroup(side("with a squared term in the model", size=17, color=PAPER), big(f"{lo:.2f} to {hi:.2f}", size=40, color=ACCENT), side(f"the fitted bend: {BEND['beta_bend'][2]:.2f}, against a true {BEND['extra']}", size=15)).arrange(DOWN, buff=0.16).move_to([2.6, -1.2, 0])
        with self.nar("s4_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(axes, curve, line, gap, names)), run_time=0.6)
            self.play(FadeIn(st2), FadeIn(fixed), FadeIn(fixed_l), FadeIn(frame2), FadeIn(dots2), run_time=1.2)
            seg.wait_until(seg.word(0, "and the ten meters settle"))
            self.play(FadeIn(settle), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Cost(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "What it cost")
        x0, x1, y0, y1, v_hi = -5.3, 0.9, -2.2, 2.3, 3.2
        X = lambda v: x0 + (x1 - x0) * v / v_hi
        Y = lambda v: y0 + (y1 - y0) * v / v_hi
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED), DashedLine([x0, y0, 0], [x1, y1, 0], dash_length=0.1, stroke_width=2, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 15, MUTED).move_to([X(v), y0 - 0.28, 0])) for v in (1, 2, 3)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(str(v), 15, MUTED).move_to([x0 - 0.32, Y(v), 0])) for v in (1, 2, 3)],
                      side("a provider's ratio, corrected model", size=16).move_to([(x0 + x1) / 2, y0 - 0.6, 0]), side("its ratio, wrong model", size=16).move_to([x0 + 1.2, y1 + 0.24, 0]))
        pts = list(zip(COST["ratio_bend"], COST["ratio_line"], COST["unusual"], COST["flip"]))
        dots = VGroup(*[Dot([X(a), Y(b), 0], radius=0.06 if u else 0.045, color=ACCENT if u else PAPER).set_opacity(1.0 if u else 0.55) for a, b, u, f in pts])
        rings = VGroup(*[Circle(radius=0.14, stroke_color=ALERT, stroke_width=2.5).move_to([X(a), Y(b), 0]) for a, b, u, f in pts if f]).set_z_index(5)
        flags = VGroup(big(f"{COST['changed']} of {N['providers']}", size=36, color=ALERT), side("providers change their flag", size=17, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX, 1.3, 0])
        blamed = VGroup(VGroup(Dot(radius=0.08, color=ACCENT), side("the fifth with the most unusual case mix", size=16, color=PAPER)).arrange(RIGHT, buff=0.15), big(f"ratios {pct(COST['excess'] - 1)} too high", size=28, color=ACCENT),
                        side("blamed for the model's mistake", size=17, color=PAPER)).arrange(DOWN, buff=0.14)
        blamed = fit_width(blamed, 4.7).move_to([SX, -0.7, 0])
        with self.nar("s5_1", gap=0.8) as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(dots, lag_ratio=0.004), run_time=1.6)
            seg.wait_until(seg.word(0, "16 of the 200"))
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.06), FadeIn(flags), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(blamed[0]), FadeIn(blamed[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "They were being blamed"))
            self.play(FadeIn(blamed[2]), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_AUC(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "What the AUC saw")
        pairs = AUC["pairs"]

        def pair(k, y):
            (a, b), ok = pairs[k], pairs[k][0] > pairs[k][1]
            left = VGroup(chip(PAPER, True, 0.14), risk_chip(a, r=0.24, color=PAPER), txt(pct(a), 18, PAPER)).arrange(RIGHT, buff=0.2)
            right = VGroup(chip(PAPER, False, 0.14), risk_chip(b, r=0.24, color=PAPER), txt(pct(b), 18, PAPER)).arrange(RIGHT, buff=0.2)
            mark = tick_mark(s=0.9) if ok else VGroup(Line(UL * 0.12, DR * 0.12, stroke_width=4, color=ALERT), Line(DL * 0.12, UR * 0.12, stroke_width=4, color=ALERT))
            return VGroup(left, side("against", size=15), right, mark).arrange(RIGHT, buff=0.45).move_to([-2.4, y, 0])

        heads = VGroup(side("was readmitted", size=16, color=PAPER).move_to([-4.6, 2.35, 0]), side("was not", size=16, color=PAPER).move_to([-1.55, 2.35, 0]), side("the model's risk for each", size=15).move_to([-3.1, 2.75, 0]))
        shown = VGroup(*[pair(k, 1.75 - 0.62 * k) for k in range(4)])
        grid = VGroup(*[Square(side_length=0.075, stroke_width=0, fill_color=GOOD if ok else ALERT, fill_opacity=1) for ok in AUC["thousand"]]).arrange_in_grid(cols=50, buff=0.025).move_to([-2.9, -1.6, 0])
        grid_l = side(f"{len(AUC['thousand']):,} such pairs: the readmitted patient ranked higher in {AUC['thousand_right']}", size=16, color=PAPER).next_to(grid, DOWN, buff=0.16)
        define = VGroup(big("the AUC", size=30, color=ACCENT), side("the chance that the readmitted patient", size=17, color=PAPER), side("was given the higher risk", size=17, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX, 1.1, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.word(0, "Take one patient"))
            self.play(FadeIn(heads), LaggedStart(*[FadeIn(VGroup(p[0], p[1], p[2])) for p in shown], lag_ratio=0.25), run_time=1.8)
            seg.wait_until(seg.word(0, "The AUC is the chance"))
            self.play(*[FadeIn(p[3]) for p in shown], FadeIn(define), run_time=0.8)
            self.play(FadeIn(grid, lag_ratio=0.02), FadeIn(grid_l), run_time=1.0)

        bx, U = 2.3, 8.4                                                      # bars on a scale from 0.5 (coin flip) to 1.0 (perfect ranking)

        def gauge(label, value, color, y):
            frame = Rectangle(width=U * 0.5, height=0.32, stroke_color=FAINT, stroke_width=1.5).move_to([bx + U * 0.25, y, 0])
            b = Rectangle(width=U * (value - 0.5), height=0.32, stroke_width=0, fill_color=color, fill_opacity=1).move_to([bx + U * (value - 0.5) / 2, y, 0])
            return VGroup(side(label, size=16, color=PAPER).move_to([bx, y + 0.36, 0], aligned_edge=LEFT), frame, b, big(f"{value:.2f}", size=26, color=color).move_to([bx + U * (value - 0.5) + 0.55, y, 0]))

        g_wrong, g_fixed = gauge("the wrong model", AUC["wrong"], ALERT, 0.3), gauge("the corrected model", AUC["fixed"], GOOD, -0.65)
        scale_l = side("0.5 is a coin flip; 1 is a perfect ranking", size=14).move_to([bx + U * 0.25, 1.1, 0])
        off = VGroup(side("yet a tenth of the patients were off by", size=16, color=PAPER), big(f"\u00d7 {TENTHS['line'][0]['ratio']:.1f}", size=34, color=ALERT), side("it measures ranking, not whether the risks are right", size=15, color=ACCENT)).arrange(DOWN, buff=0.1)
        off = fit_width(off, 4.5).move_to([SX, -1.95, 0])
        with self.nar("s6_2") as seg:
            self.play(FadeOut(define), FadeIn(scale_l), FadeIn(g_wrong), run_time=0.9)
            seg.wait_until(seg.word(0, "For the corrected one"))
            self.play(FadeIn(g_fixed), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(off[0]), FadeIn(off[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "It measures ranking"))
            self.play(FadeIn(off[2]), run_time=0.6)

        g_plain, g_prov = gauge("our crowd: the risk factors alone", AUC["plain"], PAPER, 0.3), gauge("once the model knows the provider", AUC["with_providers"], PAPER, -0.65)
        gain = VGroup(side("the gain says providers differ", size=17, color=PAPER), side("not that the risk rule got better", size=17, color=ACCENT)).arrange(DOWN, buff=0.08).move_to([SX, -1.9, 0])
        with self.nar("s6_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(g_wrong, g_fixed, off)), FadeIn(g_plain), run_time=0.9)
            seg.wait_until(seg.word(0, "and 0.74 once"))
            self.play(FadeIn(g_prov), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(gain), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Slope(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "One slope for all")
        x0, x1, y0, y1 = -5.6, 0.2, -2.2, 2.2
        X = lambda v: x0 + (x1 - x0) * (v + 3.0) / 6.0
        Y = lambda p: y0 + (y1 - y0) * p
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 15, MUTED).move_to([X(v), y0 - 0.28, 0])) for v in (-3, -2, -1, 0, 1, 2, 3)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(pct(v), 15, MUTED).move_to([x0 - 0.45, Y(v), 0])) for v in (0, 0.25, 0.5, 0.75, 1.0)],
                      side("the first risk factor", size=16).move_to([(x0 + x1) / 2, y0 - 0.6, 0]), side("chance of readmission", size=16).move_to([x0 + 1.0, y1 + 0.24, 0]))
        shared = ParametricFunction(lambda v: np.array([X(v), Y(prob(SLOPE["fitted_gamma"] + SLOPE["shared"] * v)), 0.0]), t_range=[-3, 3, 0.05], color=PAPER, stroke_width=4)
        own = ParametricFunction(lambda v: np.array([X(v), Y(prob(SLOPE["true_gamma"] + SLOPE["steep"] * v)), 0.0]), t_range=[-3, 3, 0.05], color=ACCENT, stroke_width=4.5).set_z_index(4)
        names = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4, color=PAPER), side("the shared rule, at this provider's level", size=16, color=PAPER)).arrange(RIGHT, buff=0.2),
                       VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4.5, color=ACCENT), side("its own patients: twice as steep", size=16, color=ACCENT)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        names = fit_width(names, 5.0).move_to([3.7, 2.3, 0])
        who = side(f"our largest provider: {SLOPE['patients']} patients", size=17, color=PAPER).move_to([3.7, 2.95, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), Create(shared), FadeIn(who), FadeIn(names[0]), run_time=1.5)
            seg.wait_until(seg.word(0, "risk climbs twice as steeply"))
            self.play(Create(own), FadeIn(names[1]), run_time=1.1)

        def group(label, pair_, y, color):
            o, e = pair_
            m = Meter(color, width=1.1)
            m.move_to([1.9, y, 0])
            m.tilt_to(o - e)
            return VGroup(m, side(label, size=16, color=PAPER).move_to([3.0, y + 0.2, 0], aligned_edge=LEFT),
                          VGroup(big(f"{o:.0f}", size=26, color=color), side("against", size=15), big(f"{e:.1f}", size=26, color=PAPER)).arrange(RIGHT, buff=0.18).move_to([3.0, y - 0.22, 0], aligned_edge=LEFT))

        total = group("all its patients", SLOPE["total"], 1.0, GOOD)
        low = group("its lower-risk half", SLOPE["low"], -0.4, ALERT)
        high = group("its higher-risk half", SLOPE["high"], -1.8, ALERT)
        with self.nar("s7_2") as seg:
            self.play(FadeIn(total), run_time=0.9)
            seg.wait_until(seg.word(1, "18 against 41"))
            self.play(FadeIn(low), run_time=0.7)
            seg.wait_until(seg.word(1, "And 125 against"))
            self.play(FadeIn(high), run_time=0.7)

        note = fit_width(side("one gamma: an average over the patients it happens to treat", size=17, color=ACCENT), 5.4).move_to([4.0, -2.75, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeIn(note), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Limits(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "What no check sees")
        c1 = card(6.4, 3.4).move_to([0, 0.3, 0])
        title = txt("checked by the software before fitting", 20, ACCENT, weight=SEMIBOLD).move_to(c1.get_top() + DOWN * 0.45)
        rows = VGroup(*[VGroup(tick_mark(s=0.8), txt(s, 20, PAPER)).arrange(RIGHT, buff=0.25) for s in ("missing values", "a risk factor that never varies", "two risk factors correlated above 0.9", "variance inflation above 10")]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).move_to(c1.get_center() + DOWN * 0.25)
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(c1), FadeIn(title), run_time=1.0)
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.35), run_time=2.6)

        def caution(head, lines, x):
            c = card(5.7, 3.0).move_to([x, 0.2, 0])
            return VGroup(c, txt(head, 20, ALERT, weight=SEMIBOLD).move_to(c.get_top() + DOWN * 0.5), VGroup(*[txt(s, 19, PAPER) for s in lines]).arrange(DOWN, buff=0.12).move_to(c.get_center() + DOWN * 0.3))

        unseen = caution("no check can see", ["a risk factor", "that nobody recorded"], -3.2)
        more = caution("more is not always better", ["adjust for what a provider causes,", "such as a complication, and you", "adjust its performance away"], 3.2)
        with self.nar("s8_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(c1, title, rows)), run_time=0.6)
            seg.wait_until(seg.word(0, "None can see"))
            self.play(FadeIn(unseen), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(more), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(*[tiny_meter(w=0.34).scale(1.5) for _ in range(4)]).arrange(RIGHT, buff=0.22)
        bits = VGroup(*[Rectangle(width=0.2, height=0.2, stroke_width=0, fill_color=ACCENT, fill_opacity=0.2 + 0.08 * k) for k in range(10)]).arrange(RIGHT, buff=0.03)
        tilted = Meter(ALERT, width=0.8)
        tilted.tilt_to(4.0)
        icon2 = VGroup(bits, tilted).arrange(DOWN, buff=0.25)
        icon3 = VGroup(chip(PAPER, True, 0.14), tex(">", 34, ACCENT), chip(PAPER, False, 0.14)).arrange(RIGHT, buff=0.25)
        icons = [icon1, icon2, icon3]
        caps = [["Provider meters are level", "by construction.", "They prove nothing"], ["Take the same meter to new", "groups: tenths of risk, halves", "within a provider"], ["The AUC measures ranking,", "not fairness"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.95, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        rng = np.random.default_rng(16)                                        # a sketch, not data: providers of different sizes scattered round a common line
        xs_p = np.linspace(-5.6, 0.4, 14)
        sizes = rng.uniform(0.05, 0.16, 14)
        offs = rng.normal(0.0, 1.0, 14) * (0.16 - sizes) * 9.0
        line = DashedLine([-6.0, 0.4, 0], [0.8, 0.4, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR)
        own = VGroup(*[Dot([x, 0.4 + o, 0], radius=float(s), color=PAPER) for x, s, o in zip(xs_p, sizes, offs)])
        pulled = VGroup(*[Dot([x, 0.4 + o * (s / 0.16) ** 2, 0], radius=float(s), color=ACCENT) for x, s, o in zip(xs_p, sizes, offs)])
        own_l = side("a number for each provider, estimated on its own", size=17, color=PAPER).move_to([-2.6, 1.9, 0])
        pull_l = side("or: the small ones pulled toward the average", size=17, color=ACCENT).move_to([-2.6, -1.1, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("fixed or random?", size=34)).arrange(DOWN, buff=0.2).move_to([4.3, 0.3, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(line), FadeIn(own), FadeIn(own_l), run_time=1.0)
            seg.wait_until(seg.word(0, "Many analysts would"))
            self.play(Transform(own, pulled), FadeIn(pull_l), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_3", 17, "Fixed or Random?")
