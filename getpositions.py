# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 14:03:08 2021

@author: garla
"""
import pandas as pd
from datetime import datetime,timedelta
# import matplotlib.pyplot as plt

# acc = pd.read_csv('acceldata2.csv').sort_values(by='Timestamp').reset_index(drop=True)
# InstanceStartTime = datetime.strptime(acc.loc[145148,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
# InstanceEndTime = InstanceStartTime

# acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)

def getpositions(acceldata):
    rx1 = 0
    vx1 = 0
    ry1 = 0
    vy1 = 0
    xpositions = []
    ypositions = []
    
    for k in range(len(acceldata)):
        if k == acceldata.first_valid_index() :
            continue
        if k == acceldata.first_valid_index()+1:
            ax1 = acceldata.loc[k-1, 'X acceleration (m/s^2)'] + 0.14
            ay1 = acceldata.loc[k-1, 'Y acceleration (m/s^2)'] + 0.24
            
            t2 = datetime.strptime(acceldata.loc[k,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            t1 = datetime.strptime(acceldata.loc[k-1,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
            
            vx = vx1 + (t2-t1).total_seconds()*ax1
            vy = vy1 + (t2-t1).total_seconds()*ay1
            
            vx1 = vx
            vy1 = vy
            continue
        ax2 = acceldata.loc[k-2, 'X acceleration (m/s^2)'] + 0.16
        ax1 = acceldata.loc[k-1, 'X acceleration (m/s^2)'] + 0.16
        ay2 = acceldata.loc[k-2, 'Y acceleration (m/s^2)'] + 0.25
        ay1 = acceldata.loc[k-1, 'Y acceleration (m/s^2)'] + 0.25
        
        t2 = datetime.strptime(acceldata.loc[k,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        t1 = datetime.strptime(acceldata.loc[k-1,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
        t0 = datetime.strptime(acceldata.loc[k-2,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f")
    
        vx = vx1 + (t2-t1).total_seconds()*ax1
        vy = vy1 + (t2-t1).total_seconds()*ay1
    
        rx = rx1 + (t2-t1).total_seconds()*(vx1 + (t1-t0).total_seconds()*ax2)
        ry = ry1 + (t2-t1).total_seconds()*(vy1 + (t1-t0).total_seconds()*ay2)
        # print(vx1,ax1,rx,vy1,ay1,ry)
        xpositions.append(rx)
        ypositions.append(ry)
        vx1 = vx
        rx1 = rx
        vy1 = vy
        ry1 = ry
    
    return [xpositions, ypositions]