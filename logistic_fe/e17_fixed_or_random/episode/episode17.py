"""Model in Motion · The Logistic Fixed-Effect Model · Episode 17: Fixed or Random? (pull the estimates together, or let each stand alone).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode17.py S07_CaseMix      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e17_numbers.json, written by e17_numbers.py; none is typed here. Fixed-effect values are drawn
in paper white and random-effect values in the accent yellow throughout.
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

N = json.loads((ROOT / "e17_numbers.json").read_text())
CASTN, CROWD, NOLINK, SIGMA = N["cast"], N["crowd"], N["no_link"], N["sigma"]
PROVS = CROWD["providers"]
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.5                                            # centre of the side column
FIXED, RANDOM = PAPER, ACCENT                       # the two fits' colours, everywhere in the episode
WORSE, BETTER = ALERT, GOOD


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def key_row(color, text, size=16):
    return VGroup(Dot(radius=0.08, color=color), side(text, size=size, color=PAPER)).arrange(RIGHT, buff=0.15)


class Plot:
    """A plain pair of axes: u along the bottom (optionally on a log scale), v up the side."""

    def __init__(self, x0, x1, y0, y1, u0, u1, v0, v1, logx=False):
        self.x0, self.x1, self.y0, self.y1, self.u0, self.u1, self.v0, self.v1, self.logx = x0, x1, y0, y1, u0, u1, v0, v1, logx

    def X(self, u):
        f = (np.log(u) - np.log(self.u0)) / (np.log(self.u1) - np.log(self.u0)) if self.logx else (u - self.u0) / (self.u1 - self.u0)
        return self.x0 + (self.x1 - self.x0) * f

    def Y(self, v):
        return self.y0 + (self.y1 - self.y0) * (min(max(v, self.v0), self.v1) - self.v0) / (self.v1 - self.v0)

    def P(self, u, v):
        return np.array([self.X(u), self.Y(v), 0.0])

    def frame(self, x_ticks, y_ticks, x_label, y_label, zero=True, fmt=lambda v: minus(v, 1)):
        g = VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], stroke_width=3, color=MUTED), Line([self.x0, self.y0, 0], [self.x0, self.y1, 0], stroke_width=3, color=MUTED))
        g.add(*[VGroup(Line([self.X(u), self.y0, 0], [self.X(u), self.y0 - 0.09, 0], stroke_width=2, color=MUTED), txt(f"{u:g}".replace("-", "\u2212"), 14, MUTED).move_to([self.X(u), self.y0 - 0.26, 0])) for u in x_ticks])
        g.add(*[VGroup(Line([self.x0 - 0.09, self.Y(v), 0], [self.x0, self.Y(v), 0], stroke_width=2, color=MUTED), txt(fmt(v), 14, MUTED).move_to([self.x0 - 0.38, self.Y(v), 0])) for v in y_ticks])
        if zero:
            g.add(DashedLine([self.x0, self.Y(0.0), 0], [self.x1, self.Y(0.0), 0], dash_length=0.1, stroke_width=2, color=CEDAR))
        g.add(side(x_label, size=15).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.56, 0]), side(y_label, size=15).move_to([self.x0, self.y1 + 0.24, 0], aligned_edge=LEFT))
        return g


def size_plot():
    return Plot(-5.6, 1.5, -2.1, 2.1, 18.0, 520.0, -1.7, 1.7, logx=True)


SIZE_TICKS = (20, 50, 100, 200, 500)


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        cols = {"Dune": -4.3, "Alder": -2.3, "Cedar": -0.3, "Birch": 1.7}
        v_lo, v_hi, y0, y1 = -2.2, -0.2, -2.3, 2.1
        Y = lambda v: y0 + (y1 - y0) * (v - v_lo) / (v_hi - v_lo)
        axis = VGroup(Line([-5.7, y0, 0], [-5.7, y1, 0], stroke_width=3, color=MUTED), *[VGroup(Line([-5.8, Y(v), 0], [-5.7, Y(v), 0], stroke_width=2, color=MUTED), txt(minus(v, 1), 15, MUTED).move_to([-6.15, Y(v), 0])) for v in (-2.0, -1.5, -1.0, -0.5)],
                      side("a clinic's own number: higher is worse", size=16).move_to([-5.7, y1 + 0.28, 0], aligned_edge=LEFT))
        fx = CASTN["fixed"]
        dots = {n: VGroup(Dot([cols[n], Y(fx[n]), 0], radius=0.14, color=COL[n]).set_z_index(4), txt(n, 20, COL[n], weight=SEMIBOLD), txt(minus(fx[n]), 20, PAPER, weight=MEDIUM)) for n in cols}
        for n, d in dots.items():
            d[1].next_to(d[0], UP, buff=0.14)
            d[2].next_to(d[0], DOWN, buff=0.14)

        def patients(n, y):
            k = CASTN["patients"][n]
            block = VGroup(*[chip(COL[n], False, 0.075) for _ in range(k)]).arrange_in_grid(cols=10, buff=0.06)
            return VGroup(txt(f"{n}: {k} patients", 18, COL[n], weight=SEMIBOLD), block).arrange(DOWN, buff=0.14).move_to([SX, y, 0])

        p_dune, p_alder = patients("Dune", 1.5), patients("Alder", -0.1)
        worst = side("the highest", size=16, color=ACCENT).next_to(dots["Dune"][2], DOWN, buff=0.12)
        with self.nar("s1_1") as seg:
            self.play(FadeIn(axis), LaggedStart(*[FadeIn(dots[n]) for n in cols], lag_ratio=0.2), run_time=1.6)
            seg.wait_until(seg.word(0, "the highest of any clinic"))
            self.play(Indicate(dots["Dune"][0], color=ACCENT, scale_factor=1.4), FadeIn(worst), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(p_dune), run_time=0.8)

        ask = big("which is truly the worst?", size=26, color=ACCENT).move_to([SX, -1.9, 0])
        with self.nar("s1_2") as seg:
            self.play(Indicate(dots["Alder"][0], color=ACCENT, scale_factor=1.4), FadeIn(p_alder), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.8)

        centre = CASTN["centre"]
        mean_line = VGroup(DashedLine([-5.7, Y(centre), 0], [4.9, Y(centre), 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), side("toward the average", size=15).move_to([3.8, Y(centre) - 0.25, 0]))
        pulls = VGroup(*[Arrow([cols[n] + 0.45, Y(fx[n]), 0], [cols[n] + 0.45, Y(CASTN["shrunk"][n]), 0], buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.18) for n in ("Dune", "Alder", "Birch")])
        hard = side("pulled hardest where there is least to go on", size=17, color=ACCENT).move_to([-1.9, -2.75, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(ask, worst)), FadeIn(mean_line), run_time=0.8)
            seg.wait_until(seg.word(0, "They would pull"))
            self.play(LaggedStart(*[GrowArrow(a) for a in pulls], lag_ratio=0.2), FadeIn(hard), run_time=1.3)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 17, "Fixed or Random?", "pull the estimates together, or let each stand alone")


# =================================================================================== S03
class S03_Assume(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "A different assumption")
        X = lambda v: -6.0 + (v + 2.5) * 3.9                                  # the effect scale, laid flat
        fx, centre = CASTN["fixed"], CASTN["centre"]
        ya = -0.9
        axis = VGroup(Line([X(-2.5), ya, 0], [X(-0.3), ya, 0], stroke_width=3, color=MUTED), *[VGroup(Line([X(v), ya, 0], [X(v), ya - 0.1, 0], stroke_width=2, color=MUTED), txt(minus(v, 1), 15, MUTED).move_to([X(v), ya - 0.3, 0])) for v in (-2.5, -2.0, -1.5, -1.0, -0.5)])
        up = {"Dune": 0.62, "Alder": 0.28, "Cedar": 0.28, "Birch": 0.28}
        dots = {n: VGroup(Dot([X(fx[n]), ya, 0], radius=0.12, color=COL[n]).set_z_index(5), txt(n, 17, COL[n], weight=SEMIBOLD).move_to([X(fx[n]), ya + up[n], 0])) for n in ("Dune", "Alder", "Cedar", "Birch")}
        fixed_l = VGroup(big("fixed", size=28), side("each number stands alone; nothing is assumed about them", size=17, color=PAPER)).arrange(DOWN, buff=0.1).move_to([-1.9, 2.2, 0])
        dens = lambda v: float(np.exp(-0.5 * ((v - centre) / SIGMA) ** 2))
        bell = VMobject(color=ACCENT, stroke_width=4).set_points_smoothly([np.array([X(v), ya + 0.02 + 2.3 * dens(v), 0.0]) for v in np.linspace(-2.5, -0.3, 80)]).set_z_index(3)
        cmark = VGroup(DashedLine([X(centre), ya, 0], [X(centre), ya + 2.32, 0], dash_length=0.08, stroke_width=2, color=ACCENT), side("a centre", size=15, color=ACCENT).move_to([X(centre), ya + 2.55, 0]))
        h = ya + 2.3 * dens(centre + SIGMA)
        spread = VGroup(DoubleArrow([X(centre), h, 0], [X(centre + SIGMA), h, 0], buff=0, stroke_width=3, color=ACCENT, tip_length=0.13), side("a spread", size=15, color=ACCENT).move_to([X(centre + SIGMA) + 0.65, h, 0]))
        random_l = VGroup(big("random", size=28, color=ACCENT), side("the numbers are draws from one bell curve", size=17, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX - 0.3, 2.2, 0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(axis), LaggedStart(*[FadeIn(d) for d in dots.values()], lag_ratio=0.15), run_time=1.5)
            seg.wait_until(seg.word(0, "That is what fixed means"))
            self.play(FadeIn(fixed_l), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(fixed_l.animate.set_opacity(0.35), Create(bell), FadeIn(random_l), run_time=1.4)
            seg.wait_until(seg.word(1, "with a centre"))
            self.play(FadeIn(cmark), FadeIn(spread), run_time=0.8)

        d, se = CASTN["shrunk"]["Dune"], CASTN["se"]["Dune"]
        band = Line([X(fx["Dune"]), ya - 0.62, 0], [X(centre), ya - 0.62, 0], stroke_width=5, color=DUNE)
        band_caps = VGroup(*[Line([X(v), ya - 0.74, 0], [X(v), ya - 0.5, 0], stroke_width=3, color=DUNE) for v in (fx["Dune"], centre)])
        ghost = VGroup(Dot([X(d), ya - 0.62, 0], radius=0.11, color=ACCENT).set_z_index(5), txt(minus(d), 18, ACCENT, weight=SEMIBOLD).move_to([X(d), ya - 0.98, 0]))
        formula = VGroup(side("reliability: the weight on a provider's own data", size=16, color=PAPER),
                         MathTex(r"\frac{\text{spread}^2}{\text{spread}^2 + \text{standard error}^2}", font_size=30, color=PAPER),
                         MathTex(rf"\frac{{{SIGMA:.2f}^2}}{{{SIGMA:.2f}^2 + {se:.2f}^2}} = {CASTN['reliability_dune']:.2f}", font_size=32, color=ACCENT),
                         side("Dune keeps a fifth of its distance from the centre", size=16, color=ACCENT)).arrange(DOWN, buff=0.2)
        formula = fit_width(formula, 4.9).move_to([SX - 0.2, 1.15, 0])
        with self.nar("s3_2") as seg:
            self.play(FadeOut(VGroup(fixed_l, random_l)), Create(band), FadeIn(band_caps), run_time=0.9)
            seg.wait_until(seg.word(0, "is called its reliability"))
            self.play(FadeIn(formula[0]), FadeIn(formula[1]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(formula[2]), run_time=0.8)
            seg.wait_until(seg.word(1, "Dune keeps a fifth"))
            self.play(FadeIn(ghost), FadeIn(formula[3]), run_time=0.8)

        y_top, y_bot = 1.5, -1.4
        rail = lambda y, t, dy=0.3: VGroup(Line([X(-2.5), y, 0], [X(-0.3), y, 0], stroke_width=2.5, color=MUTED), side(t, size=16, color=PAPER).move_to([X(-2.5), y + dy, 0], aligned_edge=LEFT))
        rails = VGroup(rail(y_top, "each clinic's own number", 0.8), rail(y_bot, "after the pull"), *[txt(minus(v, 1), 14, MUTED).move_to([X(v), y_bot - 0.3, 0]) for v in (-2.5, -2.0, -1.5, -1.0, -0.5)])
        sh = CASTN["shrunk"]
        links, ends = VGroup(), VGroup()
        t_up = {"Dune": 0.62, "Alder": 0.3, "Cedar": 0.62, "Birch": 0.3}
        b_dn = {"Dune": 0.62, "Alder": 0.3, "Cedar": 0.3, "Birch": 0.62, "Elm": 0.3}
        for n in ("Dune", "Alder", "Cedar", "Birch"):
            links.add(Line([X(fx[n]), y_top, 0], [X(sh[n]), y_bot, 0], stroke_width=4, color=COL[n]))
            ends.add(VGroup(Dot([X(fx[n]), y_top, 0], radius=0.11, color=COL[n]).set_z_index(5), txt(f"{n} {minus(fx[n])}", 16, COL[n], weight=SEMIBOLD).move_to([X(fx[n]), y_top + t_up[n], 0]),
                            Dot([X(sh[n]), y_bot, 0], radius=0.11, color=COL[n]).set_z_index(5), txt(f"{n} {minus(sh[n])}", 16, COL[n], weight=SEMIBOLD).move_to([X(sh[n]), y_bot - b_dn[n] - 0.3, 0])))
        elm = VGroup(side("Elm: no number of its own", size=15, color=ELM).move_to([X(-2.5) + 1.3, y_top - 0.35, 0]), Dot([X(sh["Elm"]), y_bot, 0], radius=0.11, color=ELM).set_z_index(5),
                     txt(f"Elm {minus(sh['Elm'])}", 16, ELM, weight=SEMIBOLD).move_to([X(sh["Elm"]) - 0.75, y_bot - b_dn["Elm"] + 0.62, 0]))
        flip = VGroup(big("the order has flipped", size=24, color=ACCENT), side(f"Alder keeps two fifths of its distance; Dune, one", size=15, color=PAPER), side("and Elm now has a number", size=15, color=ELM)).arrange(DOWN, buff=0.14)
        flip = fit_width(flip, 4.6).move_to([SX + 0.1, 0.1, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(rails), *[FadeIn(VGroup(e[0], e[1])) for e in ends], run_time=1.0)
            seg.wait_until(seg.word(0, "Dune moves to"))
            self.play(Create(links[0]), FadeIn(VGroup(ends[0][2], ends[0][3])), run_time=0.9)
            seg.wait_until(seg.word(0, "Alder, with more patients"))
            self.play(Create(links[1]), FadeIn(VGroup(ends[1][2], ends[1][3])), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(Create(links[2]), Create(links[3]), FadeIn(VGroup(ends[2][2], ends[2][3], ends[3][2], ends[3][3])), FadeIn(flip[0]), FadeIn(flip[1]), run_time=1.0)
            seg.wait_until(seg.word(1, "And Elm"))
            self.play(FadeIn(elm), FadeIn(flip[2]), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Pull(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "The pull, in the crowd")
        Pl = size_plot()
        frame = Pl.frame(SIZE_TICKS, (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5), "patients", "a provider's number, about the middle one")
        zones = VGroup(Rectangle(width=Pl.X(50) - Pl.X(18), height=Pl.y1 - Pl.y0, stroke_width=0, fill_color=ACCENT, fill_opacity=0.07).move_to([(Pl.X(18) + Pl.X(50)) / 2, 0, 0]),
                       Rectangle(width=Pl.X(520) - Pl.X(200), height=Pl.y1 - Pl.y0, stroke_width=0, fill_color=ACCENT, fill_opacity=0.07).move_to([(Pl.X(200) + Pl.X(520)) / 2, 0, 0]))
        links = VGroup(*[Line(Pl.P(p["n"], p["fe"]), Pl.P(p["n"], p["re"]), stroke_width=1.6, color=MUTED) for p in PROVS])
        fe = VGroup(*[Dot(Pl.P(p["n"], p["fe"]), radius=0.04, color=FIXED) for p in PROVS]).set_z_index(3)
        re = VGroup(*[Dot(Pl.P(p["n"], p["re"]), radius=0.04, color=RANDOM) for p in PROVS]).set_z_index(4)
        key = VGroup(key_row(FIXED, "fixed effects"), key_row(RANDOM, "random effects")).arrange(DOWN, buff=0.12, aligned_edge=LEFT).move_to([SX, 2.2, 0])
        rel = CROWD["reliability"]
        small = VGroup(side("under 50 patients", size=16, color=PAPER), big(f"reliability {rel['small']:.2f}", size=24, color=ACCENT), side(f"they move {CROWD['moved']['small']:.2f} on average", size=15)).arrange(DOWN, buff=0.08).move_to([SX, 0.6, 0])
        large = VGroup(side("above 200 patients", size=16, color=PAPER), big(f"reliability {rel['large']:.2f}", size=24, color=ACCENT), side(f"they move {CROWD['moved']['large']:.2f}", size=15)).arrange(DOWN, buff=0.08).move_to([SX, -1.1, 0])
        self.play(FadeIn(tag), FadeIn(frame), run_time=1.0)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(fe, lag_ratio=0.004), FadeIn(key[0]), run_time=1.2)
            seg.wait_until(seg.s(0) + 2.6)
            self.play(FadeIn(links, lag_ratio=0.004), FadeIn(re, lag_ratio=0.004), FadeIn(key[1]), run_time=1.5)
            seg.wait_until(seg.word(1, "Under 50 patients"))
            self.play(FadeIn(zones[0]), FadeIn(small), run_time=0.8)
            seg.wait_until(seg.word(1, "Above 200"))
            self.play(FadeIn(zones[1]), FadeIn(large), run_time=0.8)

        x0, x1, lo, hi, width = -5.6, 1.4, -1.6, 1.6, 0.1
        HX = lambda v: x0 + (x1 - x0) * (v - lo) / (hi - lo)
        edges = np.arange(lo, hi + 1e-9, width)
        counts = {k: np.histogram(np.clip([p[k] for p in PROVS], lo + 1e-6, hi - 1e-6), bins=edges)[0] for k in ("fe", "truth", "re")}
        top = max(int(c.max()) for c in counts.values())
        rows = (("fe", 0.75, FIXED, "fixed effects", CROWD["sd"]["fixed"]), ("truth", -0.75, CEDAR, "the truth", CROWD["sd"]["truth"]), ("re", -2.25, RANDOM, "random effects", CROWD["sd"]["random"]))
        piles, labels = VGroup(), VGroup()
        for k, y, c, name, sd in rows:
            piles.add(VGroup(Line([x0, y, 0], [x1, y, 0], stroke_width=2.5, color=MUTED), *[Rectangle(width=(x1 - x0) * width / (hi - lo) * 0.86, height=max(1.25 * n / top, 0.001), stroke_width=0, fill_color=c, fill_opacity=0.9).move_to(
                [HX(e + width / 2), y + 1.25 * n / top / 2, 0]) for e, n in zip(edges[:-1], counts[k]) if n > 0]))
            labels.add(VGroup(txt(name, 20, c, weight=SEMIBOLD), VGroup(side("spread", size=16, color=PAPER), big(f"{sd:.2f}", size=28, color=c)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.08).move_to([SX - 0.6, y + 0.55, 0]))
        ticks = VGroup(*[txt(minus(v, 1), 14, MUTED).move_to([HX(v), -2.5, 0]) for v in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5)])
        note = side("wider than the truth, and narrower", size=17, color=ACCENT).move_to([SX - 0.6, 2.45, 0])
        with self.nar("s4_2", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(piles[0]), FadeIn(labels[0]), FadeIn(ticks), run_time=0.9)
            seg.wait_until(seg.word(0, "to 0.26"))
            self.play(FadeIn(piles[2]), FadeIn(labels[2]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(piles[1]), FadeIn(labels[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "Fixed effects scatter wider"))
            self.play(FadeIn(note), run_time=0.6)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Buys(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "What it buys")
        Pl = Plot(-5.6, 1.5, -2.1, 2.1, 18.0, 520.0, -1.3, 1.3, logx=True)
        frame = Pl.frame(SIZE_TICKS, (-1.0, -0.5, 0.0, 0.5, 1.0), "patients", "error: estimate minus truth")
        fe = VGroup(*[Dot(Pl.P(p["n"], p["fe"] - p["truth"]), radius=0.045, color=FIXED).set_opacity(0.75) for p in PROVS]).set_z_index(3)
        re = VGroup(*[Dot(Pl.P(p["n"], p["re"] - p["truth"]), radius=0.045, color=RANDOM).set_opacity(0.9) for p in PROVS]).set_z_index(4)
        key = VGroup(key_row(FIXED, "fixed effects"), key_row(RANDOM, "random effects")).arrange(RIGHT, buff=0.5).move_to([SX, 2.5, 0])
        err, U = CROWD["error"], 4.2                                           # bar height per unit of error

        def pair(label, a, b, x):
            base = -1.9
            bars = VGroup(*[Rectangle(width=0.62, height=U * v, stroke_width=0, fill_color=c, fill_opacity=1).move_to([x + dx, base + U * v / 2, 0]) for v, c, dx in ((a, FIXED, -0.38), (b, RANDOM, 0.38))])
            nums = VGroup(*[txt(f"{v:.2f}", 19, c, weight=SEMIBOLD).move_to([x + dx, base + U * v + 0.22, 0]) for v, c, dx in ((a, FIXED, -0.38), (b, RANDOM, 0.38))])
            return VGroup(bars, nums, side(label, size=15, color=PAPER).move_to([x, base - 0.28, 0]))

        every = pair("all providers", err["fixed"], err["random"], SX - 1.15)
        small = pair("under 50 patients", err["fixed_small"], err["random_small"], SX + 1.15)
        head = side("the typical error", size=17, color=PAPER).move_to([SX, 0.75, 0])
        self.play(FadeIn(tag), FadeIn(frame), run_time=1.0)
        with self.nar("s5_1", gap=0.8) as seg:
            self.play(FadeIn(fe, lag_ratio=0.004), FadeIn(re, lag_ratio=0.004), FadeIn(key), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(head), FadeIn(every), run_time=0.9)
            seg.wait_until(seg.word(1, "For providers under 50"))
            self.play(FadeIn(small), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Outliers(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "What it costs: the outliers")
        x0, x1, lo, hi = -4.9, 1.9, -1.5, 1.5
        X = lambda v: x0 + (x1 - x0) * (min(max(v, lo), hi) - lo) / (hi - lo)
        six = sorted([p for p in PROVS if p["planted"]], key=lambda p: (-p["planted"], p["n"]))
        ys = [1.75 - 0.72 * k for k in range(6)]
        guides = VGroup(DashedLine([X(0), 2.3, 0], [X(0), -2.35, 0], dash_length=0.1, stroke_width=2, color=CEDAR), *[DashedLine([X(v), 2.3, 0], [X(v), -2.35, 0], dash_length=0.06, stroke_width=1.5, color=MUTED) for v in (-0.8, 0.8)],
                        side("the centre", size=14).move_to([X(0), 2.5, 0]), side("truly 0.8 better", size=14, color=BETTER).move_to([X(-0.8), 2.5, 0]), side("truly 0.8 worse", size=14, color=WORSE).move_to([X(0.8), 2.5, 0]),
                        *[txt(minus(v, 1), 14, MUTED).move_to([X(v), -2.6, 0]) for v in (-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5)])
        rows = VGroup()
        for p, y in zip(six, ys):
            c = WORSE if p["planted"] == 1 else BETTER
            row = VGroup(side(f"{p['n']} patients", size=15, color=c).move_to([x0 - 0.85, y, 0]), Line([X(lo), y, 0], [X(hi), y, 0], stroke_width=1, color=FAINT),
                         Square(side_length=0.2, stroke_color=c, stroke_width=3).rotate(PI / 4).move_to([X(p["truth"]), y, 0]),
                         Dot([X(p["fe"]), y, 0], radius=0.11, color=FIXED).set_z_index(4), Dot([X(p["re"]), y, 0], radius=0.11, color=RANDOM).set_z_index(5))
            if p["fe_flag"]:
                row.add(Circle(radius=0.2, stroke_color=FIXED, stroke_width=2.5).move_to([X(p["fe"]), y, 0]))
            if p["re_flag"]:
                row.add(Circle(radius=0.2, stroke_color=RANDOM, stroke_width=2.5).move_to([X(p["re"]), y, 0]))
            rows.add(row)
        key = VGroup(VGroup(Square(side_length=0.16, stroke_color=PAPER, stroke_width=2.5).rotate(PI / 4), side("the truth", size=15, color=PAPER)).arrange(RIGHT, buff=0.15), key_row(FIXED, "fixed effects", 15), key_row(RANDOM, "random effects", 15),
                    VGroup(Circle(radius=0.1, stroke_color=PAPER, stroke_width=2), side("flagged", size=15, color=PAPER)).arrange(RIGHT, buff=0.15)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([SX + 0.3, 1.75, 0])
        pl = CROWD["planted"]
        dist = VGroup(side("average distance from the centre", size=15, color=PAPER), VGroup(big(f"{pl['fixed']:.2f}", size=30, color=FIXED), side("against", size=15), big(f"{pl['random']:.2f}", size=30, color=RANDOM)).arrange(RIGHT, buff=0.2),
                      side(f"of a true {pl['truth']}", size=15)).arrange(DOWN, buff=0.08).move_to([SX + 0.3, -0.1, 0])
        flags = VGroup(side("flagged, of the six", size=15, color=PAPER), VGroup(big(str(pl["fixed_flags"]), size=30, color=FIXED), side("against", size=15), big(str(pl["random_flags"]), size=30, color=RANDOM)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.08).move_to([SX + 0.3, -1.75, 0])
        self.play(FadeIn(tag), FadeIn(guides), run_time=1.0)
        with self.nar("s6_1", gap=0.8) as seg:
            self.play(LaggedStart(*[FadeIn(VGroup(r[0], r[1], r[2])) for r in rows], lag_ratio=0.1), FadeIn(key[0]), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(*[FadeIn(r[3]) for r in rows], FadeIn(key[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "Random effects, at"))
            self.play(*[FadeIn(r[4]) for r in rows], FadeIn(key[2]), FadeIn(dist), run_time=0.8)
            seg.wait_until(seg.s(2))
            self.play(*[FadeIn(m) for r in rows for m in r[5:]], FadeIn(key[3]), FadeIn(flags), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
def mix_plot(x0, x1, v=1.2):
    return Plot(x0, x1, -2.0, 1.9, -1.8, 1.8, -v, v)


def trend(Pl, xs, ys, color):
    b, a = np.polyfit(xs, ys, 1)
    return Line(Pl.P(-1.7, a - 1.7 * b), Pl.P(1.7, a + 1.7 * b), stroke_width=4, color=color).set_z_index(5)


class S07_CaseMix(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "What it costs: the case mix")
        P0 = mix_plot(-5.4, 1.2)
        frame0 = P0.frame((-1.5, -1.0, -0.5, 0, 0.5, 1.0, 1.5), (-1.0, -0.5, 0.0, 0.5, 1.0), "a provider's case mix: sicker patients to the right", "its true number: higher is worse")
        ordinary = [p for p in PROVS if not p["planted"]]
        cloud = VGroup(*[Dot(P0.P(p["mu"], p["truth"]), radius=0.05, color=PAPER).set_opacity(0.8) for p in ordinary])
        line0 = trend(P0, [p["mu"] for p in ordinary], [p["truth"] for p in ordinary], CEDAR)
        told = VGroup(side("in this crowd", size=16, color=PAPER), big("sicker case mix,", size=24), big("truly better", size=24, color=GOOD), side(f"correlation {minus(CROWD['link'])}", size=16), side("random effects assume there is no such link", size=16, color=ACCENT)).arrange(DOWN, buff=0.12)
        told = fit_width(told, 4.6).move_to([SX, 0.2, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(frame0), run_time=1.0)
            seg.wait_until(seg.word(0, "providers with sicker patients"))
            self.play(FadeIn(cloud, lag_ratio=0.004), Create(line0), FadeIn(VGroup(*told[:4])), run_time=1.5)
            seg.wait_until(seg.word(0, "The random-effect model assumes"))
            self.play(FadeIn(told[4]), run_time=0.7)

        def panel(Pl, rows, key, color, title, corr):
            xs, ys = [p["mu"] for p in rows], [p[key] - p["truth"] for p in rows]
            ys = list(np.array(ys) - float(np.mean(ys)))
            fr = Pl.frame((-1.5, 0, 1.5), (-1.0, -0.5, 0.0, 0.5, 1.0), "case mix: sicker to the right", "error")
            dots = VGroup(*[Dot(Pl.P(x, y), radius=0.045, color=color).set_opacity(0.8) for x, y in zip(xs, ys)])
            head = VGroup(txt(title, 19, color, weight=SEMIBOLD), VGroup(side("correlation", size=15, color=PAPER), big(minus(corr), size=24, color=color)).arrange(RIGHT, buff=0.18)).arrange(RIGHT, buff=0.4).move_to([(Pl.x0 + Pl.x1) / 2 + 0.2, 2.55, 0])
            return VGroup(fr, dots, trend(Pl, xs, ys, color), head)

        PL, PR = mix_plot(-6.0, -0.9), mix_plot(0.7, 5.8)
        left = panel(PL, PROVS, "fe", FIXED, "fixed effects", CROWD["corr"]["fixed"])
        right = panel(PR, PROVS, "re", RANDOM, "random effects", CROWD["corr"]["random"])
        f5 = CROWD["fifths"]
        fifth = VGroup(*[VGroup(Line(PR.P(a, v), PR.P(b, v), stroke_width=7, color=ALERT).set_z_index(6), txt(("+" if v > 0 else "\u2212") + f"{abs(v):.2f}", 17, ALERT, weight=SEMIBOLD).move_to(PR.P((a + b) / 2, v) + UP * dy))
                         for a, b, v, dy in ((0.55, 1.7, f5["sick"], 0.3), (-1.7, -0.55, f5["healthy"], -0.3))])
        fifth_l = side("the sickest fifth look worse than they are; the healthiest, better", size=16, color=ALERT).move_to([0, -2.9, 0])
        with self.nar("s7_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(right), run_time=1.0)
            seg.wait_until(seg.word(0, "For fixed effects"))
            self.play(FadeIn(left), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(fifth[0]), run_time=0.7)
            seg.wait_until(seg.word(1, "The healthiest fifth"))
            self.play(FadeIn(fifth[1]), FadeIn(fifth_l), run_time=0.7)

        broken = panel(PR, NOLINK["providers"], "re", RANDOM, "random effects", NOLINK["corr"]["random"])
        broke_l = side("the same crowd, with the link broken", size=17, color=ACCENT).move_to([PR.x0 + 2.6, -2.9, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(fifth, fifth_l)), left.animate.set_opacity(0.25), run_time=0.6)
            self.play(FadeOut(right[1]), FadeOut(right[2]), FadeOut(right[3]), FadeIn(broken[1]), FadeIn(broken[2]), FadeIn(broken[3]), FadeIn(broke_l), run_time=1.2)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Choose(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Which to use")

        def option(head, color, lines, x):
            c = card(5.6, 2.5).move_to([x, 1.15, 0])
            return VGroup(c, txt(head, 24, color, weight=SEMIBOLD).move_to(c.get_top() + DOWN * 0.48), VGroup(*[txt(s, 18, PAPER) for s in lines]).arrange(DOWN, buff=0.12).move_to(c.get_center() + DOWN * 0.3))

        fixed = option("fixed effects", FIXED, ["judging individual providers,", "when performance may be", "tied to case mix"], -3.1)
        random_ = option("random effects", RANDOM, ["many tiny providers, or questions", "about providers as a population"], 3.1)
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.word(0, "If you are judging"))
            self.play(FadeIn(fixed), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(random_), run_time=0.9)

        box = VGroup(RoundedRectangle(width=7.6, height=0.95, corner_radius=0.12, stroke_color=CEDAR, stroke_width=3, fill_color=INK_2, fill_opacity=1), txt("the same standardization: observed over expected", 19, PAPER, weight=MEDIUM)).move_to([0, -1.25, 0])
        feeds = VGroup(*[Arrow(c[0].get_bottom() + DOWN * 0.05, box.get_top() + np.array([dx, 0.05, 0]), buff=0.05, stroke_width=4, color=col, max_tip_length_to_length_ratio=0.2) for c, col, dx in ((fixed, FIXED, -1.6), (random_, RANDOM, 1.6))])
        same = side("the choice changes the numbers that go in, not the arithmetic that follows", size=16, color=PAPER).move_to([0, -2.1, 0])
        caution = side("and neither protects against a risk factor nobody recorded", size=16, color=ALERT).move_to([0, -2.6, 0])
        with self.nar("s8_2", gap=0.8) as seg:
            self.play(FadeIn(box), LaggedStart(*[GrowArrow(a) for a in feeds], lag_ratio=0.2), run_time=1.2)
            seg.wait_until(seg.word(0, "The choice changes"))
            self.play(FadeIn(same), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(caution), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        mid = lambda w=1.9: DashedLine(LEFT * w / 2, RIGHT * w / 2, dash_length=0.08, stroke_width=2.5, color=CEDAR)
        icon1 = VGroup(mid(), Dot([-0.45, 0.62, 0], radius=0.09, color=FIXED), Arrow([-0.45, 0.5, 0], [-0.45, 0.16, 0], buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.35),
                       Dot([0.45, -0.5, 0], radius=0.14, color=FIXED), Arrow([0.45, -0.34, 0], [0.45, -0.2, 0], buff=0, stroke_width=4, color=ACCENT, max_tip_length_to_length_ratio=0.6))
        icon2 = VGroup(*[Rectangle(width=0.4, height=h, stroke_width=0, fill_color=c, fill_opacity=1) for h, c in ((1.0, FIXED), (0.7, RANDOM))]).arrange(RIGHT, buff=0.2, aligned_edge=DOWN)
        tilt = VGroup(mid(), *[Dot([x, 0.28 * x + dy, 0], radius=0.05, color=RANDOM) for x, dy in ((-0.8, 0.05), (-0.5, -0.12), (-0.2, 0.1), (0.1, -0.05), (0.4, 0.12), (0.75, -0.02))], Line([-0.9, -0.25, 0], [0.9, 0.25, 0], stroke_width=3, color=ALERT))
        icons = [icon1, icon2, tilt]
        caps = [["Random effects pull each", "estimate toward the centre,", "by its reliability"], ["The pull buys accuracy on", "average, and gives every", "provider an estimate"], ["It costs you the outliers,", "and it bends with", "the case mix"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 1.0, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        marks = VGroup(*[VGroup(Line(UP * 0.28, DOWN * 0.28, stroke_width=3, color=PAPER), Dot(radius=0.07, color=PAPER)) for _ in range(34)]).arrange(RIGHT, buff=0.24).move_to([0.3, 1.0, 0])
        for k, m in enumerate(marks):
            m[1].shift(UP * 0.2 * float(np.sin(1.7 * k + 0.4)))
            m.set_opacity(1.0 if k < 26 else max(0.1, 1.0 - 0.12 * (k - 25)))
        many = side("one intercept for every provider", size=18, color=PAPER).move_to([0, 1.85, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("too many intercepts", size=34)).arrange(DOWN, buff=0.2).move_to([0, -1.2, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            seg.wait_until(seg.word(0, "One intercept per provider"))
            self.play(FadeIn(marks, lag_ratio=0.03), FadeIn(many), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_3", 18, "Too Many Intercepts")
