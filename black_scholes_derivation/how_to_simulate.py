from manim import *
from scipy.stats import norm


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
        labels = ax.get_axis_labels(x_label=r"\text{Stock Price}", y_label=r"\text{Distribution Density}")
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
        negative_text = Text("Negative Stock Prices?", font_size=36, color=RED).next_to(negative_area, DOWN, buff=0.75)
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

        comparison_text = (Text("Stock prices cannot be compared directly!", font_size=36, color=RED)
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
            Tex(r"Starting Price:", font_size=40),
            Tex(r"Increase 10\%:", font_size=40),
            Tex(r"Increase 10\%:", font_size=40),
            Tex(r"Increase 10\%:", font_size=40),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).align_to(ORIGIN, RIGHT).shift(LEFT * 0.5)
        right_math = VGroup(
            MathTex(r"\$100", font_size=40),
            MathTex(r"\$100 \cdot 1.10 = \$110", font_size=40),
            MathTex(r"\$110 \cdot 1.10 = \$121", font_size=40),
            MathTex(r"\$121 \cdot 1.10 \approx \$133", font_size=40),
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
        exercise_label = (Text("Exercise #2:", color=YELLOW, font_size=36)
                          .next_to(quality_texts[-1], DOWN, buff=1.0).to_edge(LEFT, buff=0.5))
        exercise_text = Tex(
            r"\begin{flushleft}"  # a bit of a weird hack to get left-aligned multi-line latex
            r"Let $S(t)$ be the stock price at time $t$. Can you \\"
            r"transform a normal distribution and use it to \\"
            r"construct $S(t)$ so that it has these three qualities?"
            r"\end{flushleft}",
            font_size=46  # approximately the equivalent of text font size 36
        ).next_to(exercise_label, RIGHT, buff=0.25).align_to(exercise_label, UP)
        self.play(Write(exercise_label))
        self.play(Write(exercise_text))
        self.wait(1.0)

        # placeholder for hint, viewers can do the exercise without it by pausing
        hint_label = (Text("Hint:", font_size=36).next_to(exercise_text, DOWN, buff=0.5)
                      .align_to(exercise_label, RIGHT))
        hint_countdown = (Text("(revealed in 5 seconds)", font_size=36).next_to(hint_label, RIGHT, buff=0.25)
                          .align_to(hint_label, UP))
        self.play(Write(hint_label))
        self.play(Write(hint_countdown))
        self.wait(5.0)

        hint_text = Tex(
            r"\begin{flushleft}"
            r"Normal distributions ``add together.'' What kind \\"
            r"of function turns adding into multiplying?"
            r"\end{flushleft}",
            font_size=46
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
        exp_labels = exp_plot.get_axis_labels(x_label=r"x", y_label=r"e^{x}")
        exp_graph = exp_plot.plot_line_graph(
            x_values=np.linspace(*exp_plot.x_range[:2], 1000),
            y_values=np.exp(np.linspace(*exp_plot.x_range[:2], 1000)),
            line_color=BLUE, add_vertex_dots=False
        )
        self.play(Create(exp_plot), Write(exp_labels))
        self.play(Create(exp_graph), rate_func=linear, run_time=1.0)
        self.wait(1.0)

        # bottom-right: turning adding into multiplying
        exp_tex = (Tex(r"$e^{x+y} = e^{x} \cdot e^{y}$", font_size=46)
                   .next_to(exp_plot, RIGHT, buff=1.0).align_to(exp_plot, UP))
        self.play(Write(exp_tex))
        self.wait(1.0)

        consider_lognormal = Tex(r"Consider $\dfrac{S(t)}{S(0)} \sim \exp\left(N(\mu, \sigma^2)\right)$!",
                                 font_size=46).next_to(exp_tex, DOWN, buff=0.5).align_to(exp_tex, LEFT)
        self.play(Write(consider_lognormal))
        self.wait(1.0)

        # fading out everything except the lognormal text, which acts as the next slide header
        self.play(*[FadeOut(x) for x in (exercise_text, exercise_label, exp_plot, exp_labels,
                                         exp_graph, exp_tex, quality_texts)],
                  consider_lognormal.animate.move_to(ORIGIN).to_edge(UP, buff=0.5))
        return consider_lognormal

    def construct(self):
        title_text = Text("How to Simulate Stock Prices?", font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(title_text))

        # Even though we're rendering all these lines at separate times, we need to have this as a shared paragraph
        # because aligning text is a pain otherwise. Bounding boxes of text objects include ascenders/descenders from
        # the taller characters, so we can't just apply a fixed offset between the lines.
        qualities_text = Paragraph(
            "#1: Prices should not go negative",
            "#2: Price moves should be relative",
            "#3: Relative changes should multiply, not add",
            font_size=32, alignment="left", line_spacing=0.75
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

        # TODO: discuss lognormal: naming and visual before continuing
