from data_structures import *
from technical import *

class Order:
    def __init__(self, order_type, price):
        self.order_type = order_type
        self.price = price

    def execute(self):


class Backtest:
    def __init__(self, buy_strat, sell_strat, data: TimeMatrix):
        self.signal = []
        self.data = data
        self.timestamps = []
        self.entryprice = []
        self.exitprice = []
        self.current_order = None
        self.curr_position = None
        self.index = None
        self.long_strat = long_strat
        self.short_strat = short_strat

    def place_order(order_type, price):

    def ltohlc(self):
        return self.data.iloc[self.index]

    def run(data):
        # Yes, I'm aware of that lingering 65 there
        for self.index in range(65, len(data)):
            if self.curr_position == 'buy':
                price = self.buy_strat(self.ltohlc[self.index])

#this file will provide functions that the user can leverage to build their strategy
#
#import matplotlib.pyplot as plt
#import numpy as np
#
#class Strategy:
#    def __init__(self, name, universe, criteria=None, qty_type=None):
#        pass
#
#    def entry(self, id, direction, qty, limit=None):
#        pass
#
#    def exit(self, id, from_entry, qty, take_profit=None, stop_loss=None):
#        pass
#
#    def param(self, id, value, optimize=False):
#        pass
#
#
#def plot(data1, data2):
#    plt.plot(data1)
#    plt.plot(data2)
#    plt.show()
#
#def sma(data, column, window):
#    new_data = data.copy()
#    new_data[f'SMA_{window}'] = data[column].rolling(window).mean()
#    return new_data
#
#def ema(data, column, alpha):
#    new_data = data.copy()
#    new_data[f'EMA_{alpha}'] = data[column].ewm(alpha=alpha, adjust=False).mean()
#    return new_data

