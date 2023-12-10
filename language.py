# this file will provide functions that the user can leverage to build their strategy

import matplotlib.pyplot as plt
import numpy as np

class Strategy:
    params = {}
    positions = []
    
    def __init__(self, name, universe, criteria=None, qty_type=None):
        pass
    
    def entry(self, id: str, direction: str, qty: int, limit: int = None):
        pass

    def exit(self, id: str, from_entry=None, qty: int, take_profit=None, stop_loss=None):
        pass

    def exit_all(self):
        pass

    def param(self, id, value, optimize=False):
        self.params[id] = value


def plot(data1, data2):
    plt.plot(data1)
    plt.plot(data2)
    plt.show()

def sma(data, column, window):
    new_data = data.copy()
    new_data[f'SMA_{window}'] = data[column].rolling(window).mean()
    return new_data

def ema(data, column, alpha):
    new_data = data.copy()
    new_data[f'EMA_{alpha}'] = data[column].ewm(alpha=alpha, adjust=False).mean()
    return new_data