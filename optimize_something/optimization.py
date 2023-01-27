""""""  		  	   		  		 			  		 			     			  	 
"""MC1-P2: Optimize a portfolio.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		  		 			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		  		 			  		 			     			  	 
All Rights Reserved  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Template code for CS 4646/7646  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		  		 			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		  		 			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		  		 			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		  		 			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		  		 			  		 			     			  	 
or edited.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		  		 			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		  		 			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		  		 			  		 			     			  	 
GT honor code violation.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
-----do not edit anything above this line---  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
Student Name: Peilun Jiang (replace with your name)  		  	   		  		 			  		 			     			  	 
GT User ID: pjiang49 (replace with your User ID)  		  	   		  		 			  		 			     			  	 
GT ID: 903561681s (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import datetime as dt  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import matplotlib.pyplot as plt  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data
import scipy.optimize as spo
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
# This is the function that will be tested by the autograder  		  	   		  		 			  		 			     			  	 
# The student must update this code to properly implement the functionality
def eval_portfolio( allocs, prices ):
    rf = 0.0
    n_days = 252
    port_val_df = prices * allocs
    port_val = port_val_df.sum(axis = 1)
    commul_return = port_val.pct_change()
    cr = commul_return.iloc[-1]
    adr = commul_return[1:].mean()
    sddr = commul_return[1:].std()
    sr = np.sqrt(n_days) * (adr - rf)/sddr
    return [cr, adr, sddr, sr, port_val]

def maximize_sharpe_ratio(allocs, prices):
    sr = eval_portfolio(allocs,prices)[3]
    return -1.0 * sr

def optimize_portfolio(  		  	   		  		 			  		 			     			  	 
    sd=dt.datetime(2008, 1, 1),  		  	   		  		 			  		 			     			  	 
    ed=dt.datetime(2009, 1, 1),  		  	   		  		 			  		 			     			  	 
    syms=["GOOG", "AAPL", "GLD", "XOM"],  		  	   		  		 			  		 			     			  	 
    gen_plot=False,  		  	   		  		 			  		 			     			  	 
):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function should find the optimal allocations for a given set of stocks. You should optimize for maximum Sharpe  		  	   		  		 			  		 			     			  	 
    Ratio. The function should accept as input a list of symbols as well as start and end dates and return a list of  		  	   		  		 			  		 			     			  	 
    floats (as a one-dimensional numpy array) that represents the allocations to each of the equities. You can take  		  	   		  		 			  		 			     			  	 
    advantage of routines developed in the optional assess portfolio project to compute daily portfolio value and  		  	   		  		 			  		 			     			  	 
    statistics.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
    :type sd: datetime  		  	   		  		 			  		 			     			  	 
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
    :type ed: datetime  		  	   		  		 			  		 			     			  	 
    :param syms: A list of symbols that make up the portfolio (note that your code should support any  		  	   		  		 			  		 			     			  	 
        symbol in the data directory)  		  	   		  		 			  		 			     			  	 
    :type syms: list  		  	   		  		 			  		 			     			  	 
    :param gen_plot: If True, optionally create a plot named plot.png. The autograder will always call your  		  	   		  		 			  		 			     			  	 
        code with gen_plot = False.  		  	   		  		 			  		 			     			  	 
    :type gen_plot: bool  		  	   		  		 			  		 			     			  	 
    :return: A tuple containing the portfolio allocations, cumulative return, average daily returns,  		  	   		  		 			  		 			     			  	 
        standard deviation of daily returns, and Sharpe ratio  		  	   		  		 			  		 			     			  	 
    :rtype: tuple  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Read in adjusted closing prices for given symbols, date range  		  	   		  		 			  		 			     			  	 
    dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
    prices_all = get_data(syms, dates)  # automatically adds SPY  		  	   		  		 			  		 			     			  	 
    prices = prices_all[syms]  # only portfolio symbols  		  	   		  		 			  		 			     			  	 
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # find the allocations for the optimal portfolio  		  	   		  		 			  		 			     			  	 
    # note that the values here ARE NOT meant to be correct for a test case
    num_assets = len(syms)
    allocs = num_assets * [1.0/num_assets, ]

    bounds = tuple((0, 1) for x in range(num_assets))
    constraints = ({'type':'eq', 'fun': lambda x: np.sum(x)-1})
    results = spo.minimize( maximize_sharpe_ratio, allocs, args = (prices, ), method = 'SLSQP', bounds = bounds, constraints = constraints )
    allocs = results.x
    cr, adr, sddr, sr, port_val = eval_portfolio( prices, allocs )
  		  	   		  		 			  		 			     			  	 
    # Get daily portfolio value
  		  	   		  		 			  		 			     			  	 
    # Compare daily portfolio value with SPY using a normalized plot  		  	   		  		 			  		 			     			  	 
    if gen_plot:
        df_temp = pd.concat(  		  	   		  		 			  		 			     			  	 
            [port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1  		  	   		  		 			  		 			     			  	 
        )
        df_temp = df_temp/df_temp.ix[0,:]
        ax = df_temp.plot( title = "Normalized Prices: Portfolio vs. SPY" )
        ax.set_ylabel("Normalized prices")
        ax.set_xlabel("Dates")
        plt.savefig("Figure 1.png")
  		  	   		  		 			  		 			     			  	 
    return allocs, cr, adr, sddr, sr  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    This function WILL NOT be called by the auto grader.  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2009, 1, 1)  		  	   		  		 			  		 			     			  	 
    end_date = dt.datetime(2010, 1, 1)  		  	   		  		 			  		 			     			  	 
    symbols = ["GOOG", "AAPL", "GLD", "XOM", "IBM"]  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Assess the portfolio  		  	   		  		 			  		 			     			  	 
    allocations, cr, adr, sddr, sr = optimize_portfolio(  		  	   		  		 			  		 			     			  	 
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Print statistics  		  	   		  		 			  		 			     			  	 
    print(f"Start Date: {start_date}")  		  	   		  		 			  		 			     			  	 
    print(f"End Date: {end_date}")  		  	   		  		 			  		 			     			  	 
    print(f"Symbols: {symbols}")  		  	   		  		 			  		 			     			  	 
    print(f"Allocations:{allocations}")  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio: {sr}")  		  	   		  		 			  		 			     			  	 
    print(f"Volatility (stdev of daily returns): {sddr}")  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return: {adr}")  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return: {cr}")  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    # This code WILL NOT be called by the auto grader  		  	   		  		 			  		 			     			  	 
    # Do not assume that it will be called  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
