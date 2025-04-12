from manim import *


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


class SquareToCircleSections(Scene):
    # The animation sections here also get automatically exported as long as
    # manim is called with the --save-sections flag
    def construct(self):
        circle = Circle()
        circle.set_fill(PINK, opacity=0.5)
        square = Square()
        square.rotate(PI / 4)

        # can also skip animations of a section with
        #   self.next_section(skip_animations=True)
        self.play(Create(square))
        self.next_section("Some section name")
        self.play(Transform(square, circle))
        self.next_section("Another section name")
        self.play(FadeOut(square))

# Various other quality presets are:
#   -ql  854x480  15 fps
#   -qm 1280x720  30 fps
#   -l  1920x1080 60 fps
#   -u  3840x2160 60 fps
#
# A few other useful flags are:
#   -a: render all scenes in file
#   -p: play animation once rendered
#   --show_in_file_browser: open file browser at animation location
#   --format: to render out other file formats (e.g., --format gif)
