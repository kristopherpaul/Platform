"""
TODO: Add stoploss
TODO: dynamic lots/quantity (change with profit/loss)
"""

# ---------------------------------------------------Preprocessing---------------------------------------------------------------
import pandas as pd
from technical import *
import matplotlib.pyplot as plt
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
# ----------------------------------i---------------------------------------------------------------------------------------------

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
        transit = 'sell'
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
        transit = 'buy'
        return False
    return False

currpos = None
signal = []
timestamps = []
entryprice = []
exitprice = []

# Backtesting Loop
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
        if transit != 'sell' and long(data, i):
            signal.append('buy')
            timestamps.append(data.time[i])
            entryprice.append(high[i - 1])
            currpos = 'buy'
        if transit != 'buy' and short(data, i):
            signal.append('sell')
            timestamps.append(data.time[i])
            entryprice.append(low[i - 1])
            currpos = 'sell'

exitprice.append(None)
output = pd.DataFrame()

dfdata = {
    'Timestamp': timestamps,
    'Signal': signal,
    'EntryPrice': entryprice,
    'ExitPrice': exitprice,
}

df = pd.DataFrame(dfdata)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp', inplace=True)
df.to_csv('signal.csv')

cumpnl = [0]
lot = 50 # lot size of nifty in F&O market

for i in range(len(df) - 1):
    pnl = df['ExitPrice'][i] - df['EntryPrice'][i]
    pnl *= lot
    if df['Signal'][i] == 'sell':
        pnl *= -1
    cumpnl.append(cumpnl[-1] + pnl)

dfdata = {
    'trade number': [i for i in range(1, len(df) + 1)],
    'cumulative P&L': cumpnl
}

pnldf = pd.DataFrame(dfdata)
pnldf.set_index('trade number', inplace=True)
plt.plot(pnldf)
plt.show()
