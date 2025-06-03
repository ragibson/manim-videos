from manim import *


def simple_stock_simulation(start_price=100, sigma=0.15, dt=1 / 252, T=1, seed=0):
    np.random.seed(seed)
    n_steps = int(T / dt)
    increments = np.random.normal(0, sigma * np.sqrt(dt), n_steps)
    prices = start_price * np.exp(np.cumsum(increments))  # ignoring drift
    return prices


class WhatIsAStock(Scene):
    def construct(self):
        # company visualized as grid of blocks (to represent shares)
        company_blocks = VGroup([
            Square(side_length=0.4, color=BLUE, fill_opacity=0.7).shift(RIGHT * j * 0.4 + UP * i * 0.4)
            for i in range(3) for j in range(4)
        ])
        company_blocks.move_to(ORIGIN)
        company_label = Text("Company", font_size=24).next_to(company_blocks, DOWN, buff=0.3)

        # company's product shown above the company
        company_product = Triangle(radius=0.3, color=ORANGE, fill_opacity=0.7)
        company_product.move_to(company_blocks.get_center() + UP * 1)

        self.play(FadeIn(company_blocks), FadeIn(company_label))
        self.wait(1.0)

        # breaking off one of the shares of the company, moving to left
        share_block = company_blocks[0].copy()
        share_block.set_color(RED)
        share_label = Text("Share", font_size=24)

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
        customer_label = Text("Customer", font_size=24).next_to(customer, DOWN, buff=0.3)
        customer_label.align_to(company_label, DOWN)

        customer_money = VGroup([
            Text("$", font_size=24, color=YELLOW).move_to(customer.get_center() + RIGHT * (i - 1) * 0.2)
            for i in range(3)
        ])
        self.play(FadeIn(company_product))
        self.wait(1.0)
        self.play(FadeIn(customer), FadeIn(customer_label))
        self.wait(1.0)
        self.play(FadeIn(customer_money))

        # exchanging money <-> product
        self.play(
            customer_money.animate.move_to(company_blocks.get_center()),
            company_product.animate.move_to(customer.get_center() + 1.5 * customer.radius * UP)
        )
        self.wait(1.0)

        # moving a tiny amount of the profit to the share on the left
        profit_money = Text("$", font_size=20, color=YELLOW)
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
