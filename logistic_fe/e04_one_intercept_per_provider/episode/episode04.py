"""Model in Motion · The Logistic Fixed-Effect Model · Episode 4: One Intercept per Provider (the model, as parallel lines).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode04.py S05_Fit      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e04_numbers.json, written by e04_numbers.py; none is typed here.
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

N = json.loads((ROOT / "e04_numbers.json").read_text())
FIT, BETA, POOL, OBS = N["fit"]["clinics"], N["fit"]["beta"], N["pooled"], N["observed"]
G = {n: FIT[n]["gamma"] for n in FOUR}
ODDS, OWN, SEP, CROWD = N["fit"]["odds_ratio"], N["within_clinic_steps"], N["separate_lines"], N["crowd"]
GAP = N["next_episode"]["alder_minus_cedar"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.6                                    # centre of the right-hand strip (dial, sliders, notes)


def side(s, x=0.0, y=0.0, size=21, color=MUTED):
    return txt(s, size, color, font=SERIF, slant=ITALIC).move_to([x, y, 0])


def big(s, x=0.0, y=0.0, size=32, color=PAPER):
    return txt(s, size, color, weight=SEMIBOLD, font=DISPLAY).move_to([x, y, 0])


def fit_width(m, w):
    if m.width > w:
        m.scale_to_fit_width(w)
    return m


def legend(y=1.5):
    rows = VGroup(*[VGroup(Dot(radius=0.09, color=COL[n]), txt(n, 20, PAPER)).arrange(RIGHT, buff=0.2) for n in ORDER])
    rows.arrange(DOWN, buff=0.17, aligned_edge=LEFT).move_to([SX - 0.5, y, 0])
    note = txt("dot area = number of patients", 16, MUTED, font=SERIF, slant=ITALIC).next_to(rows, DOWN, buff=0.3, aligned_edge=LEFT)
    return VGroup(rows, note)


def controls(beta, gammas):
    """The machine, in the top band of the right strip: one beta dial and one gamma slider per clinic."""
    dial = Dial(beta).move_to([3.15, 1.75, 0])
    dial.turn_to(beta)
    blab = tex(r"\beta", 36, ACCENT).next_to(dial, UP, buff=0.22)
    sl = {}
    for k, n in enumerate(ORDER):
        sl[n] = Slider(n, gammas[n]).move_to([4.1 + 0.65 * k, 1.62, 0])
        sl[n].slide_to(gammas[n])
    glab = tex(r"\gamma", 36, PAPER).move_to([5.4, 3.05, 0])
    return dial, blab, sl, glab


def value_tag(slider, text, color=PAPER):
    return txt(text, 14, color).next_to(slider.track, UP, buff=0.12)


def start_ring(P, n):
    return Circle(radius=0.09, stroke_color=COL[n], stroke_width=3).set_fill(INK, opacity=1).move_to(P.P(0, G[n])).set_z_index(5)


def dim_bracket(P, t, v0, v1, dx, label):
    """A dimension line beside panel position t, from height v0 to v1, with leaders back to the exact position."""
    x = P.X(t) + dx
    a, b = np.array([x, P.Y(v0), 0.0]), np.array([x, P.Y(v1), 0.0])
    arr = DoubleArrow(a, b, buff=0, stroke_width=3, color=ACCENT, tip_length=0.12)
    lead = VGroup(*[DashedLine(P.P(t, v), np.array([x, P.Y(v), 0.0]), dash_length=0.05, stroke_width=1.5, color=ACCENT) for v in (v0, v1)])
    lab = txt(label, 22, ACCENT, weight=SEMIBOLD).next_to(arr, LEFT if dx < 0 else RIGHT, buff=0.12)
    lab.add_background_rectangle(color=INK, opacity=0.85, buff=0.05)
    return VGroup(lead, arr, lab).set_z_index(6)


def tick_mark(color=GOOD, s=1.0):
    return VGroup(Line([-0.14 * s, 0, 0], [-0.04 * s, -0.12 * s, 0], stroke_width=5, color=color),
                  Line([-0.04 * s, -0.12 * s, 0], [0.16 * s, 0.14 * s, 0], stroke_width=5, color=color))


def clear(scene, keep=()):
    return [FadeOut(m) for m in scene.mobjects if m not in keep]


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        P = LinePanel()
        a, step = POOL["start"], POOL["step"]
        pooled = P.line(a, step, MUTED, dashed=True)
        pdots = VGroup(*[Circle(radius=0.1, stroke_color=MUTED, stroke_width=3).set_fill(INK, opacity=1).move_to(P.P(t, a + step * t)).set_z_index(5)
                         for t in (0, 1)])
        plab = side("the pooled standard").move_to(P.P(0.5, a + 0.5 * step) + UP * 0.8 + LEFT * 0.9)
        l_low = txt(pct(POOL["rate_low"]), 22, MUTED, weight=SEMIBOLD).next_to(pdots[0], LEFT, buff=0.3)
        l_high = txt(pct(POOL["rate_high"]), 22, MUTED, weight=SEMIBOLD).next_to(pdots[1], UL, buff=0.1)
        D, elm, leg = P.dots(), P.elm_marker(), legend()
        off = {"Alder": -0.05, "Dune": 0.05, "Birch": -0.05, "Cedar": 0.05}     # ticks only: a vertical tick keeps its length when moved sideways
        ticks = {}
        for n in FOUR:
            for high in (False, True):
                t, v = (1 if high else 0), observed(n, high)[2]
                ticks[(n, high)] = Line(P.P(t, a + step * t) + RIGHT * off[n], P.P(t, v) + RIGHT * off[n], stroke_width=3, color=COL[n]).set_z_index(2)

        def show(names):
            return ([FadeIn(D[(n, h)], scale=0.6) for n in names for h in (False, True)]
                    + [Create(ticks[(n, h)]) for n in names for h in (False, True)])

        with self.nar("s1_1") as seg:
            self.play(FadeIn(P.g), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Create(pooled), FadeIn(pdots), FadeIn(plab), run_time=1.4)
            seg.wait_until(seg.word(1, "lower-risk patients start"))
            self.play(FadeIn(l_low, shift=RIGHT * 0.1), Indicate(pdots[0], color=PAPER, scale_factor=1.5), run_time=0.8)
            seg.wait_until(seg.word(1, "one step up"))
            self.play(FadeIn(l_high, shift=LEFT * 0.1), Indicate(pdots[1], color=PAPER, scale_factor=1.5), run_time=0.8)

        with self.nar("s1_2") as seg:
            self.play(FadeIn(leg), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(*show(["Alder"]), run_time=1.0)
            seg.wait_until(seg.word(1, "So do Dune"))
            self.play(*show(["Dune"]), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(*show(["Birch", "Cedar"]), run_time=1.1)
            seg.wait_until(seg.word(2, "And Elm"))
            self.play(FadeIn(elm, shift=DOWN * 0.15), run_time=0.9)

        q = VGroup(big("What is the smallest", size=30), big("change that fixes it?", size=30)).arrange(DOWN, buff=0.14).move_to([SX, -1.45, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(*[Indicate(t, color=PAPER, scale_factor=1.2) for t in ticks.values()], run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(q, shift=UP * 0.15), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        mark = logo_mark(1.25)
        word = wordmark(64)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.55).move_to(UP * 1.15)
        arc = txt("THE LOGISTIC FIXED-EFFECT MODEL  \u00b7  EPISODE 4", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.75)
        title = txt("One Intercept per Provider", 66, PAPER, weight=SEMIBOLD, font=DISPLAY).next_to(arc, DOWN, buff=0.32)
        sub = txt("the model, as parallel lines", 30, MUTED, font=SERIF, slant=ITALIC).next_to(title, DOWN, buff=0.26)
        a, dot, b, ring, scan = mark
        with self.nar("s2_1", gap=0.6) as seg:
            self.play(Create(a), Create(b), run_time=0.8)
            self.play(GrowFromCenter(dot), GrowFromCenter(ring), FadeIn(scan, shift=RIGHT * 0.6), Write(word), run_time=1.3)
            seg.wait_until(seg.s(1) - 0.2)
            self.play(LaggedStart(FadeIn(arc, shift=UP * 0.15), FadeIn(title, shift=UP * 0.2),
                                  FadeIn(sub, shift=UP * 0.15), lag_ratio=0.25), run_time=1.6)
        self.wait(0.8)
        self.play(*clear(self), run_time=0.9)


# =================================================================================== S03
class S03_OwnLines(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "What should clinics share?")
        P = LinePanel()
        D = P.dots()
        dots, elm, leg = VGroup(*D.values()), P.elm_marker(), legend()
        own = {n: P.line(OBS[n]["logodds_low"], OBS[n]["own_step"], COL[n], dashed=(n == "Dune")) for n in FOUR}
        own["Dune"].set_z_index(3.5)                      # Alder's and Dune's own lines coincide: Dune's is dashed over Alder's
        ep2 = side("as in Episode 2", size=17).next_to(leg[0][2], RIGHT, buff=0.25)
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(dots), FadeIn(elm), FadeIn(leg), run_time=1.0)

        with self.nar("s3_1") as seg:
            seg.wait_until(seg.word(0, "a line of its own"))
            self.play(LaggedStart(Create(own["Alder"]), Create(own["Dune"]), Create(own["Birch"]), Create(own["Cedar"]), lag_ratio=0.35), run_time=2.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ep2), Indicate(own["Cedar"], color=PAPER, scale_factor=1.03), run_time=1.0)

        six = side(f"{OBS['Alder']['n_high']} patients", size=19, color=PAPER).next_to(D[("Alder", True)], UL, buff=0.12)
        bl = dim_bracket(P, 0, OBS["Cedar"]["logodds_low"], OBS["Alder"]["logodds_low"], -0.6, f"{SEP['alder_minus_cedar_low']:.2f}")
        bh = dim_bracket(P, 1, OBS["Cedar"]["logodds_high"], OBS["Alder"]["logodds_high"], 0.6, f"{SEP['alder_minus_cedar_high']:.2f}")
        with self.nar("s3_2") as seg:
            seg.wait_until(seg.word(1, "Alder's higher-risk end"))
            self.play(FadeIn(six), Indicate(D[("Alder", True)], color=PAPER, scale_factor=1.6), run_time=1.0)
            seg.wait_until(seg.s(2))
            self.play(FadeOut(six), FadeIn(bl), run_time=0.9)
            seg.wait_until(seg.word(2, "Alder sits further above"))
            self.play(FadeIn(bh), run_time=0.9)

        qm = big("?", P.X(0.5), P.Y(1.75), 54, ACCENT)
        kinds = VGroup(big(f"2, 4, 8, 16 \u2026 {2 ** 12:,}", size=26), side("kinds of patient, with twelve"),
                       side("yes-or-no risk factors")).arrange(DOWN, buff=0.14).move_to([SX, -1.5, 0])
        with self.nar("s3_3") as seg:
            self.play(FadeIn(qm, scale=1.4), run_time=0.8)
            seg.wait_until(seg.word(0, "With a dozen"))
            self.play(FadeIn(kinds, shift=UP * 0.1), run_time=1.0)

        par = {n: P.line(G[n], BETA, COL[n]) for n in FOUR}
        bet = VGroup(big("the bet", size=30, color=ACCENT), side("one step for everyone")).arrange(DOWN, buff=0.14).move_to([SX, -1.5, 0])
        starts = VGroup(*[start_ring(P, n) for n in FOUR])
        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeOut(bl), FadeOut(bh), FadeOut(qm), FadeOut(kinds), FadeOut(ep2), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(*[ReplacementTransform(own[n], par[n]) for n in ("Alder", "Birch", "Cedar")], FadeOut(own["Dune"]), FadeIn(par["Dune"]),
                      dots.animate.set_opacity(0.35), run_time=2.2)
            seg.wait_until(seg.word(1, "the same step"))
            self.play(FadeIn(bet, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(LaggedStart(*[GrowFromCenter(s) for s in starts], lag_ratio=0.2), run_time=1.2)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Model(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "The model")
        P = LinePanel()
        dots, elm = VGroup(*P.dots().values()).set_opacity(0.3), P.elm_marker().set_opacity(0.3)
        b = ValueTracker(BETA)
        g = {n: ValueTracker(G[n]) for n in FOUR}
        lines = {n: always_redraw(lambda n=n: P.line(g[n].get_value(), b.get_value(), COL[n])) for n in FOUR}
        dial, blab, sl, glab = controls(BETA, {**G, "Elm": -2.9})
        dial.add_updater(lambda m: m.turn_to(b.get_value()))
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(g[n].get_value()))
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(dots), FadeIn(elm), run_time=0.9)
        self.add(*lines.values())

        with self.nar("s4_1") as seg:
            self.play(FadeIn(dial, scale=0.8), FadeIn(blab), run_time=1.0)
            seg.wait_until(seg.word(1, "Turn it"))
            for target, rt in ((1.1, 1.0), (2.8, 1.3), (BETA, 1.0)):
                self.play(b.animate.set_value(target), run_time=rt)

        with self.nar("s4_2") as seg:
            self.play(LaggedStart(*[FadeIn(sl[n], shift=UP * 0.1) for n in ORDER], lag_ratio=0.12), run_time=1.3)
            seg.wait_until(seg.word(0, "It moves that clinic"))
            for target, rt in ((0.25, 1.0), (-1.7, 1.3), (G["Alder"], 1.0)):
                self.play(g["Alder"].animate.set_value(target), run_time=rt)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(glab, shift=DOWN * 0.1), run_time=0.8)

        rings = {n: start_ring(P, n) for n in FOUR}
        ilab = txt("intercept", 22, PAPER, weight=SEMIBOLD).move_to(P.P(0, G["Birch"]) + LEFT * 0.85 + DOWN * 0.95)
        iarr = Arrow(ilab.get_corner(UR) + UP * 0.05, P.P(0, G["Birch"]) + DL * 0.12, buff=0.03, stroke_width=3, color=PAPER,
                     max_tip_length_to_length_ratio=0.2)
        with self.nar("s4_3") as seg:
            seg.wait_until(seg.word(0, "its intercept") - 0.3)
            self.play(GrowFromCenter(rings["Birch"]), FadeIn(ilab), GrowArrow(iarr), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[GrowFromCenter(rings[n]) for n in ("Cedar", "Alder", "Dune")], lag_ratio=0.2), run_time=1.0)
            seg.wait_until(seg.word(1, "one shared step"))
            self.play(Indicate(blab, color=ACCENT, scale_factor=1.5), run_time=0.9)

        w1 = MathTex(r"\text{a patient's log-odds}", "=", font_size=30, color=PAPER)
        w2 = MathTex(r"\gamma_{\text{clinic}}", "+", r"\beta", r"\times\,\text{higher-risk}", font_size=34, color=PAPER)
        w2[2].set_color(ACCENT)
        e1 = fit_width(VGroup(w1, w2).arrange(DOWN, buff=0.16, aligned_edge=LEFT), 4.3).move_to([SX, -0.3, 0])
        e2 = fit_width(MathTex(r"\operatorname{logit}(p_{ij})", "=", r"\gamma_i", "+", r"\beta", r"x_{ij}", font_size=38, color=PAPER), 4.3)
        e2.move_to([SX, -1.4, 0])
        e2[4].set_color(ACCENT)
        e3 = fit_width(MathTex(r"\gamma_i", "+", r"\beta_1 x_1 + \beta_2 x_2 + \beta_3 x_3", font_size=32, color=PAPER), 4.3).move_to([SX, -2.25, 0])
        e3[2].set_color(ACCENT)
        with self.nar("s4_4") as seg:
            self.play(FadeOut(ilab), FadeOut(iarr), run_time=0.5)
            self.play(Write(e1), run_time=1.6)
            seg.wait_until(seg.word(0, "plus beta"))
            self.play(Indicate(w2[2], color=ACCENT, scale_factor=1.4), FadeIn(e2, shift=UP * 0.1), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(e3, shift=UP * 0.1), run_time=1.0)

        name = VGroup(big("the logistic", size=30), big("fixed-effect model", size=30)).arrange(DOWN, buff=0.12).move_to([SX, -0.75, 0])
        f1 = fit_width(txt("fixed: each \u03b3 is its own unknown number", 17, MUTED), 4.4).move_to([SX, -1.65, 0])
        f2 = fit_width(txt("nothing assumed about how they are spread", 17, MUTED), 4.4).move_to([SX, -2.05, 0])
        with self.nar("s4_5", gap=0.8) as seg:
            self.play(FadeOut(e1), FadeOut(e2), FadeOut(e3), run_time=0.6)
            self.play(FadeIn(name, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(f1), run_time=0.8)
            seg.wait_until(seg.word(1, "We assume nothing"))
            self.play(FadeIn(f2), run_time=0.8)
        for m in [dial, *sl.values(), *lines.values()]:
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Fit(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Where the lines land")
        P = LinePanel()
        dots, elm = VGroup(*P.dots().values()), P.elm_marker()
        b0, g0 = 1.2, {"Alder": -1.5, "Birch": -1.0, "Cedar": -0.7, "Dune": -2.0}        # an unfitted position to drift in from
        b = ValueTracker(b0)
        g = {n: ValueTracker(g0[n]) for n in FOUR}
        gE = ValueTracker(-2.5)
        lines = {n: always_redraw(lambda n=n: P.line(g[n].get_value(), b.get_value(), COL[n])) for n in FOUR}
        elm_line = always_redraw(lambda: P.line(gE.get_value(), b.get_value(), ELM, dashed=True))
        dial, blab, sl, glab = controls(b0, {**g0, "Elm": -2.5})
        dial.add_updater(lambda m: m.turn_to(b.get_value()))
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(g[n].get_value()))
        sl["Elm"].add_updater(lambda m: m.slide_to(gE.get_value()))
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(dots), FadeIn(elm), FadeIn(dial), FadeIn(blab), FadeIn(glab),
                  *[FadeIn(s) for s in sl.values()], run_time=1.0)
        self.add(*lines.values())

        with self.nar("s5_1") as seg:
            seg.wait_until(seg.word(0, "For now"))
            self.play(b.animate.set_value(BETA), *[g[n].animate.set_value(G[n]) for n in FOUR], run_time=2.6)

        bval = big(f"{BETA:.2f}", size=26, color=ACCENT).next_to(dial, DOWN, buff=0.22)
        odds = txt(f"odds \u00d7 {ODDS:.1f}", 18, ACCENT).next_to(bval, DOWN, buff=0.1)
        with self.nar("s5_2") as seg:
            self.play(FadeIn(bval, shift=UP * 0.1), Indicate(blab, color=ACCENT, scale_factor=1.4), run_time=1.0)
            seg.wait_until(seg.word(1, "multiplies the odds"))
            self.play(FadeIn(odds), run_time=0.8)

        vals = {n: value_tag(sl[n], signed(G[n])) for n in FOUR}
        with self.nar("s5_3") as seg:
            for names, cue in ((["Birch"], "Birch is lowest"), (["Cedar"], "Then Cedar"), (["Alder", "Dune"], "Then Alder and Dune")):
                seg.wait_until(seg.word(0, cue))
                self.play(*[FadeIn(vals[n], shift=DOWN * 0.08) for n in names], *[Flash(sl[n].knob.get_center(), color=COL[n], flash_radius=0.2, line_length=0.1)
                                                                               for n in names], run_time=0.9)

        none = value_tag(sl["Elm"], "none", ELM)
        note = fit_width(txt("no readmissions, so no finite \u03b3", 17, ELM), 4.3).move_to([SX, -0.7, 0])
        with self.nar("s5_4") as seg:
            self.add(elm_line)
            self.play(gE.animate.set_value(-6.6), run_time=3.2, rate_func=rush_into)
            self.play(FadeIn(none), FadeIn(note), run_time=0.8)

        C = CurvePanel(BETA)
        curves = VGroup(*[C.curve(G[n], COL[n]) for n in FOUR])
        marks = {(n, h): C.marker(G[n], h, COL[n]) for n in FOUR for h in (False, True)}
        slide = DoubleArrow(C.P(-G["Alder"], 0.5), C.P(-G["Birch"], 0.5), buff=0, stroke_width=3, color=PAPER, tip_length=0.12).set_z_index(6)
        slab = side("one shape, slid sideways", size=18, color=PAPER).move_to(C.P(-G["Birch"], 0.5) + RIGHT * 1.65 + DOWN * 0.45)

        def plab(n, h, d):
            return txt(pct(FIT[n]["p_high" if h else "p_low"]), 22, COL[n], weight=SEMIBOLD).next_to(marks[(n, h)], d, buff=0.1)

        labs = {(n, h): plab(n, h, DR if n == "Birch" else UL) for n in ("Birch", "Alder") for h in (False, True)}
        with self.nar("s5_5") as seg:
            for ln in [*lines.values(), elm_line]:
                ln.clear_updaters()
            self.remove(elm_line)
            self.play(FadeOut(P.g), FadeOut(dots), FadeOut(elm), FadeOut(note), *[FadeOut(ln) for ln in lines.values()], run_time=0.9)
            self.play(FadeIn(C.g), LaggedStart(*[Create(c) for c in curves], lag_ratio=0.15), run_time=1.8)
            self.play(*[GrowFromCenter(m) for m in marks.values()], run_time=0.7)
            seg.wait_until(seg.word(0, "one shape"))
            self.play(GrowFromCenter(slide), FadeIn(slab), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(labs[("Birch", False)]), FadeIn(labs[("Alder", False)]), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(labs[("Birch", True)]), FadeIn(labs[("Alder", True)]), run_time=0.8)

        rough = VGroup(side(f"{N['cast_totals']['patients']} patients:", color=PAPER), side("rough estimates", color=PAPER)).arrange(DOWN, buff=0.1)
        rough.move_to([SX, -0.9, 0])
        with self.nar("s5_6", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "With"))
            self.play(FadeIn(rough, shift=UP * 0.1), run_time=0.9)
        for m in [dial, *sl.values()]:
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_WhereBeta(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "A rule learned inside clinics")
        P = LinePanel()
        dots, elm = VGroup(*P.dots().values()), P.elm_marker()
        lines = VGroup(*[P.line(G[n], BETA, COL[n]) for n in FOUR])
        dial, blab, sl, glab = controls(BETA, {**G, "Elm": -3.2})
        bval = big(f"{BETA:.2f}", size=26, color=ACCENT).next_to(dial, DOWN, buff=0.22)
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(dots), FadeIn(elm), FadeIn(lines), FadeIn(dial), FadeIn(blab), FadeIn(glab), FadeIn(bval),
                  *[FadeIn(s) for s in sl.values()], run_time=1.0)

        a, step = POOL["start"], POOL["step"]
        pooled = P.line(a, step, MUTED, dashed=True)
        r1 = VGroup(side("the pooled line climbs"), big(f"{step:.2f}", size=30, color=MUTED)).arrange(RIGHT, buff=0.3).move_to([SX, -0.55, 0])
        r2 = VGroup(side("these lines climb"), big(f"{BETA:.2f}", size=30, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([SX, -1.2, 0])
        r2.align_to(r1, RIGHT)
        with self.nar("s6_1") as seg:
            seg.wait_until(seg.word(0, "The pooled line climbed"))
            self.play(Create(pooled), FadeIn(r1), run_time=1.2)
            seg.wait_until(seg.word(0, "These lines climb"))
            self.play(FadeIn(r2), Indicate(bval, color=ACCENT, scale_factor=1.3), run_time=1.0)

        own = {n: Line(P.P(0, OBS[n]["logodds_low"]), P.P(1, OBS[n]["logodds_high"]), stroke_width=3.5, color=COL[n]).set_z_index(3.6) for n in FOUR}
        own["Dune"] = DashedLine(P.P(0, OBS["Dune"]["logodds_low"]), P.P(1, OBS["Dune"]["logodds_high"]), dash_length=0.14, stroke_width=3.5,
                                 color=DUNE).set_z_index(3.7)
        head = side("the step inside each clinic", size=18).move_to([SX, 0.15, 0])
        rows = {}
        for k, n in enumerate(FOUR):
            y = -0.3 - 0.4 * k
            rows[n] = VGroup(txt(n, 20, COL[n], weight=SEMIBOLD).move_to([SX - 0.75, y, 0], aligned_edge=LEFT),
                             txt(f"{OWN[n]:.2f}", 22, PAPER).move_to([SX + 0.95, y, 0], aligned_edge=RIGHT))
        with self.nar("s6_2") as seg:
            self.play(FadeOut(pooled), FadeOut(r1), FadeOut(r2), lines.animate.set_stroke(opacity=0.25), run_time=0.9)
            seg.wait_until(seg.word(0, "its own higher-risk"))
            self.play(FadeIn(head), run_time=0.7)
            for n, cue in (("Alder", "Inside Alder"), ("Birch", "Inside Birch"), ("Cedar", "Cedar,"), ("Dune", "Dune,")):
                seg.wait_until(seg.word(1, cue) - 0.2)
                self.play(Create(own[n]), FadeIn(rows[n], shift=RIGHT * 0.1), run_time=0.8)

        rule = Line([SX - 0.85, -1.74, 0], [SX + 1.05, -1.74, 0], stroke_width=2, color=FAINT)
        shared = VGroup(txt("shared", 20, ACCENT, weight=SEMIBOLD).move_to([SX - 0.75, -2.02, 0], aligned_edge=LEFT),
                        txt(f"{BETA:.2f}", 22, ACCENT, weight=SEMIBOLD).move_to([SX + 0.95, -2.02, 0], aligned_edge=RIGHT))
        elm_name = txt("Elm", 20, ELM, weight=SEMIBOLD).move_to([SX - 0.75, -2.5, 0], aligned_edge=LEFT)
        elmrow = VGroup(elm_name, side("no step, no say", size=18).next_to(elm_name, RIGHT, buff=0.3))
        with self.nar("s6_3") as seg:
            seg.wait_until(seg.word(0, "compromise"))
            self.play(Create(rule), FadeIn(shared), Indicate(bval, color=ACCENT, scale_factor=1.3), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(elmrow), Indicate(elm, color=ELM, scale_factor=1.2), run_time=1.0)

        def arrow():
            return Arrow(ORIGIN, RIGHT * 0.8, buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.3)

        m1 = VGroup(side("how sick", color=PAPER), arrow(), tex(r"\beta", 38, ACCENT)).arrange(RIGHT, buff=0.25)
        m2 = VGroup(side("where treated", color=PAPER), arrow(), tex(r"\gamma", 38, PAPER)).arrange(RIGHT, buff=0.25)
        VGroup(m1, m2).arrange(DOWN, buff=0.35, aligned_edge=RIGHT).move_to([SX, -0.85, 0])
        done = VGroup(txt("a risk rule learned from", 19, GOOD), txt("patients who share a clinic", 19, GOOD)).arrange(DOWN, buff=0.08).move_to([SX + 0.2, -2.3, 0])
        tick = tick_mark().next_to(done, LEFT, buff=0.22)
        with self.nar("s6_4", gap=0.8) as seg:
            self.play(FadeOut(VGroup(head, rule, shared, elmrow, *rows.values())), *[FadeOut(o) for o in own.values()],
                      lines.animate.set_stroke(opacity=1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(m1, shift=RIGHT * 0.1), run_time=0.8)
            self.play(FadeIn(m2, shift=RIGHT * 0.1), Indicate(glab, color=PAPER, scale_factor=1.5), run_time=1.0)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(done), Create(tick), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_NoIntercept(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "No overall intercept")
        P = LinePanel()
        dots, elm = VGroup(*P.dots().values()).set_opacity(0.3), P.elm_marker().set_opacity(0.3)
        lines = VGroup(*[P.line(G[n], BETA, COL[n]) for n in FOUR])
        c = ValueTracker(0.0)
        dial, blab, sl, glab = controls(BETA, {**G, "Elm": -3.2})
        bval = big(f"{BETA:.2f}", size=26, color=ACCENT).next_to(dial, DOWN, buff=0.22)
        vals = {}
        for n in FOUR:
            sl[n].add_updater(lambda m, n=n: m.slide_to(G[n] - c.get_value()))
            vals[n] = DecimalNumber(G[n], num_decimal_places=2, include_sign=True, font_size=18, color=PAPER)
            vals[n].add_updater(lambda m, n=n: m.set_value(G[n] - c.get_value()).next_to(sl[n].track, UP, buff=0.12))
            vals[n].update()
        self.play(FadeIn(tag), FadeIn(P.g), FadeIn(dots), FadeIn(elm), FadeIn(lines), FadeIn(dial), FadeIn(blab), FadeIn(glab), FadeIn(bval),
                  *[FadeIn(s) for s in sl.values()], *[FadeIn(v) for v in vals.values()], run_time=1.0)

        base = Slider("Alder", 0.0, h=1.3, lo=-1.0, hi=1.0, color=MUTED, tag=False).move_to([3.15, -1.45, 0])
        base.add_updater(lambda m: m.slide_to(c.get_value()))
        b0lab = tex(r"\beta_0", 34, MUTED).next_to(base, UP, buff=0.2)
        b0val = DecimalNumber(0.0, num_decimal_places=2, include_sign=True, font_size=22, color=MUTED)
        b0val.add_updater(lambda m: m.set_value(c.get_value()).next_to(base, DOWN, buff=0.18))
        b0val.update()
        with self.nar("s7_1") as seg:
            seg.wait_until(seg.word(0, "an overall starting point"))
            self.play(FadeIn(base), FadeIn(b0lab), FadeIn(b0val), run_time=1.0)

        ident = fit_width(MathTex(r"(\beta_0 + \tfrac{1}{2}) + (\gamma_i - \tfrac{1}{2})", "=", r"\beta_0 + \gamma_i", font_size=30, color=PAPER), 3.3)
        ident.move_to([5.25, -1.0, 0])
        same = VGroup(side("every line, every probability:", size=17), side("unchanged", size=19, color=PAPER)).arrange(DOWN, buff=0.08).move_to([5.25, -1.85, 0])
        cross = Cross(VGroup(base, b0lab), stroke_color=ALERT, stroke_width=5)
        with self.nar("s7_2") as seg:
            seg.wait_until(seg.word(0, "Raise that number"))
            self.play(c.animate.set_value(0.5), run_time=2.6)
            self.play(FadeIn(ident), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(same), Indicate(lines, color=PAPER, scale_factor=1.02), run_time=1.0)
            seg.wait_until(seg.word(1, "so the model keeps"))
            self.play(Create(cross), run_time=0.7)
            self.play(c.animate.set_value(0.0), run_time=1.2)

        pills = VGroup(pill("size"), pill("ownership"), pill("neighbourhood")).arrange(DOWN, buff=0.14).move_to([5.3, -1.45, 0])
        cap = fit_width(side("the same for every patient at a clinic", size=17), 4.3).move_to([4.75, -0.35, 0])
        inside = txt("already inside \u03b3", 18, PAPER).move_to([5.3, -2.55, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeOut(ident), FadeOut(same), FadeOut(base), FadeOut(b0lab), FadeOut(b0val), FadeOut(cross), run_time=0.7)
            seg.wait_until(seg.word(0, "its size"))
            self.play(FadeIn(cap), LaggedStart(*[FadeIn(p, shift=LEFT * 0.15) for p in pills], lag_ratio=0.6), run_time=2.4)
            seg.wait_until(seg.s(1))
            self.play(*[p.animate.move_to(sl["Alder"].knob.get_center()).scale(0.15).set_opacity(0) for p in pills], run_time=1.4)
            self.play(FadeIn(inside), run_time=0.8)
        for m in [*sl.values(), *vals.values()]:
            m.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Gamma(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "What gamma is, and isn't")
        Rp, Rl = prob_ruler(1.6, x0=-4.4, x1=3.4), logit_ruler(-0.4, x0=-4.4, x1=3.4)
        gA, pA = G["Alder"], FIT["Alder"]["p_low"]
        dg = Dot(Rl.P(gA), radius=0.13, color=ALDER).set_z_index(4)
        glab = MathTex(r"\gamma_{\text{Alder}}", "=", f"{gA:.2f}", font_size=32, color=ALDER).next_to(dg, DOWN, buff=0.62)
        pos = side("a position on the log-odds ruler", size=18).next_to(glab, DOWN, buff=0.18)
        dp = Dot(Rp.P(pA), radius=0.13, color=ALDER).set_z_index(4)
        plab = txt(pct(pA), 26, ALDER, weight=SEMIBOLD).next_to(dp, UP, buff=0.2)
        link = DashedLine(Rl.P(gA, 0.16), Rp.P(pA, -0.16), dash_length=0.08, stroke_width=2.5, color=ALDER)
        rc = risk_chip(pA, r=0.5, color=ALDER).move_to([5.45, 0.9, 0])
        rcap = VGroup(side("a lower-risk patient", size=18, color=PAPER), side("at Alder", size=18, color=PAPER)).arrange(DOWN, buff=0.08).next_to(rc, DOWN, buff=0.22)
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(Rp.g), FadeIn(Rl.g), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(dg), FadeIn(glab), run_time=0.9)
            seg.wait_until(seg.word(1, "It is a position"))
            self.play(FadeIn(pos), Indicate(dg, color=PAPER, scale_factor=1.6), run_time=1.0)
            seg.wait_until(seg.s(2))
            self.play(Create(link), GrowFromCenter(dp), FadeIn(plab), run_time=1.0)
            self.play(FadeIn(rc, scale=0.7), FadeIn(rcap), run_time=0.8)

        offs = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.3, height=0.2, stroke_color=FAINT, stroke_width=2) for _ in range(12)])
        offs.arrange_in_grid(rows=2, cols=6, buff=0.1).next_to(rcap, DOWN, buff=0.3)
        offcap = side("twelve risk factors, all off", size=16).next_to(offs, DOWN, buff=0.14)
        dc = Dot(Rl.P(G["Cedar"]), radius=0.13, color=CEDAR).set_z_index(4)
        gapb = DoubleArrow(Rl.P(G["Cedar"], 0.42), Rl.P(gA, 0.42), buff=0, stroke_width=3, color=ACCENT, tip_length=0.12)
        gapl = side("read the gap", size=18, color=ACCENT).next_to(gapb, UP, buff=0.1)
        with self.nar("s8_2") as seg:
            self.play(FadeIn(offs), FadeIn(offcap), run_time=0.9)
            seg.wait_until(seg.word(0, "may not exist"))
            self.play(rc.animate.set_opacity(0.2), rcap.animate.set_opacity(0.3), run_time=0.9)
            seg.wait_until(seg.word(0, "So we will mostly"))
            self.play(VGroup(link, dp, plab, pos).animate.set_opacity(0.25), GrowFromCenter(dc), run_time=0.8)
            self.play(GrowFromCenter(gapb), FadeIn(gapl), run_time=0.8)

        title = big("\u03b3 is not a pure measure of care", 0, 2.35, 34)
        bar = RoundedRectangle(corner_radius=0.2, width=1.5, height=3.6, stroke_color=ALDER, stroke_width=3, fill_color=INK_2, fill_opacity=1).move_to([-3.6, -0.35, 0])
        gl = tex(r"\gamma", 46, ALDER).next_to(bar, LEFT, buff=0.35)
        div = DashedLine(bar.get_left() + UP * 0.2, bar.get_right() + UP * 0.2, dash_length=0.1, stroke_width=3, color=PAPER)
        darr = DoubleArrow(bar.get_right() + RIGHT * 0.3 + DOWN * 0.5, bar.get_right() + RIGHT * 0.3 + UP * 0.9, buff=0, stroke_width=3, color=MUTED, tip_length=0.12)
        t_care = VGroup(txt("how well the clinic", 24, PAPER), txt("looks after its patients", 24, PAPER)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t_div = side("the data cannot place this boundary", size=19)
        t_rest = VGroup(txt("anything about its patients", 24, PAPER), txt("that we failed to measure", 24, PAPER)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        t_care.move_to([-1.9, 0.95, 0], aligned_edge=LEFT)
        t_div.move_to([-1.9, -0.15, 0], aligned_edge=LEFT)
        t_rest.move_to([-1.9, -1.3, 0], aligned_edge=LEFT)
        with self.nar("s8_3") as seg:
            self.play(*clear(self, keep=(tag,)), run_time=0.7)
            self.play(FadeIn(title, shift=UP * 0.1), FadeIn(bar), FadeIn(gl), run_time=0.9)
            seg.wait_until(seg.word(1, "how well it looks after"))
            self.play(FadeIn(t_care, shift=RIGHT * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "but also anything"))
            self.play(FadeIn(t_rest, shift=RIGHT * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "The data cannot separate"))
            self.play(Create(div), GrowFromCenter(darr), FadeIn(t_div), run_time=0.9)
            self.play(div.animate.shift(UP * 0.6), run_time=0.7)
            self.play(div.animate.shift(DOWN * 1.2), run_time=0.9)
            self.play(div.animate.shift(UP * 0.6), run_time=0.7)

        pB = FIT["Birch"]["p_low"]
        cb, ca = risk_chip(pB, r=0.62, color=BIRCH).move_to([-2.9, 0.1, 0]), risk_chip(pA, r=0.62, color=ALDER).move_to([2.9, 0.1, 0])
        nb, na = txt("at Birch", 24, BIRCH, weight=SEMIBOLD).next_to(cb, UP, buff=0.25), txt("at Alder", 24, ALDER, weight=SEMIBOLD).next_to(ca, UP, buff=0.25)
        vb, va = big(pct(pB), size=34, color=BIRCH).next_to(cb, DOWN, buff=0.25), big(pct(pA), size=34, color=ALDER).next_to(ca, DOWN, buff=0.25)
        mid = VGroup(side("the same patient", color=PAPER), side("on paper", color=PAPER), side("(lower-risk; the model's probability)", size=15)).arrange(DOWN, buff=0.1)
        mid.move_to([0, 0.1, 0])
        head2 = big("a higher \u03b3: more readmissions here than there", 0, 2.35, 28)
        why = side("why is a separate question", size=24, color=PAPER).move_to([0, -2.35, 0])
        with self.nar("s8_4", gap=0.8) as seg:
            self.play(*clear(self, keep=(tag,)), run_time=0.7)
            self.play(FadeIn(mid), run_time=0.6)
            seg.wait_until(seg.word(0, "for patients who look the same"))
            self.play(FadeIn(cb, scale=0.7), FadeIn(nb), FadeIn(ca, scale=0.7), FadeIn(na), run_time=0.9)
            seg.wait_until(seg.word(0, "more readmissions here"))
            self.play(FadeIn(vb), FadeIn(va), FadeIn(head2, shift=UP * 0.1), run_time=0.9)
            seg.wait_until(seg.word(0, "Why is a separate question"))
            self.play(FadeIn(why), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Crowd(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Two hundred lines")
        gh, bfe = np.array(CROWD["gamma_hat"]), CROWD["fixed_effect_step"]
        x0, x1, y0, y1, s_lim, v_lo, v_hi = -5.9, 0.9, -2.25, 2.6, 2.6, -5.4, 2.0

        def pt(s, v):
            return np.array([x0 + (x1 - x0) * (s + s_lim) / (2 * s_lim), y0 + (y1 - y0) * (v - v_lo) / (v_hi - v_lo), 0.0])

        frame = VGroup(Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED))
        xl, yl = side("risk score", size=18).move_to([(x0 + x1) / 2, y0 - 0.32, 0]), side("log-odds", size=18).move_to([x0 + 0.1, y1 + 0.28, 0])
        lines = VGroup()
        for gk in gh:
            sa, sb = max(-s_lim, (v_lo - gk) / bfe), min(s_lim, (v_hi - gk) / bfe)
            lines.add(Line(pt(sa, gk + bfe * sa), pt(sb, gk + bfe * sb), stroke_width=1.3, color=PAPER, stroke_opacity=0.32))
        count = side(f"{CROWD['providers']} providers, one shared step", size=19, color=PAPER).move_to([(x0 + x1) / 2 + 0.6, y1 + 0.28, 0])

        R = Ruler(-1.0, 0.65, 0.90, x0=3.1, x1=6.6, ticks=[0.65, 0.70, 0.75, 0.80, 0.85, 0.90], labels={0.70: "0.70", 0.80: "0.80", 0.90: "0.90"}, title="step")
        true, pooled, fe = CROWD["true_step"], CROWD["pooled_step"], CROWD["fixed_effect_step"]
        tr = Triangle(fill_color=PAPER, fill_opacity=1, stroke_width=0).scale(0.1).rotate(PI).move_to(R.P(true, 0.2))
        trl = txt(f"truth {true:.2f}", 18, PAPER).next_to(tr, UP, buff=0.1)
        pd = Dot(R.P(pooled), radius=0.1, color=ALERT).set_z_index(4)
        pl = VGroup(txt("pooled", 18, ALERT), txt(f"{pooled:.2f}", 22, ALERT, weight=SEMIBOLD)).arrange(DOWN, buff=0.06).move_to(R.P(pooled, -0.95))
        fd = Dot(R.P(fe), radius=0.1, color=ACCENT).set_z_index(4)
        fl = VGroup(txt("one \u03b3 per provider", 18, ACCENT), txt(f"{fe:.2f}", 22, ACCENT, weight=SEMIBOLD)).arrange(DOWN, buff=0.06).move_to([5.75, 0.25, 0])
        flead = Line(fd.get_center() + UP * 0.12, fl.get_bottom() + DOWN * 0.08 + LEFT * 0.3, stroke_width=1.5, color=ACCENT)
        sick = VGroup(side("in this crowd, providers with sicker", size=16), side("patients do a little better", size=16)).arrange(DOWN, buff=0.06).move_to([SX + 0.15, -2.55, 0])
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), FadeIn(frame), FadeIn(xl), FadeIn(yl), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(lines, lag_ratio=0.01), FadeIn(count), run_time=2.2)
            seg.wait_until(seg.word(1, "The true step"))
            self.play(FadeIn(R.g), FadeIn(tr), FadeIn(trl), run_time=1.0)

        with self.nar("s9_2", gap=0.8) as seg:
            self.play(GrowFromCenter(pd), FadeIn(pl), run_time=0.9)
            seg.wait_until(seg.word(0, "because in this crowd"))
            self.play(FadeIn(sick), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(fd), Create(flead), FadeIn(fl), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S10
class S10_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(8, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        levels = ((-0.5, BIRCH), (-0.32, CEDAR), (0.1, ALDER), (0.22, DUNE))
        icon1 = VGroup(*[Line([-0.8, y, 0], [0.8, y + 0.55, 0], stroke_width=4.5, color=c) for y, c in levels],
                       *[Circle(radius=0.07, stroke_color=c, stroke_width=2.5).set_fill(INK_2, opacity=1).move_to([-0.8, y, 0]) for y, c in levels])
        icon2 = VGroup(Dial(BETA, r=0.45), tex(r"\beta", 36, ACCENT)).arrange(RIGHT, buff=0.3)
        icon3 = VGroup(Circle(radius=0.11, stroke_color=CEDAR, stroke_width=3).set_fill(INK_2, opacity=1).move_to([-0.6, -0.35, 0]),
                       Dot([0.6, 0.35, 0], radius=0.12, color=CEDAR), step_arrow([-0.45, -0.26, 0], [0.45, 0.26, 0], tip=0.18))
        icons = [icon1, icon2, icon3]
        caps = [["Every provider gets", "its own intercept: \u03b3"], ["All providers share one step", "per risk factor: \u03b2"],
                ["\u03b2 is learned from", "comparisons inside providers"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 21, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s10_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        mini = VGroup(*[Line([-5.7, y, 0], [-1.7, y + 1.5, 0], stroke_width=4.5, color=c) for y, c in ((-1.45, BIRCH), (-1.1, CEDAR), (-0.4, ALDER), (-0.25, DUNE))])
        crossing = DashedLine([-5.7, 0.9, 0], [-1.7, -0.9, 0], dash_length=0.14, stroke_width=4.5, color=ALERT)
        crl = side("a line that crosses", size=18, color=ALERT).move_to([-4.3, 1.45, 0])
        t1 = VGroup(big("the bet", size=30, color=ACCENT), txt("the lines are parallel", 26, PAPER)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        t2 = VGroup(txt("patients' outcomes are independent,", 20, MUTED), txt("given their clinic and risk factors", 20, MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        t3 = VGroup(txt("nothing assumed about how the \u03b3 are spread,", 20, MUTED), txt("or how they relate to case mix", 20, MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        col = VGroup(t1, t2, t3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([3.0, 0.1, 0])
        with self.nar("s10_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(LaggedStart(*[Create(m) for m in mini], lag_ratio=0.15), FadeIn(t1, shift=UP * 0.1), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(Create(crossing), FadeIn(crl), run_time=1.2)
            seg.wait_until(seg.word(1, "We will come back"))
            self.play(FadeIn(t2), FadeIn(t3), run_time=0.9)

        need = big("A fair standard needs", 0, 2.45, 32)
        n1 = VGroup(big("1", size=30, color=ACCENT), txt("a risk rule learned from patients who share a clinic", 24, PAPER)).arrange(RIGHT, buff=0.35).move_to([0, 1.65, 0])
        n2 = VGroup(big("2", size=30, color=ACCENT), txt("a yardstick no single clinic can bend", 24, PAPER)).arrange(RIGHT, buff=0.35).move_to([0, 1.0, 0]).align_to(n1, LEFT)
        tick = tick_mark().next_to(n1, RIGHT, buff=0.3)
        R = Ruler(-1.05, -2.6, 0.0, x0=-3.6, x1=4.4, ticks=[-2.5, -2.0, -1.5, -1.0, -0.5, 0.0], labels={-2.0: signed(-2, 0), -1.0: signed(-1, 0), 0.0: "0"},
                  title="log-odds", ends=(True, False))
        gd = {n: Dot(R.P(G[n]), radius=0.12, color=COL[n]).set_z_index(4) for n in FOUR}
        gn = {n: txt(n, 18, COL[n], weight=SEMIBOLD).next_to(gd[n], UP, buff=0.16) for n in FOUR}
        gn["Alder"].shift(LEFT * 0.3)
        gn["Dune"].shift(RIGHT * 0.3)
        gn["Cedar"].shift(UP * 0.24)                      # clear of the ring drawn round Cedar
        elm_r = Circle(radius=0.12, stroke_color=ELM, stroke_width=3).set_fill(INK, opacity=1).move_to(R.P(-2.6) + LEFT * 0.25).set_z_index(4)
        elm_n = txt("Elm", 18, ELM, weight=SEMIBOLD).next_to(elm_r, UP, buff=0.16)
        elm_s = side("off the end", size=16).next_to(elm_r, DOWN, buff=0.16)
        ring = Circle(radius=0.3, stroke_color=ACCENT, stroke_width=3.5).move_to(gd["Cedar"])
        midl = side("the one in the middle", size=19, color=ACCENT).next_to(ring, DOWN, buff=0.45)
        once = side("it counts every clinic once, whatever its size", size=19).move_to([0.4, -2.6, 0])
        with self.nar("s10_3") as seg:
            self.play(FadeOut(VGroup(mini, crossing, crl, col)), run_time=0.7)
            self.play(FadeIn(need, shift=UP * 0.1), FadeIn(n1), FadeIn(n2), run_time=0.9)
            seg.wait_until(seg.word(0, "The risk rule"))
            self.play(Create(tick), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(R.g), FadeIn(elm_r), FadeIn(elm_n), FadeIn(elm_s),
                      LaggedStart(*[AnimationGroup(GrowFromCenter(gd[n]), FadeIn(gn[n])) for n in ("Birch", "Cedar", "Alder", "Dune")], lag_ratio=0.25), run_time=2.0)
            seg.wait_until(seg.word(1, "in the middle"))
            self.play(Create(ring), FadeIn(midl), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(once), run_time=0.8)

        P = LinePanel()
        la, lc = P.line(G["Alder"], BETA, ALDER), P.line(G["Cedar"], BETA, CEDAR)
        br = DoubleArrow(P.P(0.5, G["Cedar"] + 0.5 * BETA), P.P(0.5, G["Alder"] + 0.5 * BETA), buff=0, stroke_width=3.5, color=ACCENT, tip_length=0.14).set_z_index(6)
        brl = big(f"{GAP:.2f}", size=30, color=ACCENT).next_to(br, RIGHT, buff=0.18)
        names = VGroup(txt("Alder", 20, ALDER, weight=SEMIBOLD).next_to(P.P(1.0, G["Alder"] + BETA), UL, buff=0.12),
                       txt("Cedar", 20, CEDAR, weight=SEMIBOLD).next_to(P.P(1.0, G["Cedar"] + BETA), DR, buff=0.12))
        nxt = VGroup(txt("Next:", 26, MUTED), big("reading \u03b3", size=38)).arrange(DOWN, buff=0.2).move_to([SX, -0.2, 0])
        with self.nar("s10_4") as seg:
            self.play(*clear(self, keep=(tag,)), run_time=0.7)
            self.play(FadeIn(P.g), Create(la), Create(lc), FadeIn(names), run_time=1.2)
            seg.wait_until(seg.word(0, "above Cedar's") - 0.4)
            self.play(GrowFromCenter(br), FadeIn(brl), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)

        mark, word = logo_mark(1.0), wordmark(54)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        ep = txt("NEXT  \u00b7  EPISODE 5  \u00b7  READING \u03b3", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
        thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep, DOWN, buff=0.45)
        with self.nar("s10_5", gap=1.8) as seg:
            self.play(*clear(self), run_time=0.7)
            self.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep), run_time=1.0)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)
