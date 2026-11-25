"""Model in Motion · The Logistic Fixed-Effect Model · Episode 6: Fitting by Balance (how the dial and the sliders find their places).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode06.py S05_Moves      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Positions come from e06_numbers.json, written by e06_numbers.py. The machine's readings (expected counts, observed
minus expected, height) are computed live by mim.meters.FitMachine from the slider and dial positions.
All content stays above y = -3.0 so that burned-in captions never cover it.
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

N = json.loads((ROOT / "e06_numbers.json").read_text())
ST, DU, DI, FIT, HILL = N["start"], N["dune"], N["dial"], N["fit"], N["hill"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
G0 = {n: ST["gamma"] for n in ORDER}                    # the plain guess: every clinic at the overall rate
GF = {**FIT["gamma"], "Elm": -3.2}                      # the fit; Elm has no fitted value, so its slider is parked at the foot of its track
CAP = [-2.4, -2.72, 0]                                  # where one-line captions under the machine sit


def minus(v, places=1):
    return f"{v:.{places}f}".replace("-", "\u2212")


def box_around(m):
    return SurroundingRectangle(m, color=PAPER, buff=0.1, stroke_width=2, corner_radius=0.08).set_z_index(7)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        P = LinePanel()
        b0, g0 = 1.2, {"Alder": -1.5, "Birch": -1.0, "Cedar": -0.7, "Dune": -2.0}        # the unfitted position Episode 4 drifted in from
        b = ValueTracker(b0)
        g = {n: ValueTracker(g0[n]) for n in FOUR}
        lines = {n: always_redraw(lambda n=n: P.line(g[n].get_value(), b.get_value(), COL[n])) for n in FOUR}
        dial, blab, sl, glab = controls(b0, {**g0, "Elm": -3.2})
        dial.add_updater(lambda m: m.turn_to(b.get_value()))
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(g[n].get_value()))
        with self.nar("s1_1") as seg:
            self.play(FadeIn(P.g), FadeIn(dial), FadeIn(blab), FadeIn(glab), *[FadeIn(x) for x in sl.values()], run_time=1.0)
            self.add(*lines.values())
            self.play(b.animate.set_value(FIT["beta"]), *[g[n].animate.set_value(FIT["gamma"][n]) for n in FOUR], run_time=2.6)

        data = VGroup(big(f"{N['patients']} patients", size=30), side("and who came back", color=PAPER)).arrange(DOWN, buff=0.14).move_to([SX, -0.6, 0])
        with self.nar("s1_2") as seg:
            seg.wait_until(seg.word(0, "All they had"))
            self.play(FadeIn(data, shift=UP * 0.1), run_time=0.9)

        q = VGroup(big("What makes one setting", size=26), big("better than another?", size=26)).arrange(DOWN, buff=0.12).move_to([SX, -2.0, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.9)
        for m in [dial, *sl.values(), *lines.values()]:
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 6, "Fitting by Balance", "how the dial and the sliders find their places")


# =================================================================================== S03
class S03_Score(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Scoring a guess")
        xs = {"Alder": -5.6, "Birch": -3.95, "Cedar": -2.3, "Dune": -0.65, "Elm": 1.0}
        heads, trays = VGroup(), {}
        for n in ORDER:
            heads.add(txt(n, 20, COL[n], weight=SEMIBOLD).move_to([xs[n], 2.55, 0]))
            trays[n] = VGroup(*[Unit(COL[n], p["event"], p["high"], r=0.085).move_to([xs[n] + (j % 6 - 2.5) * 0.24, 2.05 - (j // 6) * 0.25, 0])
                                for j, p in enumerate(patients(n))])
        p0, n1, n0 = ST["rate"], N["events"], N["patients"] - N["events"]
        RX = 4.7
        plain = VGroup(side("the plain guess, for every patient", size=19, color=PAPER), big(pct(p0), size=38, color=ACCENT)).arrange(DOWN, buff=0.14).move_to([RX, 2.0, 0])
        ex1 = VGroup(chip(PAPER, True, 0.15), side("readmitted:", size=19, color=PAPER), big(pct(p0), size=28)).arrange(RIGHT, buff=0.22).move_to([RX, 0.95, 0])
        ex2 = VGroup(chip(PAPER, False, 0.15), side("not readmitted:", size=19, color=PAPER), big(pct(1 - p0), size=28)).arrange(RIGHT, buff=0.22).move_to([RX, 0.3, 0])
        prod = MathTex(rf"{p0:.2f}^{{{n1}}}", r"\times", rf"{1 - p0:.2f}^{{{n0}}}", font_size=40, color=PAPER).move_to([RX, -0.55, 0])
        tiny = MathTex(r"\approx", rf"{ST['likelihood_mantissa']:.0f}\times 10^{{{ST['likelihood_exponent']}}}", font_size=36, color=PAPER).move_to([RX, -1.2, 0])
        indep = side("treating the outcomes as independent", size=15).move_to([RX, -1.65, 0])
        logv = VGroup(side("its logarithm", color=PAPER), big(minus(ST["loglik"]), size=40, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([RX, -2.3, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads), LaggedStart(*[FadeIn(t) for t in trays.values()], lag_ratio=0.15), run_time=1.6)
            seg.wait_until(seg.word(0, "gets the overall rate"))
            self.play(FadeIn(plain, shift=UP * 0.1), run_time=0.9)

        yes, no = trays["Cedar"][0], trays["Cedar"][2]          # one readmitted patient and one who was not
        with self.nar("s3_2") as seg:
            seg.wait_until(seg.s(1))
            self.play(Indicate(yes, color=PAPER, scale_factor=2.2), FadeIn(ex1, shift=LEFT * 0.1), run_time=1.0)
            seg.wait_until(seg.word(1, "For one who"))
            self.play(Indicate(no, color=PAPER, scale_factor=2.2), FadeIn(ex2, shift=LEFT * 0.1), run_time=1.0)

        with self.nar("s3_3") as seg:
            seg.wait_until(seg.word(0, "Multiply"))
            self.play(Write(prod), FadeIn(indep), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(tiny, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "So we take"))
            self.play(FadeIn(logv, shift=UP * 0.1), run_time=0.9)

        hb = HeightBar(-70.5, -55.0, length=3.4).move_to([6.2, 0.35, 0])
        hb.level_to(ST["loglik"])
        hv = big(minus(ST["loglik"], 2), size=22).move_to([5.35, hb.Y(ST["loglik"]), 0])
        up = Arrow([6.75, -0.9, 0], [6.75, 1.7, 0], buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.1)
        better = VGroup(side("a better guess", color=PAPER), side("stands higher", color=PAPER)).arrange(DOWN, buff=0.08).move_to([4.1, 1.1, 0])
        only = VGroup(side("only the climb matters,", size=18), side("not the height itself", size=18)).arrange(DOWN, buff=0.08).move_to([4.1, 0.0, 0])
        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeOut(VGroup(plain, ex1, ex2, prod, tiny, indep)), run_time=0.6)
            self.play(FadeIn(hb), FadeIn(hv), GrowArrow(up), FadeIn(better), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(only), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Meters(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Which way is up?")
        M = FitMachine(G0, 0.0)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(M.heightcol), run_time=0.8)
            seg.wait_until(seg.word(0, "Bring back the meter"))
            self.play(LaggedStart(*[FadeIn(M.col[n], shift=UP * 0.1) for n in ORDER], lag_ratio=0.12), FadeIn(M.dialcol), run_time=1.8)

        with self.nar("s4_2") as seg:
            for n, cue in (("Dune", "Dune expected"), ("Birch", "Birch expected"), ("Elm", "Elm expected")):
                seg.wait_until(seg.word(0, cue))
                bx = box_around(VGroup(*M.col[n][3:]))
                self.play(Create(bx), run_time=0.6)
                self.wait(1.2)
                self.play(FadeOut(bx), run_time=0.4)

        arrows = VGroup()
        for n in ORDER:
            x = M.XS[n] + 0.4
            lo, hi = np.array([x, 1.25, 0.0]), np.array([x, 1.95, 0.0])
            a, b = (lo, hi) if ST["o_minus_e"][n] > 0 else (hi, lo)
            arrows.add(Arrow(a, b, buff=0, stroke_width=4, color=PAPER, max_tip_length_to_length_ratio=0.3))
        cap = side("each meter's tilt is the slope of the height in that clinic's gamma", size=18, color=PAPER).move_to(CAP)
        with self.nar("s4_3", gap=0.8) as seg:
            seg.wait_until(seg.s(1))
            self.play(FadeIn(cap), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.12), run_time=1.4)
        M.clear()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Moves(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "One at a time?")
        M = FitMachine(G0, 0.0)
        self.play(FadeIn(tag), FadeIn(M.all), run_time=1.0)
        with self.nar("s5_1") as seg:
            seg.wait_until(seg.word(0, "Push its slider up"))
            self.play(M.g["Dune"].animate.set_value(DU["level_gamma"]), run_time=3.0)

        with self.nar("s5_2") as seg:
            bx = box_around(VGroup(*M.col["Dune"][3:]))
            self.play(Create(bx), run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(M.g["Dune"].animate.set_value(DU["overshoot_gamma"]), FadeOut(bx), run_time=1.6)
            self.wait(1.2)
            self.play(M.g["Dune"].animate.set_value(DU["level_gamma"]), run_time=1.0)

        bb = box_around(VGroup(M.bnote, M.bmeter, M.bdiff, M.bobs, M.bexp))
        with self.nar("s5_3") as seg:
            self.play(M.g["Dune"].animate.set_value(ST["gamma"]), run_time=0.9)           # back to the plain guess
            seg.wait_until(seg.word(0, "It weighs only"))
            self.play(Create(bb), run_time=0.7)

        boxes = [box_around(VGroup(M.meter[n], M.diff[n])) for n in FOUR]
        with self.nar("s5_4") as seg:
            self.play(M.b.animate.set_value(DI["beta"]), FadeOut(bb), run_time=2.6)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[Create(x) for x in boxes], lag_ratio=0.15), run_time=1.2)

        cap = side("nothing settles one piece at a time", size=20, color=PAPER).move_to(CAP)
        with self.nar("s5_5", gap=0.8) as seg:
            self.play(*[FadeOut(x) for x in boxes], FadeIn(cap), run_time=0.8)
        M.clear()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Level(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Level everything")
        M = FitMachine(G0, 0.0)
        self.play(FadeIn(tag), FadeIn(M.all), run_time=1.0)
        with self.nar("s6_1") as seg:
            self.play(M.b.animate.set_value(FIT["beta"]), *[M.g[n].animate.set_value(GF[n]) for n in ORDER], run_time=3.2)

        boxes = [box_around(VGroup(M.col[n][5], M.expd[n])) for n in FOUR]
        bal = big("fitting is balancing", size=26, color=ACCENT).move_to(CAP)
        with self.nar("s6_2") as seg:
            seg.wait_until(seg.word(0, "expected now equals observed"))
            self.play(LaggedStart(*[Create(x) for x in boxes], lag_ratio=0.2), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(*[FadeOut(x) for x in boxes], FadeIn(bal), run_time=0.8)

        a0, a1 = FIT["alder_split"]
        o0, o1 = CLINICS["Alder"]["low"][1], CLINICS["Alder"]["high"][1]
        note = side(f"Alder: {a0:.1f} + {a1:.1f} expected, {o0} + {o1} observed, {o0 + o1} either way", size=18, color=PAPER).move_to(CAP)
        with self.nar("s6_3") as seg:
            self.play(FadeOut(bal), run_time=0.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(note), run_time=0.8)

        eb = box_around(VGroup(M.meter["Elm"], M.diff["Elm"], M.col["Elm"][5], M.expd["Elm"]))
        foot = M.sl["Elm"].track.get_bottom()
        off = Arrow(foot + RIGHT * 0.3 + UP * 0.3, foot + RIGHT * 0.3 + DOWN * 0.15, buff=0, stroke_width=4, color=ELM, max_tip_length_to_length_ratio=0.45).set_z_index(6)
        with self.nar("s6_4") as seg:
            self.play(FadeOut(note), Create(eb), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(M.g["Elm"].animate.set_value(-6.0), GrowArrow(off), run_time=3.4)

        climb = VGroup(side("the height:", color=PAPER), big(minus(ST["loglik"]), size=26, color=MUTED),
                       Arrow(ORIGIN, RIGHT * 0.8, buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.3),
                       big(minus(FIT["loglik"]), size=28, color=ACCENT)).arrange(RIGHT, buff=0.25).move_to(CAP)
        with self.nar("s6_5", gap=0.8) as seg:
            self.play(FadeOut(eb), FadeIn(climb), run_time=0.8)
        M.clear()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
def hill_chart(x0, x1, y0, y1, b_hi=4.0, h_lo=-63.5, h_hi=-55.0):
    """The profile of the height over the dial position, from the numbers file. Returns (X, Y, axes, curve)."""
    X = lambda bv: x0 + (x1 - x0) * bv / b_hi
    Y = lambda hv: y0 + (y1 - y0) * (hv - h_lo) / (h_hi - h_lo)
    axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
    pts = [np.array([X(bv), Y(hv), 0.0]) for bv, hv in HILL["profile"] if bv <= b_hi]
    curve = VMobject(color=PAPER, stroke_width=4.5).set_points_smoothly(pts)
    return X, Y, axes, curve


class S07_Hill(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "The hill")
        x0, x1, y0, y1 = -5.4, 1.6, -2.0, 2.4
        X, Y, axes, curve = hill_chart(x0, x1, y0, y1)
        xt = VGroup(*[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 17, MUTED).move_to([X(v), y0 - 0.32, 0])) for v in range(5)])
        yt = VGroup(*[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(minus(v, 0), 17, MUTED).move_to([x0 - 0.5, Y(v), 0])) for v in (-62, -60, -58, -56)])
        xl = side("position of the dial", size=18).move_to([(x0 + x1) / 2, y0 - 0.68, 0])
        yl = side("height", size=18).move_to([x0, y1 + 0.28, 0])
        tracer = Dot(curve.get_start(), radius=0.09, color=ACCENT).set_z_index(5)
        pb, ph, qb, qh = HILL["peak_beta"], HILL["peak"], HILL["pooled_beta"], HILL["pooled"]
        peak = Dot([X(pb), Y(ph), 0], radius=0.11, color=ACCENT).set_z_index(5)
        peak_l = big(f"{pb:.2f}", size=28, color=ACCENT).next_to(peak, UP, buff=0.2)
        pool = Dot([X(qb), Y(qh), 0], radius=0.09, color=MUTED).set_z_index(4)
        pool_l = side(f"the pooled step, {qb:.2f}", size=18, color=PAPER).move_to([X(qb) - 1.7, Y(qh) - 1.0, 0])
        lead = Line(pool_l.get_corner(UR) + UP * 0.05, pool.get_center() + DL * 0.1, stroke_width=1.5, color=MUTED)
        near = [bv for bv, hv in HILL["profile"] if hv >= ph - 0.5]              # dial positions within half a unit of the top
        arc = ArcBetweenPoints(np.array([X(min(near)), Y(ph) + 0.75, 0.0]), np.array([X(max(near)), Y(ph) + 0.75, 0.0]), angle=-PI / 3, color=ACCENT, stroke_width=3)
        gentle = side("a gently rounded top", size=19, color=ACCENT).next_to(arc, UP, buff=0.12)
        how = VGroup(side("for each dial position:", size=18, color=PAPER), side("level the clinics' meters,", size=18, color=PAPER),
                     side("record the height", size=18, color=PAPER)).arrange(DOWN, buff=0.1).move_to([4.6, 0.9, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(yl), FadeIn(how), run_time=1.0)
            self.add(tracer)
            self.play(Create(curve), MoveAlongPath(tracer, curve), run_time=3.2, rate_func=linear)
            self.play(FadeOut(tracer), run_time=0.3)

        with self.nar("s7_2") as seg:
            seg.wait_until(seg.word(0, "with one top"))
            self.play(GrowFromCenter(peak), FadeIn(peak_l), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(pool), Create(lead), FadeIn(pool_l), run_time=0.9)

        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeOut(peak_l), Create(arc), FadeIn(gentle), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(chip(PAPER, True, 0.14), tex("p", 34), chip(PAPER, False, 0.14), tex("1-p", 34)).arrange(RIGHT, buff=0.22)
        tilted = Meter(DUNE)
        tilted.tilt_to(ST["o_minus_e"]["Dune"])
        icon2 = VGroup(tilted, Arrow(DOWN * 0.3, UP * 0.3, buff=0, stroke_width=4, color=PAPER, max_tip_length_to_length_ratio=0.35).next_to(tilted, RIGHT, buff=0.35))
        level = Meter(CEDAR)
        level.tilt_to(0.0)
        icon3 = VGroup(level, tick_mark().next_to(level, RIGHT, buff=0.35))
        icons = [icon1, icon2, icon3]
        caps = [["A guess is scored", "by the probability it gave", "to what happened"], ["Observed minus expected says", "which way each slider moves"],
                ["At the best fit, every meter", "that can level is level"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        warn = VGroup(big("Level meters do not show that the model is right", size=30),
                      side("any model with a number for each clinic will level them", size=22),
                      side("whether it is right is judged inside the clinics, later", size=22)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        with self.nar("s8_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(warn[0], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(warn[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "Whether it is right"))
            self.play(FadeIn(warn[2]), run_time=0.7)

        X, Y, axes, curve = hill_chart(-5.4, 1.6, -2.0, 2.4)
        top = Dot([X(HILL["peak_beta"]), Y(HILL["peak"]), 0], radius=0.11, color=ACCENT).set_z_index(5)
        startp = np.array([X(0.0), Y(HILL["at_zero"]), 0.0])
        climber = Dot(startp, radius=0.1, color=PAPER).set_z_index(5)
        qm = big("?", size=40, color=ACCENT).next_to(climber, UR, buff=0.15)
        nxt = VGroup(txt("Next:", 26, MUTED), big("climbing the hill", size=34)).arrange(DOWN, buff=0.2).move_to([4.6, -0.4, 0])
        with self.nar("s8_3") as seg:
            self.play(FadeOut(warn), run_time=0.6)
            self.play(FadeIn(axes), Create(curve), GrowFromCenter(top), run_time=1.4)
            seg.wait_until(seg.word(0, "not how to get there"))
            self.play(GrowFromCenter(climber), FadeIn(qm), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s8_4", 7, "Climbing the hill")
