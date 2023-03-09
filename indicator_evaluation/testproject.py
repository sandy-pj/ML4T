""""""
"""MC2-P1: test project .

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

import indicator_evaluation.TheoreticallyOptimalStrategy as tos
from indicator_evaluation.indicators import *
from indicator_evaluation.marketsimcode import *
import datetime as dt
import pandas as pd
import os
import matplotlib.pyplot as plt
from marketsimcode import compute_portvals

DEBUG = 1

def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "pjiang49"  # replace tb34 with your Georgia Tech username

class Report(object):
    symbol = 'JPM'
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009,12,31)
    sv = 100000

    def getBenchmarkPortfolioTrades(self):
        """
        return val:
            df_trades: A single column data frame, indexed by date, whose values represent trades for each trading day (from the start date to the end date of a given period). Legal values are +1000.0 indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal so long as net holdings are constrained to -1000, 0, and 1000. Note: The format of this data frame differs from the one developed in a prior project.
        """
        # df prices
        df_prices = get_data([self.symbol], pd.date_range(self.sd, self.ed))
        df_prices = df_prices[[self.symbol]]  # remove spy

        # df_trades
        df_trades = df_prices.copy()
        df_trades[:] = 0
        df_trades[self.symbol].iloc[0] = 1000

        """
        if DEBUG:
            df_trades.to_csv("benchmark_port_df_trades.csv") 
        """

        return df_trades

    def implementPartI(self):
        df_trades_benchmark = self.getBenchmarkPortfolioTrades()
        df_portval_benchmark = compute_portvals(df_trades_benchmark, start_val= self.sv, commission=0, impact=0)

        df_trades_tos = tos.testPolicy(symbol = self.symbol, sd = self.sd, ed = self.ed, sv = self.sv)
        df_portval_tos = compute_portvals(df_trades_tos, start_val= self.sv, commission=0, impact=0)

        # normalize
        df_portval_benchmark['cumulative_return'] = df_portval_benchmark / df_portval_benchmark.iloc[0]
        df_portval_tos['cumulative_return'] = df_portval_tos / df_portval_tos.iloc[0]


        plt.figure(figsize=(14, 8))
        plt.title("Cumulative Return: TOS vs. Benchmark")
        plt.xlabel("Date")
        plt.ylabel("Cumulative Return")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_portval_benchmark['cumulative_return'], label="benchmark", color="purple")
        plt.plot(df_portval_tos['cumulative_return'], label="tos", color="red")
        plt.legend()
        plt.savefig("report/CumulativeReturn.png", bbox_inches='tight')
        plt.clf()

        # stats
        benchmark_cum_ret = df_portval_benchmark['cumulative_return'][-1]
        benchmark_dai_std = df_portval_benchmark['value'].std(axis = 0)
        benchmark_mean = df_portval_benchmark['value'].mean(axis = 0)

        tos_cum_ret = df_portval_tos['cumulative_return'][-1]
        tos_dai_std = df_portval_tos['value'].std(axis = 0)
        tos_mean = df_portval_tos['value'].mean(axis = 0)

        report_dict = { 'TOS': {'cumulative_return': tos_cum_ret,
                                'daily_std': tos_dai_std,
                                'daily_mean': tos_mean },
                        'Benchmark': {'cumulative_return': benchmark_cum_ret,
                                'daily_std': benchmark_dai_std,
                                'daily_mean': benchmark_mean },
                        }
        df_report = pd.DataFrame(report_dict)
        df_report.to_csv('report/report.csv')


if __name__ == "__main__":
    df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)
    ins = Report()
    ins.implementPartI()
