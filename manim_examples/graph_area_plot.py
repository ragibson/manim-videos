from manim import *


class GraphAreaPlot(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 5], y_range=[0, 6],
            x_axis_config={"numbers_to_include": [2, 3]},
            tips=False
        )
        labels = ax.get_axis_labels()

        curve1 = ax.plot(lambda x: 4 * x - x ** 2, x_range=[0, 4], color=BLUE_C)
        curve2 = ax.plot(
            lambda x: 0.8 * x ** 2 - 3 * x + 4,
            x_range=[0, 4],
            color=GREEN_B
        )

        line1 = ax.get_vertical_line(ax.i2gp(2, curve1), color=YELLOW)
        line2 = ax.get_vertical_line(ax.i2gp(3, curve1), color=YELLOW)

        riemann_area = ax.get_riemann_rectangles(curve1, x_range=[0.3, 0.6], dx=0.03,
                                                 color=BLUE, fill_opacity=0.5)
        area = ax.get_area(curve2, [2, 3], bounded_graph=curve1, color=GREY, opacity=0.5)

        self.add(ax, labels, curve1, curve2, line1, line2, riemann_area, area)
