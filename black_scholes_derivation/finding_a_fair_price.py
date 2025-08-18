from shared_data_and_functions import *


class GuessingTheFuture(Scene):
    def construct(self):
        display_section_title(self, "fair price for an option?")

        future_quote = MarkupText(f'"An option is ... '
                                  f'on a specific date <span foreground="{BLUE}">in the future</span>."',
                                  font_size=TEXT_SIZE_MEDIUM).to_edge(UP, buff=0.5)
        self.play(Write(future_quote))
        self.wait(2.0)

        how_to_text = (MarkupText(fr'<span foreground="{YELLOW}">Exercise #1:</span> '
                                  'How could you find a fair price for this?', font_size=TEXT_SIZE_MEDIUM)
                       .next_to(future_quote, DOWN, buff=0.5))
        self.play(Write(how_to_text))
        self.wait(5.0)

        ax, labels, simulated_path, graph, strike_line = stock_price_to_today(how_to_text)
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

        simulate_text = (Text("Simulate!", font_size=TEXT_SIZE_MEDIUM, color=YELLOW)
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
        ax, labels, strike_line = stock_price_simulation_graph()
        self.play(Create(ax), Write(labels), Create(strike_line, rate_func=linear), run_time=1.0)
        self.wait(1.0)

        self.generate_next_path(ax)
        self.play(Create(self.simulation_graphs[-1], rate_func=linear), run_time=1.0)

        # right: histogram of option profit
        bar_chart = BarChart(
            values=[0.0] * len(self.histogram_counts),
            bar_names=[fr"\${5 * i}" if i % 2 == 0 else "" for i in range(len(self.histogram_counts))],
            y_range=[0, 1.01, 0.25],
            bar_colors=[BLUE],
            x_length=4,
            y_length=4,
            x_axis_config={"font_size": 30}
        ).to_edge(RIGHT, buff=1.0)
        bar_labels = bar_chart.get_axis_labels(x_label=Tex(r"\text{Option Profit}", font_size=TEXT_SIZE_XSMALL),
                                               y_label=Tex(r"\text{Frequency}", font_size=TEXT_SIZE_XSMALL))

        self.play(Create(bar_chart), Write(bar_labels), run_time=2.0)
        self.wait(1.0)

        self.play(bar_chart.animate.change_bar_values([x / sum(self.histogram_counts) for x in self.histogram_counts]))
        self.wait(1.0)

        # ~550 paths over 5.3 seconds, exponentially decaying
        decay_curve = 0.25 * np.exp(-np.linspace(0, 4, 50))
        schedule = [(1, t) if t >= 1 / 60 else (int(np.ceil(1 / 60 / t)), 1 / 60)
                    for t in decay_curve]
        schedule += [schedule[-1]] * 120
        path_opacity = lambda: min(0.2, max(0.005, 1.0 / len(self.simulation_paths)))

        # add new paths, faster and faster
        for num_paths_this_tick, run_time in schedule:
            assert run_time >= 1 / 60

            # dim prior paths, generate new paths, update histogram
            self.play(*[
                self.simulation_graphs[-idx].animate.set_stroke(opacity=path_opacity())
                for idx in range(1, num_paths_this_tick + 1)], run_time=run_time)
            for _ in range(num_paths_this_tick):
                self.generate_next_path(ax)

            self.play(
                *[Create(self.simulation_graphs[-idx], rate_func=linear) for idx in range(1, num_paths_this_tick + 1)],
                bar_chart.animate.change_bar_values([x / sum(self.histogram_counts) for x in self.histogram_counts]),
                run_time=run_time
            )
        else:
            # dim final paths
            self.play(*[
                self.simulation_graphs[-idx].animate.set_stroke(opacity=path_opacity())
                for idx in range(1, num_paths_this_tick + 1)], run_time=run_time)

        self.wait(1.0)

        # highlight the histogram bars in a left-to-right sweep before we plot the average profit
        # this use of Succession requires an undocumented conversion of _AnimationBuilder to Animations
        self.play(LaggedStart(*[Succession(bar.animate.set_color(YELLOW).build(),
                                           bar.animate.set_color(BLUE).build())
                                for bar in bar_chart.bars], run_time=1.0, lag_ratio=0.1))

        # plot a vertical line at the average profit
        average_profit = np.mean([max(0, sim[-1] - 300) for sim in self.simulation_paths])
        # division by 5 in the c2p is needed to account for each bar being $5 wide
        average_profit_line = DashedLine(bar_chart.c2p(average_profit / 5, 0),
                                         bar_chart.c2p(average_profit / 5, 1.0),
                                         color=YELLOW, z_index=2)
        self.play(Create(average_profit_line, rate_func=linear))

        profit_text = (
            Tex(fr"\text{{Average:}} ${{\sim}}\${average_profit:.0f}$", font_size=TEXT_SIZE_MEDIUM, color=YELLOW)
            .next_to(average_profit_line.get_top(), aligned_edge=LEFT, buff=0.25)
            .shift(DOWN * 0.25))
        self.play(Create(profit_text, run_time=1.0))
        self.wait(1.0)

        self.play(*[FadeOut(x) for x in [ax, labels, strike_line] + self.simulation_graphs
                    + [bar_chart, bar_labels, average_profit_line, profit_text]])
