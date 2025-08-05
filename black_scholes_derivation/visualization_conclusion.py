from manim import *
from scipy.stats import lognorm

from shared_data_and_functions import TEXT_SIZE_MEDIUM, MATH_SIZE_MEDIUM


class BlackScholesVisualization(Scene):
    def __init__(self):
        super().__init__()

        self.price_ax = Axes(
            x_range=[250.0, 350.1, 25],
            y_range=[0.0, 0.05, 0.01],
            x_length=4,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).to_edge(LEFT, buff=1.0)

        # HACK: manually adding in dollar signs on the x-axis label numbers
        self.price_ax.x_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                                         for i in np.arange(*self.price_ax.x_range)})

        self.price_labels = self.price_ax.get_axis_labels(
            x_label=Tex(r"\text{Stock Price at Time $t$}", font_size=TEXT_SIZE_MEDIUM),
            y_label=Tex(r"\text{Distribution Density}", font_size=TEXT_SIZE_MEDIUM)
        )
        self.price_labels[0].next_to(self.price_ax.x_axis.get_center(), DOWN, buff=0.75)

        self.S0, self.sigma, self.T, self.K = (ValueTracker(x) for x in (300.0, 0.10, 0.25, 310.0))
        self.plot_xs = np.linspace(*self.price_ax.x_range[:2], 1000)

        self.variable_positions = None  # will be used to fix positions of the Black-Scholes variables latex

    def create_price_distribution(self)
        """Create the graph for the price distribution, depending on the current Black-Scholes parameters."""
        lognorm_scale = self.S0.get_value() * np.exp(self.sigma.get_value() ** 2 * self.T.get_value() / 2)
        lognorm_s = self.sigma.get_value() * np.sqrt(self.T.get_value())
        lognorm_pdf = lambda xs: lognorm.pdf(xs, scale=lognorm_scale, s=lognorm_s)

        price_pdf_plot = self.price_ax.plot_line_graph(self.plot_xs, lognorm_pdf(self.plot_xs), line_color=BLUE,
                                                       add_vertex_dots=False, z_index=1)
        strike_line = DashedLine(self.price_ax.c2p(self.K.get_value(), 0.0),
                                 self.price_ax.c2p(self.K.get_value(), self.price_ax.y_range[1]))
        area_above_strike = self.price_ax.get_area(self.price_ax.plot(lognorm_pdf),
                                                   x_range=(self.K.get_value(), self.price_ax.x_range[1]),
                                                   color=BLUE, opacity=0.5)

        return price_pdf_plot, strike_line, area_above_strike

    def create_text(self):
        """Create TeX for the Black-Scholes variables with some hacky fixed positioning."""
        variables = VGroup(
            MathTex(rf"S(0) = \${self.S0.get_value():.0f}", font_size=MATH_SIZE_MEDIUM),
            MathTex(rf"\sigma = {100 * self.sigma.get_value():.1f}\%", font_size=MATH_SIZE_MEDIUM),
            MathTex(rf"T = {self.T.get_value():.2f}", font_size=MATH_SIZE_MEDIUM),
            MathTex(rf"K = \${self.K.get_value():.0f}", font_size=MATH_SIZE_MEDIUM)
        ).arrange(RIGHT, buff=1.0).to_edge(UP, buff=0.5)

        if self.variable_positions:
            # overriding positions from arrange to avoid shifting text as latex width changes
            for i, v in enumerate(variables):
                v.move_to(self.variable_positions[i])
        else:
            self.variable_positions = [x.get_center() for x in variables]

        return variables

    def construct(self):
        variables = self.create_text()
        self.play(Write(variables), run_time=2.0)
        self.wait(1.0)

        price_pdf_plot, strike_line, area_above_strike = self.create_price_distribution()
        self.play(Create(self.price_ax), Write(self.price_labels), run_time=2.0)
        self.play(Create(price_pdf_plot, rate_func=linear))
        self.wait(1.0)

        self.play(Create(strike_line), rate_func=linear)
        self.play(FadeIn(area_above_strike))
        self.wait(1.0)

        price_pdf_plot.add_updater(lambda m: m.become(self.create_price_distribution()[0]))
        strike_line.add_updater(lambda m: m.become(self.create_price_distribution()[1]))
        area_above_strike.add_updater(lambda m: m.become(self.create_price_distribution()[2]))
        variables.add_updater(lambda m: m.become(self.create_text()))

        # while just the price distribution is on screen, sweep each variable up and down
        for variable, values in [
            (self.S0, (280.0, 300.0, 320.0)),
            (self.sigma, (0.05, 0.15, 0.10)),
            (self.T, (0.10, 0.50, 0.25)),
            (self.K, (280.0, 320.0, 310.0))
        ]:
            for v in values:
                self.play(variable.animate.set_value(v), run_time=2.0)
            self.wait(1.0)
