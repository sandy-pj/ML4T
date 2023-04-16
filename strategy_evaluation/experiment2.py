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
import datetime as dt
import numpy as np
import pandas as pd
import random

import QLearner as ql
from marketsimcode import compute_portvals
import ManualStrategy as ms
import indicators as ind
import util as ut
import StrategyLearner as sl
from matplotlib import cm as cm
from matplotlib import style
import matplotlib.pyplot as plt
from util import *
def plot_results():
    res = []
    for impact in [0, 0.005, 0.025, 0.05]:
        # value of StrategyLearner portfolio
        ins_sl = sl.StrategyLearner(verbose = False, impact=impact, commission= = 0)
        df_trades_sl = ins_sl.add_evidence(symbol='JPM',
                           sd=dt.date(2008,1,1),
                           ed=dt.date(2009,12,31),
                           sv=100000)
        df_orders_sl = ins_sl._build_df_orders(df_trades_sl,'JPM')
        portvals_sl = compute_portvals(df_orders_sl,
                                       start_val = 100000,
                                       commission=0,
                                       impact=0)
        #print(portvals_sl)

    # value of ManualStrategy portfolio
    df_trades_ms = ms.testPolicy(symbol='JPM',
                                 sd=dt.date(2010,1,1),
                                 ed=dt.date(2011,12,31),
                                 sv=100000)
    df_orders_ms = ms._build_df_orders(df_trades_ms,symbol='JPM')
    portvals_ms = compute_portvals(df_orders_ms, start_val = 100000)
    print(portvals_ms)

    # value of Benchmark portfolio
        # format
        # Date, Symbol, Order, Shares
        # 2011 - 01 - 10, AAPL, BUY, 1500
        # 2011 - 01 - 13, AAPL, SELL, 1500

    dates = pd.date_range(dt.date(2010,1,1), dt.date(2011, 12, 31))
    df_prices = get_data(['JPM'], dates)
    df_prices = df_prices['JPM']
    df_orders_bm = pd.DataFrame([[df_prices.index.min().strftime('%Y-%m-%d'), 'JPM','BUY',1000],
                                 [df_prices.index.max().strftime('%Y-%m-%d'), 'JPM','SELL',1000],
                                 ],
                                columns = ['Date', 'Symbol', 'Order', 'Shares'])
    portvals_bm = compute_portvals(df_orders_bm, start_val=100000)
    print(portvals_bm)

    # normalize
    portvals_ms = normalize_val(portvals_ms)
    portvals_sl = normalize_val(portvals_sl)
    portvals_bm = normalize_val(portvals_bm)

    chart_df = pd.concat([portvals_ms, portvals_sl, portvals_bm], axis=1)
    chart_df.columns = ['Manual Strategy', 'Strategy Learner', 'Benchmark']
    chart_df.plot(grid=True, title='Comparing Strategies', use_index=True, color=['Red', 'Blue', 'Purple'])
    plt.show()

def normalize_val(prices):
    #fill_missing_values(prices)
    return prices / prices.iloc[0]

def get_the_first_trading_day_between(sd, ed, symbol):
    dates = pd.date_range(sd, ed)
    df_prices = get_data([symbol], dates)
    df_prices = df_prices[symbol]
    first_trading_date = df_prices.index.min()
    return first_trading_date

# def fill_missing_values(prices):
#     """Fill missing values in data frame, in place."""
#     prices.fillna(method='ffill', inplace=True)
#     prices.fillna(method='bfill', inplace=True)

def author():
    return 'pjiang49'

if __name__ == "__main__":
    plot_results()