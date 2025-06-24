from manim import *

from shared_data_and_functions import simple_stock_simulation


class GuessingTheFuture(Scene):
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
            x_range=[0, 1.01, 0.25],
            y_range=[225, 375.1, 25],
            x_length=8,
            y_length=4,
            axis_config={"include_numbers": False},
            tips=False
        ).next_to(how_to_text, DOWN, buff=1.0)

        # HACK: manually adding in dollar signs on the left of the y-axis label numbers
        ax.y_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.y_range)})
        ax.x_axis.add_labels({0.5: "Today"})
        labels = ax.get_axis_labels(x_label=r"\text{Time}", y_label=r"\text{Stock Price}")

        # plot first just up to "today" (internally, t=0.5)
        simulated_path = simple_stock_simulation(start_price=300, sigma=0.15, seed=10, T=0.5)
        graph = ax.plot_line_graph(
            x_values=np.linspace(0, 0.5, len(simulated_path)),
            y_values=simulated_path,
            line_color=BLUE,
            add_vertex_dots=False
        )
        strike_line = DashedLine(ax.c2p(0.0, 300), ax.c2p(1.0, 300))
        self.play(Create(ax), Write(labels), run_time=2.0)
        self.play(Create(strike_line))
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
                line_color=[GREEN, GOLD, RED][idx],
                add_vertex_dots=False
            ) for idx in range(len(brownian_rvs))
        ]
        for g in possible_futures_graphs:
            self.play(Create(g, rate_func=linear, run_time=2.0))
            self.wait(1.0)
        self.wait(1.0)

        simulate_text = (Text("Simulate!", font_size=36, color=YELLOW)
                         .move_to(ax.get_center() + UP * 2.0 + RIGHT * 2.0))
        self.play(Write(simulate_text))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in [ax, labels, graph, future_quote, how_to_text, simulate_text, strike_line]
                    + possible_futures_graphs])


class DemonstrateSimulation(Scene):
    _current_seed = 12347
    simulation_paths = []
    simulation_graphs = []
    histogram_counts = [0.0] * 11

    def generate_next_path(self, ax):
        T = 0.25
        simulated_path = simple_stock_simulation(start_price=300, sigma=0.1, T=T, seed=self._current_seed)
        self._current_seed += 1

        graph = ax.plot_line_graph(
            x_values=np.linspace(0, T, len(simulated_path)),
            y_values=simulated_path,
            line_color=BLUE,
            add_vertex_dots=False
        )
        self.simulation_paths.append(simulated_path)
        self.simulation_graphs.append(graph)

        rounded_profit = int(round((simulated_path[-1] - 300) / 5, 0) * 5)
        bin_idx = min(max(0, rounded_profit // 5), len(self.histogram_counts) - 1)
        self.histogram_counts[bin_idx] += 1

    def construct(self):
        # left: simulated stock prices
        ax = Axes(
            x_range=[0, 0.251, 0.05],
            y_range=[250, 350.1, 25],
            x_length=4,
            y_length=4,
            x_axis_config={"include_numbers": True},
            axis_config={"include_numbers": False},
            tips=False
        ).to_edge(LEFT, buff=1.0)

        # HACK: manually adding in dollar signs on the left of the y-axis label numbers
        ax.y_axis.add_labels({i: Tex(fr"\${i:.0f}", font_size=30) for i in np.arange(*ax.y_range)})
        labels = ax.get_axis_labels(x_label=Tex(r"\text{Time (years)}", font_size=30),
                                    y_label=Tex(r"\text{Stock Price}", font_size=30))

        strike_line = DashedLine(ax.c2p(0.0, 300), ax.c2p(0.25, 300))
        self.play(Create(ax), Write(labels), run_time=2.0)
        self.play(Create(strike_line, rate_func=linear))
        self.wait(1.0)

        self.generate_next_path(ax)
        self.play(Create(self.simulation_graphs[-1], rate_func=linear), run_time=2.0)

        # right: histogram of option profit
        bars = BarChart(
            values=[0.0] * len(self.histogram_counts),
            bar_names=[fr"\${5 * i}" if i % 2 == 0 else "" for i in range(len(self.histogram_counts))],
            y_range=[0, 1.01, 0.25],
            bar_colors=[BLUE],
            x_length=4,
            y_length=4,
            x_axis_config={"font_size": 30}
        ).to_edge(RIGHT, buff=1.0)
        bar_labels = bars.get_axis_labels(x_label=Tex(r"\text{Option Profit}", font_size=30),
                                          y_label=Tex(r"\text{Frequency}", font_size=30))

        self.play(Create(bars), Write(bar_labels), run_time=2.0)
        self.wait(1.0)

        self.play(bars.animate.change_bar_values([x / sum(self.histogram_counts) for x in self.histogram_counts]))
        self.wait(1.0)

        # ~550 paths over 5.3 seconds, exponentially decaying
        decay_curve = 0.25 * np.exp(-np.linspace(0, 4, 50))
        schedule = [(1, t) if t >= 1 / 60 else (int(np.ceil(1 / 60 / t)), 1 / 60)
                    for t in decay_curve]
        schedule += [schedule[-1]] * 120

        # add new paths, faster and faster
        for num_paths_this_tick, run_time in schedule:
            assert run_time >= 1 / 60

            # dim prior paths, generate new paths, update histogram
            self.play(*[
                self.simulation_graphs[-idx].animate.set_stroke(opacity=min(0.1, 1.0 / len(self.simulation_paths)))
                for idx in range(1, num_paths_this_tick + 1)], run_time=run_time)
            for _ in range(num_paths_this_tick):
                self.generate_next_path(ax)

            self.play(*[Create(self.simulation_graphs[-idx], rate_func=linear)
                        for idx in range(1, num_paths_this_tick + 1)],
                      bars.animate.change_bar_values([x / sum(self.histogram_counts) for x in self.histogram_counts]),
                      run_time=run_time)
        else:
            # dim final paths
            self.play(*[
                self.simulation_graphs[-idx].animate.set_stroke(opacity=min(0.1, 1.0 / len(self.simulation_paths)))
                for idx in range(1, num_paths_this_tick + 1)], run_time=run_time)

        self.wait(1.0)

        # TODO: plot vertical line for average profit
