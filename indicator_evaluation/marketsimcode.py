""""""
"""MC2-P1: market sim code.

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
from util import *
DEBUG = 0
def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "pjiang49"  # replace tb34 with your Georgia Tech username

def compute_portvals(
        df_trades,
        start_val=1000000,
        commission=9.95,
        impact=0.005,
):
    """
    Computes the portfolio values.

    :param df_trades: the df_trades whose index is of type datatime and columns are symbols
    :type df_trades: pandas.DataFrame
    :param start_val: The starting value of the portfolio
    :type start_val: int
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)
    :type commission: float
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction
    :type impact: float
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.
    :rtype: pandas.DataFrame
    """
    symbols = df_trades.columns
    df_trades.sort_index(inplace=True)

    start_date = df_trades.index.min()
    end_date = df_trades.index.max()
    symbols = df_trades.columns.unique()

    # df price
    df_prices = get_data(symbols, pd.date_range(start_date, end_date))
    df_prices = df_prices[symbols]

    # df holdings
    df_holdings = df_trades.copy()
    df_holdings = df_holdings.cumsum()

    # adjust for cash
    df_prices['Cash'] = 1.0
    df_trades['Cash'] = 0.0
    df_buy = df_trades[symbols] > 0
    df_trade_prices = df_prices.copy()
    df_trade_prices[df_buy][symbols] = df_prices[symbols][df_buy] * (1+impact)
    df_trade_prices[~df_buy][symbols] = df_prices[symbols][~df_buy] * (1-impact)
    df_trades['Cash'] = 0.0-(df_trade_prices * df_trades).sum(axis = 1) - commission
    df_holdings['Cash'] = start_val
    df_holdings['Cash'] += df_trades['Cash'].cumsum()

    # df port_val
    df_port_val = (df_prices * df_holdings).sum(axis=1)
    df_port_val = pd.DataFrame( df_port_val, columns = ['value'] )

    if DEBUG:
        df_buy.to_csv('df_buy.csv')
        df_trades.to_csv('df_trades.csv')
        df_prices.to_csv('df_prices.csv')
        df_holdings.to_csv('df_holdings.csv')
        df_port_val.to_csv('df_port_val.csv')

    return df_port_val