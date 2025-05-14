from manim import *

from data import OCC_options_ADV  # noqa


# TODO: also want "title card" style animation at the beginning

class BlackScholesIntroduction(Scene):
    def slide1(self):
        title = Text("1973: Black-Scholes-Merton Formula", font_size=48, t2c={"1973": YELLOW})
        title.to_edge(UP, buff=0.5)

        self.play(Write(title))
        self.wait(1)

        # black, scholes, merton images
        black_img = ImageMobject("licensed_images/Fischer_Black_cropped.jpg")
        scholes_img = ImageMobject("licensed_images/Myron_Scholes_2008_in_Lindau.jpg")
        merton_img = ImageMobject("licensed_images/Robert_Merton_November_2010_03_resized.jpg")

        for im in [black_img, scholes_img, merton_img]:
            im.height = 5.0

        images = Group(black_img, scholes_img, merton_img).arrange(RIGHT, buff=1.0)

        # names beneath the images
        labels = VGroup(
            Text("Fischer Black", font_size=40),
            Text("Myron Scholes", font_size=40),
            Text("Robert Merton", font_size=40)
        )
        for i, label in enumerate(labels):
            label.next_to(images[i], DOWN, buff=0.3)

        for i in range(len(images)):
            self.play(FadeIn(images[i]), FadeIn(labels[i]))
            self.wait(0.5)

        self.play(FadeOut(images), FadeOut(labels), FadeOut(title))

    def slide2(self):
        # setting up axes and plot for OCC options daily volume
        axes = Axes(
            x_range=[1973, 2025, 4], y_range=[0, 60_000_000, 10_000_000],
            x_length=10, y_length=6, tips=False,
            axis_config={"include_numbers": True, "font_size": 24},
            x_axis_config={"include_numbers": [1973, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025]}
        )
        x_label, y_label = axes.get_axis_labels(x_label=r"\text{Year}", y_label=r"\text{Average Daily Trading Volume}")

        graph = axes.plot_line_graph(
            x_values=list(OCC_options_ADV.keys()),
            y_values=list(OCC_options_ADV.values()),
            add_vertex_dots=False, line_color=YELLOW, stroke_width=2
        )

        self.play(Write(y_label))  # using this as kind of a slide header
        self.play(Create(axes, run_time=4.0), Write(x_label))
        self.play(Create(graph), run_time=4.0)
        self.wait(2.0)

        # adding in image of the Nobel Prize medal
        nobel_image = ImageMobject("licensed_images/Nobel_Prize.png")
        nobel_image.height = 3.0
        nobel_image.shift(LEFT * 2.0 + UP * 1.0)

        self.play(FadeIn(nobel_image))
        self.wait(1.0)

    def construct(self):
        # TODO: actually rename this functions into something meaningful
        self.slide1()
        self.slide2()
