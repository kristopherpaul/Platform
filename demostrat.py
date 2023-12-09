"""
TODO: Add stoploss
TODO: dynamic lots/quantity (change with profit/loss)
"""

# ---------------------------------------------------Preprocessing---------------------------------------------------------------
import pandas as pd
from technical import *
import datetime
papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = TimeMatrix(papadata)

expavg = xavg(data.close, 65)
high = highest(data.high, 10)
low = lowest(data.low, 10)
# -------------------------------------------------------------------------------------------------------------------------------

# Strategy begins

transit = None

def long(data: TimeMatrix, i: int):
    global transit
    if data.close[i] > expavg[i] and transit != 'buy':
        transit = 'buy'
        return False
    if transit == 'buy':
        if data.high[i] > high[i - 1] + 0.05:
            transit = None
            return True
    if data.close[i] < expavg[i]:
        transit = None
        return False
    return False

def short(data: TimeMatrix, i: int):
    global transit
    if data.close[i] < expavg[i] and transit != 'sell':
        transit = 'sell'
        return False
    if transit == 'sell':
        if data.low[i] < low[i - 1] - 0.05:
            transit = None
            return True
    if data.close[i] > expavg[i]:
        transit = None
        return False
    return False

currpos = None
signal = []
timestamps = []
entryprice = []
exitprice = []
for i in range(65, len(data)):
    if currpos == 'buy':
        if short(data, i):
            signal.append('sell')
            timestamps.append(data.time[i])
            entryprice.append(low[i - 1])
            exitprice.append(low[i - 1])
            currpos = 'sell'
    elif currpos == 'sell':
        if long(data, i):
            signal.append('buy')
            timestamps.append(data.time[i])
            entryprice.append(high[i - 1])
            exitprice.append(high[i - 1])
            currpos = 'buy'
    else:
        if long(data, i):
            signal.append('buy')
            timestamps.append(data.time[i])
            entryprice.append(high[i - 1])
            currpos = 'buy'
        else:
            signal.append('sell')
            timestamps.append(data.time[i])
            entryprice.append(low[i - 1])
            currpos = 'sell'

exitprice.append(None)
output = pd.DataFrame()

data = {
    'Timestamp': timestamps,
    'Signal': signal,
    'EntryPrice': entryprice,
    'ExitPrice': exitprice,
}

df = pd.DataFrame(data)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)
df.to_csv('signal.csv')