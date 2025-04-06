from manim import *


class CreateCircle(Scene):
    # "Animating a circle"
    # Scene is the class through which Manim generates videos
    def construct(self):
        # all animations must reside within the construct() method
        # helper functions may reside outside the class
        circle = Circle()  # create a circle
        circle.set_fill(PINK, opacity=0.5)  # set the color and transparency
        self.play(Create(circle))  # show the circle on screen


class SquareToCircle(Scene):
    # "Transforming a square into a circle"
    def construct(self):
        # create circle, pink and 50% transparent
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)

        # create square, rotated 1/8th turn
        square = Square()
        square.rotate(PI / 4)

        # animate
        #  1) square creation
        #  2) transformation into a circle
        #  3) final fade out
        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))
