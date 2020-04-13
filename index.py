from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import pandas as pd
import yfinance as yf
from pandas_datareader import data as pdr


import datetime as dt # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])
import requests

# Import the backtrader platform
import backtrader as bt

from strategies.test_strategy import TestStrategy
from sizers.sizer import MaxRiskSizer


if __name__ == '__main__':

    # dynamic variables:
    #     - stake
    #     - margin
    #     - stops


    # Create a cerebro entity
    cerebro = bt.Cerebro()

    cerebro.addstrategy(TestStrategy)

    yf.pdr_override()

    startyear = 2020
    startmonth = 1
    startday = 1
    start = dt.datetime(startyear, startmonth, startday)
    end = dt.datetime.now()
    asset = "EURUSD=X"

    df = pdr.get_data_yahoo(asset, start, end)

    data = bt.feeds.PandasData(dataname=df)

    # Add the Data Feed to Cerebro
    cerebro.adddata(data)

    startcash = 1000.0
    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # Add a FixedSize sizer according to the stake
    # cerebro.addsizer(bt.sizers.FixedSize, stake=10)
    cerebro.addsizer(MaxRiskSizer, risk=0.2)

    # Set the commission
    cerebro.broker.setcommission(commission=0.0)

    # Print out the starting conditions
    print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # Run over everything
    cerebro.run()

    portvalue = cerebro.broker.getvalue()
    pnl = portvalue - startcash

    # Print out the final result
    print('----SUMMARY----')
    print('Final Portfolio Value: ${}'.format(portvalue))
    print('P/L: ${}'.format(pnl))

    cerebro.plot()
