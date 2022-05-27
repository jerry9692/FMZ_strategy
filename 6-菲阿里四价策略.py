'''backtest
start: 2020-01-01 09:00:00
end: 2021-05-25 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import time

position = 0

def onTick():
    global position
    bar = ext.get_record('rb888', 2, PERIOD_D1)
    if not bar:
        return
    high_prev, low_prev, open_new = bar[-2].High, bar[-2].Low, bar[-1].Open
    bar = _C(exchange.GetRecords)
    last = bar[-1].Close
    ts_new = time.localtime(bar[-1].Time/1000)
    hm_new = time.strftime('%H:%M', ts_new)
    long_stop = high_prev if open_new / high_prev > 1 + adj_coef else open_new if open_new / high_prev < 1 - adj_coef else (high_prev + low_prev) / 2
    short_stop = low_prev if open_new / low_prev < 1 - adj_coef else open_new if open_new / low_prev > 1 + adj_coef else (high_prev + low_prev) / 2
    
    if position == 1:
        if last < long_stop or hm_new > '14:50':
            position = ext.Trade(position, 'closebuy', last)
    if position == -1:    
        if last > long_stop or hm_new > '14:50':
            position = ext.Trade(position, 'closesell', last)
    if position == 0 and '09:30' < hm_new < '14:50':
        if last > high_prev:
            position = ext.Trade(position, 'buy', last)
        elif last < low_prev:
            position = ext.Trade(position, 'sell', last)
        
def main():
    while True:
        onTick()
        Sleep(1000)