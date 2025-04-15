from manim import *


class MovingDots(Scene):
    def construct(self):
        d1, d2 = Dot(color=BLUE), Dot(color=GREEN)
        dg = VGroup(d1, d2).arrange(RIGHT, buff=1)  # this actually moves d2
        l1 = Line(d1.get_center(), d2.get_center()).set_color(RED)

        x, y = ValueTracker(0), ValueTracker(0)

        # updaters to move the dots according to ValueTrackers x, y
        d1.add_updater(lambda z: z.set_x(x.get_value()))
        d2.add_updater(lambda z: z.set_y(y.get_value()))
        l1.add_updater(lambda z: z.become(Line(d1.get_center(), d2.get_center())))

        self.add(d1, d2, l1)
        self.play(x.animate.set_value(5))
        self.play(y.animate.set_value(4))
        self.play(x.animate.set_value(2), y.animate.set_value(3))
        self.wait()
