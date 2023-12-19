# pytrader.py

import pandas as pd
import pytrader.MarkeDataEntity_pb2 as mde

import datetime
import pytrader.filetime as filetime
from calendar import monthrange
import os
from enum import Enum


from read_protobuf import read_protobuf

__tickDataRootPath = 'C:\\TickData'
__currencies = ['USD','EUR','GBP','CHF','JPY','AUD','NZD','CAD']
__pairs = ['EURUSD','EURGBP','EURAUD','EURCHF','EURJPY','GBPUSD','GBPCHF','GBPJPY','GBPAUD','AUDUSD','AUDCHF','AUDJPY','USDCHF','USDJPY','CHFJPY','USDCAD','AUDCAD','AUDNZD','CADCHF','CADJPY','EURCAD','EURNZD','GBPCAD','GBPNZD','NZDCAD','NZDCHF','NZDJPY','NZDUSD']


class TimeFrame(Enum):
    M1 = 1
    M5 = 52
    M15 = 15
    H1 = 60
    H4 = 240
    D1 = 1440


def __validateRootFolder():
    if (len(__tickDataRootPath) == 0 or not os.path.exists(__tickDataRootPath) ) :
        raise ValueError("Call setTickDataRoot to set the source folder for bar data")
    
def __getTickDataPath(symbol: str, timeframe: TimeFrame, year: int, month: int, day: int) -> str :
    root = __tickDataRootPath
    file = f'{symbol}_{timeframe.value}.dat'
    year = str(year)
    month = str(month - 1).rjust(2,'0')
    day = str(day).rjust(2, '0')
    path = os.path.join(root, symbol, year, month, day, file)
    return path

def getAsBar(val: dict) -> mde.Bar:
    print(type(val))
    res = mde.Bar()
    res.Symbol = val['Symbol']
    res.Period = val['Period']
    res.Date = val['Date']
    res.Open = val['Open']
    res.High = val['High']
    res.Low = val['Low']
    res.Close = val['Close']
    res.Volume = val['Volume']
    return res


def setTickDataRoot(path: str):
    global __tickDataRootPath
    __tickDataRootPath = path
    __validateRootFolder()

def getPairs() -> [str]:
    return __pairs.copy()

def getCurrencies() -> [str]:
    return __currencies.copy()

def getMarketDataDay(symbol: str, timeframe: TimeFrame, year: int, month: int, day: int) -> pd.DataFrame :
    __validateRootFolder()
    MessageType = mde.MarketDataEntity()
    file = __getTickDataPath(symbol, timeframe, year, month, day)

    if (not os.path.exists(file)):
        return None

    #print(f'Loading: {file}')

    try:
        df = read_protobuf(file, MessageType, flatten=False)

        newdf = pd.DataFrame.from_dict(df['Data'].tolist())
        newdf['Date'] = newdf['Date'].apply(lambda x: filetime.to_datetime(x))
        newdf = newdf.astype({"Period": int})
        newdf.sort_values(by='Date', inplace=True)  
        del df
        return newdf
    except Exception as ex:
        if (not (ex.__class__.__name__ == 'ValueError' and len(ex.args) > 0 and ex.args[0] == 'If using all scalar values, you must pass an index')):
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        return None 

def getMarketDataMonth(symbol: str, timeframe: TimeFrame, year: int, month: int) -> pd.DataFrame :
    r = monthrange(year, month)[1]
    dfs = [] 
    for i in range(1, r):
        ldf = getMarketDataDay(symbol, timeframe, year, month, i)
        if (ldf is not None):
            dfs.append(ldf)

    if (len(dfs) > 0):
        return pd.concat(dfs)
    return None

def getMarketDataYear(symbol: str, timeframe: TimeFrame, year: int) -> pd.DataFrame :
    dfs = [] 
    for i in range(1,12):
        ldf = getMarketDataMonth(symbol, timeframe, year, i)
        if (ldf is not None):
            dfs.append(ldf)

    if (len(dfs) > 0):
        return pd.concat(dfs)
    return None

def getMarketData(symbol: str, timeframe: TimeFrame, year: int, month: int = None, day: int = None) -> pd.DataFrame :
    __validateRootFolder()
    if (day is not None and month is not None) :
        return getMarketDataDay(symbol, timeframe, year, month, day)

    if (day is None and month is not None) :
        return getMarketDataMonth(symbol, timeframe, year, month)

    return getMarketDataYear(symbol, timeframe, year)

def getMarketDataFrom(symbol: str, timeframe: TimeFrame, year: int, month: int, day: int) -> pd.DataFrame :
    start = datetime.date(year, month, day)
    end = datetime.datetime.now(datetime.timezone.utc).date()
    res = pd.date_range(str(start), str(end))
    dfs = [] 
    for d in res:
        ldf = getMarketDataDay(symbol, timeframe, d.year, d.month, d.day)
        if (ldf is not None):
            dfs.append(ldf)
    if (len(dfs) > 0):
        return pd.concat(dfs)
    return None

def getMarketDataFromTo(symbol: str, timeframe: TimeFrame, year: int, month: int, day: int, toyear: int, tomonth: int, today: int) -> pd.DataFrame :
    start = datetime.date(year, month, day)
    end = datetime.date(toyear, tomonth, today)
    res = pd.date_range(str(start), str(end))
    dfs = [] 
    for d in res:
        ldf = getMarketDataDay(symbol, timeframe, d.year, d.month, d.day)
        if (ldf is not None):
            dfs.append(ldf)
    if (len(dfs) > 0):
        return pd.concat(dfs)
    return None
   