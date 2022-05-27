'''backtest
start: 2019-01-01 09:00:00
end: 2021-05-26 15:00:00
period: 1h
basePeriod: 15m
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

position = 0
lower = upper = 0

def onTick():
    global position, lower, upper
    bar = ext.get_record('rb000', 100)
    if not bar:
        return
    last = bar[-1].Close
    if bar[-1].High > bar[-2].High:
        lower = TA.Lowest(bar, periods, 'Low')
    if bar[-1].Low < bar[-2].Low:
        upper = TA.Highest(bar, periods, 'High')
    mid = (TA.Lowest(bar, periods, 'Low') + TA.Highest(bar, periods, 'High')) / 2
    
    if position == 0:
        if last > upper:
            position = ext.Trade(position, 'buy', last)
        if last < lower:
            position = ext.Trade(position, 'sell', last)
    if position == 1 and last < mid:
        position = ext.Trade(position, 'closebuy', last)
    if position == -1 and last > mid:
        position = ext.Trade(position, 'closesell', last)
    
def main():
    while True:
        onTick()
        Sleep(1000)