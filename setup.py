#--------------preprocessing--------------------------------
from numpy import nan
import pandas as pd
import datetime
from data_structures import *
df = pd.read_csv('data.csv')
df = df.filter(['date', 'open', 'high', 'low', 'close'])
#print(df)
date_format = "%Y-%m-%d %H:%M:%S%z"
df['date'] = (df['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = TimeMatrix(df)
#-----------------------------------------------------------
# user writes from here

def ts_mean(x: TimeArray, d):
    values = []
    window_sum = 0
    for i in range(d):
        values.append(nan)
        window_sum += x[i]
    for j in range(d, len(x)):
        values.append(window_sum / d)
        window_sum -= x[j - d]
        window_sum += x[j]
    return TimeArray(values, x.timestamps)

y = ts_mean(data.open, 2)
print(y)