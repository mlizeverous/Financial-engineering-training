# coding=utf-8
import numpy as np
import pandas as pd
from numpy import log
import os

path = "../Data"
files = os.listdir(path)
store = pd.Panel()


# x中d天内最小的值
def ts_min(df, window=10):
    return df.rolling(window).min()


# x中d天内最大的值
def ts_max(df, window=10):
    return df.rolling(window).max()

# 表示x值的最新值减去x值在d天前的值
def delta(df, period=1):
    return df.diff(period)


# 表示某股票x值在横截面上的升序排名序号，并将排名归一到[0,1]的闭区间
def rank(df):
    return df.rank(axis=1, pct=True)


def rolling_prod(df):
    return df.prod(axis=0)


# d天以来x值的乘积
def product(df, window=10):
    return df.rolling(window).apply(rolling_prod)


# x和y两个变量d天以来的值的相关系数
def correlation(x, y, window=10):
    # type: (object, object, object) -> object
    return x.rolling(window).corr(y)


# 过去d天内的平均dollar volume
def adv(df, window=10):
    return df.rolling(window).mean()

flag = 0
panelTemp = 0
# 用一个panel来存储读入的数据
for file in files:
    pathN = path+"/"+file
    new = pd.read_excel(pathN)
    data = {file: new}
    if flag == 0:
        panelTemp = pd.Panel(data)
    else:
        panelTemp = panelTemp.join(pd.Panel(data))

    flag = flag+1

# 计算alpha011
# ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3)))
inner = panelTemp.minor_xs('vwap') - panelTemp.minor_xs('close')
temp1 = ts_max(inner, 3)
temp2 = ts_min(inner, 3)
temp3 = delta(panelTemp.minor_xs('volume'), 3)
alpha011 = (rank(temp1) + rank(temp2)) * rank(temp3)


# 计算alpha081
#((rank(Log(product(rank((rank(correlation(vwap, sum(adv10, 49.6054), 8.47743)) ^ 4)), 14.9655))) < rank(correlation(rank(vwap), rank(volume), 5.07914))) * -1)
vwap = panelTemp.minor_xs('vwap')
volume = panelTemp.minor_xs('volume')
in1 = correlation(vwap, (adv(vwap*volume*100, 10) + 49.6054), 8)
in2 = rank(in1) ** 4
in_left = rank(log(product(rank(in2), 15)))
in3 = correlation(rank(vwap), rank(volume), 5)
in_right = rank(in3)
alpha081 = ((in_left < in_right) * (-1))

# 将计算结果写入新的excel表里，名称为result_股票代码
count = 0
for file in files:

    alpha_011 = pd.Series(alpha011.iloc[:, count], index=alpha011.index)
    alpha_081 = pd.Series(alpha081.iloc[:, count], index=alpha081.index)
    Alpha = pd.DataFrame(index=alpha011.index)
    Alpha['alpha_011'] = alpha_011
    Alpha['alpha_081'] = alpha_081
    Alpha.to_excel('../result/result_'+file)
    count = count+1
