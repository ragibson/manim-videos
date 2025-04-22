from manim import *


class PointWithTrace(Scene):
    def construct(self):
        # this path does not actually display as of 0.19.0
        # see https://github.com/ManimCommunity/manim/issues/4218
        path = VMobject()
        dot = Dot()

        path.set_points_as_corners([dot.get_center(), dot.get_center()])

        def update_path(path):
            previous_path = path.copy()
            previous_path.add_points_as_corners([dot.get_center()])  # adding the _new_ center of dot
            path.become(previous_path)

        path.add_updater(update_path)

        self.add(path, dot)
        self.play(Rotating(dot, radians=PI, about_point=RIGHT, run_time=2))
        self.wait()
        self.play(dot.animate.shift(UP))
        self.play(dot.animate.shift(LEFT))
        self.wait()
