""""""
"""MC2-P1: theoretically optimal strategy.

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

"""
Policy:
If price goes up tomorrow, I long to maximize my position to +1000;
If price goes down tomorrow, I short to minimize my position to -1000.

Possible positions:
[-1000, 0, +1000]

Possible trades to make per day:
[-2000, -1000, 0, 1000, 2000]
"""
import datetime as dt

from util import *
DEBUG = 0


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "pjiang49"  # replace tb34 with your Georgia Tech username



def testPolicy(symbol="AAPL", sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011, 12, 31), sv=100000):
    """
    The input parameters are:
        symbol: the stock symbol to act on
        sd: A DateTime object that represents the start date
        ed: A DateTime object that represents the end date
        sv: Start value of the portfolio

    return val:
        df_trades: A single column data frame, indexed by date, whose values represent trades for each trading day (from the start date to the end date of a given period). Legal values are +1000.0 indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal so long as net holdings are constrained to -1000, 0, and 1000. Note: The format of this data frame differs from the one developed in a prior project.
    """
    # df prices
    df_prices = get_data([symbol], pd.date_range(sd, ed))
    df_prices = df_prices[[symbol]] # remove spy

    # df_holdings
    df_holdings = df_prices.copy()
    df_holdings[:] = 0

    df_return_1 = df_prices[1:].values - df_prices[:-1]
    df_holdings[df_return_1 < 0] = -1000
    df_holdings[df_return_1 > 0] = +1000

    # df_trades
    df_trades = df_prices.copy()
    df_trades[:] = 0
    df_trades.iloc[0] = df_holdings.iloc[0]
    df_trades[1:] = df_holdings[1:] - df_holdings[0:-1].values

    if DEBUG:
        df_prices.to_csv("tos_df_prices.csv")
        df_return_1.to_csv("tos_df_return_1.csv")
        df_holdings.to_csv("tos_df_holdings.csv")
        df_trades.to_csv("tos_df_trades.csv")

    return df_trades


