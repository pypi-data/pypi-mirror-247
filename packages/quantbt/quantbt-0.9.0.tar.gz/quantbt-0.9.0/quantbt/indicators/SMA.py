import talib
from numba import njit


def talib_SMA(data, period=21):
    return talib.MA(data, timeperiod=period, matype=talib.MA_Type.SMA)


# @njit(parallel=True, cache=True)
# def SMA(data, period):
