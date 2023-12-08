fast = strategy.param("TIMEPERIOD_FAST", 12)
slow = strategy.param("TIMEPERIOD_SLOW", 26)
signal = strategy.param("TIMEPERIOD_SIGNAL", 9)
macdline, macdsignal, histogram, zeroline = technical.MACD(data.close,fast,slow,signal)
if technical.crossover(macdline, macdsignal):
    strategy.entry('trade 1', "LONG")
elif technical.crossunder(macdline, macdsignal):
    strategy.exit('trade 1')