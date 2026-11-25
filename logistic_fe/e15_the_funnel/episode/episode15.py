"""Model in Motion · The Logistic Fixed-Effect Model · Episode 15: The Funnel (every provider's result, and its uncertainty, in one picture).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.

Render one scene:   manim -ql --media_dir build/media episode/episode15.py S05_Crowd      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e15_numbers.json, written by e15_numbers.py; none is typed here. The funnel's edges are drawn
by mim.funnel from the one formula, 1 +- 1.96 / sqrt(precision).
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
from mim.piles import Hist  # noqa: E402
from mim.funnel import Funnel  # noqa: E402

N = json.loads((ROOT / "e15_numbers.json").read_text())
CAST_F, LEAGUE, LEVEL, SIZE, CAT, DIFFER = (N[k] for k in ("cast", "league", "level", "size", "caterpillar", "differ"))
COL = {n: CLINICS[n]["color"] for n in ORDER}
SX = 4.55                                           # centre of the side column beside a chart
WORSE, BETTER = ALERT, GOOD                         # the two kinds of provider planted in the crowd


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def minus(v, places=2):
    return f"{v:.{places}f}".replace("-", "\u2212")


def box_around(m, color=PAPER, buff=0.1):
    return SurroundingRectangle(m, color=color, buff=buff, stroke_width=2.5, corner_radius=0.06).set_z_index(7)


def cast_funnel():
    return Funnel(p_lo=1.5, p_hi=50.0, ticks=(5, 10, 20, 30, 40, 50))


def crowd_funnel():
    return Funnel(p_lo=1.5, p_hi=350.0, ticks=(5, 20, 50, 100, 200, 300))


def crowd_dots(F, dots, colour=lambda d: PAPER, radius=0.05):
    return VGroup(*[F.dot(d["precision"], d["ratio"], colour(d), radius, 0.8) for d in dots])


def hatched_ring(center, r=0.14, color=ELM):
    c = np.array(center, dtype=float)
    u, w = np.array([1.0, 1.0, 0.0]) / np.sqrt(2), np.array([-1.0, 1.0, 0.0]) / np.sqrt(2)
    return VGroup(Circle(radius=r, stroke_color=color, stroke_width=3).move_to(c),
                  *[Line(c + w * r * d - u * r * 0.9 * np.sqrt(1 - d * d), c + w * r * d + u * r * 0.9 * np.sqrt(1 - d * d), stroke_width=2, color=color) for d in (-0.5, 0.0, 0.5)])


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        planted = LEAGUE["planted"]                         # in league order: +1 truly worse, -1 truly better, 0 identical
        field = VGroup(*[Dot(radius=0.07, color=PAPER) for _ in range(200)]).arrange_in_grid(cols=20, buff=0.2).move_to([0, 0.3, 0])
        spots = {r: k for k, r in enumerate([17, 52, 88, 113, 146, 181])}          # where in the field the six are shown; the field itself has no order
        six = [i for i, v in enumerate(planted) if v]
        count = side("two hundred providers", size=20, color=PAPER).move_to([0, 2.75, 0])
        truth = VGroup(VGroup(Dot(radius=0.09, color=WORSE), side("three truly worse", size=18, color=PAPER)).arrange(RIGHT, buff=0.2), VGroup(Dot(radius=0.09, color=BETTER), side("three truly better", size=18, color=PAPER)).arrange(RIGHT, buff=0.2),
                      VGroup(Dot(radius=0.09, color=PAPER), side("194 identical", size=18, color=PAPER)).arrange(RIGHT, buff=0.2)).arrange(RIGHT, buff=0.9).move_to([0, -2.45, 0])
        with self.nar("s1_1") as seg:
            self.play(FadeIn(field, lag_ratio=0.005), FadeIn(count), run_time=1.6)
            seg.wait_until(seg.word(1, "three worse"))
            self.play(*[field[pos].animate.set_color(WORSE if planted[six[k]] == 1 else BETTER).scale(1.6) for pos, k in spots.items()], FadeIn(truth[0]), FadeIn(truth[1]), run_time=0.9)
            seg.wait_until(seg.word(1, "The other 194"))
            self.play(FadeIn(truth[2]), run_time=0.6)
            self.play(*[field[pos].animate.set_color(PAPER).scale(1 / 1.6) for pos in spots], run_time=0.8)

        x0, x1, y0, y1, r_lo, r_hi = -5.6, 5.6, -2.1, 2.1, 0.2, 2.2
        X = lambda rank: x0 + (x1 - x0) * (rank - 1) / 199.0
        Y = lambda r: y0 + (y1 - y0) * (r - r_lo) / (r_hi - r_lo)
        axes = VGroup(Line([x0 - 0.3, y0, 0], [x1 + 0.3, y0, 0], stroke_width=3, color=MUTED), Line([x0 - 0.3, y0, 0], [x0 - 0.3, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([x0 - 0.4, Y(v), 0], [x0 - 0.3, Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([x0 - 0.65, Y(v), 0])) for v in (0.5, 1, 1.5, 2)],
                      DashedLine([x0 - 0.3, Y(1), 0], [x1 + 0.3, Y(1), 0], dash_length=0.1, stroke_width=2, color=CEDAR),
                      side("ratio", size=16).move_to([x0 - 0.3, y1 + 0.25, 0]), side("highest", size=15).move_to([x0 + 0.3, y0 - 0.3, 0]), side("lowest", size=15).move_to([x1 - 0.3, y0 - 0.3, 0]),
                      side("a league table: all two hundred, in order of ratio", size=16).move_to([0, y0 - 0.3, 0]))
        table = VGroup(*[Dot([X(k + 1), Y(r), 0], radius=0.05, color=PAPER) for k, r in enumerate(LEAGUE["ratios"])])
        ask = big("can you pick out the six?", size=28, color=ACCENT).move_to([1.6, 1.7, 0])
        with self.nar("s1_2") as seg:
            self.play(FadeOut(VGroup(field, count, truth)), run_time=0.6)
            self.play(FadeIn(axes), FadeIn(table, lag_ratio=0.004), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(ask, shift=UP * 0.1), run_time=0.7)

        top, bottom = VGroup(*table[:3]), VGroup(*table[-3:])
        boxes = VGroup(box_around(top, ACCENT, 0.14), box_around(bottom, ACCENT, 0.14))
        colour = lambda k: WORSE if planted[k] == 1 else BETTER
        sizes = LEAGUE["picks_wrong_sizes"]
        small_top = side(f"{sizes[0]} and {sizes[1]} patients", size=15, color=PAPER).next_to(boxes[0], RIGHT, buff=0.2)
        small_bot = side(f"{sizes[2]} and {sizes[3]} patients", size=15, color=PAPER).next_to(boxes[1], LEFT, buff=0.2)
        verdict = VGroup(big("right about two", size=24, color=ACCENT), side("the other four: identical, and small", size=18, color=PAPER)).arrange(DOWN, buff=0.12).move_to([1.6, 1.65, 0])
        luck = side("a league table cannot tell luck from difference", size=20, color=PAPER).move_to([0.4, -2.85, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeOut(ask), Create(boxes), run_time=0.9)
            seg.wait_until(seg.word(0, "and you would be right about two"))
            self.play(*[table[k].animate.set_color(colour(k)).scale(2.0) for k in six], FadeIn(verdict[0]), run_time=0.9)
            seg.wait_until(seg.word(0, "The other four"))
            self.play(FadeIn(small_top), FadeIn(small_bot), FadeIn(verdict[1]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(luck), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 15, "The Funnel", "every provider's result, and its uncertainty, in one picture")


# =================================================================================== S03
class S03_Band(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "From pile to band")
        d = CAST_F["Dune"]
        H = Hist(-5.6, 1.6, -0.9, 2.0, 12, 0.3)
        axis, bars = H.axis(), H.bars(N["dune_pmf"], color=DUNE, opacity=0.8)
        ratio_axis = VGroup(*[txt(f"{k / d['E']:.2f}", 14, ACCENT).move_to([H.X(k), H.y0 - 1.0, 0]) for k in range(0, 13, 2)], side("the same counts, divided by the 4.8 expected: ratios", size=16, color=ACCENT).move_to([(H.x0 + H.x1) / 2, H.y0 - 1.32, 0]))
        centre = VGroup(DashedLine([H.X(d["E"]), H.y0, 0], [H.X(d["E"]), H.y1, 0], dash_length=0.08, stroke_width=2.5, color=CEDAR), txt("1", 18, CEDAR, weight=SEMIBOLD).move_to([H.X(d["E"]), H.y1 + 0.22, 0]))
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(axis), FadeIn(bars), run_time=1.3)
            seg.wait_until(seg.word(1, "Divide every count"))
            self.play(FadeIn(ratio_axis), FadeIn(centre), run_time=1.0)

        a, b = d["lower"] * d["E"], d["upper"] * d["E"]                      # the band's ends, back on the axis of counts
        stretch = VGroup(Line([H.X(a), H.y0 - 1.75, 0], [H.X(b), H.y0 - 1.75, 0], stroke_width=7, color=ACCENT), *[Line([H.X(v), H.y0 - 1.87, 0], [H.X(v), H.y0 - 1.63, 0], stroke_width=4, color=ACCENT) for v in (a, b)])
        ends = VGroup(big(f"{d['lower']:.2f}", size=20, color=ACCENT).next_to(stretch[0].get_start(), LEFT, buff=0.15), big(f"{d['upper']:.2f}", size=20, color=ACCENT).next_to(stretch[0].get_end(), RIGHT, buff=0.15))
        inside = [k for k in N["dune_band_counts"]]
        hold = side(f"{pct(sum(N['dune_pmf'][k] for k in inside))} of the pile", size=17, color=PAPER).move_to([SX, 1.6, 0])
        ry0, ry1 = -1.4, 1.2                                                 # a short ratio scale in the side column, for the upright band
        RY = lambda r: ry0 + (ry1 - ry0) * r / 2.0
        upright = VGroup(Line([SX, RY(d["lower"]), 0], [SX, RY(d["upper"]), 0], stroke_width=7, color=ACCENT), *[Line([SX - 0.14, RY(v), 0], [SX + 0.14, RY(v), 0], stroke_width=4, color=ACCENT) for v in (d["lower"], d["upper"])])
        up_l = VGroup(big(f"{d['upper']:.2f}", size=20, color=ACCENT).move_to([SX + 0.6, RY(d["upper"]), 0]), big(f"{d['lower']:.2f}", size=20, color=ACCENT).move_to([SX + 0.6, RY(d["lower"]), 0]),
                      VGroup(Line([SX - 0.3, RY(1), 0], [SX + 0.3, RY(1), 0], stroke_width=2.5, color=CEDAR), txt("1", 16, CEDAR, weight=SEMIBOLD).move_to([SX - 0.55, RY(1), 0])),
                      side("inside the band: unremarkable for Dune", size=15, color=PAPER).move_to([SX, ry0 - 0.5, 0]))
        with self.nar("s3_2") as seg:
            self.play(Create(stretch), FadeIn(ends), FadeIn(hold), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(TransformFromCopy(stretch, upright), FadeIn(up_l[0]), FadeIn(up_l[1]), FadeIn(up_l[2]), run_time=1.3)
            self.play(FadeIn(up_l[3]), run_time=0.6)

        F = cast_funnel()
        f_axes = F.axes(x_label="precision: how much a clinic can tell us")
        bands = {n: F.band(CAST_F[n]["precision"], COL[n]) for n in ("Dune", "Birch")}
        labels = {n: VGroup(txt(n, 18, COL[n], weight=SEMIBOLD), side(f"precision {CAST_F[n]['precision']:.0f}", size=15, color=PAPER), side(f"{CAST_F[n]['lower']:.2f} to {CAST_F[n]['upper']:.2f}", size=15, color=PAPER)).arrange(DOWN, buff=0.05)
                  for n in ("Dune", "Birch")}
        for n in labels:
            labels[n].next_to(bands[n], UP, buff=0.14)
        formula = VGroup(side("precision", size=17, color=PAPER), MathTex(r"= \frac{\text{expected}^2}{\text{its variance}}", font_size=30, color=PAPER)).arrange(RIGHT, buff=0.2)
        formula = fit_width(formula, 4.3).move_to([SX, 1.4, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(axis, bars, ratio_axis, centre, stretch, ends, hold, upright, up_l)), run_time=0.6)
            self.play(FadeIn(f_axes), FadeIn(formula), run_time=1.0)
            seg.wait_until(seg.word(0, "Dune's is 10"))
            self.play(FadeIn(bands["Dune"]), FadeIn(labels["Dune"]), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(bands["Birch"]), FadeIn(labels["Birch"]), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Funnel(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Join the edges")
        F = cast_funnel()
        axes = F.axes(x_label="precision: how much a clinic can tell us")
        many = VGroup(*[F.band(p, PAPER, width=3, caps=False).set_stroke(opacity=0.35) for p in (2, 3, 4, 5, 7, 10, 13, 17, 22, 28, 34, 39, 45, 50)])
        edges = F.edges()
        wide = side("wide: little to go on", size=16, color=PAPER).move_to(F.P(4.5, 2.25) + RIGHT * 1.0)
        narrow = side("narrow: more to go on", size=16, color=PAPER).move_to(F.P(42, 1.62))
        name = big("a funnel", size=30, color=ACCENT).move_to([SX, 1.4, 0])
        edge_f = MathTex(r"1 \pm \frac{1.96}{\sqrt{\text{precision}}}", font_size=34, color=PAPER).move_to([SX, 0.3, 0])
        self.play(FadeIn(tag), FadeIn(axes), run_time=1.0)
        with self.nar("s4_1") as seg:
            self.play(LaggedStart(*[FadeIn(b) for b in many], lag_ratio=0.08), run_time=1.6)
            self.play(Create(edges[0]), Create(edges[1]), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(wide), run_time=0.6)
            seg.wait_until(seg.word(1, "Narrow on the right"))
            self.play(FadeIn(narrow), run_time=0.6)
            seg.wait_until(seg.word(1, "A funnel"))
            self.play(FadeIn(name), FadeIn(edge_f), run_time=0.8)

        where = {"Dune": LEFT, "Cedar": DOWN, "Birch": DOWN, "Alder": UP}
        dots = {n: VGroup(F.dot(CAST_F[n]["precision"], CAST_F[n]["ratio"], COL[n], 0.13).set_z_index(5), txt(n, 18, COL[n], weight=SEMIBOLD)) for n in ("Dune", "Cedar", "Birch", "Alder")}
        for n in dots:
            dots[n][1].next_to(dots[n][0], where[n], buff=0.14)
        ring = Circle(radius=0.28, stroke_color=ALERT, stroke_width=3.5).move_to(dots["Alder"][0]).set_z_index(6)
        flagged = VGroup(side("outside the funnel", size=18, color=PAPER), big("flagged", size=26, color=ALERT), side("by the bell-curve test: the same sum, drawn", size=15)).arrange(DOWN, buff=0.1)
        flagged = fit_width(flagged, 4.4).move_to([SX, -1.2, 0])
        with self.nar("s4_2") as seg:
            self.play(FadeOut(VGroup(many, wide, narrow)), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(dots[n]) for n in ("Dune", "Cedar", "Birch")], lag_ratio=0.25), run_time=1.2)
            seg.wait_until(seg.word(0, "Alder, at"))
            self.play(FadeIn(dots["Alder"]), Create(ring), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(flagged), run_time=0.8)

        e = CAST_F["Elm"]
        elm = VGroup(hatched_ring(F.P(e["precision"], 0.0)).set_z_index(5), txt("Elm", 18, ELM, weight=SEMIBOLD).move_to(F.P(e["precision"], 0.0) + UP * 0.38 + RIGHT * 0.1))
        zero = VGroup(Line([F.x0, F.Y(0.0), 0], [F.x1, F.Y(0.0), 0], stroke_width=1.5, color=FAINT), side("no readmissions at all", size=14).move_to([F.x1 - 1.3, F.Y(0.0) - 0.2, 0]))
        low = VGroup(Dot(F.P(e["precision"], e["lower"]), radius=0.07, color=ACCENT).set_z_index(6), big(minus(e["lower"]), size=18, color=ACCENT).move_to(F.P(e["precision"], e["lower"]) + RIGHT * 0.55))
        never = VGroup(side("the lower edge is below zero:", size=17, color=PAPER), side("no count could flag Elm as better", size=17, color=ACCENT)).arrange(DOWN, buff=0.08)
        never = fit_width(never, 4.4).move_to([SX, -1.2, 0])
        with self.nar("s4_3", gap=0.8) as seg:
            self.play(FadeOut(flagged), FadeIn(zero), FadeIn(elm), run_time=0.9)
            seg.wait_until(seg.word(0, "At Elm's precision"))
            self.play(FadeIn(low), run_time=0.7)
            seg.wait_until(seg.word(0, "No count, not even none"))
            self.play(FadeIn(never), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Crowd(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Two hundred at once")
        F = crowd_funnel()
        axes, edges = F.axes(), F.edges()
        dots = crowd_dots(F, LEVEL["dots"])
        lucky = [k for k, d in enumerate(LEVEL["dots"]) if d["out"] and not d["planted"]]
        rings = VGroup(*[Circle(radius=0.13, stroke_color=ACCENT, stroke_width=2.5).move_to(dots[k]) for k in lucky]).set_z_index(5)
        outside = VGroup(big(f"{LEVEL['outside']} of {LEVEL['ordinary']}", size=34, color=ACCENT), side("identical providers, outside by luck alone", size=16, color=PAPER)).arrange(DOWN, buff=0.1)
        outside = fit_width(outside, 4.4).move_to([SX, 1.4, 0])
        redraw = VGroup(side(f"over {LEVEL['redraws']} redraws of the crowd:", size=16, color=PAPER), big(f"{pct(LEVEL['redraw_share'], 1)} on average", size=24), side("that is what a 5% line means", size=16)).arrange(DOWN, buff=0.1)
        redraw = fit_width(redraw, 4.4).move_to([SX, -0.2, 0])
        self.play(FadeIn(tag), FadeIn(axes), FadeIn(edges), run_time=1.0)
        with self.nar("s5_1") as seg:
            self.play(FadeIn(dots, lag_ratio=0.005), run_time=1.5)
            seg.wait_until(seg.word(0, "13 fall outside"))
            self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.08), FadeIn(outside), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(redraw), run_time=0.9)

        planted = [k for k, d in enumerate(LEVEL["dots"]) if d["planted"]]
        marks = VGroup()
        for k in planted:
            d = LEVEL["dots"][k]
            c = WORSE if d["planted"] == 1 else BETTER
            m = VGroup(F.dot(d["precision"], d["ratio"], c, 0.11).set_z_index(6), txt(str(d["n"]), 15, c, weight=SEMIBOLD))
            m[1].next_to(m[0], UP if d["planted"] == 1 else DOWN, buff=0.1)
            if d["out"]:
                m.add(Circle(radius=0.22, stroke_color=c, stroke_width=3).move_to(m[0]).set_z_index(6))
            marks.add(m)
        key = VGroup(VGroup(Dot(radius=0.09, color=WORSE), side("truly worse", size=16, color=PAPER)).arrange(RIGHT, buff=0.15), VGroup(Dot(radius=0.09, color=BETTER), side("truly better", size=16, color=PAPER)).arrange(RIGHT, buff=0.15),
                    side("the number beside each: its patients", size=14)).arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to([SX, 1.6, 0])
        caught = VGroup(big("three caught", size=26, color=ACCENT), side("missed: both with 37 patients,", size=16, color=PAPER), side("and the better one with 105", size=16, color=PAPER)).arrange(DOWN, buff=0.1).move_to([SX, 0.0, 0])
        with self.nar("s5_2") as seg:
            self.play(FadeOut(VGroup(outside, redraw, rings)), run_time=0.5)
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.1), FadeIn(key), run_time=1.2)
            seg.wait_until(seg.word(0, "The funnel catches three"))
            self.play(FadeIn(caught[0]), run_time=0.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(caught[1]), run_time=0.6)
            seg.wait_until(seg.word(1, "And it misses"))
            self.play(FadeIn(caught[2]), run_time=0.6)

        notes = VGroup(VGroup(side("a dot outside:", size=17, color=PAPER), big("not a verdict", size=22, color=ACCENT)).arrange(DOWN, buff=0.06), VGroup(side("a dot inside:", size=17, color=PAPER), big("not an acquittal", size=22, color=ACCENT)).arrange(DOWN, buff=0.06),
                      side("inside means consistent with the reference, not equal to it", size=15, color=PAPER)).arrange(DOWN, buff=0.3)
        notes = VGroup(notes[0], notes[1], fit_width(notes[2], 4.5)).arrange(DOWN, buff=0.3).move_to([SX, 0.2, 0])
        with self.nar("s5_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(key, caught)), FadeIn(notes[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "and a dot inside"))
            self.play(FadeIn(notes[1]), run_time=0.6)
            seg.wait_until(seg.word(0, "Inside means"))
            self.play(FadeIn(notes[2]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Precision(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Why precision, not size")
        F = crowd_funnel()
        axes, edges = F.axes(), F.edges().set_stroke(opacity=0.6)

        def provider(p, color, y):
            row = VGroup(*[risk_chip(p, r=0.075, color=color) for _ in range(100)]).arrange_in_grid(cols=25, buff=0.04)
            lab = VGroup(side("100 patients, each near", size=16, color=PAPER), big(pct(p), size=22, color=color)).arrange(RIGHT, buff=0.2)
            return VGroup(lab, row).arrange(DOWN, buff=0.12).move_to([SX - 0.15, y, 0])

        lo, hi = provider(0.05, BIRCH, 1.55), provider(0.40, DUNE, -0.35)
        marks = VGroup(*[VGroup(Line(F.P(v, F.r_lo), F.P(v, F.r_hi), stroke_width=3.5, color=c), big(f"{v:.0f}", size=24, color=c).move_to(F.P(v, 2.15) + RIGHT * 0.32)).set_z_index(5) for v, c in ((SIZE["low_risk"], BIRCH), (SIZE["high_risk"], DUNE))])
        same = side("the same size, at opposite ends of the funnel", size=16, color=ACCENT)
        same = fit_width(same, 4.5).move_to([SX, -1.75, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(edges), run_time=1.1)
            seg.wait_until(seg.word(1, "One treats patients"))
            self.play(FadeIn(lo), run_time=0.9)
            seg.wait_until(seg.word(1, "the other, near"))
            self.play(FadeIn(hi), run_time=0.9)
            seg.wait_until(seg.s(2))
            self.play(FadeIn(marks[0]), FadeIn(marks[1]), run_time=0.8)
            seg.wait_until(seg.word(2, "The same size"))
            self.play(FadeIn(same), run_time=0.7)

        near = [d for d in LEVEL["dots"] if 90 <= d["n"] <= 110]
        dots = crowd_dots(F, LEVEL["dots"]).set_opacity(0.3)
        picked = VGroup(*[F.dot(d["precision"], d["ratio"], ACCENT, 0.09).set_z_index(5) for d in near])
        a, b = SIZE["near_100"]
        span = VGroup(Line(F.P(a, -0.3), F.P(b, -0.3), stroke_width=6, color=ACCENT), *[Line(F.P(v, -0.3) + DOWN * 0.1, F.P(v, -0.3) + UP * 0.1, stroke_width=4, color=ACCENT) for v in (a, b)]).set_z_index(5)
        real = VGroup(side(f"{len(near)} providers of about a hundred patients", size=16, color=PAPER), big(f"precision {a:.0f} to {b:.0f}", size=24, color=ACCENT)).arrange(DOWN, buff=0.1)
        real = fit_width(real, 4.5).move_to([SX, 0.5, 0])
        with self.nar("s6_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(lo, hi, marks, same)), FadeIn(dots), run_time=0.9)
            self.play(FadeIn(picked), Create(span), FadeIn(real), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Cater(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "The caterpillar")
        x0, x1, y0, y1, r_hi = -5.9, 5.9, -2.2, 2.2, 2.7
        X = lambda k: x0 + (x1 - x0) * k / 199.0
        Y = lambda r: y0 + (y1 - y0) * min(r, r_hi) / r_hi
        axes = VGroup(Line([x0 - 0.25, y0, 0], [x1 + 0.2, y0, 0], stroke_width=3, color=MUTED), Line([x0 - 0.25, y0, 0], [x0 - 0.25, y1, 0], stroke_width=3, color=MUTED),
                      *[VGroup(Line([x0 - 0.35, Y(v), 0], [x0 - 0.25, Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([x0 - 0.6, Y(v), 0])) for v in (0, 0.5, 1, 1.5, 2, 2.5)],
                      DashedLine([x0 - 0.25, Y(1), 0], [x1 + 0.2, Y(1), 0], dash_length=0.1, stroke_width=2.5, color=CEDAR), side("ratio, with its exact interval", size=16).move_to([x0 + 1.4, y1 + 0.25, 0]),
                      side("two hundred providers, from the highest ratio to the lowest", size=16).move_to([0, y0 - 0.32, 0]))
        whiskers = VGroup(*[Line([X(k), Y(c["low"]), 0], [X(k), Y(c["high"]), 0], stroke_width=2.2, color=ACCENT if c["flag"] else MUTED) for k, c in enumerate(CAT)])
        points = VGroup(*[Dot([X(k), Y(c["ratio"]), 0], radius=0.035, color=ACCENT if c["flag"] else PAPER) for k, c in enumerate(CAT)]).set_z_index(4)
        flagged = sum(c["flag"] for c in CAT)
        key = VGroup(VGroup(Line(ORIGIN, UP * 0.3, stroke_width=3, color=ACCENT), side(f"flagged: the interval leaves out 1 ({flagged})", size=15, color=PAPER)).arrange(RIGHT, buff=0.15)).move_to([2.9, 2.3, 0])
        order = side("it shows the order, and how little the order can be trusted", size=18, color=ACCENT).move_to([0.6, -2.85, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), run_time=1.0)
            self.play(FadeIn(whiskers, lag_ratio=0.004), FadeIn(points, lag_ratio=0.004), FadeIn(key), run_time=1.8)
            seg.wait_until(seg.word(1, "The caterpillar shows"))
            self.play(FadeIn(order), run_time=0.8)

        d = CAST_F["Dune"]
        ry0, ry1 = -2.0, 2.0
        RY = lambda r: ry0 + (ry1 - ry0) * r / 2.6
        scale = VGroup(Line([-2.0, ry0, 0], [-2.0, ry1, 0], stroke_width=3, color=MUTED), *[VGroup(Line([-2.1, RY(v), 0], [-2.0, RY(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([-2.35, RY(v), 0])) for v in (0, 0.5, 1, 1.5, 2, 2.5)],
                       side("ratio, at Dune's precision", size=16).move_to([-2.0, ry1 + 0.28, 0]))
        counts = VGroup(*[VGroup(Dot([-1.2, RY(k / d["E"]), 0], radius=0.08, color=PAPER if k in N["dune_band_counts"] else ALERT), txt(str(k), 13, MUTED).move_to([-0.85, RY(k / d["E"]), 0])) for k in range(0, 13)])
        counts_l = side("the counts Dune could have", size=15).move_to([-0.9, ry0 - 0.32, 0])
        smooth = VGroup(*[VGroup(Line([0.2, RY(v), 0], [2.4, RY(v), 0], stroke_width=4, color=ACCENT), big(f"{v:.2f}", size=20, color=ACCENT).move_to([2.9, RY(v), 0])) for v in (d["lower"], d["upper"])], side("the smooth edges", size=16, color=ACCENT).move_to([1.3, RY(d["upper"]) + 0.3, 0]))
        ex = N["dune_exact_limits"]
        exact = VGroup(*[VGroup(DashedLine([0.2, RY(v), 0], [2.4, RY(v), 0], dash_length=0.1, stroke_width=3.5, color=PAPER), big(f"{v:.2f}", size=20, color=PAPER).move_to([3.75, RY(v), 0])) for v in ex], side("the exact limits, half-way between counts", size=16, color=PAPER).move_to([2.1, RY(ex[1]) - 0.3, 0]))
        guide = side("the smooth curve is a guide to them", size=18, color=ACCENT).move_to([3.4, -2.3, 0])
        with self.nar("s7_2", gap=0.8) as seg:
            self.play(FadeOut(VGroup(axes, whiskers, points, key, order)), run_time=0.6)
            self.play(FadeIn(scale), FadeIn(counts), FadeIn(counts_l), FadeIn(smooth), run_time=1.1)
            seg.wait_until(seg.word(0, "With the exact test"))
            self.play(FadeIn(exact), run_time=0.9)
            seg.wait_until(seg.word(0, "The smooth curve"))
            self.play(FadeIn(guide), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Differ(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "When providers truly differ")
        F = crowd_funnel()
        axes, edges = F.axes(), F.edges()
        dots = crowd_dots(F, LEVEL["dots"])
        before = VGroup(side("all but six identical", size=17, color=PAPER), big(f"{LEVEL['outside']} of {LEVEL['ordinary']} outside", size=24)).arrange(DOWN, buff=0.1).move_to([SX, 1.4, 0])
        moved = VGroup(*[F.dot(d["precision"], d["ratio"], ACCENT if (d["out"] and not d["planted"]) else PAPER, 0.05, 0.85) for d in DIFFER["dots"]])
        after = VGroup(side("providers that truly differ a little", size=17, color=PAPER), big(f"{DIFFER['outside']} of {LEVEL['ordinary']} outside", size=26, color=ACCENT), side("about a quarter", size=18, color=PAPER)).arrange(DOWN, buff=0.1)
        after = fit_width(after, 4.4).move_to([SX, -0.2, 0])
        self.play(FadeIn(tag), FadeIn(axes), FadeIn(edges), FadeIn(dots), FadeIn(before), run_time=1.2)
        with self.nar("s8_1") as seg:
            seg.wait_until(seg.word(0, "Let them truly differ"))
            self.play(*[Transform(dots[k], moved[k]) for k in range(len(dots))], run_time=2.4)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(after), run_time=0.9)

        ask = VGroup(big("each one an outlier?", size=24), big("or a funnel too narrow?", size=24, color=ACCENT)).arrange(DOWN, buff=0.15).move_to([SX, -1.95, 0])
        with self.nar("s8_2", gap=0.8) as seg:
            self.play(FadeOut(before), FadeIn(ask[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "Or is the funnel"))
            self.play(FadeIn(ask[1]), run_time=0.7)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])

        def mini(dots=()):
            f = Funnel(x0=-0.95, x1=0.95, y0=-0.5, y1=0.5, p_lo=1.5, p_hi=120.0, r_lo=0.0, r_hi=2.0)
            g = VGroup(Line([f.x0, f.Y(1), 0], [f.x1, f.Y(1), 0], stroke_width=2, color=CEDAR), f.edges(width=3))
            g.add(*[f.dot(p, r, c, 0.055) for p, r, c in dots])
            return g

        ax = VGroup(Arrow([-0.8, -0.45, 0], [0.9, -0.45, 0], buff=0, stroke_width=3.5, color=PAPER, max_tip_length_to_length_ratio=0.12), Arrow([-0.8, -0.45, 0], [-0.8, 0.55, 0], buff=0, stroke_width=3.5, color=PAPER, max_tip_length_to_length_ratio=0.2),
                    txt("ratio", 14, PAPER).move_to([-0.35, 0.5, 0]), txt("precision", 14, PAPER).move_to([0.35, -0.68, 0]))
        icons = [ax, mini(((12, 1.75, ALERT), (40, 1.1, PAPER), (80, 0.92, PAPER))), mini(((4, 0.35, PAPER), (5, 1.7, PAPER), (7, 1.2, PAPER), (90, 1.02, PAPER)))]
        caps = [["Up the side, the ratio.", "Along the bottom, precision"], ["The funnel: what luck allows.", "Outside it means flagged"], ["Dots on the left are not worse.", "They are quieter"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.95, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        top = mini(((12, 1.75, ALERT), (40, 1.1, PAPER), (80, 0.92, PAPER), (20, 0.8, PAPER))).scale(1.6).move_to([-2.6, 1.0, 0])
        block = VGroup(Rectangle(width=4.2, height=0.9, stroke_color=ACCENT, stroke_width=3, fill_color=INK_2, fill_opacity=1), txt("the risk model", 22, ACCENT, weight=SEMIBOLD)).move_to([-2.6, -0.75, 0])
        rests = side("every picture in this act rests on it", size=17, color=PAPER).move_to([-2.6, -1.6, 0])
        nxt = VGroup(txt("Next:", 26, MUTED), big("can we trust it?", size=34)).arrange(DOWN, buff=0.2).move_to([3.4, 0.2, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(top), run_time=0.8)
            seg.wait_until(seg.word(0, "the risk model itself"))
            self.play(FadeIn(block), FadeIn(rests), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)
        end_card(self, "s9_3", 16, "Trusting the Risk Model")
