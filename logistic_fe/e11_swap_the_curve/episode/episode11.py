"""Model in Motion · The Logistic Fixed-Effect Model · Episode 11: Swap the Curve (observed against expected, at a reference clinic).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode11.py S04_Swap      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e11_numbers.json, written by e11_numbers.py; none is typed here. The cast's counts come from
mim.castfit. The middle value in S05 is recomputed live as one slider is pushed away.
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

N = json.loads((ROOT / "e11_numbers.json").read_text())
REFD, AL, EXP, RATIO, POOLED, RATE, LINK, MEAN, CROWD, TOT = (N[k] for k in ("reference", "alder", "expected", "ratio", "pooled", "rate", "link", "mean_reference", "crowd", "totals"))
REF, BETA, G, ELM_AT = REFD["gamma"], N["fit"]["beta"], N["fit"]["gamma"], N["elm_printed"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
OBS = {n: CAST[n][1] + CAST[n][3] for n in ORDER}
SX = 4.3                                            # centre of the side column beside the probability panel


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def pct(p):
    return f"{100 * p:.0f}%"


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.1, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def tray(name, r=0.105):
    """A clinic's patients as chips, filled where the patient was readmitted: lower-risk block, then higher-risk block."""
    n0, e0, n1, e1 = CAST[name]
    lo = VGroup(*[chip(COL[name], k < e0, r) for k in range(n0)]).arrange_in_grid(cols=6, buff=0.09)
    hi = VGroup(*[chip(COL[name], k < e1, r) for k in range(n1)]).arrange_in_grid(cols=3, buff=0.09)
    return VGroup(VGroup(lo, side(f"{n0} lower-risk", size=15)).arrange(DOWN, buff=0.16), VGroup(hi, side(f"{n1} higher-risk", size=15)).arrange(DOWN, buff=0.16)).arrange(RIGHT, buff=0.55, aligned_edge=UP)


def hatched_ring(center, r=0.14, color=ELM):
    """Elm's marker: a ring with hatching, for a clinic with no finite estimate."""
    c = np.array(center, dtype=float)
    u, w = np.array([1.0, 1.0, 0.0]) / np.sqrt(2), np.array([-1.0, 1.0, 0.0]) / np.sqrt(2)
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=3).move_to(c),
                  *[Line(c + w * r * d - u * r * 0.9 * np.sqrt(1 - d * d), c + w * r * d + u * r * 0.9 * np.sqrt(1 - d * d), stroke_width=2, color=color) for d in (-0.5, 0.0, 0.5)])


def slider_ruler(y=-0.3):
    return Ruler(y, -7.5, 0.6, x0=-4.9, x1=6.2, ticks=list(range(-7, 1)), labels={v: str(v).replace("-", "\u2212") for v in range(-7, 1)}, title="log-odds")


def mini_curve(color, shift=0.0, w=1.7, h=1.0):
    return ParametricFunction(lambda t: np.array([w * t, h * (1.0 / (1.0 + np.exp(-6.0 * (t - shift))) - 0.5), 0.0]), t_range=[-0.5, 0.5, 0.02], color=color, stroke_width=4)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        chips = tray("Alder").move_to([-3.5, 0.55, 0])
        name = txt("Alder", 28, ALDER, weight=SEMIBOLD).next_to(chips, UP, buff=0.4)
        count = VGroup(big(f"{OBS['Alder']} of {CAST['Alder'][0] + CAST['Alder'][2]}", size=30), side("readmitted", size=18, color=PAPER)).arrange(RIGHT, buff=0.25).next_to(chips, DOWN, buff=0.45)
        answers = VGroup(*[VGroup(side(lab, size=18, color=PAPER), VGroup(big(f"{v:.1f}", size=44, color=c), side("times expected", size=18)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.12)
                           for lab, v, c in (("against everyone pooled together", POOLED["Alder"], PAPER), ("against everyone but Alder itself", N["alder_rest"], PAPER))]).arrange(DOWN, buff=0.7).move_to([3.3, 0.45, 0])
        ep3 = side("Episode 3", size=16).next_to(answers, UP, buff=0.4)
        with self.nar("s1_1") as seg:
            self.play(FadeIn(name), LaggedStart(*[FadeIn(c, scale=0.6) for c in [*chips[0][0], *chips[1][0]]], lag_ratio=0.02), FadeIn(chips[0][1]), FadeIn(chips[1][1]), run_time=1.6)
            self.play(FadeIn(count), run_time=0.6)
            seg.wait_until(seg.word(1, "Against everyone pooled"))
            self.play(FadeIn(ep3), FadeIn(answers[0], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "Against everyone but"))
            self.play(FadeIn(answers[1], shift=UP * 0.1), run_time=0.8)

        def need(lines, extra, y):
            c = card(5.6, 1.5).move_to([3.2, y, 0])
            return VGroup(c, VGroup(*[txt(s, 19, PAPER) for s in lines]).arrange(DOWN, buff=0.1).move_to(c).shift(LEFT * 0.55), extra.move_to(c.get_right() + LEFT * 0.6))

        rule = need(["a risk rule learned from patients", "who share a clinic"], VGroup(tex(r"\beta", 34, ACCENT), tick_mark(s=0.9)).arrange(DOWN, buff=0.12), 1.15)
        yard = need(["a yardstick no single clinic", "can bend"], txt("today", 18, ACCENT, weight=SEMIBOLD), -0.75)
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(ep3, answers)), run_time=0.5)
            self.play(FadeIn(rule[0]), FadeIn(rule[1]), FadeIn(yard[0]), FadeIn(yard[1]), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(rule[2]), run_time=0.6)
            seg.wait_until(seg.word(1, "Today, the yardstick"))
            yard_box = box_around(yard[0], ACCENT)
            self.play(FadeIn(yard[2]), Create(yard_box), run_time=0.8)

        frame = RoundedRectangle(width=3.6, height=2.6, corner_radius=0.2, stroke_color=CEDAR, stroke_width=3, fill_color=INK_2, fill_opacity=1).move_to([3.4, 0.55, 0])
        frame_l = txt("the middle clinic", 22, CEDAR, weight=SEMIBOLD).next_to(frame, UP, buff=0.25)
        q = big("?", size=72, color=CEDAR).move_to(frame)
        arrow = Arrow(chips.get_right() + RIGHT * 0.25, frame.get_left() + LEFT * 0.15, buff=0, stroke_width=5, color=PAPER, max_tip_length_to_length_ratio=0.12)
        paper = side("on paper", size=16).next_to(arrow, UP, buff=0.1)
        ask = big(f"more than {OBS['Alder']}, or fewer?", size=30, color=ACCENT).move_to([0, -2.4, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(rule, yard, yard_box)), run_time=0.5)
            seg.wait_until(seg.word(0, "send them"))
            self.play(FadeIn(frame), FadeIn(frame_l), GrowArrow(arrow), FadeIn(paper), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(q), FadeIn(ask, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 11, "Swap the Curve", "observed against expected, at a reference clinic")


# =================================================================================== S03
class S03_Reference(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "The reference clinic")
        R = slider_ruler(-0.3)
        lift = {"Alder": 0.34, "Dune": 0.66, "Cedar": 0.34, "Birch": 0.66}
        marks = VGroup(*[VGroup(Dot(R.P(G[n]), radius=0.11, color=COL[n]).set_z_index(4), txt(n, 16, COL[n], weight=SEMIBOLD).move_to(R.P(G[n], lift[n]))) for n in FOUR])
        e = ValueTracker(ELM_AT)
        elm = always_redraw(lambda: VGroup(hatched_ring(R.P(e.get_value())), txt("Elm", 16, ELM, weight=SEMIBOLD).move_to(R.P(e.get_value(), 0.34))).set_z_index(4))
        mid = VGroup(Line(R.P(REF, 0.0), R.P(REF, -1.25), stroke_width=3, color=CEDAR),
                     VGroup(side("the middle one", size=18, color=PAPER), big(minus(REF), size=30, color=CEDAR)).arrange(RIGHT, buff=0.25).move_to(R.P(REF, -1.6))).set_z_index(3)
        stays = side("wherever Elm's slider stops, the middle one stays", size=17).move_to([-1.6, 1.6, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(R.g), LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15), run_time=1.4)
            self.add(elm)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(mid), run_time=0.8)
            seg.wait_until(seg.word(1, "it stays put"))
            self.play(e.animate.set_value(-7.2), FadeIn(stays), run_time=1.3)
            self.play(e.animate.set_value(ELM_AT), run_time=1.0)
        elm.clear_updaters()

        C = CurvePanel(BETA)
        ref_curve = C.curve(REF, CEDAR)
        ref_l = txt("the reference", 20, CEDAR, weight=SEMIBOLD).move_to(C.P(3.75, 0.7))
        pts = {}
        for key, s, p, where in (("lo", 0.0, REFD["p_low"], DR), ("hi", BETA, REFD["p_high"], DR)):
            c = risk_chip(p, r=0.28, color=PAPER).move_to(C.P(s, p)).set_z_index(5)
            pts[key] = VGroup(c, big(pct(p), size=26, color=PAPER).next_to(c, where, buff=0.08))
        with self.nar("s3_2") as seg:
            self.play(FadeOut(VGroup(R.g, marks, elm, mid, stays)), run_time=0.6)
            self.play(FadeIn(C.g), Create(ref_curve), FadeIn(ref_l), run_time=1.5)
            seg.wait_until(seg.word(1, "a lower-risk patient"))
            self.play(FadeIn(pts["lo"], scale=0.8), run_time=0.7)
            seg.wait_until(seg.word(1, "A higher-risk patient"))
            self.play(FadeIn(pts["hi"], scale=0.8), run_time=0.7)

        note = VGroup(big("a clinic,", size=28), big("not an average patient", size=28, color=ACCENT), side("one clinic's level,", size=19, color=PAPER), side("applied to whoever walks in", size=19, color=PAPER)).arrange(DOWN, buff=0.16)
        note = fit_width(note, 4.6).move_to([SX, 0.4, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            seg.wait_until(seg.s(0) + 2.0)
            self.play(FadeIn(note, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Swap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Swap the curve")
        C = CurvePanel(BETA)
        ref_curve = C.curve(REF, CEDAR)
        own_curve = C.curve(G["Alder"], ALDER)
        key = lambda label, color: VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4.5, color=color), txt(label, 17, color, weight=SEMIBOLD)).arrange(RIGHT, buff=0.15)
        own_l, ref_l = key("Alder's own curve", ALDER), key("the reference", CEDAR)
        VGroup(own_l, ref_l).arrange(DOWN, buff=0.14, aligned_edge=LEFT).move_to([-0.35, -1.55, 0])
        n0, n1 = CAST["Alder"][0], CAST["Alder"][2]
        spots = {"lo": (0.0, AL["p_low"], REFD["p_low"], n0, LEFT), "hi": (BETA, AL["p_high"], REFD["p_high"], n1, RIGHT)}
        chips, labels, ghosts, drops, new_labels = {}, {}, {}, {}, {}
        for k, (s, p_own, p_ref, n, where) in spots.items():
            chips[k] = risk_chip(p_own, r=0.3, color=ALDER).move_to(C.P(s, p_own)).set_z_index(6)
            labels[k] = VGroup(big(pct(p_own), size=24, color=ALDER), side(f"{n} patients", size=15, color=PAPER)).arrange(DOWN, buff=0.04)
            labels[k].next_to(chips[k], LEFT, buff=0.14).shift(UP * 0.18) if k == "lo" else labels[k].next_to(chips[k], UL, buff=0.04)
            ghosts[k] = Circle(radius=0.3, stroke_color=ALDER, stroke_width=2).set_stroke(opacity=0.45).move_to(C.P(s, p_own)).set_z_index(4)
            drops[k] = DashedLine(C.P(s, p_own) + DOWN * 0.3, C.P(s, p_ref) + UP * 0.3, dash_length=0.07, stroke_width=2.5, color=PAPER).set_z_index(4)
            new_labels[k] = VGroup(big(pct(p_ref), size=24, color=PAPER), side(f"{n} patients", size=15, color=PAPER)).arrange(DOWN, buff=0.04).next_to(C.P(s, p_ref) + (LEFT if k == "lo" else RIGHT) * 0.3, where, buff=0.14).shift(UP * 0.18 if k == "lo" else DOWN * 0.24)

        def tally(title, color, a, b, total, places, y):
            f = MathTex(rf"{n0} \times {a:.3f} + {n1} \times {b:.3f}", "=", f"{total:.{places}f}", font_size=32, color=PAPER)
            f[2].set_color(color)
            g = VGroup(side(title, size=17, color=color), fit_width(f, 4.7)).arrange(DOWN, buff=0.14)
            return g.move_to([SX, y, 0])

        own_sum = tally("on Alder's own curve", ALDER, AL["p_low"], AL["p_high"], AL["own_expected"], 1, 1.95)
        ref_sum = tally("on the reference curve", CEDAR, REFD["p_low"], REFD["p_high"], AL["ref_expected"], 2, 0.6)
        balanced = VGroup(tick_mark(s=0.8), side(f"what Alder observed: {OBS['Alder']}", size=16, color=PAPER)).arrange(RIGHT, buff=0.15).next_to(own_sum, DOWN, buff=0.14)
        self.play(FadeIn(tag), FadeIn(C.g), FadeIn(ref_curve), FadeIn(ref_l), run_time=1.0)
        with self.nar("s4_1") as seg:
            self.play(Create(own_curve), FadeIn(own_l), run_time=1.0)
            seg.wait_until(seg.word(0, "24 lower-risk patients"))
            self.play(FadeIn(chips["lo"], scale=0.8), FadeIn(labels["lo"]), run_time=0.7)
            seg.wait_until(seg.word(0, "and 6 higher-risk"))
            self.play(FadeIn(chips["hi"], scale=0.8), FadeIn(labels["hi"]), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(own_sum), run_time=0.9)
            seg.wait_until(seg.word(1, "Exactly what Alder"))
            self.play(FadeIn(balanced), run_time=0.6)

        with self.nar("s4_2") as seg:
            seg.wait_until(seg.word(0, "The same 30 patients"))
            self.add(*ghosts.values())
            self.play(*[Create(drops[k]) for k in spots], *[FadeOut(labels[k]) for k in spots],
                      *[Transform(chips[k], risk_chip(spots[k][2], r=0.3, color=ALDER).move_to(C.P(spots[k][0], spots[k][2])).set_z_index(6)) for k in spots], run_time=1.8)
            self.play(*[FadeIn(new_labels[k]) for k in spots], run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ref_sum), run_time=0.9)

        frac = MathTex(rf"\frac{{{OBS['Alder']}}}{{{AL['ref_expected']:.2f}}}", "=", f"{AL['ratio']:.2f}", font_size=54, color=PAPER)
        frac[2].set_color(ACCENT)
        frac_g = VGroup(frac, side("observed, over expected at the reference", size=16, color=PAPER)).arrange(DOWN, buff=0.16).move_to([SX, -0.95, 0])
        name = side("the indirect standardized ratio", size=14).next_to(frac_g, DOWN, buff=0.1)
        with self.nar("s4_3") as seg:
            seg.wait_until(seg.s(1))
            self.play(Write(frac), FadeIn(frac_g[1]), run_time=1.3)
            self.play(FadeIn(name), run_time=0.5)

        steps = VGroup(*[pill(s, 17) for s in ("keep the patients", "swap the curve", "count")]).arrange(RIGHT, buff=0.3)
        steps = fit_width(steps, 5.3).move_to([SX, -2.68, 0])
        with self.nar("s4_4", gap=0.8) as seg:
            for k, cue in enumerate(("Keep the patients", "Swap the curve", "Count")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(steps[k], scale=0.9), run_time=0.45)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_All(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "All five clinics")
        AX = lambda r: -2.3 + 2.8 * r
        y_ax, ys = -1.75, {n: 1.75 - 0.72 * k for k, n in enumerate(ORDER)}
        axis = VGroup(Line([AX(0), y_ax, 0], [AX(2.1), y_ax, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([AX(v), y_ax, 0], [AX(v), y_ax - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([AX(v), y_ax - 0.3, 0])) for v in (0, 0.5, 1, 1.5, 2)],
                      side("observed, over expected at the reference", size=16).move_to([AX(1.05), y_ax - 0.64, 0]))
        one = VGroup(DashedLine([AX(1), y_ax, 0], [AX(1), 2.25, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), txt("the reference", 16, CEDAR, weight=SEMIBOLD).move_to([AX(1), 2.5, 0]))
        rows = {}
        for n in ORDER:
            y, r = ys[n], RATIO[n]
            dot = Dot([AX(r), y, 0], radius=0.14, color=COL[n]).set_z_index(5) if r > 0 else hatched_ring([AX(0), y, 0]).set_z_index(5)
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.2, y, 0], aligned_edge=LEFT), side(f"{OBS[n]} \u00f7 {EXP[n]:.2f}", size=16).move_to([-3.8, y, 0]),
                             Line([AX(1), y, 0], [AX(r), y, 0], stroke_width=4, color=COL[n]).set_stroke(opacity=0.7), dot, big(f"{r:.2f}" if r > 0 else "0", size=24, color=COL[n]).move_to([4.15, y, 0]))
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(axis), FadeIn(one), run_time=1.0)
            for n, cue in zip(ORDER, ("Alder,", "Birch,", "Cedar,", "Dune,", "And Elm")):
                seg.wait_until(seg.word(0, cue))
                self.play(FadeIn(rows[n]), run_time=0.5)
            seg.wait_until(seg.s(1))
            self.play(Indicate(rows["Cedar"][3], color=PAPER, scale_factor=1.6), run_time=0.9)

        ya = ys["Alder"]
        old = VGroup(*[VGroup(Circle(radius=0.11, stroke_color=PAPER, stroke_width=2.5).move_to([AX(v), ya, 0]), txt(f"{v:.1f}", 14, PAPER).move_to([AX(v), ya + 0.3, 0])) for v in (POOLED["Alder"], N["alder_rest"])]).set_z_index(6)
        old_l = side("Episode 3's two answers", size=15, color=PAPER).move_to([AX(1.6) + 0.95, ya + 0.66, 0])
        R = slider_ruler(-0.3)
        a = ValueTracker(G["Alder"])
        middle = lambda: float(np.median([a.get_value(), G["Birch"], G["Cedar"], G["Dune"], ELM_AT]))
        lift = {"Dune": 0.66, "Cedar": 0.34, "Birch": 0.66}
        fixed = VGroup(*[VGroup(Dot(R.P(G[n]), radius=0.11, color=COL[n]).set_z_index(4), txt(n, 16, COL[n], weight=SEMIBOLD).move_to(R.P(G[n], lift[n]))) for n in ("Birch", "Cedar", "Dune")],
                       VGroup(hatched_ring(R.P(ELM_AT)), txt("Elm", 16, ELM, weight=SEMIBOLD).move_to(R.P(ELM_AT, 0.34))))
        mover = always_redraw(lambda: VGroup(Dot(R.P(a.get_value()), radius=0.13, color=ALDER), txt("Alder", 16, ALDER, weight=SEMIBOLD).move_to(R.P(a.get_value(), 0.98))).set_z_index(6))
        mid = always_redraw(lambda: VGroup(Line(R.P(middle(), 0.0), R.P(middle(), -1.2), stroke_width=3, color=ACCENT),
                                           Triangle(color=ACCENT, fill_opacity=1, stroke_width=0).scale(0.14).move_to(R.P(middle(), -0.22))).set_z_index(3))
        mid_n = DecimalNumber(REF, num_decimal_places=2, font_size=38, color=ACCENT)
        mid_n.add_updater(lambda m: m.set_value(middle()).move_to(R.P(middle(), -1.55)))
        mid_l = side("the middle value", size=17, color=ACCENT).move_to([5.35, -1.85, 0])
        push = side("push one slider as far as you like", size=18, color=PAPER).move_to([-1.2, 2.25, 0])
        stop = side("the middle value stops at the next clinic along", size=18, color=ACCENT).move_to([-1.2, 1.7, 0])
        with self.nar("s5_2") as seg:
            self.play(FadeIn(old), FadeIn(old_l), run_time=0.8)
            seg.wait_until(seg.word(1, "Push any one slider") - 1.4)
            self.play(*[FadeOut(m) for m in (axis, one, old, old_l, *rows.values())], run_time=0.6)
            self.play(FadeIn(R.g), FadeIn(fixed), run_time=0.7)
            self.add(mover, mid, mid_n)
            self.play(FadeIn(mid_l), FadeIn(push), run_time=0.5)
            seg.wait_until(seg.word(1, "Push any one slider") + 0.4)
            self.play(a.animate.set_value(-7.2), run_time=3.2, rate_func=linear)
            self.play(FadeIn(stop), run_time=0.6)
        mid_n.clear_updaters(); mover.clear_updaters(); mid.clear_updaters()

        tots = VGroup(*[VGroup(big(v, size=54, color=c), *[side(s, size=18, color=PAPER) for s in lab]).arrange(DOWN, buff=0.14)
                        for v, c, lab in ((str(TOT["observed"]), PAPER, ["readmissions", "observed"]), (f"{TOT['pooled']:.1f}", MUTED, ["expected, against", "the pooled standard"]),
                                          (f"{TOT['reference']:.1f}", ACCENT, ["expected, against", "the middle clinic"]))]).arrange(RIGHT, buff=1.3, aligned_edge=UP).move_to([0, 0.5, 0])
        even = side("the clinics no longer break even as a group, and they need not", size=20, color=PAPER).move_to([0, -1.9, 0])
        with self.nar("s5_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in (R.g, fixed, mover, mid, mid_n, mid_l, push, stop)], run_time=0.6)
            self.play(FadeIn(tots[0]), FadeIn(tots[1]), run_time=0.9)
            seg.wait_until(seg.word(0, "Against the middle clinic"))
            self.play(FadeIn(tots[2], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(even), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Rate(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "As a rate")
        U, bx = 5.6, -3.4
        overall = N["overall"]
        rows = {}
        for k, n in enumerate(ORDER):
            y, v = 1.6 - 0.72 * k, RATE[n] / 100
            frame = Rectangle(width=U, height=0.36, stroke_color=FAINT, stroke_width=1.5).move_to([bx + U / 2, y, 0])
            bar = Rectangle(width=max(U * v, 0.01), height=0.36, stroke_width=0, fill_color=COL[n], fill_opacity=1 if v else 0).move_to([bx + max(U * v, 0.01) / 2, y, 0])
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.2, y, 0], aligned_edge=LEFT), frame, bar, big(pct(v), size=26, color=COL[n]).move_to([bx + U + 0.7, y, 0]),
                             side(f"{RATIO[n]:.2f} \u00d7 {pct(overall)}" if RATIO[n] else f"0 \u00d7 {pct(overall)}", size=16).move_to([bx + U + 2.5, y, 0]))
        line = VGroup(DashedLine([bx + U * overall, 2.05, 0], [bx + U * overall, -1.75, 0], dash_length=0.1, stroke_width=2.5, color=PAPER),
                      side(f"the overall rate: {pct(overall)}", size=16, color=PAPER).move_to([bx + U * overall, 2.35, 0]))
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), *[FadeIn(VGroup(rows[n][0], rows[n][1])) for n in ORDER], FadeIn(line), run_time=1.3)
            self.play(*[FadeIn(rows[n][4]) for n in ORDER], run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(rows[n][2], LEFT), FadeIn(rows[n][3])) for n in ORDER], lag_ratio=0.45), run_time=4.0)

        real = VGroup(side("what Alder's patients really face:", size=18, color=PAPER),
                      *[VGroup(risk_chip(p, r=0.22, color=ALDER), big(pct(p), size=24, color=ALDER)).arrange(RIGHT, buff=0.15) for p in (AL["p_low"], AL["p_high"])]).arrange(RIGHT, buff=0.45).move_to([-1.2, -2.3, 0])
        same = side(f"{pct(RATE['Alder'] / 100)} is the ratio {RATIO['Alder']:.2f}, moved to a familiar scale. It is nobody's chance.", size=17, color=ACCENT).move_to([-0.2, -2.85, 0])
        with self.nar("s6_2", gap=0.8) as seg:
            self.play(Create(box_around(VGroup(rows["Alder"][0], rows["Alder"][3]), ALDER)), run_time=0.7)
            seg.wait_until(seg.word(0, "No patient at Alder"))
            self.play(FadeIn(real), run_time=0.8)
            seg.wait_until(seg.word(0, "It is the same ratio"))
            self.play(FadeIn(same), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Link(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "Ratio and gamma")
        x0, x1, y0, y1, g_lo, g_hi, r_hi = -5.3, 1.1, -1.9, 2.2, -3.2, 1.2, 3.2
        X = lambda g: x0 + (x1 - x0) * (g - g_lo) / (g_hi - g_lo)
        Y = lambda r: y0 + (y1 - y0) * r / r_hi
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 16, MUTED).move_to([X(v), y0 - 0.3, 0])) for v in range(-3, 2)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(str(v), 16, MUTED).move_to([x0 - 0.35, Y(v), 0])) for v in (0, 1, 2, 3)],
                      side("position of Alder's slider", size=17).move_to([(x0 + x1) / 2, y0 - 0.64, 0]), side("Alder's ratio", size=17).move_to([x0 + 0.45, y1 + 0.26, 0]))
        level = DashedLine([x0, Y(1), 0], [x1, Y(1), 0], dash_length=0.1, stroke_width=1.8, color=FAINT)
        curve = VMobject(color=ALDER, stroke_width=4.5).set_points_smoothly([np.array([X(g), Y(r), 0.0]) for g, r in zip(LINK["grid"], LINK["curve"]) if r <= r_hi]).set_z_index(3)
        p_ref = VGroup(Dot([X(REF), Y(1.0), 0], radius=0.12, color=CEDAR).set_z_index(5), VGroup(side("at the reference", size=16, color=CEDAR), big("1", size=26, color=CEDAR)).arrange(RIGHT, buff=0.2))
        p_ref[1].next_to(p_ref[0], DR, buff=0.12)
        p_own = VGroup(Dot([X(G["Alder"]), Y(AL["ratio"]), 0], radius=0.12, color=ALDER).set_z_index(5), VGroup(side("at Alder's own gamma", size=16, color=ALDER), big(f"{AL['ratio']:.2f}", size=26, color=ALDER)).arrange(RIGHT, buff=0.2))
        p_own[1].next_to(p_own[0], UL, buff=0.12)
        rising = big("one rising curve", size=28).move_to([SX + 0.1, 1.5, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(level), run_time=1.0)
            self.play(Create(curve), FadeIn(rising), run_time=1.5, rate_func=linear)
            seg.wait_until(seg.word(1, "With the slider at the reference"))
            self.play(FadeIn(p_ref), run_time=0.7)
            seg.wait_until(seg.word(1, "At Alder's own gamma"))
            self.play(FadeIn(p_own), run_time=0.7)

        (ga, gb), (ra, rb) = LINK["gamma_interval"], LINK["ratio_interval"]
        on_x = Line([X(ga), y0 + 0.08, 0], [X(gb), y0 + 0.08, 0], stroke_width=9, color=ACCENT).set_z_index(4)
        on_y = Line([x0 + 0.08, Y(ra), 0], [x0 + 0.08, Y(rb), 0], stroke_width=9, color=ACCENT).set_z_index(4)
        guides = VGroup(*[VGroup(DashedLine([X(g), y0, 0], [X(g), Y(r), 0], dash_length=0.08, stroke_width=2, color=ACCENT), DashedLine([X(g), Y(r), 0], [x0, Y(r), 0], dash_length=0.08, stroke_width=2, color=ACCENT)) for g, r in ((ga, ra), (gb, rb))])
        carried = VGroup(side("Episode 9's interval for Alder's gamma", size=17, color=PAPER), big(f"{minus(ga)} to {gb:.2f}", size=28, color=PAPER),
                         side("becomes an interval for its ratio", size=17, color=PAPER), big(f"{ra:.2f} to {rb:.2f}", size=34, color=ACCENT)).arrange(DOWN, buff=0.16)
        carried = fit_width(carried, 4.7).move_to([SX + 0.1, -0.2, 0])
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(p_ref[1], p_own[1])), run_time=0.5)
            seg.wait_until(seg.word(0, "Episode 9's interval"))
            self.play(Create(on_x), FadeIn(carried[0]), FadeIn(carried[1]), run_time=0.9)
            self.play(LaggedStart(*[Create(g_) for pair in guides for g_ in pair], lag_ratio=0.3), run_time=1.6)
            self.play(Create(on_y), FadeIn(carried[2]), FadeIn(carried[3]), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Cautions(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Two cautions")
        R = Ruler(0.9, 0.0, 2.1, x0=-4.6, x1=4.6, ticks=[0, 0.5, 1, 1.5, 2], labels={v: f"{v:g}" for v in (0, 0.5, 1, 1.5, 2)}, title="ratio")
        one = VGroup(Line(R.P(1.0, -0.05), R.P(1.0, 1.0), stroke_width=4, color=CEDAR), big("like the reference clinic", size=26, color=CEDAR).move_to(R.P(1.0, 1.35)))
        grade = VGroup(big("1", size=30, color=CEDAR), side("is not a grade", size=22, color=PAPER)).arrange(RIGHT, buff=0.2).move_to([0, -0.35, 0])
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(R.g), run_time=1.0)
            seg.wait_until(seg.s(0) + 1.4)
            self.play(Create(one[0]), FadeIn(one[1]), run_time=0.9)
            seg.wait_until(seg.word(0, "It does not mean good"))
            self.play(FadeIn(grade), run_time=0.7)

        a1 = Dot(R.P(RATIO["Alder"]), radius=0.14, color=ALDER).set_z_index(5)
        a2 = Circle(radius=0.14, stroke_color=ALDER, stroke_width=4).move_to(R.P(MEAN["ratio"]["Alder"])).set_z_index(5)
        two = VGroup(VGroup(Dot(radius=0.11, color=ALDER), big(f"{RATIO['Alder']:.2f}", size=28, color=ALDER), side("Alder, against the middle clinic", size=19, color=PAPER)).arrange(RIGHT, buff=0.25),
                     VGroup(Circle(radius=0.11, stroke_color=ALDER, stroke_width=3.5), big(f"{MEAN['ratio']['Alder']:.2f}", size=28, color=ALDER), side("Alder, against a size-weighted average", size=19, color=PAPER)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([0, -1.7, 0])
        say = side("say which reference, every time", size=20, color=ACCENT).move_to([0, -2.75, 0])
        with self.nar("s8_2") as seg:
            self.play(FadeOut(grade), FadeIn(a1), FadeIn(two[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "Against that"))
            self.play(FadeIn(a2), FadeIn(two[1]), run_time=0.8)
            self.play(FadeIn(say), run_time=0.6)

        x0, x1, lo, hi, y_ax = -5.4, 5.4, 0.3, 2.1, -1.6
        X = lambda r: x0 + (x1 - x0) * (r - lo) / (hi - lo)
        axis = VGroup(Line([x0, y_ax, 0], [x1, y_ax, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y_ax, 0], [X(v), y_ax - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 16, MUTED).move_to([X(v), y_ax - 0.3, 0])) for v in (0.5, 1, 1.5, 2)],
                      side("ratio", size=17).move_to([0, y_ax - 0.64, 0]))
        width, stack, dots = 0.05, {}, VGroup()
        for r in CROWD["ratios"]:
            b = int(np.floor((r - lo) / width))
            k = stack.get(b, 0); stack[b] = k + 1
            dots.add(Dot([X(lo + (b + 0.5) * width), y_ax + 0.16 + 0.125 * k, 0], radius=0.052, color=PAPER).set_opacity(0.8))
        ref = VGroup(DashedLine([X(1), y_ax, 0], [X(1), 2.0, 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), txt("the reference", 16, CEDAR, weight=SEMIBOLD).move_to([X(1), 2.25, 0]))
        ends = VGroup(big(f"{CROWD['min']:.2f}", size=24, color=ACCENT).move_to([X(CROWD["min"]), y_ax + 0.75, 0]), big(f"{CROWD['max']:.2f}", size=24, color=ACCENT).move_to([X(CROWD["max"]), y_ax + 0.75, 0]))
        halves = VGroup(side(f"{len(CROWD['ratios']) - CROWD['above']} below", size=18, color=PAPER).move_to([X(1) - 1.3, 1.75, 0]), side(f"{CROWD['above']} above", size=18, color=PAPER).move_to([X(1) + 1.3, 1.75, 0]))
        luck = big("real differences, or luck?", size=28, color=ACCENT).move_to([3.4, 2.75, 0])
        with self.nar("s8_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in (R.g, one, a1, a2, two, say)], run_time=0.6)
            self.play(FadeIn(axis), FadeIn(ref), FadeIn(dots, lag_ratio=0.01), run_time=1.8)
            self.play(FadeIn(ends), FadeIn(halves), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(luck, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(mini_curve(CEDAR), txt("reference", 15, CEDAR, weight=SEMIBOLD)).arrange(DOWN, buff=0.1)
        c_up, c_dn = mini_curve(ALDER, shift=-0.12), mini_curve(CEDAR, shift=0.12)
        icon2 = VGroup(c_up, c_dn, Arrow([-0.05, 0.3, 0], [-0.05, -0.22, 0], buff=0, stroke_width=4, color=PAPER, max_tip_length_to_length_ratio=0.35))
        icon3 = VGroup(big(f"{AL['ratio']:.2f}", size=30, color=ALDER), pill("against the middle clinic", 16)).arrange(DOWN, buff=0.15)
        icons = [icon1, icon2, icon3]
        caps = [["The reference is", "the middle clinic's curve"], ["Keep the patients, swap in", "that curve, and count:", "observed over expected"], ["Name the reference", "with every ratio"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.9, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        def picture(curves, chip_colors, caption, x):
            c = card(4.4, 2.9).move_to([x, 0.55, 0])
            cs = VGroup(*curves).move_to(c.get_center() + UP * 0.45)
            ch = VGroup(*[chip(col, k % 2 == 0, 0.12) for k, col in enumerate(chip_colors)]).arrange(RIGHT, buff=0.12).move_to(c.get_center() + DOWN * 0.6)
            return VGroup(c, cs, ch, txt(caption, 18, PAPER).move_to(c.get_center() + DOWN * 1.1))

        this = picture([mini_curve(ALDER, shift=-0.12).set_stroke(opacity=0.35), mini_curve(CEDAR, shift=0.12)], [ALDER] * 6, "same patients, new curve", -3.3)
        nxt_p = picture([mini_curve(ALDER)], [ALDER, BIRCH, CEDAR, DUNE, ELM, BIRCH], "same curve, new patients", 3.3)
        labels = VGroup(side("this time", size=18).next_to(this, UP, buff=0.2), txt("Next:", 22, MUTED).next_to(nxt_p, UP, buff=0.2))
        nxt = big("swap the patients", size=34).move_to([3.3, -1.75, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(this), FadeIn(labels[0]), run_time=1.0)
            seg.wait_until(seg.word(0, "Next time"))
            self.play(FadeIn(nxt_p), FadeIn(labels[1]), run_time=1.0)
            self.play(FadeIn(nxt, shift=UP * 0.1), run_time=0.7)
        end_card(self, "s9_3", 12, "Swap the Patients")
