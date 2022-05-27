'''backtest
start: 2018-02-01 09:00:00
end: 2021-05-25 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import time

position = 0
profit = 0
trade_count = 0
upper = lower = 0

def onTick():
    global position, profit, trade_count, upper, lower
    bar = ext.get_record('rb000', 0, PERIOD_M1)
    last = bar[-1].Close
    ts_new = time.localtime(bar[-1].Time/1000)
    hm_new = time.strftime('%H:%M', ts_new)
    if hm_new == '09:30':
        bar = ext.get_record('rb000', 0, PERIOD_D1)
        upper, lower = bar[-1].High, bar[-1].Low
        trade_count = 0
    pos = _C(exchange.GetPosition)
    if len(pos) > 0:
        profit = pos[0].Profit
    else:
        position = 0
        profit = 0  
    if hm_new > '14:50' or profit > 300 or profit < -100:
        if position == 1:
            position = ext.Trade(position, 'closebuy', last)
        if position == -1:
            position = ext.Trade(position, 'closesell', last)
    if position == 0 and trade_count < 3 and '09:30' < hm_new < '14:50':
        if last > upper:
            position = ext.Trade(position, 'buy', last)
        elif last < lower:
            position = ext.Trade(position, 'sell', last)
        trade_count = trade_count + 1
    
def main():
    while True:
        onTick()
        Sleep(1000)