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
            Create(graph, run_time=2.0, rate_func=linear)
        )
        self.wait(2.0)
        return axes, graph, x_label, y_label

    def construct(self):
        BSM_title = self.play_BSM_title()
        self.play_author_images()
        nobel_image = self.play_nobel_prize()
        OCC_components = self.play_OCC_volume_plot(BSM_title, nobel_image)
        self.play(*[FadeOut(x) for x in (BSM_title, nobel_image) + OCC_components])


class BlackScholesTraditionalDerivation(Scene):
    def construct(self):
        title = Text("Traditional Derivation is Complicated!", font_size=40, t2c={"Complicated!": RED})
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # bullet points of topics
        topics = VGroup(  # probably could've used BulletedList here
            Text("• Basic Probability & Statistics", font_size=32),
            Text("• Portfolio Hedging", font_size=32),
            Text("• Stochastic Calculus", font_size=32),
            Text("• Partial Differential Equations", font_size=32),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        topics.to_edge(LEFT, buff=0.5)
        topics.shift(DOWN * 0.5)

        # "complicated looking" math on the right side
        math_exprs = VGroup(
            MathTex(r"\mathbb{E}[X], \quad N\left(\mu, \sigma^2\right), \quad "
                    r"F(x) = \int_{-\infty}^x f(x)\, \text{d}x", font_size=32),
            MathTex(r"\Pi = \Delta S - V", font_size=32),
            MathTex(r"dS = \mu S dt + \sigma S dW_t", font_size=32),
            MathTex(r"\frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} "
                    r"+ r S \frac{\partial V}{\partial S} - rV = 0", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        math_exprs.next_to(topics, RIGHT, buff=1.0)
        math_exprs.to_edge(RIGHT, buff=0.5)

        for text, expr in zip(topics, math_exprs):
            # topics moving ->, expressions moving <-
            self.play(FadeIn(text, shift=RIGHT), FadeIn(expr, shift=LEFT))
            self.wait(0.5)
        self.wait(1.5)

        # cross marks through everything except probability & statistics
        xmarks = VGroup([Cross(topics[i], color=RED, stroke_width=6) for i in range(1, len(topics))]
                        + [Cross(math_exprs[i], color=RED, stroke_width=6) for i in range(1, len(topics))])

        # going to transform selected words in title to switch to simpler derivation
        first_word = title[0:len("Traditional")]
        new_first_word = Text("Alternate", font_size=40).next_to(first_word.get_right(), LEFT, buff=0.0)
        last_word = title[-len("Complicated!"):]
        new_last_word = Text("Simpler!", font_size=40, t2c={"Simpler!": GREEN}).next_to(last_word.get_left(), RIGHT,
                                                                                        buff=0.0)
        self.play(
            *[Create(cross, run_time=2.0) for cross in xmarks],
            topics[0].animate(run_time=0.5).set_color(GREEN),
            math_exprs[0].animate(run_time=0.5).set_color(GREEN),
            Transform(first_word, new_first_word, run_time=0.5),
            Transform(last_word, new_last_word, run_time=0.5)
        )
        self.wait(2.0)

        self.play(FadeOut(topics), FadeOut(math_exprs), FadeOut(xmarks), FadeOut(title))
        self.wait(1.0)


class LookingAhead(Scene):
    def construct(self):
        title = Text('Looking Ahead: "Pricing an Option"', font_size=40, t2c={'"Pricing an Option"': BLUE})
        title.to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # bullet points of topics
        topics = VGroup(  # probably could've used BulletedList here
            Text("• What is a stock? What is an option?", font_size=36, t2c={"option": YELLOW}),
            Text("• How would you assign a fair price for an option?", font_size=36, t2c={"fair price": YELLOW}),
            Text("• Making things fully analytical", font_size=36, t2c={"analytical": YELLOW})
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        topics.to_edge(LEFT, buff=1.0)

        for t in topics:
            self.play(FadeIn(t))
            self.wait(0.5)

        self.play(FadeOut(topics), FadeOut(title))
