"""Model in Motion · The Logistic Fixed-Effect Model · Episode 10: No Events, No Peak (what a clinic with no readmissions can tell us).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode10.py S04_March      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e10_numbers.json, written by e10_numbers.py; none is typed here. Readouts that move with
Elm's marker (the size-weighted average, Elm's expected count) are computed live from the same cast and fit.
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
from mim.castfit import CAST  # noqa: E402

N = json.loads((ROOT / "e10_numbers.json").read_text())
HILL, MARCH, PR, BR, SV, FT = N["hill"], N["march"], N["printed"], N["breaks"], N["survives"], N["footnotes"]
REF, BETA, G = N["reference"], N["fit"]["beta"], N["fit"]["gamma"]
N_ELM = N["elm"]["patients"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SIZES = {n: CAST[n][0] + CAST[n][2] for n in ORDER}
READM = {n: CAST[n][1] + CAST[n][3] for n in ORDER}
RX = 4.6


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def prob(g):
    return 1.0 / (1.0 + float(np.exp(-g)))


def elm_height(g):
    """Elm's own height at slider position g: eleven lower-risk patients, none readmitted."""
    return -N_ELM * float(np.log1p(np.exp(g)))


def mean_reference(elm):
    """The size-weighted average of the five gammas when Elm's printed value is `elm`."""
    return (sum(SIZES[n] * G[n] for n in FOUR) + SIZES["Elm"] * elm) / sum(SIZES.values())


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.1, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


class Track:
    """Elm's slider as one long horizontal track, so that a march of many units fits on screen."""

    def __init__(self, y=0.6, lo=-13.0, hi=0.5, x0=-5.9, x1=5.9, step=2):
        self.y, self.lo, self.hi, self.x0, self.x1 = y, lo, hi, x0, x1
        ticks = VGroup()
        for v in range(int(np.ceil(lo / step) * step), int(np.floor(hi)) + 1, step):
            ticks.add(VGroup(Line(self.P(v, -0.1), self.P(v, 0.1), stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 16, MUTED).move_to(self.P(v, -0.34))))
        self.g = VGroup(Line([x0, y, 0], [x1, y, 0], stroke_width=4, color=MUTED), ticks)

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (v - self.lo) / (self.hi - self.lo)

    def P(self, v, dy=0.0):
        return np.array([self.X(v), self.y + dy, 0.0])

    def others(self):
        """The four clinics whose sliders do settle, as small marks on the track."""
        dots = VGroup(*[Dot(self.P(G[n]), radius=0.08, color=COL[n]).set_z_index(3) for n in FOUR])
        label = side("the other four clinics", size=15).move_to(self.P(G["Cedar"], 0.78))
        return VGroup(dots, label)

    def flag(self, v, text, up=True, height=0.9, color=PAPER):
        s = 1 if up else -1
        pole = Line(self.P(v, 0.0), self.P(v, s * height), stroke_width=2.5, color=color)
        lab = VGroup(side(text, size=15, color=PAPER), big(minus(v), size=22, color=color)).arrange(DOWN, buff=0.05)
        lab.next_to(self.P(v, s * height), UP if up else DOWN, buff=0.08)
        return VGroup(pole, lab)


def long_ruler(y=-0.6):
    """A log-odds ruler long enough to hold Elm's printed values."""
    return Ruler(y, -12.6, 0.6, x0=-4.9, x1=6.3, ticks=list(range(-12, 1, 2)), labels={v: str(v).replace("-", "\u2212") for v in range(-12, 1, 2)}, title="log-odds")


def clinic_marks(R):
    """The four fitted clinics on the ruler, their initials staggered so that Alder and Dune stay apart."""
    lift = {"Alder": 0.32, "Dune": 0.62, "Cedar": 0.32, "Birch": 0.62}
    return VGroup(*[VGroup(Dot(R.P(G[n]), radius=0.1, color=COL[n]).set_z_index(4), txt(n[0], 16, COL[n], weight=SEMIBOLD).move_to(R.P(G[n], lift[n]))) for n in FOUR])


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        U, bx = 6.0, -3.2
        rows = {}
        for k, n in enumerate(ORDER):
            y, rate = 1.75 - 0.78 * k, READM[n] / SIZES[n]
            frame = Rectangle(width=U * 0.62, height=0.36, stroke_color=FAINT, stroke_width=1.5).move_to([bx + U * 0.31, y, 0])
            bar = Rectangle(width=max(U * rate, 0.01), height=0.36, stroke_width=0, fill_color=COL[n], fill_opacity=1 if rate else 0).move_to([bx + max(U * rate, 0.01) / 2, y, 0])
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-5.9, y, 0], aligned_edge=LEFT), frame, bar,
                             txt(f"{READM[n]} of {SIZES[n]}", 18, PAPER).move_to([bx + U * 0.62 + 0.9, y, 0]), txt(f"{100 * rate:.0f}%", 20, COL[n], weight=SEMIBOLD).move_to([bx + U * 0.62 + 2.2, y, 0]))
        head = side("readmitted", size=16).move_to([bx + U * 0.31, 2.4, 0])
        best = big("the best record in the cast", size=24, color=ACCENT).move_to([0, -2.45, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(rows[n]) for n in FOUR], lag_ratio=0.15), run_time=1.4)
            seg.wait_until(seg.s(1))
            bx_elm = box_around(rows["Elm"], ELM)
            self.play(FadeIn(rows["Elm"]), Create(bx_elm), run_time=1.0)
            seg.wait_until(seg.word(1, "The best record"))
            self.play(FadeIn(best, shift=UP * 0.1), run_time=0.8)

        def printout(label, value, x):
            c = card(4.7, 2.5).move_to([x, 0.45, 0])
            body = VGroup(side(f'algorithm = "{label}"', size=20), VGroup(txt("Elm", 28, ELM, weight=SEMIBOLD), tex(r"\gamma =", 40, PAPER), big(minus(value), size=44, color=PAPER)).arrange(RIGHT, buff=0.28)).arrange(DOWN, buff=0.4)
            return VGroup(c, body.move_to(c))

        a, b = printout("Serbin", PR["together"], -2.85), printout("Ban", PR["turns"], 2.85)
        same = side("same patients  \u00b7  same model  \u00b7  two answers", size=22, color=PAPER).move_to([0, -1.6, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(head, best, bx_elm, *rows.values())), run_time=0.6)
            seg.wait_until(seg.word(0, "Ask the software"))
            self.play(FadeIn(a, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(b, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(same), run_time=0.7)

        crosses = VGroup(*[VGroup(Line(m[0].get_corner(UL), m[0].get_corner(DR), stroke_width=5, color=ALERT), Line(m[0].get_corner(DL), m[0].get_corner(UR), stroke_width=5, color=ALERT)).set_stroke(opacity=0.8) for m in (a, b)]).set_z_index(8)
        neither = big("Neither.", size=44, color=ACCENT).move_to([0, -2.4, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "Neither"))
            self.play(Create(crosses), FadeOut(same), FadeIn(neither, scale=0.9), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 10, "No Events, No Peak", "what a clinic with no readmissions can tell us")


# =================================================================================== S03
class S03_Ramp(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "A hill with no top")
        x0, x1, y0, y1, g_lo, g_hi, h_lo, h_hi = -5.6, 1.6, -1.9, 2.1, -13.0, 0.0, -2.7, 0.3
        X = lambda g: x0 + (x1 - x0) * (g - g_lo) / (g_hi - g_lo)
        Y = lambda h: y0 + (y1 - y0) * (h - h_lo) / (h_hi - h_lo)
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 16, MUTED).move_to([X(v), y0 - 0.3, 0])) for v in range(-12, 1, 2)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 16, MUTED).move_to([x0 - 0.38, Y(v), 0])) for v in (0, -1, -2)],
                      side("position of Elm's slider", size=17).move_to([-3.2, y0 - 0.64, 0]), side("height", size=17).move_to([x0 + 0.1, y1 + 0.26, 0]))
        middle = VGroup(Line([X(REF), y0 - 0.02, 0], [X(REF), y0 + 0.22, 0], stroke_width=4, color=CEDAR), side("the middle clinic", size=15, color=CEDAR).move_to([X(REF), y0 - 0.64, 0]))
        pts = sorted([(g, h) for g, h in HILL["curve"] if g_lo <= g and h >= h_lo])
        ramp = VMobject(color=ELM, stroke_width=4.5).set_points_smoothly([np.array([X(g), Y(h), 0.0]) for g, h in pts]).set_z_index(3)
        marks = {}
        for key, g, where in (("reference", REF, RIGHT), ("-3", -3.0, RIGHT), ("-6.25", -6.25, DOWN), ("-11.5", -11.5, DOWN)):
            h = HILL["at"][key]
            d = Dot([X(g), Y(h), 0], radius=0.1, color=PAPER).set_z_index(5)
            marks[key] = VGroup(d, big(minus(h, 4 if key == "-11.5" else 2), size=22, color=PAPER).next_to(d, where, buff=0.16))
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(middle), run_time=1.1)
            self.play(Create(ramp), run_time=1.6, rate_func=linear)
            for key, cue in (("reference", "the height is"), ("-3", "At minus 3"), ("-6.25", "At minus 6.25")):
                seg.wait_until(seg.word(1, cue))
                self.play(GrowFromCenter(marks[key][0]), FadeIn(marks[key][1]), run_time=0.6)

        ceiling = DashedLine([x0, Y(0.0), 0], [x1, Y(0.0), 0], dash_length=0.12, stroke_width=2.5, color=ACCENT)
        ceiling_l = side("the ceiling: zero", size=17, color=ACCENT).move_to([0.5, Y(0.0) + 0.24, 0])
        verdict = VGroup(big("a ramp, not a hill", size=30), side("there is no top to find", size=20, color=PAPER)).arrange(DOWN, buff=0.18).move_to([RX, 0.9, 0])
        with self.nar("s3_2") as seg:
            seg.wait_until(seg.word(0, "toward a ceiling"))
            self.play(Create(ceiling), FadeIn(ceiling_l), GrowFromCenter(marks["-11.5"][0]), FadeIn(marks["-11.5"][1]), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.8)

        gp = ValueTracker(REF)
        rider = always_redraw(lambda: Dot([X(gp.get_value()), Y(elm_height(gp.get_value())), 0], radius=0.14, color=ACCENT).set_z_index(6))
        mx = 3.0
        obs = VGroup(side("observed", size=18, color=PAPER).move_to([mx, 0.75, 0], aligned_edge=LEFT), big("0", size=34, color=PAPER).move_to([mx + 2.3, 0.75, 0]))
        exp_l = side("expected", size=18, color=PAPER).move_to([mx, -0.05, 0], aligned_edge=LEFT)
        exp_n = DecimalNumber(N_ELM * prob(REF), num_decimal_places=2, font_size=44, color=ELM).move_to([mx + 2.3, -0.05, 0])
        exp_n.add_updater(lambda m: m.set_value(N_ELM * prob(gp.get_value())))
        exp_bar = always_redraw(lambda: Rectangle(width=max(1.3 * N_ELM * prob(gp.get_value()), 0.03), height=0.22, stroke_width=0, fill_color=ELM, fill_opacity=1).move_to([mx, -0.6, 0], aligned_edge=LEFT))
        never = side("never down to zero", size=17, color=ELM).move_to([mx, -1.0, 0], aligned_edge=LEFT)
        lower = VGroup(Arrow([X(-7.0), y0 + 0.75, 0], [X(-10.5), y0 + 0.75, 0], buff=0, stroke_width=5, color=ACCENT, max_tip_length_to_length_ratio=0.18),
                       big("the meter always says: lower", size=22, color=ACCENT)).arrange(DOWN, buff=0.15).move_to([X(-8.4), y0 + 0.75, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(FadeOut(verdict), run_time=0.5)
            self.add(rider)
            self.play(FadeIn(obs), FadeIn(exp_l), FadeIn(exp_n), run_time=0.9)
            self.add(exp_bar)
            seg.wait_until(seg.word(0, "But wherever"))
            self.play(gp.animate.set_value(-6.25), FadeIn(never), run_time=3.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(lower, shift=LEFT * 0.2), run_time=1.0)
        exp_n.clear_updaters(); rider.clear_updaters(); exp_bar.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_March(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Where the slider stops")
        T = Track()
        others = T.others()
        path = MARCH["path"]
        knob = Dot(T.P(path[0]), radius=0.17, color=ELM, stroke_color=INK, stroke_width=2).set_z_index(6)
        knob_l = txt("Elm", 18, ELM, weight=SEMIBOLD)
        knob_l.add_updater(lambda m: m.next_to(knob, UP, buff=0.14))
        prints = VGroup()
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(T.g), FadeIn(others), FadeIn(knob), FadeIn(knob_l), run_time=1.1)
            for v in path[1:]:
                self.play(knob.animate.move_to(T.P(v)), run_time=0.55)
                prints.add(Dot(T.P(v), radius=0.06, color=ELM).set_opacity(0.55))
                self.add(prints[-1])
            seg.wait_until(seg.word(1, "That takes five steps"))
            f_together = T.flag(PR["together"], f"stepping together: {PR['steps']['together']} steps", up=True, height=1.0, color=ELM)
            knob_l.clear_updaters()
            self.play(FadeIn(f_together), FadeOut(knob_l), run_time=0.8)

        wall_x = T.X(PR["wall"])
        wall = VGroup(Line([wall_x, T.y - 0.18, 0], [wall_x, T.y + 1.1, 0], stroke_width=9, color=PAPER),
                      *[Line([wall_x - 0.28, T.y + 0.02 + 0.26 * k, 0], [wall_x, T.y + 0.22 + 0.26 * k, 0], stroke_width=2.5, color=PAPER) for k in range(4)]).set_z_index(5)
        wall_l = VGroup(side("the wall", size=17, color=PAPER), big(minus(PR["wall"]), size=24, color=ELM)).arrange(DOWN, buff=0.06).move_to([wall_x + 0.15, T.y + 1.6, 0])
        ten = VGroup(DoubleArrow(T.P(PR["wall"], -0.95), T.P(REF, -0.95), buff=0, stroke_width=3, color=MUTED, tip_length=0.14), side("ten units below the middle clinic", size=16).move_to(T.P((PR["wall"] + REF) / 2, -1.25)))
        waits = side("taking turns waits for every slider to settle", size=17, color=PAPER).move_to([2.9, 2.75, 0])
        never = side(f"without the wall: still running after {PR['rounds_without_wall']:,.0f} rounds", size=17).move_to([0, -2.35, 0])
        with self.nar("s4_2") as seg:
            self.play(FadeIn(waits), run_time=0.7)
            seg.wait_until(seg.word(1, "So the software builds"))
            self.play(FadeIn(wall), FadeIn(wall_l[0]), GrowFromCenter(ten[0]), FadeIn(ten[1]), run_time=1.1)
            seg.wait_until(seg.word(1, "Elm's slider runs"))
            self.play(knob.animate.move_to(T.P(PR["wall"]) + RIGHT * 0.17), run_time=2.0, rate_func=linear)
            self.play(FadeIn(wall_l[1]), FadeIn(never), run_time=0.7)

        f_loose = T.flag(PR["looser"], "looser rule", up=False, height=0.95, color=MUTED)
        f_tight = T.flag(PR["tighter"], "tighter rule", up=False, height=0.95, color=MUTED)
        with self.nar("s4_3") as seg:
            self.play(FadeOut(ten), FadeOut(waits), run_time=0.5)
            seg.wait_until(seg.word(0, "Loosen it"))
            self.play(FadeIn(f_loose), run_time=0.7)
            seg.wait_until(seg.word(0, "Tighten it"))
            self.play(FadeIn(f_tight), run_time=0.7)

        none = big("four printed values, none of them an estimate", size=24, color=ALERT).move_to([0, -2.2, 0])
        safe = VGroup(tick_mark(s=0.9), side(f"the dial at {BETA:.4f} and the other four sliders: the same in every run", size=18, color=PAPER)).arrange(RIGHT, buff=0.25).move_to([0, -2.78, 0])
        with self.nar("s4_4", gap=0.8) as seg:
            self.play(FadeOut(never), run_time=0.4)
            seg.wait_until(seg.word(0, "None of them"))
            self.play(FadeIn(none, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(safe), Indicate(others[0], color=PAPER, scale_factor=1.6), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Breaks(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "What breaks")
        lo, hi = BR["interval"]
        iv = VGroup(DashedLine([-5.2, 1.6, 0], [5.2, 1.6, 0], dash_length=0.16, stroke_width=6, color=ELM),
                    Arrow([-5.1, 1.6, 0], [-5.75, 1.6, 0], buff=0, stroke_width=5, color=ELM, max_tip_length_to_length_ratio=0.5), Arrow([5.1, 1.6, 0], [5.75, 1.6, 0], buff=0, stroke_width=5, color=ELM, max_tip_length_to_length_ratio=0.5))
        iv_l = VGroup(txt("Elm's interval", 20, ELM, weight=SEMIBOLD), big(f"{minus(lo, 1)} to +{hi:.1f}", size=26, color=PAPER)).arrange(RIGHT, buff=0.35).move_to([0, 2.15, 0])
        built = big("anything built on the printed gamma", size=26, color=ALERT).move_to([0, 0.3, 0])
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(built, shift=UP * 0.1), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Create(iv[0]), GrowArrow(iv[1]), GrowArrow(iv[2]), FadeIn(iv_l), run_time=1.2)

        R = long_ruler(-0.85)
        marks = clinic_marks(R)
        e = ValueTracker(PR["together"])
        elm = always_redraw(lambda: VGroup(Dot(R.P(e.get_value()), radius=0.14, color=ELM), txt("Elm", 17, ELM, weight=SEMIBOLD).move_to(R.P(e.get_value(), 0.38))).set_z_index(5))
        avg = always_redraw(lambda: VGroup(Triangle(color=ACCENT, fill_opacity=1, stroke_width=0).scale(0.16).move_to(R.P(mean_reference(e.get_value()), -0.62)),
                                           Line(R.P(mean_reference(e.get_value()), -0.48), R.P(mean_reference(e.get_value()), 0.0), stroke_width=3, color=ACCENT)).set_z_index(4))
        avg_n = DecimalNumber(mean_reference(PR["together"]), num_decimal_places=2, font_size=36, color=ACCENT)
        avg_n.add_updater(lambda m: m.set_value(mean_reference(e.get_value())).move_to(R.P(mean_reference(e.get_value()), -1.05)))
        avg_l = side("the average gamma, weighted by size", size=17, color=ACCENT).move_to([2.9, -2.4, 0])
        state = {k: side(s, size=18, color=PAPER).move_to([-3.3, 0.6, 0]) for k, s in (("together", "after stepping together"), ("turns", "after taking turns"))}
        alder = VGroup(txt("Alder's readmissions", 20, ALDER, weight=SEMIBOLD),
                       VGroup(big(f"{BR['ratio']['together']['Alder']:.2f}", size=40, color=PAPER), side("or", size=20), big(f"{BR['ratio']['turns']['Alder']:.2f}", size=40, color=ALERT), side("times expected", size=20, color=PAPER)).arrange(RIGHT, buff=0.28)).arrange(DOWN, buff=0.15).move_to([2.9, 1.25, 0])
        with self.nar("s5_2") as seg:
            self.play(FadeOut(VGroup(iv, iv_l, built)), run_time=0.6)
            self.play(FadeIn(R.g), FadeIn(marks), run_time=0.9)
            self.add(elm)
            seg.wait_until(seg.word(0, "Suppose the reference"))
            self.add(avg, avg_n)
            self.play(FadeIn(avg_l), FadeIn(state["together"]), run_time=0.8)
            seg.wait_until(seg.word(1, "and minus 2.31"))
            self.play(e.animate.set_value(PR["turns"]), FadeOut(state["together"]), FadeIn(state["turns"]), run_time=2.2)
            seg.wait_until(seg.word(2, "Measured against it"))
            self.play(FadeIn(alder[0]), FadeIn(alder[1][0]), FadeIn(alder[1][3]), run_time=0.8)
            seg.wait_until(seg.word(2, "or 2.76 times"))
            self.play(FadeIn(alder[1][1]), FadeIn(alder[1][2]), run_time=0.7)

        direct = side(f"Elm's direct rate: {BR['direct_rate']['together']:.2f}% or {BR['direct_rate']['turns']:.3f}%", size=16).move_to([-3.3, 0.15, 0])
        yard = big("Elm has moved the yardstick for everyone", size=24, color=ACCENT).move_to([-0.2, 2.35, 0])
        with self.nar("s5_3", gap=0.8) as seg:
            self.play(FadeIn(yard, shift=UP * 0.1), FadeIn(direct), run_time=0.9)
        avg_n.clear_updaters(); elm.clear_updaters(); avg.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Survives(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "What survives")
        R = long_ruler(-0.85)
        marks = clinic_marks(R)
        e = ValueTracker(PR["together"])
        elm = always_redraw(lambda: VGroup(Dot(R.P(e.get_value()), radius=0.14, color=ELM), txt("Elm", 17, ELM, weight=SEMIBOLD).move_to(R.P(e.get_value(), 0.38))).set_z_index(5))
        avg = always_redraw(lambda: VGroup(Triangle(color=MUTED, fill_opacity=1, stroke_width=0).scale(0.14).move_to(R.P(mean_reference(e.get_value()), -0.62)),
                                           txt("average", 14, MUTED).move_to(R.P(mean_reference(e.get_value()), -0.95))).set_z_index(3))
        med = VGroup(Line(R.P(SV["median"], 0.0), R.P(SV["median"], 1.35), stroke_width=3, color=CEDAR),
                     VGroup(txt("the middle clinic", 18, CEDAR, weight=SEMIBOLD), big(minus(SV["median"]), size=30, color=PAPER)).arrange(RIGHT, buff=0.25).move_to(R.P(SV["median"] - 1.9, 1.65))).set_z_index(4)
        built = big("anything built on the count", size=26, color=GOOD).move_to([-2.6, 2.3, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(built, shift=UP * 0.1), FadeIn(R.g), FadeIn(marks), run_time=1.2)
            self.add(elm, avg)
            seg.wait_until(seg.word(1, "Take the middle clinic"))
            self.play(FadeIn(med), run_time=0.8)
            seg.wait_until(seg.word(1, "The median does not care"))
            self.play(e.animate.set_value(PR["turns"]), run_time=1.8)
            self.play(e.animate.set_value(PR["together"]), run_time=1.4)
        elm.clear_updaters(); avg.clear_updaters()

        xs = [-5.0 + 0.86 * k for k in range(N_ELM)]
        people = VGroup(*[VGroup(Circle(radius=0.27, stroke_color=ELM, stroke_width=4).move_to([x, 1.35, 0]), txt(f"{100 * SV['stay']:.0f}%", 15, PAPER).move_to([x, 0.82, 0])) for x in xs])
        people_l = side(f"Elm's {N_ELM} patients, at the middle clinic's level", size=18, color=PAPER).move_to([-0.7, 2.15, 0])
        stay_l = side("each one's chance of staying out", size=16).move_to([-0.7, 0.42, 0])
        counts = VGroup(VGroup(side("expected", size=20, color=PAPER), big(f"{SV['expected']:.2f}", size=44, color=PAPER)).arrange(RIGHT, buff=0.3),
                        VGroup(side("observed", size=20, color=PAPER), big("0", size=44, color=ELM)).arrange(RIGHT, buff=0.3)).arrange(RIGHT, buff=1.2).move_to([-0.7, -0.55, 0])
        chance = MathTex(rf"{SV['stay']:.2f}^{{{N_ELM}}}", "=", f"{SV['p_none']:.2f}", font_size=44, color=PAPER)
        chance[2].set_color(ACCENT)
        chance_g = VGroup(chance, big(f"{100 * SV['p_none']:.0f}%", size=44, color=ACCENT)).arrange(RIGHT, buff=0.8).move_to([-0.7, -1.75, 0])
        with self.nar("s6_2") as seg:
            self.play(FadeOut(VGroup(built, R.g, marks, elm, avg, med)), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(p[0], scale=0.8) for p in people], lag_ratio=0.06), FadeIn(people_l), FadeIn(counts[0]), run_time=1.5)
            seg.wait_until(seg.word(0, "Elm had none"))
            self.play(FadeIn(counts[1]), run_time=0.6)
            seg.wait_until(seg.word(1, "Each patient has"))
            self.play(LaggedStart(*[FadeIn(p[1]) for p in people], lag_ratio=0.05), FadeIn(stay_l), run_time=1.1)
            seg.wait_until(seg.word(1, "For all eleven"))
            self.play(Write(chance), FadeIn(chance_g[1]), run_time=1.2)

        verdict = VGroup(pill("not rare, so not flagged", 22), side("zero is not automatically excellent", size=20, color=PAPER)).arrange(DOWN, buff=0.25).move_to([4.75, -1.55, 0])
        verdict = fit_width(verdict, 4.0).move_to([4.85, -1.55, 0])
        with self.nar("s6_3") as seg:
            seg.wait_until(seg.word(0, "So Elm is not flagged"))
            self.play(FadeIn(verdict[0], scale=0.9), run_time=0.7)
            seg.wait_until(seg.word(0, "Zero is not"))
            self.play(FadeIn(verdict[1]), run_time=0.7)

        x0, x1, y0, y1 = -5.2, 1.5, -1.9, 2.0
        X = lambda n: x0 + (x1 - x0) * n / 36.0
        Y = lambda p: y0 + (y1 - y0) * (np.log10(p) + 3.0) / 3.0
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 16, MUTED).move_to([X(v), y0 - 0.3, 0])) for v in (0, 10, 20, 30)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(s, 16, MUTED).move_to([x0 - 0.52, Y(v), 0])) for v, s in ((1.0, "100%"), (0.1, "10%"), (0.01, "1%"), (0.001, "0.1%"))],
                      side("such patients, none readmitted", size=17).move_to([(x0 + x1) / 2, y0 - 0.64, 0]), side("chance of that", size=17).move_to([x0 + 0.6, y1 + 0.26, 0]))
        curve = VMobject(color=ELM, stroke_width=4.5).set_points_as_corners([np.array([X(0), Y(1.0), 0.0])] + [np.array([X(n), Y(p), 0.0]) for n, p in SV["curve"] if n <= 35]).set_z_index(3)
        five = VGroup(DashedLine([x0, Y(0.05), 0], [x1, Y(0.05), 0], dash_length=0.1, stroke_width=2.5, color=ALERT), txt("5%", 16, ALERT).move_to([x1 + 0.32, Y(0.05), 0]))
        pt = {}
        for n, lab in ((N_ELM, f"{N_ELM} patients: {100 * SV['p_none']:.0f}%"), (SV["first_flag"], f"{SV['first_flag']}: the first below 5%"), (30, f"30: {100 * SV['p_thirty']:.1f}%")):
            p = SV["stay"] ** n
            d = Dot([X(n), Y(p), 0], radius=0.11, color=ACCENT if n != N_ELM else PAPER).set_z_index(5)
            pt[n] = VGroup(d, side(lab, size=17, color=PAPER).next_to(d, UR, buff=0.1))
        speaks = VGroup(big("the count speaks,", size=26), big("even when gamma cannot", size=26, color=ACCENT)).arrange(DOWN, buff=0.12).move_to([RX + 0.15, 1.0, 0])
        ratio = side(f"exact interval for Elm's ratio: 0 to {SV['ratio_upper']:.2f}", size=16).move_to([RX + 0.15, -0.9, 0])
        ratio = fit_width(ratio, 3.9).move_to([RX + 0.2, -0.9, 0])
        with self.nar("s6_4", gap=0.8) as seg:
            self.play(FadeOut(VGroup(people, people_l, stay_l, counts, chance_g, verdict)), run_time=0.6)
            self.play(FadeIn(axes), Create(curve), FadeIn(five), run_time=1.5)
            self.play(FadeIn(pt[N_ELM]), run_time=0.5)
            seg.wait_until(seg.word(0, "about three chances"))
            self.play(FadeIn(pt[30]), FadeIn(pt[SV["first_flag"]]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(speaks, shift=UP * 0.1), FadeIn(ratio), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Footnotes(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "Two footnotes")
        T = Track(y=0.5, lo=-13.0, hi=11.0, x0=-5.9, x1=5.9, step=4)
        up_wall = REF + (REF - PR["wall"])                 # ten units above the same middle clinic; in the all-readmitted cast the middle clinic itself shifts

        def wall(v, sign):
            x = T.X(v)
            return VGroup(Line([x, T.y - 0.18, 0], [x, T.y + 1.0, 0], stroke_width=9, color=PAPER),
                          *[Line([x + sign * 0.28, T.y + 0.02 + 0.26 * k, 0], [x, T.y + 0.22 + 0.26 * k, 0], stroke_width=2.5, color=PAPER) for k in range(4)]).set_z_index(5)

        lo_w, hi_w = wall(PR["wall"], -1), wall(up_wall, 1)
        lo_l = VGroup(side("no readmissions", size=17, color=PAPER), side("the lower wall", size=15)).arrange(DOWN, buff=0.05).move_to([T.X(PR["wall"]) + 0.9, T.y + 1.5, 0])
        hi_l = VGroup(side("every patient readmitted", size=17, color=PAPER), side("the upper wall", size=15)).arrange(DOWN, buff=0.05).move_to([T.X(up_wall) - 1.1, T.y + 1.5, 0])
        mid = VGroup(Dot(T.P(REF), radius=0.09, color=CEDAR), side("the middle clinic", size=15, color=CEDAR).move_to(T.P(REF, 0.4)))
        a = Dot(T.P(REF - 1.0), radius=0.16, color=ELM, stroke_color=INK, stroke_width=2).set_z_index(6)
        b = Dot(T.P(REF + 1.0), radius=0.16, color=ALERT, stroke_color=INK, stroke_width=2).set_z_index(6)
        ten = side("ten units either side of the middle clinic", size=17).move_to([0, T.y - 1.25, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(T.g), FadeIn(mid), run_time=1.0)
            seg.wait_until(seg.word(0, "First, the mirror image"))
            self.play(FadeIn(lo_w), FadeIn(lo_l), FadeIn(a), FadeIn(ten), run_time=0.8)
            self.play(a.animate.move_to(T.P(PR["wall"]) + RIGHT * 0.17), run_time=1.3)
            seg.wait_until(seg.word(0, "runs to an upper wall"))
            self.play(FadeIn(hi_w), FadeIn(hi_l), FadeIn(b), run_time=0.7)
            self.play(b.animate.move_to(T.P(up_wall) + LEFT * 0.17), run_time=1.3)

        U, bx = 0.25, -3.6
        cut = FT["cutoff"]
        sizes = [(n, SIZES[n], COL[n]) for n in ORDER] + [("Fen", FT["fen"]["patients"], MUTED)]
        rows = {}
        for k, (n, s, c) in enumerate(sizes):
            y = 1.95 - 0.7 * k
            bar = Rectangle(width=U * s, height=0.34, stroke_width=0, fill_color=c, fill_opacity=1).move_to([bx + U * s / 2, y, 0])
            rows[n] = VGroup(txt(n, 22, c, weight=SEMIBOLD).move_to([-5.9, y, 0], aligned_edge=LEFT), bar, txt(str(s), 20, PAPER).next_to(bar, RIGHT, buff=0.15))
        screen = VGroup(DashedLine([bx + U * cut, 2.35, 0], [bx + U * cut, -1.95, 0], dash_length=0.1, stroke_width=3, color=ACCENT),
                        side(f"the screen: more than {cut} records", size=17, color=ACCENT).move_to([bx + U * cut + 1.9, -2.3, 0]))
        fen_l = side("never entered the fit", size=17, color=PAPER).next_to(rows["Fen"], RIGHT, buff=0.6)
        elm_l = side("in by a single patient", size=17, color=ELM).next_to(rows["Elm"], RIGHT, buff=0.6)
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(T.g, mid, lo_w, hi_w, lo_l, hi_l, a, b, ten)), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(rows[n]) for n in ORDER], lag_ratio=0.1), run_time=1.0)
            seg.wait_until(seg.word(0, "Fen, with"))
            self.play(FadeIn(rows["Fen"]), run_time=0.6)
            seg.wait_until(seg.word(0, "because the software screens"))
            self.play(Create(screen[0]), FadeIn(screen[1]), FadeIn(fen_l), rows["Fen"].animate.set_opacity(0.45), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(elm_l), Indicate(rows["Elm"][1], color=ELM, scale_factor=1.08), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        ramp = ParametricFunction(lambda t: np.array([t, -0.85 * np.exp(2.4 * (t - 0.75)), 0.0]), t_range=[-0.9, 0.75, 0.02], color=ELM, stroke_width=4.5)
        icon1 = VGroup(DashedLine([-0.9, 0.06, 0], [0.75, 0.06, 0], dash_length=0.08, stroke_width=2.5, color=ACCENT), ramp)
        g_sym = tex(r"\hat\gamma", 46, MUTED)
        g_x = VGroup(g_sym, Line(g_sym.get_corner(UL), g_sym.get_corner(DR), stroke_width=4, color=ALERT), Line(g_sym.get_corner(DL), g_sym.get_corner(UR), stroke_width=4, color=ALERT))
        icon2 = VGroup(g_x, VGroup(txt("count", 24, PAPER, weight=SEMIBOLD), tick_mark(s=1.0)).arrange(RIGHT, buff=0.18)).arrange(RIGHT, buff=0.6)
        icon3 = VGroup(*[Circle(radius=0.16, stroke_color=ELM, stroke_width=3.5) for _ in range(4)], tex("?", 44, ACCENT)).arrange(RIGHT, buff=0.14)
        icons = [icon1, icon2, icon3]
        caps = [["No readmissions: a hill with no top.", "The printed gamma records", "where the fitting stopped"], ["Built on that gamma: breaks.", "Built on the count: survives"],
                ["Zero, from a handful of", "patients, is weak evidence"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.9, 0])
            captions.add(fit_width(VGroup(*[txt(s, 18, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        count = VGroup(VGroup(side("observed", size=24, color=PAPER), big("0", size=72, color=ELM)).arrange(DOWN, buff=0.15),
                       side("against", size=22), VGroup(side("expected at the reference", size=24, color=PAPER), big(f"{SV['expected']:.2f}", size=72, color=PAPER)).arrange(DOWN, buff=0.15)).arrange(RIGHT, buff=0.7).move_to([-1.9, 0.2, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("swap the curve", size=34)).arrange(DOWN, buff=0.2).move_to([RX + 0.2, 0.2, 0])
        with self.nar("s8_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(count, scale=0.95), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s8_3", 11, "Swap the Curve")
