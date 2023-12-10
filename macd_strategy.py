fast = param("TIMEPERIOD_FAST", 12)
slow = param("TIMEPERIOD_SLOW", 26)
signal = param("TIMEPERIOD_SIGNAL", 9)
macdline, macdsignal, _ = MACD(close,fast,slow,signal)
if crossover(macdline, macdsignal):
    entry(id='long trade', direction="LONG")
elif crossunder(macdline, macdsignal):
    exit(id='long trade exit',from_entry='long trade')
