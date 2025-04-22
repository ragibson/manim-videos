from manim import *


class FixedInFrameMobjectTest(ThreeDScene):  # yet another specialized scene for 3D
    def construct(self):
        axes = ThreeDAxes()
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        text3d = Text("This is 3D text")
        self.add_fixed_in_frame_mobjects(text3d)
        text3d.to_corner(UL)

        self.add(axes)
        self.wait()
