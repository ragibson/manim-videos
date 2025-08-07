from manim import *
from scipy.stats import norm

# just hardcoding this data here, as of May 10, 2025
# from https://www.theocc.com/market-data/market-data-reports/volume-and-open-interest/historical-volume-statistics
OCC_options_ADV = {1973: 6470, 1974: 22462, 1975: 71553, 1976: 127960, 1977: 157291, 1978: 227107, 1979: 254011,
                   1980: 382326, 1981: 432434, 1982: 543394, 1983: 593107, 1984: 776432, 1985: 924248, 1986: 1143127,
                   1987: 1206201, 1988: 774501, 1989: 900860, 1990: 829734, 1991: 785777, 1992: 795259, 1993: 919614,
                   1994: 1116597, 1995: 1140068, 1996: 1160621, 1997: 1398510, 1998: 1612473, 1999: 2015442,
                   2000: 2883841, 2001: 3150250, 2002: 3105746, 2003: 3612900, 2004: 4699648, 2005: 5992132,
                   2006: 8079074, 2007: 11405682, 2008: 14160366, 2009: 14335861, 2010: 15472495, 2011: 18106144,
                   2012: 15888378, 2013: 16314586, 2014: 16926067, 2015: 16443005, 2016: 16123905, 2017: 16691422,
                   2018: 20466938, 2019: 19440621, 2020: 29513935, 2021: 39167335, 2022: 41117424, 2023: 44207806,
                   2024: 48508840, 2025: 58971333}

# I thought this would be helpful for text size consistency across the scripts but frankly there are enough exceptions
# that it wasn't particularly useful. TEXT_SIZE_MEDIUM is a similar size to math mode MATH_SIZE_MEDIUM.
TEXT_SIZE_TINY = 24
TEXT_SIZE_XSMALL = 28
TEXT_SIZE_SMALL = 32
TEXT_SIZE_MEDIUM_SMALL = 34
TEXT_SIZE_MEDIUM = 36
TEXT_SIZE_LARGE = 40

MATH_SIZE_TINY = 32
MATH_SIZE_XSMALL = 36
MATH_SIZE_SMALL = 42
MATH_SIZE_MEDIUM = 46

# used for extremely simple section breaks
TITLES, TITLE_HIGHLIGHTS = [
    "What is a stock? What is an option?",
    "How would you assign a fair price for an option?",
    "Making things fully analytical",
    "Visualizing our pricing formula",
    "6 exercises throughout (with hints and solutions!)"
], ["option", "fair price", "analytical", "Visualizing", "exercises"]


def display_section_title(scene, section_shorthand):
    idx = [i for i, s in enumerate(TITLES) if section_shorthand in s][0]
    title = (Text(TITLES[idx], font_size=TEXT_SIZE_LARGE, t2c={TITLE_HIGHLIGHTS[idx]: YELLOW})
             .move_to(ORIGIN))
    scene.play(FadeIn(title))
    scene.wait(2.0)
    scene.play(FadeOut(title))


def simple_stock_simulation(start_price=100, sigma=0.15, dt=1 / 252, T=1, seed=0):
    np.random.seed(seed)
    n_steps = int(T / dt)
    increments = np.random.normal(0, sigma * np.sqrt(dt), n_steps)
    increments[0] = 0.0  # want t0 exactly at the start price
    prices = start_price * np.exp(np.cumsum(increments) - (sigma ** 2 / 2) * dt * np.arange(n_steps))
    return prices


def stock_price_to_today(header_object, sigma=0.15):
    """Plot stock price graph up to today, leaving the second half of the graph empty."""
    # add in stock price graph
    ax = Axes(
        x_range=[0, 1.01, 0.25],
        y_range=[225, 375.1, 25],
        x_length=8,
        y_length=4,
        axis_config={"include_numbers": False},
        tips=False
    ).next_to(header_object, DOWN, buff=1.0)

    # HACK: manually adding in dollar signs on the left of the y-axis label numbers
    ax.y_axis.add_labels({i: fr"\${i:.0f}" for i in np.arange(*ax.y_range)})
    ax.x_axis.add_labels({0.5: "Today"})
    labels = ax.get_axis_labels(x_label=r"\text{Time}", y_label=r"\text{Stock Price}")

    # plot first just up to "today" (internally, t=0.5)
    simulated_path = simple_stock_simulation(start_price=300, sigma=sigma, seed=10, T=0.5)
    graph = ax.plot_line_graph(
        x_values=np.linspace(0, 0.5, len(simulated_path)),
        y_values=simulated_path,
        line_color=BLUE,
        add_vertex_dots=False
    )
    strike_line = DashedLine(ax.c2p(0.0, 300), ax.c2p(1.0, 300))

    return ax, labels, simulated_path, graph, strike_line


def stock_price_simulation_graph(stock_price_range=(250, 350.1, 25), strike=300, shift_amt=0.0 * DOWN):
    """Create a graph for showing many simulated stock prices on the left side of the screen."""
    ax = Axes(
        x_range=[0, 0.251, 0.05],
        y_range=stock_price_range,
        x_length=4,
        y_length=4,
        x_axis_config={"include_numbers": True},
        axis_config={"include_numbers": False},
        tips=False
    ).to_edge(LEFT, buff=1.0).shift(shift_amt)

    # HACK: manually adding in dollar signs on the left of the y-axis label numbers
    ax.y_axis.add_labels({i: Tex(fr"\${i:.0f}", font_size=TEXT_SIZE_XSMALL) for i in np.arange(*ax.y_range)})
    labels = ax.get_axis_labels(x_label=Tex(r"\text{Time (years)}", font_size=TEXT_SIZE_XSMALL),
                                y_label=Tex(r"\text{Stock Price}", font_size=TEXT_SIZE_XSMALL))

    strike_line = DashedLine(ax.c2p(0.0, strike), ax.c2p(0.25, strike))
    return ax, labels, strike_line


def black_scholes_price(S0, K, sigma, t, r):
    D = np.exp(-r * t)
    d_plus = (np.log(S0 / D / K) + sigma ** 2 * t / 2) / (sigma * np.sqrt(t))
    d_minus = d_plus - sigma * np.sqrt(t)
    return D * (S0 / D * norm.cdf(d_plus) - K * norm.cdf(d_minus))
