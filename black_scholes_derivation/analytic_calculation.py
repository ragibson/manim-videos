from scipy.stats import lognorm

from shared_data_and_functions import *


class AnalyticCalculation(Scene):
    def plot_distribution(self):
        # left: simulated stock prices from before
        stock_S0, stock_sigma, T = 300, 0.1, 0.25
        strike = 320
        stock_range = (260, 350.1, 20)
        ax, labels, strike_line_left = stock_price_simulation_graph(stock_price_range=stock_range, strike=strike,
                                                                    shift_amt=DOWN * 0.25)

        self.play(Create(ax, run_time=2.0), Write(labels, run_time=2.0))
        self.wait(1.0)

        simulation_paths = [simple_stock_simulation(start_price=stock_S0, sigma=stock_sigma, T=T, seed=i)
                            for i in range(100, 200)]
        simulation_graphs = [
            ax.plot_line_graph(
                x_values=np.linspace(0, T, len(simulated_path)),
                y_values=simulated_path,
                line_color=BLUE,
                add_vertex_dots=False
            ).set_stroke(opacity=0.2) for simulated_path in simulation_paths
        ]
        self.play(*[Create(p, rate_func=linear) for p in simulation_graphs], run_time=2.0)
        self.wait(1.0)

        distribution_form = MathTex(
            r"S(t) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2} \cdot t, "
            r"\sigma^2 \cdot t\right)\right)",
            font_size=MATH_SIZE_MEDIUM
        ).to_edge(UP, buff=0.25)
        self.play(Write(distribution_form))

        # right: plot distribution directly
        density_range = (0.0, 0.03, 0.01)
        distribution_ax = Axes(
            x_range=stock_range,
            y_range=density_range,
            x_length=4,
            y_length=4,
            y_axis_config={"include_numbers": True},
            axis_config={"include_numbers": False},
            tips=False
        ).to_edge(RIGHT, buff=1.0).shift(DOWN * 0.25)

        # HACK: manually adding in dollar signs on the left of the x-axis label numbers
        distribution_ax.x_axis.add_labels({i: Tex(fr"\${i:.0f}", font_size=TEXT_SIZE_XSMALL)
                                           for i in np.arange(*ax.y_range)})
        distribution_labels = distribution_ax.get_axis_labels(
            x_label=Tex(r"\text{Stock Price}", font_size=TEXT_SIZE_XSMALL),
            y_label=Tex(r"\text{Distribution Density}", font_size=TEXT_SIZE_XSMALL)
        )
        distribution_labels[0] = distribution_labels[0].shift(RIGHT * 0.2)
        self.play(Create(distribution_ax, run_time=2.0), Write(distribution_labels, run_time=2.0))
        self.wait(1.0)

        lognorm_sigma = stock_sigma * np.sqrt(T)
        lognorm_mu = -stock_sigma ** 2 / 2 * T
        lognormal_pdf = lambda xs: lognorm.pdf(xs / stock_S0, loc=lognorm_mu, s=lognorm_sigma) / stock_S0
        distribution_graph = distribution_ax.plot(
            lognormal_pdf, x_range=stock_range[:2], color=BLUE
        )
        self.play(Create(distribution_graph, rate_func=linear), run_time=2.0)
        self.wait(1.0)

        strike_line_right = DashedLine(distribution_ax.c2p(strike, 0.0), distribution_ax.c2p(strike, density_range[1]))
        self.play(Create(strike_line_left, rate_func=linear), Create(strike_line_right, rate_func=linear), run_time=1.0)
        self.wait(1.0)

        profit_path_indices = [i for i, p in enumerate(simulation_paths) if p[-1] >= strike]
        right_pdf_area = distribution_ax.get_area(distribution_graph, x_range=(strike, stock_range[1]), color=GREEN,
                                                  opacity=0.5)
        self.play(
            *[simulation_graphs[i].animate.set_stroke(opacity=0.75, color=GREEN) for i in profit_path_indices],
            FadeIn(right_pdf_area), run_time=1.0
        )
        self.wait(1.0)

        analytical_note = Text(r"Calculate it all analytically!",
                               font_size=TEXT_SIZE_MEDIUM, color=YELLOW).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(analytical_note), run_time=1.0)
        self.wait(1.0)

        distribution_group = VGroup(
            distribution_ax, distribution_labels, distribution_graph, strike_line_right, right_pdf_area
        )
        self.play(*[FadeOut(x) for x in [ax, labels, strike_line_left, analytical_note, *simulation_graphs]],
                  distribution_group.animate.to_edge(LEFT, buff=0.5), run_time=1.0)
        return distribution_form, distribution_group

    def display_option_price_formula(self, distribution_group):
        math_lines = MathTex(
            r"{{\widetilde{C} &=}} \mathbb{E}\left[S(t)-K \mid S(t) > K\right]\\",
            r"&= \mathbb{E}\left[S(t) \mid S(t) > K\right] {{- K \cdot \mathbb{P}\left[S(t) > K\right]}}",
            font_size=MATH_SIZE_SMALL
        ).next_to(distribution_group, RIGHT, buff=-1.0).align_to(distribution_group, UP)

        for line in math_lines:
            self.play(Write(line))
            self.wait(1.0)

        self.play(*[FadeOut(x) for x in (distribution_group, math_lines)])

    def calculate_probability_term(self, distribution_header):
        exercise_label = (Text("Exercise #5:", color=YELLOW, font_size=TEXT_SIZE_MEDIUM)
                          .next_to(distribution_header, DOWN, buff=0.3).to_edge(LEFT, buff=1.0))
        exercise_text = Tex(r"Calculate $\mathbb{P}\left[S(t) > K\right]$", font_size=MATH_SIZE_MEDIUM
                            ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text), run_time=1.0)
        self.wait(1.0)

        # placeholder for hint, viewers can do the exercise without it by pausing
        hint_label = (Text("Hint:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=0.5)
                      .align_to(exercise_label, RIGHT))
        hint_countdown = (Text("(revealed in 5 seconds)", font_size=TEXT_SIZE_MEDIUM)
                          .next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP))
        self.play(Write(hint_label))
        self.play(Write(hint_countdown))
        self.wait(5.0)

        hint_text = Tex(r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
                        r"Transform $S(t)$ so that you can use \\"
                        r"the standard normal CDF."
                        r"\end{flushleft}",
                        font_size=MATH_SIZE_MEDIUM).next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP)
        self.play(FadeOut(hint_countdown))
        self.play(Write(hint_text))
        self.wait(3.0)

        self.play(FadeOut(hint_label), FadeOut(hint_text))

        answer_body = MathTex(
            r"\mathbb{P}\left[S(t) > K\right] &= \mathbb{P}\left[\ln\left(\frac{S(t)}{S(0)}\right) "
            r"> \ln\left(\frac{K}{S(0)}\right)\right] \\",
            r"&= \mathbb{P}\left[N\left(-\frac{\sigma^2}{2} \cdot t, "
            r"\sigma^2 \cdot t\right) > \ln\left(\frac{K}{S(0)}\right)\right] \\",
            r"&= \mathbb{P}\left[N\left(0, "
            r"\sigma^2 \cdot t\right) > \ln\left(\frac{K}{S(0)}\right) + \frac{\sigma^2}{2} \cdot t\right] \\",
            r"&= \mathbb{P}\left[N\left(0, 1\right) > "
            r"\frac{\ln\left(\frac{K}{S(0)}\right) + \frac{\sigma^2}{2} \cdot t}{\sigma \cdot \sqrt{t}}\right] \\",
            r"&= 1-\Phi\left(\frac{\ln\left(\frac{K}{S(0)}\right) + "
            r"\frac{\sigma^2}{2} \cdot t}{\sigma \cdot \sqrt{t}}\right)",
            font_size=MATH_SIZE_SMALL
        ).next_to(exercise_text, DOWN, buff=0.3).to_edge(LEFT, buff=1.0)

        for line in answer_body[:-1]:
            self.play(Write(line))
            self.wait(1.0)

        self.play(*[FadeOut(x) for x in (answer_body[0][9:], answer_body[1:-2])],
                  answer_body[0][:9].animate.shift(DOWN * 0.5),
                  # manual alignment of equal sign
                  answer_body[-2].animate.shift(UP * 3.525))
        answer_body[-1].shift(UP * 3.525)
        self.wait(1.0)

        self.play(Write(answer_body[-1]))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (exercise_label, exercise_text, answer_body[0][:9], answer_body[-2:])])

    def calculate_expectation_term(self, distribution_header):
        exercise_label = (Text("Exercise #6:", color=YELLOW, font_size=TEXT_SIZE_MEDIUM)
                          .next_to(distribution_header, DOWN, buff=0.3).to_edge(LEFT, buff=0.5))
        exercise_text = Tex(r"Calculate $\mathbb{E}\left[S(t) \mid S(t) > K\right]$", font_size=MATH_SIZE_MEDIUM
                            ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text), run_time=1.0)
        self.wait(1.0)

        # placeholder for hint, viewers can do the exercise without it by pausing
        hint_label = (Text("Hint:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=0.5)
                      .align_to(exercise_label, RIGHT))
        hint_countdown = (Text("(revealed in 5 seconds)", font_size=TEXT_SIZE_MEDIUM)
                          .next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP))
        self.play(Write(hint_label))
        self.play(Write(hint_countdown))
        self.wait(5.0)

        hint_text = Text(r"This is very similar to Exercise #4",
                         font_size=TEXT_SIZE_MEDIUM).next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP)
        self.play(FadeOut(hint_countdown))
        self.play(Write(hint_text))
        self.wait(3.0)

        self.play(FadeOut(hint_label), FadeOut(hint_text))

        answer_start = (Tex(r"Note that $S(t) \sim \exp\left(N\left(\ln S(0) - \frac{\sigma^2}{2} \cdot t, "
                            r"\sigma^2 \cdot t\right)\right)$. Then,", font_size=MATH_SIZE_MEDIUM)
                        .next_to(exercise_text, DOWN, buff=0.5)).to_edge(LEFT, buff=0.5)
        self.play(Write(answer_start))
        self.wait(1.0)

        answer_body = MathTex(
            r"&\mathbb{E}\left[S(t) \mid S(t) > K\right]\\",
            r"&= \int_K^{\infty} x \cdot f_{\exp\left[N\left(\ln S(0)-\frac{\sigma^2}{2} \cdot t, "
            r"\sigma^2\cdot t\right)\right]}(x) \text{ d}x \\",
            r"&= \int_K^{\infty} \frac{1}{\sigma\sqrt{t}\cdot\sqrt{2\pi}} \exp\left(-\frac{\left(\ln(x) "
            r"- \ln S(0) + \frac{\sigma^2}{2}\cdot t\right)^2}{2\sigma^2\cdot t}\right)\text{ d}x",
            font_size=MATH_SIZE_SMALL
        ).next_to(answer_start, DOWN, buff=0.5).align_to(answer_start, LEFT).shift(RIGHT * 1.0)

        for line in answer_body:
            self.play(Write(line))
            self.wait(1.0)

        # moving up last line to replace the first equality, fading out everything else
        self.play(*[FadeOut(x) for x in (answer_start, exercise_label, exercise_text,
                                         distribution_header, answer_body[1])],
                  answer_body[0].animate.to_edge(UP, buff=0.5), answer_body[2].animate.to_edge(UP, buff=1.0))
        self.wait(1.0)

        # substituting to get as close to a standard normal as possible, doing two columns here due to space constraints
        u_substitution = MathTex(
            r"\text{Let } u &= \frac{\ln x - \ln S(0) + \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}&",
            r"\text{ so } \text{d}u &= \frac{1}{x \cdot \sigma \sqrt{t}} \text{ d}x\\",
            r"x &= S(0)\cdot\exp\left(u \cdot \sigma\sqrt{t} - \frac{\sigma^2}{2}\cdot t\right)&",
            r"x \cdot \sigma\sqrt{t} \text{ d}u &= \text{d}x",
            font_size=MATH_SIZE_SMALL, color=BLUE_B
        ).next_to(answer_body[2], DOWN, buff=2.0).to_edge(LEFT, buff=0.5)
        for line in (u_substitution[idx] for idx in (0, 1, 3, 2)):
            self.play(Write(line))
            self.wait(1.0)

        combined_dx = MathTex(
            r"S(0) \cdot \sigma\sqrt{t} \cdot \exp\left(u \cdot \sigma\sqrt{t} - \frac{\sigma^2}{2}\cdot t\right) "
            r"\text{d}u = \text{d}x",
            font_size=MATH_SIZE_SMALL, color=BLUE_B
        ).align_to(u_substitution[2], DOWN)
        self.play(FadeOut(u_substitution[2], shift=LEFT), FadeOut(u_substitution[3], shift=LEFT),
                  FadeIn(combined_dx, shift=LEFT))
        self.wait(1.0)

        # continuing with the main calculation
        answer_body_end = MathTex(
            r"&= \int_{\frac{\ln K - \ln S(0) + \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}}^{\infty} "
            r"\frac{S(0)}{\sqrt{2\pi}} \exp\left(-\frac{u^2}{2}"
            r"+ u \cdot \sigma\sqrt{t} - \frac{\sigma^2}{2}\cdot t\right) \text{ d}u\\",
            r"&= S(0) \cdot \int_{\frac{\ln K - \ln S(0) + \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}}^{\infty} "
            r"\frac{1}{\sqrt{2\pi}} \exp\left(-\frac{\left(u-\sigma\sqrt{t}\right)^2}{2}\right) \text{ d}u\\",
            r"&= S(0) \cdot \left[1 - \Phi\left(\frac{\ln K - \ln S(0) + \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}"
            r"- \sigma\sqrt{t}\right)\right]\\",
            r"&= S(0) \cdot \left[1 - \Phi\left(\frac{\ln\left(\frac{K}{S(0)}\right) "
            r"- \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}\right)\right]",
            font_size=MATH_SIZE_SMALL
        ).next_to(answer_body[2], DOWN, buff=0.3).align_to(answer_body[2], LEFT)

        self.play(Write(answer_body_end[0]))
        self.wait(1.0)
        self.play(FadeOut(u_substitution[0]), FadeOut(u_substitution[1]), FadeOut(combined_dx))
        self.wait(1.0)

        for line in answer_body_end[1:-1]:
            self.play(Write(line))
            self.wait(1.0)

        # still need a bit more space
        previous_y = answer_body_end[0].get_y()
        self.play(FadeOut(answer_body[2]),
                  answer_body_end[:-1].animate.to_edge(UP, buff=1.25))

        answer_body_end[-1].shift(UP * (answer_body_end[0].get_y() - previous_y))
        self.play(Write(answer_body_end[-1]))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (answer_body[0], answer_body_end)])

    def combining_together(self):
        math_lines = MathTex(
            r"\widetilde{C} &= \mathbb{E}\left[S(t)-K \mid S(t) > K\right]\\",
            r"&= \mathbb{E}\left[S(t) \mid S(t) > K\right] - K \cdot \mathbb{P}\left[S(t) > K\right]\\",
            r"&= S(0) \cdot \left[1 - \Phi\left(\frac{\ln\left(\frac{K}{S(0)}\right) "
            r"- \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}\right)\right]"
            r"- K \cdot \left[1-\Phi\left(\frac{\ln\left(\frac{K}{S(0)}\right) + "
            r"\frac{\sigma^2}{2} \cdot t}{\sigma \cdot \sqrt{t}}\right)\right]\\",
            r"&= S(0) \cdot \Phi\left(-\frac{\ln\left(\frac{K}{S(0)}\right) "
            r"- \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}\right)"
            r"- K \cdot \Phi\left(-\frac{\ln\left(\frac{K}{S(0)}\right) + "
            r"\frac{\sigma^2}{2} \cdot t}{\sigma \cdot \sqrt{t}}\right)\\",
            r"&= S(0) \cdot \Phi\left(\frac{\ln\left(\frac{S(0)}{K}\right) "
            r"+ \frac{\sigma^2}{2}\cdot t}{\sigma \sqrt{t}}\right)"
            r"- K \cdot \Phi\left(\frac{\ln\left(\frac{S(0)}{K}\right) - "
            r"\frac{\sigma^2}{2} \cdot t}{\sigma \cdot \sqrt{t}}\right)\\",
            r"&= S(0) \cdot \Phi(d_+) - K \cdot \Phi(d_-)",
            font_size=MATH_SIZE_SMALL
        ).scale(0.9).to_edge(UP, buff=0.5).to_edge(LEFT, buff=0.5)
        self.play(FadeIn(math_lines[:2]))

        for line in math_lines[2:]:
            self.play(Write(line))
            self.wait(1.0)

        # moving short version to top and fading out the rest
        self.play(*[FadeOut(x) for x in (math_lines[1:-1], math_lines[0][2:])],
                  math_lines[-1].animate.align_to(math_lines[0], DOWN))

        shorthand = MathTex(
            r"\text{where } d_+ = "
            r"{ \ln\left(S(0) \over ",
            r"K",
            r"\right) + {\sigma^2 \over 2} \cdot t \over \sigma \cdot \sqrt{t} }, "
            r"\hspace{0.5em}"
            r"d_- = d_+ - \sigma \cdot \sqrt{t}", font_size=MATH_SIZE_SMALL
        ).next_to(math_lines[-1], DOWN, buff=0.5).align_to(math_lines[0], LEFT)
        self.play(Write(shorthand))
        self.wait(1.0)

        return VGroup(math_lines[0][:2], math_lines[-1]), shorthand

    def discuss_discounting(self, previous_formula, previous_footer):
        exp_plot = Axes(
            x_range=[0, 10, 2],
            y_range=[1.00, 1.51, 0.1],
            x_length=4,
            y_length=3,
            axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": False},
            tips=False
        ).next_to(previous_footer, DOWN, buff=1.0)

        # HACK: manually adding in dollar signs on the left of the x-axis label numbers
        # including cents this time around
        exp_plot.y_axis.add_labels({i: Tex(fr"\${i:.2f}", font_size=TEXT_SIZE_XSMALL)
                                    for i in np.arange(*exp_plot.y_range)})
        exp_labels = exp_plot.get_axis_labels(x_label=Tex(r"\text{Time (years)}", font_size=MATH_SIZE_MEDIUM),
                                              y_label=Tex(r"\text{Future Value of Money}", font_size=MATH_SIZE_MEDIUM))

        r = 0.04  # generally reasonable risk-free rate over the long-term
        exp_graph = exp_plot.plot_line_graph(
            x_values=np.linspace(*exp_plot.x_range[:2], 1000),
            y_values=np.exp(r * np.linspace(*exp_plot.x_range[:2], 1000)),
            line_color=BLUE, add_vertex_dots=False
        )
        self.play(Create(exp_plot), Write(exp_labels))
        self.play(Create(exp_graph), rate_func=linear, run_time=1.0)
        self.wait(1.0)

        discounting_math = (
            MathTex(
                r"\text{Cash}(t) &= e^{rt} \cdot \text{Cash}(0)\\",
                r"\text{Cash}(0) &= e^{-rt} \cdot \text{Cash}(t)",
                font_size=MATH_SIZE_MEDIUM,
                substrings_to_isolate=[r"\text{Cash}(t)", r"\text{Cash}(0)"]
            ).set_color_by_tex(r"\text{Cash}(t)", BLUE).set_color_by_tex(r"\text{Cash}(0)", YELLOW)
            .next_to(exp_plot, RIGHT, buff=1.0).shift(UP * 1.0)
        )
        for line in (discounting_math[:3], discounting_math[3:]):
            self.play(Write(line))
            self.wait(1.0)

        # rewriting this whole thing to avoid quirks of MatchingTex and nested \overs
        extended_footer = MathTex(
            r"\text{where } d_+ = "
            r"{ \ln\left(S(0) \over ",
            r"K",
            r"\right) + {\sigma^2 \over 2} \cdot t \over \sigma \cdot \sqrt{t} }, "
            r"\hspace{0.5em}"
            r"d_- = d_+ - \sigma \cdot \sqrt{t}, \hspace{0.5em} D = e^{-rt}",
            font_size=MATH_SIZE_SMALL
        ).move_to(previous_footer, LEFT).align_to(previous_footer, DOWN)
        self.play(FadeIn(extended_footer))
        self.remove(previous_footer)

        self.play(*[FadeOut(x) for x in (exp_plot, exp_labels, exp_graph, discounting_math)])

        bullet_points = (
            VGroup(  # some gross latex structure here needed to get the colors to render correctly
                MathTex(r"\text{Need to:}", font_size=MATH_SIZE_MEDIUM),
                MathTex(r"\text{• Convert the }\text{future option price } \widetilde{C} "
                        r"\text{ to }\text{current value } D \cdot \widetilde{C}", font_size=MATH_SIZE_MEDIUM,
                        substrings_to_isolate=[r"\text{future option price }", r"\text{current value }"])
                .set_color_by_tex("future option price", BLUE).set_color_by_tex("current value", YELLOW),
                MathTex(r"\text{• Convert the }\text{current price } S(0) \text{ to }\text{future value } "
                        r"\frac{S(0)}{D}", font_size=MATH_SIZE_MEDIUM,
                        substrings_to_isolate=[r"\text{current price }", r"\text{future value }"])
                .set_color_by_tex("current price", YELLOW).set_color_by_tex("future value", BLUE)
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(previous_footer, DOWN, buff=0.5)
            .align_to(previous_footer, LEFT)
        )
        for line in bullet_points:
            self.play(Write(line))
            self.wait(1.0)

        final_formula = MathTex(
            r"C &= D \cdot \left[\frac{S(0)}{D} \cdot \Phi(d_+) - K \cdot \Phi(d_-)\right]",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(bullet_points, DOWN, buff=0.3)
        self.play(Write(final_formula))
        self.wait(1.0)

        # we actually need to add the D factor into the d_+ term as well
        # K is matched to D \cdot K with the whole thing replaced to avoid quirks of MatchingTex / nested \overs
        final_footer = MathTex(
            r"\text{where } d_+ = "
            r"{ \ln\left(S(0) \over ",
            r"D \cdot K",
            r"\right) - {\sigma^2 \over 2} \cdot t \over \sigma \cdot \sqrt{t} }, "
            r"\hspace{0.5em}"
            r"d_- = d_+ - \sigma \cdot \sqrt{t}, \hspace{0.5em} D = e^{-rt}", font_size=MATH_SIZE_SMALL
        ).move_to(extended_footer, LEFT)
        self.play(TransformMatchingTex(extended_footer, final_footer))
        self.wait(1.0)

        self.play(Circumscribe(final_formula))
        self.wait(1.0)

        title = (Text("Black-Scholes-Merton Formula for Pricing Options", font_size=TEXT_SIZE_LARGE, color=YELLOW)
                 .move_to(ORIGIN + UP * 2.0))
        self.play(*[FadeOut(x) for x in (bullet_points, previous_formula)],
                  FadeIn(title),
                  final_formula.animate.move_to(ORIGIN + 0.75 * UP),
                  final_footer.animate.move_to(ORIGIN + DOWN))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (title, final_formula, final_footer)])
        self.wait(1.0)

    def construct(self):
        display_section_title(self, "fully analytical")

        distribution_header, distribution_plot_group = self.plot_distribution()
        self.display_option_price_formula(distribution_plot_group)
        self.calculate_probability_term(distribution_header)
        self.calculate_expectation_term(distribution_header)

        non_discounted_formula, combined_formula_footer = self.combining_together()
        self.discuss_discounting(non_discounted_formula, combined_formula_footer)
