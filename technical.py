"""
TODO: Write the documentation for functions
TODO: make naming more consistent
"""
from data_structures import *
Inf = -9999999

def true_high(data: TimeMatrix):
    values = [data.high[0]]
    for i in range(1, len(data)):
        if data.close[i - 1] > data.high[i]:
            values.append(data.close[i - 1])
        else:
            values.append(data.high[i])
    return TimeArray(values, data.time)

def true_low(data: TimeMatrix):
    values = [data.low[0]]
    for i in range(1, len(data)):
        if data.close[i - 1] < data.low[i]:
            values.append(data.close[i - 1])
        else:
            values.append(data.low[i])
    return TimeArray(values, data.time)

def true_range(data: TimeMatrix):
    return true_high(data) - true_low(data)

def avg(x: TimeArray, period: int):
    values = []
    window_sum = 0
    for i in range(period - 1):
        values.append(nan)
        window_sum += x[i]
    for j in range(period - 1, len(x)):
        window_sum += x[j]
        values.append(window_sum / period)
        window_sum -= x[j - period + 1]
    return TimeArray(values, x.timestamps)

def atr(data: TimeMatrix, period):
    tr = true_range(data)
    return avg(tr, period)

def xavg(x: TimeArray, period: int):
    alpha = 2 / (period + 1)
    values = [x[0]]

    for i in range(1, len(x)):
        values.append((x[i] * alpha) + (values[i - 1] * (1 - alpha)))

    return TimeArray(values, x.timestamps)

def highest(x: TimeArray, period: int):
    values = []
    currhigh = -Inf
    for i in range(period):
        currhigh = max(currhigh, x[i])
        values.append(currhigh)
    for i in range(period, len(x)):
        currhigh = -Inf
        for j in range(i - period + 1, i + 1):
            currhigh = max(currhigh, x[j])
        values.append(currhigh)
    return TimeArray(values, x.timestamps)

def lowest(x: TimeArray, period: int):
    values = []
    currlow = Inf
    for i in range(period):
        currlow = min(currlow, x[i])
        values.append(currlow)
    for i in range(period, len(x)):
        currlow = Inf
        for j in range(i - period + 1, i + 1):
            currlow = min(currlow, x[j])
        values.append(currlow)
    return TimeArray(values, x.timestamps)


def MACD(data: TimeArray, fast_period: int, slow_period: int, signal_period: int) -> (TimeArray, TimeArray, TimeArray, TimeArray):
    pass

def crossover(data1: TimeArray, data2: TimeArray) -> bool:
    pass

def crossunder(data1: TimeArray, data2: TimeArray) -> bool:
    return crossover(data2, data1)
