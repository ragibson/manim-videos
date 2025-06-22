from manim import *

from shared_data_and_functions import simple_stock_simulation


class FindingAFairPrice(Scene):
    def construct(self):
        future_quote = MarkupText(f'"An option is ... '
                                  f'on a specific date <span foreground="{BLUE}">in the future</span>."',
                                  font_size=36).to_edge(UP, buff=0.5)
        self.play(Write(future_quote))
        self.wait(2.0)

        how_to_text = (Text("How could you find a fair price for this?", font_size=36)
                       .next_to(future_quote, DOWN, buff=0.5))
        self.play(Write(how_to_text))

        # add in stock price graph
        ax = Axes(
            x_range=[0, 1.1, 0.25],
            y_range=[225, 375.1, 25],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": False},
            tips=False
        ).next_to(how_to_text, DOWN, buff=1.0)

        # HACK: manually adding in dollar signs on the left of the y-axis label numbers
        ax.y_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.y_range)})
        ax.x_axis.add_labels({0.5: "Today"})
        ax.get_axis_labels(x_label=r"\text{Time}", y_label=r"\text{Stock Price}")

        # plot first just up to "today" (internally, t=0.5)
        simulated_path = simple_stock_simulation(start_price=300, sigma=0.15, seed=10, T=0.5)
        graph = ax.plot_line_graph(
            x_values=np.linspace(0, 0.5, len(simulated_path)),
            y_values=simulated_path,
            line_color=BLUE,
            add_vertex_dots=False
        )
        self.play(Create(ax))
        self.play(Create(graph, rate_func=linear, run_time=2.0))
        self.wait(1.0)

        # continue forward to "guess" possible futures
        # push possibilities up/down (via Brownian bridges) to aid spoken explanation
        brownian_rvs = [simple_stock_simulation(start_price=simulated_path[-1], sigma=0.15, seed=seed, T=0.5)
                        - simulated_path[-1] for seed in [4, 1, 2]]
        ts = np.linspace(0, 0.5, len(brownian_rvs[0]))
        brownian_rvs = [sim - ts / 0.5 * sim[-1]
                        + np.linspace(simulated_path[-1], end_point, len(sim))
                        for sim, end_point in zip(brownian_rvs, [350, 300, 250])]

        possible_futures_graphs = [
            ax.plot_line_graph(
                x_values=np.linspace(0.5, 1.0, len(brownian_rvs[idx])),
                y_values=brownian_rvs[idx],
                line_color=[GREEN, YELLOW, RED][idx],
                add_vertex_dots=False
            ) for idx in range(len(brownian_rvs))
        ]
        for g in possible_futures_graphs:
            self.play(Create(g, rate_func=linear, run_time=2.0))
        self.wait(1.0)
