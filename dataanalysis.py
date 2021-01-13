# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 10:37:41 2021

@author: garla
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from getpositions import getpositions
import csv

gamestateDF = pd.read_csv('gamestatedata2.csv')
acceldataDF = pd.read_csv('acceldata2.csv').sort_values(by='Timestamp').reset_index(drop=True)

def data_analyser(gsd,acc):         #anaylsing gsdata to figure out when a spray, burst or tap has occured.
    weaponnames = gsd['Weapon Name'].unique()
    TotalBullets = 0
    InstanceBullets = 0
    InstanceKills = 0
    useful = []
    for i in range(len(weaponnames)):
        df = pd.DataFrame(gsd[gsd['Weapon Name'] == weaponnames[i]]).reset_index(drop=True)
     #   print(len(df))
        for j in range(len(df)):
            add_to_useful = []
            if j == df.first_valid_index():
                pass
            elif df.loc[j,'Current Ammo'] - df.loc[j-1,'Current Ammo'] == -1: # checking if bullet has been fired
                TotalBullets += 1
                InstanceBullets += 1
                dt = datetime.strptime(df.loc[j,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f") #detection time
                pt = datetime.strptime(df.loc[j-1,'Timestamp'], "%Y-%m-%d %H:%M:%S.%f") #time of detection of previous gamestate
                timediff = (dt-pt).total_seconds()
                dk = df.loc[j,'Current Kills']
                pk = df.loc[j-1,'Current Kills']
                if dk - pk >= 1:
                    InstanceKills += (dk-pk)
                if timediff <= 0.25: #if the timedifference constitutes a spray/burst, look for the next instance (continue until time constraint is not satisfied)
                    if InstanceBullets == 1: # if it is the first bullet in the sequence, set start time, (the bullet could be part of an upcoming spray so do not append yet)
                        InstanceStartTime = dt
                        continue
                elif timediff > 0.25: #as soon as the timedifference is longer than acceptable for a spray/burst, stop adding to the instance, and append teh results.
                    if InstanceBullets == 1:
                        stype = 'Tap'
                        InstanceStartTime = dt
                        InstanceEndTime = InstanceStartTime
                        InstanceBullets = 1
                        acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                        positions = getpositions(acceldata)
                        session = df.loc[j,'SessionID']
                        add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                        useful.append(add_to_useful)
                        InstanceBullets = 0
                        InstanceKills = 0
                    elif 2 <= InstanceBullets <= 6:
                        stype = 'Burst'
                        InstanceEndTime = dt
                        acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                        positions = getpositions(acceldata)
                        session = df.loc[j,'SessionID']
                        add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                        useful.append(add_to_useful)
                        InstanceBullets = 0
                        InstanceKills = 0
                    elif InstanceBullets > 6:
                        stype = 'Spray' 
                        InstanceEndTime = dt
                        acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                        positions = getpositions(acceldata)
                        session = df.loc[j,'SessionID']
                        add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                        useful.append(add_to_useful)
                        InstanceBullets = 0
                        InstanceKills = 0 
            elif j == df.last_valid_index():
                if InstanceBullets == 1:
                    stype = 'Tap'
                    InstanceEndTime = InstanceStartTime
                    InstanceBullets = 1
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0
                elif 2 <= InstanceBullets <= 6:
                    stype = 'Burst'
                    InstanceEndTime = dt
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0
                elif InstanceBullets > 6:
                    stype = 'Spray' 
                    InstanceEndTime = dt
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0 
                
            else:
                if InstanceBullets == 1:
                    stype = 'Tap'
                    InstanceEndTime = InstanceStartTime
                    InstanceBullets = 1
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0
                elif 2 <= InstanceBullets <= 6:
                    stype = 'Burst'
                    InstanceEndTime = dt
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0
                elif InstanceBullets > 6:
                    stype = 'Spray' 
                    InstanceEndTime = dt
                    acceldata = pd.DataFrame(acc[acc['Timestamp'].between(str(InstanceStartTime- timedelta(microseconds=500000)),str(InstanceEndTime + timedelta(microseconds=500000)))]).reset_index(drop=True)
                    positions = getpositions(acceldata)
                    session = df.loc[j,'SessionID']
                    add_to_useful = [stype,weaponnames[i],InstanceBullets,InstanceKills, positions, session, TotalBullets]
                    useful.append(add_to_useful)
                    InstanceBullets = 0
                    InstanceKills = 0 
                InstanceBullets = 0
                InstanceKills = 0
                continue
    return useful                    
                
           
with open('usefuldata.csv','w',newline="") as csv_file:
    CSVWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)  
    useful = data_analyser(gamestateDF, acceldataDF)
    CSVWriter.writerow(["Type","Weapon Name","InstanceBullets","InstanceKills","Position Data","SessionID","Total Bullets"])
    for i in range(len(useful)):
        CSVWriter.writerow(useful[i])                
                
        
                          