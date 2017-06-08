
import numpy as np

import pandas as pd

temp = pd.DataFrame(index=[pd.date_range('1/5/2015', '5/5/2015', freq='15Min')])
#s = pd.DataFrame([temp])
#temp.to_excel('result.xls')

ss = pd.read_excel(r'..\AU.SHF.xls')
#print(ss.iloc[2])

#print(a)

l = pd.DataFrame()


aa = ss.head()
print(aa)
#a = aa.icol(0)
#print(a)
#MySlowK = ss
#MySlowK = MySlowK.drop('high', 1)
#MySlowK = MySlowK.drop('open', 1)
#MySlowK = MySlowK.drop('low', 1)
#MySlowK = MySlowK.drop('close', 1)
#MySlowK = MySlowK.drop('volume', 1)
#MySlowK.to_excel('result.xls')
tempS = pd.DataFrame(columns=['slowK'])
tempS.to_excel('result.xls')

for index, row in aa.iterrows():
    for col_name in aa.columns:

        ll = pd.Series([row[col_name]])
        l[col_name] = ll
    #print(l)

#print(s)





