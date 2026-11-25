"""Model in Motion · The Logistic Fixed-Effect Model · Episode 9: How Sure Are We? (what the shape of the hill says).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode09.py S06_Share      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e09_numbers.json, written by e09_numbers.py; none is typed here.
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

N = json.loads((ROOT / "e09_numbers.json").read_text())
DIAL, HILL, TESTS, CAT, CROWD, SHARE = N["dial"], N["hill"], N["tests"], N["caterpillar"], N["crowd"], N["share"]
WOB, OWN, HEADS = N["wobble"], N["own_se"], N["heads"]
BETA, S_ = DIAL["beta"], DIAL["S"]
G = {c["clinic"]: c["gamma"] for c in CAT}
COL = {n: CLINICS[n]["color"] for n in ORDER}
IDX = {n: i for i, n in enumerate(ORDER)}
RX = 4.6
Z95 = 1.959964


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def box_around(m, color=PAPER):
    return SurroundingRectangle(m, color=color, buff=0.08, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def hill_chart(x0, x1, y0, y1, b_lo=0.0, b_hi=4.0, h_lo=-63.5, h_hi=-55.0):
    """Episode 6's hill: the height over the dial position. Returns (X, Y, axes, curve, ticks)."""
    X = lambda bv: x0 + (x1 - x0) * (bv - b_lo) / (b_hi - b_lo)
    Y = lambda hv: y0 + (y1 - y0) * (hv - h_lo) / (h_hi - h_lo)
    axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED))
    pts = [np.array([X(bv), Y(hv), 0.0]) for bv, hv in HILL["profile"] if b_lo <= bv <= b_hi and hv >= h_lo]
    curve = VMobject(color=PAPER, stroke_width=4.5).set_points_smoothly(pts)
    ticks = VGroup(*[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 17, MUTED).move_to([X(v), y0 - 0.3, 0]))
                     for v in range(int(np.ceil(b_lo)), int(b_hi) + 1)],
                   side("position of the dial", size=17).move_to([(x0 + x1) / 2, y0 - 0.62, 0]), side("height", size=17).move_to([x0 + 0.1, y1 + 0.26, 0]))
    return X, Y, axes, curve, ticks


def se_line(name, t):
    """Standard error of a clinic's fitted line at risk position t: its own part plus the dial's share, which grows away from its patients."""
    i = IDX[name]
    xb = float(np.sqrt(SHARE["borrowed_var"][i] * S_))
    return float(np.sqrt(SHARE["own_var"][i] + (xb - t) ** 2 / S_))


def band(P, name, t0=-0.3, t1=1.3):
    """The 95% band round a clinic's fitted line: narrow where its patients are, wide where they are not."""
    ts = np.linspace(t0, t1, 41)
    clip = lambda v: min(max(v, P.lo), P.hi)
    up = [P.P(t, clip(G[name] + BETA * t + Z95 * se_line(name, t))) for t in ts]
    dn = [P.P(t, clip(G[name] + BETA * t - Z95 * se_line(name, t))) for t in ts[::-1]]
    return Polygon(*up, *dn, stroke_width=0, fill_color=COL[name], fill_opacity=0.22).set_z_index(1)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        gap = G["Alder"] - G["Cedar"]
        items = [(f"{BETA:.2f}", "the step"), (f"{gap:.2f}", "Alder above Cedar"), (f"\u00d7 {DIAL['or']:.1f}", "the odds")]
        cards = VGroup(*[VGroup(big(v, size=54, color=PAPER), side(l, color=MUTED)).arrange(DOWN, buff=0.2).move_to([x, 0.6, 0]) for (v, l), x in zip(items, (-4.2, 0.0, 4.2))])
        tags = VGroup(*[pill("rough estimate", 19).next_to(c, DOWN, buff=0.35) for c in cards])
        with self.nar("s1_1") as seg:
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in cards], lag_ratio=0.3), run_time=1.6)
            seg.wait_until(seg.word(1, "Rough, we said"))
            self.play(LaggedStart(*[FadeIn(t, scale=0.8) for t in tags], lag_ratio=0.2), run_time=1.0)

        R = Ruler(-0.9, 0.0, float(np.log(30)), x0=-4.6, x1=4.6, ticks=[float(np.log(v)) for v in (1, 2, 5, 10, 20, 30)],
                  labels={float(np.log(v)): f"\u00d7 {v}" for v in (1, 2, 5, 10, 20, 30)}, title="odds")
        mark = Dot(R.P(np.log(DIAL["or"])), radius=0.13, color=ACCENT).set_z_index(4)
        mark_l = big(f"\u00d7 {DIAL['or']:.1f}", size=30, color=ACCENT).next_to(mark, UP, buff=0.25)
        guess = VGroup(DoubleArrow(R.P(np.log(5), 0.95), R.P(np.log(10), 0.95), buff=0, stroke_width=3, color=MUTED, tip_length=0.12), big("?", size=34, color=MUTED))
        guess[1].next_to(guess[0], UP, buff=0.1)
        ask = big("Between what and what?", size=32).move_to([0, 2.2, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(cards, tags)), run_time=0.6)
            self.play(FadeIn(R.g), GrowFromCenter(mark), FadeIn(mark_l), run_time=1.0)
            seg.wait_until(seg.word(1, "Would you stake"))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "On somewhere between"))
            self.play(GrowFromCenter(guess[0]), FadeIn(guess[1]), run_time=0.8)

        hint = side("the answer is in the shape of the hill", size=24, color=ACCENT).move_to([0, -2.3, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(hint, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 9, "How Sure Are We?", "what the shape of the hill says")


# =================================================================================== S03
class S03_Dial(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "The dial")
        X, Y, axes, hill, ticks = hill_chart(-5.6, 1.2, -1.6, 2.3, b_lo=0.0, b_hi=4.0, h_lo=-59.2, h_hi=-55.2)
        top = Dot([X(BETA), Y(HILL["peak"]), 0], radius=0.11, color=ACCENT).set_z_index(5)
        top_l = big(f"{BETA:.2f}", size=26, color=ACCENT).next_to(top, UP, buff=0.18)
        q = lambda bv: HILL["peak"] - 0.5 * S_ * (bv - BETA) ** 2
        par = ParametricFunction(lambda bv: np.array([X(bv), Y(q(bv)), 0.0]), t_range=[BETA - 1.55, BETA + 1.55, 0.02], color=ACCENT, stroke_width=3.5).set_z_index(3)
        sharp = ParametricFunction(lambda t: np.array([t, -2.6 * t * t, 0.0]), t_range=[-0.5, 0.5, 0.02], color=PAPER, stroke_width=4)
        flat = ParametricFunction(lambda t: np.array([t, -0.35 * t * t, 0.0]), t_range=[-0.8, 0.8, 0.02], color=PAPER, stroke_width=4)
        kinds = VGroup(VGroup(sharp, side("a sharp peak pins the dial", size=17, color=PAPER)).arrange(DOWN, buff=0.15),
                       VGroup(flat, side("a flat one lets it wander", size=17, color=PAPER)).arrange(DOWN, buff=0.15)).arrange(DOWN, buff=0.4).move_to([RX, 1.2, 0])
        curv = VGroup(side("the curvature", color=PAPER), big(f"{S_:.2f}", size=40, color=ACCENT)).arrange(RIGHT, buff=0.3).move_to([RX, -0.9, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(ticks), Create(hill), run_time=1.8)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(top), FadeIn(top_l), run_time=0.8)

        with self.nar("s3_2") as seg:
            self.play(Create(par), FadeIn(kinds[0]), run_time=1.4)
            seg.wait_until(seg.word(0, "A flat one"))
            self.play(FadeIn(kinds[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "the folded number"))
            self.play(FadeIn(curv, shift=UP * 0.1), run_time=0.8)

        se_f = MathTex(r"\text{standard error}", "=", rf"\frac{{1}}{{\sqrt{{{S_:.2f}}}}}", "=", f"{DIAL['se']:.2f}", font_size=34, color=PAPER)
        se_f[4].set_color(ACCENT)
        se_f = fit_width(se_f, 4.5).move_to([RX, 1.5, 0])
        ya = Y(-59.2) + 0.45
        iv = DoubleArrow([X(DIAL["low"]), ya, 0], [X(DIAL["high"]), ya, 0], buff=0, stroke_width=4, color=ACCENT, tip_length=0.16).set_z_index(5)
        drops = VGroup(*[DashedLine([X(v), ya, 0], [X(v), Y(q(v)), 0], dash_length=0.08, stroke_width=2, color=ACCENT) for v in (DIAL["low"], DIAL["high"])])
        iv_l = VGroup(*[big(f"{DIAL[k]:.2f}", size=20, color=ACCENT).move_to([X(DIAL[k]), ya - 0.24, 0]) for k in ("low", "high")])
        iv_t = side("95% interval for the dial", size=18, color=PAPER).move_to([RX, 0.55, 0])
        with self.nar("s3_3") as seg:
            self.play(FadeOut(kinds), curv.animate.move_to([RX, 2.45, 0]).scale(0.8), run_time=0.7)
            self.play(Write(se_f), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(iv), Create(drops), FadeIn(iv_l), FadeIn(iv_t), run_time=1.2)

        O = Ruler(-1.35, 0.0, float(np.log(30)), x0=2.7, x1=6.6, ticks=[float(np.log(v)) for v in (1, 2, 5, 10, 20, 30)],
                  labels={float(np.log(v)): str(v) for v in (1, 2, 5, 10, 20)}, title="odds \u00d7")
        o_bar = Line(O.P(np.log(DIAL["or_low"])), O.P(np.log(DIAL["or_high"])), stroke_width=9, color=ACCENT).set_z_index(3)
        o_dot = Dot(O.P(np.log(DIAL["or"])), radius=0.1, color=PAPER).set_z_index(4)
        o_l = VGroup(big(f"{DIAL['or_low']:.1f}", size=22, color=ACCENT).next_to(o_bar.get_start(), UP, buff=0.18), big(f"{DIAL['or_high']:.1f}", size=22, color=ACCENT).next_to(o_bar.get_end(), UP, buff=0.18),
                     txt(f"{DIAL['or']:.1f}", 18, PAPER).next_to(o_dot, UP, buff=0.18))
        verdict = VGroup(side("higher risk raises the odds: clear", size=18, color=PAPER), side("by a factor of two, or of twenty: not settled", size=18, color=PAPER)).arrange(DOWN, buff=0.08)
        verdict = fit_width(verdict, 4.4).move_to([RX, -2.4, 0])
        with self.nar("s3_4", gap=0.8) as seg:
            self.play(FadeIn(O.g), Create(o_bar), GrowFromCenter(o_dot), FadeIn(o_l), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(verdict), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Zero(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Is the step there at all?")
        X, Y, axes, hill, ticks = hill_chart(-5.6, 1.2, -1.9, 2.3)
        top = Dot([X(BETA), Y(HILL["peak"]), 0], radius=0.11, color=ACCENT).set_z_index(5)
        zero = Dot([X(0.0), Y(HILL["at_zero"]), 0], radius=0.11, color=PAPER).set_z_index(5)
        zero_l = VGroup()                                   # the dot sits over the axis tick "0": no label needed
        yb = Y(HILL["at_zero"])
        across = DoubleArrow([X(0.0) + 0.16, yb, 0], [X(BETA), yb, 0], buff=0, stroke_width=3.5, color=ACCENT, tip_length=0.14)
        halves = round(TESTS["z"] * 2) / 2                   # to the nearest half, as the narration says it
        across_l = side(f"across: about {halves:g} standard errors", size=18, color=ACCENT).next_to(across, UP, buff=0.16).shift(RIGHT * 0.25)
        xd = X(BETA) + 0.35
        down = DoubleArrow([xd, Y(HILL["at_zero"]), 0], [xd, Y(HILL["peak"]), 0], buff=0, stroke_width=3.5, color=BIRCH, tip_length=0.14)
        down_l = side(f"down: {TESTS['drop']:.1f}", size=18, color=BIRCH).next_to(down, RIGHT, buff=0.12)
        (b1, h1) = HILL["profile"][1]
        u = np.array([X(b1) - X(0.0), Y(h1) - Y(HILL["at_zero"]), 0.0])
        u = u / np.linalg.norm(u)
        slope = Arrow(zero.get_center(), zero.get_center() + u * 1.3, buff=0, stroke_width=4, color=DUNE, max_tip_length_to_length_ratio=0.2).set_z_index(4)
        slope_l = side("slope: still climbing steeply", size=18, color=DUNE).next_to(slope.get_end(), RIGHT, buff=0.3).shift(DOWN * 0.35)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(ticks), Create(hill), GrowFromCenter(top), run_time=1.6)
            self.play(GrowFromCenter(zero), FadeIn(zero_l), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(across), FadeIn(across_l), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(GrowFromCenter(down), FadeIn(down_l), run_time=0.9)
            seg.wait_until(seg.s(3))
            self.play(GrowArrow(slope), FadeIn(slope_l), run_time=0.9)

        stats = VGroup(*[VGroup(side(lab, size=18, color=c), big(f"{TESTS[k]:.2f}", size=30, color=c)).arrange(RIGHT, buff=0.35)
                         for lab, k, c in (("across", "wald", ACCENT), ("down", "lr", BIRCH), ("slope", "score", DUNE))]).arrange(DOWN, buff=0.28, aligned_edge=RIGHT).move_to([RX, 0.9, 0])
        verdict = VGroup(side("a step this large, by chance:", size=18, color=PAPER), big("less than 1 in 1,000", size=28, color=GOOD)).arrange(DOWN, buff=0.12).move_to([RX, -1.2, 0])
        with self.nar("s4_2", gap=0.8) as seg:
            self.play(LaggedStart(*[FadeIn(s, shift=LEFT * 0.1) for s in stats], lag_ratio=0.25), run_time=1.4)
            seg.wait_until(seg.s(0) + 2.2)
            self.play(FadeIn(verdict, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Clinic(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "One clinic")
        U, x0 = 0.5, -3.6
        heads = VGroup(side("patients", -4.4, 2.35, 16), side("wobble", x0 + 0.5, 2.35, 16), side("standard error on its own", 1.15, 2.35, 16))
        rows = {}
        for k, n in enumerate(ORDER):
            y = 1.7 - 0.72 * k
            bar = Rectangle(width=max(U * WOB[k], 0.03), height=0.34, stroke_width=0, fill_color=COL[n], fill_opacity=1).move_to([x0 + max(U * WOB[k], 0.03) / 2, y, 0])
            rows[n] = VGroup(txt(n, 22, COL[n], weight=SEMIBOLD).move_to([-6.3, y, 0], aligned_edge=LEFT), txt(str(HEADS[k]), 22, PAPER).move_to([-4.4, y, 0]), bar,
                             txt(f"{WOB[k]:.2f}", 20, PAPER).next_to(bar, RIGHT, buff=0.15),
                             big(f"{OWN[k]:.2f}", 1.15, y, 26, COL[n]) if n != "Elm" else side("not meaningful", 1.15, y, 16))
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads[1]), LaggedStart(*[AnimationGroup(FadeIn(rows[n][0]), GrowFromEdge(rows[n][2], LEFT), FadeIn(rows[n][3])) for n in ORDER], lag_ratio=0.2), run_time=2.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(heads[2]), FadeIn(rows["Alder"][4]), run_time=0.8)
            seg.wait_until(seg.word(1, "Dune's is"))
            self.play(FadeIn(rows["Dune"][4]), run_time=0.7)

        hx0, hx1, hy0, hy1 = 3.0, 6.7, -0.4, 1.7
        HX = lambda p: hx0 + (hx1 - hx0) * p
        HY = lambda v: hy0 + (hy1 - hy0) * v / 0.27
        hump = VGroup(Line([hx0, hy0, 0], [hx1, hy0, 0], stroke_width=3, color=MUTED),
                      ParametricFunction(lambda p: np.array([HX(p), HY(p * (1 - p)), 0.0]), t_range=[0.0, 1.0, 0.01], color=PAPER, stroke_width=4),
                      *[txt(f"{v}%", 15, MUTED).move_to([HX(v / 100), hy0 - 0.25, 0]) for v in (0, 50, 100)],
                      side("what one patient adds", size=16).move_to([(hx0 + hx1) / 2, hy1 + 0.25, 0]))
        rare = VGroup(side("100 patients at 2%:", size=17, color=PAPER), big(f"{N['rare_example']:.2f}", size=24, color=MUTED)).arrange(RIGHT, buff=0.25).move_to([(hx0 + hx1) / 2, -1.45, 0])
        with self.nar("s5_2", gap=0.8) as seg:
            self.play(FadeIn(hump), FadeIn(heads[0]), *[FadeIn(rows[n][1]) for n in ORDER], FadeIn(rows["Birch"][4]), FadeIn(rows["Cedar"][4]), run_time=1.2)
            seg.wait_until(seg.s(1))
            bx = VGroup(box_around(VGroup(rows["Elm"][1], rows["Elm"][3]), ELM), box_around(VGroup(rows["Dune"][1], rows["Dune"][3]), DUNE))
            self.play(Create(bx), FadeIn(rows["Elm"][4]), run_time=0.9)
            seg.wait_until(seg.word(1, "A hundred patients"))
            self.play(FadeIn(rare, shift=UP * 0.1), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Share(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "The dial's share")
        P = LinePanel()
        D = P.dots()
        lines = {n: P.line(G[n], BETA, COL[n]) for n in FOUR}
        faint = VGroup(lines["Cedar"], lines["Dune"]).set_stroke(opacity=0.25)
        bands = {n: band(P, n) for n in ("Birch", "Alder")}
        z = ValueTracker(0.0)
        mline = always_redraw(lambda: Line(P.P(z.get_value(), P.lo), P.P(z.get_value(), P.hi), stroke_width=3, color=ACCENT).set_z_index(2))
        mlab = txt("read here", 17, ACCENT, weight=SEMIBOLD)
        mlab.add_updater(lambda m: m.next_to(P.P(z.get_value(), P.hi), UP, buff=0.08))
        mark = VGroup(mline, mlab)
        birch_dots = VGroup(D[("Birch", False)], D[("Birch", True)])

        SX = 3.75                                           # left edge of the side column, clear of the probability axis

        def stack(n, y):
            i, U = IDX[n], 5.0
            a, b = SHARE["own_var"][i], SHARE["borrowed_var"][i]
            r1 = Rectangle(width=U * a, height=0.3, stroke_width=0, fill_color=COL[n], fill_opacity=1).move_to([SX + U * a / 2, y, 0])
            r2 = Rectangle(width=max(U * b, 0.02), height=0.3, stroke_width=0, fill_color=ACCENT, fill_opacity=1).move_to([SX + U * a + max(U * b, 0.02) / 2, y, 0])
            l1 = VGroup(txt(n, 18, COL[n], weight=SEMIBOLD), side(f"{OWN[i]:.2f} on its own", size=16, color=PAPER)).arrange(RIGHT, buff=0.18).move_to([SX, y + 0.72, 0], aligned_edge=LEFT)
            l2 = VGroup(big(f"{SHARE['text_se'][i]:.2f}", size=22, color=ACCENT), side("read at zero", size=16, color=PAPER)).arrange(RIGHT, buff=0.18).move_to([SX, y + 0.38, 0], aligned_edge=LEFT)
            return VGroup(l1, l2, r1, r2)

        sb, sa = stack("Birch", 0.75), stack("Alder", -0.75)
        lean = VGroup(side("Birch: 24 of its 30 patients", size=16, color=BIRCH), side("are higher-risk", size=16, color=BIRCH)).arrange(DOWN, buff=0.06, aligned_edge=LEFT).move_to([SX, 2.2, 0], aligned_edge=LEFT)
        legend = VGroup(side("clinic colour: its own", size=14), side("yellow: the dial's share", size=14)).arrange(DOWN, buff=0.05, aligned_edge=LEFT).move_to([SX, -1.3, 0], aligned_edge=LEFT)
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(P.g), FadeIn(faint), FadeIn(lines["Birch"]), FadeIn(lines["Alder"]), FadeIn(birch_dots), run_time=1.2)
            self.add(mark)
            seg.wait_until(seg.word(0, "getting there leans"))
            self.play(FadeIn(bands["Birch"]), FadeIn(lean), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(sb), FadeIn(legend), run_time=0.9)
            seg.wait_until(seg.word(1, "Alder barely"))
            self.play(FadeIn(bands["Alder"]), FadeIn(sa), run_time=0.9)

        gapb = DoubleArrow(P.P(0.75, G["Cedar"] + 0.75 * BETA), P.P(0.75, G["Alder"] + 0.75 * BETA), buff=0, stroke_width=3, color=PAPER, tip_length=0.12).set_z_index(6)
        gap_l = side(f"Alder above Cedar: {G['Alder'] - G['Cedar']:.2f}, unchanged", size=15, color=PAPER).move_to([SX, -2.78, 0], aligned_edge=LEFT)
        away = VGroup(side("zero recorded three units away:", size=17, color=PAPER),
                      VGroup(txt("Alder", 18, ALDER, weight=SEMIBOLD), big(f"{SHARE['text_se'][0]:.2f}", size=22, color=MUTED),
                             Arrow(ORIGIN, RIGHT * 0.6, buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.35), big(f"{SHARE['three_higher'][0]:.1f}", size=30, color=ALERT)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([SX, -2.05, 0], aligned_edge=LEFT)
        off = Arrow(P.P(-0.05, P.hi - 0.3), P.P(-0.32, P.hi - 0.3), buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.4).set_z_index(6)
        with self.nar("s6_2") as seg:
            seg.wait_until(seg.word(0, "Record the risk factor"))
            self.play(z.animate.set_value(-0.3), GrowArrow(off), FadeIn(away), run_time=1.6)
            seg.wait_until(seg.word(0, "though no gap"))
            self.play(GrowFromCenter(gapb), FadeIn(gap_l), run_time=0.8)

        avg = VGroup(side("read at the average case mix:", size=17, color=PAPER),
                     VGroup(*[VGroup(txt(n, 17, COL[n], weight=SEMIBOLD), big(f"{SHARE['avg_se'][IDX[n]]:.2f}", size=24, color=PAPER)).arrange(DOWN, buff=0.06) for n in FOUR]).arrange(RIGHT, buff=0.24)).arrange(DOWN, buff=0.2)
        avg = fit_width(avg, 3.15).move_to([5.4, 0.1, 0])
        fair = fit_width(side("the ones a fair comparison needs", size=17, color=ACCENT), 3.15).next_to(avg, DOWN, buff=0.3)
        with self.nar("s6_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(sb, sa, legend, away, off, gapb, gap_l, lean)), run_time=0.6)
            self.play(z.animate.set_value(SHARE["xbar"]), faint.animate.set_stroke(opacity=1), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(avg), run_time=0.9)
            seg.wait_until(seg.word(1, "These are the ones"))
            self.play(FadeIn(fair), run_time=0.7)
        mline.clear_updaters()
        mlab.clear_updaters()
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Caterpillar(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "The caterpillar")
        R = Ruler(-2.15, -3.4, 1.4, x0=-4.6, x1=4.2, ticks=[-3, -2, -1, 0, 1], labels={v: signed(v, 0) for v in (-3, -2, -1, 0, 1)}, title="log-odds")
        order = sorted(CAT[:4], key=lambda c: c["gamma"])
        rows = {}
        for k, c in enumerate(order):
            y, n = 1.9 - 0.82 * k, c["clinic"]
            line = Line([R.X(c["low"]), y, 0], [R.X(c["high"]), y, 0], stroke_width=6, color=COL[n])
            caps = VGroup(*[Line([R.X(v), y - 0.12, 0], [R.X(v), y + 0.12, 0], stroke_width=4, color=COL[n]) for v in (c["low"], c["high"])])
            rows[n] = VGroup(txt(n, 20, COL[n], weight=SEMIBOLD).move_to([-6.3, y, 0], aligned_edge=LEFT), line, caps, Dot([R.X(c["gamma"]), y, 0], radius=0.11, color=PAPER).set_z_index(4))
        a, b = max(c["low"] for c in CAT[:4]), min(c["high"] for c in CAT[:4])
        shared = Rectangle(width=R.X(b) - R.X(a), height=3.3, stroke_width=0, fill_color=PAPER, fill_opacity=0.1).move_to([(R.X(a) + R.X(b)) / 2, 0.65, 0]).set_z_index(0)
        shared_l = side("all four overlap here", size=16, color=PAPER).move_to([(R.X(a) + R.X(b)) / 2, 2.5, 0])
        verdict = VGroup(side("an opinion about the order,", size=18, color=PAPER), side("and very little confidence in it", size=18, color=PAPER)).arrange(DOWN, buff=0.08).move_to([5.0, 0.7, 0])
        verdict = fit_width(verdict, 3.6).move_to([5.25, 0.7, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(R.g), run_time=0.9)
            self.play(LaggedStart(*[AnimationGroup(FadeIn(rows[c["clinic"]][0]), Create(rows[c["clinic"]][1]), FadeIn(rows[c["clinic"]][2]), GrowFromCenter(rows[c["clinic"]][3])) for c in order], lag_ratio=0.3), run_time=2.2)

        with self.nar("s7_2") as seg:
            self.play(FadeIn(shared), FadeIn(shared_l), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(verdict), run_time=0.9)

        elm = CAT[4]
        ye = 1.9 - 0.82 * 4
        e_line = DashedLine([-4.6, ye, 0], [4.2, ye, 0], dash_length=0.16, stroke_width=6, color=ELM)
        e_ends = VGroup(Arrow([-4.5, ye, 0], [-5.1, ye, 0], buff=0, stroke_width=5, color=ELM, max_tip_length_to_length_ratio=0.5), Arrow([4.1, ye, 0], [4.7, ye, 0], buff=0, stroke_width=5, color=ELM, max_tip_length_to_length_ratio=0.5))
        e_name = txt("Elm", 20, ELM, weight=SEMIBOLD).move_to([-6.3, ye, 0], aligned_edge=LEFT)
        e_l = VGroup(big(f"{minus(elm['low'], 1)} to +{elm['high']:.1f}", size=22, color=ELM), side("not an estimate: a warning sign", size=17, color=PAPER)).arrange(RIGHT, buff=0.3).move_to([-0.2, ye - 0.36, 0])
        with self.nar("s7_3") as seg:
            self.play(FadeOut(verdict), FadeIn(e_name), Create(e_line), GrowArrow(e_ends[0]), GrowArrow(e_ends[1]), run_time=1.3)
            seg.wait_until(seg.word(0, "That is not an estimate"))
            self.play(FadeIn(e_l), run_time=0.8)

        note = side("each interval is about one clinic; comparing two is a separate calculation", size=18, color=PAPER).move_to([-0.6, -2.82, 0])
        with self.nar("s7_4", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "Each interval"))
            self.play(FadeIn(note), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Size(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "What size buys")
        x0, x1, y0, y1 = -5.4, 1.4, -1.9, 2.3
        n_lo, n_hi, s_lo, s_hi = np.log(16), np.log(700), np.log(0.07), np.log(1.0)
        X = lambda nv: x0 + (x1 - x0) * (np.log(nv) - n_lo) / (n_hi - n_lo)
        Y = lambda sv: y0 + (y1 - y0) * (np.log(sv) - s_lo) / (s_hi - s_lo)
        axes = VGroup(Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED), Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([X(v), y0, 0], [X(v), y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(str(v), 16, MUTED).move_to([X(v), y0 - 0.3, 0])) for v in (20, 50, 100, 200, 500)],
                      *[VGroup(Line([x0 - 0.1, Y(v), 0], [x0, Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v}", 16, MUTED).move_to([x0 - 0.42, Y(v), 0])) for v in (0.1, 0.2, 0.5)],
                      side("patients", size=17).move_to([(x0 + x1) / 2, y0 - 0.62, 0]), side("standard error", size=17).move_to([x0 + 0.55, y1 + 0.26, 0]))
        cloud = VGroup(*[Dot([X(nv), Y(sv), 0], radius=0.04, color=PAPER).set_opacity(0.55) for nv, sv in zip(CROWD["n"], CROWD["se"])])
        meds = VGroup()
        for nv, sv in zip((25, 100, 450), CROWD["medians"]):
            d = Dot([X(nv), Y(sv), 0], radius=0.12, color=ACCENT).set_z_index(5)
            meds.add(VGroup(d, big(f"{sv:.2f}", size=24, color=ACCENT).next_to(d, UR, buff=0.12)))
        k, c = np.polyfit(np.log(CROWD["n"]), np.log(CROWD["se"]), 1)
        fitl = Line([X(18), Y(np.exp(c) * 18 ** k), 0], [X(650), Y(np.exp(c) * 650 ** k), 0], stroke_width=3, color=ACCENT).set_z_index(3)
        rule = VGroup(big("four times the patients,", size=24), big("half the error", size=24, color=ACCENT)).arrange(DOWN, buff=0.12).move_to([RX, 1.1, 0])
        plan = VGroup(side("a standard error of 0.1,", size=17, color=PAPER), side("at a 20% readmission rate:", size=17, color=PAPER), big(f"{CROWD['plan']:.0f} patients", size=30, color=PAPER)).arrange(DOWN, buff=0.12).move_to([RX, -0.9, 0])
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(cloud, lag_ratio=0.01), run_time=1.6)
            for k_, cue in enumerate(("those with 20 to 30", "Near 100", "Above 400")):
                seg.wait_until(seg.word(1, cue if k_ else "those with"))
                self.play(GrowFromCenter(meds[k_][0]), FadeIn(meds[k_][1]), run_time=0.6)

        with self.nar("s8_2", gap=0.8) as seg:
            self.play(Create(fitl), FadeIn(rule), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(plan, shift=UP * 0.1), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        peak = ParametricFunction(lambda t: np.array([t, -2.2 * t * t, 0.0]), t_range=[-0.45, 0.45, 0.02], color=PAPER, stroke_width=4)
        icon1 = VGroup(peak, MathTex(r"\frac{1}{\sqrt{\text{curvature}}}", font_size=30, color=ACCENT)).arrange(RIGHT, buff=0.35)
        icon2 = VGroup(Rectangle(width=1.0, height=0.34, stroke_width=0, fill_color=BIRCH, fill_opacity=1), Rectangle(width=0.7, height=0.34, stroke_width=0, fill_color=ACCENT, fill_opacity=1)).arrange(RIGHT, buff=0)
        icon3 = VGroup(Line([-0.8, -0.45, 0], [0.8, 0.1, 0], stroke_width=4.5, color=CEDAR), Line([-0.8, 0.0, 0], [0.8, 0.55, 0], stroke_width=4.5, color=ALDER),
                       Line([-0.05, -0.65, 0], [-0.05, 0.75, 0], stroke_width=3.5, color=ACCENT))
        icons = [icon1, icon2, icon3]
        caps = [["A sharp peak means", "a small standard error"], ["A clinic's uncertainty: its own,", "plus a share of the dial's"], ["For a fair comparison, read", "at the average case mix"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.85, 0])
            captions.add(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        warn = VGroup(big("All of this assumes independent patients", size=30), side("count the same patient twice, and these intervals are too narrow", size=22)).arrange(DOWN, buff=0.3).move_to([0, 0.2, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(warn[0], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(0, "Count the same patient"))
            self.play(FadeIn(warn[1]), run_time=0.7)

        ring = Circle(radius=0.55, stroke_color=ELM, stroke_width=6).move_to([-2.2, 0.2, 0])
        u, w = np.array([1.0, 1.0, 0.0]) / np.sqrt(2), np.array([-1.0, 1.0, 0.0]) / np.sqrt(2)
        hatch = VGroup(*[Line(ring.get_center() + w * 0.55 * d - u * 0.5 * np.sqrt(1 - d * d), ring.get_center() + w * 0.55 * d + u * 0.5 * np.sqrt(1 - d * d), stroke_width=4, color=ELM) for d in (-0.5, 0.0, 0.5)])
        elm_l = VGroup(txt("Elm", 30, ELM, weight=SEMIBOLD), side("11 patients, no readmissions", size=20, color=PAPER)).arrange(DOWN, buff=0.12).next_to(ring, DOWN, buff=0.4)
        nxt = VGroup(txt("Next:", 26, MUTED), big("no events, no peak", size=34)).arrange(DOWN, buff=0.2).move_to([3.0, 0.2, 0])
        with self.nar("s9_3") as seg:
            self.play(FadeOut(warn), run_time=0.6)
            self.play(Create(ring), Create(hatch), FadeIn(elm_l), run_time=1.2)
            seg.wait_until(seg.s(0) + 3.2)
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_4", 10, "No events, no peak")
