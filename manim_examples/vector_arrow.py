from manim import *


class VectorArrow(Scene):
    def construct(self):
        dot = Dot(ORIGIN)
        arrow = Arrow(ORIGIN, [2, 2, 0], buff=0)  # buff=0 forces arrow to go all the way to its start point

        numberplane = NumberPlane()  # wow, I guess this is common enough to warrant its own object

        origin_text = Text('(0, 0)').next_to(dot, DOWN)
        tip_text = Text('(2, 2)').next_to(arrow.get_end(), RIGHT)

        self.add(numberplane, dot, arrow, origin_text, tip_text)
