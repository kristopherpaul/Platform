"""
Time Matrix is always going to be a OHLCV data indexed by timestamps

Time Vector is always a series of values indexed by timestamps
"""

"""
TODO: implement custom time class
"""

import datetime
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

    def __getitem__(self, i):
        """
        TODO: implement for slice
        format of time is (year, month, day, hour, min, sec)
        """
        if isinstance(i, int):
            return self.values[i]
        if isinstance(i, datetime.datetime):
            i = np.datetime64(i, 'm')
            if ((i - self.begin) % self.step):
                # TODO: ERORR
                return -1

            index = (i - self.begin) // self.step
            return self.values[index]

    def getRange(self, start, end):
        """
        format of start and end is (year, month, day, hour, min, sec) [inclusive]
        """
        start = np.datetime64(start)
        end = np.datetime64(end)
        if (((start - self.begin) % self.step) > 0) and (((end - self.begin) % self.step) != 0):
            # TODO: ERROR
            return -1

        
        start_index = max(0, (start - self.begin) // self.step)
        end_index = min(len(self.values) - 1, (end - self.begin) // self.step)
        return TimeArray(self.values[start_index:end_index + 1], self.timestamps[start_index:end_index + 1])
    
    def __repr__(self):
        # TODO: fix if the length of the dataset is less than 10
        ret = "Time \t\t\t Value"
        for i in range(5):
            ret += '\n'
            ret += f"{np.datetime_as_string(self.timestamps[i], 'm').replace('T', ' ')} \t {self.values[i]}"
        ret += '\n... \t\t\t ...'
        for i in range(len(self.values) - 5, len(self.values)):
            ret += '\n'
            ret += f"{np.datetime_as_string(self.timestamps[i], 'm').replace('T', ' ')} \t {self.values[i]}"
        
        return ret

class TimeMatrix:
    def __init__(self, data):
        """ 
        data must have a time column indexed by 'time'
        """
        self.time = np.array(data['date'], dtype='datetime64[m]')
        self.open = TimeArray(data['open'], self.time)
        self.high = TimeArray(data['open'], self.time)
        self.low = TimeArray(data['open'], self.time)
        self.close = TimeArray(data['open'], self.time)
        self.begin = self.time[0]
        self.end = self.time[-1]
        self.step = self.time[1] - self.time[0]