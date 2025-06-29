from manim import *
from scipy.stats import norm


class HowToSimulate(Scene):
    def construct(self):
        title_text = Text("How to Simulate Stock Prices?", font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(title_text))

        ax = Axes(
            x_range=[-10, 50.1, 10],
            y_range=[0.0, 0.1, 0.025],
            x_length=6,
            y_length=4,
            axis_config={"include_numbers": False},
            y_axis_config={"include_numbers": True},
            tips=False
        ).next_to(title_text, DOWN, buff=1.0)

        # HACK: manually adding in dollar signs on the x-axis label numbers
        ax.x_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.x_range)})
        labels = ax.get_axis_labels(x_label=r"\text{Stock Price}", y_label=r"\text{Distribution Density}")
        self.play(Create(ax), Write(labels))
        self.wait(1.0)

        plot_xs = np.linspace(*ax.x_range[:2], 1000)
        normal_dist = ax.plot_line_graph(plot_xs, norm.pdf(plot_xs, loc=25, scale=5),
                                         line_color=BLUE, add_vertex_dots=False)
        self.play(Create(normal_dist, run_time=2.0))
        self.wait(1.0)
