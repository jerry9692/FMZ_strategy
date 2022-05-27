'''backtest
start: 2018-05-01 09:00:00
end: 2021-05-24 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import talib
import numpy as np

position = 0

def is_cross(arr1, arr2):
    if arr1[-2] < arr2[-2] and arr1[-1] > arr2[-1]:
        return True

def onTick():
    global position
    bar = ext.get_record('rb000', 100)
    if not bar:
        return
    close_arr = np.array(ext.get_data(bar))
    last = close_arr[-1]
    ama1 = talib.KAMA(close_arr, 10).tolist()
    ama2 = talib.KAMA(close_arr, 100).tolist()
    if is_cross(ama1, ama2):
        if position == 0:
            position = ext.Trade(position, 'buy', last)
        if position == -1:
            position = ext.Trade(position, 'closesell', last)
    if is_cross(ama2, ama1):
        if position == 0:
            position = ext.Trade(position, 'sell', last)
        if position == 1:
            position = ext.Trade(position, 'closebuy', last)

def main():
    while True:
        onTick()
        Sleep(1000)
