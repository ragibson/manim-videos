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
        hint1_label = (Text("Hint:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=0.5)
                       .align_to(exercise_label, RIGHT))
        hint1_countdown = (Text("(revealed in 5 seconds)", font_size=TEXT_SIZE_MEDIUM)
                           .next_to(hint1_label, RIGHT, buff=0.25).align_to(hint1_label, UP))
        self.play(Write(hint1_label))
        self.play(Write(hint1_countdown))
        self.wait(5.0)

        hint1_text = Tex(r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
                         r"Transform $S(t)$ so that you can use \\"
                         r"the standard normal CDF."
                         r"\end{flushleft}",
                         font_size=MATH_SIZE_MEDIUM).next_to(hint1_label, RIGHT, buff=0.25).align_to(hint1_label, UP)
        self.play(FadeOut(hint1_countdown))
        self.play(Write(hint1_text))
        self.wait(3.0)

        self.play(FadeOut(hint1_label), FadeOut(hint1_text))

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
            r"\frac{\sigma^2}{2} \cdot T}{\sigma \cdot \sqrt{T}}\right)",
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

    def construct(self):
        distribution_header, distribution_plot_group = self.plot_distribution()
        self.display_option_price_formula(distribution_plot_group)
        self.calculate_probability_term(distribution_header)
