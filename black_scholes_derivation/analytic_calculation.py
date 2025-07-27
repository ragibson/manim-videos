from scipy.stats import lognorm

from shared_data_and_functions import *


class AnalyticCalculation(Scene):
    def plot_distribution(self):
        # left: simulated stock prices from before
        stock_S0, stock_sigma, T = 300, 0.1, 0.25
        ax, labels, strike_line = stock_price_simulation_graph(shift_amt=DOWN * 0.5)

        self.play(Create(ax, run_time=2.0), Write(labels, run_time=2.0),
                  Create(strike_line, rate_func=linear, run_time=1.0))
        self.wait(1.0)

        simulation_paths = [simple_stock_simulation(start_price=stock_S0, sigma=stock_sigma, T=T, seed=i)
                            for i in range(100)]
        simulation_graphs = [
            ax.plot_line_graph(
                x_values=np.linspace(0, T, len(simulated_path)),
                y_values=simulated_path,
                line_color=BLUE,
                add_vertex_dots=False
            ).set_stroke(opacity=0.1) for simulated_path in simulation_paths
        ]
        self.play(*[Create(p, rate_func=linear) for p in simulation_graphs], run_time=2.0)
        self.wait(1.0)

        distribution_form = MathTex(
            r"S(t) &\sim S(0) \cdot \exp\left(N\left(-\frac{\sigma^2}{2} \cdot t, "
            r"\sigma^2 \cdot t\right)\right)",
            font_size=MATH_SIZE_MEDIUM
        ).to_edge(UP, buff=0.5)
        self.play(Write(distribution_form))

        # right: plot distribution directly
        distribution_ax = Axes(
            x_range=[250, 350.1, 25],
            y_range=[0, 0.03, 0.01],
            x_length=4,
            y_length=4,
            y_axis_config={"include_numbers": True},
            axis_config={"include_numbers": False},
            tips=False
        ).to_edge(RIGHT, buff=1.0).shift(DOWN * 0.5)

        # HACK: manually adding in dollar signs on the left of the x-axis label numbers
        distribution_ax.x_axis.add_labels({i: Tex(fr"\${i:.0f}", font_size=TEXT_SIZE_XSMALL)
                                           for i in np.arange(*ax.y_range)})
        distribution_labels = distribution_ax.get_axis_labels(
            x_label=Tex(r"\text{Stock Price}", font_size=TEXT_SIZE_XSMALL),
            y_label=Tex(r"\text{Distribution Density}", font_size=TEXT_SIZE_XSMALL)
        )
        distribution_labels[0] = distribution_labels[0].shift(RIGHT * 0.25)
        self.play(Create(distribution_ax, run_time=2.0), Write(distribution_labels, run_time=2.0))

        lognorm_sigma = stock_sigma * np.sqrt(T)
        lognorm_mu = -stock_sigma ** 2 / 2 * T
        lognormal_pdf = lambda xs: lognorm.pdf(xs / stock_S0, loc=lognorm_mu, s=lognorm_sigma) / stock_S0
        distribution_graph = distribution_ax.plot(
            lognormal_pdf, x_range=[250, 350.1], color=BLUE
        )
        self.play(Create(distribution_graph, rate_func=linear), run_time=2.0)
        self.wait(1.0)

    def construct(self):
        self.plot_distribution()
