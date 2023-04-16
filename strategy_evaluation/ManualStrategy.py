""""""
"""MC2-P8: strategy evaluation.

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

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
from indicators import Indicators
import matplotlib.pyplot as plt

DEBUG = 1

def author(self):
    return 'pjiang49'

def testPolicy(
        symbol = 'JPM',
        sd=dt.datetime(2010, 1, 1),
        ed=dt.datetime(2011, 12, 31),
        sv = 100000):
    """
    :param symbol: The stock symbol that you trained on on
    :type symbol: str
    :param sd: A datetime object that represents the start date, defaults to 1/1/2008
    :type sd: datetime
    :param ed: A datetime object that represents the end date, defaults to 1/1/2009
    :type ed: datetime
    :param sv: The starting value of the portfolio
    :type sv: int
    :return: A DataFrame with values representing trades for each day. Legal values are +1000.0 indicating
        a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING.
        Values of +2000 and -2000 for trades are also legal when switching from long to short or short to
        long so long as net holdings are constrained to -1000, 0, and 1000.
    :rtype: pandas.DataFrame
    """
    #eval states
    dates = pd.date_range(sd, ed)
    df_prices = get_data([symbol], dates)
    df_prices = df_prices[symbol]

    lookback = 14
    p_sma = Indicators.p_sma(symbol, sd, ed, lookback)
    bbp = Indicators.bbp(symbol, sd, ed, lookback)
    cci = Indicators.cci(symbol, sd, ed, lookback)

    decisions = pd.DataFrame(index = df_prices.index)
    decisions['bbp'] = [-1 if x > 0.9 else 1 if x < 0.1 else 0 for x in bbp[symbol]]
    decisions['sma'] = [-1 if x > 1.05 else 1 if x < 0.95 else 0 for x in p_sma[symbol]]
    decisions['cci'] = [+1 if x > 100 else -1 if x < -100 else 0 for x in cci[symbol]]
    decisions['holding'] = [0 if x == 0 else +1000 if x > 0 else -1000 for x in decisions.sum(axis = 1)]
    decisions['trades'] = decisions.iloc[1:]['holding'] - decisions.iloc[:-1]['holding'].values
    decisions['trades'].iloc[0] = 0
    df_trades = decisions['trades'].to_frame()
    df_trades.rename(columns = {'trades':symbol},inplace = True)
    if DEBUG:
        df_trades.to_csv("df_trades.csv")
        decisions.to_csv('decision.csv')
    return df_trades

def _build_df_orders(_df_trades, symbol):
    """
    Convert _df_trades to the following format
        Date,Symbol,Order,Shares
        2011-01-10,AAPL,BUY,1500
        2011-01-13,AAPL,SELL,1500
    """
    columns = ['Date','Symbol','Order','Shares']
    df_orders = _df_trades.copy()
    df_orders = df_orders[_df_trades[symbol]!=0]
    df_orders['Date'] = df_orders.index.map(lambda x: x.strftime('%Y-%m-%d'))
    df_orders['Symbol'] = symbol
    df_orders['Order'] = df_orders[symbol].map( lambda x: 'BUY' if x>0 else 'SELL' )
    df_orders['Shares'] = df_orders[symbol].map(lambda x: x if x>0 else -x)
    df_orders.drop(symbol, axis = 1, inplace = True)
    return df_orders


if __name__ == "__main__":
    df_trades = testPolicy(symbol='JPM',
                     sd=dt.date(2010,1,1),
                     ed=dt.date(2011,12,31),
                     sv=100000)
    df_orders = _build_df_orders(df_trades,symbol='JPM')
    print(df_orders.head())

