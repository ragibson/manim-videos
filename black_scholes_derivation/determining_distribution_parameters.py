from manim import *


class DeterminingDistributionParameters(Scene):
    def calculate_lognormal_pdf(self):
        exercise_label = Text("Exercise #3:", color=YELLOW, font_size=36).to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0)
        exercise_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"Determine the probability density function \\"
            r"of $X \sim \exp\left(N(\mu,\sigma^2)\right)$"
            r"\end{flushleft}",
            font_size=46  # approximately the equivalent of text font size 36
        ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text))
        self.wait(1.0)

        remember_label = (Text("Remember:", font_size=36).next_to(exercise_text, DOWN, buff=1.0)
                          .align_to(exercise_label, RIGHT))
        remember_text = Tex(
            r"$f_{N(\mu,\sigma^2)}(x) = \dfrac{1}{\sigma \cdot \sqrt{2\pi}}"
            r"\exp\left(-\dfrac{\left(x-\mu\right)^2}{2\sigma^2}\right)$",
            font_size=46
        ).next_to(remember_label, RIGHT, buff=0.25).align_to(remember_label, UP + DOWN)
        self.play(Write(remember_label))
        self.play(Write(remember_text))
        self.wait(1.0)

        self.play(FadeOut(remember_label), FadeOut(remember_text))
        self.wait(1.0)

        # TODO: continue with answer

    def construct(self):
        self.calculate_lognormal_pdf()
