"""
Time Matrix is always going to be a OHLCV data indexed by timestamps

Time Vector is always a series of values indexed by timestamps
"""

"""
1. TODO: type hint everything
2. TODO: use @overload wherever necessary
3. TODO: implement binary search for indexing using datetime
4. TODO: write code for error handling wherever necessary
"""

import datetime
from typing import overload
import numpy as np


class TimeArray:
    def __init__(self, values, timestamps):
        """
        data must have a time column indexed by 'time'
        """
        self.values = np.array(values)
        self.timestamps = np.array(timestamps)
        self.begin = self.timestamps[0]
        self.end = self.timestamps[-1]
        self.step = self.timestamps[1] - self.timestamps[0]

    def __len__(self):
        return len(self.values)

    def __getitem__(self, i: int):
        """
        TODO: implement for slice
        format of time is (year, month, day, hour, min, sec)
        """
        if isinstance(i, int):
            return self.values[i]
        if isinstance(i, datetime.datetime):
            # TODO: Implement this, use binary search
            pass

    def __repr__(self):
        ret = "Time \t\t\t Value"

        if len(self.values) <= 15:
            for i in range(len(self.values)):
                ret += '\n'
                ret += f"{np.datetime_as_string(self.timestamps[i], 'm').replace('T', ' ')} \t {self.values[i]}"
        else:
            for i in range(5):
                ret += '\n'
                ret += f"{np.datetime_as_string(self.timestamps[i], 'm').replace('T', ' ')} \t {self.values[i]}"
            ret += '\n... \t\t\t ...'
            for i in range(len(self.values) - 5, len(self.values)):
                ret += '\n'
                ret += f"{np.datetime_as_string(self.timestamps[i], 'm').replace('T', ' ')} \t {self.values[i]}"
        
        return ret
    
    def __sub__(self, other):
        # TODO: handle errors when self and other is not compatible
        ret_values = []
        for i in range(len(self)):
            ret_values.append(self[i] - other[i])
        return TimeArray(ret_values, self.timestamps)


class TimeMatrix:
    def __init__(self, data):
        """ 
        data must have a time column indexed by 'time'
        """
        self.time = np.array(data['date'], dtype='datetime64[m]')
        self.open = TimeArray(data['open'], self.time)
        self.high = TimeArray(data['high'], self.time)
        self.low = TimeArray(data['low'], self.time)
        self.close = TimeArray(data['close'], self.time)
        self.begin = self.time[0]
        self.end = self.time[-1]
        self.step = self.time[1] - self.time[0]

    def __len__(self):
        return len(self.open)
