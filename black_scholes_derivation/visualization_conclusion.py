from manim import *
from scipy.stats import lognorm

from shared_data_and_functions import TEXT_SIZE_MEDIUM, MATH_SIZE_MEDIUM, black_scholes_price


class BlackScholesVisualization(Scene):
    def __init__(self):
        super().__init__()

        self.price_ax = Axes(
            x_range=[250.0, 350.1, 25],
            y_range=[0.0, 0.05, 0.01],
            x_length=5.25,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).to_edge(LEFT, buff=0.5)

        # HACK: manually adding in dollar signs on the x-axis label numbers
        self.price_ax.x_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                                         for i in np.arange(*self.price_ax.x_range)})

        self.price_labels = self.price_ax.get_axis_labels(
            x_label=Tex(r"\text{Stock Price at Time $t$}", font_size=TEXT_SIZE_MEDIUM),
            y_label=Tex(r"\text{Distribution Density}", font_size=TEXT_SIZE_MEDIUM)
        )
        self.price_labels[0].next_to(self.price_ax.x_axis.get_center(), DOWN, buff=0.75)

        self.S0, self.sigma, self.t, self.K, self.r = (ValueTracker(x) for x in (300.0, 0.10, 0.25, 310.0, 0.04))
        self.variable_positions = None  # will be used to fix positions of the Black-Scholes variables latex

        self.payoff_ax = Axes(
            x_range=[250.0, 350.1, 25],
            y_range=[0.0, 50.1, 10.0],
            x_length=5.25,
            y_length=4,
            axis_config={"include_numbers": False},
            tips=False
        ).to_edge(RIGHT, buff=0.5)

        # HACK: manually adding in dollar signs on the x-axis label numbers
        self.payoff_ax.x_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                                          for i in np.arange(*self.payoff_ax.x_range)})
        self.payoff_ax.y_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                                          for i in np.arange(*self.payoff_ax.y_range)})

        self.payoff_labels = self.payoff_ax.get_axis_labels(
            x_label=Tex(r"\text{Current Stock Price}", font_size=TEXT_SIZE_MEDIUM),
            y_label=Tex(r"\text{Option Payoff}", font_size=TEXT_SIZE_MEDIUM)
        )
        self.payoff_labels[0].next_to(self.payoff_ax.x_axis.get_center(), DOWN, buff=0.75)

    def create_price_distribution(self):
        """Create the graph for the price distribution, depending on the current Black-Scholes parameters."""
        lognorm_scale = self.S0.get_value() * np.exp(self.sigma.get_value() ** 2 * self.t.get_value() / 2)
        lognorm_s = self.sigma.get_value() * np.sqrt(self.t.get_value())
        lognorm_pdf = lambda xs: lognorm.pdf(xs, scale=lognorm_scale, s=lognorm_s)

        plot_xs = np.linspace(*self.price_ax.x_range[:2], 1000)
        price_pdf_plot = self.price_ax.plot_line_graph(plot_xs, lognorm_pdf(plot_xs), line_color=BLUE,
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
            MathTex(rf"t = {self.t.get_value():.2f}", font_size=MATH_SIZE_MEDIUM),
            MathTex(rf"K = \${self.K.get_value():.0f}", font_size=MATH_SIZE_MEDIUM),
            MathTex(rf"r = {100 * self.r.get_value():.1f}\%", font_size=MATH_SIZE_MEDIUM)
        ).arrange(RIGHT, buff=0.8).to_edge(UP, buff=0.5)

        if self.variable_positions:
            # overriding positions from arrange to avoid shifting text as latex width changes
            for i, v in enumerate(variables):
                v.move_to(self.variable_positions[i])
        else:
            self.variable_positions = [x.get_center() for x in variables]

        return variables

    def create_payoff_diagram(self):
        """Create payoff diagram with option prices. A dot will indicate the one for the current stock price."""
        plot_xs = np.linspace(*self.price_ax.x_range[:2], 1000)
        intrinsic_price = self.payoff_ax.plot_line_graph(
            x_values=plot_xs,
            y_values=np.maximum(plot_xs - self.K.get_value(), 0.0),
            line_color=WHITE, add_vertex_dots=False, z_index=1
        )
        intrinsic_price = DashedVMobject(intrinsic_price['line_graph'], num_dashes=50)

        def option_price_fn(x):
            return black_scholes_price(
                S0=x, K=self.K.get_value(), sigma=self.sigma.get_value(), t=self.t.get_value(), r=self.r.get_value()
            )

        option_price_dot = Dot(
            self.payoff_ax.c2p(self.S0.get_value(), option_price_fn(self.S0.get_value())),
            color=WHITE, radius=0.1
        )
        option_price_plot = self.payoff_ax.plot_line_graph(
            x_values=plot_xs,
            y_values=[option_price_fn(x) for x in plot_xs],
            line_color=BLUE, add_vertex_dots=False, z_index=1
        )
        return intrinsic_price, option_price_dot, option_price_plot

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

        # updaters for price distribution plot (left)
        price_pdf_plot.add_updater(lambda m: m.become(self.create_price_distribution()[0]))
        strike_line.add_updater(lambda m: m.become(self.create_price_distribution()[1]))
        area_above_strike.add_updater(lambda m: m.become(self.create_price_distribution()[2]))
        variables.add_updater(lambda m: m.become(self.create_text()))

        # while just the price distribution is on screen, sweep each variable up and down
        for variable, values in [
            (self.S0, (280.0, 320.0, 300.0)),
            (self.sigma, (0.06, 2.0, 0.10)),
            (self.t, (0.10, 1.0, 0.25)),
            (self.K, (280.0, 320.0, 310.0))
        ]:
            for v in values:
                self.play(variable.animate.set_value(v), run_time=2.0)
                self.wait(1.0)

        intrinsic_price, option_price_dot, option_price_plot = self.create_payoff_diagram()
        self.play(Create(self.payoff_ax), Write(self.payoff_labels), run_time=2.0)
        self.play(Create(intrinsic_price), rate_func=linear)
        self.wait(1.0)

        self.play(FadeIn(option_price_dot))
        self.wait(1.0)

        # updaters for payoff diagram dot (right)
        option_price_dot.add_updater(lambda m: m.become(self.create_payoff_diagram()[1]))

        # sweep the dot left and right before we show the actual option price plot
        for v in (260.0, 340.0, 300.0):  # larger range than before
            self.play(self.S0.animate.set_value(v), run_time=2.0)
            self.wait(1.0)

        self.play(FadeIn(option_price_plot))
        self.wait(1.0)

        # this updater needs to come after the FadeIn for it to render properly
        option_price_plot.add_updater(lambda m: m.become(self.create_payoff_diagram()[2]))

        # sweeping all the variables again (including the risk-free rate) now that the payoff diagram is displayed
        for variable, values in [
            (self.S0, (260.0, 340.0, 300.0)),
            (self.sigma, (0.06, 2.0, 0.10)),
            (self.t, (0.10, 1.0, 0.25)),
            (self.K, (280.0, 320.0, 310.0)),
            (self.r, (0.01, 0.10, 0.04))
        ]:
            for v in values:
                self.play(variable.animate.set_value(v), run_time=2.0)
                self.wait(1.0)

        # some final sweeping to hint at basic delta sensitivity
        for v in (260.0, 280.0, 260.0, 340.0, 320.0, 340.0, 300):
            self.play(self.S0.animate.set_value(v), run_time=2.0)
            self.wait(1.0)

        self.wait(1.0)

        for m in (price_pdf_plot, strike_line, area_above_strike, variables, option_price_dot, option_price_plot):
            m.clear_updaters()
        self.play(*[FadeOut(x) for x in (
            self.price_ax, self.price_labels, price_pdf_plot, strike_line, area_above_strike, variables,
            self.payoff_ax, self.payoff_labels, intrinsic_price, option_price_dot, option_price_plot,
        )])
