from manim import *

from shared_data_and_functions import *


class WhatIsAStock(Scene):
    def construct(self):
        # company visualized as grid of blocks (to represent shares)
        company_blocks = VGroup([
            Square(side_length=0.4, color=BLUE, fill_opacity=0.7).shift(RIGHT * j * 0.4 + UP * i * 0.4)
            for i in range(3) for j in range(4)
        ])
        company_blocks.move_to(ORIGIN)
        company_label = Text("Company", font_size=TEXT_SIZE_MEDIUM).next_to(company_blocks, DOWN, buff=0.3)

        # company's product shown above the company
        company_product = Triangle(radius=0.3, color=ORANGE, fill_opacity=0.7)
        company_product.move_to(company_blocks.get_center() + UP * 1)

        self.play(FadeIn(company_blocks), FadeIn(company_label))
        self.wait(1.0)

        # breaking off one of the shares of the company, moving to left
        share_block = company_blocks[0].copy()
        share_block.set_color(RED)
        share_label = Text("Share (Stock)", font_size=TEXT_SIZE_MEDIUM)

        self.play(
            share_block.animate.move_to(LEFT * 4).align_to(company_blocks, DOWN),
            company_blocks[0].animate.set_opacity(0.3)
        )
        share_label.next_to(share_block, DOWN, buff=0.3)
        self.play(FadeIn(share_label))
        self.wait(1.0)

        # customer over on the right, will buy the product in exchange for money
        customer = Circle(radius=0.5, color=GREEN, fill_opacity=0.7)
        customer.shift(RIGHT * 4)
        customer.align_to(company_blocks, DOWN)
        customer_label = Text("Customer", font_size=TEXT_SIZE_MEDIUM).next_to(customer, DOWN, buff=0.3)
        customer_label.align_to(company_label, DOWN)

        customer_money = VGroup([
            Text("$", font_size=TEXT_SIZE_SMALL, color=YELLOW).move_to(customer.get_center() + RIGHT * (i - 1) * 0.2)
            for i in range(3)
        ])
        self.play(FadeIn(company_product))
        self.wait(1.0)
        self.play(FadeIn(customer), FadeIn(customer_label), FadeIn(customer_money))
        self.wait(1.0)

        # exchanging money <-> product
        self.play(
            customer_money.animate.move_to(company_blocks.get_center()),
            company_product.animate.move_to(customer.get_center() + 1.5 * customer.radius * UP)
        )
        self.wait(1.0)

        # moving a tiny amount of the profit to the share on the left
        profit_money = Text("$", font_size=TEXT_SIZE_XSMALL, color=YELLOW)
        profit_money.move_to(customer_money[0].get_center())
        self.play(
            Transform(customer_money[0], profit_money),
            profit_money.animate.move_to(share_block.get_center())
        )
        self.wait(1.0)

        # flashing the share block to emphasize the value
        self.play(
            share_block.animate.set_stroke(color=YELLOW, width=3),
            Flash(share_block, color=YELLOW)
        )
        self.wait(2.0)

        self.play(FadeOut(company_blocks), FadeOut(company_label), FadeOut(share_block), FadeOut(share_label),
                  FadeOut(company_product), FadeOut(customer), FadeOut(customer_label), FadeOut(customer_money),
                  FadeOut(profit_money))


class StockSimulation(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 1.01, 0.25],
            y_range=[80, 120.1, 10],
            x_length=8,
            y_length=6,
            axis_config={"include_numbers": True},
            y_axis_config={"include_numbers": False},
            tips=False
        ).to_edge(DOWN)

        # HACK: manually adding in dollar signs on the left of the y-axis label numbers
        ax.y_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.y_range)})

        labels = ax.get_axis_labels(x_label=r"\text{Time (years)}", y_label=r"\text{Stock Price}")
        self.play(Create(ax[1]), Write(labels[1]))

        # first, let's draw a flat line to describe what a price even means -- buyers and sellers basically "agree" on
        # a price, people are willing to buy at ~$100 and others are willing to sell at that price
        flat_price = ax.plot_line_graph(
            x_values=np.linspace(0, 0.1, 10),
            y_values=100 * np.ones(10),
            line_color=BLUE,
            add_vertex_dots=False
        )
        self.play(FadeIn(flat_price, run_time=0.5, rate_func=linear))
        self.wait(1.0)
        for _ in range(2):
            self.play(flat_price.animate.shift(UP * 0.1), run_time=0.25, rate_func=rush_from)
            self.play(flat_price.animate.shift(DOWN * 0.1), run_time=0.25, rate_func=rush_from)
        self.wait(1.0)
        for _ in range(2):
            self.play(flat_price.animate.shift(DOWN * 0.1), run_time=0.25, rate_func=rush_from)
            self.play(flat_price.animate.shift(UP * 0.1), run_time=0.25, rate_func=rush_from)
        self.play(FadeOut(flat_price))

        # now include time dimension and simulation
        simulated_path = simple_stock_simulation(start_price=100, sigma=0.15, seed=10)
        graph = ax.plot_line_graph(
            x_values=np.linspace(0, 1, len(simulated_path)),
            y_values=simulated_path,
            line_color=BLUE,
            add_vertex_dots=False
        )
        self.play(Create(ax[0]), Write(labels[0]))
        self.play(Create(graph, run_time=2.0, rate_func=linear))
        self.wait(1.0)

        # add in example history for Netflix, all of these prices are publicly available (pretty much)
        # you can own about two billionths of the company for the low price of $1300 :D
        # I'm just plopping this over the graph, it's a bit awkward but seems alright?
        netflix_example = ImageMobject("stock_history_examples/NFLX.png")
        netflix_example.height = 4.0
        self.play(FadeIn(netflix_example))
        self.wait(4.0)

        self.play(*[FadeOut(x) for x in (ax, labels, graph, netflix_example)])


class WhatIsAnOption(Scene):
    def written_description(self):
        lines = [
            f'An option is a contract that:',
            f'• gives you the <span foreground="{YELLOW}">option</span> to buy a stock',
            f'• at a <span foreground="{GREEN}">predetermined price</span> (the "strike price")',
            f'• on a <span foreground="{BLUE}">specific date</span> in the future.<sup>*</sup>'
        ]

        option_definition_lines = (VGroup(*[MarkupText(line, font_size=TEXT_SIZE_MEDIUM) for line in lines])
                                   .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
                                   .to_edge(UP))
        footnote = Tex(r"$^*$Technically, this specific type is called a ``European call option''.",
                       font_size=TEXT_SIZE_TINY)
        footnote.to_edge(DOWN, buff=0.25).align_to(option_definition_lines, LEFT)

        for line in option_definition_lines[:-1]:
            self.wait(0.5)
            self.play(Write(line))
        self.play(Write(option_definition_lines[-1]))
        self.play(FadeIn(footnote))
        self.wait(2.0)

        # briefly mention standard financial-ese here on the right but not the obligation
        alternate_line2 = MarkupText(
            f'• gives you the <span foreground="{YELLOW}">right, but not the obligation,</span> to buy a stock',
            font_size=TEXT_SIZE_MEDIUM_SMALL
        )
        alternate_line2.move_to(option_definition_lines[1].get_left(), aligned_edge=LEFT)
        original_line2 = option_definition_lines[1].copy()
        self.play(Transform(option_definition_lines[1], alternate_line2))
        self.wait(2.0)
        self.play(Transform(option_definition_lines[1], original_line2))
        self.wait(2.0)

        return option_definition_lines, footnote

    def written_example(self, option_definition_lines, footnote):
        # example to make things a bit more concrete
        example_text = (MarkupText("Example: ", font_size=TEXT_SIZE_SMALL)
                        .next_to(option_definition_lines.get_bottom(), DOWN, buff=1.0)
                        .to_edge(LEFT, buff=0.5))
        example_body = MarkupText(
            f'You buy an <span foreground="{YELLOW}">option to buy 1 share</span> of Apple\'s stock\n'
            f'<span foreground="{GREEN}">for $300</span> in '
            f'<span foreground="{BLUE}">3 months</span>.',
            font_size=TEXT_SIZE_SMALL
        ).next_to(example_text, RIGHT, buff=0.25).align_to(example_text, UP)
        self.play(Write(example_text), run_time=0.25)
        self.play(FadeOut(footnote), Write(example_body))

        # two cases to show off asymmetry
        lines = [
            f'• If Apple\'s stock increases to $325, you make $25!',
            f'• If Apple\'s stock falls to $275, you make nothing.',
        ]
        example_lines = (VGroup(*[MarkupText(line, font_size=TEXT_SIZE_SMALL) for line in lines])
                         .arrange(DOWN, aligned_edge=LEFT, buff=0.25)
                         .next_to(example_body, DOWN, buff=0.25)
                         .align_to(option_definition_lines, LEFT))
        for line in example_lines:
            self.play(Write(line))
            self.wait(1.0)
        self.wait(1.0)

        example_block = VGroup(example_text, example_body, example_lines)
        return example_block

    def payoff_diagram(self, example_block):
        ax = Axes(
            x_range=[260, 340.1, 10], y_range=[-20, 40.1, 10],
            x_length=6,
            y_length=4.25,
            axis_config={"include_numbers": False, "font_size": 28, "numbers_to_exclude": [300]},
            x_axis_config={"label_direction": UP},
            y_axis_config={"include_numbers": False},
            tips=False
        ).to_edge(DOWN, buff=0.25)

        # HACK: manually force tick labels to include dollar signs
        x_line = ax.x_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.x_range) if i != 300})
        y_line = ax.y_axis.add_labels({i: fr"\${i:.0f}" if i >= 0 else fr"-\${abs(i):.0f}"
                                       for i in np.arange(*ax.y_range) if i != 0})
        x_line.labels.set_stroke(BLACK, width=4.0, background=True).set_z_index(2)  # for visibility on overlap
        y_line.labels.set_stroke(BLACK, width=4.0, background=True).set_z_index(2)

        # plot the actual payoff, ignoring premium for now
        # need to do this before shifting the axis
        left_side = ax.plot_line_graph(
            x_values=np.linspace(300, 260, 10),
            y_values=0 * np.ones(10),
            line_color=BLUE, add_vertex_dots=False, z_index=1
        )
        right_side = ax.plot_line_graph(
            x_values=np.linspace(300, 340, 10),
            y_values=np.linspace(0, 40, 10),
            line_color=BLUE, add_vertex_dots=False, z_index=1
        )

        # brace and text for the premium, again needed before the axis shift
        option_premium_brace = (BraceBetweenPoints(ax.c2p(275, -9 / 0.5), ax.c2p(275, -0.5),
                                                   direction=LEFT, z_index=3)
                                .scale(0.5).move_to(ax.c2p(275, -0.5), aligned_edge=UP))
        option_premium_text = Tex(r"\text{Option Price (``Premium'')}", font_size=TEXT_SIZE_MEDIUM)
        option_premium_text.next_to(option_premium_brace, LEFT, buff=0.1)

        # (manually) centering y-axis at $300 instead of $0
        # probably there was a better way to do this
        ax.get_axes()[1].shift(ax.c2p(300, 0) - ax.c2p(ax.x_range[0], 0))
        labels = ax.get_axis_labels(x_label=Tex(r"\text{Final Stock Price}", font_size=TEXT_SIZE_MEDIUM, z_index=4),
                                    y_label=Tex(r"\text{Option Profit}", font_size=TEXT_SIZE_MEDIUM, z_index=4))
        labels.shift(DOWN * 0.25)

        self.play(Create(ax), Create(labels))
        self.wait(5.0)

        # emphasizing the part of the example corresponding to the left vs. right side while plotting
        example_profit, example_worthless = example_block[-1]
        self.play(LaggedStart(ApplyWave(example_profit, rate_func=linear, ripples=2, amplitude=0.1),
                              Create(right_side, rate_func=linear, run_time=2.0), lag_ratio=0.25))
        self.wait(1.0)
        self.play(LaggedStart(ApplyWave(example_worthless, rate_func=linear, ripples=2, amplitude=0.1),
                              Create(left_side, rate_func=linear, run_time=2.0), lag_ratio=0.25))
        self.wait(1.0)

        # adding in the premium
        self.play(left_side.animate.shift(ax.c2p(0, -10) - ax.c2p(0, 0)),
                  right_side.animate.shift(ax.c2p(0, -10) - ax.c2p(0, 0)))
        self.play(FadeIn(option_premium_brace), FadeIn(option_premium_text))
        self.wait(3.0)

        self.play(*[FadeOut(x) for x in (ax, labels, left_side, right_side,
                                         option_premium_brace, option_premium_text, example_block)])

    def construct(self):
        option_definition_lines, footnote = self.written_description()
        example_block = self.written_example(option_definition_lines, footnote)

        # moving the example up to make room for a payoff diagram
        self.play(FadeOut(option_definition_lines), example_block.animate.to_edge(UP))
        self.wait(1.0)

        self.payoff_diagram(example_block)
