position = 0  #持仓量
    
def onTick():
    global position
    bar = ext.get_record('rb000', long+1)
    if not bar:
        return
    last, close1, ma1, ma2 = bar[-1].Close, bar[-2].Close, TA.MA(bar, short)[-2], TA.MA(bar, long)[-2]
    bias1, bias2 = (close1 - ma1) / ma1 * 100, (close1 - ma2) / ma2 * 100
    
    cond = {'buy': position == 0 and bias1 < bias2,
            'sell': position == 0 and bias1 > bias2,
            'closebuy': position == 1 and bias1 >= bias2,
            'closesell': position == -1 and bias1 <= bias2}
    position = ext.Trade_under_conditions(position, last, cond)

def main():
    while True:
        onTick()
        Sleep(1000)