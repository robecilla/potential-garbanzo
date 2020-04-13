import backtrader as bt


class TestStrategy(bt.Strategy):
    '''
    This is a simple mean reversion bollinger band strategy.

    Entry Critria:
        - Long:
            - Price closes below the lower band
            - Stop Order entry when price crosses back above the lower band
        - Short:
            - Price closes above the upper band
            - Stop order entry when price crosses back below the upper band
    Exit Critria
        - Long/Short: Price touching the median line
    '''

    params = (
        ("period", 20),
        ("devfactor", 2),
        ("debug", False)
    )

    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        self.boll = bt.indicators.BollingerBands(period=self.p.period, devfactor=self.p.devfactor)
        # self.sx = bt.indicators.CrossDown(self.data.close, self.boll.lines.top)
        # self.lx = bt.indicators.CrossUp(self.data.close, self.boll.lines.bot)

    def next(self):

        orders = self.broker.get_orders_open()
        size = self.getsizing()

        # Cancel open orders so we can track the median line
        if orders:
            for order in orders:
                self.broker.cancel(order)

        if not self.position:

            if self.data.close > self.boll.lines.top:
                self.log(f'Price: {self.boll.lines.top[0]}')
                price = self.boll.lines.top[0] * (1 + 0.05)
                self.log(f'Stop Price: {price}')
                self.sell(exectype=bt.Order.Stop, price=self.boll.lines.top[0])

            if self.data.close < self.boll.lines.bot:
                self.log(f'Price: {self.boll.lines.bot[0]}')
                price = self.boll.lines.bot[0] * (1 - 0.05)
                self.log(f'Stop Price: {price}')
                self.buy(exectype=bt.Order.Stop, price=self.boll.lines.bot[0])


        else:

            if self.position.size > 0:
                self.sell(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.position.size)

            else:
                self.buy(exectype=bt.Order.Limit, price=self.boll.lines.mid[0], size=self.position.size)

        if self.p.debug:
            print('---------------------------- NEXT ----------------------------------')
            print("1: Data Name:                            {}".format(self.data._name))
            print("2: Bar Num:                              {}".format(len(self.data)))
            print("3: Current date:                         {}".format(self.data.datetime.datetime()))
            print('4: Open:                                 {}'.format(self.data.open[0]))
            print('5: High:                                 {}'.format(self.data.high[0]))
            print('6: Low:                                  {}'.format(self.data.low[0]))
            print('7: Close:                                {}'.format(self.data.close[0]))
            print('8: Volume:                               {}'.format(self.data.volume[0]))
            print('9: Position Size:                       {}'.format(self.position.size))
            print('--------------------------------------------------------------------')

    def notify_trade(self, trade):
        if trade.isclosed:
            dt = self.data.datetime.date()

            print('---------------------------- TRADE ---------------------------------')
            print("1: Data Name:                            {}".format(trade.data._name))
            print("2: Bar Num:                              {}".format(len(trade.data)))
            print("3: Current date:                         {}".format(dt))
            print('4: Status:                               Trade Complete')
            print('5: Ref:                                  {}'.format(trade.ref))
            print('6: PnL:                                  {}'.format(round(trade.pnl, 2)))
            print('7: Volumen:                              {}'.format(self.data.volume[0]))
            print('8: Size:                                 {}'.format(self.getsizing()))
            print('9: Trade total:                          {}'.format(self.getsizing() * trade.price))
            print('--------------------------------------------------------------------')


