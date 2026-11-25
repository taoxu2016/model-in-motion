"""Model in Motion: piles. A histogram of counts, one bar for each whole number, shared from Episode 13 on.

`Hist` draws the bars, the axis, a marker for an observed count and, from Episode 14, a bell curve to the same scale.
The numbers behind a pile come from mim.castfit (coin_pmf, mid_p); nothing here computes a probability of its own
except the bell curve's height.
"""
from mim.common import *  # noqa: F401,F403
from mim.boards import side


class Hist:
    """A histogram of counts: one bar for each whole number of readmissions."""

    def __init__(self, x0, x1, y0, y1, k_max, p_max):
        self.x0, self.x1, self.y0, self.y1, self.k_max, self.p_max = x0, x1, y0, y1, k_max, p_max
        self.step = (x1 - x0) / (k_max + 1)

    def X(self, k):                     # the centre of the bar for count k; also used for positions between whole counts
        return self.x0 + self.step * (k + 0.5)

    def H(self, p):
        return (self.y1 - self.y0) * p / self.p_max

    def bar(self, k, p, color=PAPER, opacity=0.9, outline=False):
        h = max(self.H(p), 0.004)
        r = Rectangle(width=self.step * 0.8, height=h, stroke_color=color, stroke_width=2.5 if outline else 0, fill_color=color, fill_opacity=0 if outline else opacity)
        return r.move_to([self.X(k), self.y0 + h / 2, 0])

    def bars(self, pmf, color=PAPER, colors=None, opacity=0.9, outline=False):
        return VGroup(*[self.bar(k, pmf[k] if k < len(pmf) else 0.0, colors[k] if colors else color, opacity, outline) for k in range(self.k_max + 1)])

    def axis(self, every=1, label="readmissions"):
        return VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], stroke_width=3, color=MUTED),
                      VGroup(*[txt(str(k), 15, MUTED).move_to([self.X(k), self.y0 - 0.25, 0]) for k in range(0, self.k_max + 1, every)]),
                      side(label, size=16).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.58, 0]))

    def marker(self, k, label, color, top):
        """An arrow pointing down at the bar for count k, labelled beside it, where the neighbouring bars are low."""
        tip = np.array([self.X(k), top + 0.1, 0.0])
        a = Arrow(tip + UP * 0.75, tip, buff=0, stroke_width=5, color=color, max_tip_length_to_length_ratio=0.3).set_z_index(6)
        return VGroup(a, txt(label, 18, color, weight=SEMIBOLD).next_to(a, RIGHT, buff=0.14).shift(UP * 0.12))

    @staticmethod
    def density(x, mean, sd):
        return float(np.exp(-0.5 * ((x - mean) / sd) ** 2) / (sd * np.sqrt(2.0 * np.pi)))

    def bell(self, mean, sd, lo=None, hi=None, color=ACCENT, width=4):
        """A bell curve with the given centre and spread, drawn to the same scale as the bars (each bar is one unit wide)."""
        lo, hi = (-0.5 if lo is None else lo), (self.k_max + 0.5 if hi is None else hi)
        return ParametricFunction(lambda x: np.array([self.X(x), self.y0 + self.H(self.density(x, mean, sd)), 0.0]), t_range=[lo, hi, 0.05], color=color, stroke_width=width).set_z_index(5)

    def bell_area(self, mean, sd, a, b, color=ACCENT, opacity=0.5):
        """The region under that bell curve between a and b."""
        top = [np.array([self.X(x), self.y0 + self.H(self.density(x, mean, sd)), 0.0]) for x in np.linspace(a, b, 40)]
        return Polygon(*top, np.array([self.X(b), self.y0, 0.0]), np.array([self.X(a), self.y0, 0.0]), stroke_width=0, fill_color=color, fill_opacity=opacity).set_z_index(4)


def tail_colors(observed, k_max, on, off=PAPER):
    """Bar colours that pick out the counts at or beyond the observed one."""
    return [on if k >= observed else off for k in range(k_max + 1)]
