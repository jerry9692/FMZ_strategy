def get_record(contract, bar_length = 0, period = None):
    '''
    获取record信息。
    contract：要获取的期货种类
    bar_length：至少获取bar的长度，默认为0
    period：获取数据周期
    '''
    _C(exchange.SetContractType, contract)
    if not period:
        bar = _C(exchange.GetRecords)
    else:
        bar = _C(exchange.GetRecords, period)
    if len(bar) < bar_length:
        return
    return bar

def get_data(bars, get_list = ['Close']):
    '''
    从exchange.GetRecords得到的bar中获取需要的数据。
    bars：全部数据
    get_list：需要获取的数据，默认为“Close”
    '''
    if len(get_list) == 1 and get_list[0] in bars[0].keys():
        return [bars[i][get_list[0]] for i in range(len(bars))]
    elif len(get_list) > 1 and all(item in bars[0].keys() for item in get_list):
        arr = [[] for i in range(len(get_list))]
        for i in bars:
            for j,k in zip(list(range(len(get_list))),get_list):
                arr[j].append(i[k])
        return arr
    else:
        Log['error']

def Trade(pos, direction, close):
    '''
    交易执行函数。
    pos：仓位
    direction：交易方向，可以是'closebuy'，'closesell'，'buy'，'sell'
    close：交易价格
    '''
    exchange.SetDirection(direction)
    if direction in ['closebuy','sell']:
        exchange.Sell(close-1, 1)
        return pos-1 
    elif direction in ['closesell','buy']:
        exchange.Buy(close, 1)
        return pos+1
    else:
        Log("Direction error!")

def Trade_under_conditions(position, last, conditions):
    if conditions['buy']:
        return ext.Trade(position, 'buy', last)
    elif conditions['sell']:
        return ext.Trade(position, 'sell', last)
    elif conditions['closebuy']:
        return ext.Trade(position, 'closebuy', last)
    elif conditions['closesell']:
        return ext.Trade(position, 'closesell', last)
    else:
        return position

    
ext.get_record = get_record
ext.get_data = get_data
ext.Trade = Trade
ext.Trade_under_conditions = Trade_under_conditions

