import csv
import pandas 
import numpy as np
import re
import sys

sys.path.insert(1,'../data')

f=open("../data/ziplineAverage.csv",'r')
reader=csv.reader(f)
datas=list(reader)

lis=data['zip'] == 12345
lis = np.flatnonzero(lis)[0]+1
print(datas[lis])
#ret=[]
for i in range(1,9):
    if re.search("[0-9]",datas[lis][i]):
        print((float)(datas[lis][i]))
    else: 
        print(0.0)



