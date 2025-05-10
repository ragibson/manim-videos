from manim import *

from data import OCC_options_ADV  # noqa


# TODO: also want "title card" style animation at the beginning

class BlackScholesIntroduction(Scene):
    def construct(self):
        title = Text("Black-Scholes Formula", font_size=48)
        title.to_edge(UP, buff=0.5)
        subtitle = Text("(or the Black-Scholes-Merton formula)", font_size=32)
        subtitle.next_to(title, DOWN, buff=0.25)

        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(subtitle), run_time=1.0)
        self.wait(1)
