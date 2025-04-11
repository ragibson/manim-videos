from manim import *


# Manim provides three different concepts
#   the mobject ("mathematical objects")
#   the animation, and
#   the scene

# Each class that derives from Mobject represents an object that can be
# displayed on the screen. E.g., Circle, Arrow, Rectangle, Axes,
# FunctionGraph, and BarChart.
#
# That said, Mobject itself is just an abstract base class, so displaying it
# would just result in an empty frame.
#
# Most of the time, we'll be dealing with the derived class VMobject
# ("vectorized Mobject"), i.e., an mobject that uses vector graphics for
# display.


class CreatingMobjects(Scene):
    def construct(self):
        circle = Circle()

        # add() is the principal way of displaying mobjects when not animated
        self.add(circle)
        self.wait(1)
        self.remove(circle)  # likewise, remove() removes it from the scene
        self.wait(1)


class PlacingShapes(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # notably, manim's coordinates start at the center of the screen (i.e.,
        # the origin with down/up being -y / +y and left/right being -x / +x)
        circle.shift(LEFT)
        square.shift(UP)
        triangle.shift(RIGHT)

        # again, this seems to accept an iterable *mobjects
        self.add(circle, square, triangle)
        self.wait(1)


class MobjectPlacement(Scene):
    def construct(self):
        circle = Circle()
        square = Square()
        triangle = Triangle()

        # can also place mobjects with move_to(), next_to(), align_to()

        # two units left of origin, absolute units
        circle.move_to(LEFT * 2)

        # relative units, one unit left of circle mobject passed
        square.next_to(circle, LEFT)

        # aligning to the left border of circle (imaginary bounding box)
        triangle.align_to(circle, LEFT)

        self.add(circle, square, triangle)
        self.wait(1)


class MobjectStyling(Scene):
    def construct(self):
        # manipulating returned objects and then assigning them to variables
        circle = Circle().shift(LEFT)
        square = Square().shift(UP)
        triangle = Triangle().shift(RIGHT)

        # set_stroke() sets visual style of mobject's border
        circle.set_stroke(color=GREEN, width=20)

        # set_fill() changes style of mobject's interior. the default opacity
        # is 0.0 (fully transparent), so the opacity needs to specified
        square.set_fill(YELLOW, opacity=1.0)
        triangle.set_fill(PINK, opacity=0.5)

        # VMobjects implement set_stroke/set_fill while Mobjects actually
        # implement set_color instead, but usually we're using VMobjects

        # order matters here! E.g.,
        #   self.add(triangle, square, circle)
        # would have the triangle drawn first (visually "at the back")
        self.add(circle, square, triangle)
        self.wait(1)


class SomeAnimations(Scene):
    def construct(self):
        square = Square()

        # play() generally adds animations to the scene
        self.play(FadeIn(square))  # display
        self.play(Rotate(square, PI / 4))  # moving/rotating
        self.play(FadeOut(square))  # remove
        self.wait(1)

        # all of these just interpolate between two mobjects, sometimes with
        # one version being completely transparent for fading in/out
        # similarly, Rotate() interpolates the mobject's angle
