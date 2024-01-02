from abc import ABC, abstractmethod
from typing import final
from data_structures import *
import pandas as pd
from technical import *

papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = OHLC(papadata)
# -------------------------------------------------------------------------------------------------------------------------------

#class _InternalDS:
#    def __init__(self2, values):
#        self2.values = values
#    def __getitem__(self2, i: int = 0):
#        return self2.values[self.index - i]

class Root:
    def __init__(self, data: OHLC):
        self.barIndex = 0
        self.data = data
        self.time = self.data.time
        self._len = len(self.data)
        self.initializeStructures()
        self.initializeOHLC()
        self.initializeTechnical()

    def initializeStructures(self):
        class BarDS:
            def __init__(bar, time_array: TimeArray):
                """
                data must have a time column indexed by 'time'
                """
                bar.values = time_array.values
                bar.timestamps = time_array.timestamps

            def __len__(bar):
                return len(bar.values)

            def __getitem__(bar, i: int):
                return bar.values[self.barIndex - i]

            def getAt(bar, i: int):
                return bar.values[i]

            def __repr__(bar):
                ret = "Time \t\t\t Value"

                if len(bar.values) <= 15:
                    for i in range(len(bar.values)):
                        ret += '\n'
                        ret += f"{np.datetime_as_string(bar.timestamps[i], 'm').replace('T', ' ')} \t {bar.values[i]}"
                else:
                    for i in range(5):
                        ret += '\n'
                        ret += f"{np.datetime_as_string(bar.timestamps[i], 'm').replace('T', ' ')} \t {bar.values[i]}"
                    ret += '\n... \t\t\t ...'
                    for i in range(len(bar.values) - 5, len(bar.values)):
                        ret += '\n'
                        ret += f"{np.datetime_as_string(bar.timestamps[i], 'm').replace('T', ' ')} \t {bar.values[i]}"
                
                return ret
            
            # TODO: handle errors when bar and other is not compatible
            def __sub__(bar, other):
                return BarDS(TimeArray(bar.values - other.values, bar.timestamps))

            def __add__(bar, other):
                return BarDS(TimeArray(bar.values + other.values, bar.timestamps))
            
            def __mul__(bar, other):
                return BarDS(TimeArray(bar.values * other.values, bar.timestamps))

            def __div__(bar, other):
                return BarDS(TimeArray(bar.values / other.values))

            def _tolist(bar):
                return bar.values.tolist()

        self.BarDS = BarDS

    def initializeOHLC(self):
        self.open = self.BarDS(self.data.open)
        self.high = self.BarDS(self.data.high)
        self.low = self.BarDS(self.data.low)
        self.close = self.BarDS(self.data.close)

    def initializeTechnical(self):
        class Technical:
            def __init__(ta):
                pass
            def true_high(ta):
                values = [self.high.getAt(0)]
                for i in range(1, self._len):
                    if self.close.getAt(i - 1) > self.high.getAt(i):
                        values.append(self.close.getAt(i - 1))
                    else:
                        values.append(self.high.getAt(i))
                return self.BarDS(TimeArray(values, self.time))

            def true_low(ta):
                values = [self.low.getAt(0)]
                for i in range(1, self._len):
                    if self.close.getAt(i - 1) < self.low.getAt(i):
                        values.append(self.close.getAt(i - 1))
                    else:
                        values.append(self.low.getAt(i))
                return self.BarDS(TimeArray(values, self.time.values))

            def true_range(ta):
                return true_high(data) - true_low(data)

            def avg(ta, x: self.BarDS, period: int):
                values = []
                window_sum = 0
                for i in range(period - 1):
                    window_sum += x.getAt(i)
                    values.append(window_sum / (i + 1))
                for j in range(period - 1, len(x)):
                    window_sum += x.getAt(j)
                    values.append(window_sum / period)
                    window_sum -= x.getAt(j - period + 1)
                return self.BarDS(TimeArray(values, x.timestamps))

            def atr(data: OHLC, period):
                tr = true_range(data)
                return avg(tr, period)

            def xavg(x: self.BarDS, period: int):
                alpha = 2 / (period + 1)
                values = [x.getAt(0)]

                for i in range(1, len(x)):
                    values.append((x.getAt(i) * alpha) + (values[i - 1] * (1 - alpha)))

                return self.barDS(TimeArray(values, x.timestamps))

            def highest(x: self.BarDS, period: int):
                values = []
                currhigh = -Inf
                for i in range(period):
                    currhigh = max(currhigh, x.getAt(i))
                    values.append(currhigh)
                for i in range(period, len(x)):
                    currhigh = -Inf
                    for j in range(i - period + 1, i + 1):
                        currhigh = max(currhigh, x.getAt(j))
                    values.append(currhigh)
                return self.barDS(TimeArray(values, x.timestamps))

            def lowest(x: self.BarDS, period: int):
                values = []
                currlow = Inf
                for i in range(period):
                    currlow = min(currlow, x.getAt(i))
                    values.append(currlow)
                for i in range(period, len(x)):
                    currlow = Inf
                    for j in range(i - period + 1, i + 1):
                        currlow = min(currlow, x.getAt(j))
                    values.append(currlow)
                return self.BarDS(TimeArray(values, x.timestamps))

        self.ta = Technical()

    def initialize(self):
        self.sma_10 = self.ta.avg(self.close, 10)
        self.sma_50 = self.ta.avg(self.close, 50)

    def strategy(self):
        if (self.close[0] < self.sma_10[1]):
            print(f"buy at {self.close[0]}")
        
    def run(self):
        self.initialize()
        for self.index in range(0, len(data)):
            self.strategy()

        
m = Root(data = data)
m.run()