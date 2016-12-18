import time
import pandas as pd
import logging

def kline_parser(k_list):
    logger = logging.getLogger()      
    map_buf = []
    for line in k_list:
        unit = {}
        unit["time_stamp"] = line[0]
        unit["open"] = line[1]
        unit["high"] = line[2]
        unit["low"] = line[3]
        unit["close"] = line[4]
        unit["vol"] = line[5]
        
        timeTuple = time.localtime(int(unit["time_stamp"])/1000)
        unit["time"] = time.strftime('%Y-%m-%d_%H:%M:%S',timeTuple)
        
        map_buf.append(unit)
    logger.info(unit["time"]+':'+str(unit["close"]))
    return map_buf
    
def MA(data, avg):
    prepend = []
    if len(data)<=avg:
        return []
    prepend_value = data[0]
    for i in range(0,avg-1):
        prepend.append(prepend_value)
    prepend.extend(data)
    
    result = []
    for i in range(0,len(data)):
        tmp_sum = 0
        for j in range(0,avg):
            tmp_sum += prepend[i+j]
        result.append(tmp_sum/avg)
    
    return result