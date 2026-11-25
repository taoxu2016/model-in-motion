"""Model in Motion: drawing kit shared from Episode 2 on (rulers, risk chip, step arrow)."""
from mim.common import *  # noqa: F401,F403

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
