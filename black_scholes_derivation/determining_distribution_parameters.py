from scipy.optimize import bisect

from how_to_simulate import create_normal_lognormal_comparison
from shared_data_and_functions import *


class DeterminingDistributionMu(Scene):
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
        self.play(Write(exercise_text), run_time=3.0)
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
        answer_body = MathTex(
            r"f_X(x) &= \frac{\text{d}}{\text{d}x} \mathbb{P}\left[X \leq x\right]",
            r"= \frac{\text{d}}{\text{d}x}\mathbb{P}\left[Y \leq \ln x\right]",
            r"= \frac{\text{d}}{\text{d}x}F_Y(\ln x)\\",
            r"&= f_Y(\ln x) \cdot \frac{1}{x}\\",
            r"&= \frac{1}{x\sigma\cdot\sqrt{2\pi}} \exp\left(-\frac{\left(\ln x - \mu\right)^2}{2\sigma^2}\right)",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(answer_start, DOWN, buff=0.5).align_to(answer_start, LEFT)
        self.play(Write(answer_start))
        self.wait(1.0)
        for line in list(answer_body):
            self.play(Write(line))
            self.wait(1.0)  # TODO: may need to be specific to each line

        self.play(*[FadeOut(x) for x in (exercise_label, exercise_text, answer_start, answer_body)])

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

        # actually render out the bounded areas, fading in/out like before
        # decided not to use DrawBorderThenFill() since it wasn't akin to the sweep I originally thought of
        self.play(FadeIn(left_area), rate_func=linear)
        self.wait(1.0)
        self.play(FadeOut(left_area))
        self.wait(1.0)
        self.play(FadeIn(right_area), rate_func=linear)
        self.wait(1.0)
        self.play(FadeOut(right_area))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (ax, labels, price_distribution, normal_dist_original, lognormal_dist)])
        self.wait(1.0)
        return math_header

    def exercise_mu(self, S1_header):
        exercise_label = (Text("Exercise #4:", color=YELLOW, font_size=TEXT_SIZE_MEDIUM)
                          .next_to(S1_header, DOWN, buff=0.5).to_edge(LEFT, buff=1.0))
        exercise_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"Given $\sigma$, find the value of $\mu$ that keeps the stock \\"
            r"price flat, on average. That is, $\mathbb{E}\left[S(1)\right] = S(0)$."
            r"\end{flushleft}",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text), run_time=3.0)
        self.wait(1.0)

        # placeholder for hint, viewers can do the exercise without it by pausing
        hint1_label = (Text("Hint #1:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=0.5)
                       .align_to(exercise_label, RIGHT))
        hint1_countdown = (Text("(revealed in 5 seconds)", font_size=TEXT_SIZE_MEDIUM)
                           .next_to(hint1_label, RIGHT, buff=0.25).align_to(hint1_label, UP))
        hint2_label = (Text("Hint #2:", font_size=TEXT_SIZE_MEDIUM).next_to(hint1_label, DOWN, buff=0.5)
                       .align_to(exercise_label, RIGHT))
        hint2_countdown = (Text("(revealed in 10 seconds)", font_size=TEXT_SIZE_MEDIUM)
                           .next_to(hint2_label, RIGHT, buff=0.25).align_to(hint2_label, UP))
        self.play(Write(hint1_label), Write(hint2_label))
        self.play(Write(hint1_countdown), Write(hint2_countdown))
        self.wait(5.0)

        hint1_text = (Tex(r"What happens if $\mu = 0$?", font_size=MATH_SIZE_MEDIUM)
                      .next_to(hint1_label, RIGHT, buff=0.25).align_to(hint1_label, UP))
        self.play(FadeOut(hint1_countdown))
        self.play(Write(hint1_text))
        self.wait(5.0)

        hint2_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"The integral for $\mathbb{E}\left[S(1)\right]$ can be transformed so \\"
            r"that you're integrating a normal PDF. Then, \\"
            r"no integration calculations are needed."
            r"\end{flushleft}",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(hint1_label, RIGHT, buff=0.25).align_to(hint2_label, UP)
        self.play(FadeOut(hint2_countdown))
        self.play(Write(hint2_text), run_time=3.0)
        self.wait(5.0)

        # proceeding onto answer
        self.play(FadeOut(hint1_label), FadeOut(hint1_text), FadeOut(hint2_label), FadeOut(hint2_text))
        return exercise_label, exercise_text

    def exercise_mu_answer(self, S1_header, exercise_label, exercise_text):
        self.wait(1.0)

        answer_start = (Tex(r"Take $\mu = 0$. Then,", font_size=MATH_SIZE_MEDIUM)
                        .next_to(exercise_text, DOWN, buff=0.5)).to_edge(LEFT, buff=1.0)
        answer_body = MathTex(
            r"\mathbb{E}\left[S(1)\right] &= \mathbb{E}\left[S(0) \cdot "
            r"\exp\left(N\left(0, \sigma^2\right)\right)\right] \\",
            r"&= S(0) \cdot \mathbb{E}\left[\exp\left(N\left(0, \sigma^2\right)\right)\right] \\",
            r"&= S(0) \cdot \exp\left(\frac{\sigma^2}{2}\right)",  # won't be displayed until after the derivation
            font_size=MATH_SIZE_MEDIUM
        ).next_to(answer_start, DOWN, buff=0.5).align_to(answer_start, LEFT)

        self.play(Write(answer_start))
        self.wait(1.0)
        for line in list(answer_body[:-1]):
            self.play(Write(line))
            self.wait(1.0)

        distribution_expectation = answer_body[1][6:]  # everything after S(0) \cdot
        self.play(Indicate(distribution_expectation, scale_factor=1.1))

        # fading everything out for more space
        self.play(*[FadeOut(x) for x in (S1_header, exercise_label, exercise_text, answer_start, answer_body[:-1])])

        # focusing on the expectation of zero-mu lognormal
        expectation_body = MathTex(
            r"\mathbb{E}\left[\exp\left(N\left(0, \sigma^2\right)\right)\right] &= "
            r"\int_0^{\infty} x \cdot f_{\exp\left(N\left(0, \sigma^2\right)\right)}(x) \text{ d}x \\",
            r"&= \int_0^{\infty} x \cdot \frac{1}{x} \cdot \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(\ln x\right)^2}{2\sigma^2}\right) \text{ d}x \\",
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{u^2}{2\sigma^2}\right) \cdot \exp(u) \text{ d}u\\",
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{u^2}{2\sigma^2} + u\right) \text{ d}u",
            font_size=MATH_SIZE_SMALL
        ).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
        for line in expectation_body[:2]:
            self.play(Write(line))
            self.wait(1.0)

        line2_replacement = MathTex(
            r"&= \int_0^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(\ln x\right)^2}{2\sigma^2}\right) \text{ d}x",
            font_size=MATH_SIZE_SMALL
        ).move_to(expectation_body[1].get_left(), LEFT)
        self.play(FadeOut(expectation_body[1], shift=LEFT), FadeIn(line2_replacement, shift=LEFT))
        self.wait(1.0)

        # note about choice of u-substitution
        u_substitution = MathTex(
            r"\text{Let } u &= \ln x, \text{ so } \exp(u) = x\\",
            r"\text{d}u &= \frac{1}{x} \text{ d}x\\",
            r"\exp(u) \text{ d}u &= \text{d}x",
            font_size=MATH_SIZE_SMALL, color=BLUE_B
        ).next_to(expectation_body[1], DOWN, buff=2.0).shift(LEFT * 2.0)
        for line in u_substitution:
            self.play(Write(line))
            self.wait(1.0)

        # continuing on with main body with the u-substitution
        self.play(Write(expectation_body[2]))
        self.wait(1.0)
        self.play(Indicate(expectation_body[2][3:5], scale_factor=1.1))  # change of lower bound: 0 -> {-\infty}
        self.wait(1.0)
        self.play(FadeOut(u_substitution))
        self.wait(1.0)

        # next line with (-u^2/2\sigma^2 + u) in the exp() expression
        self.play(Write(expectation_body[3]))
        self.wait(1.0)

        normal_goal = MathTex(
            r"\text{We want this integrand to look like } \exp\left(-\frac{\left(u-\mu\right)^2}{2\sigma^2}\right)",
            font_size=MATH_SIZE_SMALL, color=BLUE_B
        ).next_to(expectation_body[2], DOWN, buff=2.0).shift(LEFT * 2.0)
        self.play(Write(normal_goal))
        self.wait(1.0)

        # fade out everything and shift our current line of the derivation up to the top so we have more space
        self.play(expectation_body[3].animate.align_to(expectation_body[0].get_top() + UP * 0.025, UP),
                  normal_goal.animate.shift(UP * 1.0),
                  *[FadeOut(x) for x in (
                      expectation_body[0][15:],  # first line beyond equal sign
                      line2_replacement,  # probably should've had expectation_body[1] become() this?
                      expectation_body[2]
                  )])

        # going to replace the shifted line with a new object that's easier to work with
        new_expectation_body = MathTex(
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{u^2}{2\sigma^2} + u\right) \text{ d}u \\",
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{u^2 - 2\sigma^2 \cdot u}{2\sigma^2}\right) \text{ d}u\\",
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(u - \sigma^2\right)^2}{2\sigma^2} + \frac{\sigma^4}{2\sigma^2}\right) \text{ d}u"
            r"\\",
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(u - \sigma^2\right)^2}{2\sigma^2}\right) \cdot \exp\left(\frac{\sigma^2}{2}\right) "
            r"\text{ d}u \\",
            r"&= \exp\left(\frac{\sigma^2}{2}\right) \cdot \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(u - \sigma^2\right)^2}{2\sigma^2}\right) \text{ d}u",
            font_size=MATH_SIZE_SMALL
        ).move_to(expectation_body[3].get_left(), LEFT).align_to(expectation_body[3], UP)
        self.remove(expectation_body[3])
        self.add(new_expectation_body[0])
        self.wait(1.0)

        self.play(Write(new_expectation_body[1]))
        self.wait(1.0)

        completing_the_square = MathTex(
            r"\left(u - \mu\right)^2 = u^2 - 2\mu \cdot u + \mu^2",
            font_size=MATH_SIZE_SMALL, color=BLUE_B
        ).next_to(normal_goal, DOWN, buff=0.25)
        self.play(Write(completing_the_square))
        self.wait(1.0)

        self.play(Write(new_expectation_body[2]))
        self.wait(1.0)

        self.play(FadeOut(normal_goal), FadeOut(completing_the_square))
        self.wait(1.0)

        line3_replacement = MathTex(
            r"&= \int_{-\infty}^{\infty} \frac{1}{\sigma\cdot\sqrt{2\pi}} "
            r"\exp\left(-\frac{\left(u - \sigma^2\right)^2}{2\sigma^2} + \frac{\sigma^2}{2}\right) \text{ d}u",
            font_size=MATH_SIZE_SMALL
        ).move_to(new_expectation_body[2].get_left(), LEFT)
        self.play(FadeOut(new_expectation_body[2], shift=LEFT), FadeIn(line3_replacement, shift=LEFT))
        self.wait(1.0)

        self.play(Write(new_expectation_body[3]))
        self.wait(1.0)
        self.play(Write(new_expectation_body[4]))
        self.wait(1.0)

        self.play(FadeOut(new_expectation_body[4][10:]))  # the whole integral is just 1
        self.wait(1.0)

        self.play(FadeIn(S1_header), FadeIn(answer_body[:-1]), FadeIn(exercise_label), FadeIn(exercise_text),
                  *[FadeOut(x) for x in
                    (expectation_body[0][:15],  # first line up to the equal sign
                     line3_replacement) + tuple(new_expectation_body[i] for i in (0, 1, 3))
                    + (new_expectation_body[4][:10],)  # last line up to the integral
                    ])
        self.wait(1.0)
        self.play(Write(answer_body[-1]))
        self.wait(1.0)

        new_header = self.final_header()
        new_header.set_color_by_tex(r"1", BLUE)
        self.play(FadeOut(S1_header, shift=LEFT), FadeIn(new_header, shift=LEFT))
        self.wait(1.0)

        # fading out everything except the header
        self.play(*[FadeOut(x) for x in (exercise_label, exercise_text, answer_body)])

    def final_header(self):
        return MathTex(r"{S({{1}} ) \over S(0)} \sim "
                       r"\exp\left(N\left(-\frac{\sigma^2}{2}, {{\sigma}}^2\right)\right)",
                       font_size=MATH_SIZE_MEDIUM).to_edge(UP, buff=0.5)

    def construct(self):
        self.calculate_lognormal_pdf()

        S1_header = self.consider_S1()
        exercise_label, exercise_text = self.exercise_mu(S1_header)
        self.exercise_mu_answer(S1_header, exercise_label, exercise_text)


class DeterminingDistributionSigmaAndSt(Scene):
    def discuss_sigma(self, S1_header):
        self.wait(1.0)
        self.play(S1_header[-2].animate.set_color(YELLOW))  # highlighting sigma
        self.wait(1.0)

        ax, labels, simulated_path, past_graph, _ = stock_price_to_today(S1_header, sigma=0.2)
        self.play(Create(ax), Write(labels), run_time=2.0)
        self.play(Create(past_graph, rate_func=linear, run_time=2.0))
        self.wait(1.0)

        def create_future_graph_and_text(sigma):
            graph = ax.plot_line_graph(
                x_values=np.linspace(0.5, 1.0, len(simulated_path)),
                y_values=simple_stock_simulation(start_price=simulated_path[-1], sigma=sigma, seed=1, T=0.5),
                line_color=GREEN,
                add_vertex_dots=False
            )
            text = MathTex(rf"\sigma = {future_sigma.get_value() * 100:.1f}\%", font_size=MATH_SIZE_MEDIUM)
            return graph, text.move_to(ax.get_center() + UP * 2.0 + RIGHT * 2.0)

        future_sigma = ValueTracker(0.1)
        sigma_text, future_graph = create_future_graph_and_text(future_sigma.get_value())
        self.play(FadeIn(sigma_text), Create(future_graph, rate_func=linear), run_time=1.0)
        self.wait(1.0)

        future_graph.add_updater(
            lambda g: g.become(create_future_graph_and_text(future_sigma.get_value())[0])
        )
        sigma_text.add_updater(
            lambda t: t.become(create_future_graph_and_text(future_sigma.get_value())[1])
        )
        self.play(future_sigma.animate.set_value(0.3), run_time=2.0)
        self.wait(1.0)
        self.play(future_sigma.animate.set_value(0.2), run_time=2.0)
        self.wait(1.0)

        # forcing text mode to avoid automatically inserted newlines
        footnote = Tex(r"$^*$\text{This really tells us how volatile the stock \emph{used to be}. In practice, you'd "
                       r"use slightly more complicated techniques to estimate \emph{future} volatility.}",
                       font_size=TEXT_SIZE_TINY).scale(0.9)
        footnote.to_edge(DOWN, buff=0.25).to_edge(LEFT, buff=0.25)
        self.play(FadeIn(footnote))
        self.wait(1.0)

        future_graph.clear_updaters()
        sigma_text.clear_updaters()
        self.play(*[FadeOut(x) for x in (ax, labels, past_graph, sigma_text, future_graph, S1_header, footnote)])

    def discuss_St(self):
        header_text = Tex(r"What does $S(t)$ look like?", font_size=MATH_SIZE_MEDIUM).to_edge(UP, buff=0.25)
        self.play(Write(header_text))
        self.wait(1.0)

        math_lines = MathTex(
            r"S(1) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2}, \sigma^2\right)\right) \\\\",
            r"S(2) &\sim S(1) \cdot \exp\left(N\left(-\frac{\sigma^2}{2}, \sigma^2\right)\right) \\",
            r"S(2) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2}, \sigma^2\right)\right) "
            r"\cdot \exp\left(N\left(-\frac{\sigma^2}{2}, \sigma^2\right)\right) \\",
            r"S(2) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2}, \sigma^2\right) "
            r"+ N\left(-\frac{\sigma^2}{2}, \sigma^2\right)\right) \\",
            r"S(2) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2} \cdot 2, "
            r"\sigma^2 \cdot 2\right)\right)",
            font_size=MATH_SIZE_SMALL
        ).next_to(header_text, DOWN, buff=0.25)

        for line in math_lines:
            self.play(Write(line))
            self.wait(1.0)

        self.play(*[FadeOut(x) for x in math_lines[:-1]], math_lines[-1].animate.move_to(ORIGIN))
        self.wait(1.0)

        # convert all the t=2 to t=3 and then t
        for new_tex in ["3", "t"]:
            self.play(*[Transform(x, MathTex(new_tex, font_size=MATH_SIZE_SMALL).move_to(x))
                        # gross hack but keeps easy line boundaries in MathTex above
                        for x in [math_lines[-1][i] for i in (2, 22, 27)]])
            self.wait(1.0)

        self.play(*[FadeOut(x) for x in (header_text, math_lines[-1])])

    def construct(self):
        S1_header = DeterminingDistributionMu().final_header()
        self.add(S1_header)
        self.discuss_sigma(S1_header)
        self.discuss_St()
