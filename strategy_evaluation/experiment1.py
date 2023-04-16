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
    symbol = 'JPM'
    ################### in-sample comparison ############################
    # ----- value of StrategyLearner portfolio
    ins_sl = sl.StrategyLearner(verbose = False, impact=0.0)
    df_trades_sl = ins_sl.add_evidence(symbol='JPM',
                       sd=dt.date(2008,1,1),
                       ed=dt.date(2009,12,31),
                       sv=100000)
    df_orders_sl = ins_sl._build_df_orders(df_trades_sl,'JPM')
    portvals_sl = compute_portvals(df_orders_sl, start_val = 100000)
    #print(portvals_sl)

    # ----- value of ManualStrategy portfolio
    df_trades_ms = ms.testPolicy(symbol='JPM',
                                 sd=dt.date(2008,1,1),
                                 ed=dt.date(2009,12,31),
                                 sv=100000)
    df_orders_ms = ms._build_df_orders(df_trades_ms,symbol='JPM')
    portvals_ms = compute_portvals(df_orders_ms, start_val = 100000)
    # print(portvals_ms)

    # ----- value of Benchmark portfolio
    dates = pd.date_range(dt.date(2008,1,1), dt.date(2009, 12, 31))
    df_prices = get_data(['JPM'], dates)
    df_prices = df_prices['JPM']
    df_orders_bm = pd.DataFrame([[df_prices.index.min().strftime('%Y-%m-%d'), 'JPM','BUY',1000],
                                 [df_prices.index.max().strftime('%Y-%m-%d'), 'JPM','SELL',1000],
                                 ],
                                columns = ['Date', 'Symbol', 'Order', 'Shares'])
    portvals_bm = compute_portvals(df_orders_bm, start_val=100000)
    # print(portvals_bm)

    portvals_ms = normalize_val(portvals_ms)
    portvals_sl = normalize_val(portvals_sl)
    portvals_bm = normalize_val(portvals_bm)

    chart_df = pd.concat([portvals_ms, portvals_sl, portvals_bm], axis=1)
    chart_df.columns = ['Manual Strategy', 'Strategy Learner', 'Benchmark']
    chart_df.plot(grid=True, title='Comparing Strategies', use_index=True, color=['Red', 'Blue', 'Purple'])
    plt.title("In-Sample Comparison")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.savefig('images/In-Sample-Comparison.png')
    plt.clf()

    ################### out-of-sample comparison ############################
    # ----- value of StrategyLearner portfolio
    df_trades_sl = ins_sl.testPolicy(symbol='JPM',
                     sd=dt.date(2010,1,1),
                     ed=dt.date(2011,12,31),
                     sv=100000)
    df_orders_sl = ins_sl._build_df_orders(df_trades_sl,'JPM')
    portvals_sl = compute_portvals(df_orders_sl, start_val = 100000)

    # ----- value of Manual portfolio
    df_trades_ms = ms.testPolicy(symbol='JPM',
                                 sd=dt.date(2010,1,1),
                                 ed=dt.date(2011,12,31),
                                 sv=100000)
    df_orders_ms = ms._build_df_orders(df_trades_ms,symbol='JPM')
    portvals_ms = compute_portvals(df_orders_ms, start_val = 100000)
    # print(portvals_ms)

    # ----- value of StrategyLearner portfolio
    dates = pd.date_range(dt.date(2010, 1, 1), dt.date(2011, 12, 31))
    df_prices = get_data(['JPM'], dates)
    df_prices = df_prices['JPM']
    df_orders_bm = pd.DataFrame([[df_prices.index.min().strftime('%Y-%m-%d'), 'JPM', 'BUY', 1000],
                                 [df_prices.index.max().strftime('%Y-%m-%d'), 'JPM', 'SELL', 1000],
                                 ],
                                columns = ['Date', 'Symbol', 'Order', 'Shares'])
    portvals_bm = compute_portvals(df_orders_bm, start_val=100000)

    # normalize
    portvals_ms = normalize_val(portvals_ms)
    portvals_sl = normalize_val(portvals_sl)
    portvals_bm = normalize_val(portvals_bm)

    chart_df = pd.concat([portvals_ms, portvals_sl, portvals_bm], axis=1)
    chart_df.columns = ['Manual Strategy', 'Strategy Learner', 'Benchmark']
    chart_df.plot(grid=True, title='Comparing Strategies', use_index=True, color=['Red', 'Blue', 'Purple'])
    plt.title("Out-Of-Sample Comparison")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.savefig('images/Out-Of-Sample Comparison.png')
    plt.clf()

def normalize_val(prices):
    return prices / prices.iloc[0]

def author():
    return 'pjiang49'

if __name__ == "__main__":
    plot_results()