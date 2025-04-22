from manim import *


class MovingZoomedSceneAround(ZoomedScene):  # another special scene for zooming
    # originally contributed by www.youtube.com/c/TheoremofBeethoven
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self, zoom_factor=0.3, zoomed_display_height=1, zoomed_display_width=6,
            image_frame_stroke_width=20, zoomed_camera_config={"default_frame_stroke_width": 3}, **kwargs
        )

    def construct(self):
        dot = Dot().shift(UL * 2)
        # simple image that will just appear as some grayscale gradients
        image = ImageMobject(np.uint8([[0, 100, 30, 200], [255, 0, 5, 33]]))
        image.height = 7
        frame_text = Text("Frame", color=PURPLE, font_size=67)
        zoomed_camera_text = Text("Zoomed Camera", color=RED, font_size=67)

        self.add(image, dot)
        zoomed_camera, zoomed_display = self.zoomed_camera, self.zoomed_display
        frame, zoomed_display_frame = zoomed_camera.frame, zoomed_display.display_frame

        frame.move_to(dot)
        frame.set_color(PURPLE)
        zoomed_display_frame.set_color(RED)
        zoomed_display.shift(DOWN)

        frame_text.next_to(frame, DOWN)

        # adding a rectangle to show zoomed-in area (border but no fill)
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)
        self.add_foreground_mobject(zd_rect)

        # continuously update this rectangle with the zoomed display area
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))

        self.play(Create(frame), FadeIn(frame_text, shift=UP))
        self.activate_zooming()

        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)

        # reshape zoomed in area
        scale_factor = [0.5, 1.5, 0]  # x y z
        self.play(
            frame.animate.scale(scale_factor),
            zoomed_display.animate.scale(scale_factor),
            FadeOut(zoomed_camera_text),
            FadeOut(frame_text)
        )

        self.wait()
        self.play(ScaleInPlace(zoomed_display, 2))
        self.wait()
        self.play(frame.animate.shift(2.5 * DOWN))
        self.wait()

        # move the zoomed display back to the source area and animate its disappearance
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera, rate_func=lambda t: smooth(1 - t))
        self.play(Uncreate(zoomed_display_frame), FadeOut(frame))
        self.wait()
