""""""  		  	   		  		 			  		 			     			  	 
"""MC2-P1: Market simulator.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
GT ID: 903561681 (replace with your GT ID)  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import datetime as dt  		  	   		  		 			  		 			     			  	 
import os  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import numpy as np  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
import pandas as pd  		  	   		  		 			  		 			     			  	 
from util import get_data, plot_data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
DEBUG = 1


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "pjiang49"  # replace tb34 with your Georgia Tech username

def compute_portvals(  		  	   		  		 			  		 			     			  	 
    orders_file="./orders/orders-01.csv",
    start_val=1000000,  		  	   		  		 			  		 			     			  	 
    commission=9.95,  		  	   		  		 			  		 			     			  	 
    impact=0.005,  		  	   		  		 			  		 			     			  	 
):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Computes the portfolio values.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param orders_file: Path of the order file or the file object  		  	   		  		 			  		 			     			  	 
    :type orders_file: str or file object  		  	   		  		 			  		 			     			  	 
    :param start_val: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
    :type start_val: int  		  	   		  		 			  		 			     			  	 
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		  		 			  		 			     			  	 
    :rtype: pandas.DataFrame  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is the function the autograder will call to test your code  		  	   		  		 			  		 			     			  	 
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		  		 			  		 			     			  	 
    # code should work correctly with either input
  		  	   		  		 			  		 			     			  	 
    # In the template, instead of computing the value of the portfolio, we just  		  	   		  		 			  		 			     			  	 
    # read in the value of IBM over 6 months
    df_orders = pd.read_csv(orders_file, parse_dates = ['Date',],
                            usecols = ['Date', 'Symbol', 'Order', 'Shares'])
    df_orders.sort_index(inplace = True)

    start_date = df_orders['Date'].min()
    end_date = df_orders['Date'].max()
    symbols = df_orders['Symbol'].unique()

    # df price
    df_prices = get_data(symbols, pd.date_range(start_date, end_date))
    df_prices['Cash'] = 1.0

    # df trades
    df_trades = df_prices.copy()
    df_trades.iloc[:] = 0
    for i, row in df_orders.iterrows():
        _date = row['Date']
        _sym = row['Symbol']
        _direction = 1 if row['Order'] == "BUY" else -1
        _quantity = row['Shares'] * _direction
        _market_impact_fac = (1+impact) if _direction == 1 else (1-impact)
        _price_trade = df_prices.loc[_date][_sym] * _market_impact_fac
        _dCash = (-1) * _price_trade * _quantity
        df_trades.loc[_date][_sym] += _quantity
        df_trades.loc[_date]['Cash'] += _dCash - commission

    # df holdings
    df_holdings = df_trades.copy()
    df_holdings.iloc[0]['Cash'] += start_val
    df_holdings = df_holdings.cumsum()

    # df values
    df_values = df_prices * df_holdings

    # df port_val
    df_port_val = df_values.sum(axis = 1)

    if DEBUG:
        df_orders.to_csv('df_orders.csv')
        df_trades.to_csv('df_trades.csv')
        df_prices.to_csv('df_prices.csv')
        df_holdings.to_csv('df_holdings.csv')
        df_values.to_csv('df_values.csv')
        df_port_val.to_csv('df_port_val.csv')
    return df_port_val

  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
def test_code():  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    Helper function to test code  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # this is a helper function you can use to test your code  		  	   		  		 			  		 			     			  	 
    # note that during autograding his function will not be called.  		  	   		  		 			  		 			     			  	 
    # Define input parameters  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    of = "./orders/orders-02.csv"
    sv = 1000000  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Process orders  		  	   		  		 			  		 			     			  	 
    portvals = compute_portvals(orders_file=of, start_val=sv)  		  	   		  		 			  		 			     			  	 
    if isinstance(portvals, pd.DataFrame):  		  	   		  		 			  		 			     			  	 
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		  		 			  		 			     			  	 
    else:  		  	   		  		 			  		 			     			  	 
        "warning, code did not return a DataFrame"  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Get portfolio stats  		  	   		  		 			  		 			     			  	 
    # Here we just fake the data. you should use your code from previous assignments.  		  	   		  		 			  		 			     			  	 
    start_date = dt.datetime(2008, 1, 1)  		  	   		  		 			  		 			     			  	 
    end_date = dt.datetime(2008, 6, 1)  		  	   		  		 			  		 			     			  	 
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [  		  	   		  		 			  		 			     			  	 
        0.2,  		  	   		  		 			  		 			     			  	 
        0.01,  		  	   		  		 			  		 			     			  	 
        0.02,  		  	   		  		 			  		 			     			  	 
        1.5,  		  	   		  		 			  		 			     			  	 
    ]  		  	   		  		 			  		 			     			  	 
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [  		  	   		  		 			  		 			     			  	 
        0.2,  		  	   		  		 			  		 			     			  	 
        0.01,  		  	   		  		 			  		 			     			  	 
        0.02,  		  	   		  		 			  		 			     			  	 
        1.5,  		  	   		  		 			  		 			     			  	 
    ]  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    # Compare portfolio against $SPX  		  	   		  		 			  		 			     			  	 
    print(f"Date Range: {start_date} to {end_date}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		  		 			  		 			     			  	 
    print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Cumulative Return of SPY : {cum_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		  		 			  		 			     			  	 
    print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")  		  	   		  		 			  		 			     			  	 
    print()  		  	   		  		 			  		 			     			  	 
    print(f"Final Portfolio Value: {portvals[-1]}")  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    test_code()  		  	   		  		 			  		 			     			  	 
