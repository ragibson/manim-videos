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


class AnimateExample(Scene):
    def construct(self):
        square = Square().set_fill(RED, opacity=1.0)
        self.add(square)

        # any property that can be changed can be animated and any method
        # that changes an mobject's property can be used as an animation
        self.play(square.animate.set_fill(WHITE))
        self.wait(1)

        # the shift and rotate here occur at the same time
        # animate() is a property of all mobjects that animates all the
        # methods that come afterwards
        self.play(square.animate.shift(UP).rotate(PI / 3))
        self.wait(1)


class RunTime(Scene):
    def construct(self):
        square = Square()
        self.add(square)
        # default run time is 1 second but can be changed
        self.play(square.animate.shift(UP), run_time=3)
        self.wait(1)


# You can define your own custom animation if you ever need to smoothly
# animate from one state of an Mobject to another in a way that is not already
# built in to Manim.
#
# To do so, we just extend the Animation class and override
# interpolate_mobject(), which receives a parameter alpha that varies
# throughout the animation, starting at 0 and moving to 1.
class Count(Animation):
    def __init__(self, number: DecimalNumber, start: float, end: float,
                 **kwargs):
        # initialize Mobject with passed DecinalNumber
        super().__init__(number, **kwargs)
        self.start = start
        self.end = end

    def interpolate_mobject(self, alpha: float) -> None:
        value = self.start + (alpha * (self.end - self.start))
        self.mobject.set_value(value)


class CountingScene(Scene):
    def construct(self):
        number = DecimalNumber().set_color(WHITE).scale(5)
        # add updater to recenter the DecimalNumber as it changes
        number.add_updater(lambda number: number.move_to(ORIGIN))

        self.add(number)
        self.wait()

        # play Count animation from 0 to 100 over 4 seconds
        self.play(Count(number, 0, 100), run_time=4, rate_func=linear)
        self.wait()


# Mobjects contain points that define their boundaries, e.g., get_center(),
# get_top(), and get_start()
class MobjectBounds(Scene):
    def construct(self):
        p1 = [-1, -1, 0]
        p2 = [1, -1, 0]
        p3 = [1, 1, 0]
        p4 = [-1, 1, 0]

        a = (Line(p1, p2).append_points(Line(p2, p3).points)
             .append_points(Line(p3, p4).points))
        point_start = a.get_start()
        point_end = a.get_end()
        point_center = a.get_center()
        self.add(Text(f"a.get_start() = {np.round(point_start, 2).tolist()}",
                      font_size=24).to_edge(UR).set_color(YELLOW))
        self.add(Text(f"a.get_end() = {np.round(point_end, 2).tolist()}",
                      font_size=24).next_to(self.mobjects[-1], DOWN).set_color(RED))
        self.add(Text(f"a.get_center() = {np.round(point_center, 2).tolist()}",
                      font_size=24).next_to(self.mobjects[-1], DOWN).set_color(BLUE))

        # In short,
        #   p4 (end) ------- top ------------ p3
        #                                     |
        #                   center     from_proportion(0.5)
        #                                     |
        #   p1 (start) ---- bottom ---------- p2
        self.add(Dot(a.get_start()).set_color(YELLOW).scale(2))
        self.add(Dot(a.get_end()).set_color(RED).scale(2))
        self.add(Dot(a.get_top()).set_color(GREEN_A).scale(2))
        self.add(Dot(a.get_bottom()).set_color(GREEN_D).scale(2))
        self.add(Dot(a.get_center()).set_color(BLUE).scale(2))
        self.add(Dot(a.point_from_proportion(0.5)).set_color(ORANGE).scale(2))
        self.add(*[Dot(x) for x in a.points])
        self.add(a)


class ExampleTransform(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1 = Square().set_color(RED)
        m2 = Rectangle().set_color(RED).rotate(0.2)

        # we can transform an mobject into another, which actually just maps
        # the points of the previous mobject to those of the next
        self.play(Transform(m1, m2))


class ExampleRotation(Scene):
    def construct(self):
        self.camera.background_color = WHITE
        m1a = Square().set_color(RED).shift(LEFT)
        m1b = Circle().set_color(RED).shift(LEFT)
        m2a = Square().set_color(BLUE).shift(RIGHT)
        m2b = Circle().set_color(BLUE).shift(RIGHT)

        # since Transforms operate pointwise, we may need to flip objects and
        # reposition points via np.roll for the animation to look right

        points = m2a.points
        # reorder points so top-right corner gets mapped to top of circle
        points = np.roll(points, int(len(points) / 4), axis=0)
        m2a.points = points

        self.play(Transform(m1a, m1b), Transform(m2a, m2b), run_time=1)

# Again,
#   * Scene is the connective tissue of the animation
#   * Every Mobject gets "added" to a scene to display or "removed" to hide
#   * Every animation has to be "played" by a scene
#   * Every time interval without animation is determined by calls to wait()
#   * All code of a video must be contained in the construct() method of a
#     class derived from Scene
#   * Files can contain multiple Scenes if the corresponding video scenes are
#     to be rendered at the same time
