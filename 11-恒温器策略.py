position = 0

def onTick():
    global position
    bar = ext.get_record('rb000', 100)
    if not bar:
        return
    *bar, last_bar = bar
    last, close1, close30, open1 = last_bar.Close, bar[-1].Close, bar[-30].Close, bar[-1].Open
    hh30, ll30 = TA.Highest(bar, 30, 'High'), TA.Lowest(bar, 30, 'Low')
    CMI = abs((close1 - close30) / (hh30 - ll30)) * 100
    hl_avg = (bar[-1].High + bar[-1].Low) / 2
    atr = TA.ATR(bar, 10)[-1]
    high_avg, low_avg = (bar[-1].High + bar[-2].High + bar[-3].High) / 3, (bar[-1].Low + bar[-2].Low + bar[-3].Low) / 3
    (lep0, sep0) = (open1 + atr * 3, open1 - atr * 2) if close1 > hl_avg else (open1 + atr * 2, open1 - atr * 3)
    lep, sep = max(lep0, high_avg), min(sep0, low_avg)
    boll = TA.BOLL(bar, 50, 2)
    upper, mid, lower = boll[0][-1], boll[1][-1], boll[2][-1]
    
    conditions_shock = {'buy': position == 0 and lep < close1 < hl_avg,
                        'sell': position == 0 and hl_avg < close1 < sep, 
                        'closebuy': position == 1 and close1 > min(high_avg, hl_avg),
                        'closesell': position == -1 and close1 < max(low_avg, hl_avg)}
    conditions_trend = {'buy': position == 0 and close1 > upper,
                        'sell': position == 0 and close1 < lower, 
                        'closebuy': position == 1 and close1 < mid, 
                        'closesell': position == -1 and close1 > mid}
    if CMI < 20:
        position = ext.Trade_under_conditions(position, last, conditions_shock)
    else:
        position = ext.Trade_under_conditions(position, last, conditions_trend)
    
def main():
    while True:
        onTick()
        Sleep(1000)