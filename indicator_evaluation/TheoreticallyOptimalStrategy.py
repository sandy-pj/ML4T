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
    df_orders = pd.read_csv(orders_file, parse_dates=['Date', ],
                            usecols=['Date', 'Symbol', 'Order', 'Shares'])
    df_orders.sort_index(inplace=True)

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
        _market_impact_fac = (1 + impact) if _direction == 1 else (1 - impact)
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
    df_port_val = df_values.sum(axis=1)

    if DEBUG:
        df_orders.to_csv('df_orders.csv')
        df_trades.to_csv('df_trades.csv')
        df_prices.to_csv('df_prices.csv')
        df_holdings.to_csv('df_holdings.csv')
        df_values.to_csv('df_values.csv')
        df_port_val.to_csv('df_port_val.csv')
    return df_port_val

def testPolicy(symbol=”AAPL”, sd=dt.datetime(2010, 1, 1), ed=dt.datetime(2011,12,31), sv = 100000):
    """
    The input parameters are:
        symbol: the stock symbol to act on
        sd: A DateTime object that represents the start date
        ed: A DateTime object that represents the end date
        sv: Start value of the portfolio

    return val:
        df_trades: A single column data frame, indexed by date, whose values represent trades for each trading day (from the start date to the end date of a given period). Legal values are +1000.0 indicating a BUY of 1000 shares, -1000.0 indicating a SELL of 1000 shares, and 0.0 indicating NOTHING. Values of +2000 and -2000 for trades are also legal so long as net holdings are constrained to -1000, 0, and 1000. Note: The format of this data frame differs from the one developed in a prior project.
    """
    # df price
    df_price = get_data(symbol, pd.date_range(sd, ed))

    # df_holding
    df_holding = df_price.copy()
    df_holding.iloc[:] = 0

    df_ind = df_price.iloc[1:] - df_price.iloc[0:-1]
    df_holding[ df_ind < 0] = +1000
    df_holding[ df_ind > 0 ] = -1000

    # df_trades
    df_trades = df_price.copy()
    df_trades.iloc[1:] = df_holding[1:] - df_holding[0:-1]
    df_trades.iloc[-1] = 0

    return df_trades



