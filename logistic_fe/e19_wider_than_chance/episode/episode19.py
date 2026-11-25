"""Model in Motion · The Logistic Fixed-Effect Model · Episode 19: Wider than Chance (what a flag should mean).

ANIMATIC PASS. Every narration clip has its board. The compositions are meant to stay; most of the motion is still to come.
This is the last episode of the arc: its final scene closes the series, and its end card names no next episode.

Render one scene:   manim -ql --media_dir build/media episode/episode19.py S06_Empirical      (run from the episode folder)
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that voiceover clip and
holds the scene until the clip (plus a short gap) has finished.
Every number comes from e19_numbers.json, written by e19_numbers.py; none is typed here. The standard bell curve is
drawn in the cedar grey and the curves fitted to the providers in the accent yellow.
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
from mim.funnel import Funnel  # noqa: E402
from mim.meters import Meter  # noqa: E402

N = json.loads((ROOT / "e19_numbers.json").read_text())
E15 = json.loads((ROOT.parent / "e15_the_funnel" / "e15_numbers.json").read_text())
STEPS, SIZE, NULL, DOTS, COST, Z95 = N["steps"], N["size"], N["null"], N["dots"], N["cost"], N["z95"]
SX = 4.5                                            # centre of the side column
STANDARD, FITTED = CEDAR, ACCENT
WORSE, BETTER = ALERT, GOOD


def pct(p, places=0):
    return f"{100 * p:.{places}f}%"


def cross(m, color=ALERT):
    a, b = m.get_corner(DL) + LEFT * 0.1, m.get_corner(UR) + RIGHT * 0.1
    return Line([a[0], (a[1] + b[1]) / 2, 0], [b[0], (a[1] + b[1]) / 2, 0], stroke_width=4, color=color).set_z_index(8)


def crowd_funnel(x0=-5.6, x1=1.6, y0=-2.15, y1=2.25):
    return Funnel(x0=x0, x1=x1, y0=y0, y1=y1, p_lo=1.5, p_hi=350.0, ticks=(5, 20, 50, 100, 200, 300))


class ZPile:
    """A pile of z-values in bins half a unit wide, with room for bell curves over it."""

    def __init__(self, x0, x1, y0, y1, top, lo=-6.0, hi=6.0, width=0.5):
        self.x0, self.x1, self.y0, self.y1, self.top, self.lo, self.hi, self.width = x0, x1, y0, y1, top, lo, hi, width

    def X(self, z):
        return self.x0 + (self.x1 - self.x0) * (z - self.lo) / (self.hi - self.lo)

    def H(self, count):
        return (self.y1 - self.y0) * count / self.top

    def axis(self, label="z: distance from the reference, in units of what luck allows", ticks=(-6, -4, -2, 0, 2, 4, 6), size=15):
        g = VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], stroke_width=3, color=MUTED), *[VGroup(Line([self.X(v), self.y0, 0], [self.X(v), self.y0 - 0.09, 0], stroke_width=2, color=MUTED), txt(str(v).replace("-", "\u2212"), 14, MUTED).move_to([self.X(v), self.y0 - 0.26, 0])) for v in ticks])
        if label:
            g.add(side(label, size=size).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.56, 0]))
        return g

    def bars(self, counts, color=PAPER, opacity=0.85):
        w = (self.x1 - self.x0) * self.width / (self.hi - self.lo)
        g = VGroup()
        for k, c in enumerate(counts):
            h = max(self.H(c), 0.002)
            g.add(Rectangle(width=w * 0.9, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity if c else 0.0).move_to([self.X(self.lo + (k + 0.5) * self.width), self.y0 + h / 2, 0]))
        return g

    def curve(self, total, mean=0.0, sd=1.0, color=STANDARD, width=4):
        f = lambda z: total * self.width * float(np.exp(-0.5 * ((z - mean) / sd) ** 2) / (sd * np.sqrt(2 * np.pi)))
        return ParametricFunction(lambda z: np.array([self.X(z), self.y0 + self.H(f(z)), 0.0]), t_range=[self.lo, self.hi, 0.05], color=color, stroke_width=width).set_z_index(4)

    def cuts(self, color=ALERT):
        return VGroup(*[DashedLine([self.X(s * Z95), self.y0, 0], [self.X(s * Z95), self.y1, 0], dash_length=0.07, stroke_width=2, color=color) for s in (-1, 1)])


class Knob:
    """The crowd's knob: how much providers truly differ, with four marked settings."""

    def __init__(self, cx, cy, length=3.2):
        self.settings = N["knob"]
        self.x0, self.x1, self.y = cx - length / 2, cx + length / 2, cy
        self.track = VGroup(Line([self.x0, cy, 0], [self.x1, cy, 0], stroke_width=4, color=MUTED), *[VGroup(Line([self.X(t), cy - 0.1, 0], [self.X(t), cy + 0.1, 0], stroke_width=3, color=MUTED), txt(f"{t:g}", 15, MUTED).move_to([self.X(t), cy - 0.32, 0])) for t in self.settings],
                            side("how much providers truly differ", size=15, color=PAPER).move_to([cx, cy + 0.42, 0]))
        self.handle = Dot([self.X(self.settings[0]), cy, 0], radius=0.15, color=ACCENT).set_z_index(5)

    def X(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.settings[-1]

    def to(self, t):
        return self.handle.animate.move_to([self.X(t), self.y, 0])


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        FL, FR = crowd_funnel(-6.4, -1.0, -1.25, 1.75), crowd_funnel(1.2, 6.6, -1.25, 1.75)

        def panel(F, dots, key, title, note):
            ax = F.axes(x_label="precision", y_label="ratio")
            pts = VGroup(*[F.dot(d["precision"], d["ratio"], ACCENT if (d[key] and not d["planted"]) else PAPER, 0.045, 0.85) for d in dots])
            return VGroup(ax, F.edges(), pts, txt(title, 19, PAPER, weight=SEMIBOLD).move_to([(F.x0 + F.x1) / 2 + 0.3, F.y1 + 1.05, 0]), side(note, size=16, color=ACCENT).move_to([(F.x0 + F.x1) / 2 + 0.3, F.y1 + 0.68, 0]))

        differ = panel(FR, DOTS, "out0", "providers that truly differ a little", f"{NULL['outside'][0]} of {N['ordinary']} outside: a quarter")
        level = panel(FL, E15["level"]["dots"], "out", "identical providers", f"{E15['level']['outside']} of {N['ordinary']} outside: about one in twenty")
        with self.nar("s1_1") as seg:
            self.play(FadeIn(VGroup(differ[0], differ[1], differ[3])), run_time=1.1)
            self.play(FadeIn(differ[2], lag_ratio=0.004), run_time=1.3)
            seg.wait_until(seg.word(0, "and a quarter of them"))
            self.play(FadeIn(differ[4]), run_time=0.7)

        with self.nar("s1_2") as seg:
            self.play(FadeIn(level), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(Indicate(differ[4], color=PAPER, scale_factor=1.08), run_time=0.9)

        q1, q2 = big("a quarter of them outliers?", size=24), big("a broken test?", size=24)
        qs = VGroup(q1, q2).arrange(RIGHT, buff=1.4).move_to([0, -2.3, 0])
        answer = side("neither: the test is answering a question that has stopped being useful", size=18, color=ACCENT).move_to([0, -2.85, 0])
        with self.nar("s1_3", gap=0.8) as seg:
            self.play(FadeIn(q1), run_time=0.7)
            seg.wait_until(seg.word(0, "Or is something wrong"))
            self.play(FadeIn(q2), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(Create(cross(q1)), Create(cross(q2)), FadeIn(answer), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        title_card(self, "s2_1", 19, "Wider than Chance", "what a flag should mean")


# =================================================================================== S03
class S03_Knob(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Turn the knob")
        P = ZPile(-5.9, 1.9, -1.9, 1.5, 50.0)
        K = Knob(SX, 2.2)
        axis, cuts = P.axis(), P.cuts()
        bell = P.curve(N["ordinary"])
        bars = P.bars(STEPS[0]["hist"])
        bell_l = side("the bell curve: what luck alone gives", size=15, color=STANDARD).move_to([P.X(4.0), P.y0 + P.H(42), 0])

        def readout(step):
            return VGroup(VGroup(side("flagged, of the 194", size=16, color=PAPER), big(str(step["flags"]), size=44, color=ALERT)).arrange(DOWN, buff=0.06), VGroup(side("spread of the pile", size=16, color=PAPER), big(f"{step['sd']:.2f}", size=30)).arrange(DOWN, buff=0.06)).arrange(DOWN, buff=0.4).move_to([SX, -0.2, 0])

        read = readout(STEPS[0])
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(K.track), FadeIn(K.handle), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(axis), FadeIn(bars, lag_ratio=0.03), run_time=1.3)
            seg.wait_until(seg.word(1, "hugs the bell curve"))
            self.play(Create(bell), FadeIn(bell_l), run_time=1.0)
            seg.wait_until(seg.e(1) - 1.9)
            self.play(FadeIn(cuts), FadeIn(read), run_time=0.8)

        with self.nar("s3_2") as seg:
            for k, step in enumerate(STEPS[1:]):
                seg.wait_until([seg.s(1), seg.word(1, "then 35") - 0.5, seg.word(1, "then 48") - 0.6][k])
                new = readout(step)
                self.play(K.to(step["tau"]), Transform(bars, P.bars(step["hist"])), Transform(read, new), run_time=0.9)

        odds = VGroup(side("at this setting, a typical provider's odds are", size=16, color=PAPER), big(f"{pct(N['odds']['above'])} above the reference,", size=20, color=ACCENT), big(f"or {pct(N['odds']['below'])} below", size=20, color=ACCENT),
                      side("not much, but real", size=16, color=PAPER)).arrange(DOWN, buff=0.1)
        odds = fit_width(odds, 4.7).move_to([SX, -2.2, 0])
        with self.nar("s3_3", gap=0.8) as seg:
            self.play(read.animate.shift(UP * 0.55), FadeIn(odds), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S04
class S04_Large(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "The large ones go first")
        F = crowd_funnel()
        axes, edges = F.axes(), F.edges()
        colour = lambda d: ALERT if (d["flag0"] and not d["planted"]) else PAPER
        dots = VGroup(*[F.dot(d["precision"], d["ratio"], colour(d), 0.05, 0.85) for d in DOTS])

        def tally(label, total, hit, share, y):
            grid = VGroup(*[Dot(radius=0.06, color=ALERT if k < hit else MUTED) for k in range(total)]).arrange_in_grid(cols=16, buff=0.07)
            return VGroup(side(label, size=16, color=PAPER), grid, VGroup(big(pct(share), size=32, color=ALERT), side("flagged", size=16, color=PAPER)).arrange(RIGHT, buff=0.2)).arrange(DOWN, buff=0.14).move_to([SX, y, 0])

        large = tally(f"the {SIZE['large_n']} with 200 patients or more", SIZE["large_n"], SIZE["large_flagged"], SIZE["large"], 1.2)
        small = tally(f"the {SIZE['small_n']} with fewer than 50", SIZE["small_n"], SIZE["small_flagged"], SIZE["small"], -1.3)
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(axes), FadeIn(edges), FadeIn(dots, lag_ratio=0.004), run_time=1.6)
            seg.wait_until(seg.word(0, "Of the providers with"))
            self.play(FadeIn(large), run_time=0.8)
            seg.wait_until(seg.word(0, "Of those with fewer"))
            self.play(FadeIn(small), run_time=0.8)

        P = ZPile(-5.9, 0.9, -1.9, 0.6, 1.0)
        dens = lambda z, sd: float(np.exp(-0.5 * (z / sd) ** 2) / sd)
        narrow = ParametricFunction(lambda z: np.array([P.X(z), P.y0 + 2.3 * dens(z, 1.0), 0.0]), t_range=[-6, 6, 0.05], color=STANDARD, stroke_width=4)
        wide = ParametricFunction(lambda z: np.array([P.X(z), P.y0 + 2.3 * dens(z, SIZE["sd"]), 0.0]), t_range=[-6, 6, 0.05], color=FITTED, stroke_width=4).set_z_index(4)
        shade = VGroup(*[Polygon(*[np.array([P.X(z), P.y0 + 2.3 * dens(z, SIZE["sd"]), 0.0]) for z in np.linspace(a, b, 30)], np.array([P.X(b), P.y0, 0.0]), np.array([P.X(a), P.y0, 0.0]), stroke_width=0, fill_color=ALERT, fill_opacity=0.35) for a, b in ((-6.0, -Z95), (Z95, 6.0))])
        line = VGroup(side("the spread of a provider's z", size=17, color=PAPER), MathTex(r"\sqrt{\,1 + \frac{\text{true spread}^2}{\text{standard error}^2}\,}", font_size=34, color=PAPER)).arrange(RIGHT, buff=0.4).move_to([-2.4, 2.15, 0])
        worked = VGroup(side(f"known to within {SIZE['se']}, with a true spread of {N['knob'][-1]}:", size=16, color=PAPER), big(f"{SIZE['sd']:.1f} times the spread of chance alone", size=22, color=FITTED), big(f"flagged {pct(SIZE['flagged'])} of the time", size=22, color=ALERT)).arrange(DOWN, buff=0.14)
        worked = fit_width(worked, 4.8).move_to([SX - 0.3, -0.3, 0])
        names = VGroup(side("chance alone", size=15, color=STANDARD).move_to([P.X(0), P.y0 + 2.55, 0]), side("this provider", size=15, color=FITTED).move_to([P.X(3.7), P.y0 + 0.95, 0]))
        with self.nar("s4_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(line), FadeIn(P.axis(label="z")), Create(narrow), FadeIn(names[0]), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(Create(wide), FadeIn(names[1]), FadeIn(worked[0]), run_time=1.0)
            seg.wait_until(seg.word(1, "Its z has three times"))
            self.play(FadeIn(worked[1]), run_time=0.7)
            seg.wait_until(seg.word(1, "and it is flagged"))
            self.play(FadeIn(P.cuts()), FadeIn(shade), FadeIn(worked[2]), run_time=0.8)

        x0, x1 = -5.2, 2.2
        X = lambda v: x0 + (x1 - x0) * (v + 1.0) / 2.0                         # a scale for a provider's number about the reference, from -1 to 1
        ref = VGroup(DashedLine([X(0), -1.6, 0], [X(0), 1.9, 0], dash_length=0.1, stroke_width=2.5, color=STANDARD), side("the reference", size=15, color=STANDARD).move_to([X(0), 2.15, 0]))
        true = N["knob"][-1]

        def interval(label, se, y, color):
            lo, hi = true - Z95 * se, true + Z95 * se
            return VGroup(Line([X(max(lo, -1.0)), y, 0], [X(min(hi, 1.0)), y, 0], stroke_width=6, color=color), Dot([X(true), y, 0], radius=0.11, color=color).set_z_index(5), side(label, size=16, color=PAPER).move_to([X(true), y + 0.38, 0]))

        a = interval(f"a small provider: standard error {SIZE['se_small']:.2f}", SIZE["se_small"], 0.8, MUTED)
        b = interval(f"our largest: standard error {SIZE['se_min']:.2f}", SIZE["se_min"], -0.6, ALERT)
        same = side("the same true distance from the reference", size=16, color=PAPER).move_to([X(true), -1.5, 0])
        moral = VGroup(big("not worse:", size=24), big("measured better", size=24, color=ACCENT)).arrange(DOWN, buff=0.12).move_to([SX + 0.2, 0.2, 0])
        with self.nar("s4_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(ref), FadeIn(a), FadeIn(b), FadeIn(same), run_time=1.2)
            seg.wait_until(seg.word(0, "They are measured better"))
            self.play(FadeIn(moral), run_time=0.8)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S05
class S05_Question(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Nothing is wrong with the test")

        def box(head, question, color, y):
            c = card(9.6, 1.9).move_to([0, y, 0])
            return VGroup(c, side(head, size=16, color=color).move_to(c.get_top() + DOWN * 0.42), big(question, size=28, color=PAPER).move_to(c.get_center() + DOWN * 0.22))

        old = box("the standard test asks", "is this provider exactly at the reference?", STANDARD, 1.2)
        nobody = side("every flag is true; but with enough patients, nobody is exactly at the reference", size=17, color=PAPER).move_to([0, -0.15, 0])
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.word(0, "Every one of those flags"))
            self.play(FadeIn(old), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(nobody), run_time=0.8)

        new = box("a better question", "is this provider unusual, among providers?", ACCENT, -1.6)
        with self.nar("s5_2", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "is this provider unusual") - 0.4)
            self.play(old.animate.set_opacity(0.35), FadeIn(new, shift=UP * 0.15), run_time=1.0)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S06
class S06_Empirical(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "A null drawn from the providers")
        names = ("small", "medium", "large")
        piles = VGroup()
        for k, g in enumerate(("1", "2", "3")):
            cx = -4.5 + 4.5 * k
            P = ZPile(cx - 1.95, cx + 1.95, -1.5, 1.3, 15.0)
            counts = NULL["groups_z"][g]
            lo, hi, _ = NULL["bounds"][k]
            piles.add(VGroup(P.axis(label="", ticks=(-6, -3, 0, 3, 6)), P.bars(counts), P.curve(sum(counts)), P.curve(sum(counts), NULL["centres"][k], NULL["spreads"][k], FITTED),
                             VGroup(txt(f"{names[k]} providers", 19, PAPER, weight=SEMIBOLD), side(f"{lo} to {hi} patients", size=15)).arrange(DOWN, buff=0.06).move_to([cx, 2.25, 0]),
                             VGroup(side("fitted spread", size=16, color=PAPER), big(f"{NULL['spreads'][k]:.2f}", size=28, color=FITTED)).arrange(RIGHT, buff=0.2).move_to([cx, -2.3, 0])))
        key = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4, color=STANDARD), side("the bell curve, taken on faith", size=15, color=PAPER)).arrange(RIGHT, buff=0.15), VGroup(Line(ORIGIN, RIGHT * 0.5, stroke_width=4, color=FITTED), side("the empirical null: fitted to the bulk of the z-values", size=15, color=PAPER)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8).move_to([0, -2.85, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), *[FadeIn(VGroup(p[0], p[1], p[2], p[4])) for p in piles], FadeIn(key[0]), run_time=1.5)
            seg.wait_until(seg.word(0, "and fit one to the providers"))
            self.play(*[Create(p[3]) for p in piles], run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(key[1]), run_time=0.7)
            seg.wait_until(seg.word(2, "The fitted spreads are"))
            self.play(LaggedStart(*[FadeIn(p[5]) for p in piles], lag_ratio=0.5), run_time=2.2)

        st, em = N["all_flags"]["standard"], N["all_flags"]["empirical"]

        def count(head, t, color, x):
            return VGroup(side(head, size=17, color=PAPER), big(str(t[0]), size=64, color=color), side(f"{t[1]} ordinary, {t[2]} planted", size=16)).arrange(DOWN, buff=0.1).move_to([x, 0.9, 0])

        c0, c1 = count("flagged against the bell curve", st, STANDARD, -3.0), count("flagged against its own group's curve", em, FITTED, 3.0)
        arrow = Arrow([-1.0, 0.9, 0], [1.0, 0.9, 0], buff=0, stroke_width=4, color=MUTED, max_tip_length_to_length_ratio=0.15)
        redraw = VGroup(side(f"over {NULL['redraws']} redraws of the crowd, ordinary providers flagged", size=17, color=PAPER), VGroup(big(pct(NULL["standard_rate"]), size=30, color=STANDARD), side("then", size=16), big(pct(NULL["empirical_rate"]), size=30, color=FITTED)).arrange(RIGHT, buff=0.3)).arrange(DOWN, buff=0.14).move_to([0, -1.6, 0])
        with self.nar("s6_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(c0), run_time=0.7)
            seg.wait_until(seg.word(0, "and 13 are flagged") - 0.2)
            self.play(GrowArrow(arrow), FadeIn(c1), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(redraw), run_time=0.9)

        F = crowd_funnel()
        axes = F.axes()
        old_edges = F.edges(color=STANDARD, width=2.5)
        wider = VGroup()
        for g in (1, 2, 3):
            ps = [d["precision"] for d in DOTS if d["group"] == g]
            a, b, c, s = float(np.sqrt(min(ps))), float(np.sqrt(max(ps))), NULL["funnel_centres"][g - 1], NULL["funnel_spreads"][g - 1]
            for sign in (-1, 1):
                wider.add(ParametricFunction(lambda t, c=c, s=s, sign=sign: F.P(t * t, min(max(1.0 + (c + sign * Z95 * s) / t, F.r_lo), F.r_hi)), t_range=[a, b, 0.05], color=FITTED, stroke_width=3.2).set_stroke(opacity=0.5 + 0.2 * (g - 1)).set_z_index(3))
        dots = VGroup(*[F.dot(d["precision"], d["ratio"], ACCENT if (d["out1"] and not d["planted"]) else PAPER, 0.045, 0.8) for d in DOTS])
        lim, p280 = NULL["limits_280"], NULL["precision_280"]
        seg0 = Line(F.P(p280, lim[0]), F.P(p280, lim[1]), stroke_width=7, color=STANDARD).set_z_index(6)
        seg1 = Line(F.P(p280, lim[2]), F.P(p280, lim[3]), stroke_width=4, color=FITTED).set_z_index(5)
        moved = VGroup(side("a provider of 280 patients: its limits", size=16, color=PAPER), VGroup(big(f"{lim[0]:.2f} and {lim[1]:.2f}", size=22, color=STANDARD), side("out to", size=15), big(f"{lim[2]:.2f} and {lim[3]:.2f}", size=22, color=FITTED)).arrange(DOWN, buff=0.08)).arrange(DOWN, buff=0.14)
        moved = fit_width(moved, 4.6).move_to([SX, 0.9, 0])
        out = VGroup(side("ordinary providers outside the limits", size=16, color=PAPER), VGroup(big(str(NULL["outside"][0]), size=28, color=STANDARD), side("then", size=15), big(str(NULL["outside"][1]), size=28, color=FITTED)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.1).move_to([SX, -1.4, 0])
        with self.nar("s6_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(axes), FadeIn(old_edges), FadeIn(dots, lag_ratio=0.004), run_time=1.3)
            self.play(LaggedStart(*[Create(w) for w in wider], lag_ratio=0.1), FadeIn(out), run_time=1.5)
            seg.wait_until(seg.s(0) + 4.6)
            self.play(FadeIn(seg0), FadeIn(seg1), FadeIn(moved), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S07
class S07_Costs(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "What it costs")
        six = sorted(COST["planted"], key=lambda d: (d["kind"] != "worse", d["n"]))
        xs = [-5.0 + 2.0 * k for k in range(6)]

        def verdict(ok):
            return tick_mark(s=0.9) if ok else VGroup(Line(UL * 0.1, DR * 0.1, stroke_width=4, color=MUTED), Line(DL * 0.1, UR * 0.1, stroke_width=4, color=MUTED))

        cols = VGroup()
        for d, x in zip(six, xs):
            c = WORSE if d["kind"] == "worse" else BETTER
            cols.add(VGroup(Dot([x, 1.5, 0], radius=0.14, color=c), VGroup(txt(f"truly {d['kind']}", 16, c, weight=SEMIBOLD), side(f"{d['n']} patients", size=15, color=PAPER)).arrange(DOWN, buff=0.04).move_to([x, 0.85, 0]), verdict(d["standard"]).move_to([x, -0.2, 0]), verdict(d["empirical"]).move_to([x, -1.2, 0])))
        rows = VGroup(side("the standard test", size=16, color=STANDARD).move_to([-5.0, 0.2, 0], aligned_edge=LEFT), side("the empirical null", size=16, color=FITTED).move_to([-5.0, -0.8, 0], aligned_edge=LEFT))
        totals = VGroup(big(f"{sum(d['standard'] for d in six)} caught", size=24, color=STANDARD).move_to([0, -2.0, 0]), big(f"{sum(d['empirical'] for d in six)} caught", size=24, color=FITTED).move_to([0, -2.0, 0]))
        totals.arrange(RIGHT, buff=1.2).move_to([0, -2.1, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), LaggedStart(*[FadeIn(VGroup(c[0], c[1])) for c in cols], lag_ratio=0.1), run_time=1.5)
            seg.wait_until(seg.word(0, "the standard test caught four"))
            self.play(FadeIn(rows[0]), *[FadeIn(c[2]) for c in cols], FadeIn(totals[0]), run_time=0.8)
            seg.wait_until(seg.word(0, "This one catches three"))
            self.play(FadeIn(rows[1]), *[FadeIn(c[3]) for c in cols], FadeIn(totals[1]), run_time=0.8)

        zero = COST["zero"]
        K = Knob(-3.6, 1.7)
        narrow = VGroup(side("with the knob at zero, this crowd's fitted spreads", size=17, color=PAPER), big("   ".join(f"{v:.2f}" for v in zero["spreads"]), size=28, color=FITTED), side("too narrow: they should all be 1", size=16, color=ALERT)).arrange(DOWN, buff=0.12).move_to([-3.6, 0.0, 0])
        flags = VGroup(side("ordinary providers flagged", size=16, color=PAPER), VGroup(big(str(zero["empirical"]), size=30, color=FITTED), side("where the standard test flags", size=15), big(str(zero["standard"]), size=30, color=STANDARD)).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.1).move_to([-3.6, -1.7, 0])
        assume = VGroup(card(5.4, 2.6), VGroup(txt("it assumes most providers are ordinary", 18, ALERT, weight=SEMIBOLD), txt("if many are not,", 18, PAPER), txt("the curve widens to hide them", 18, PAPER)).arrange(DOWN, buff=0.16)).move_to([3.7, 0.0, 0])
        with self.nar("s7_2") as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            seg.wait_until(seg.word(0, "With the knob back at zero"))
            self.play(FadeIn(K.track), FadeIn(K.handle), FadeIn(narrow), run_time=1.0)
            seg.wait_until(seg.word(0, "and flagged 20"))
            self.play(FadeIn(flags), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(assume), run_time=0.9)

        means = VGroup(card(5.6, 2.9), VGroup(side("it has not made anything more exact", size=17, color=PAPER), side("it has changed the question", size=17, color=PAPER), txt("a flag now means", 19, MUTED), big("unusual among providers", size=24, color=ACCENT)).arrange(DOWN, buff=0.18)).move_to([-3.4, 0.1, 0])
        others = VGroup(txt("other answers", 19, PAPER, weight=SEMIBOLD), *[VGroup(Dot(radius=0.06, color=MUTED), txt(s, 18, PAPER)).arrange(RIGHT, buff=0.2) for s in ("shrunken estimates (Episode 17)", "an allowance for extra spread, fixed in advance", "intervals, and no flags at all")]).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        others = fit_width(others, 5.6).move_to([3.6, 0.1, 0])
        with self.nar("s7_3", gap=0.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects if m is not tag], run_time=0.6)
            self.play(FadeIn(means[0]), FadeIn(VGroup(means[1][0], means[1][1])), run_time=1.0)
            seg.wait_until(seg.word(0, "A flag now means"))
            self.play(FadeIn(VGroup(means[1][2], means[1][3])), run_time=0.8)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(others), run_time=0.9)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        bell = lambda sd, color: VMobject(color=color, stroke_width=3.5).set_points_smoothly([np.array([0.28 * z, 0.75 * float(np.exp(-0.5 * (z / sd) ** 2)) / sd, 0.0]) for z in np.linspace(-3.6, 3.6, 40)])
        icon1 = VGroup(bell(1.0, STANDARD), bell(1.9, FITTED))
        icon2 = VGroup(VGroup(Line(UP * 0.35, DOWN * 0.35, stroke_width=3, color=STANDARD), Dot(RIGHT * 0.35, radius=0.09, color=PAPER)), txt("or", 16, MUTED), VGroup(*[Dot([0.16 * k, 0.1 * ((k * 7) % 3 - 1), 0], radius=0.05, color=MUTED) for k in range(5)], Dot([1.25, 0.25, 0], radius=0.09, color=ACCENT))).arrange(RIGHT, buff=0.35)
        icon3 = VGroup(Dot(radius=0.12, color=PAPER), Circle(radius=0.26, stroke_color=ALERT, stroke_width=3), tex("?", 30, ACCENT).shift(RIGHT * 0.6))
        icons = [icon1, icon2, icon3]
        caps = [["When providers truly differ a", "little, z spreads wider than", "chance: most for large providers"], ["Exactly at the reference?", "Or unusual among providers?", "Two different questions"], ["Choosing between them is", "choosing what a flag", "should mean"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 1.0, 0])
            captions.add(fit_width(VGroup(*[txt(s, 19, PAPER) for s in cp]).arrange(DOWN, buff=0.1), 3.6).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1", gap=0.8) as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)
        self.play(*clear(self), run_time=1.0)


# =================================================================================== S09
class S09_Close(EpisodeScene):
    def construct(self):
        xs = (-5.1, -1.7, 1.7, 5.1)
        marks = VGroup(*[VGroup(Line(UP * 0.25, DOWN * 0.25, stroke_width=3, color=PAPER), Dot(UP * 0.12 * float(np.sin(1.9 * k)), radius=0.06, color=PAPER)) for k in range(7)]).arrange(RIGHT, buff=0.18)
        meter = Meter(PAPER, width=1.3)
        ratio = VGroup(txt("observed", 20, PAPER, weight=MEDIUM), Line(LEFT * 0.75, RIGHT * 0.75, stroke_width=3, color=PAPER), txt("expected", 20, PAPER, weight=MEDIUM)).arrange(DOWN, buff=0.12)
        f = Funnel(x0=-1.1, x1=1.1, y0=-0.55, y1=0.55, p_lo=1.5, p_hi=120.0, r_lo=0.0, r_hi=2.0)
        funnel = VGroup(Line([f.x0, f.Y(1), 0], [f.x1, f.Y(1), 0], stroke_width=2, color=CEDAR), f.edges(width=3), *[f.dot(p, r, c, 0.055) for p, r, c in ((12, 1.75, ALERT), (30, 1.15, PAPER), (60, 0.9, PAPER), (95, 1.04, PAPER))])
        pictures = [marks, meter, ratio, funnel]
        lines = [("one intercept", "for every provider"), ("a fit that balances", "observed against expected"), ("what the reference would have", "done with the same patients"), ("a test that knows", "how far luck can reach")]
        steps = VGroup()
        for x, pic, line in zip(xs, pictures, lines):
            pic.move_to([x, 0.7, 0])
            steps.add(VGroup(pic, fit_width(VGroup(*[side(t, size=16, color=PAPER) for t in line]).arrange(DOWN, buff=0.08), 3.1).move_to([x, -0.6, 0])))
        head = VGroup(txt("the logistic fixed-effect model", 26, PAPER, weight=SEMIBOLD), side("from an unfair comparison to a flag you can defend", size=18, color=ACCENT)).arrange(DOWN, buff=0.14).move_to([0, 2.5, 0])
        joins = VGroup(*[Arrow([xs[k] + 1.25, 0.7, 0], [xs[k + 1] - 1.25, 0.7, 0], buff=0, stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.25) for k in range(3)])
        cues = ("One intercept for every provider", "A fit that balances", "A ratio that asks", "And a test that knows")
        with self.nar("s9_1", gap=1.0) as seg:
            self.play(FadeIn(head[0]), run_time=0.9)
            seg.wait_until(seg.word(0, "from an unfair comparison"))
            self.play(FadeIn(head[1]), run_time=0.7)
            for k in range(4):
                seg.wait_until(seg.word(1, cues[k]))
                self.play(FadeIn(steps[k], shift=UP * 0.1), *([GrowArrow(joins[k - 1])] if k else []), run_time=0.9)
        series_end_card(self, "s9_2", "The Logistic Fixed-Effect Model  \u00b7  nineteen episodes")
