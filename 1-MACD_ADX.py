'''backtest
start: 2019-05-23 09:00:00
end: 2021-05-23 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import talib
import numpy as np

position = 0  #持仓量
    
def onTick():
    global position
    bar = ext.get_record('rb000', 100)
    if not bar:
        return
    macd = TA.MACD(bar, 5, 50, 15)
    dif = macd[0][-2]
    dea = macd[1][-2]
    np_arr = np.array(ext.get_data(bar, ['High', 'Low', 'Close']))
    adx_arr = talib.ADX(np_arr[0], np_arr[1], np_arr[2], 14)
    adx1 = adx_arr[-2]
    adx2 = adx_arr[-3]
    last = bar[-1]['Close']
    
    #开仓
    if position == 0 and adx1 > adx2:
        position = ext.Trade(position, 'buy', last) if dif > dea else ext.Trade(position, 'sell', last)
        
    
    #平仓
    if position == 1 and (dif < dea or adx1 < adx2):
        position = ext.Trade(position, 'closebuy', last)
    if position == -1 and (dif > dea or adx1 < adx2):
        position = ext.Trade(position, 'closesell', last)


def main():
    while True:
        onTick()
        Sleep(1000*60*60*1)
