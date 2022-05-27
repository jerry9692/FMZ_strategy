'''backtest
start: 2019-01-01 09:00:00
end: 2021-01-01 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import talib
import numpy as np

position = 0

def onTick():
    global position
    bar = ext.get_record('ZC000', 100)
    if not bar:
        return
    arr = np.array(ext.get_data(bar, ['High', 'Low']))
    aroon = talib.AROON(arr[0], arr[1], period)
    aroon_up = aroon[1][-2]
    aroon_down = aroon[0][-2]
    last = bar[-1].Close
    
    if position == 0:
        if aroon_up > aroon_down and aroon_up > 50:
            position = ext.Trade(position, 'buy', last)
        if aroon_up < aroon_down and aroon_down > 50:
            position = ext.Trade(position, 'sell', last)
    if position == 1 and (aroon_up < aroon_down or aroon_up < 50):
        position = ext.Trade(position, 'closebuy', last)
    if position == -1 and (aroon_up > aroon_down or aroon_down < 50):
        position = ext.Trade(position, 'closesell', last)    
    
def main():
    while True:
        onTick()
        Sleep(1000)