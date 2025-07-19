from manim import *
from scipy.optimize import bisect

from how_to_simulate import create_normal_lognormal_comparison
from shared_data_and_functions import *


class DeterminingDistributionParameters(Scene):
    def calculate_lognormal_pdf(self):
        exercise_label = (Text("Exercise #3:", color=YELLOW, font_size=TEXT_SIZE_MEDIUM)
                          .to_edge(UP, buff=0.5).to_edge(LEFT, buff=1.0))
        exercise_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"Determine the probability density function \\"
            r"of $X \sim \exp\left(N(\mu,\sigma^2)\right)$"
            r"\end{flushleft}",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text))
        self.wait(1.0)

        remember_label = (Text("Remember:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=1.0)
                          .align_to(exercise_label, RIGHT))
        remember_text = Tex(
            r"$f_{N(\mu,\sigma^2)}(x) = \dfrac{1}{\sigma \cdot \sqrt{2\pi}}"
            r"\exp\left(-\dfrac{\left(x-\mu\right)^2}{2\sigma^2}\right)$",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(remember_label, RIGHT, buff=0.25).align_to(remember_label, UP + DOWN)
        self.play(Write(remember_label))
        self.play(Write(remember_text))
        self.wait(1.0)

        self.play(FadeOut(remember_label), FadeOut(remember_text))
        self.wait(1.0)

        answer_start = (Tex(r"Let $Y \sim N\left(\mu, \sigma^2\right)$, $X \sim \exp(Y)$", font_size=MATH_SIZE_MEDIUM)
                        .next_to(exercise_text, DOWN, buff=0.5)).to_edge(LEFT, buff=1.0)
        # TODO: not sure I really like the layout of this
        answer_body_left = MathTex(
            r"f_X(x) &= \frac{\text{d}}{\text{d}x} \mathbb{P}\left[X \leq x\right]",
            r"= \frac{\text{d}}{\text{d}x}\mathbb{P}\left[Y \leq \ln x\right]",
            r"= \frac{\text{d}}{\text{d}x}F_Y(\ln x)\\",
            r"&= f_Y(\ln x) \cdot \frac{1}{x}\\",
            r"&= \frac{1}{x\sigma\cdot\sqrt{2\pi}} \exp\left(-\frac{\left(\ln x - \mu\right)^2}{2\sigma^2}\right)",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(answer_start, DOWN, buff=0.5).align_to(answer_start, LEFT)
        self.play(Write(answer_start))
        self.wait(1.0)
        for line in list(answer_body_left):
            self.play(Write(line))
            self.wait(1.0)  # TODO: may need to be specific to each line

        self.play(*[FadeOut(x) for x in (exercise_label, exercise_text, answer_start, answer_body_left)])

    def consider_S1(self):
        # TODO: text header for this section?
        math_header = MathTex(r"{S(t ) \over S(0)} \sim \exp\left(N(\mu, \sigma^2)\right)",
                              substrings_to_isolate=["t ", r"\mu", r"\sigma^2"],
                              font_size=MATH_SIZE_MEDIUM).to_edge(UP, buff=0.5)
        t = math_header[1]
        one = MathTex("1", font_size=MATH_SIZE_MEDIUM, color=BLUE).move_to(t.get_center())

        self.play(Write(math_header))
        self.wait(1.0)

        mu_substring, sigma_substring = math_header[3], math_header[5]
        self.play(Circumscribe(mu_substring), Circumscribe(sigma_substring))
        self.wait(1.0)

        self.play(ReplacementTransform(t, one))
        self.wait(1.0)

        self.play(Indicate(mu_substring), mu_substring.animate.set_color(YELLOW))
        self.wait(1.0)

        # show the normal vs. lognormal transformation from earlier
        ax = Axes(
            x_range=[-10, 60.1, 10],
            y_range=[0.0, 0.05, 0.01],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).next_to(math_header, DOWN, buff=1.0).align_to(ORIGIN, LEFT + RIGHT)

        (labels, price_distribution, specific_norm_pdf, normal_dist_original, specific_lognorm_pdf, lognormal_dist,
         left_arrow, left_text, right_arrow, right_text) = create_normal_lognormal_comparison(ax)
        self.play(*[FadeIn(x) for x in (ax, labels, price_distribution)])  # original normal distribution
        self.wait(1.0)

        # transform to lognormal with original normal distribution in grey
        self.add(normal_dist_original)
        self.play(ReplacementTransform(price_distribution, lognormal_dist),
                  Transform(labels[1], Tex(r"\text{Lognormal Distribution Density}", font_size=TEXT_SIZE_MEDIUM)
                            .move_to(labels[1], aligned_edge=LEFT)), run_time=2.0)
        self.wait(2.0)

        # highlight the areas where the PDF has changed drastically
        # there's a small hack here that we use get_area() on graphs we don't actually plot because that function
        # doesn't actually work on the output from the plot_line_graph() function we were using earlier
        left_pdf_intersection = bisect(lambda x: (specific_norm_pdf(x) - specific_lognorm_pdf(x)), 0, 15, xtol=1e-8)
        right_pdf_intersection = bisect(lambda x: (specific_norm_pdf(x) - specific_lognorm_pdf(x)), 30, 50, xtol=1e-8)
        lognorm_graph = ax.plot(specific_lognorm_pdf, x_range=ax.x_range[:2])
        norm_graph = ax.plot(specific_norm_pdf, x_range=ax.x_range[:2])
        left_area = ax.get_area(lognorm_graph, x_range=(ax.x_range[0], left_pdf_intersection),
                                bounded_graph=norm_graph, color=YELLOW)
        right_area = ax.get_area(lognorm_graph, x_range=(right_pdf_intersection, ax.x_range[1]),
                                 bounded_graph=norm_graph, color=YELLOW)

        # actually render out the bounded areas
        # TODO: better way to display this area? sweeping left-to-right?
        self.play(DrawBorderThenFill(left_area), rate_func=linear)
        self.wait(1.0)
        self.play(FadeOut(left_area))
        self.wait(1.0)
        self.play(DrawBorderThenFill(right_area), rate_func=linear)
        self.wait(1.0)
        self.play(FadeOut(right_area))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (ax, labels, price_distribution, normal_dist_original, lognormal_dist)])
        self.wait(1.0)

    def construct(self):
        self.calculate_lognormal_pdf()

        self.consider_S1()
