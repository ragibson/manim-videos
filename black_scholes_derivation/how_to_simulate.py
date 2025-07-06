from manim import *
from scipy.stats import norm


class DesiredSimulationQualities(Scene):
    def normal_allows_negative_prices(self, title_text):
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

        first_quality_text = (Text("#1: Prices should not go negative", font_size=32)
                              .move_to(title_text).align_to(title_text, LEFT))
        self.play(Transform(title_text, first_quality_text))
        self.wait(1.0)
        self.play(*[FadeOut(x) for x in (ax, labels, normal_dist, negative_area, negative_text)])
        self.wait(1.0)

        return first_quality_text

    def stock_prices_are_on_different_scales(self, first_quality_text):
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

        second_quality_text = (Text("#2: Price moves should be relative", font_size=32)
                               .next_to(first_quality_text, DOWN, buff=0.25).align_to(first_quality_text, LEFT))
        self.play(Write(second_quality_text))
        self.wait(1.0)
        self.play(*[FadeOut(x) for x in (nvda_image, hd_image, nvda_price_rectangle,
                                         hd_price_rectangle, comparison_text)])
        self.wait(1.0)

        return second_quality_text

    def relative_moves_should_compound(self, second_quality_text):
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

        third_quality_text = (Text("#3: Relative changes should multiply", font_size=32)
                              .next_to(second_quality_text, DOWN, buff=0.25).align_to(second_quality_text, LEFT))
        self.play(Write(third_quality_text))
        self.wait(1.0)

        self.play(FadeOut(left_text), FadeOut(right_math))
        self.wait(1.0)

        return third_quality_text

    def construct(self):
        title_text = Text("How to Simulate Stock Prices?", font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(title_text))

        first_quality_text = self.normal_allows_negative_prices(title_text)
        self.play(first_quality_text.animate.set_color(GRAY))

        second_quality_text = self.stock_prices_are_on_different_scales(first_quality_text)
        self.play(second_quality_text.animate.set_color(GRAY))

        third_quality_text = self.relative_moves_should_compound(second_quality_text)
        self.play(third_quality_text.animate.set_color(GRAY))
