from manim import *

from data import OCC_options_ADV  # noqa


class BlackScholesIntroduction(Scene):
    def play_BSM_title(self):
        title = Text("1973: Black-Scholes-Merton Formula for Pricing Options", font_size=36, t2c={"1973": YELLOW})
        title.to_edge(UP, buff=0.5)

        self.play(Write(title))
        self.wait(1.0)
        return title  # need to FadeOut later

    def play_author_images(self):
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

        self.play(FadeOut(images), FadeOut(labels))

    def play_nobel_prize(self):
        # adding in image of the Nobel Prize medal
        nobel_image = ImageMobject("licensed_images/Nobel_Prize.png")
        nobel_image.height = 3.0

        self.play(FadeIn(nobel_image, run_time=0.5))
        self.wait(1.0)
        return nobel_image  # going to want to shift this while OCC volume plot is being drawn

    def play_OCC_volume_plot(self, title, nobel_image):
        # setting up axes and plot for OCC options daily volume
        axes = Axes(
            x_range=[1973, 2025, 4], y_range=[0, 60_000_000, 10_000_000],
            x_length=10, y_length=4.5, tips=False,
            axis_config={"include_numbers": True, "font_size": 24},
            x_axis_config={
                "include_numbers": [1973, 1975, 1980, 1985, 1990, 1995, 2000, 2005, 2010, 2015, 2020, 2025],
                "decimal_number_config": {
                    "group_with_commas": False,  # these are years, so no commas
                    "num_decimal_places": 0
                }
            }
        )
        axes.next_to(title, DOWN, buff=1.0)
        x_label, y_label = axes.get_axis_labels(x_label=r"\text{Year}", y_label=r"\text{Average Daily Trading Volume}")

        graph = axes.plot_line_graph(
            x_values=list(OCC_options_ADV.keys()),
            y_values=list(OCC_options_ADV.values()),
            add_vertex_dots=False, line_color=YELLOW, stroke_width=2
        )

        self.play(
            Write(y_label),  # using this as kind of a slide header
            nobel_image.animate.shift(LEFT * 1.0),
            Create(axes, run_time=2.0), Write(x_label),
            Create(graph, run_time=2.0)
        )
        self.wait(2.0)
        return axes, graph, x_label, y_label

    def construct(self):
        BSM_title = self.play_BSM_title()
        self.play_author_images()
        nobel_image = self.play_nobel_prize()
        OCC_components = self.play_OCC_volume_plot(BSM_title, nobel_image)
        self.play(*[FadeOut(x) for x in (BSM_title, nobel_image) + OCC_components])
