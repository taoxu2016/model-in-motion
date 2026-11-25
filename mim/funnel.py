"""Model in Motion: the funnel. A provider's ratio against its precision, with the two edges that mark what luck allows.

Shared from Episode 15 on. Precision runs along the bottom on a square-root scale, so that small clinics are not
crushed against the left edge and the two edges, 1 +- z / sqrt(precision), are smooth curves.
"""
from mim.common import *  # noqa: F401,F403
from mim.boards import side


class Funnel:
    """Ratio (observed over expected) against precision (expected squared over its variance)."""

    def __init__(self, x0=-5.6, x1=1.6, y0=-2.15, y1=2.25, p_lo=1.5, p_hi=125.0, r_lo=-0.45, r_hi=2.45, ticks=(5, 10, 20, 40, 80, 120), z=1.959964):
        self.x0, self.x1, self.y0, self.y1, self.p_lo, self.p_hi, self.r_lo, self.r_hi, self.ticks, self.z = x0, x1, y0, y1, p_lo, p_hi, r_lo, r_hi, ticks, z

    def X(self, precision):
        a, b = np.sqrt(self.p_lo), np.sqrt(self.p_hi)
        return self.x0 + (self.x1 - self.x0) * (np.sqrt(precision) - a) / (b - a)

    def Y(self, ratio):
        return self.y0 + (self.y1 - self.y0) * (ratio - self.r_lo) / (self.r_hi - self.r_lo)

    def P(self, precision, ratio):
        return np.array([self.X(precision), self.Y(ratio), 0.0])

    def limits(self, precision):
        """The lower and upper edge at a precision: what luck allows for a provider like the reference."""
        d = self.z / np.sqrt(precision)
        return 1.0 - d, 1.0 + d

    def axes(self, r_ticks=(0, 0.5, 1, 1.5, 2), x_label="precision: how much a provider can tell us", y_label="ratio"):
        frame = VGroup(Line([self.x0, self.y0, 0], [self.x1, self.y0, 0], stroke_width=3, color=MUTED), Line([self.x0, self.y0, 0], [self.x0, self.y1, 0], stroke_width=3, color=MUTED))
        xt = VGroup(*[VGroup(Line([self.X(v), self.y0, 0], [self.X(v), self.y0 - 0.1, 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([self.X(v), self.y0 - 0.28, 0])) for v in self.ticks])
        yt = VGroup(*[VGroup(Line([self.x0 - 0.1, self.Y(v), 0], [self.x0, self.Y(v), 0], stroke_width=2, color=MUTED), txt(f"{v:g}", 15, MUTED).move_to([self.x0 - 0.35, self.Y(v), 0])) for v in r_ticks])
        one = DashedLine([self.x0, self.Y(1.0), 0], [self.x1, self.Y(1.0), 0], dash_length=0.1, stroke_width=2.5, color=CEDAR)
        labels = VGroup(side(x_label, size=16).move_to([(self.x0 + self.x1) / 2, self.y0 - 0.6, 0]), side(y_label, size=16).move_to([self.x0 + 0.25, self.y1 + 0.24, 0]))
        return VGroup(frame, xt, yt, one, labels)

    def edges(self, color=ACCENT, width=3.5):
        """The funnel's two edges, clipped to the chart."""
        a, b = float(np.sqrt(self.p_lo)), float(np.sqrt(self.p_hi))
        upper = ParametricFunction(lambda s: self.P(s * s, min(1.0 + self.z / s, self.r_hi)), t_range=[a, b, 0.05], color=color, stroke_width=width)
        lower = ParametricFunction(lambda s: self.P(s * s, max(1.0 - self.z / s, self.r_lo)), t_range=[a, b, 0.05], color=color, stroke_width=width)
        return VGroup(upper, lower).set_z_index(3)

    def band(self, precision, color=PAPER, width=5, caps=True):
        """The upright band at one precision: the stretch of ratios that luck allows there."""
        lo, hi = self.limits(precision)
        lo, hi = max(lo, self.r_lo), min(hi, self.r_hi)
        g = VGroup(Line(self.P(precision, lo), self.P(precision, hi), stroke_width=width, color=color))
        if caps:
            g.add(*[Line(self.P(precision, v) + LEFT * 0.12, self.P(precision, v) + RIGHT * 0.12, stroke_width=width * 0.7, color=color) for v in (lo, hi)])
        return g

    def dot(self, precision, ratio, color=PAPER, radius=0.05, opacity=1.0):
        return Dot(self.P(precision, min(max(ratio, self.r_lo), self.r_hi)), radius=radius, color=color).set_opacity(opacity)
