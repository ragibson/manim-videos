# black_scholes_derivation

TODO: create frozen requirements.txt for final package versions used in the render
TODO: more comments throughout the scripts?

The sequence of scenes here is:

* [introduction.py](introduction.py): Introduce authors, Nobel Prize, and options market growth. Then, allude to the
  traditional derivation being complicated and some basic steps we'll take to dodge those complications.
* [what_is_an_option.py](what_is_an_option.py): Describe what a stock is, how stock value is determined over time, and
  what an option is. The option introduction includes an explicit example and the (call) payoff diagram.
* [finding_a_fair_price.py](finding_a_fair_price.py): Mention the difficulty of pricing an asset that depends on
  (unknown) future stock prices, and how a simulation could address this.
* [how_to_simulate.py](how_to_simulate.py): Explain qualities of a simulation that we would like to have, and the
  corresponding distribution that gives us these qualities is the lognormal distribution.
* [determining_distribution_parameters.py](determining_distribution_parameters.py): Derive the PDF of a lognormal
  distribution and the parameters for a particular stock (mu, sigma).
* [analytic_calculation.py](analytic_calculation.py): Finally derive the Black-Scholes formula by splitting the
  calculation into an expectation and a probability calculation. A discounting step is introduced at the very end to
  complete the derivation.
* [visualization_conclusion.py](visualization_conclusion.py): Animation of the stock price distribution and payoff
  diagram as we sweep each of the variables up and down. The section closes with a simple list of high-level takeaways
  from the entire discussion.