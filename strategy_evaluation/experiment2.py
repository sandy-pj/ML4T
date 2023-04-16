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
def run():
    impact_list = [0, 0.0025, 0.0050]
    res_port_val = []
    res_num_trades = []
    res_sharpe_ratio = []
    for impact in impact_list:
        # value of StrategyLearner portfolio
        ins_sl = sl.StrategyLearner(verbose = False, impact=impact, commission=0)
        df_trades_sl = ins_sl.add_evidence(symbol='JPM',
                           sd=dt.date(2008,1,1),
                           ed=dt.date(2009,12,31),
                           sv=100000)
        df_trades_sl = ins_sl.testPolicy(symbol='JPM',
                                         sd=dt.date(2008, 1, 1),
                                         ed=dt.date(2009, 12, 31),
                                         sv=100000)
        df_orders_sl = ins_sl._build_df_orders(df_trades_sl,'JPM')
        # portfolio value
        portvals_sl = compute_portvals(df_orders_sl,
                                       start_val = 100000,
                                       commission=0,
                                       impact=impact)
        portvals_sl = normalize_val(portvals_sl)
        res_port_val.append(portvals_sl)
        # number of trades
        res_num_trades.append(len(df_orders_sl))
        # sharpe ratio
        res_sharpe_ratio.append( portvals_sl.mean()/portvals_sl.std() )

    ###
    df_impact = pd.DataFrame( res_port_val).T
    df_impact.columns = ['Impact 0',
                                              'Impact 0.0025',
                                              'Impact 0.0050']
    df_impact.plot(grid=True, use_index=True, color=['Red', 'Blue', 'Purple','Orange'])
    plt.title("Impact vs. Strategy Learner Performance")
    plt.xlabel("Date")
    plt.ylabel("Normalized Portfolio Value")
    plt.legend()
    plt.savefig('images/impact_vs_strategy_learner_performance.png')
    plt.clf()

    ###
    plt.plot(impact_list, res_num_trades, label = 'number of trades' )
    plt.title('Number of Trades vs. Impact')
    plt.xlabel("Impact")
    plt.ylabel("Number of Trades")
    plt.legend()
    plt.savefig('images/impact_vs_num_trades.png')
    plt.clf()

    ###
    plt.plot(impact_list, res_sharpe_ratio, label = 'Sharpe Ratio')
    plt.title('Sharpe Ratio vs. Impact')
    plt.xlabel("Impact")
    plt.ylabel("Sharpe Ratio")
    plt.legend()
    plt.savefig('images/impact_vs_sharpe_ratio.png')
    plt.clf()

def normalize_val(prices):
    return prices / prices.iloc[0]

def author():
    return 'pjiang49'

if __name__ == "__main__":
    run()