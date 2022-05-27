'''backtest
start: 2016-01-01 00:00:00
end: 2021-05-29 23:59:00
period: 1h
basePeriod: 1h
exchanges: [{"eid":"Futures_CTP","currency":"FUTURES"}]
'''

def cal_prices(o,h,l,c):
    p = (h+c+l)/3
    return p, 2*p-l, p+h-l, h+2*(p-l), 2*p-h, p-h+l, l-2*(h-p)
    
def onTick():
    bar = ext.get_record('rb000', 2, PERIOD_D1)
    if not bar:
        return
    pivot, r1, r2, r3, s1, s2, s3 = cal_prices(bar[-2].Open, bar[-2].High, bar[-2].Low, bar[-2].Close)
    last = _C(exchange.GetTicker).Last
    position_arr = _C(exchange.GetPosition)  			# 获取持仓数组
    if len(position_arr) > 0:  							# 如果持仓数组大于0
        for i in position_arr:
            position = i['Amount'] if i['Type'] % 2 == 0 else -i['Amount']
    else:
        position = 0  									# 赋值持仓数量为0
        
    if position == 0:
        if last > r3:
            position = ext.Trade(position, 'buy', last)
        if last < s3:
            position = ext.Trade(position, 'sell', last)
    if position > 0:
        if bar[-1].High > r2 and last < r1 or last < s3:
            position = ext.Trade(ext.Trade(position, 'closebuy', last), 'sell', last)
    if position < 0:
        if bar[-1].Low < s2 and last > s1 or last > r3:
            position = ext.Trade(ext.Trade(position, 'closesell', last), 'buy', last)
    
def main():
    while True:
        onTick()
        Sleep(1000)