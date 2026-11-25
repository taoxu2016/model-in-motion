"""Model in Motion · The Logistic Fixed-Effect Model · Episode 2: Odds and the S-Curve.

Render one scene:   manim -qh --media_dir build/media episode/episode02.py S06_Curve
Every scene reads audio/manifest.json; each `with self.nar("sX_Y") as seg:` block starts that
voiceover clip and holds the scene until the clip (plus a short gap) has finished.
All content stays above y = -3.0 so that burned-in captions never cover it.
"""
import sys
from pathlib import Path

import os  # noqa: E402

os.environ["MIM_EPISODE"] = str(Path(__file__).resolve().parents[1])   # this episode's folder
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))           # the repository root, for the shared mim package
from mim.common import *  # noqa: E402,F403

LN4 = float(np.log(4))


def pulse(mobs, k=1.3):
    return [m.animate(rate_func=there_and_back).scale(k) for m in mobs]


def expit(x):
    return 1 / (1 + np.exp(-x))


def logit(p):
    return float(np.log(p / (1 - p)))


def signed(v, places=2):
    return ("+" if v > 0 else "\u2212" if v < 0 else "") + f"{abs(v):.{places}f}"


class Ruler:
    """A horizontal scale: value -> x.  `ends` adds an arrow tip where the scale runs on forever."""

    def __init__(self, y, lo, hi, x0=-4.0, x1=5.2, ticks=(), labels=None, title="", ends=(False, False)):
        self.y, self.lo, self.hi, self.x0, self.x1 = y, lo, hi, x0, x1
        a = np.array([x0 - (0.5 if ends[0] else 0), y, 0.0])
        b = np.array([x1 + (0.5 if ends[1] else 0), y, 0.0])
        self.line = Line(a, b, stroke_width=5, color=PAPER)
        self.tips = VGroup()
        if ends[0]:
            self.tips.add(Triangle(fill_color=PAPER, fill_opacity=1, stroke_width=0).scale(0.11).rotate(PI / 2).move_to(a + LEFT * 0.06))
        if ends[1]:
            self.tips.add(Triangle(fill_color=PAPER, fill_opacity=1, stroke_width=0).scale(0.11).rotate(-PI / 2).move_to(b + RIGHT * 0.06))
        self.ticks = VGroup(*[Line([self.X(v), y, 0], [self.X(v), y - 0.12, 0], stroke_width=2, color=MUTED) for v in ticks])
        self.labels = VGroup(*[txt(s, 18, MUTED).move_to([self.X(v), y - 0.34, 0]) for v, s in (labels or {}).items()])
        self.title = txt(title, 20, MUTED, font=SERIF, slant=ITALIC)
        self.title.move_to([a[0] - 0.35 - self.title.width / 2, y, 0])
        self.g = VGroup(self.line, self.tips, self.ticks, self.labels, self.title)

    def X(self, v):
        return self.x0 + (self.x1 - self.x0) * (v - self.lo) / (self.hi - self.lo)

    def P(self, v, dy=0.0):
        return np.array([self.X(v), self.y + dy, 0.0])


def prob_ruler(y, x0=-4.0, x1=5.2):
    return Ruler(y, 0, 1, x0, x1, ticks=[k / 10 for k in range(11)], labels={0: "0%", 0.5: "50%", 1: "100%"}, title="probability")


def odds_ruler(y, x0=-4.0, x1=5.2):
    return Ruler(y, 0, 5, x0, x1, ticks=range(6), labels={k: str(k) for k in range(6)}, title="odds", ends=(False, True))


def logit_ruler(y, x0=-3.5, x1=4.7):
    return Ruler(y, -4, 4, x0, x1, ticks=range(-4, 5), labels={k: signed(k, 0) for k in range(-4, 5, 2)}, title="log-odds",
                 ends=(True, True))


def pill(s, size=21):
    t = txt(s, size, PAPER)
    box = RoundedRectangle(corner_radius=0.16, width=t.width + 0.5, height=0.52, stroke_color=FAINT, stroke_width=2,
                           fill_color=INK_2, fill_opacity=1)
    return VGroup(box, t)


def hero_chip(r=0.16):
    u = Unit(PAPER, True, True, r=r)
    u.chip.set_stroke(width=28 * r)
    return u


def risk_chip(p, r=0.38, color=PAPER):
    """The series' risk chip: a disc whose shaded slice is the patient's probability."""
    ring = Circle(radius=r, stroke_color=color, stroke_width=3).set_fill(INK_2, opacity=1)
    wedge = Sector(radius=r * 0.86, angle=-p * TAU, start_angle=PI / 2, stroke_width=0, fill_color=color, fill_opacity=0.9)
    return VGroup(ring, wedge)


def step_arrow(a, b, color=ACCENT, width=4, tip=0.25):
    return Arrow(a, b, buff=0, stroke_width=width, color=color, max_tip_length_to_length_ratio=tip, max_stroke_width_to_length_ratio=20)


FACTORS = [("age 81", 25, 0.45), ("diabetes", 30, 0.50), ("third stay this year", 35, 0.55)]   # name, points, risk alone
STEPS = [logit(p) - logit(0.2) for _, _, p in FACTORS]                                         # 1.19, 1.39, 1.59


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        R = prob_ruler(-0.9, x0=-4.4, x1=3.6)
        big = hero_chip(0.3).move_to([0, 1.55, 0])
        spots = [(-3.9, 2.35), (3.9, 2.35), (0, 2.95)]
        pills = VGroup(*[pill(w).move_to([x, y, 0]) for (w, _, _), (x, y) in zip(FACTORS, spots)])
        links = VGroup(*[Line(big.get_center() + 0.5 * (pl.get_center() - big.get_center()) / np.linalg.norm(pl.get_center() - big.get_center()),
                              pl.get_center() + (big.get_center() - pl.get_center()) / np.linalg.norm(pl.get_center() - big.get_center()) * 0.4,
                              stroke_width=1.5, color=FAINT) for pl in pills[:2]])
        with self.nar("s1_1") as seg:
            self.play(GrowFromCenter(big), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(pl, shift=(pl.get_center() - big.get_center()) * 0.06) for pl in pills], lag_ratio=0.25),
                      FadeIn(links), run_time=1.6)
            seg.wait_until(seg.word(0, "one ruler for risk"))
            self.play(FadeIn(R.g, shift=UP * 0.15), run_time=1.2)

        mk = hero_chip(0.16).move_to(R.P(0.2, 0.3))
        lab = txt("20%", 26, PAPER, weight=SEMIBOLD).move_to(R.P(0.2, 0.78))
        row = VGroup(*[VGroup(pill(w), txt(f"+{k}", 26, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.22) for w, k, _ in FACTORS])
        row.arrange(RIGHT, buff=0.7).move_to([0, 2.45, 0])
        with self.nar("s1_2") as seg:
            seg.wait_until(seg.s(1))
            self.play(Transform(big, mk), FadeOut(links), *[Transform(pills[k], row[k][0]) for k in range(3)], run_time=1.4)
            self.play(FadeIn(lab, shift=UP * 0.1), run_time=0.5)
            seg.wait_until(seg.word(1, "then add points"))
            self.play(LaggedStart(*[FadeIn(row[k][1], shift=LEFT * 0.1) for k in range(3)], lag_ratio=0.2), run_time=1.0)

        total, segs = 0.2, VGroup()
        with self.nar("s1_3", gap=0.2) as seg:
            for k, cue in enumerate(("Age eighty-one", "Diabetes", "A third hospital stay")):
                seg.wait_until(seg.word(0, cue))
                new = total + FACTORS[k][1] / 100
                bar = Line(R.P(total), R.P(new), stroke_width=10, color=ACCENT if new <= 1 else ALERT)
                pts = txt(f"+{FACTORS[k][1]}", 20, ACCENT if new <= 1 else ALERT, weight=SEMIBOLD).move_to(R.P((total + new) / 2, -0.75))
                newlab = txt(f"{round(100 * new)}%", 26, PAPER if new <= 1 else ALERT, weight=SEMIBOLD).move_to(R.P(new, 0.78))
                self.play(*pulse([pills[k], row[k][1]], 1.12), run_time=0.5)
                self.play(big.animate(path_arc=-1.3).move_to(R.P(new, 0.3)), Create(bar), FadeIn(pts), FadeOut(lab), FadeIn(newlab), run_time=1.0)
                segs.add(bar, pts)
                lab, total = newlab, new

        cross = VGroup(Line(UL * 0.16, DR * 0.16, stroke_width=5, color=ALERT), Line(UR * 0.16, DL * 0.16, stroke_width=5, color=ALERT)).move_to(R.P(1.0, 0))
        with self.nar("s1_4", gap=0.7) as seg:
            self.play(Indicate(lab, color=ALERT, scale_factor=1.4), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Create(cross), Wiggle(big), run_time=1.2)
            seg.wait_until(seg.word(1, "on the wrong ruler"))
            self.play(Indicate(R.line, color=ALERT, scale_factor=1.0), Indicate(R.title, color=ALERT), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        mark = logo_mark(1.25)
        word = wordmark(64)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.55).move_to(UP * 1.15)
        arc = txt("THE LOGISTIC FIXED-EFFECT MODEL  \u00b7  EPISODE 2", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.75)
        title = txt("Odds and the S-Curve", 70, PAPER, weight=SEMIBOLD, font=DISPLAY).next_to(arc, DOWN, buff=0.32)
        sub = txt("how risk factors become a probability", 32, MUTED, font=SERIF, slant=ITALIC).next_to(title, DOWN, buff=0.26)
        a, dot, b, ring, scan = mark
        with self.nar("s2_1", gap=0.6) as seg:
            self.play(Create(a), Create(b), run_time=0.8)
            self.play(GrowFromCenter(dot), GrowFromCenter(ring), FadeIn(scan, shift=RIGHT * 0.6), Write(word), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(FadeIn(arc, shift=UP * 0.15), FadeIn(title, shift=UP * 0.2),
                                  FadeIn(sub, shift=UP * 0.15), lag_ratio=0.25), run_time=1.8)
        self.wait(0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S03
class S03_Odds(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "Odds")
        row = [Circle(radius=0.2, stroke_color=PAPER, stroke_width=4.5).set_fill(PAPER, opacity=0).move_to([(k - 4.5) * 0.62, 2.4, 0])
               for k in range(10)]

        def fill_to(n):
            return [row[k].animate.set_fill(opacity=1.0 if k < n else 0.0) for k in range(10)
                    if (row[k].get_fill_opacity() > 0.5) != (k < n)]

        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[GrowFromCenter(c) for c in row], lag_ratio=0.08), run_time=1.6)
            seg.wait_until(seg.word(1, "On average"))
            self.play(*fill_to(2), run_time=0.9)

        l1 = VGroup(txt("probability", 22, MUTED, font=SERIF, slant=ITALIC), txt("2 of 10", 24, PAPER), txt("=  20%", 28, PAPER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.3)
        l2 = VGroup(txt("odds", 22, MUTED, font=SERIF, slant=ITALIC), txt("2 against 8", 24, PAPER), txt("=  1 to 4  =  0.25", 28, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.3)
        l1.move_to([0, 1.55, 0])
        l2.move_to([0, 1.02, 0])
        allbox = SurroundingRectangle(VGroup(*row), color=MUTED, buff=0.14, corner_radius=0.14, stroke_width=2)
        with self.nar("s3_2") as seg:
            self.play(Create(allbox), FadeIn(l1, shift=UP * 0.1), run_time=1.1)
            seg.wait_until(seg.s(1))
            self.play(FadeOut(allbox), *[c.animate.shift(RIGHT * 0.45) for c in row[2:]], *[c.animate.shift(LEFT * 0.15) for c in row[:2]], run_time=0.8)
            self.play(FadeIn(l2, shift=UP * 0.1), run_time=0.8)

        Rp, Ro = prob_ruler(0.2), odds_ruler(-1.3)
        eta = ValueTracker(logit(0.2))
        mp, mo = Dot(radius=0.13, color=PAPER), Dot(radius=0.13, color=PAPER)
        mp.add_updater(lambda m: m.move_to(Rp.P(expit(eta.get_value()), 0.28)))
        mo.add_updater(lambda m: m.move_to(Ro.P(min(np.exp(eta.get_value()), 5.45), 0.28)))
        link = always_redraw(lambda: Line(mp.get_center() + DOWN * 0.17, mo.get_center() + UP * 0.17, stroke_width=1.5, color=MUTED).set_stroke(opacity=0.6))
        stamps = VGroup()

        def stamp(ps, os_):
            new = VGroup(txt(ps, 24, PAPER, weight=SEMIBOLD).move_to(mp.get_center() + UP * 0.42),
                         txt(os_, 24, ACCENT, weight=SEMIBOLD).move_to(mo.get_center() + UP * 0.42))
            self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
            stamps.add(*new)
            return new

        def go(p, n=None, rt=1.3):
            old = list(stamps)
            stamps.remove(*old)
            extra = fill_to(n) if n is not None else []
            self.play(eta.animate.set_value(logit(p)), *[FadeOut(o) for o in old], *extra, run_time=rt)

        with self.nar("s3_3") as seg:
            self.play(FadeIn(Rp.g), FadeIn(Ro.g), FadeOut(l1), FadeOut(l2), *[c.animate.shift(LEFT * 0.45) for c in row[2:]],
                      *[c.animate.shift(RIGHT * 0.15) for c in row[:2]], run_time=1.0)
            self.add(link, mp, mo)
            stamp("20%", "0.25")
            go(0.5, 5)
            stamp("50%", "1")
            seg.wait_until(seg.s(1))
            go(0.8, 8)
            stamp("80%", "4")

        with self.nar("s3_4", gap=0.6) as seg:
            for p, cue, o in ((0.9, "nine,", "9"), (0.99, "ninety-nine,", "99"), (0.999, "nine hundred", "999")):
                seg.wait_until(seg.word(0, cue) - 0.6)
                go(p, 9 if p == 0.9 else 10, rt=0.7)
                stamp(f"{100 * p:g}%", o)
            seg.wait_until(seg.s(1))
            self.play(Indicate(Ro.tips, color=ACCENT, scale_factor=2.2), run_time=1.0)
        mp.clear_updaters()
        mo.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S04
class S04_LogOdds(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Log-odds")
        Ro = odds_ruler(0.75)
        lo_bar = Line(Ro.P(0), Ro.P(1), stroke_width=11, color=ALERT)
        hi_bar = Line(Ro.P(1), Ro.P(5.4), stroke_width=11, color=BIRCH)
        lo_lab = txt("everyone below 50%", 19, ALERT, font=SERIF, slant=ITALIC).move_to(Ro.P(0.5, 0.45)).shift(LEFT * 0.35)
        hi_lab = txt("everyone above 50%", 19, BIRCH, font=SERIF, slant=ITALIC).move_to(Ro.P(3.2, 0.45))
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(Ro.g), run_time=1.0)
            seg.wait_until(seg.word(1, "squeezed"))
            self.play(Create(lo_bar), FadeIn(lo_lab), run_time=0.9)
            seg.wait_until(seg.word(1, "while everyone above"))
            self.play(Create(hi_bar), FadeIn(hi_lab), run_time=1.1)

        vals = [0.25, 0.5, 1, 2, 4]
        names = ["1/4", "1/2", "1", "2", "4"]
        Rl = Ruler(-0.95, -4, 4, -3.5, 4.7, ticks=[np.log(v) for v in vals], title="log-odds", ends=(True, True),
                   labels={float(np.log(v)): signed(float(np.log(v))) if v != 1 else "0" for v in vals})
        src = VGroup(*[VGroup(Line(Ro.P(v, 0.14), Ro.P(v, -0.14), stroke_width=3, color=ACCENT),
                              txt(n, 19, ACCENT, weight=SEMIBOLD).move_to(Ro.P(v, 0.42))) for v, n in zip(vals, names)])
        dst = VGroup(*[VGroup(Line(Rl.P(np.log(v), 0.14), Rl.P(np.log(v), -0.14), stroke_width=3, color=ACCENT),
                              txt(n, 19, ACCENT, weight=SEMIBOLD).move_to(Rl.P(np.log(v), 0.42))) for v, n in zip(vals, names)])
        oddsname = txt("odds", 18, ACCENT, font=SERIF, slant=ITALIC).move_to(Rl.P(np.log(4), 0.42)).shift(RIGHT * 0.75)
        with self.nar("s4_2") as seg:
            self.play(FadeOut(VGroup(lo_bar, hi_bar, lo_lab, hi_lab)), LaggedStart(*[FadeIn(s) for s in src], lag_ratio=0.15), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(Rl.line), FadeIn(Rl.tips), FadeIn(Rl.title), run_time=0.8)
            self.play(LaggedStart(*[TransformFromCopy(s, d) for s, d in zip(src, dst)], lag_ratio=0.3), run_time=seg.until(seg.e(1)) - 0.2)
            self.play(FadeIn(Rl.labels), FadeIn(oddsname), run_time=0.7)

        Rp = prob_ruler(2.3)
        eta = ValueTracker(0.0)
        marks = [Dot(radius=0.13, color=PAPER).set_z_index(4) for _ in range(3)]
        marks[0].add_updater(lambda m: m.move_to(Rp.P(expit(eta.get_value()), 0.28)))
        marks[1].add_updater(lambda m: m.move_to(Ro.P(min(np.exp(eta.get_value()), 5.45), 0.28)))
        marks[2].add_updater(lambda m: m.move_to(Rl.P(eta.get_value(), 0.28)))
        links = VGroup(*[always_redraw(lambda i=i: Line(marks[i].get_center() + DOWN * 0.17, marks[i + 1].get_center() + UP * 0.17,
                                                        stroke_width=1.5, color=MUTED).set_stroke(opacity=0.55)) for i in range(2)])
        stamps = VGroup()

        def go(p, texts, rt=1.4):
            old = list(stamps)
            stamps.remove(*old)
            self.play(eta.animate.set_value(logit(p)), *[FadeOut(o) for o in old], run_time=rt)
            if texts:
                new = VGroup(*[txt(t, 23, c, weight=SEMIBOLD).move_to(m.get_center() + UP * 0.4)
                               for t, c, m in zip(texts, (PAPER, PAPER, ACCENT), marks)])
                self.play(FadeIn(new, shift=UP * 0.08), run_time=0.4)
                stamps.add(*new)

        with self.nar("s4_3") as seg:
            self.play(FadeIn(Rp.g), FadeOut(src), FadeOut(VGroup(*[d[1] for d in dst])), FadeOut(oddsname), run_time=1.0)
            self.add(links, *marks)
            self.play(*[GrowFromCenter(m) for m in marks], run_time=0.5)
            go(0.5, ("50%", "1", "0"), rt=0.3)
            seg.wait_until(seg.s(1))
            go(0.2, ("20%", "0.25", signed(-LN4)))
            seg.wait_until(seg.word(1, "and eighty percent"))
            go(0.8, ("80%", "4", signed(LN4)))

        with self.nar("s4_4", gap=0.6) as seg:
            go(expit(-3.9), None, rt=1.8)
            self.play(Indicate(Rl.tips[0], color=ACCENT, scale_factor=2.0), run_time=0.6)
            go(expit(3.9), None, rt=2.2)
            self.play(Indicate(Rl.tips[1], color=ACCENT, scale_factor=2.0), run_time=0.6)
        for m in marks:
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S05
class S05_Steps(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Where risks add")
        Rp, Rl = prob_ruler(1.35), logit_ruler(-1.75)
        demo = step_arrow(Rl.P(0, 0.45), Rl.P(LN4, 0.45))
        demo_lab = VGroup(txt("\u00d7 4 in odds", 21, PAPER), txt("=", 21, MUTED), txt("+1.39 in log-odds", 21, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.18)
        demo_lab.move_to(Rl.P(LN4 / 2, 0.9))
        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(Rl.g), run_time=1.0)
            seg.wait_until(seg.word(0, "a risk factor is simply a step"))
            self.play(GrowArrow(demo), run_time=0.9)
            seg.wait_until(seg.word(1, "a step of"))
            self.play(FadeIn(demo_lab, shift=UP * 0.1), run_time=0.8)

        p0 = [0.05, 0.2, 0.5, 0.8]
        p1 = [float(expit(logit(p) + LN4)) for p in p0]
        dy = [0.32 + 0.34 * k for k in range(4)]

        def ring(pos):
            return Circle(radius=0.12, stroke_color=PAPER, stroke_width=3).set_fill(INK, 1).move_to(pos)

        def disc(pos):
            return Dot(pos, radius=0.125, color=PAPER)

        lr = [ring(Rl.P(logit(p), d)) for p, d in zip(p0, dy)]
        ld = [disc(Rl.P(logit(p) + LN4, d)) for p, d in zip(p0, dy)]
        la = [step_arrow(Rl.P(logit(p), d) + RIGHT * 0.16, Rl.P(logit(p) + LN4, d) + LEFT * 0.16, tip=0.2) for p, d in zip(p0, dy)]
        pr = [ring(Rp.P(p, d)) for p, d in zip(p0, dy)]
        pd = [disc(Rp.P(q, d)) for q, d in zip(p1, dy)]
        pa = [step_arrow(Rp.P(p, d) + RIGHT * 0.16, Rp.P(q, d) + LEFT * 0.16, color=PAPER, width=3.5, tip=0.1) for p, q, d in zip(p0, p1, dy)]
        pl = [txt(f"{round(100 * p)}%  \u2192  {round(100 * q)}%", 19, PAPER).next_to(pd[k], RIGHT, buff=0.22) for k, (p, q) in enumerate(zip(p0, p1))]
        with self.nar("s5_2") as seg:
            self.play(FadeOut(demo), FadeOut(demo_lab), FadeIn(Rp.g), LaggedStart(*[GrowFromCenter(r) for r in lr + pr], lag_ratio=0.06), run_time=1.4)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(d)) for a, d in zip(la, ld)], lag_ratio=0.2), run_time=1.6)

        with self.nar("s5_3") as seg:
            for k, cue in enumerate(("five percent", "Twenty becomes", "Fifty becomes", "And eighty")):
                seg.wait_until(seg.word(0, cue) - 0.1)
                self.play(GrowArrow(pa[k]), FadeIn(pd[k]), run_time=0.7)
                self.play(FadeIn(pl[k], shift=LEFT * 0.08), run_time=0.4)

        end = txt("100%", 18, ALERT, weight=SEMIBOLD).move_to(Rp.labels[2])
        with self.nar("s5_4", gap=0.6) as seg:
            self.play(*[Indicate(a, color=ACCENT, scale_factor=1.08) for a in la], run_time=1.0)
            seg.wait_until(seg.word(0, "very different jumps"))
            self.play(*[Indicate(a, color=PAPER, scale_factor=1.08) for a in pa], run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Indicate(Rp.labels[2], color=ACCENT, scale_factor=1.5), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S06
class S06_Curve(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "The S-curve")
        x0, x1, y0, y1, g0, b0 = -5.0, 2.0, -2.3, 1.9, -2.8, 0.7

        def X(s):
            return x0 + (x1 - x0) * s / 8

        def YL(v):
            return y0 + (y1 - y0) * (v + 3.5) / 7

        def YP(p):
            return y0 + (y1 - y0) * p

        def path(f, n=81):
            return VMobject(stroke_width=5, color=PAPER).set_points_smoothly([[X(s), f(s), 0] for s in np.linspace(0, 8, n)])

        xa = Line([x0, y0, 0], [x1 + 0.2, y0, 0], stroke_width=2.5, color=MUTED)
        ya = Line([x0, y0, 0], [x0, y1 + 0.2, 0], stroke_width=2.5, color=MUTED)
        xt = VGroup(*[Line([X(s), y0, 0], [X(s), y0 - 0.1, 0], stroke_width=2, color=MUTED) for s in range(9)])
        xl = VGroup(*[txt(str(s), 18, MUTED).move_to([X(s), y0 - 0.3, 0]) for s in range(9)])
        xn = txt("earlier hospital stays", 19, MUTED, font=SERIF, slant=ITALIC).move_to([(x0 + x1) / 2, y0 - 0.62, 0])
        yl_L = VGroup(*[txt(signed(v, 0) if v else "0", 18, MUTED).move_to([x0 - 0.38, YL(v), 0]) for v in (-3, 0, 3)])
        yl_P = VGroup(*[txt(f"{round(100 * p)}%", 18, MUTED).move_to([x0 - 0.45, YP(p), 0]) for p in (0, 0.5, 1)])
        yn_L = txt("log-odds", 20, PAPER, font=SERIF, slant=ITALIC).move_to([x0 + 0.75, y1 + 0.45, 0])
        yn_P = txt("probability", 20, PAPER, font=SERIF, slant=ITALIC).move_to([x0 + 0.9, y1 + 0.45, 0])
        dots = VGroup(*[Dot([X(s), YL(g0 + b0 * s), 0], radius=0.085, color=PAPER).set_z_index(3) for s in range(9)])
        stairs = VGroup(*[VGroup(Line([X(s), YL(g0 + b0 * s), 0], [X(s + 1), YL(g0 + b0 * s), 0], stroke_width=2, color=MUTED),
                                 Line([X(s + 1), YL(g0 + b0 * s), 0], [X(s + 1), YL(g0 + b0 * (s + 1)), 0], stroke_width=3.5, color=ACCENT))
                          for s in range(8)])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), Create(xa), Create(ya), FadeIn(xt), FadeIn(xl), FadeIn(xn), FadeIn(yl_L), FadeIn(yn_L), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(dots[0]), run_time=0.4)
            self.play(LaggedStart(*[AnimationGroup(Create(stairs[s]), GrowFromCenter(dots[s + 1])) for s in range(8)], lag_ratio=0.6),
                      run_time=seg.until(seg.e(1)))

        line = path(lambda s: YL(g0 + b0 * s))
        curve = path(lambda s: YP(expit(g0 + b0 * s)))
        beta = tex(r"\beta", 44, ACCENT).move_to([X(5) + 0.42, YL(g0 + b0 * 4.5), 0])
        with self.nar("s6_2") as seg:
            self.play(Create(line), run_time=1.4)
            seg.wait_until(seg.word(0, "Its slope"))
            self.play(*[st.animate.set_stroke(opacity=0.25) for k, st in enumerate(stairs) if k != 4], FadeIn(beta, shift=LEFT * 0.1), run_time=0.9)
            self.play(Indicate(stairs[4][1], color=ACCENT, scale_factor=1.3), run_time=0.8)

        with self.nar("s6_3") as seg:
            self.play(FadeOut(stairs), FadeOut(beta), run_time=0.6)
            self.play(Transform(line, curve), *[d.animate.move_to([X(s), YP(expit(g0 + b0 * s)), 0]) for s, d in enumerate(dots)],
                      ReplacementTransform(yl_L, yl_P), ReplacementTransform(yn_L, yn_P), run_time=2.6)
            seg.wait_until(seg.word(1, "steep in the middle"))
            self.play(Indicate(VGroup(*dots[3:6]), color=ACCENT, scale_factor=1.25), run_time=0.9)
            seg.wait_until(seg.word(1, "flat at both ends"))
            self.play(Indicate(VGroup(*dots[:2], *dots[7:]), color=ACCENT, scale_factor=1.25), run_time=0.9)

        s_t = ValueTracker(0.6)

        def p_at(s):
            return float(expit(g0 + b0 * s))

        def tangent():
            s, p = s_t.get_value(), p_at(s_t.get_value())
            v = np.array([(x1 - x0) / 8, (y1 - y0) * b0 * p * (1 - p), 0])
            v = v / np.linalg.norm(v)
            c = np.array([X(s), YP(p), 0])
            return VGroup(Line(c - 0.9 * v, c + 0.9 * v, stroke_width=4, color=ACCENT), Dot(c, radius=0.09, color=ACCENT)).set_z_index(4)

        bx = 3.35
        st_title = VGroup(txt("steepness", 22, PAPER), tex(r"\propto\; p\,(1-p)", 34, ACCENT)).arrange(RIGHT, buff=0.2).move_to([bx + 1.5, 1.2, 0])
        track = Rectangle(width=3.0, height=0.2, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([bx + 1.5, 0.5, 0])
        bar = always_redraw(lambda: Rectangle(width=max(0.02, 12 * p_at(s_t.get_value()) * (1 - p_at(s_t.get_value()))), height=0.2, stroke_width=0,
                                              fill_color=ACCENT, fill_opacity=1).move_to(track.get_left(), aligned_edge=LEFT))
        cap = txt("greatest at 50%", 19, MUTED, font=SERIF, slant=ITALIC).move_to([bx + 1.5, 0.05, 0])
        tan = always_redraw(tangent)
        with self.nar("s6_4") as seg:
            self.play(FadeOut(dots), run_time=0.5)
            self.add(tan)
            self.play(FadeIn(track), FadeIn(st_title), run_time=0.8)
            self.add(bar)
            seg.wait_until(seg.word(0, "greatest at fifty-fifty") - 0.8)
            self.play(s_t.animate.set_value(4.0), run_time=2.2)
            self.play(FadeIn(cap), run_time=0.5)
            seg.wait_until(seg.word(0, "fading to nothing"))
            self.play(s_t.animate.set_value(7.6), run_time=2.2)
            seg.wait_until(seg.s(1))
            self.play(Indicate(st_title, color=ACCENT, scale_factor=1.12), run_time=1.0)

        bt, mid = ValueTracker(b0), ValueTracker(4.0)
        live = always_redraw(lambda: path(lambda s: YP(expit(bt.get_value() * (s - mid.get_value())))))
        knob = Circle(radius=0.55, stroke_color=ACCENT, stroke_width=4).set_fill(INK_2, 1).move_to([bx + 1.5, -0.2, 0])
        hand = always_redraw(lambda: Line(knob.get_center(), knob.get_center() + 0.5 * np.array(
            [np.sin(2.2 * (bt.get_value() - b0)), np.cos(2.2 * (bt.get_value() - b0)), 0]), stroke_width=5, color=ACCENT))
        kname = VGroup(tex(r"\beta", 40, ACCENT), txt("dial", 21, MUTED, font=SERIF, slant=ITALIC)).arrange(RIGHT, buff=0.15).next_to(knob, DOWN, buff=0.22)
        with self.nar("s6_5", gap=0.6) as seg:
            self.remove(tan, bar)
            self.play(FadeOut(VGroup(track, st_title, cap)), FadeIn(knob), FadeIn(kname), run_time=0.7)
            self.remove(line)
            self.add(live, hand)
            self.play(bt.animate.set_value(1.6), run_time=1.3)
            self.play(bt.animate.set_value(0.4), run_time=1.2)
            self.play(bt.animate.set_value(b0), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(mid.animate.set_value(2.3), run_time=1.3)
            self.play(mid.animate.set_value(5.7), run_time=1.5)
            self.play(mid.animate.set_value(4.0), run_time=0.8)
        live.clear_updaters()
        hand.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S07
class S07_Cedar(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "One real clinic")
        crd = card(7.0, 1.75).move_to([0, 2.15, 0])
        name = txt("Cedar", 28, CEDAR, weight=SEMIBOLD).move_to([-5.0, 2.15, 0])
        gx = (-2.2, 2.2)
        units = []
        for h, (n, e) in enumerate((CLINICS["Cedar"]["low"], CLINICS["Cedar"]["high"])):
            for j in range(n):
                units.append(Unit(CEDAR, j < e, bool(h), r=0.14).move_to([gx[h] + (j % 5 - 2) * 0.42, 2.2 - (j // 5) * 0.42, 0]))
        glab = [txt(s, 20, MUTED, font=SERIF, slant=ITALIC).move_to([x, 2.78, 0]) for s, x in zip(("lower risk", "higher risk"), gx)]
        ya, yb = 0.72, 0.1
        pa = [VGroup(txt(a, 22, MUTED), txt(b, 30, PAPER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.25).move_to([x, ya, 0])
              for (a, b), x in zip((("2 of 10", "20%"), ("6 of 10", "60%")), gx)]
        ob = [VGroup(txt(a, 22, MUTED), txt(b, 30, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.25).move_to([x, yb, 0])
              for (a, b), x in zip((("odds  2 : 8", "0.25"), ("odds  6 : 4", "1.5")), gx)]
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(crd), FadeIn(name), *[FadeIn(g) for g in glab], run_time=1.0)
            self.play(LaggedStart(*[GrowFromCenter(u) for u in units], lag_ratio=0.03), run_time=1.2)
            seg.wait_until(seg.word(1, "Ten lower-risk"))
            self.play(*pulse([u for u in units[:10] if u.event]), FadeIn(pa[0], shift=UP * 0.1), run_time=1.0)
            seg.wait_until(seg.word(1, "Ten higher-risk"))
            self.play(*pulse([u for u in units[10:] if u.event]), FadeIn(pa[1], shift=UP * 0.1), run_time=1.0)

        with self.nar("s7_2") as seg:
            seg.wait_until(seg.word(0, "two to eight") - 0.2)
            self.play(FadeIn(ob[0], shift=UP * 0.1), run_time=0.8)
            seg.wait_until(seg.word(0, "and six to four") - 0.1)
            self.play(FadeIn(ob[1], shift=UP * 0.1), run_time=0.8)

        x6 = VGroup(step_arrow([-0.55, yb, 0], [0.4, yb, 0]), txt("\u00d7 6", 30, ACCENT, weight=SEMIBOLD)).arrange(DOWN, buff=0.08).move_to([0, yb - 0.08, 0])
        x3 = VGroup(txt("\u00d7 3", 30, PAPER, weight=SEMIBOLD), step_arrow([-0.55, ya, 0], [0.4, ya, 0], color=PAPER)).arrange(DOWN, buff=0.08).move_to([0, ya + 0.08, 0])
        orl = txt("odds ratio", 19, ACCENT, font=SERIF, slant=ITALIC).next_to(x6, DOWN, buff=0.1)
        with self.nar("s7_3") as seg:
            seg.wait_until(seg.word(0, "an odds ratio of six") - 0.3)
            self.play(FadeIn(x6, shift=UP * 0.1), FadeIn(orl), run_time=1.0)
            seg.wait_until(seg.word(0, "multiplies the odds"))
            self.play(Indicate(x6, color=ACCENT, scale_factor=1.2), run_time=0.9)

        Rl = logit_ruler(-2.0)
        gam, bet = logit(0.2), float(np.log(6))
        c1 = Unit(CEDAR, False, False, r=0.14).move_to(Rl.P(gam, 0.3))
        c2 = Unit(CEDAR, True, True, r=0.14).move_to(Rl.P(gam + bet, 0.3))
        arr = step_arrow(Rl.P(gam, 0.3) + RIGHT * 0.22, Rl.P(gam + bet, 0.3) + LEFT * 0.26)
        blab = VGroup(tex(r"\beta =", 34, ACCENT), txt("1.79", 24, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.14).move_to(Rl.P(gam + bet / 2, 0.68))
        glab2 = VGroup(tex(r"\gamma =", 34, PAPER), txt(signed(gam), 24, PAPER, weight=SEMIBOLD)).arrange(RIGHT, buff=0.14).move_to(Rl.P(gam, 0.68)).shift(LEFT * 1.25)
        model = tex(r"\text{log-odds} \;=\; \gamma \;+\; \beta \cdot \text{(higher risk)}", 32, PAPER).move_to([3.5, -0.95, 0])
        with self.nar("s7_4") as seg:
            self.play(FadeIn(Rl.g), FadeOut(orl), run_time=0.9)
            self.play(TransformFromCopy(ob[0][1], c1), TransformFromCopy(ob[1][1], c2), run_time=1.0)
            seg.wait_until(seg.word(0, "a step of") - 0.2)
            self.play(GrowArrow(arr), FadeIn(blab), run_time=0.9)
            seg.wait_until(seg.word(0, "starting from") - 0.1)
            self.play(FadeIn(glab2, shift=RIGHT * 0.1), run_time=0.7)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(model, shift=UP * 0.1), run_time=1.0)

        with self.nar("s7_5", gap=0.7) as seg:
            seg.wait_until(seg.s(1))
            self.play(FadeIn(x3, shift=DOWN * 0.1), run_time=0.9)
            seg.wait_until(seg.word(1, "three times, not six"))
            self.play(Indicate(x3[0], color=PAPER, scale_factor=1.35), run_time=0.7)
            self.play(Indicate(x6[1], color=ACCENT, scale_factor=1.35), run_time=0.7)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S08
class S08_RiskChip(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "The risk chip")
        Rp, Rl = prob_ruler(1.15, x0=-4.4, x1=3.6), logit_ruler(-1.75, x0=-3.9, x1=4.7)
        eta = ValueTracker(logit(0.2))
        mp, ml = hero_chip(0.16), hero_chip(0.16)
        mp.add_updater(lambda m: m.move_to(Rp.P(expit(eta.get_value()), 0.3)))
        ml.add_updater(lambda m: m.move_to(Rl.P(eta.get_value(), 0.3)))
        ghost = txt("110%", 26, ALERT, weight=SEMIBOLD).move_to(Rp.P(1.1, 0.3)).set_opacity(0.55)
        row = VGroup(*[VGroup(pill(w), txt(signed(s), 26, ACCENT, weight=SEMIBOLD)).arrange(RIGHT, buff=0.22) for (w, _, _), s in zip(FACTORS, STEPS)])
        row.arrange(RIGHT, buff=0.7).move_to([0, 2.75, 0])
        plab = txt("20%", 26, PAPER, weight=SEMIBOLD).move_to(Rp.P(0.2, 0.8))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), FadeIn(Rp.g), FadeIn(ghost), run_time=1.0)
            self.add(mp)
            self.play(GrowFromCenter(mp), FadeIn(plab), run_time=0.6)
            seg.wait_until(seg.word(0, "This time"))
            self.add(ml)
            self.play(FadeIn(Rl.g), GrowFromCenter(ml), LaggedStart(*[FadeIn(r, shift=DOWN * 0.1) for r in row], lag_ratio=0.2), run_time=1.4)

        at, arrows = logit(0.2), VGroup()
        with self.nar("s8_2", gap=0.2) as seg:
            per = max(1.2, (seg.dur - 0.6) / 3)
            for k, s in enumerate(STEPS):
                a = step_arrow(Rl.P(at, 0.78), Rl.P(at + s, 0.78))
                al = txt(signed(s), 20, ACCENT, weight=SEMIBOLD).move_to(Rl.P(at + s / 2, 1.08))
                newlab = txt(f"{round(100 * float(expit(at + s)))}%", 26, PAPER, weight=SEMIBOLD).move_to(Rp.P(float(expit(at + s)), 0.8))
                self.play(*pulse([row[k]], 1.1), run_time=0.4)
                self.play(GrowArrow(a), FadeIn(al), eta.animate.set_value(at + s), FadeOut(plab), run_time=per - 0.75)
                self.play(FadeIn(newlab), run_time=0.35)
                arrows.add(a, al)
                plab, at = newlab, at + s

        strike = Line(ghost.get_left() + LEFT * 0.08, ghost.get_right() + RIGHT * 0.08, stroke_width=4, color=ALERT)
        with self.nar("s8_3") as seg:
            seg.wait_until(seg.word(0, "Ninety-four") - 0.2)
            self.play(Indicate(plab, color=ACCENT, scale_factor=1.5), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Create(strike), run_time=0.7)

        mp.clear_updaters()
        ml.clear_updaters()
        cy = 0.02
        rcs = [risk_chip(p).move_to([Rp.X(p), cy, 0]) for p in (0.2, 0.5, float(expit(at)))]
        rls = [txt(f"{round(100 * p)}%", 21, MUTED).next_to(rc, LEFT, buff=0.18) for rc, p in zip(rcs, (0.2, 0.5, float(expit(at))))]
        drops = [DashedLine(Rp.P(p, -0.5), [Rp.X(p), cy + 0.45, 0], dash_length=0.06, stroke_width=1.5, color=MUTED) for p in (0.2, 0.5, float(expit(at)))]
        with self.nar("s8_4", gap=0.7) as seg:
            self.play(FadeOut(VGroup(ghost, strike)), Create(drops[2]), TransformFromCopy(mp, rcs[2]), FadeIn(rls[2]), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(Create(drops[0]), GrowFromCenter(rcs[0]), FadeIn(rls[0]), run_time=0.9)
            self.play(Create(drops[1]), GrowFromCenter(rcs[1]), FadeIn(rls[1]), run_time=0.8)
            seg.wait_until(seg.word(1, "nearly the whole disc"))
            self.play(Indicate(rcs[2], color=ACCENT, scale_factor=1.2), run_time=0.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S09
class S09_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(7, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(*[chip(PAPER, k < 2, 0.1).move_to([(k - 4.5) * 0.27 + (0.2 if k >= 2 else 0), 0, 0]) for k in range(10)],
                       txt("2 : 8", 24, ACCENT, weight=SEMIBOLD).move_to([0, -0.48, 0]))
        rl = Line([-1.5, 0, 0], [1.5, 0, 0], stroke_width=4, color=PAPER)
        icon2 = VGroup(rl, *[Line([x, 0, 0], [x, -0.1, 0], stroke_width=2, color=MUTED) for x in np.linspace(-1.2, 1.2, 7)],
                       *[step_arrow([-1.2 + 0.8 * k, 0.28, 0], [-0.4 + 0.8 * k, 0.28, 0], width=3.5) for k in range(3)])
        sc = VMobject(stroke_width=5, color=PAPER).set_points_smoothly([[x, 1.2 * float(expit(3.2 * x)) - 0.6, 0] for x in np.linspace(-1.5, 1.5, 41)])
        icon3 = VGroup(Line([-1.5, -0.6, 0], [1.5, -0.6, 0], stroke_width=2, color=MUTED), Line([-1.5, 0.6, 0], [1.5, 0.6, 0], stroke_width=1.5, color=FAINT), sc)
        icons = [icon1, icon2, icon3]
        caps = [["Odds: those who come back", "against those who don't"], ["Log-odds: the ruler", "where risk factors add"],
                ["The S-curve carries the sum", "back to a probability"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 21, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s9_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        ps = [0.2] * 10 + [0.6] * 10
        rcs = [risk_chip(p, r=0.24, color=CEDAR).move_to([(j % 10 - 4.5) * 0.62, 2.2 - (j // 10) * 0.66, 0]) for j, p in enumerate(ps)]
        cname = txt("Cedar", 26, CEDAR, weight=SEMIBOLD).move_to([-4.3, 1.87, 0])
        bx0, by, unit = -3.0, -0.35, 0.3                                   # 0.3 per patient: 20 patients = 6.0 wide
        track = Rectangle(width=20 * unit, height=0.3, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([bx0 + 10 * unit, by, 0])
        fillb = Rectangle(width=8 * unit, height=0.3, stroke_width=0, fill_color=CEDAR, fill_opacity=1).move_to([bx0 + 4 * unit, by, 0])
        elab = VGroup(txt("expected", 22, MUTED, font=SERIF, slant=ITALIC), txt("8.0", 34, PAPER, weight=SEMIBOLD, font=DISPLAY)).arrange(RIGHT, buff=0.25).move_to([4.6, by, 0])
        summ = txt("10 \u00d7 20%  +  10 \u00d7 60%", 21, MUTED).move_to([0, by - 0.5, 0])
        with self.nar("s9_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(LaggedStart(*[GrowFromCenter(r) for r in rcs], lag_ratio=0.04), FadeIn(cname), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(track), run_time=0.5)
            self.play(LaggedStart(*[TransformFromCopy(r[1], Rectangle(width=unit * p, height=0.3, stroke_width=0, fill_color=CEDAR, fill_opacity=1).move_to(
                [bx0 + unit * (sum(ps[:j]) + p / 2), by, 0])) for j, (r, p) in enumerate(zip(rcs, ps))], lag_ratio=0.05), run_time=2.6)
            self.play(FadeIn(elab, shift=LEFT * 0.1), FadeIn(summ), run_time=0.8)

        obs = VGroup(*[chip(CEDAR, True, 0.13).move_to([bx0 + unit * (k + 0.5), by - 1.25, 0]) for k in range(8)])
        olab = VGroup(txt("observed", 22, MUTED, font=SERIF, slant=ITALIC), txt("8", 34, PAPER, weight=SEMIBOLD, font=DISPLAY)).arrange(RIGHT, buff=0.25)
        olab.move_to([4.6, by - 1.25, 0]).align_to(elab, LEFT)
        nxt = VGroup(txt("Next:", 26, MUTED), txt("observed versus expected", 36, PAPER, weight=SEMIBOLD, font=DISPLAY)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
        nxt.move_to([0, -2.55, 0])
        with self.nar("s9_3") as seg:
            self.play(FadeOut(summ), LaggedStart(*[GrowFromCenter(c) for c in obs], lag_ratio=0.08), FadeIn(olab), run_time=1.4)
            seg.wait_until(seg.word(0, "Observed, versus"))
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.9)

        mark, word = logo_mark(1.0), wordmark(54)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        ep3 = txt("NEXT  \u00b7  EPISODE 3  \u00b7  OBSERVED VERSUS EXPECTED", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
        thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep3, DOWN, buff=0.45)
        with self.nar("s9_4", gap=1.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
            self.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep3), run_time=1.0)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
