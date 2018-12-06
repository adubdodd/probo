from probo.marketdata import MarketData
from probo.payoff import ExoticPayoff, geometricAsianCallPayoff
from probo.engine import MonteCarloEngine, NaiveMonteCarloPricer, PathwiseNaiveMonteCarloPricer, ControlVariatePricer
from probo.facade import OptionFacade
import time

## Set up the market data
spot = 100
rate = 0.06
volatility = 0.20
dividend = 0.03
thedata = MarketData(rate, spot, volatility, dividend)

## Set up the option
expiry = 1
strike = 100
the_simple_monte_carlo_call = ExoticPayoff(expiry, strike, geometricAsianCallPayoff)
the_geom_monte_carlo_call = ExoticPayoff(expiry, strike, geometricAsianCallPayoff)

## Set up Naive Monte Carlo
nreps = 10000
steps = 10
pricer = NaiveMonteCarloPricer
pricer_1 = PathwiseNaiveMonteCarloPricer
mc_engine_1 = MonteCarloEngine(nreps, steps, pricer_1)
pricer_2 = ControlVariatePricer
mc_engine_2 = MonteCarloEngine(nreps, steps, pricer_2)

## Calculate the price
option1 = OptionFacade(the_simple_monte_carlo_call, mc_engine_1, thedata)
time_start_1 = time.clock()
price1 = option1.price()
time_elapsed_1 = (time.clock() - time_start_1)
#print("The call price via Simple Monte Carlo is: {0:.4f}. The std err is: {1:.4f}. The time elapsed was {2:.4f} seconds.".format(*price1, time_elapsed_1))

option2 = OptionFacade(the_geom_monte_carlo_call, mc_engine_2, thedata)
time_start_2 = time.clock()
price2 = option2.price()
time_elapsed_2 = (time.clock() - time_start_2)
#print("The call price via Geometric Asian Control Variate Monte Carlo is: {0:.4f} The std err is: {1:.4f} The time elapsed was {2:.4f} seconds. ".format(*price2, time_elapsed_2))

print('|                      | Call Option Price  | Call Option Std. Err. | Relative Comp. Time |')
print('| -------------------- | ------------------ | --------------------- | ------------------- |')
print('| Simple Monte Carlo   | {0:.4f}             | {1:.4f}                |  {2:.4f}             |'.format(*price1, time_elapsed_1) )
print('| Geom. Asian M. Carlo | {0:.4f}             | {1:.4f}                |  {2:.4f}             |'.format(*price2, time_elapsed_2) )