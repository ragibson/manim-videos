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

        answer_start = (Tex(r"Let $Y \sim N\left(\mu, \sigma^2\right)$, $X \sim \exp(Y)$", font_size=46)
                        .next_to(exercise_text, DOWN, buff=0.5)).to_edge(LEFT, buff=1.0)
        # TODO: not sure I really like the layout of this
        answer_body_left = MathTex(
            r"f_X(x) &= \frac{\text{d}}{\text{d}x} \mathbb{P}\left[X \leq x\right]",
            r"= \frac{\text{d}}{\text{d}x}\mathbb{P}\left[Y \leq \ln x\right]",
            r"= \frac{\text{d}}{\text{d}x}F_Y(\ln x)\\",
            r"&= f_Y(\ln x) \cdot \frac{1}{x}\\",
            r"&= \frac{1}{x\sigma\cdot\sqrt{2\pi}} \exp\left(-\frac{\left(\ln x - \mu\right)^2}{2\sigma^2}\right)",
            font_size=46
        ).next_to(answer_start, DOWN, buff=0.5).align_to(answer_start, LEFT)
        self.play(Write(answer_start))
        self.wait(1.0)
        for line in list(answer_body_left):
            self.play(Write(line))
            self.wait(1.0)  # TODO: may need to be specific to each line

        self.play(*[FadeOut(x) for x in (exercise_label, exercise_text, answer_start, answer_body_left)])

    def consider_S1(self):
        pass

    def construct(self):
        self.calculate_lognormal_pdf()
