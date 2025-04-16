from manim import *


class MovingFrameBox(Scene):
    def construct(self):
        text = MathTex(
            r"\frac{d}{dx} f(x)g(x)=", r"f(x) \frac{d}{dx} g(x)", "+",
            r"g(x) \frac{d}{dx} f(x)"
        )
        self.play(Write(text))  # the classic text rendering animation

        framebox1 = SurroundingRectangle(text[1], buff=0.1)  # indexing into the Tex sequence we wrote
        framebox2 = SurroundingRectangle(text[3], buff=0.1)
        self.play(Create(framebox1))
        self.wait()

        self.play(ReplacementTransform(framebox1, framebox2))
        self.wait()
