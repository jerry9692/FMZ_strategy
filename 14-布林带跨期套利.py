'''backtest
start: 2020-01-01 09:00:00
end: 2021-05-31 15:00:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

import operator

position1 = position2 = 0

def onTick():
    global position1, position2
    bar1 = ext.get_record('rb000', 10)
    bar2 = ext.get_record('MA000', 10)
    if (not bar1 or not bar2) or (bar1[-1].Time != bar2[-1].Time):
        return
    min_len = min(len(bar1), len(bar2))
    bar1, bar2 = bar1[-min_len:], bar2[-min_len:]
    diff = []
    for i in range(min_len):
        diff.append(bar1[i].Close - bar2[i].Close)
    if len(diff) < MAperiod:
        return
    boll = TA.BOLL(diff, MAperiod, ratio)
    last1, last2 = bar1[-1].Close, bar2[-1].Close
    if position1 == position2 == 0:
        if diff[-1] > boll[0][-1]:
            position1 = ext.Trade(position1, 'sell', last1)
            position2 = ext.Trade(position2, 'buy', last2)
        if diff[-1] < boll[2][-1]:
            position1 = ext.Trade(position1, 'buy', last1)
            position2 = ext.Trade(position2, 'sell', last2)
    if position1 == 1 and position2 == -1 and diff[-1] > boll[1][-1]:
        position1 = ext.Trade(position1, 'closebuy', last1)
        position2 = ext.Trade(position2, 'closesell', last2)
    if position1 == -1 and position2 == 1 and diff[-1] < boll[1][-1]:
        position1 = ext.Trade(position1, 'closesell', last1)
        position2 = ext.Trade(position2, 'closebuy', last2)

def main():
    while True:
        onTick()
        Sleep(1000)