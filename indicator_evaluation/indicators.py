""""""
"""MC2-P1: indicators.

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
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

DEBUG = 0


def author():
    """
    :return: The GT username of the student
    :rtype: str
    """
    return "pjiang49"  # replace tb34 with your Georgia Tech username


class Indicators:
    def sma(sym, sd, ed, lookback=14):
        """
        sma: simple moving average
        return: 1-column dataframe with sma timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        sma = df_price.rolling(window=lookback, min_periods=lookback).mean()
        sma_normalized = sma/sma.iloc[lookback]
        return sma, sma_normalized

    def ema(sym, sd, ed, span=12):
        """
        ema: exponential moving average with a certain span
        return: 1-column dataframe with sma timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        ema = df_price.ewm(span=span).mean()
        return ema

    def macd(sym, sd, ed):
        """
        macd:   MACD~line=EMA_{12}-EMA_{26}}
                Signal~line=EMA_{9}(MACD~line)}
        return: 1-column dataframe with sma timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        ema12 = df_price.ewm(span=12).mean()
        ema26 = df_price.ewm(span=26).mean()
        macd = ema12 - ema26
        macd_signal_line = macd.ewm(span=9).mean()
        return macd, macd_signal_line

    def bbp(sym, sd, ed, lookback=14):
        """
        Bollinger Band Percentage
        bbp := (price - sma) / (upperband - lowerband)
        return: 1-column dataframe with bbp timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        rolling_std = df_price.rolling(window=lookback, min_periods=lookback).std()
        sma = df_price.rolling(window=lookback, min_periods=lookback).mean()
        top_band = sma + 2.0 * rolling_std
        bottom_band = sma - 2.0 * rolling_std
        bbp = (df_price - bottom_band) / (top_band - bottom_band)
        return bbp, top_band, bottom_band

    def RSI(sym, sd, ed, lookback=14):
        """
        RSI: relative strength index
        RS := upgain / downloss
        RSI = 100 - 100/(1+RS)
        return: 1-column dataframe with RSI timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        daily_rets = df_price.copy()
        daily_rets.iloc[0] = np.nan
        daily_rets.iloc[1:] = df_price.iloc[1:] - df_price.iloc[0:].values
        upgain = daily_rets.copy()
        downloss = daily_rets.copy()
        upgain[:] = np.nna
        downloss[:] = np.nan
        for i in range(lookback - 1, daily_rets.shape[0] - 1):
            upgain.iloc[i] = daily_rets.iloc[i - lookback + 1: i + 1].where(daily_rets >= 0).sum()
            downloss.iloc[i] = -1.0 * daily_rets.iloc[i - lookback + 1: i + 1].where(daily_rets < 0).sum()
        rs = upgain / downloss
        rsi = 100 - 100 / (1 + rs)
        rsi.iloc[:lookback] = np.nan
        return rsi

    def momentum(sym, sd, ed, lookback=14):
        """
        momentum: return of a window of # of lookback days
        momentun = price[t]/price[t-lookback]-1
        return: 1-column dataframe with momentum timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        momentum = df_price.copy()
        momentum[:] = np.nan
        momentum.iloc[lookback:] = df_price.iloc[lookback:] / df_price.iloc[:-lookback].values - 1.0
        normalized_momentum = momentum.iloc[lookback:] / momentum.iloc[lookback]
        return momentum, normalized_momentum

    def cci(sym, sd, ed, lookback = 14):
        """
        cci: Commodity Channel Index of # of lookback days
        cci = (price[t]-sma[t])/(0.015 * mean deviation[t])
        return: 1-column dataframe with cci timeseries
        rtype: pd.DataFrame
        """
        df_price = get_data([sym], pd.date_range(sd, ed))
        df_price = df_price[[sym]]
        sma = df_price.rolling(window = lookback, min_periods = lookback).mean()
        std = df_price.rolling(window = lookback, min_periods = lookback).std()
        cci = (df_price - sma)/(0.015 * std)
        return cci


class Report(object):

    sym = "JPM"
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009, 12, 31)

    def implementPartII(self):
        df_price = get_data([self.sym], pd.date_range(self.sd, self.ed))
        df_price = df_price[[self.sym]]
        df_price_norm_line = df_price / df_price.iloc[0]

        # sma
        sma, sma_norm_line = Indicators.sma(self.sym, self.sd, self.ed, lookback=14)
        price_sma_line = df_price / sma
        plt.figure(figsize=(14, 8))
        plt.title("SMA")
        plt.xlabel("Date")
        plt.ylabel("SMA")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_price_norm_line, label="normalized price", color="blue")
        plt.plot(sma_norm_line, label="normalized sma", color="red")
        plt.plot(price_sma_line, label="price/sma", color="purple")
        plt.legend()
        plt.savefig("indicator_sma.png", bbox_inches='tight')
        plt.clf()

        # bbp
        bbp, top_band, bottom_band = Indicators.bbp(self.sym, self.sd, self.ed, lookback=14)
        plt.figure(figsize=(14, 8))
        plt.title("Bollinger Bands")
        plt.xlabel("Date")
        plt.ylabel("Price")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_price, label="Normalized price", color="blue")
        plt.plot(top_band, label="Top Bollinger Band", color="purple")
        plt.plot(bottom_band, label="Bottom Bollinger Band", color="purple")
        #plt.plot(bbp / bbp.iloc[0], label="Bollinger Band Percentage", color="red")
        plt.legend()
        plt.savefig("indicator_bbp.png", bbox_inches='tight')
        plt.clf()

        # momentum
        _, normalized_momentum = Indicators.momentum(self.sym, self.sd, self.ed, lookback=14)
        plt.figure(figsize=(14, 8))
        plt.title("Momentum")
        plt.xlabel("Date")
        plt.ylabel("Momentum")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_price_norm_line, label="Normalized price", color="blue")
        plt.plot(normalized_momentum, label="Momentum", color="red")
        plt.legend()
        plt.savefig("indicator_momentum.png", bbox_inches='tight')
        plt.clf()

        # cci
        cci = Indicators.cci(self.sym, self.sd, self.ed, lookback=14)
        plt.figure(figsize=(14, 8))
        plt.title("CCI")
        plt.xlabel("Date")
        plt.ylabel("CCI")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_price, label="Price", color="blue")
        plt.plot(cci, label="CCI", color="red")
        plt.legend()
        plt.savefig("indicator_cci.png", bbox_inches='tight')
        plt.clf()

        # cci
        macd, macd_sinal_line = Indicators.macd(self.sym, self.sd, self.ed)
        plt.figure(figsize=(14, 8))
        plt.title("MACD")
        plt.xlabel("Date")
        plt.ylabel("value")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(df_price_norm_line, label="Price", color="blue")
        plt.plot(macd, label="MACD", color="red")
        plt.plot(macd_sinal_line, label="MACD signal line", color="orange")
        plt.legend()
        plt.savefig("indicator_macd.png", bbox_inches='tight')
        plt.clf()


if __name__ == "__main__":
    Report().implementPartII()
