"""Model in Motion · The Logistic Fixed-Effect Model · Episode 7: Climbing the Hill (how a computer finds the top).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode07.py S06_Stairs      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Positions, steps, round counts and the map come from e07_numbers.json, written by e07_numbers.py. The machine's
readings are computed live by mim.meters.FitMachine. All content stays above y = -3.0, clear of the captions.
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
from mim.meters import *  # noqa: E402,F403

N = json.loads((ROOT / "e07_numbers.json").read_text())
FIT, DU, ROUNDS, RC, ELM_STEPS, MAP, HILL, JOINT = N["fit"], N["dune"], N["rounds_plain"], N["rounds"], N["elm"], N["map"], N["hill"], N["joint"]
BETA, G, G0V = FIT["beta"], FIT["gamma"], N["start_gamma"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
CAP = [-2.4, -2.72, 0]
RX = 4.6                                                # centre of the right-hand notes


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def box_around(m):
    return SurroundingRectangle(m, color=PAPER, buff=0.1, stroke_width=2, corner_radius=0.08).set_z_index(7)


def hill_chart(x0, x1, y0, y1, b_hi=4.0, h_lo=-63.5, h_hi=-55.0):
    """Episode 6's hill: the height over the dial position. Returns (X, Y, axes, curve)."""
    X = lambda bv: x0 + (x1 - x0) * bv / b_hi
    Y = lambda hv: y0 + (y1 - y0) * (hv - h_lo) / (h_hi - h_lo)
    axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
    curve = VMobject(color=PAPER, stroke_width=4.5).set_points_smoothly([np.array([X(bv), Y(hv), 0.0]) for bv, hv in HILL["profile"] if bv <= b_hi])
    return X, Y, axes, curve


def dune_height(gv):
    """Dune's own height for a slider position, with the dial held at its fitted place."""
    c, t = CLINICS["Dune"], 0.0
    for (n, e), eta in ((c["low"], gv), (c["high"], gv + BETA)):
        p = float(expit(eta))
        t += e * np.log(p) + (n - e) * np.log(1 - p)
    return float(t)


def the_map(x0=-5.6, x1=1.2, y0=-2.1, y1=2.4):
    """The hill from above: the dial against Birch's slider, the other clinics levelled. Returns (MX, MY, group)."""
    (b0, b1), (g0, g1) = MAP["beta_range"], MAP["gamma_range"]
    MX = lambda bv: x0 + (x1 - x0) * (bv - b0) / (b1 - b0)
    MY = lambda gv: y0 + (y1 - y0) * (gv - g0) / (g1 - g0)
    axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
    xt = VGroup(*[VGroup(Line([MX(v), y0, 0], [MX(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 17, MUTED).move_to([MX(v), y0 - 0.3, 0])) for v in (0, 1, 2, 3)])
    yt = VGroup(*[VGroup(Line([x0 - 0.1, MY(v), 0], [x0, MY(v), 0], stroke_width=2, color=MUTED), txt(minus(v, 0), 17, MUTED).move_to([x0 - 0.4, MY(v), 0])) for v in (-3, -2, -1, 0)])
    xl = side("the dial", size=18).move_to([(x0 + x1) / 2, y0 - 0.62, 0])
    yl = side("Birch's slider", size=18).move_to([x0 + 0.55, y1 + 0.28, 0])
    rings = VGroup()
    for k, c in enumerate(sorted(MAP["contours"], key=lambda c: -c["below_top"])):
        line = VMobject(color=MUTED, stroke_width=1.6 + 0.25 * k).set_points_as_corners([np.array([MX(a), MY(b), 0.0]) for a, b in c["points"]])
        rings.add(line.set_stroke(opacity=0.45 + 0.08 * k))
    top = Dot([MX(BETA), MY(G["Birch"]), 0], radius=0.1, color=ACCENT).set_z_index(5)
    return MX, MY, VGroup(axes, xt, yt, xl, yl, rings, top)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        X, Y, axes, curve = hill_chart(-5.4, 1.6, -2.0, 2.4)
        top = Dot([X(HILL["peak_beta"]), Y(HILL["peak"]), 0], radius=0.11, color=ACCENT).set_z_index(5)
        top_l = side("every meter level", size=18, color=ACCENT).next_to(top, UP, buff=0.2)
        (ba, ha), (bb, hb) = HILL["profile"][0], HILL["profile"][2]
        foot = np.array([X(ba), Y(ha), 0.0])
        u = np.array([X(bb) - X(ba), Y(hb) - Y(ha), 0.0])
        u = u / np.linalg.norm(u)
        climber = Dot(foot, radius=0.1, color=PAPER).set_z_index(5)
        qm = big("?", size=40, color=ACCENT).next_to(climber, UR, buff=0.15)
        with self.nar("s1_1") as seg:
            self.play(FadeIn(axes), Create(curve), run_time=1.4)
            self.play(GrowFromCenter(top), FadeIn(top_l), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(climber), FadeIn(qm), run_time=0.8)

        eq = fit_width(MathTex(r"\sum_{j}\ \frac{1}{1 + e^{-(\gamma_i + \beta x_{ij})}}", "=", r"O_i", font_size=38, color=PAPER), 4.4).move_to([RX, 0.9, 0])
        eq_l = side("expected = observed, for each clinic", size=17).next_to(eq, UP, buff=0.3)
        no = fit_width(side("no formula solves this for gamma and beta", size=18, color=PAPER), 4.4).next_to(eq, DOWN, buff=0.35)
        slope = Arrow(foot, foot + u * 1.0, buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.25).set_z_index(4)
        nrm = np.array([-u[1], u[0], 0.0])
        bend = ArcBetweenPoints(foot + u * 0.3 - nrm * 0.28, foot + u * 1.25 - nrm * 0.5, angle=PI / 5, color=MUTED, stroke_width=3)
        with self.nar("s1_2") as seg:
            seg.wait_until(seg.word(0, "It cannot solve"))
            self.play(FadeIn(eq_l), Write(eq), run_time=1.6)
            self.play(FadeIn(no), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(qm), GrowArrow(slope), run_time=0.8)
            seg.wait_until(seg.word(1, "and how the slope"))
            self.play(Create(bend), run_time=0.8)

        q = VGroup(big("How do you climb a hill", size=26), big("you can only feel?", size=26)).arrange(DOWN, buff=0.12).move_to([RX, -1.7, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 7, "Climbing the Hill", "how a computer finds the top")


# =================================================================================== S03
class S03_OneStep(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "One slider, one step")
        x0, x1, y0, y1, g_lo, g_hi, h_lo, h_hi = -5.7, 1.1, -2.0, 2.3, -2.4, 0.8, -10.4, -6.2
        X = lambda gv: x0 + (x1 - x0) * (gv - g_lo) / (g_hi - g_lo)
        Y = lambda hv: y0 + (y1 - y0) * (hv - h_lo) / (h_hi - h_lo)
        Pt = lambda gv, hv: np.array([X(gv), Y(hv), 0.0])
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
        xt = VGroup(*[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(minus(v, 1), 16, MUTED).move_to([X(v), y0 - 0.3, 0]))
                      for v in (-2.0, -1.5, -1.0, -0.5, 0.0, 0.5)])
        xl = side("Dune's slider", size=18).move_to([(x0 + x1) / 2, y0 - 0.62, 0])
        yl = side("Dune's height", size=18).move_to([x0 + 0.55, y1 + 0.28, 0])
        hill = ParametricFunction(lambda gv: Pt(gv, dune_height(gv)), t_range=[g_lo, g_hi, 0.02], color=MUTED, stroke_width=4).set_stroke(opacity=0.45)
        s0, s1, s2 = DU["steps"][0], DU["steps"][1], DU["steps"][2]

        def parabola(s, left, right, width=4):
            q = lambda gv: s["height"] + s["tilt"] * (gv - s["gamma"]) - 0.5 * s["wobble"] * (gv - s["gamma"]) ** 2
            return ParametricFunction(lambda gv: Pt(gv, q(gv)), t_range=[s["gamma"] - left, s["gamma"] + right, 0.02], color=ACCENT, stroke_width=width).set_z_index(3)

        par1, par2 = parabola(s0, 0.55, 1.75), parabola(s1, 0.75, 0.75, 3)
        peak1_h = s0["height"] + 0.5 * s0["tilt"] ** 2 / s0["wobble"]              # the top of the first parabola
        climber = Dot(Pt(s0["gamma"], s0["height"]), radius=0.11, color=PAPER).set_z_index(6)
        mark1 = Circle(radius=0.11, stroke_color=ACCENT, stroke_width=3).move_to(Pt(s1["gamma"], peak1_h)).set_z_index(5)
        jump1 = DoubleArrow(Pt(s0["gamma"], h_lo + 0.45), Pt(s1["gamma"], h_lo + 0.45), buff=0, stroke_width=3, color=ACCENT, tip_length=0.14)
        jump1_l = big(f"+{s0['step']:.2f}", size=26, color=ACCENT).next_to(jump1, UP, buff=0.12)
        jump2_l = big(minus(s1["step"], 3), size=22, color=ACCENT).next_to(Pt(s1["gamma"], s1["height"]), UP, buff=0.45)
        here = txt(minus(s0["gamma"]), 18, PAPER).next_to(climber, DOWN, buff=0.2)
        land1 = txt(minus(s1["gamma"]), 18, ACCENT).next_to(mark1, UP, buff=0.18)
        top_l = VGroup(big(minus(s2["gamma"]), size=28, color=ACCENT), side("two steps", size=19, color=PAPER)).arrange(DOWN, buff=0.1).move_to(Pt(s2["gamma"], s2["height"]) + UP * 0.95)
        tan = np.array([X(s0["gamma"] + 0.3) - X(s0["gamma"]), Y(s0["height"] + 0.3 * s0["tilt"]) - Y(s0["height"]), 0.0])
        tan = tan / np.linalg.norm(tan)
        slope = Arrow(climber.get_center(), climber.get_center() + tan * 1.1, buff=0, stroke_width=4, color=PAPER, max_tip_length_to_length_ratio=0.25).set_z_index(5)
        dial = Dial(BETA, r=0.45).move_to([3.4, 1.3, 0])
        dial.turn_to(BETA)
        held = VGroup(tex(r"\beta", 32, ACCENT), side("held at", size=17, color=PAPER), big(f"{BETA:.2f}", size=22, color=ACCENT)).arrange(RIGHT, buff=0.15).next_to(dial, DOWN, buff=0.25)
        gt = ValueTracker(s0["gamma"])
        sl = Slider("Dune", s0["gamma"], h=1.7, lo=g_lo, hi=g_hi).move_to([5.6, 1.15, 0])
        sl.add_updater(lambda m: m.slide_to(gt.get_value()))
        sv = DecimalNumber(s0["gamma"], num_decimal_places=2, include_sign=True, font_size=22, color=PAPER)
        sv.add_updater(lambda m: m.set_value(gt.get_value()).next_to(sl.track, UP, buff=0.14))
        sv.update()
        know = VGroup(side("we know only:", size=18), side("the slope here,", size=18, color=PAPER), side("and how fast it is changing", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, -1.3, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(dial), FadeIn(held), FadeIn(sl), FadeIn(sv), FadeIn(axes), FadeIn(xt), FadeIn(xl), FadeIn(yl), run_time=1.2)

        with self.nar("s3_2") as seg:
            self.play(Create(hill), run_time=1.6)
            self.play(GrowFromCenter(climber), FadeIn(here), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(hill.animate.set_stroke(opacity=0.15), FadeIn(know[0]), run_time=0.8)
            seg.wait_until(seg.word(1, "the slope under our feet"))
            self.play(GrowArrow(slope), FadeIn(know[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "and how fast"))
            self.play(FadeIn(know[2]), run_time=0.7)

        with self.nar("s3_3") as seg:
            self.play(FadeOut(slope), Create(par1), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(mark1), GrowFromCenter(jump1), FadeIn(jump1_l), FadeIn(land1), run_time=1.0)
            self.play(climber.animate.move_to(Pt(s1["gamma"], s1["height"])), gt.animate.set_value(s1["gamma"]), FadeOut(here), run_time=1.2)

        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeOut(par1), FadeOut(mark1), FadeOut(land1), Create(par2), run_time=1.0)
            seg.wait_until(seg.word(0, "The second jump"))
            self.play(FadeIn(jump2_l), climber.animate.move_to(Pt(s2["gamma"], s2["height"])), gt.animate.set_value(s2["gamma"]), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(par2), FadeOut(jump2_l), FadeOut(know), hill.animate.set_stroke(opacity=0.9), FadeIn(top_l), run_time=1.0)
        sl.clear_updaters()
        sv.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Tilt(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Tilt over wobble")
        s0 = DU["steps"][0]
        meter = Meter(DUNE)
        meter.tilt_to(s0["tilt"])
        meter.scale(2.2).move_to([-4.6, 1.05, 0])
        ob = VGroup(side("observed", size=17), big(str(s0["observed"]), size=26, color=DUNE)).arrange(DOWN, buff=0.06).next_to(meter, DL, buff=0.1).shift(RIGHT * 0.5)
        ex = VGroup(side("expected", size=17), big(f"{s0['expected']:.1f}", size=26, color=DUNE)).arrange(DOWN, buff=0.06).next_to(meter, DR, buff=0.1).shift(LEFT * 0.5 + UP * 0.2)
        tilt = VGroup(side("the tilt", color=PAPER), big(f"{s0['tilt']:.1f}", size=38, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([-4.6, -0.75, 0])

        x0, x1, y0, y1 = -1.4, 3.6, -0.6, 1.9
        HX = lambda p: x0 + (x1 - x0) * p
        HY = lambda v: y0 + (y1 - y0) * v / 0.27
        haxes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
        hxt = VGroup(*[txt(f"{v}%", 16, MUTED).move_to([HX(v / 100), y0 - 0.28, 0]) for v in (0, 50, 100)])
        hxl = side("a patient's probability", size=17).move_to([(x0 + x1) / 2, y0 - 0.62, 0])
        hyl = side("what one patient adds to the wobble", size=17).move_to([x0 + 1.75, y1 + 0.28, 0])
        hump = ParametricFunction(lambda p: np.array([HX(p), HY(p * (1 - p)), 0.0]), t_range=[0.0, 1.0, 0.01], color=PAPER, stroke_width=4)
        w = DU["wobble_per_patient"]
        half = VGroup(Dot([HX(0.5), HY(0.25), 0], radius=0.09, color=ACCENT), txt(f"{w['at_half']:.2f}", 18, ACCENT).move_to([HX(0.5), HY(0.25) + 0.3, 0]))
        edge = VGroup(Dot([HX(0.02), HY(w["at_two_percent"]), 0], radius=0.08, color=MUTED), Dot([HX(0.98), HY(w["at_two_percent"]), 0], radius=0.08, color=MUTED),
                      txt(f"{w['at_two_percent']:.2f}", 16, MUTED).move_to([HX(0.02) + 0.42, HY(w["at_two_percent"]) + 0.22, 0]))
        n_low, n_high = CLINICS["Dune"]["low"][0], CLINICS["Dune"]["high"][0]
        d_low = VGroup(Dot([HX(DU["p_low"]), HY(w["low"]), 0], radius=0.1, color=DUNE), txt(f"{n_low} \u00d7 {w['low']:.2f}", 17, DUNE).move_to([HX(DU["p_low"]) + 0.85, HY(w["low"]) - 0.22, 0]))
        d_high = VGroup(Dot([HX(DU["p_high"]), HY(w["high"]), 0], radius=0.1, color=DUNE), txt(f"{n_high} \u00d7 {w['high']:.2f}", 17, DUNE).move_to([HX(DU["p_high"]) + 0.85, HY(w["high"]) + 0.2, 0]))
        wob = VGroup(side("the wobble", color=PAPER), tex("V", 34, PAPER), big(f"{s0['wobble']:.2f}", size=38, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([5.3, 0.6, 0])
        wob = fit_width(wob, 3.2).move_to([5.45, 0.6, 0])
        frac = MathTex(r"\text{step}", "=", r"\frac{\text{tilt}}{\text{wobble}}", "=", rf"\frac{{{s0['tilt']:.1f}}}{{{s0['wobble']:.2f}}}", "=", f"{s0['step']:.2f}", font_size=40, color=PAPER).move_to([0, -2.05, 0])
        frac[6].set_color(ACCENT)
        how = side("which way, and how far", size=24, color=ACCENT).next_to(frac, RIGHT, buff=0.6)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(meter), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ob), FadeIn(ex), run_time=0.8)
            seg.wait_until(seg.word(1, "a gap of"))
            self.play(FadeIn(tilt, shift=UP * 0.1), run_time=0.8)

        with self.nar("s4_2") as seg:
            self.play(FadeIn(haxes), FadeIn(hxt), FadeIn(hxl), FadeIn(hyl), Create(hump), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(half[0]), FadeIn(half[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "A patient near zero"))
            self.play(FadeIn(edge), run_time=0.7)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(d_low), FadeIn(d_high), run_time=0.8)
            self.play(FadeIn(wob, shift=UP * 0.1), run_time=0.8)

        with self.nar("s4_3") as seg:
            self.play(Write(frac[:3]), run_time=1.2)
            seg.wait_until(seg.word(0, "divided by") - 0.6)
            self.play(FadeIn(frac[3:5]), run_time=0.7)
            seg.wait_until(seg.word(1, "move"))
            self.play(FadeIn(frac[5:]), run_time=0.7)

        with self.nar("s4_4", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "It does not just say"))
            self.play(FadeIn(how, shift=LEFT * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Turns(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Taking turns")
        M = FitMachine({n: G0V for n in ORDER}, 0.0)
        rd = Integer(0, font_size=34, color=ACCENT)
        counter = VGroup(side("round", color=PAPER), rd).arrange(RIGHT, buff=0.25).move_to(CAP)

        def sliders(r, rt):
            self.play(*[M.g[n].animate.set_value(ROUNDS[r]["gamma_after"][i]) for i, n in enumerate(ORDER)], run_time=rt)

        def dial(r, rt):
            self.play(M.b.animate.set_value(ROUNDS[r]["beta_after"]), run_time=rt)
            rd.set_value(r + 1)

        self.play(FadeIn(tag), FadeIn(M.all), run_time=1.0)
        with self.nar("s5_1") as seg:
            seg.wait_until(seg.word(0, "Every clinic can take"))
            sliders(0, 1.6)

        with self.nar("s5_2") as seg:
            self.play(FadeIn(counter), run_time=0.4)
            dial(0, 1.4)
            seg.wait_until(seg.s(1))
            sliders(1, 0.9)
            dial(1, 0.8)
            sliders(2, 0.8)
            dial(2, 0.7)

        bx = box_around(VGroup(M.dial, M.bval))
        with self.nar("s5_3") as seg:
            for r in range(3, 8):
                sliders(r, 0.4)
                dial(r, 0.35)
            self.play(Create(bx), run_time=0.5)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(bx), run_time=0.3)
            self.play(M.b.animate.set_value(BETA), *[M.g[n].animate.set_value(G[n]) for n in FOUR], M.g["Elm"].animate.set_value(G["Cedar"] - 10.0),
                      ChangeDecimalToValue(rd, RC["plain"]), run_time=3.0)

        eb = box_around(VGroup(M.sl["Elm"], M.gval["Elm"]))
        elm_list = txt(",  ".join(minus(v) for v in ELM_STEPS) + "  \u2026", 18, ELM).move_to([M.XS["Elm"] + 1.2, -2.72, 0])
        with self.nar("s5_4", gap=0.8) as seg:
            self.play(FadeOut(counter), Create(eb), FadeIn(side("Elm, round by round:", size=18, color=PAPER).next_to(elm_list, LEFT, buff=0.3)), FadeIn(elm_list), run_time=0.9)
        M.clear()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Stairs(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Why it zig-zags")
        MX, MY, board = the_map()
        pts = [np.array([MX(a), MY(b), 0.0]) for a, b in MAP["stair"]]
        stair = VMobject(color=PAPER, stroke_width=3.5).set_points_as_corners(pts).set_z_index(4)
        begin = VGroup(Dot(pts[0], radius=0.08, color=PAPER).set_z_index(5), side("the plain guess", size=16, color=PAPER).next_to(pts[0], DOWN, buff=0.3).shift(RIGHT * 0.55))
        (g_lo, g_hi) = MAP["gamma_range"]
        rpts = [np.array([MX(a), MY(b), 0.0]) for a, b in MAP["ridge"] if g_lo + 0.05 < b < g_hi - 0.05]
        ridge = DashedVMobject(VMobject().set_points_as_corners(rpts), num_dashes=34, color=ACCENT, stroke_width=3).set_z_index(3)
        ridge_l = side("the ridge", size=18, color=ACCENT).move_to(rpts[int(len(rpts) * 0.88)] + UR * 0.4)
        note = side("a slice of the hill: the other clinics levelled", size=15).move_to([-2.2, 2.75, 0]).shift(RIGHT * 1.6)
        rows = []
        for k, (label, value, color) in enumerate((("zero at a lower-risk patient", f"{RC['plain']} rounds", PAPER),
                                                   ("zero five units away", f"{RC['five_higher']:,} rounds", ALERT),
                                                   ("zero in the middle  (pprof_py)", f"{RC['centred']} rounds", GOOD))):
            rows.append(VGroup(side(label, size=17, color=PAPER), big(value, size=28, color=color)).arrange(DOWN, buff=0.08, aligned_edge=LEFT).move_to([3.1, 1.3 - 1.25 * k, 0], aligned_edge=LEFT))
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(board), FadeIn(note), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(begin), run_time=0.5)
            self.play(Create(stair), run_time=3.2, rate_func=linear)

        with self.nar("s6_2") as seg:
            self.play(Create(ridge), FadeIn(ridge_l), run_time=1.4)

        with self.nar("s6_3") as seg:
            seg.wait_until(seg.word(0, "where we put zero"))
            self.play(FadeIn(rows[0], shift=LEFT * 0.1), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(rows[1], shift=LEFT * 0.1), run_time=0.8)

        with self.nar("s6_4", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "the ridge straightens"))
            self.play(FadeIn(rows[2], shift=LEFT * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = MathTex(r"\frac{O - E}{V}", font_size=46, color=PAPER)
        icon2 = VGroup(*[VGroup(Line(DOWN * 0.4, UP * 0.4, stroke_width=4, color=FAINT), Dot(UP * dy, radius=0.09, color=c)) for dy, c in ((0.2, ALDER), (-0.15, BIRCH), (0.0, CEDAR), (0.25, DUNE))],
                       Dial(BETA, r=0.32)).arrange(RIGHT, buff=0.28)
        icon3 = VGroup(DashedLine([-0.8, 0.6, 0], [0.8, -0.6, 0], dash_length=0.1, stroke_width=3, color=ACCENT),
                       VMobject(color=PAPER, stroke_width=4).set_points_as_corners([np.array(p + [0.0]) for p in ([-0.8, 0.9], [-0.8, 0.6], [-0.4, 0.6], [-0.4, 0.3], [0.0, 0.3], [0.0, 0.0], [0.4, 0.0], [0.4, -0.3])]))
        icons = [icon1, icon2, icon3]
        caps = [["A step is tilt over wobble:", "which way, and how far"], ["The sliders can step together;", "the dial steps in turn"], ["Taking turns climbs", "a diagonal ridge by staircase"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        same = side("every route climbs toward the same top; they differ in how long they take", size=20, color=PAPER).move_to([0, -2.4, 0])
        with self.nar("s7_2") as seg:
            self.play(FadeIn(same, shift=UP * 0.1), run_time=0.9)

        MX, MY, board = the_map()
        jp = [np.array([MX(a), MY(b), 0.0]) for a, b in JOINT["path"]]
        straight = VMobject(color=ACCENT, stroke_width=4.5).set_points_as_corners(jp).set_z_index(4)
        dots = VGroup(*[Dot(p, radius=0.07, color=ACCENT).set_z_index(5) for p in jp[:-1]])
        five = VGroup(big(f"{JOINT['steps']} steps", size=30, color=ACCENT), side("sliders and dial together", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([RX, 0.9, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("the arrow matrix", size=34)).arrange(DOWN, buff=0.2).move_to([RX, -1.0, 0])
        with self.nar("s7_3") as seg:
            self.play(FadeOut(VGroup(cards, captions, same, *icons)), run_time=0.7)
            self.play(FadeIn(board), run_time=1.0)
            seg.wait_until(seg.word(0, "step together"))
            self.play(Create(straight), FadeIn(dots), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(five, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "Next time"))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s7_4", 8, "The arrow matrix")
