from scipy.stats import norm, lognorm

from shared_data_and_functions import *


def create_normal_lognormal_comparison(ax):
    """Create a series of objects for a normal -> lognormal transformation plot."""
    # HACK: manually adding in dollar signs on the x-axis label numbers
    ax.x_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                          for i in np.arange(*ax.x_range)})
    labels = ax.get_axis_labels(x_label=Tex(r"\text{Stock Price}", font_size=TEXT_SIZE_MEDIUM),
                                y_label=Tex(r"\text{Normal Distribution Density}", font_size=TEXT_SIZE_MEDIUM))

    plot_xs = np.linspace(*ax.x_range[:2], 1000)
    norm_mu, norm_sigma = 20.0, 10.0
    specific_norm_pdf = lambda xs: norm.pdf(xs, loc=norm_mu, scale=norm_sigma)
    price_distribution = ax.plot_line_graph(plot_xs, specific_norm_pdf(plot_xs),
                                            line_color=BLUE, add_vertex_dots=False, z_index=0)
    normal_dist_original = price_distribution.copy().set_stroke(opacity=0.5).set_color(GRAY)

    # rescaling S(t)/S(0) ~ exp(N()) to S(t) ~ S(0) * exp(N())
    specific_lognorm_pdf = lambda xs: lognorm.pdf(xs / norm_mu, loc=0.0, s=norm_sigma / norm_mu) / norm_mu
    lognormal_dist = ax.plot_line_graph(plot_xs, specific_lognorm_pdf(plot_xs),
                                        line_color=BLUE, add_vertex_dots=False, z_index=1)

    # emphasize the major differences, left: no negatives, right: compounding (multiplying) returns
    left_arrow = Arrow(
        start=ax.c2p(-20, 0.025), end=ax.c2p(3, specific_lognorm_pdf(3)),
        color=RED, buff=0
    )
    left_text = (Text("No negatives!", font_size=TEXT_SIZE_MEDIUM, color=RED)
                 .next_to(left_arrow.get_start(), UP, buff=0.0).shift(LEFT * 1.0))
    right_arrow = Arrow(
        start=ax.c2p(55, 0.025), end=ax.c2p(45, specific_lognorm_pdf(45)),
        color=GREEN, buff=0
    )
    right_text = (Text("Compounding returns!", font_size=TEXT_SIZE_MEDIUM, color=GREEN)
                  .next_to(right_arrow.get_start(), UP, buff=0.0).shift(RIGHT * 1.0))

    return (labels, price_distribution, specific_norm_pdf, normal_dist_original, specific_lognorm_pdf, lognormal_dist,
            left_arrow, left_text, right_arrow, right_text)


class DesiredSimulationQualities(Scene):
    def normal_allows_negative_prices(self, title_text, first_quality_text):
        ax = Axes(
            x_range=[-10, 50.1, 10],
            y_range=[0.0, 0.08, 0.02],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).next_to(title_text, DOWN, buff=1.0)

        # HACK: manually adding in dollar signs on the x-axis label numbers
        ax.x_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                              for i in np.arange(*ax.x_range)})
        labels = ax.get_axis_labels(x_label=Tex(r"\text{Stock Price}", font_size=TEXT_SIZE_MEDIUM),
                                    y_label=Tex(r"\text{Distribution Density}", font_size=TEXT_SIZE_MEDIUM))
        self.play(Create(ax), Write(labels))
        self.wait(1.0)

        # plotting out an arbitrary normal distribution of future prices
        scale_tracker = ValueTracker(5.0)
        plot_xs = np.linspace(*ax.x_range[:2], 1000)
        normal_dist = ax.plot_line_graph(plot_xs, norm.pdf(plot_xs, loc=20, scale=scale_tracker.get_value()),
                                         line_color=BLUE, add_vertex_dots=False)
        self.play(Create(normal_dist, run_time=2.0))
        self.wait(1.0)

        # animate out the scale getting larger, eventually hitting negative numbers with non-negligible probability
        normal_dist.add_updater(
            lambda x: x.become(ax.plot_line_graph(plot_xs, norm.pdf(plot_xs, loc=20, scale=scale_tracker.get_value()),
                                                  line_color=BLUE, add_vertex_dots=False))
        )
        self.play(scale_tracker.animate.set_value(10.0), run_time=2.0)
        self.wait(1.0)
        normal_dist.clear_updaters()

        # shade the area under the curve where the stock price is negative
        negative_area = ax.get_area(
            ax.plot(lambda x: norm.pdf(x, loc=20, scale=scale_tracker.get_value())),
            x_range=(-10, 0), color=RED, opacity=0.75
        )
        negative_text = (Text("Negative Stock Prices?", font_size=TEXT_SIZE_MEDIUM, color=RED)
                         .next_to(negative_area, DOWN, buff=0.75))
        self.play(FadeIn(negative_area), FadeIn(negative_text), run_time=1.0)
        self.wait(1.0)

        self.play(ReplacementTransform(title_text, first_quality_text))
        self.wait(1.0)
        self.play(*[FadeOut(x) for x in (ax, labels, normal_dist, negative_area, negative_text)])
        self.wait(1.0)

    def stock_prices_are_on_different_scales(self, second_quality_text):
        nvda_image = (ImageMobject("stock_history_examples/NVDA.png").scale(1.25)
                      .to_edge(LEFT, buff=0.5).shift(DOWN * 0.5))
        nvda_price_rectangle = Rectangle(width=1.35, height=0.4, color=YELLOW).move_to((-5.9, 0.7, 0))
        nvda_return_rectangle = Rectangle(width=0.625, height=0.2, color=YELLOW).move_to((-5.73, 0.38, 0))

        self.play(FadeIn(nvda_image))
        self.wait(1.0)
        self.play(Create(nvda_price_rectangle))
        self.wait(1.0)

        hd_image = (ImageMobject("stock_history_examples/HD.png").scale(1.25)
                    .to_edge(RIGHT, buff=0.5).shift(DOWN * 0.5))
        hd_price_rectangle = Rectangle(width=1.45, height=0.4, color=YELLOW).move_to((1.1, 0.7, 0))
        hd_return_rectangle = Rectangle(width=0.55, height=0.2, color=YELLOW).move_to((1.2, 0.38, 0))
        self.play(FadeIn(hd_image))
        self.wait(1.0)
        self.play(Create(hd_price_rectangle))
        self.wait(1.0)

        comparison_text = (Text("Stock prices cannot be compared directly!", font_size=TEXT_SIZE_MEDIUM, color=RED)
                           .align_to(ORIGIN, ORIGIN).shift(DOWN * 3.25))
        self.play(Create(comparison_text))
        self.wait(1.0)

        # moving price boxes over to the returns
        self.play(Transform(hd_price_rectangle, hd_return_rectangle),
                  Transform(nvda_price_rectangle, nvda_return_rectangle))
        self.wait(1.0)

        self.play(Write(second_quality_text))
        self.wait(1.0)
        self.play(*[FadeOut(x) for x in (nvda_image, hd_image, nvda_price_rectangle,
                                         hd_price_rectangle, comparison_text)])
        self.wait(1.0)

    def relative_moves_should_compound(self, third_quality_text):
        # have to split these to get the alignment right
        left_text = VGroup(
            Tex(r"Starting Price:", font_size=MATH_SIZE_MEDIUM),
            Tex(r"Increase 10\%:", font_size=MATH_SIZE_MEDIUM),
            Tex(r"Increase 10\%:", font_size=MATH_SIZE_MEDIUM),
            Tex(r"Increase 10\%:", font_size=MATH_SIZE_MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).align_to(ORIGIN, RIGHT).shift(LEFT * 0.5)
        right_math = VGroup(
            MathTex(r"\$100", font_size=MATH_SIZE_MEDIUM),
            MathTex(r"\$100 \cdot 1.10 = \$110", font_size=MATH_SIZE_MEDIUM),
            MathTex(r"\$110 \cdot 1.10 = \$121", font_size=MATH_SIZE_MEDIUM),
            MathTex(r"\$121 \cdot 1.10 \approx \$133", font_size=MATH_SIZE_MEDIUM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(left_text, RIGHT, buff=0.5)

        for text, expression in zip(left_text, right_math):
            self.play(Write(text))
            self.play(Write(expression))
            self.wait(0.5)

        self.play(Write(third_quality_text))
        self.wait(1.0)

        self.play(FadeOut(left_text), FadeOut(right_math))
        self.wait(1.0)

    def set_up_exercise(self, quality_texts):
        exercise_label = (Text("Exercise #2:", color=YELLOW, font_size=TEXT_SIZE_MEDIUM)
                          .next_to(quality_texts[-1], DOWN, buff=1.0).to_edge(LEFT, buff=0.5))
        exercise_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"Let $S(t)$ be the stock price at time $t$. Can you \\"
            r"transform a normal distribution and use it to \\"
            r"construct $S(t)$ so that it has these three qualities?"
            r"\end{flushleft}",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text), run_time=3.0)
        self.wait(1.0)

        # placeholder for hint, viewers can do the exercise without it by pausing
        hint_label = (Text("Hint:", font_size=TEXT_SIZE_MEDIUM).next_to(exercise_text, DOWN, buff=0.5)
                      .align_to(exercise_label, RIGHT))
        hint_countdown = (Text("(revealed in 5 seconds)", font_size=TEXT_SIZE_MEDIUM)
                          .next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP))
        self.play(Write(hint_label))
        self.play(Write(hint_countdown))
        self.wait(5.0)

        hint_text = Tex(
            r"\begin{flushleft}"
            r"Normal distributions ``add together.'' What kind \\"
            r"of function turns adding into multiplying?"
            r"\end{flushleft}",
            font_size=MATH_SIZE_MEDIUM
        ).next_to(hint_label, RIGHT, buff=0.25).align_to(hint_label, UP)
        self.play(FadeOut(hint_countdown))
        self.play(Write(hint_text))
        self.wait(5.0)

        self.play(*[FadeOut(x) for x in (hint_label, hint_text)])

        # bottom-left: exp(x) plot
        exp_plot = Axes(
            x_range=[-2, 2.01, 1],
            y_range=[0, 8.01, 2],
            x_length=3,
            y_length=2,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": False},
            tips=False
        ).to_edge(DOWN, buff=0.5).to_edge(LEFT, buff=2.0)
        exp_labels = exp_plot.get_axis_labels(x_label=Tex(r"$x$", font_size=MATH_SIZE_MEDIUM),
                                              y_label=Tex(r"$e^{x}$", font_size=MATH_SIZE_MEDIUM))
        exp_graph = exp_plot.plot_line_graph(
            x_values=np.linspace(*exp_plot.x_range[:2], 1000),
            y_values=np.exp(np.linspace(*exp_plot.x_range[:2], 1000)),
            line_color=BLUE, add_vertex_dots=False
        )
        self.play(Create(exp_plot), Write(exp_labels))
        self.play(Create(exp_graph), rate_func=linear, run_time=1.0)
        self.wait(1.0)

        # bottom-right: turning adding into multiplying
        exp_tex = (Tex(r"$e^{x+y} = e^{x} \cdot e^{y}$", font_size=MATH_SIZE_MEDIUM)
                   .next_to(exp_plot, RIGHT, buff=1.0).align_to(exp_plot, UP))
        self.play(Write(exp_tex))
        self.wait(1.0)

        # isolating mu and sigma so we can emphasize them as the parameters we want to determine
        consider_lognormal = (MathTex(r"\text{Consider } \dfrac{S(t)}{S(0)} \sim \exp\left(N(\mu, \sigma^2)\right)"
                                      r"\text{!}", substrings_to_isolate=[r"\mu", r"\sigma^2"],
                                      font_size=MATH_SIZE_MEDIUM)
                              .next_to(exp_tex, DOWN, buff=0.5).align_to(exp_tex, LEFT))
        self.play(Write(consider_lognormal))
        self.wait(1.0)

        # fading out everything except the lognormal text, which acts as the next slide header
        self.play(*[FadeOut(x) for x in (exercise_text, exercise_label, exp_plot, exp_labels,
                                         exp_graph, exp_tex, quality_texts)],
                  consider_lognormal.animate.move_to(ORIGIN).to_edge(UP, buff=0.5))
        return consider_lognormal

    def discuss_lognormal(self, lognormal_header):
        lognormal_text = (Text('"Lognormal Distribution"', font_size=TEXT_SIZE_MEDIUM, color=BLUE)
                          .next_to(lognormal_header, DOWN, buff=0.5).to_edge(LEFT, buff=1.0))
        self.play(Write(lognormal_text))

        nomenclature_explanation = (Tex(r"$X \sim \exp\left(N(\mu, \sigma^2)\right) \iff "
                                        r"\ln\left(X\right) \sim N(\mu, \sigma^2)$", font_size=MATH_SIZE_MEDIUM)
                                    .next_to(lognormal_text, DOWN, buff=0.5).align_to(lognormal_text, LEFT)
                                    .shift(RIGHT * 1.0))
        self.play(Write(nomenclature_explanation))
        self.wait(2.0)
        self.play(FadeOut(lognormal_text), FadeOut(nomenclature_explanation))

        # Create axes that work for both distributions
        ax = Axes(
            x_range=[-10, 60.1, 10],
            y_range=[0.0, 0.05, 0.01],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).next_to(lognormal_header, DOWN, buff=1.0).align_to(ORIGIN, LEFT + RIGHT)

        (labels, price_distribution, _, normal_dist_original, specific_lognorm_pdf, lognormal_dist,
         left_arrow, left_text, right_arrow, right_text) = create_normal_lognormal_comparison(ax)

        self.play(Create(ax), Write(labels))

        self.play(Create(price_distribution), run_time=2.0)
        self.wait(1.0)

        self.add(normal_dist_original)
        self.play(ReplacementTransform(price_distribution, lognormal_dist),
                  Transform(labels[1], Tex(r"\text{Lognormal Distribution Density}", font_size=TEXT_SIZE_MEDIUM)
                            .move_to(labels[1], aligned_edge=LEFT)), run_time=2.0)
        self.wait(1.0)

        self.play(Create(left_arrow), Write(left_text))
        self.wait(1.0)
        self.play(Create(right_arrow), Write(right_text))
        self.wait(1.0)

        # flagging that finding the parameters of the distribution is the next step
        mu_substring, sigma_substring = lognormal_header[1], lognormal_header[3]
        self.play(Circumscribe(mu_substring), Circumscribe(sigma_substring))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in (ax, labels, price_distribution, normal_dist_original, lognormal_dist,
                                         lognormal_header, left_arrow, left_text, right_arrow, right_text)])

    def construct(self):
        title_text = Text("How to Simulate Stock Prices?", font_size=TEXT_SIZE_MEDIUM).to_edge(UP, buff=0.5)
        self.play(Write(title_text))

        # Even though we're rendering all these lines at separate times, we need to have this as a shared paragraph
        # because aligning text is a pain otherwise. Bounding boxes of text objects include ascenders/descenders from
        # the taller characters, so we can't just apply a fixed offset between the lines.
        qualities_text = Paragraph(
            "#1: Prices should not go negative",
            "#2: Price moves should be relative",
            "#3: Relative changes should compound",
            font_size=TEXT_SIZE_SMALL, alignment="left", line_spacing=0.75
        ).move_to(title_text, aligned_edge=UP).align_to(title_text, LEFT)

        # misnomer in Manim, chars is a VGroup of the three lines of text (each a VGroup)
        first_quality, second_quality, third_quality = qualities_text.chars

        self.normal_allows_negative_prices(title_text, first_quality)
        self.play(first_quality.animate.set_color(GRAY))

        self.stock_prices_are_on_different_scales(second_quality)
        self.play(second_quality.animate.set_color(GRAY))

        self.relative_moves_should_compound(third_quality)
        self.play(third_quality.animate.set_color(GRAY))

        self.play(*[t.animate.set_color(WHITE) for t in qualities_text])
        lognormal_header = self.set_up_exercise(qualities_text)

        self.discuss_lognormal(lognormal_header)
