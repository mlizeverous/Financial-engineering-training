import talib
import numpy as np
import pandas as pd

MySlowK = pd.DataFrame()
ss = pd.read_excel(r'..\AU.SHF.xls')

MySlowK = ss
MySlowK = MySlowK.drop('high', 1)
MySlowK = MySlowK.drop('open', 1)
MySlowK = MySlowK.drop('low', 1)
MySlowK = MySlowK.drop('close', 1)
MySlowK = MySlowK.drop('volume', 1)

tempS = pd.Series()


slowk = talib.STOCH(ss['high'].values,
                    ss['low'].values,
                    ss['close'].values,
                    fastk_period=5,
                    slowk_period=3,
                    slowk_matype=0,
                    slowd_period=3,
                    slowd_matype=0)
slowk = slowk[-1]
print(slowk)
slowk = pd.Series(slowk, index = ss.index)

print(slowk)

MySlowK['slowK'] = slowk

print(ss.index)
MySlowK.to_excel('result.xls')