position = 0
last_bar = 0
upper = lower = 0

def onTick():
    global position, last_bar, upper, lower
    bar = ext.get_record('rb000', cycle)
    last = bar[-1].Close
    if last_bar != bar[-1].Time:
        highest, highest_close = TA.Highest(bar, cycle, 'High'), TA.Highest(bar, cycle, 'Close')
        lowest, lowest_close = TA.Lowest(bar, cycle, 'Low'), TA.Lowest(bar, cycle, 'Close')
        Range = max(highest - lowest_close, highest_close - lowest)
        upper, lower = bar[-1].Open + Ks * Range, bar[-1].Open - Kx * Range
        last_bar = bar[-1].Time
    if position == 0:
        if last >= upper:
            position = ext.Trade(position, 'buy', last)
        if last <= lower:
            position = ext.Trade(position, 'sell', last)
    if position == 1 and last <= lower:
        position = ext.Trade(position, 'closebuy', last)
    if position == -1 and last >= upper:
        position = ext.Trade(position, 'closesell', last)
        
def main():
    while True:
        onTick()
        Sleep(1000)