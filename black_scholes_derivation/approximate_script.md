# Can You Price Options with Just Basic Statistics? A Simple Black-Scholes Pricing Derivation

(This script is mostly what's in the video along with some notes on what parts of the animation are shown at each
point. I self-edited on the fly at a few places, so it's a little different from the final result but should be quite
close overall. In particular, I think a few asides were completely cut due to pacing issues.)

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

## determining_distribution_parameters.py

("Exercise #3: Determine the probability density of X ~ exp(N(mu, sigma^2))")

("Remember: f_{N(mu, sigma^2)}(x) = 1/(sigma * sqrt(2*pi)) * exp(-(x - mu)^2 / (2 * sigma^2)))

Before that, we're going to need the probability density function of the lognormal distribution.

This will be our third exercise, and I've put the normal PDF on the screen for reference if you need it.

(pause)

This is a pretty standard exercise. Let's say that Y is the normal distribution in question, and let X be e^Y.

We know that the PDF of X is going to be the derivative of its cumulative distribution function, which I'll write here
as the probability that capital X is less than or equal to x.

But since X is the exponential of Y, this is the same as the probability that capital Y is less than or equal to the log
of x.

That, in turn, is the CDF of Y evaluated at log(x).

Taking the derivative, we get the PDF of Y, evaluated at log(x), and then we pick up a factor of 1/x from the chain
rule.

Plugging everything in, this looks like the normal PDF, except you replace x with log(x) and add a 1/x in front.

Not too bad. And this will come in very handy for the later exercises.

(Screen switches to "S(t) / S(0) ~ exp(N(mu, sigma^2))", and then "S(t)" becomes "S(1)")

Going back to our stock price simulation, S(t) / S(0) is lognormally distributed, and we're interested in what those
parameters, mu and sigma, should be in general.

To start off simple, let's just think about S(1) and look at that mu term.

Mu will shift the distribution left and right, so it determines how much the stock price tends to drift upward or
downward on average.

But actually we don't want to assume that the stock drifts up or down at all!

The whole point of our simulation is to predict a bunch of future scenarios, and if we built in an upward bias, we'd end
up incorrectly pricing our option. Nobody truly knows whether the stock will rise or fall, so we want our simulation to
be unbiased.

Okay, so do we just set mu to be zero? It's not actually as simple as that.

(Normal Distribution Density vs. Stock Price is plotted)

Look, here's a normal distribution and let's think back at what the lognormal transformation did.

(Transformed to Lognormal Distribution Density. Movement in the left tail is highlighted, and then the right tail.)

The left tail had its values shifted right when we eliminated negative prices.

And then also the right tail had its values shifted right because of our compounding returns.

Both of these are upward shifts to the distribution, so that lognormal will definitely have a larger mean than the
normal distribution that it came from.

("Exercise #4: Given sigma, find the value of mu that keeps the stock price flat, on average. That is, E[S(1)] = S(0).")

This is our fourth exercise. If you knew sigma already, find the value of mu that keeps the stock price flat on average.
That is, the expected value of S(1) should be S(0).

(pause)
("Hint 1: What happens if mu = 0?")

We know a mu of zero won't work, but you can try that as a starting point as see how far off you are. That should give
you a sense of how to adjust mu accordingly.

(pause)
("Hint 2: The integral for E[S(1)] can be transformed so that you're integrating a normal PDF. Then, no integration
calculations are needed.")

This second hint is more strategic. The integral you're computing here can be simplified so that it looks like a normal
PDF instead of a lognormal one. If you transform it accordingly, you can avoid doing more complicated integration.

(pause)

Following the hints, let's see what happens if we take mu = 0.

The expected value of S(1) is the expected value of S(0) times the lognormal factor.

And since S(0) is a constant, we can pull it out of the expectation.

Then, we really just need to find the expected value of this zero-mu lognormal.

So let's set that up.

This is the integral of x times the PDF over its entire domain, 0 to infinity.

Plugging in the PDF we derived earlier, you'll see that the x factor is going to cancel with the 1/x from the PDF, so
I'll just rewrite that real quick.

This already looks a lot taking the area under a standard normal PDF. If we could transform it to be exactly a normal,
the entire integral would just be a normal CDF.

To do this, we can set up a u-substitution. The only part that doesn't match a normal PDF is the log x term in the
exponential, so let's change variables to get rid of it.

Taking u to be log x (and thus e^u to be x) gives us that du = 1/x dx.

Moving that x to the left hand side and substituting, we get that exp(u) du = dx.

Bringing this back into our integral, log x becomes u and then we get an extra exp(u) factor on the right side.

Crucially, that bottom limit of integration becomes negative infinity to match the behavior of log x as x approaches
zero.

Simplifying a bit, let's collect the exponential terms together.

This is closer to a normal PDF, but it doesn't quite match yet. We really want it to take the form of
(u - mu)^2 / 2 sigma^2.

To this end, we get a common denominator and notice that it looks even closer to a distributed version of (u - mu)^2.

Writing it out explicitly, all that we're missing is the equivalent of the mu^2 term, where in our case, sigma^2 is
actually taking the place of mu.

Completing the square leaves us with an extra summand of sigma^4 in the numerator.

Which I'll simplify real quick as sigma^2 / 2 and then pull it back out of the exponential.

Anything involving sigma is a constant with respect to u, so we can actually pull it out of the integral altogether.

And we're left this interesting integral over a normal distribution with mean sigma^2 and standard deviation sigma.

But it's an integral over the entire domain, negative infinity to positive infinity. It's just 1. The whole term
disappears.

Our final answer is that the expected value term is the exponential of sigma^2 over 2.

All this means that the lognormal transformation effectively shifted the normal distribution in the exponent over by
this amount.

So we can cancel out that effect by setting mu to be negative sigma^2 / 2. This completes the exercise.

(Screen shows a plot of a stock price over time, briefly stopping at "Today" and continuing forward in a different
color. A value of sigma = 10% is shown and then animated up to 30% and back down to 20%.)

Let's briefly talk about the other parameter, sigma. This one won't be an exercise or anything since it's a bit more
freeform.

Sigma determines how volatile the stock is in the simulation, how wide the distribution of price changes will be, so
this will vary from stock to stock.

You could look how the stock has moved in the past and then use that to get an idea of what sigma should be. For
example, simulating forward with a volatility of 10% here seems a bit too stable.

And sweeping up to 30% looks a bit too volatile. Something like 20% is reasonable given the historical trends we have
here.

This is the type of thing you could estimate by simply calculating the standard deviation of historical returns.

Otherwise, we don't need to worry about this parameter too much. Just know that it's something that can be estimated
for a specific stock, and you can search volatilities online if you want to get a feel for them.

This gives us all the parameters we were looking for. Mu is based on sigma, and sigma represents the stock's volatility.

(Screen changes to "What does S(t) look like?")

Taking a step back, we had calculated out the distribution for S(1), so we have to figure out what it looks like for an
arbitrary time t.

This isn't too complicated because we can just take another step ahead to get S(2). It'll be S(1) times the same type of
lognormal distribution.

Substituting back in for S(1), we see that we're multiplying by two lognormal distributions. One from the first time
step, and one from the second.

Like before, we can collect these into the exponent together and make use of the fact that normal distributions add
together nicely.

Those two means of -sigma^2/2 will add together to be twice as large, and variances add together in the same way.

So, S(2) looks exactly like S(1) with its parameters doubled.

Needless to say, this pattern continues for 3 and t in general.

That's our distribution for the stock price at time t!

S(t) is S(0) times the exponential of a normal distribution with mean -sigma^2/2 * t and variance sigma^2 * t.

## analytic_calculation.py

(Left side shows simulations of stock prices from $300 out to 0.25 years. The header displays
S(t) ~ S(0) * exp(N(-sigma^2/2 * t, sigma^2 * t)). The right side shows the distribution density of the final stock
price.)

Up to this point, we've been simulating the stock price into the future, which looks something like this out to 3
months.

We've calculated that this should follow the lognormal distribution with the parameters that we derived.

On the right, you can see what the distribution of the final stock price looks like.

So, if this were an option with strike $320, we care about how often the stock finishes above that strike after 3
months.

On the left plot, that's all the simulated paths that end up above the strike, and on the right plot it's the shaded
part of the distribution on the right tail.

("Calculate it all analytically!")

So really there's no point in doing a simulation at all! We can calculate the probabilities directly.

This was honestly the whole point of basing the distribution off of a normal in the first place. We needed this to
remain simple enough to be converted into an analytic formula at the end of the day.

Let's see this calculation through.

(Left plot disappears and \tilde{C} = E[S(t) - K | S(t) > K] is shown.)

We want to calculate the price of the option, which is traditionally denoted C since this type of option is referred to
as a "call option".

And we've set it up so that the price is the average profit. That's the expected value of the stock price minus
the strike, in the cases where the stock actually ends up above the strike.

Visually, this is the average amount that S(t) exceeds the strike in that right tail I've highlighted. Whenever S(t)
finishes below the strike, the option pays nothing, it's worthless, so we just need to focus on the right tail.

(Formula is expanded into E[S(t) | S(t) > K] - K * P[S(t) > K])

Expanding this into two terms, we have the average value of S(t) when it's above the strike, minus the strike times the
probability of this scenario.

Our final two exercises will be to calculate each of these terms.

("Exercise #5 : Calculate P[S(t) > K]". Later, a hint is shown of "Hint: Transform S(t) so that you can use the standard
normal CDF.")

First, we'll do the probability term, so the exercise is to calculate the probability that S(t) ends up larger than K.

(pause)

This will come down to manipulating the form of S(t) until you can use the standard normal CDF.

(pause)

Towards the goal of manipulating S(t) into a normal, let's divide through by S(0) and take the log of both sides.

Then, we've really isolated the normal distribution inside the exponent, so we just need to determine the probability
this normal part exceeds log(K / S(0)).

We want to use the standard normal CDF, so let's normalize it piece by piece. We can move the mean over to the right
side.

And then divide through by the standard deviation to get this into the form of a standard normal.

The CDF gives the probability of the left tail, so our right tail probability is just 1 minus the CDF of this larger
expression that we've created.

That completes exercise 5.

("Exercise #6: Calculate E[S(t) | S(t) > K]")

The last exercise is to compute the expectation term. What's the average value of the stock price when it's above the
strike.

(pause)

This will be an integral very similar to the one we did in Exercise 4.

(pause)

It will be easier to work with a lognormal distribution directly, so I'm going to move S(0) into the exponential by
taking its log and then also moving it into the mean of the normal distribution.

The expectation that we're trying to calculate is going to be the integral of x times the PDF over the right tail only,
K to infinity.

Once again, that leading x will cancel with the 1/x from the lognormal PDF, so plugging everything in gives us this
integral.

We'll be doing another u substitution here to try and get everything looking more like a standard normal, so let's
choose u to normalize the entire distribution in the exponent. We're including both the mean and the standard deviation
to try and get it to mean 0 and standard deviation 1.

du is just 1/x from the log term along with the sigma sqrt(t) constant, all times dx.

And so our dx will become x times sigma sqrt(t) du, where we get x by solving for it in the u substitution.

If we bring that all together and rearrange a bit, dx is S(0) times sigma sqrt(t) times the exponential of
u sigma sqrt(t) - sigma^2 / 2 t.

When we plug all this back into our integral, the sigma sqrt(t) factor at the start cancels out, and the exponential
term becomes -u^2/2 from our substitution along with those two terms from the dx expression.

Remember that we also have to adjust the lower limit of integration, so that becomes our u substitution with K in place
of x.

Simplifying the exponent and pulling the S(0) constant out of the integral, we see that this is a normal distribution
PDF with mean sigma sqrt(t).

And we can get this right tail of the distribution by calculating 1 minus the standard normal CDF as long as we adjust
by that mean.

Simplifying a bit again, we can collect those log terms and bring everything into a single fraction, which just ends up
flipping the sign on the sigma summand.

("C = E[S(t) | S(t) > K] - K * P[S(t) > K]" and it's solved out piece by piece)

All we have to do now is put these answers from our exercises back into the formula we had before.

I'll simplify this so it looks a tiny bit nicer. We can take advantage of the symmetry of the standard normal to rewrite
1 - CDF(x) as CDF(-x).

And then distribute that negative sign into the fractions themselves.

So our final answer is S(0) times the CDF of a large expression, minus the strike times the CDF of a similar looking
expression.

Most often, this is written with those expressions as helper variables d+ and d-. And since they're basically the same
with just a sign flipped, we write d- as d+ with the necessary adjustment from earlier.

(Plot shows "Future Value of Money" vs. "Time (years)")

Now, there is actually one minor piece to add. In finance, getting a dollar today is worth more than getting a dollar in
the future.

Why? Because if you had the money right now, you could earn interest on it in something like a savings account, and it
would grow exponentially in value over time.

Mathematically, one dollar becomes e^{rt} dollars after t years, where r is the interest rate you could earn on that
money.

If we wanted to fairly compare money we're getting in the future with money today, we'd need to scale it back by the
opposite factor, e^{-rt}. This is called the "discount factor", and it translates between future value and today's
value.

("Need to: Convert the future option price C to current value D*C. Convert the current price S(0) to future value
S(0) / D.")

In our option formula, we need to use this discount factor translator in two different ways.

The option profit is made in the future. So, to get the price of the option today, we multiply by D.

And then our probability calculations were all about the stock price at time t. But we were using today's price, S(0).
To make it consistent with those future-time calculations, we actually need to convert S(0) to future value by dividing
by D.

Bringing it all together, that's an extra D factor on the outside and a division by D whenever we're using S(0).

Note that this division of S(0)/D also takes place in the helper variables defined.

And that's it! That's the full Black-Scholes-Merton formula for pricing an option.

# visualization_conclusion.py

I want to finish off with a visualization of this pricing formula to build some intuition for how it behaves, and
especially how each parameter influences the option price.

(parameters are shown at top of screen)

Here are all the parameters in the formula. Remember,

S(0) is the current stock price,
sigma is the stock's volatility,
t is the years until the option expires,
K is the strike price,
and r is the interest rate that you could earn on money in the meantime, which we were using in the discount factor.

(Stock price distribution is shown on left, "Stock Price at Time t" vs "Distribution Density")

On the left, let's plot the lognormal distribution of the stock price at expiration. I'll mark the strike with a
vertical dotted line.

This shaded area on the right is where the option makes a profit, so the size and distance from the strike will
determine how valuable the option is.

(Sweep through changing the parameters one-by-one. The plots are animated accordingly.)

Let's change each of these parameters one at a time and see what happens.

Changing S(0), the current stock price, shifts the whole distribution left and right.

The volatility sigma controls how much the stock price tends to move. So, lower volatility keeps the prices clustered
near the current level. And higher volatility widens the distribution out.

The time t has a similar effect. If there's less time for the stock to move, its price can't wander very far. And as t
increases, the distribution widens.

Moving the strike K just shifts the vertical line, changing how much of the distribution falls into the profitable
region.

And we'll get back to r later.

("Current stock price vs. option price" plot is shown on the left. The intrinsic price is plotted in a dashed line.)

Now, on the right, let's plot the option price against the current stock price. The dashed line shows how much money
you'd make if you were able to exercise the option immediately, so it's the stock price minus the strike.

The white dot is the actual option price for this example, a few dollars.

(Sweeping through all the parameters again)

Let's change each parameter again.

Moving S(0) down makes the option decrease in value since it's increasingly unlikely to ever end above the strike. And
pushing S(0) far above the strike means it's a bit more valuable than just exercising the option now. The extra value
comes from the extra chance of even higher profits before expiration.

This is all tracing out a curve above that dashed line, so let's show it for all potential S(0) values. As we change
S(0), the white dot will follow this blue curve.

For volatility, decreasing it lowers the option value since the stock is less likely to rise above the
strike. And increasing it raises the value since there's _more_ chance to profit.

Again, time has a similar effect. Less time before expiration means the stock is less likely to rise above the strike,
decreasing the price of the option towards that dashed line. And more time increases the option price for the opposite
reason.

For the strike, lowering it makes the option more valuable, since more of the distribution is in the profitable region.
And raising it does the opposite by making the profitable region smaller.

The interest rate r has a smaller effect since it adjusts how much you prefer having money now vs. waiting for the
option's profit in the future.

A lower r decreases the option price since there's less benefit to holding onto cash right now. And a higher r makes
cash more attractive, so the option price increases.

(Going back to sweeping S(0) briefly)

This also gives some intuition on why the option price responds differently to changes in the stock price depending on
where it is relative to the strike.

If the stock price is far below the strike, moves in the stock barely matter since the option will almost certainly
be worthless anyway.

If the stock is far above the strike, almost the entire distribution is profitable, so each dollar change in the stock
price will affect the profit of the option by the same amount. Hence, the option's value moves nearly one-to-one with
the stock price itself.

(Visualization fades out and is replaced with "What We Learned"
"Some new financial knowledge"
"Brief peek into the complexities of mathematical finance"
"*General problem-solving technique:* simulate, iterate, and possibly refine to an analytic result")

Finally, I want to briefly take a step back and look at what we've done.

We covered some basics about stocks, options, and so on that may have been new to you.

But I also hope this gave you a sense of how complicated mathematical finance can be. People in the financial
industry are constantly inventing new products and adding exotic features to existing ones, so it's extremely important
to be able to determine how much these things are worth.

And it's far from a simple task in general! The Black-Scholes-Merton formula we derived here is one of the simpler
cases.

Most importantly, the technique we applied here is a general problem-solving strategy that you should have in your
mathematical toolbox. There's a whole class of problems that are hard to reason about but relatively easy to simulate.
Then, you can try and find ways to refine or simplify the simulation bit by bit. Either you'll end up with a fully
analytic solution like we had here, or you simply find more efficient ways to simulate your problem!

Far outside of finance, that is a really powerful tool to have on hand.

That's all I've got for you today, so thanks for watching, and I hope you learned something new.