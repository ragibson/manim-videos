# Can You Price Options with Just Basic Statistics? A Simple Black-Scholes Pricing Derivation

(This script is mostly what's in the video along with some notes on what parts of the animation are shown at each
point. I self-edited on the fly at a few places, so it's a little different from the final result but should be quite
close overall.)

## introduction.py

(Screen shows "1973: Black-Scholes-Merton Formula for Pricing Options" and images of the three authors)

Today, I want to talk about arguably the most important discovery in mathematical finance over the last 100 years.

This is the "Black-Scholes-Merton" model, which provides a method for determining the fair price of a certain type of
financial asset known as an "option".

Unsurprisingly, that name comes from its three inventors: Fischer Black, Myron Scholes, and Robert Merton.

(Screen switches to showing an image of a Nobel Prize and the average daily options trading volume from 1973 to 2025)

Their work won them the Nobel Prize in Economics and led to an explosion in options trading, which is now a market worth
trillions upon trillions of dollars.

What I want to do is walk you through a derivation of this formula in a way that is accessible to anyone familiar with
basic probability and statistics. The kind you'd see in a calculus-based statistics course in high school or college.

(Screen switches to "Basic Probability and Statistics" and some related formulas. Later shows "Traditional Derivation is
Complicated" and "Portfolio Hedging", "Stochastic Calculus", "Partial Differential Equations", before crossing them all
out other than the probability one and changing the title to "Alternate Derivation is Simpler!")

Now, being Nobel Prize-winning work, the traditional derivation is actually quite complex and requires much more
machinery, but the final formula doesn't actually require all of that.

The traditional derivation ends up pulling in a risk management concept called "portfolio hedging", stochastic
calculus (which is an extension of calculus to random processes), and partial differential equations.

Needless to say, that requires a _huge_ amount of specialized knowledge that you're not going to have unless you've
earned a degree in this field, so we'll be taking a different route that bypasses these concepts while still remaining
mostly faithful to the original work.

To be clear, we will be doing a complete derivation of the "Black-Scholes-Merton" formula, just taking a few different
paths along the way to keep things from getting too complex.

(Screen switches to "Looking Ahead: 'Pricing an Option'" with five bullet points: "What is a stock? What is an
*option*?", "How would you assign a *fair price* to an option?", "Making things fully *analytical*", "*Visualizing* our
pricing formula", "6 *exercises* throughout (with hints and solutions!)")

So, how are we actually going to do this?

Because I'm not assuming any financial knowledge at all, we're going to have to start with what an option even is, and
that requires a bit of discussion on the stock market.

We're then going to talk about how you would even assign a fair price to an option, which is a surprisingly difficult
to do.

We'll reason about making that process fully analytical so that we get a relatively simple formula that gives us that
fair price.

And we'll end with some visualizations of our final pricing formula.

This is going to be structured as a complete lesson, so a lot of the major focus points are going to be in the form of
exercises. I'll go through my sample solutions in the video, but I encourage you to actually pause and try these out
yourself. It'll be a lot more meaningful if you discover some of the "ah-ha" moments here on your own rather than
watching me give some answers.

## what_is_an_option.py

(Screen shows a company broken up into blocks. One piece is moved off and labeled "stock (share)". A triangle appears
above the company and a customer with money appears on the right. The triangle is exchanged for the money and then a
small piece gets moved over to the stock.)

To start, let's talk about what a stock is. At a high-level, a stock is just a tiny piece of a company, so when you buy
a share, you gain ownership of that small piece.

Then, if the company makes a product and sells it to a customer, you are generally entitled to a small fraction of the
profit they earn.

This is interesting because it means that your stock is inherently worth something, it's directly tied to the overall
value of the company itself.

(Screen switches to a stock price chart that's initially flat at $100)

And since stocks have value, people buy and sell them all the time. This is what the stock market is! It's a public
place where you can see how much people are buying stocks for and how much they're being sold for.

The price of the stock is where the buyers and sellers have met in the middle. If a stock is worth $100, that means
buyers are currently willing to pay $100 for it, and there are sellers that are willing to give their own shares away in
exchange for that $100.

But of course, this is always in flux. Stock prices fluctuate up and down all the time as news about the company comes
out and people react to it.

(The chart extends out to 1 year and a simulated path moves up and down to about $115 and back to $105ish.)

The price might go up if the company announces a new exciting product, or it might go down if they experience a
significant scandal.

This is the sort of thing you can just look up online. You can search the current stock price of a company and see how
it's performed in the recent past. And indeed, you could own about two billionths of Netflix for the low price of $1300!

(Screen switches to a definition of an option)

That's the basics of a stock, and an option is something that's built on _top_ of a stock

It's a contract that gives you the option (hence the name) to buy a stock...

At a specific price that you choose, called the "strike price". This doesn't have to be the current stock price, it
can be anything.

And you'd buy the stock on a specific date in the future.

Importantly, you never _have_ to buy the stock when the contract expires. The financial legalese that people normally
use to make this clear is that the option conveys "the right but not the obligation" to buy the stock.

Now, technically, there are more complicated types of options and the one we're talking about here is called a "European
call option", but this is the type that the Black-Scholes-Merton model is designed for, so I'm just going to refer to
this as an option for our purposes.

Let's look at an example to make this a bit more concrete.

Say you're entering into one of these contracts to buy a share of Apple's stock for $300 in 3 months.

If at that time, Apple's stock price has increased to $325, you've made $25 in profit! You could buy the stock for $300
in the contract and then immediately sell it in the market for $325, pocketing the $25 difference.

On the other hand, if Apple's stock fell to $275, you make nothing. But you also don't lose anything! You simply
choose to not exercise the option to buy the stock!

(Screen switches to showing a payoff diagram)

So this isn't symmetric! If we plot out the profit you're making on this option vs. the final price of stock, hopefully
you can see that it's linear beyond that strike price of $300. For every dollar above $300, you make a dollar in profit.

And then on the other side, the profit is always zero.

But of course, as structured here, this is a contract with no downside. So in practice the person you're buying the
option from is going to charge you a fee to take on that risk.

That fee is known as the "premium" or "price" of the option, and it's what we're interested in figuring out.

What's a fair price to charge for this option? And more importantly, how much should you be willing to pay for it?

## finding_a_fair_price.py

(Screen shows "An option is ... on a specific date in the future")

The reason why determining a fair price is so difficult is that this contract fundamentally depends on the future
behavior of the stock price and obviously there's no way to know that in advance!

In fact, before the Black-Scholes-Merton formula, people made millions exploiting the fact that these things are
difficult to price. Before a rigorous method existed, some of it used to come down to trader intuition and vibes,
honestly.

(Screen shows "Exercise #1: How could you find a fair price for this?")

This brings us to our first exercise, which is a pretty open-ended one. How would you go about finding a fair price for
this?

(pause)

This really comes down to realizing that while the future is unknown, we could always try to guess!

We can research how the stock price has moved in the past. So, if it's moved from $300 to around $325, we might
predict...

That maybe it keeps going up to around $350...

Or maybe it goes back down to $300...

And maybe it falls even more than that!

(Screen shows "Simulate!")

So one thing we can try is to somehow simulate all these possibilities and get a sense of how much profit this option
would make in each case.

(Screen switches over to a plot of Stock Price vs. Time on the left and a histogram of Option Profit on the right.
The stock price paths are simulated iteratively until the histogram is denser and denser.)

Let's take a look at what that might look like.

Here's a plot of a simulated path of the stock price out to 3 months in the future, and it happens to end up around
$325.

That's $25 dollars above our strike price, and so the option would make $25 in profit.

If we simulate out more and more paths, we can simply record how much profit the option makes in each case, and start to
see how that profit ends up being distributed across all the various simulated scenarios.

(Average of $6 is plotted on the histogram)

At the end, we could look at that distribution and take the average, which ends up being about $6 here.

If we charged that amount as the fee of the option, then we'd expect it to cancel out the average profit of the option.
In other words, neither the buyer nor the seller would make any money on average.

And that would be a fair price! That's the very definition of fairness in this context.

## how_to_simulate.py

(Screen switches to showing "How to Simulate Stock Prices?" A Distribution Density vs. Stock Price distribution will be
plotted and have its width / standard deviation increase.)

This is good progress, but it kind of kicks the can down the road. How should we perform this simulation?

The first instinct of any statistician would be to just throw down a normal distribution and call it a day. Then we
could sample from it, and we'd be done.

But think about what happens if we look far into the future or at extremely volatile stocks. That distribution just
keeps getting wider and wider, until eventually it crosses over into negative prices.

(Left tail highlighted, "Negative Stock Prices?")

That makes no sense! Remember, a stock is partial ownership of a company, so it can't be worth less than
nothing. The _worst_ thing that can happen is that the company goes bankrupt and your stock becomes worthless.
It's never going below zero, you can't _owe_ money just for holding a share.

(Screen shows: "#1: Prices should not go negative")

So that's the first property we want in our simulation: prices should never go negative.

(A plot of Nvidia's prices over the last 1Y is shown, with the current price highlighted, ~$160. Later, Home Depot's is
shown around $370 a share.)

Another important fact is that the actual price of a stock doesn't directly represent the value of the company. Here on
the left we have NVIDIA, which is the most valuable company in the United States, worth more than $4 trillion. They
design all the GPUs that are powering the current AI craze, so their valuations are sky-high.

On the right, Home Depot trades around $370 a share, which is more than double NVIDIA's price. But Home Depot is nowhere
near as valuable as NVIDIA. So what gives?

These companies basically get to choose how many shares they issue, and thus how small of a slice you get to own of the
company when you buy their stock.

Buying a share of NVIDIA just gives you a much, much smaller fraction of the company than buying a share of Home Depot.

("Stock prices cannot be compared directly!" is displayed)

So stock prices can't be compared directly. What we *do* tend to look at are relative price moves. For example, NVIDIA
went up about 27% over the last year, while Home Depot rose closer to 10%.

("#2: Price moves should be relative" is displayed)

This is the second property our simulation should have. Stock price moves should be relative to the current price.

The final property is a consequence of this. Think about what happens if you have a constant relative price increase
day-over-day.

If we start at $100, a 10% increase makes it $110. If we increase 10% again, we're at $121. And then $133, and so on.

These increases are building on top of each other, so the final price is up 33% rather than just 30%. This is compound
growth, which is the final quality we'll want.

("#3: Relative changes should compound")

("Exercise #2: Let S(t) be the stock price at time t. Can you transform a normal distribution and use it to construct
S(t) so that it has these three qualities?")

So those are three qualities we want, which brings us to our second exercise.

Let's say S(t) is the distribution of the stock price at time t. Can you transform a normal distribution and use it to
construct S(t) so that it has these three qualities that we want?

Again, we'd really love to use a normal distribution here, so let's see if we could tweak it a bit to meet our
requirements.

("Hint: Normal distributions 'add together.' What kind of function turns adding into multiplying?")

If you're stuck here, remember that one of the important qualities of a normal distribution is that adding two of them
together still gives you a normal distribution, just shifted and scaled a bit differently.

So, they're best for processes that add together. But compound growth multiplies, so what kind of function turns the
addition of the normal distribution into multiplication?

(pause)

(shows a plot of e^x and e^{x+y} = e^x * e^y)

The perfect candidate here is an exponential function. e^x is always positive. Even e^(–100) is just 1 divided by
e^(100), so it's a very tiny _positive_ number. That guarantees prices never go negative.

And the whole point of an exponential is that it represents repeated multiplication or compound growth. e to the x plus
y is e to the x times e to the y. That's the compounding we want.

("Consider S(t) / S(0) ~ exp(N(mu, sigma^2))")

To capture relative price moves, we can look at S(t) / S(0), which is the distribution of the stock price relative to
its starting point.

If we set this to be the exponential of a normal distribution, we get all three of our properties.

(Moves "Consider ..." to top of screen and adds "Lognormal distribution")
("X ~ exp(N(mu, sigma^2)) <-> ln(X) ~ N(mu, sigma^2)")

This exponential of a normal distribution is known as a lognormal distribution, for the somewhat confusing reason that
the log of the distribution is normal.

That log cancels out the exponential.

This is actually one of the _assumptions_ of the Black-Scholes-Merton model, that the stock price follows a lognormal
distribution, but I didn't want to drop it on you out of nowhere. It's a choice that makes sense from first principles.

("Plot shows a comparison of a normal density and a lognormal one")

Let's take a look at what this transformation did for us.

Here's one of those normal distributions we were looking at earlier with the negative prices.

And when I switch over to this lognormal transformation, you'll see two things.

("No negatives!")

All the negative prices on the left tail disappear because they get shifted above zero by the exponential function.

("Compounding returns!")

And then the right tail gets a little heavier because of e^x's tendency to blow up. Those are the compound returns
kicking in.

(mu and sigma get highlighted briefly)

All that remains for our simulation is to figure out what values of mu and sigma to use for this distribution.