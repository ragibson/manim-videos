# Can You Price Options with Just Basic Statistics? A Simple Black-Scholes Pricing Derivation

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