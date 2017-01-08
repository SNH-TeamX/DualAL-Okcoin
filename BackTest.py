import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
import pickle
import os


def read_bench():
    result = pd.DataFrame()
    path = 'D:/data/1min/bench/'
    file_list = os.listdir(path)
    for file in file_list:
        
        if file != "20170101":
            continue
        
        fp = open(path + file, 'br')
        tmp = pickle.load(fp)
        tmp.index = tmp["time_stamp"]
        fp.close()
        result = pd.concat([result,tmp], join='inner')
    print(result)
    return result
    
data = read_bench()

raw = data

#fp = open(path, 'br')
#raw = pickle.load(fp)
#fp.close()

data = pd.DataFrame(raw['close'])

acc = 0;
acc_list = []
sig = []

for i in range(0,len(data)-1):
    avg_30 = sum(data['close'].iloc[i-20:i])/20
    avg_7 = sum(data['close'].iloc[i-7:i])/7
    
    ser = np.array(data['close'].iloc[i-10:i])
    std = np.std(ser)
    
    if avg_7>avg_30:
        acc += data['close'].iloc[i+1] - data['close'].iloc[i]
        sig.append(1)
    elif avg_7<avg_30:
        acc += -(data['close'].iloc[i+1] - data['close'].iloc[i])
        sig.append(-1)
    else:
        sig.append(0)
        
#    if data['close'].iloc[i]>avg_30+std*3:
#        acc += data['close'].iloc[i+1] - data['close'].iloc[i]
#        sig.append(1)
#    elif data['close'].iloc[i]<avg_30-std*3:
#        acc += -(data['close'].iloc[i+1] - data['close'].iloc[i])
#        sig.append(-1)
#    else:
#        sig.append(0)
        
    acc_list.append(acc)

plt.figure(0)
plt.plot(acc_list)

plt.figure(1)
plt.plot(raw['close'])