'''backtest
start: 2021-04-01 00:00:00
end: 2021-05-01 00:00:00
period: 1m
basePeriod: 1m
exchanges: [{"eid":"Binance","currency":"BTC_USDT","balance":100000,"fee":[0.1,0.1]}]
args: [["GridNum",15],["GridPointDis",500],["GridCovDis",700]]
'''

import time
import json

StopLoss = StopWin = 0    #止损、止盈
Grid = []                 #网格 
GridPointDis = GridCovDis = 0

def cal_cmi(bar_arr, n):
    close0 = bar_arr[-1]['Close']  			# 获取最新价格（卖价），用于开平仓
    bar_arr.pop()  							# 删除K线数组最后一个元素
    close1 = bar_arr[-1]['Close']  			# 最新收盘价
    closen = bar_arr[-n]['Close'] 		# 前n根K线的收盘价
    hh = TA.Highest(bar_arr, n, 'High')	# 最近n根K线的最高价
    ll = TA.Lowest(bar_arr, n, 'Low')  	# 最近n根K线的最低价
    cmi = abs((close1 - closen) / (hh - ll)) * 100	# 计算市场波动指数
    return cmi
    
def cal_boll_width(bar_arr, n):
    boll = TA.BOLL(bar_arr, n, 2)
    return boll[0][-1] - boll[2][-1]
    
    
def UpdateGrid(nowBidsPrice, nowAsksPrice, direction, GridPointDis, GridCovDis):    #direction:向上为1，向下为-1
    global StopLoss, StopWin, Grid
    last = Grid[-1]['price'] if len(Grid) > 0 else 0
    if(len(Grid) == 0 or (direction == 1 and nowBidsPrice - last > GridPointDis) or (direction == -1 and last - nowAsksPrice > GridPointDis)):
        nowPrice = nowBidsPrice if direction == 1 else nowAsksPrice
        Grid.append({'price': nowPrice if len(Grid) == 0 else last + GridPointDis * direction, 'hold': {'price': 0, 'amount': 0}, 
                     'coverPrice' : nowPrice - direction * GridCovDis if len(Grid) == 0 else last + (GridPointDis - GridCovDis) * direction})
        tradeInfo =  ext.Sell(GridPointAmount) if direction == 1 else ext.Buy(GridPointAmount)
        Grid[-1]['hold']['price'], Grid[-1]['hold']['amount'] = tradeInfo['price'], tradeInfo['amount']
        #ext.PlotFlag(time.time() * 1000, json.dumps(tradeInfo), "O")
        #Log(1,Grid)
        Log(GridPointDis, GridCovDis)
    if(len(Grid) > 0 and ((direction == 1 and nowAsksPrice < Grid[-1]['coverPrice']) or (direction == -1 and nowBidsPrice > Grid[-1]['coverPrice']))):
        coverInfo = ext.Buy(Grid[-1]['hold']['amount']) if direction == 1 else ext.Sell(Grid[-1]['hold']['amount'])
        Grid.pop()
        #ext.PlotFlag(time.time() * 1000, json.dumps(coverInfo), "C")
        StopWin = StopWin + 1
        #Log(2,Grid)
        Log(GridPointDis, GridCovDis)
    elif(len(Grid) > GridNum):
        coverfirstInfo = ext.Buy(Grid[0]['hold']['amount']) if direction == 1 else ext.Sell(Grid[0]['hold']['amount'])
        Grid = Grid[1:]
        #ext.PlotFlag(time.time() * 1000, json.dumps(coverfirstInfo), "C")
        StopLoss = StopLoss + 1
        #Log(3,Grid)
        Log(GridPointDis, GridCovDis)

def main():
    while True:
        global Grid
        ticker = _C(exchange.GetTicker)
        records = _C(exchange.GetRecords)
        CMI = cal_cmi(records, 30)
        boll_coef = cal_boll_width(records, 50)
        #ext.PlotRecords(records, "kline")
        GridPointDis = TA.ATR(records, 10)[-1] * 5 * (1 + len(Grid) / 20)
        GridCovDis = GridPointDis * 2.5
        UpdateGrid(ticker['Buy'], ticker['Sell'], direction, GridPointDis, GridCovDis)
        msg = ""
        for i in range(len(Grid)):
            msg += json.dumps(Grid[i]) + "\n"
        LogStatus(_D(), "StopWin:", StopWin, "StopLoss:", StopLoss, _C(exchange.GetAccount), "\n", "len(Grid):", len(Grid), "GridNum:", GridNum, "\n", msg)
        Sleep(500)


