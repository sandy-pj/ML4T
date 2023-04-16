""""""  		  	   		  		 			  		 			     			  	 
"""  		  	   		  		 			  		 			     			  	 
Template for implementing StrategyLearner  (c) 2016 Tucker Balch  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
import random  		  	   		  		 			  		 			     			  	 
from indicators import Indicators
import pandas as pd  		  	   		  		 			  		 			     			  	 
import util as ut
import QLearner as ql
from marketsimcode import *
import numpy as np
DEBUG = 0
VERBOSE = False
  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
class StrategyLearner(object):  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    A strategy learner that can learn a trading policy using the same indicators used in ManualStrategy.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
    :param verbose: If “verbose” is True, your code can print out information for debugging.  		  	   		  		 			  		 			     			  	 
        If verbose = False your code should not generate ANY output.  		  	   		  		 			  		 			     			  	 
    :type verbose: bool  		  	   		  		 			  		 			     			  	 
    :param impact: The market impact of each transaction, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type impact: float  		  	   		  		 			  		 			     			  	 
    :param commission: The commission amount charged, defaults to 0.0  		  	   		  		 			  		 			     			  	 
    :type commission: float  		  	   		  		 			  		 			     			  	 
    """  		  	   		  		 			  		 			     			  	 
    # constructor  		  	   		  		 			  		 			     			  	 
    def __init__(self, verbose=False, impact=0.0, commission=0.0):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Constructor method  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        self.verbose = verbose  		  	   		  		 			  		 			     			  	 
        self.impact = impact  		  	   		  		 			  		 			     			  	 
        self.commission = commission

        # prepare for QLearner
        self.num_bins = 10
        self.ql = ql.QLearner(num_states=1000, num_actions=3, alpha=0.2, gamma=0.9, rar=0.5, radr=0.99, dyna=0, verbose=False)

    def _discretize(self, indicators):
        group_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        _, sma_bins = pd.qcut(indicators['p_sma'], self.num_bins, retbins = True)
        _, bbp_bins = pd.qcut(indicators['bbp'], self.num_bins, retbins=True)
        _, cci_bins = pd.qcut(indicators['cci'], self.num_bins, retbins=True)
        state = pd.DataFrame(index = indicators.index)
        state['sma_state'] = pd.cut(indicators['p_sma'], bins = sma_bins, labels=group_names)
        state['bbp_state'] = pd.cut(indicators['bbp'], bins = bbp_bins, labels=group_names)
        state['cci_state'] = pd.cut(indicators['cci'], bins = cci_bins, labels=group_names)
        state['state'] = state['sma_state'].astype(str) + state['bbp_state'].astype(str) + \
                         state['cci_state'].astype(str)
        state['state'] = state['state'].apply( lambda x: 0 if 'nan' in x else int(x) )
        state.drop('sma_state', axis=1, inplace=True)
        state.drop('bbp_state', axis=1, inplace=True)
        state.drop('cci_state', axis=1, inplace=True)
        if DEBUG:
            state.to_csv('state.csv')
        return state

    def _get_daily_return(self, port_val):
        daily_returns = port_val.copy()
        daily_returns.iloc[1:] = daily_returns.iloc[1:] - daily_returns.iloc[:-1].values
        daily_returns.iloc[0] = 0
        return daily_returns
  		  	   		  		 			  		 			     			  	 
    # this method should create a QLearner, and train it for trading  		  	   		  		 			  		 			     			  	 
    def add_evidence(  		  	   		  		 			  		 			     			  	 
        self,  		  	   		  		 			  		 			     			  	 
        symbol="IBM",  		  	   		  		 			  		 			     			  	 
        sd=dt.date(2008, 1, 1),
        ed=dt.date(2009, 1, 1),
        sv=10000,  		  	   		  		 			  		 			     			  	 
    ):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Trains your strategy learner over a given time frame.  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        :param symbol: The stock symbol to train on  		  	   		  		 			  		 			     			  	 
        :type symbol: str  		  	   		  		 			  		 			     			  	 
        :param sd: A datetime object that represents the start date, defaults to 1/1/2008  		  	   		  		 			  		 			     			  	 
        :type sd: datetime  		  	   		  		 			  		 			     			  	 
        :param ed: A datetime object that represents the end date, defaults to 1/1/2009  		  	   		  		 			  		 			     			  	 
        :type ed: datetime  		  	   		  		 			  		 			     			  	 
        :param sv: The starting value of the portfolio  		  	   		  		 			  		 			     			  	 
        :type sv: int  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        # add your code to do learning here  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
        # example usage of the old backward compatible util function  		  	   		  		 			  		 			     			  	 
        syms = [symbol]  		  	   		  		 			  		 			     			  	 
        dates = pd.date_range(sd, ed)  		  	   		  		 			  		 			     			  	 
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY  		  	   		  		 			  		 			     			  	 
        prices = prices_all[syms]  # only portfolio symbols  		  	   		  		 			  		 			     			  	 
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later  		  	   		  		 			  		 			     			  	 
        if self.verbose:  		  	   		  		 			  		 			     			  	 
            print(prices)

        # calculate indicators
        lookback = 14
        p_sma = Indicators.p_sma(symbol, sd, ed, lookback)
        bbp = Indicators.bbp(symbol, sd, ed, lookback)
        cci = Indicators.cci(symbol, sd, ed, lookback)
        indicators = pd.concat([p_sma, bbp, cci], axis=1)
        indicators.columns = ['p_sma', 'bbp', 'cci']
        state = self._discretize(indicators)
        daily_return = self._get_daily_return(prices)
        if DEBUG:
            daily_return.to_csv('daily_return.csv')

        # initial state
        initial_state = state['state'].iloc[0]
        self.ql.querysetstate(initial_state)

        # interation
        # df_holding = pd.Series(index = prices.index)
        prices['holding'] = 0
        i=0
        converged = False
        while not converged or i < 10:
            i += 1
            df_holding_prev = prices['holding'].copy()
            holding = 0
            transaction_cost = 0
            for date, price in prices.iterrows():
                reward = holding * daily_return[symbol].loc[date] - transaction_cost
                if VERBOSE:
                    print("reward = {} | holding = {} | daily_return = {}".format(reward, holding, daily_return[symbol].loc[date]))
                a = self.ql.query(state['state'].loc[date], reward)
                if a == 0:
                    prices['holding'].loc[date] = +1000
                elif a == 1:
                    prices['holding'].loc[date] = -1000
                elif a == 2:
                    prices['holding'].loc[date] = 0
                dholding = prices['holding'].loc[date] - holding
                transaction_cost = np.abs(dholding*prices[symbol].loc[date]*self.impact)+self.commission
                holding = prices['holding'].loc[date]
            if prices['holding'].equals(df_holding_prev):
                converged = True

        print("Stopped after {} iterations".format(i))
        price['trades'] = prices['holding'].iloc[1:] - prices['holding'].iloc[:-1].values
        price['trades'].iloc[0] = 0
        df_trades = price['trades'].to_frame(symbol)
        # df_trades.to_csv('df_trades_QL_training.csv')
        return df_trades

  		  	   		  		 			  		 			     			  	 
    # this method should use the existing policy and test it against new data  		  	   		  		 			  		 			     			  	 
    def testPolicy(  		  	   		  		 			  		 			     			  	 
        self,  		  	   		  		 			  		 			     			  	 
        symbol="IBM",  		  	   		  		 			  		 			     			  	 
        sd=dt.date(2009, 1, 1),
        ed=dt.date(2010, 1, 1),
        sv=10000,  		  	   		  		 			  		 			     			  	 
    ):  		  	   		  		 			  		 			     			  	 
        """  		  	   		  		 			  		 			     			  	 
        Tests your learner using data outside of the training data  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
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
  		  	   		  		 			  		 			     			  	 
        # here we build a fake set of trades  		  	   		  		 			  		 			     			  	 
        # your code should return the same sort of data  		  	   		  		 			  		 			     			  	 
        syms = [symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all["SPY"]  # only SPY, for comparison later
        if self.verbose:
            print(prices)

        # calculate indicators
        lookback = 14
        p_sma = Indicators.p_sma(symbol, sd, ed, lookback)
        bbp = Indicators.bbp(symbol, sd, ed, lookback)
        cci = Indicators.cci(symbol, sd, ed, lookback)
        indicators = pd.concat([p_sma, bbp, cci], axis=1)
        indicators.columns = ['p_sma', 'bbp', 'cci']
        state = self._discretize(indicators)
        daily_return = self._get_daily_return(prices)

        # QLearner query
        df_holding = prices.copy()
        df_holding.loc[:] = 0
        df_holding['Cash'] = 0
        df_holding['Cash'].iloc[0] = sv
        df_trade = prices.copy()
        df_trade.loc[:] = 0
        holding_prev = 0
        date_prev = prices.index[0]
        for date in prices.index[1:-1]:
            a = self.ql.querysetstate(state['state'].loc[date])
            if a == 0:
                df_holding[symbol].loc[date] = +1000
            elif a == 1:
                df_holding[symbol].loc[date] = -1000
            elif a == 2:
                df_holding[symbol].loc[date] = 0
            trade = df_holding[symbol].loc[date] - holding_prev
            df_trade[symbol].loc[date] = trade
            df_holding['Cash'].loc[date] = df_holding['Cash'].loc[date_prev]\
                                           - trade * prices[symbol].loc[date] * (1-self.impact)
            holding_prev = df_holding[symbol].loc[date]
            date_prev = date
        # clear position at the end date
        trade = 0 - holding_prev
        df_trade[symbol].loc[prices.index[-1]] = trade
        df_holding['Cash'].loc[prices.index[-1]] = df_holding['Cash'].loc[date_prev] \
                                       - trade * prices[symbol].loc[prices.index[-1]] * (1 - self.impact)

        if DEBUG:
            df_holding.to_csv("df_holding_QL_test.csv")
            df_trade.to_csv("df_trade_QL_test.csv")
            df_orders = self._build_df_orders(df_trade, symbol)
            df_orders.to_csv('df_orders.csv')
            df_port_val = compute_portvals( df_orders,
                              start_val=sv,
                              commission=0,
                              impact=self.impact)
            df_port_val.to_csv("df_port_val_StrategyLearner_test.csv")

        return df_trade

    def _build_df_orders(self, _df_trades, symbol):
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
        df_orders.drop(symbol, axis = 1)
        return df_orders


  		  	   		  		 			  		 			     			  	 
  		  	   		  		 			  		 			     			  	 
if __name__ == "__main__":  		  	   		  		 			  		 			     			  	 
    print("One does not simply think up a strategy")

    ins = StrategyLearner(impact = 0.05,commission=0)
    df_trades = ins.add_evidence(symbol='JPM',
                     sd=dt.date(2008,1,1),
                     ed=dt.date(2009,12,31),
                     sv=100000)
    # df_trades = ins.testPolicy(symbol='JPM',
    #                  sd=dt.date(2010,1,1),
    #                  ed=dt.date(2011,12,31),
    #                  sv=100000)
    df_orders = ins._build_df_orders(df_trades, 'JPM')
    # portfolio value
    portvals = compute_portvals(df_orders,
                                   start_val=100000,
                                   commission=0,
                                   impact=0.05)
    portvals.to_csv('portvals.csv')