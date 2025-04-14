from manim import *


class GradientImageFromArray(Scene):
    def construct(self):
        n = 256
        image_array = np.uint8([  # okay, manim seems to import numpy for us
            [i * 256 / n for i in range(n)]
            for _ in range(n)
        ])

        # allegedly defaulting to RGBA but seems to infer grayscale here
        # putting tuples in the image array does indeed display in color
        image = ImageMobject(image_array).scale(2)
        image.background_rectangle = SurroundingRectangle(image, color=GREEN)

        self.add(image, image.background_rectangle)
