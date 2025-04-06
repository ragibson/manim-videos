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


class SquareAndCircle(Scene):
    # Positioning `Mobject`s
    def construct(self):
        # same as before, setting up two shapes
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        # setting a position for one object relative to another
        square.next_to(circle, RIGHT, buff=0.5)

        # interesting, play() seems to simultaneously play an iterable of animations
        self.play(Create(circle), Create(square))


class AnimatedSquareToCircle(Scene):
    # Using `.animate` syntax to animate methods
    def construct(self):
        circle = Circle()
        square = Square()

        # `.animate` here shows the rotate and set_fill actions being applied
        # to the objects dynamically rather than when they're created
        self.play(Create(square))
        self.play(square.animate.rotate(PI / 4))
        self.play(Transform(square, circle))
        self.play(square.animate.set_fill(PINK, opacity=0.5))


class DifferentRotations(Scene):
    def construct(self):
        left_square = Square(color=BLUE, fill_opacity=0.7).shift(2 * LEFT)
        right_square = Square(color=GREEN, fill_opacity=0.7).shift(2 * RIGHT)
        # typical animations are just an interpolation between the starting
        # and ending state, so the left square here appears to shrink and grow
        # rather than visually rotate. The conventional animation method
        # Rotate() fixes this quirk.
        self.play(
            left_square.animate.rotate(PI), Rotate(right_square, angle=PI),
            run_time=2
        )
        self.wait()


class TwoTransforms(Scene):
    # `Transform` vs. `ReplacementTransform`
    #
    # Transform transforms the points (and attributes, e.g., color) of one
    # object into another while ReplacementTransform literally replaces one
    # object on the scene with another.
    #
    # The use of one over the other is mostly up to personal preference
    def transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        self.play(Transform(a, b))  # a gets transformed into b
        self.play(Transform(a, c))  # a (again) gets transformed into c
        self.play(FadeOut(a))

    def replacement_transform(self):
        a = Circle()
        b = Square()
        c = Triangle()
        # a gets completely replaced by b
        self.play(ReplacementTransform(a, b))
        # b (not a) gets replaced by c
        self.play(ReplacementTransform(b, c))
        self.play(FadeOut(c))

    def construct(self):
        self.transform()
        self.wait(0.5)  # 0.5 second wait
        self.replacement_transform()


class TransformCycle(Scene):
    def construct(self):
        a = Circle()
        t1 = Square()
        t2 = Triangle()
        self.add(a)
        self.wait()
        for t in [t1, t2]:
            # here, Transform is more beneficial since you don't have to carry
            # around the reference to the last mobject that was transformed
            self.play(Transform(a, t))
