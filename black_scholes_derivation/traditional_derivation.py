from manim import *


class BlackScholesTraditional(Scene):
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
        topics.to_edge(LEFT, buff=1.0)
        topics.shift(DOWN * 0.5)

        # "complicated looking" math on the right side
        math_exprs = VGroup(
            MathTex(r"\mathbb{E}[X], \quad N\left(\mu, \sigma^2\right), \quad "
                    r"F(x) = \int_{-\infty}^x f(x)\, \text{d}t", font_size=32),
            MathTex(r"\Pi = \Delta S - V", font_size=32),
            MathTex(r"dS = \mu S dt + \sigma S dW_t", font_size=32),
            MathTex(r"\frac{\partial V}{\partial t} + \frac{1}{2} \sigma^2 S^2 \frac{\partial^2 V}{\partial S^2} "
                    r"+ r S \frac{\partial V}{\partial S} - rV = 0", font_size=32)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.75)
        math_exprs.next_to(topics, RIGHT, buff=1.0)

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
