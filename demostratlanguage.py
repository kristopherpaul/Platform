from language import *
from technical import *
import pandas as pd
import matplotlib.pyplot as plt
import datetime

# ---------------------------------------------------Preprocessing---------------------------------------------------------------
papadata = pd.read_csv('NIFTNEAR.csv')
papadata['time'] = papadata['time'].apply(lambda x: "0" * (4 - len(str(x))) + str(x))
papadata['time'] = papadata['time'].apply(lambda x: f"{x[0:2]}:{x[2:]}")
papadata['date'] = papadata['date'] + ' ' + papadata['time']
date_format = "%d-%m-%y %H:%M"
papadata['date'] = (papadata['date'].apply(lambda x: datetime.datetime.strptime(x, date_format).replace(tzinfo=None)))
data = OHLC(papadata)
# -------------------------------------------------------------------------------------------------------------------------------

expavg = xavg(data.close, 65)
high = highest(data.high, 10)
low = lowest(data.low, 10)

def long(ltp, i):
    if ltp["close"] > expavg[i]:
        return high[i]
    return None

def short(ltp, i):
    if ltp["close"] < expavg[i]:
        return low[i]
    return None

test = Backtest(long, short, data)
test.run()

dfdata = {
    "timestamp": test.timestamps,
    "signal": test.signal,
    "EntryPrice": test.entryprice,
    "ExitPrice": test.exitprice
}

df = pd.DataFrame(dfdata)
df.to_csv('signal.csv')