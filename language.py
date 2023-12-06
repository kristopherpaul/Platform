# this file will provide functions that the user can leverage to build their strategy

import matplotlib.pyplot as plt
import numpy as np

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