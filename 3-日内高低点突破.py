'''backtest
start: 2021-04-01 00:00:00
end: 2021-05-24 00:00:00
period: 5m
basePeriod: 1m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import time

position = 0
upper = lower = 0

def strf(ts, format_list):
    return [int(time.strftime(i, ts)) for i in format_list]
    
def onTick():
    global position, upper, lower
    bar = ext.get_record('MA888', 10)
    if not bar:
        return
    ts_new, ts_prev = time.localtime(bar[-1].Time/1000), time.localtime(bar[-2].Time/1000)
    hm_new = time.strftime('%H:%M', ts_new)
    high, low = bar[-2].High, bar[-2].Low
    if int(time.strftime('%d', ts_new)) != int(time.strftime('%d', ts_prev)):
        upper, lower = high * up_coef, low * down_coef
    if hm_new < '09:30':
        if high > upper:
            upper = high * up_coef
        if low < lower:
            lower = low * down_coef
    if upper - lower < 10:
        return
    
    last = bar[-1].Close
    if position == 1 and (last < lower or hm_new > '14:50'):
        position = ext.Trade(position, 'closebuy', last)
    if position == -1 and (last > upper or hm_new > '14:50'):
        position = ext.Trade(position, 'closesell', last)
    if position == 0 and '09:30' < hm_new < '14:50':
        if last > upper:
            position = ext.Trade(position, 'buy', last)
        elif last < lower:
            position = ext.Trade(position, 'sell', last)
            
def main():
    while True:
        onTick()
        Sleep(1000)
