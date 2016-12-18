import time
import json
import pandas as pd
import logging

from OkcoinSpotAPI import *
from greenlet import greenlet
import AnalysisTool
from APIKey import *

def init_log():
    logger = logging.getLogger()
    
    #set loghandler  
    fh = logging.FileHandler("./logTest.log")
    logger.addHandler(fh)
    
    ch = logging.StreamHandler()
    logger.addHandler(ch)

    #set formater  
    #formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")  
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    
    #set log level  
    logger.setLevel(logging.NOTSET)
  

def get_info(okcoinSpot):
    try:
        position_raw = okcoinSpot.userinfo()
    except:
        return None
    position = json.loads(position_raw)
    if position["result"]==False:
        return None
    available_btc = position["info"]['funds']['free']['btc']
    return available_btc

init_log()
sig = 0
last_time = 0


okcoinRESTURL = 'www.okcoin.cn'   #请求注意：国内账号需要 修改为 www.okcoin.cn
okcoinSpot = OKCoinSpot(okcoinRESTURL,apikey,secretkey)


while True:
    curtime = time.time()
    if curtime - last_time >5:
        last_time = curtime
        print("****************************************************")
        kline_data = okcoinSpot.getKline('1min','1000000','1362745600000')
        try:
            tick_data = okcoinSpot.ticker("btc_cny")
        except:
            continue
        print(tick_data["ticker"])
    
        bid = float(tick_data["ticker"]['buy'])
        
        
        pd_kline_data = pd.DataFrame(AnalysisTool.kline_parser(kline_data))
        #plt.plot(pd_kline_data['close'])
        one_min_30_line = AnalysisTool.MA(pd_kline_data["close"],30)
        one_min_7_line = AnalysisTool.MA(pd_kline_data["close"],7)
        one_min_3_line = AnalysisTool.MA(pd_kline_data["close"],3)
        
    #    plt.plot(one_min_7_line)
    #    plt.plot(one_min_30_line)
        #plt.plot(pd_kline_data["close"])
        #    
        one_min_30_last_one = one_min_30_line[len(one_min_30_line)-1]
        one_min_7_last_one = one_min_7_line[len(one_min_7_line)-1]
        one_min_3_last_one = one_min_3_line[len(one_min_3_line)-1]
        #print("30 line:" + str(one_min_30_last_one))
        #print("7 line:" + str(one_min_7_last_one))
        #print("3 line:" + str(one_min_3_last_one))
        
        sig = 0
        
        if one_min_7_last_one>one_min_30_last_one:
            if one_min_7_last_one - one_min_30_last_one>10:
                if bid>one_min_7_last_one:

                    sig = 1
                else:
                    sig = 0
            else:
                sig = 1
        else:
            sig = 0
            
    available_btc = get_info(okcoinSpot)
    if  available_btc == None:
        continue
    
    #print("holdings:" + available_btc)
    

    

    if bid < one_min_30_last_one:
        sig = 0
        #print("prevent loss")

    if sig==1:
        if float(available_btc)<0.02:
            buy_amount = 0.02-float(available_btc)
            a = okcoinSpot.trade('btc_cny','buy','6000',str(buy_amount))
            #print("buy:"+str(0.02-float(available_btc)))
    else:
        if float(available_btc)>0:
            sell_amount = float(available_btc)
            a = okcoinSpot.trade('btc_cny','sell','5000',str(sell_amount))
            #print("sell:"+str(0.02-float(available_btc)))





