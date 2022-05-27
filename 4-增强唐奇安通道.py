'''backtest
start: 2019-01-01 09:00:00
end: 2021-05-25 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

position = 0

def onTick():
    global position
    bar = ext.get_record('rb000', 60)
    if not bar:
        return
    last = bar[-1].Close
    last_prev = bar[-2].Close
    bar.pop()
    upper = TA.Highest(bar, periods, 'High') * up_coef
    lower = TA.Lowest(bar, periods, 'Low') * down_coef
    mid = (upper + lower) / 2

    if position > 0 and last_prev < mid:
        position = ext.Trade(position, 'closebuy', last)
    if position < 0 and last_prev > mid:
        position = ext.Trade(position, 'closesell', last)
    if position == 0:
        if last_prev > upper:
            position = ext.Trade(position, 'buy', last)
        if last_prev < lower:
            position = ext.Trade(position, 'sell', last)

def main():
    while True:
        onTick()
        Sleep(1000)
