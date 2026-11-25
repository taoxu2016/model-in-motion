"""Model in Motion · The Logistic Fixed-Effect Model · Episode 3: Observed versus Expected.

Render one scene:   manim -qh --media_dir build/media episode/episode03.py S04_Meter
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
from mim.kit import *  # noqa: E402,F403

POOL = {False: 13 / 57, True: 29 / 46}        # pooled readmission rates: lower-risk, higher-risk
OTHERS = {False: 5 / 33, True: 24 / 40}       # the same pool without Alder


def expected(name, rates=POOL):
    c = CLINICS[name]
    return c["low"][0] * rates[False] + c["high"][0] * rates[True]


def obs_row(name, x0, y, u, r):
    return VGroup(*[chip(CLINICS[name]["color"], True, r).move_to([x0 + (k + 0.5) * u, y, 0]) for k in range(events(name))])


def exp_bar(name, x0, y, u, h, rates=POOL):
    """Expected count as a bar: one piece per patient, as wide as that patient's probability; dashed outline."""
    col, pieces, x = CLINICS[name]["color"], VGroup(), x0
    for p in patients(name):
        w = u * rates[p["high"]]
        pieces.add(Rectangle(width=w, height=h, stroke_color=INK, stroke_width=1, fill_color=col, fill_opacity=0.45).move_to([x + w / 2, y, 0]))
        x += w
    box = Rectangle(width=x - x0, height=h, stroke_color=col, stroke_width=2.5).move_to([(x0 + x) / 2, y, 0])
    return pieces, DashedVMobject(box, num_dashes=int(16 * (x - x0)) + 8)


def side(s, x, y):
    return txt(s, 21, MUTED, font=SERIF, slant=ITALIC).move_to([x, y, 0])


def big(s, x, y, size=32, color=PAPER):
    return txt(s, size, color, weight=SEMIBOLD, font=DISPLAY).move_to([x, y, 0])


# =================================================================================== S01
class S01_ColdOpen(EpisodeScene):
    def construct(self):
        ps = [0.2] * 10 + [0.6] * 10
        rcs = [risk_chip(p, r=0.24, color=CEDAR).move_to([(j % 10 - 4.5) * 0.62, 2.3 - (j // 10) * 0.66, 0]) for j, p in enumerate(ps)]
        cname = txt("Cedar", 26, CEDAR, weight=SEMIBOLD).move_to([-4.3, 1.97, 0])
        bx0, by, unit = -3.0, -0.1, 0.3
        track = Rectangle(width=20 * unit, height=0.3, stroke_width=0, fill_color=FAINT, fill_opacity=1).move_to([bx0 + 10 * unit, by, 0])
        fillb = Rectangle(width=8 * unit, height=0.3, stroke_width=0, fill_color=CEDAR, fill_opacity=1).move_to([bx0 + 4 * unit, by, 0])
        elab = VGroup(side("expected", 0, 0), big("8.0", 0, 0, 34)).arrange(RIGHT, buff=0.25).move_to([4.6, by, 0])
        obs = VGroup(*[chip(CEDAR, True, 0.13).move_to([bx0 + unit * (k + 0.5), by - 0.85, 0]) for k in range(8)])
        olab = VGroup(side("observed", 0, 0), big("8", 0, 0, 34)).arrange(RIGHT, buff=0.25).move_to([4.6, by - 0.85, 0]).align_to(elab, LEFT)
        with self.nar("s1_1") as seg:
            self.play(LaggedStart(*[GrowFromCenter(r) for r in rcs], lag_ratio=0.03), FadeIn(cname), run_time=1.4)
            seg.wait_until(seg.word(0, "added them up"))
            self.play(FadeIn(track), GrowFromEdge(fillb, LEFT), FadeIn(elab), run_time=1.2)
            seg.wait_until(seg.word(0, "Cedar had exactly"))
            self.play(LaggedStart(*[GrowFromCenter(c) for c in obs], lag_ratio=0.06), FadeIn(olab), run_time=1.0)

        loop = CurvedArrow([bx0 - 0.25, by - 0.85, 0], [-3.35, 1.97, 0], angle=-TAU / 3.2, color=ACCENT, stroke_width=4, tip_length=0.2)
        looplab = txt("built from", 21, ACCENT, font=SERIF, slant=ITALIC).move_to([-5.45, 0.35, 0])
        with self.nar("s1_2") as seg:
            self.play(Indicate(elab[1], color=ACCENT, scale_factor=1.3), Indicate(olab[1], color=ACCENT, scale_factor=1.3), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(Create(loop), FadeIn(looplab), run_time=1.4)
            seg.wait_until(seg.word(1, "We compared"))
            self.play(Indicate(cname, color=ACCENT, scale_factor=1.2), run_time=0.9)

        q = big("expected, according to whom?", 0, -2.2, 40)
        qm = big("?", 0, 0, 34, ACCENT).move_to(elab[1])
        with self.nar("s1_3", gap=0.7) as seg:
            self.play(FadeOut(loop), FadeOut(looplab), *[FadeOut(r[1]) for r in rcs], FadeOut(fillb), FadeOut(elab[1]), FadeIn(qm), run_time=1.3)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(q, shift=UP * 0.15), run_time=1.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)


# =================================================================================== S02
class S02_Title(EpisodeScene):
    def construct(self):
        mark = logo_mark(1.25)
        word = wordmark(64)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.55).move_to(UP * 1.15)
        arc = txt("THE LOGISTIC FIXED-EFFECT MODEL  \u00b7  EPISODE 3", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.75)
        title = txt("Observed versus Expected", 66, PAPER, weight=SEMIBOLD, font=DISPLAY).next_to(arc, DOWN, buff=0.32)
        sub = txt("how many readmissions should a clinic have had?", 30, MUTED, font=SERIF, slant=ITALIC).next_to(title, DOWN, buff=0.26)
        a, dot, b, ring, scan = mark
        with self.nar("s2_1", gap=0.6) as seg:
            self.play(Create(a), Create(b), run_time=0.8)
            self.play(GrowFromCenter(dot), GrowFromCenter(ring), FadeIn(scan, shift=RIGHT * 0.6), Write(word), run_time=1.3)
            seg.wait_until(seg.s(1) - 0.2)
            self.play(LaggedStart(FadeIn(arc, shift=UP * 0.15), FadeIn(title, shift=UP * 0.2),
                                  FadeIn(sub, shift=UP * 0.15), lag_ratio=0.25), run_time=1.6)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S03
class S03_Standard(EpisodeScene):
    def construct(self):
        tag = chapter_tag(1, "A first standard")
        cx = {"Alder": -5.0, "Birch": -2.4, "Cedar": 0.1, "Dune": 2.3, "Elm": 4.5}
        nc = {"Alder": 6, "Birch": 6, "Cedar": 5, "Dune": 4, "Elm": 4}
        units, names = [], VGroup()
        for n in ORDER:
            pat, col = patients(n), CLINICS[n]["color"]
            order = np.random.default_rng(JUMBLE[n]).permutation(len(pat))
            for k, p in enumerate(pat):
                s = int(order[k])
                units.append(Unit(col, p["event"], p["high"], r=0.11).move_to([cx[n] + (s % nc[n] - (nc[n] - 1) / 2) * 0.3, 2.3 - (s // nc[n]) * 0.3, 0]))
            names.add(txt(n, 22, col, weight=SEMIBOLD).move_to([cx[n], 2.8, 0]))
        total = big("103 patients", 0, 0.1, 34)
        with self.nar("s3_1") as seg:
            self.play(FadeIn(tag), FadeIn(names), LaggedStart(*[GrowFromCenter(u) for u in units], lag_ratio=0.01), run_time=2.0)
            seg.wait_until(seg.word(0, "one hundred and three") - 0.2)
            self.play(FadeIn(total, shift=UP * 0.1), run_time=0.8)

        lows = sorted([u for u in units if not u.high], key=lambda u: not u.event)
        highs = sorted([u for u in units if u.high], key=lambda u: not u.event)
        lx, hx, ty = -2.75, 3.3, 1.5
        moves = [Transform(u, Unit(MUTED, u.event, False, r=0.11).move_to([lx + (j % 19 - 9) * 0.3, ty - (j // 19) * 0.3, 0])) for j, u in enumerate(lows)]
        moves += [Transform(u, Unit(MUTED, u.event, True, r=0.11).move_to([hx + (j % 16 - 7.5) * 0.3, ty - (j // 16) * 0.3, 0])) for j, u in enumerate(highs)]
        heads = VGroup(side("lower risk", lx, ty + 0.45), side("higher risk", hx, ty + 0.45))
        cl = VGroup(txt("13 of 57", 24, MUTED), big("23%", 0, 0, 36)).arrange(RIGHT, buff=0.3).move_to([lx, 0.2, 0])
        ch = VGroup(txt("29 of 46", 24, MUTED), big("63%", 0, 0, 36)).arrange(RIGHT, buff=0.3).move_to([hx, 0.2, 0])
        with self.nar("s3_2") as seg:
            self.play(FadeOut(total), FadeOut(names), LaggedStart(*moves, lag_ratio=0.006), run_time=2.6)
            self.play(FadeIn(heads), run_time=0.5)
            seg.wait_until(seg.s(1))
            self.play(*pulse([u for u in lows if u.event], 1.35), FadeIn(cl, shift=UP * 0.1), run_time=1.1)
            seg.wait_until(seg.s(2))
            self.play(*pulse([u for u in highs if u.event], 1.35), FadeIn(ch, shift=UP * 0.1), run_time=1.1)

        sl = risk_chip(POOL[False], r=0.5).move_to([lx, -1.45, 0])
        sh = risk_chip(POOL[True], r=0.5).move_to([hx, -1.45, 0])
        name = big("the pooled standard", 0.28, -1.45, 32)
        with self.nar("s3_3", gap=0.7) as seg:
            self.play(TransformFromCopy(cl[1], sl), TransformFromCopy(ch[1], sh), run_time=1.2)
            seg.wait_until(seg.word(0, "the pooled standard") - 0.2)
            self.play(FadeIn(name, shift=UP * 0.1), run_time=0.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S04
class S04_Meter(EpisodeScene):
    def construct(self):
        tag = chapter_tag(2, "Expected")
        pat = patients("Alder")

        def grid(k, c):
            return np.array([c + (k % 10 - 4.5) * 0.42, 2.25 - (k // 10) * 0.42, 0])

        left = [Unit(ALDER, p["event"], p["high"], r=0.15).move_to(grid(k, -3.5)) for k, p in enumerate(pat)]
        right = [risk_chip(POOL[p["high"]], r=0.17, color=ALDER).move_to(grid(k, 3.5)) for k, p in enumerate(pat)]
        lt, rt_ = side("what happened", -3.5, 2.85), side("what the standard expects", 3.5, 2.85)
        name = txt("Alder", 30, ALDER, weight=SEMIBOLD).move_to([0, 1.85, 0])
        with self.nar("s4_1") as seg:
            self.play(FadeIn(tag), FadeIn(name), run_time=0.8)
            self.play(LaggedStart(*[GrowFromCenter(u) for u in left], lag_ratio=0.03), FadeIn(lt), run_time=1.4)
            seg.wait_until(seg.s(1))
            self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(left, right)], lag_ratio=0.03), FadeIn(rt_), run_time=2.0)

        u, x0, yo, ye, ys = 0.4, -2.7, -0.4, -1.2, -1.85
        scale = VGroup(Line([x0, ys, 0], [x0 + 15 * u, ys, 0], stroke_width=2.5, color=MUTED),
                       *[Line([x0 + k * u, ys, 0], [x0 + k * u, ys - (0.14 if k % 5 == 0 else 0.07), 0], stroke_width=2, color=MUTED) for k in range(16)],
                       *[txt(str(k), 18, MUTED).move_to([x0 + k * u, ys - 0.34, 0]) for k in (0, 5, 10, 15)],
                       side("patients", x0 + 15 * u + 0.85, ys))
        pieces, frame = exp_bar("Alder", x0, ye, u, 0.32)
        E = expected("Alder")
        el, ev = side("expected", x0 - 0.95, ye), big(f"{E:.1f}", x0 + E * u + 0.5, ye)
        with self.nar("s4_2") as seg:
            self.play(FadeIn(scale), FadeIn(el), run_time=0.8)
            self.play(LaggedStart(*[TransformFromCopy(r[1], pc) for r, pc in zip(right, pieces)], lag_ratio=0.04), run_time=seg.until(seg.e(0)) - 0.9)
            self.play(Create(frame), FadeIn(ev, shift=LEFT * 0.1), run_time=0.8)
            seg.wait_until(seg.word(1, "expected count"))
            self.play(Indicate(ev, color=ACCENT, scale_factor=1.3), run_time=0.9)

        row = obs_row("Alder", x0, yo, u, 0.15)
        ol, ov = side("observed", x0 - 0.95, yo), big("13", x0 + 13 * u + 0.4, yo)
        gap = DoubleArrow([x0 + E * u, yo - 0.4, 0], [x0 + 13 * u, yo - 0.4, 0], buff=0, stroke_width=3.5, color=ACCENT, tip_length=0.16)
        gl = big("+3.7", x0 + (E + 13) / 2 * u, yo - 0.4, 26, ACCENT).shift(DOWN * 0.02)
        gl.add_background_rectangle(color=INK, opacity=1, buff=0.06)
        ratio = VGroup(txt("13 / 9.3", 22, MUTED), big("= 1.40", 0, 0, 38)).arrange(RIGHT, buff=0.25).move_to([5.0, yo - 0.4, 0])
        piv = Triangle(fill_color=MUTED, fill_opacity=1, stroke_width=0).scale(0.14).move_to([5.0, 0.42, 0])
        beam = VGroup(Line([4.2, 0.62, 0], [5.8, 0.62, 0], stroke_width=5, color=PAPER), Dot([4.2, 0.8, 0], radius=0.15, color=ALDER),
                      DashedVMobject(Circle(radius=0.15, stroke_color=ALDER, stroke_width=2.5).move_to([5.8, 0.8, 0]), num_dashes=10))
        with self.nar("s4_3", gap=0.8) as seg:
            src = [x.chip for x in left if x.event]
            self.play(LaggedStart(*[TransformFromCopy(a, b) for a, b in zip(src, row)], lag_ratio=0.05), FadeIn(ol), run_time=1.3)
            self.play(FadeIn(ov, shift=LEFT * 0.1), run_time=0.4)
            seg.wait_until(seg.s(1))
            self.play(GrowFromCenter(gap), FadeIn(gl), FadeIn(piv), FadeIn(beam), run_time=1.0)
            self.play(Rotate(beam, 0.2, about_point=[5.0, 0.62, 0]), run_time=0.8)
            seg.wait_until(seg.word(1, "as a ratio"))
            self.play(FadeIn(ratio, shift=UP * 0.1), run_time=0.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S05
class S05_Five(EpisodeScene):
    def construct(self):
        tag = chapter_tag(3, "Five verdicts")
        u, x0, ys = 0.3, -4.4, [2.45, 1.45, 0.45, -0.55, -1.55]
        rows = {}
        for n, y in zip(ORDER, ys):
            col, E, O = CLINICS[n]["color"], expected(n), events(n)
            pieces, frame = exp_bar(n, x0, y - 0.17, u, 0.24)
            rows[n] = dict(name=txt(n, 24, col, weight=SEMIBOLD).move_to([x0 - 1.0, y, 0]), obs=obs_row(n, x0, y + 0.19, u, 0.11),
                           bar=VGroup(pieces, frame), detail=txt(f"{O} / {E:.1f}", 21, MUTED).move_to([1.7, y, 0]),
                           ratio=big(f"{O / E:.2f}", 3.9, y, 34), raw=txt(pct(rate(n)), 24, MUTED).move_to([5.6, y, 0]))
        heads = VGroup(side("observed / expected", 1.7, 3.1), side("ratio", 3.9, 3.1))
        rawhead = side("raw rate", 5.6, 3.1)

        def show(n):
            r = rows[n]
            parts = [r["name"], r["bar"], r["detail"], r["ratio"]] + ([r["obs"]] if len(r["obs"]) else [])
            return AnimationGroup(*[FadeIn(p, shift=RIGHT * 0.1) for p in parts])

        with self.nar("s5_1") as seg:
            self.play(FadeIn(tag), FadeIn(heads), run_time=0.7)
            self.play(LaggedStart(*[show(n) for n in ORDER], lag_ratio=0.35), run_time=max(2.0, seg.until(seg.dur)))

        box = SurroundingRectangle(VGroup(rows["Birch"]["name"], rows["Birch"]["ratio"]), color=BIRCH, buff=0.2, corner_radius=0.14, stroke_width=3)
        with self.nar("s5_2") as seg:
            self.play(Create(box), run_time=0.9)
            seg.wait_until(seg.word(0, "a ratio of"))
            self.play(Indicate(rows["Birch"]["ratio"], color=ACCENT, scale_factor=1.3), run_time=0.9)

        with self.nar("s5_3") as seg:
            self.play(FadeOut(box), FadeIn(rawhead), FadeIn(rows["Alder"]["raw"]), FadeIn(rows["Birch"]["raw"]), run_time=0.9)
            seg.wait_until(seg.word(0, "Birch's raw rate"))
            self.play(Indicate(rows["Birch"]["raw"], color=ACCENT, scale_factor=1.3), run_time=0.8)
            self.play(Indicate(rows["Alder"]["raw"], color=ACCENT, scale_factor=1.3), run_time=0.8)
            seg.wait_until(seg.word(1, "Birch comes out ahead") - 0.3)
            self.play(rows["Birch"]["ratio"].animate.set_color(GOOD), rows["Alder"]["ratio"].animate.set_color(ALERT), run_time=0.9)

        tot = VGroup(side("all five:", 0, 0), txt("expected", 22, MUTED), big("42.0", 0, 0, 30), txt("=", 24, MUTED), txt("observed", 22, MUTED),
                     big("42", 0, 0, 30)).arrange(RIGHT, buff=0.22).move_to([-0.6, -2.5, 0])
        with self.nar("s5_4", gap=0.7) as seg:
            self.play(*[FadeIn(rows[n]["raw"]) for n in ("Cedar", "Dune", "Elm")], run_time=0.6)
            seg.wait_until(seg.word(0, "add up to"))
            self.play(*[Indicate(rows[n]["bar"][1], color=ACCENT, scale_factor=1.03) for n in ORDER], FadeIn(tot, shift=UP * 0.1), run_time=1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S06
class S06_Flaw(EpisodeScene):
    def construct(self):
        tag = chapter_tag(4, "Who built the standard?")
        chips_, k = [], 0
        for n in ORDER:
            nl, el = CLINICS[n]["low"]
            for j in range(nl):
                c = chip(CLINICS[n]["color"], j < el, 0.13).move_to([-3.24 + (k // 3) * 0.36, 2.2 - (k % 3) * 0.36, 0])
                c.clinic, c.event = n, j < el
                chips_.append(c)
                k += 1
        head = side("lower-risk patients, all five clinics", 0, 2.75)
        r1 = VGroup(txt("13 of 57", 24, MUTED), big("22.8%", 0, 0, 34)).arrange(RIGHT, buff=0.3).move_to([0, 0.85, 0])
        with self.nar("s6_1") as seg:
            self.play(FadeIn(tag), FadeIn(head), LaggedStart(*[GrowFromCenter(c) for c in chips_], lag_ratio=0.015), run_time=1.8)
            self.play(FadeIn(r1, shift=UP * 0.1), run_time=0.7)

        mine = [c for c in chips_ if c.clinic == "Alder"]
        rest = [c for c in chips_ if c.clinic != "Alder"]
        box = SurroundingRectangle(VGroup(*mine), color=ALDER, buff=0.13, corner_radius=0.12, stroke_width=3)
        own = txt("Alder's own: 24, with 8 readmitted", 21, ALDER).next_to(box, DOWN, buff=0.16).align_to(box, LEFT)
        with self.nar("s6_2") as seg:
            seg.wait_until(seg.word(0, "twenty-four are Alder's") - 0.2)
            self.play(Create(box), run_time=0.9)
            seg.wait_until(seg.s(0) + seg.word(0, "And they supplied") - seg.s(0))
            self.play(*pulse([c for c in mine if c.event], 1.4), FadeIn(own), r1.animate.shift(RIGHT * 3.3), run_time=1.1)

        r2 = VGroup(txt("5 of 33", 24, MUTED), big("15.2%", 0, 0, 34, ACCENT)).arrange(RIGHT, buff=0.3).move_to([0, 0.85, 0])
        u, x0, yo = 0.36, -4.2, -0.55
        row = obs_row("Alder", x0, yo, u, 0.13)
        p1, f1 = exp_bar("Alder", x0, yo - 0.62, u, 0.28)
        p2, f2 = exp_bar("Alder", x0, yo - 1.3, u, 0.28, OTHERS)
        E1, E2 = expected("Alder"), expected("Alder", OTHERS)
        labs = VGroup(side("observed", x0 - 0.95, yo), side("expected", x0 - 0.95, yo - 0.62), side("expected", x0 - 0.95, yo - 1.3))
        t0 = VGroup(big("13", 0, 0, 28)).move_to([x0 + 13 * u + 0.4, yo, 0])
        t1 = VGroup(big(f"{E1:.1f}", 0, 0, 28), txt("pooled standard", 20, MUTED), big(f"ratio {13 / E1:.2f}", 0, 0, 28)).arrange(RIGHT, buff=0.35)
        t1.move_to([x0 + E1 * u + 0.3, yo - 0.62, 0], aligned_edge=LEFT)
        t2 = VGroup(big(f"{E2:.1f}", 0, 0, 28), txt("everyone else", 20, MUTED), big(f"ratio {13 / E2:.2f}", 0, 0, 28, ACCENT)).arrange(RIGHT, buff=0.35)
        t2.move_to([x0 + E2 * u + 0.3, yo - 1.3, 0], aligned_edge=LEFT)
        with self.nar("s6_3", gap=0.8) as seg:
            self.play(FadeOut(VGroup(*mine, box, own), shift=UP * 0.4), *[c.animate.shift(LEFT * 1.44) for c in rest],
                      FadeOut(r1), FadeIn(r2), run_time=1.6)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(row), FadeIn(VGroup(p1, f1)), FadeIn(labs[:2]), FadeIn(t0), FadeIn(t1), run_time=1.2)
            seg.wait_until(seg.word(1, "Against everyone else"))
            self.play(FadeIn(VGroup(p2, f2), shift=UP * 0.1), FadeIn(labs[2]), FadeIn(t2), run_time=1.2)
            self.play(Indicate(t2[2], color=ACCENT, scale_factor=1.25), run_time=0.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S07
class S07_Rule(EpisodeScene):
    def construct(self):
        tag = chapter_tag(5, "A bent risk rule")
        R = logit_ruler(-2.05, x0=-2.6, x1=5.0)

        def step(label, color, lo, hi, y, mult, start=None):
            a = logit(lo) if start is None else start
            b = a + (logit(hi) - logit(lo))
            return VGroup(txt(label, 22, color, weight=SEMIBOLD).move_to([-5.3, y, 0]),
                          Circle(radius=0.11, stroke_color=color, stroke_width=3).set_fill(INK, 1).move_to([R.X(a), y, 0]),
                          step_arrow([R.X(a) + 0.15, y, 0], [R.X(b) - 0.15, y, 0], color=color, tip=0.12),
                          Dot([R.X(b), y, 0], radius=0.115, color=color),
                          big(mult, R.X(b) + 0.75, y, 26, color))

        pooled = step("the pool", PAPER, POOL[False], POOL[True], 2.35, "\u00d7 5.8")
        within = step("inside clinics", ACCENT, POOL[False], POOL[True], 1.7, "\u00d7 7.5", start=logit(POOL[False]))
        within[2].become(step_arrow([R.X(logit(POOL[False])) + 0.15, 1.7, 0], [R.X(logit(POOL[False]) + float(np.log(7.417))) - 0.15, 1.7, 0], tip=0.12))
        within[3].move_to([R.X(logit(POOL[False]) + float(np.log(7.417))), 1.7, 0])
        within[4].move_to([R.X(logit(POOL[False]) + float(np.log(7.417))) + 0.75, 1.7, 0])
        cl = {n: step(n, CLINICS[n]["color"], CLINICS[n]["low"][1] / CLINICS[n]["low"][0], CLINICS[n]["high"][1] / CLINICS[n]["high"][0], y, m)
              for n, y, m in (("Alder", 0.85, "\u00d7 10"), ("Dune", 0.25, "\u00d7 10"), ("Cedar", -0.35, "\u00d7 6"), ("Birch", -0.95, "\u00d7 5.9"))}
        legend = VGroup(Circle(radius=0.1, stroke_color=MUTED, stroke_width=3), txt("lower risk", 19, MUTED), Dot(radius=0.105, color=MUTED),
                        txt("higher risk", 19, MUTED)).arrange(RIGHT, buff=0.18).move_to([4.6, 3.05, 0])
        with self.nar("s7_1") as seg:
            self.play(FadeIn(tag), FadeIn(R.g), FadeIn(legend), run_time=1.0)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(pooled[0]), GrowFromCenter(pooled[1]), run_time=0.6)
            self.play(GrowArrow(pooled[2]), FadeIn(pooled[3]), run_time=1.0)
            self.play(FadeIn(pooled[4], shift=LEFT * 0.1), run_time=0.6)

        with self.nar("s7_2") as seg:
            for n, cue in (("Alder", "ten at Alder"), ("Dune", "ten at Dune"), ("Cedar", "about six"), ("Birch", "and at Birch")):
                seg.wait_until(seg.word(0, cue) - 0.5)
                self.play(FadeIn(cl[n][0]), GrowFromCenter(cl[n][1]), GrowArrow(cl[n][2]), FadeIn(cl[n][3]), FadeIn(cl[n][4]), run_time=0.9)
            seg.wait_until(seg.s(1))
            self.play(FadeIn(within[0]), GrowFromCenter(within[1]), GrowArrow(within[2]), FadeIn(within[3]), FadeIn(within[4]), run_time=1.1)
            self.play(Indicate(within[4], color=ACCENT, scale_factor=1.3), run_time=0.8)

        g1 = DashedLine(cl["Alder"][1].get_center(), pooled[1].get_center() + DOWN * 0.14, dash_length=0.07, stroke_width=2, color=ALDER)
        g2 = DashedLine(cl["Birch"][3].get_center(), pooled[3].get_center() + DOWN * 0.14, dash_length=0.07, stroke_width=2, color=BIRCH)
        with self.nar("s7_3", gap=0.8) as seg:
            seg.wait_until(seg.word(0, "Most higher-risk"))
            self.play(Create(g2), Indicate(cl["Birch"][3], color=BIRCH, scale_factor=1.8), run_time=1.2)
            seg.wait_until(seg.word(0, "Most lower-risk"))
            self.play(Create(g1), Indicate(cl["Alder"][1], color=ALDER, scale_factor=1.8), run_time=1.2)
            seg.wait_until(seg.s(1))
            self.play(Indicate(pooled[2], color=ALERT, scale_factor=1.05), Indicate(pooled[4], color=ALERT, scale_factor=1.3), run_time=1.1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)


# =================================================================================== S08
class S08_Recap(EpisodeScene):
    def construct(self):
        tag = chapter_tag(6, "Recap")
        xs = (-4.45, 0.0, 4.45)
        cards = VGroup(*[card(4.05, 3.7).move_to([x, 0.15, 0]) for x in xs])
        icon1 = VGroup(*[risk_chip(p, r=0.2, color=CEDAR).move_to([-1.0 + 0.5 * k, 0.35, 0]) for k, p in enumerate((0.2, 0.2, 0.6, 0.6, 0.2))],
                       DashedVMobject(Rectangle(width=1.6, height=0.22, stroke_color=CEDAR, stroke_width=2.5).move_to([-0.3, -0.35, 0]), num_dashes=22))
        icon2 = VGroup(*[chip(ALDER, True, 0.1).move_to([-1.2 + 0.27 * k, 0.25, 0]) for k in range(9)],
                       DashedVMobject(Rectangle(width=1.7, height=0.22, stroke_color=ALDER, stroke_width=2.5).move_to([-0.48, -0.2, 0]), num_dashes=22),
                       DoubleArrow([0.4, -0.2, 0], [1.12, -0.2, 0], buff=0, stroke_width=3, color=ACCENT, tip_length=0.12))
        icon3 = VGroup(DashedVMobject(Rectangle(width=2.0, height=0.26, stroke_color=PAPER, stroke_width=2.5), num_dashes=26),
                       big("?", 0, 0.55, 40, ACCENT))
        icons = [icon1, icon2, icon3]
        caps = [["Expected: a sum of probabilities", "over a clinic's own patients"], ["Observed minus expected,", "and observed over expected"],
                ["Only as fair as", "the standard behind them"]]
        captions = VGroup()
        for k, (ic, cp) in enumerate(zip(icons, caps)):
            ic.move_to([xs[k], 0.8, 0])
            captions.add(VGroup(*[txt(s, 21, PAPER) for s in cp]).arrange(DOWN, buff=0.1).move_to([xs[k], -0.85, 0]))
        with self.nar("s8_1") as seg:
            self.play(FadeIn(tag), run_time=0.8)
            for k in range(3):
                seg.wait_until(seg.s(k + 1) - 0.1)
                self.play(FadeIn(cards[k], shift=UP * 0.15), FadeIn(captions[k], shift=UP * 0.1), FadeIn(icons[k], shift=UP * 0.1), run_time=1.1)

        need = big("A fair standard needs", 0, 2.2, 34)
        n1 = VGroup(big("1", 0, 0, 30, ACCENT), txt("a risk rule learned from patients who share a clinic", 26, PAPER)).arrange(RIGHT, buff=0.35).move_to([0, 1.15, 0])
        n2 = VGroup(big("2", 0, 0, 30, ACCENT), txt("a yardstick no single clinic can bend", 26, PAPER)).arrange(RIGHT, buff=0.35).move_to([0, 0.4, 0]).align_to(n1, LEFT)
        with self.nar("s8_2") as seg:
            self.play(FadeOut(VGroup(cards, captions, *icons)), run_time=0.7)
            self.play(FadeIn(need, shift=UP * 0.1), run_time=0.7)
            seg.wait_until(seg.word(0, "a risk rule"))
            self.play(FadeIn(n1, shift=RIGHT * 0.15), run_time=0.8)
            seg.wait_until(seg.word(0, "and a yardstick"))
            self.play(FadeIn(n2, shift=RIGHT * 0.15), run_time=0.8)

        lines = VGroup(*[Line([3.0, y, 0], [6.2, y + 0.9, 0], stroke_width=5, color=CLINICS[n]["color"])
                         for n, y in (("Dune", -1.5), ("Alder", -1.7), ("Cedar", -2.2), ("Birch", -2.4), ("Elm", -2.85))])
        nxt = VGroup(txt("Next:", 26, MUTED), big("one intercept per provider", 0, 0, 36)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN).move_to([-1.6, -1.75, 0])
        with self.nar("s8_3") as seg:
            seg.wait_until(seg.word(0, "every clinic gets"))
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.2), run_time=1.6)
            self.play(FadeIn(nxt, shift=UP * 0.15), run_time=0.8)

        mark, word = logo_mark(1.0), wordmark(54)
        head = VGroup(mark, word).arrange(RIGHT, buff=0.5).move_to(UP * 0.7)
        ep = txt("NEXT  \u00b7  EPISODE 4  \u00b7  ONE INTERCEPT PER PROVIDER", 22, MUTED, weight=MEDIUM).next_to(head, DOWN, buff=0.6)
        thanks = txt("thanks for following the story", 28, PAPER, font=SERIF, slant=ITALIC).next_to(ep, DOWN, buff=0.45)
        with self.nar("s8_4", gap=1.8) as seg:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
            self.play(FadeIn(head, shift=UP * 0.15), FadeIn(ep), run_time=1.0)
            self.play(FadeIn(thanks, shift=UP * 0.1), run_time=0.8)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.0)
