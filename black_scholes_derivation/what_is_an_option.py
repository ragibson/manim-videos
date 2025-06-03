from manim import *


def simple_stock_simulation(start_price=100, sigma=0.15, dt=1 / 252, T=1, seed=0):
    np.random.seed(seed)
    n_steps = int(T / dt)
    increments = np.random.normal(0, sigma * np.sqrt(dt), n_steps)
    prices = start_price * np.exp(np.cumsum(increments))  # ignoring drift
    return prices


class WhatIsAnOption(Scene):
    def construct(self):
        simulated_path = simple_stock_simulation(start_price=100, sigma=0.15, seed=0)

        ax = Axes(
            x_range=[0, 1.1, 5],
            y_range=[80, 125, 10],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True}
        ).to_edge(DOWN)

        labels = ax.get_axis_labels(x_label=r"\text{Time (years)}", y_label=r"\text{Stock Price}")
        graph = ax.plot_line_graph(
            x_values=np.linspace(0, 1, len(simulated_path)),
            y_values=simulated_path,
            line_color=BLUE,
            add_vertex_dots=False
        )

        self.play(Create(ax), Write(labels))
        self.play(Create(graph, run_time=5.0, rate_func=linear))
        self.wait(1)
