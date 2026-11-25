"""Model in Motion: the line panel (log-odds), the curve panel (probability), the beta dial and the gamma sliders.

Shared from Episode 4 of the logistic fixed-effect arc on.

Dots are always drawn at their true heights. Clinics whose dots coincide are nested or split, never nudged
sideways: on a sloped line a sideways nudge changes a dot's distance from the line, and that distance is the point.
"""
from mim.common import *  # noqa: F401,F403
from mim.kit import expit, logit, signed  # noqa: F401

FOUR = ["Alder", "Birch", "Cedar", "Dune"]          # the clinics whose intercept has a finite estimate


def dot_radius(n):
    """Dot area is proportional to the number of patients."""
    return 0.036 * float(np.sqrt(n))


def observed(name, high):
    """(patients, readmitted, log-odds or None) for one clinic at one risk level."""
    n, e = CLINICS[name]["high" if high else "low"]
    return n, e, (logit(e / n) if 0 < e < n else None)


class LinePanel:
    """Log-odds against risk level. The left ruler reads log-odds, the right one probability: the same heights, two labellings."""

    def __init__(self, x_low=-4.6, x_high=-0.4, y0=-2.25, y1=2.6, lo=-3.4, hi=2.4, pad=1.4):
        self.xl, self.xh, self.y0, self.y1, self.lo, self.hi = x_low, x_high, y0, y1, lo, hi
        self.XL, self.XR = x_low - pad, x_high + pad
        left = Line([self.XL, y0, 0], [self.XL, y1, 0], stroke_width=3, color=MUTED)
        right = Line([self.XR, y0, 0], [self.XR, y1, 0], stroke_width=3, color=MUTED)
        lt, rt = VGroup(), VGroup()
        for v in range(-3, 3):
            lt.add(Line([self.XL - 0.1, self.Y(v), 0], [self.XL, self.Y(v), 0], stroke_width=2, color=MUTED))
            lt.add(txt(signed(v, 0), 17, MUTED).move_to([self.XL - 0.4, self.Y(v), 0]))
        for p in (0.05, 0.10, 0.20, 0.35, 0.50, 0.65, 0.80, 0.90):
            y = self.Y(logit(p))
            rt.add(Line([self.XR, y, 0], [self.XR + 0.1, y, 0], stroke_width=2, color=MUTED))
            rt.add(txt(f"{round(100 * p)}%", 17, PAPER).move_to([self.XR + 0.5, y, 0]))
        guides = VGroup(*[Line([x, y0, 0], [x, y1, 0], stroke_width=1.5, color=FAINT) for x in (x_low, x_high)],
                        Line([self.XL, self.Y(0), 0], [self.XR, self.Y(0), 0], stroke_width=1.5, color=FAINT))
        names = VGroup(txt("lower-risk patients", 20, PAPER).move_to([x_low, y0 - 0.32, 0]),
                       txt("higher-risk patients", 20, PAPER).move_to([x_high, y0 - 0.32, 0]))
        titles = VGroup(txt("log-odds", 18, MUTED, font=SERIF, slant=ITALIC).move_to([self.XL - 0.15, y1 + 0.28, 0]),
                        txt("probability", 18, MUTED, font=SERIF, slant=ITALIC).move_to([self.XR + 0.35, y1 + 0.28, 0]))
        self.g = VGroup(guides, left, right, lt, rt, names, titles)

    def X(self, t):                     # t = 0 at the lower-risk position, 1 at the higher-risk position
        return self.xl + (self.xh - self.xl) * t

    def Y(self, v):                     # v in log-odds
        return self.y0 + (self.y1 - self.y0) * (v - self.lo) / (self.hi - self.lo)

    def P(self, t, v):
        return np.array([self.X(t), self.Y(v), 0.0])

    def segment(self, gamma, beta, t0=-0.3, t1=1.3):
        """End points of the line log-odds = gamma + beta t, clipped to the panel's height (None if it lies outside)."""
        if abs(beta) > 1e-9:
            a, b = sorted(((self.lo - gamma) / beta, (self.hi - gamma) / beta))
            t0, t1 = max(t0, a), min(t1, b)
        elif not (self.lo <= gamma <= self.hi):
            return None
        if t1 - t0 < 1e-3:
            return None
        return self.P(t0, gamma + beta * t0), self.P(t1, gamma + beta * t1)

    def line(self, gamma, beta, color, width=4.5, dashed=False, t0=-0.3, t1=1.3):
        seg = self.segment(gamma, beta, t0, t1)
        if seg is None:
            return VMobject()
        if dashed:
            m = DashedLine(seg[0], seg[1], dash_length=0.14, stroke_width=width, color=color)
        else:
            m = Line(seg[0], seg[1], stroke_width=width, color=color)
        return m.set_z_index(3)

    def dots(self, names=FOUR):
        """Observed log-odds as dots, keyed by (clinic, high). Coinciding dots are nested (different sizes) or split."""
        out = {}
        for high in (False, True):
            groups = {}
            for name in names:
                n, e, v = observed(name, high)
                if v is not None:
                    groups.setdefault(round(v, 9), []).append((name, n))
            for v, members in groups.items():
                c = self.P(1 if high else 0, v)
                members.sort(key=lambda m: -m[1])                       # the largest first, so smaller dots sit on top
                same_size = len(members) > 1 and len({n for _, n in members}) == 1
                for k, (name, n) in enumerate(members):
                    col, r = CLINICS[name]["color"], dot_radius(n)
                    if same_size:                                        # equal dots at one spot: a disc split between them
                        ang = TAU / len(members)
                        d = Sector(radius=r, angle=ang, start_angle=PI / 2 + k * ang, stroke_width=0, fill_color=col, fill_opacity=1).shift(c)
                    else:
                        d = Dot(c, radius=r, color=col).set_stroke(INK, 1.5)
                    out[(name, high)] = d.set_z_index(4 + 0.1 * k)
        return out

    def elm_marker(self, label="Elm: 0 of 11"):
        """Elm has no readmissions, so its log-odds has no finite position: a hatched ring at the bottom edge."""
        r, c = dot_radius(CLINICS["Elm"]["low"][0]), self.P(0, self.lo + 0.42)
        ring = Circle(radius=r, stroke_color=ELM, stroke_width=3).move_to(c)
        u, w = np.array([1.0, 1.0, 0.0]) / np.sqrt(2), np.array([-1.0, 1.0, 0.0]) / np.sqrt(2)
        hatch = VGroup(*[Line(c + w * r * d - u * r * 0.9 * np.sqrt(1 - d * d), c + w * r * d + u * r * 0.9 * np.sqrt(1 - d * d),
                              stroke_width=2, color=ELM) for d in (-0.5, 0.0, 0.5)])
        tip = Triangle(fill_color=ELM, fill_opacity=1, stroke_width=0).scale(0.07).rotate(PI).move_to(c + DOWN * (r + 0.1))
        text = txt(label, 16, ELM).next_to(ring, RIGHT, buff=0.15)
        return VGroup(ring, hatch, tip, text).set_z_index(4)


class CurvePanel:
    """Probability against risk score: the same model on the probability ruler. Curves of one shape, slid sideways."""

    def __init__(self, beta, x0=-5.6, x1=1.0, y0=-2.25, y1=2.6, s_lo=-3.0, s_hi=4.6):
        self.beta, self.x0, self.x1, self.y0, self.y1, self.s_lo, self.s_hi = beta, x0, x1, y0, y1, s_lo, s_hi
        left = Line([x0, y0, 0], [x0, y1, 0], stroke_width=3, color=MUTED)
        bottom = Line([x0, y0, 0], [x1, y0, 0], stroke_width=3, color=MUTED)
        lt = VGroup()
        for p in (0, 0.25, 0.5, 0.75, 1.0):
            lt.add(Line([x0 - 0.1, self.Y(p), 0], [x0, self.Y(p), 0], stroke_width=2, color=MUTED))
            lt.add(txt(f"{round(100 * p)}%", 17, PAPER).move_to([x0 - 0.5, self.Y(p), 0]))
        guides = VGroup(*[Line([self.X(s), y0, 0], [self.X(s), y1, 0], stroke_width=1.5, color=FAINT) for s in (0, beta)],
                        Line([x0, self.Y(0.5), 0], [x1, self.Y(0.5), 0], stroke_width=1.5, color=FAINT))
        names = VGroup(txt("lower-risk", 18, PAPER).move_to([self.X(0), y0 - 0.32, 0]),
                       txt("higher-risk", 18, PAPER).move_to([self.X(beta), y0 - 0.32, 0]))
        title = txt("probability", 18, MUTED, font=SERIF, slant=ITALIC).move_to([x0 + 0.2, y1 + 0.28, 0])
        self.g = VGroup(guides, left, bottom, lt, names, title)

    def X(self, s):
        return self.x0 + (self.x1 - self.x0) * (s - self.s_lo) / (self.s_hi - self.s_lo)

    def Y(self, p):
        return self.y0 + (self.y1 - self.y0) * p

    def P(self, s, p):
        return np.array([self.X(s), self.Y(p), 0.0])

    def curve(self, gamma, color, width=4.5):
        return ParametricFunction(lambda s: self.P(s, expit(gamma + s)), t_range=[self.s_lo, self.s_hi, 0.05],
                                  color=color, stroke_width=width).set_z_index(3)

    def marker(self, gamma, high, color):
        s = self.beta if high else 0.0
        return Dot(self.P(s, expit(gamma + s)), radius=0.09, color=color).set_stroke(INK, 1.5).set_z_index(5)


class Dial(VGroup):
    """The beta dial: one knob that tilts every line."""

    def __init__(self, value, r=0.5, lo=0.0, hi=3.0):
        super().__init__()
        self.r, self.lo, self.hi, self.value = r, lo, hi, value
        self.face = Circle(radius=r, stroke_color=ACCENT, stroke_width=4).set_fill(INK_2, opacity=1)
        self.marks = VGroup(*[Line(self.unit(v) * (r + 0.05), self.unit(v) * (r + 0.14), stroke_width=2, color=MUTED)
                              for v in np.linspace(lo, hi, 7)])
        self.needle = Line(ORIGIN, self.unit(value) * r * 0.78, stroke_width=5, color=ACCENT)
        self.hub = Dot(ORIGIN, radius=0.05, color=ACCENT)
        self.add(self.face, self.marks, self.needle, self.hub)

    def unit(self, v):
        a = np.deg2rad(225 - 270 * (min(max(v, self.lo), self.hi) - self.lo) / (self.hi - self.lo))
        return np.array([np.cos(a), np.sin(a), 0.0])

    def turn_to(self, v):
        c = self.face.get_center()
        self.needle.put_start_and_end_on(c, c + self.unit(v) * self.r * 0.78)
        self.hub.move_to(c)
        self.value = v
        return self


class Slider(VGroup):
    """A gamma slider: one clinic's intercept, on a track that reads log-odds."""

    def __init__(self, name, value, h=1.5, lo=-3.2, hi=0.4, color=None, tag=True):
        super().__init__()
        self.h, self.lo, self.hi, self.value = h, lo, hi, value
        col = color or CLINICS[name]["color"]
        self.track = Line(DOWN * h / 2, UP * h / 2, stroke_width=4, color=FAINT)
        self.knob = Dot(radius=0.105, color=col).set_stroke(INK, 1.5)
        self.add(self.track, self.knob)
        if tag:
            self.tag = txt(name, 14, col, weight=SEMIBOLD).next_to(self.track, DOWN, buff=0.14)
            self.add(self.tag)
        self.slide_to(value)

    def pos(self, v):
        v = min(max(v, self.lo), self.hi)
        return self.track.get_bottom() + UP * self.h * (v - self.lo) / (self.hi - self.lo)

    def slide_to(self, v):
        self.knob.move_to(self.pos(v))
        self.value = v
        return self
