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
data = OHLC(papadata)

expavg = xavg(data.close, 65)
high = highest(data.high, 10)
low = lowest(data.low, 10)
atr_values = atr(data, 20)
# -------------------------------------------------------------------------------------------------------------------------------

# Strategy begins

transit = None

def long(data: OHLC, i: int): 
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

def short(data: OHLC, i: int):
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

def stoploss_long(data: OHLC, entryprice, i, curri):
    lx2n = entryprice - 2 * atr_values[i]
    if data[curri]["low"] <= lx2n:
        return lx2n
    return None

def stoploss_short(data: OHLC, entryprice, i, curri):
    lx2n = entryprice + 2 * atr_values[i]
    if data[curri]["high"] >= lx2n:
        return lx2n
    return None

currpos = None
signal = []
timestamps = []
entryprice = []
exitprice = []
true_index = []

# Backtesting Loop

lasti = None
for i in range(65, len(data)):
    if currpos == 'buy':
        if short(data, i):
            signal.append('sell')
            timestamps.append(data.time[i])
            entryprice.append(min(low[i - 1], data.open[i]))
            exitprice.append(min(low[i - 1], data.open[i]))
            true_index.append(i)
            lasti = i
            currpos = 'sell'
            
        lx2n = stoploss_long(data, entryprice[-1], lasti, i)
        if lx2n:
            lx2n = min(lx2n, data.open[i])
            currpos = None
            exitprice.append(f'π{lx2n}')
    elif currpos == 'sell':
        if long(data, i):
            signal.append('buy')
            timestamps.append(data.time[i])
            entryprice.append(max(data.open[i], high[i - 1]))
            true_index.append(i)
            exitprice.append(max(data.open[i], high[i - 1]))
            lasti = i
            currpos = 'buy'
        lx2n = stoploss_short(data, entryprice[-1], lasti, i)
        if lx2n:
            lx2n = max(lx2n, data.open[i])
            currpos = None
            exitprice.append(f'π{lx2n}')
    else:
        if long(data, i):
            signal.append('buy')
            timestamps.append(data.time[i])
            entryprice.append(high[i - 1])
            true_index.append(i)
            lasti = i
            currpos = 'buy'
        elif short(data, i):
            signal.append('sell')
            lasti = i
            timestamps.append(data.time[i])
            entryprice.append(low[i - 1])
            true_index.append(i)
            currpos = 'sell'

exitprice.append(None)
output = pd.DataFrame()

dfdata = {
    'true_index': true_index,
    'Timestamp': timestamps,
    'Signal': signal,
    'EntryPrice': entryprice,
    'ExitPrice': exitprice,
}

df = pd.DataFrame(dfdata)

df['Timestamp'] = pd.to_datetime(df['Timestamp'])
#df.set_index('Timestamp', inplace=True)
df.to_csv('signal.csv')

lot = 50 # lot size of nifty in F&O market
init_capital = 200000
leverage = 3
risk = 0.01

cumpnl = [init_capital]

for i in range(len(df) - 1):
    capital = cumpnl[-1]
    net_equity = capital * leverage
    sl = 2 * atr_values[int(df['true_index'][i]-1)]
    if (df['Signal'][i] == 'buy'):
        qty1 = ((net_equity * risk / sl) // lot) * lot
        qty2 = (net_equity // (lot * high[int(df['true_index'][i])-1])) * lot
    else:
        qty1 = ((net_equity * risk // sl) // lot) * lot
        qty2 = (net_equity // (lot * low[int(df['true_index'][i])-1])) * lot
    finqty = min(qty1, qty2)
    try:
        pnl = (df['ExitPrice'][i] - df['EntryPrice'][i]) * finqty
    except:
        pnl = (float(df['ExitPrice'][i][1:]) - df['EntryPrice'][i]) * finqty
    if df['Signal'][i] == 'sell':
        pnl *= -1
    cumpnl.append(cumpnl[-1] + pnl)

dfdata = {
    'trade number': [i for i in range(1, len(df) + 1)],
    'cumulative P&L': cumpnl
}
