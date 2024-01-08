"""
Notes:
1. currently exit strat is the opposite of the entry strat
2. not sure but I don't think backtest needs to be a class, could do with a function too
3. Same with Order, maybe can just get away with a tuple
4. TODO: implement the functionality for having multiple orders and positions at once
5. Maybe a way to handle indicators used by the user without passing in the index
"""
from data_structures import *
import pandas as pd

# ---------------------------------------------------Preprocessing---------------------------------------------------------------
papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = OHLC(papadata)
# -------------------------------------------------------------------------------------------------------------------------------


class Order:
    def __init__(self, order_type, price):
        self.order_type = order_type
        self.price = price

class Backtest:
    def __init__(self, long_strat, short_strat, data: OHLC):
        self.signal = []
        self.data = data
        self.timestamps = []
        self.entryprice = []
        self.exitprice = []
        self.current_order = None
        self.current_position = None
        self.index = None
        self.long_strat = long_strat
        self.short_strat = short_strat
        self.initial_capital = 1000000

    def ltohlc(self):
        return self.data[self.index]

    def place_order(self, order_type, price):
        self.current_order = Order(order_type, price)

    def check_order(self):
        if self.current_order.order_type == "buy" and self.long_strat(self.ltohlc(), self.index) is None:
            self.current_order = None
        elif self.current_order.order_type == "sell" and self.short_strat(self.ltohlc(), self.index) is None:
            self.current_order = None

    def execute_order(self):
        if self.current_order.order_type == "buy":
            if self.ltohlc.high > self.current_order.price + 0.05:
                self.signal.append('buy')
                self.timestamps.append(self.data.time[self.index])
                self.entryprice.append(self.current_order.price)
                if self.current_position is not None:
                    self.exitprice.append(self.current_order.price)
                self.current_position = "buy"
                self.current_order = None
        else:
            if self.ltohlc.low < self.current_order.price - 0.05:
                self.signal.append('sell')
                self.timestamps.append(self.data.time[self.index])
                self.entryprice.append(self.current_order.price)
                if self.current_position is not None:
                    self.exitprice.append(self.current_order.price)
                self.current_position = "sell"
                self.current_order = None

    def run(self):
        # Yes, I'm aware of that lingering 65 there
        for self.index in range(65, len(self.data)):
            if self.current_order is not None:
                self.execute_order()

            if self.current_order is not None:
                self.check_order()

            if self.current_position == "buy" and self.current_order is None:
                price = self.short_strat(self.ltohlc(), self.index)
                if price is not None:
                    self.place_order("sell", price)

            elif self.current_position == "sell" and self.current_order is None:
                price = self.long_strat(self.ltohlc(), self.index)
                if price is not None:
                    self.place_order("buy", price)

            elif self.current_position is None and self.current_order is None:
                price1 = self.long_strat(self.ltohlc(), self.index)
                price2 = self.short_strat(self.ltohlc(), self.index)
                if price1 is not None:
                    self.place_order("buy", price1)
                elif price2 is not None:
                    self.place_order("sell", price2)
        self.exitprice.append(None)

    def cumulative_pnl(self):
        # TODO: implement the function
        pass

    def stats(self):
        pass

open = data.open
high = data.high
low = data.low
close = data.close