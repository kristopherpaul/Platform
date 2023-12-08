from data_structures import *

def MACD(data: TimeArray, fast_period: int, slow_period: int, signal_period: int) -> (TimeArray, TimeArray, TimeArray, TimeArray):
    pass

def crossover(data1: TimeArray, data2: TimeArray) -> bool:
    pass

def crossunder(data1: TimeArray, data2: TimeArray) -> bool:
    return crossover(data2, data1)