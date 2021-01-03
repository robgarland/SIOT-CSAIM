# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 18:04:44 2020

@author: garla
"""
from server import GSIServer
import time, csv

def info():
   # while x == 1:
        data = [] #array to add as a row to csv
        acceptgun = ["Pistol","SniperRifle","Rifle","Submachine Gun","Machine Gun","Shotgun"] #target weapons
        weaponstates = ["active","reloading"] #target weapon states
        
        kills = server.get_info("player","match_stats","kills") #info i want to obtain
        deaths = server.get_info("player","match_stats","deaths")
        health = server.get_info("player","state","health")
        weapons = server.get_info("player","weapons")
        team = server.get_info("player","team")
        mapname = server.get_info("map","name")
        
        obsid = server.get_info("player","steamid") #looked at to ensure i only get data from myself (issues occured with getting spectated data which was unwanted))
        providerid = server.get_info("provider","steamid")
        
        if obsid == providerid:
            for i in range(10):         #weapons are sent as a detailed json, to het the bit i want i have to split like so, 10 weapons at one time is a reasonable limit
                try:
                    weapon = weapons["weapon_"+str(i)]
                except KeyError:
                    continue
                else:
                    if weapon["state"] in weaponstates and weapon["type"] in acceptgun:
                        if team == "T": #adding rounnd info scores to data
                            teamscore = server.get_info("map","team_t","score")
                            enemyscore = server.get_info("map","team_ct","score")
                            data.append(kills)
                            data.append(deaths)
                            data.append(health)
                            data.append(mapname)
                            data.append(weapon["name"])
                            data.append(weapon["ammo_clip_max"])
                            data.append(weapon["ammo_clip"])
                            data.append(teamscore)
                            data.append(enemyscore)  
                        elif team == "CT":
                            teamscore = server.get_info("map","team_ct","score")
                            enemyscore = server.get_info("map","team_t","score")
                            data.append(kills)
                            data.append(deaths)
                            data.append(health)
                            data.append(mapname)
                            data.append(weapon["name"])
                            data.append(weapon["ammo_clip_max"])
                            data.append(weapon["ammo_clip"])
                            data.append(teamscore)
                            data.append(enemyscore)  
        return data        

def getGSIdata():
    try:    #block for csv file, creates new if unable to open existing - effectively first time program start
        csv_file = open('gamestatedata.csv','r', newline = "")
        GSIReader = csv.reader(csv_file, delimiter=',')
        cs = list(GSIReader)
        csv_file.close()  #closing read object for append object
    except:
        csv_file = open('gamestatedata.csv', 'w', newline="")
        GSIWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
        GSIWriter.writerow(['Current Kills','Current Deaths','Health','Map Name','Weapon Name','Weapon Clip Size','Current Ammo','Player Team Score','Enemy Team Score','Timestamp','SessionID'])
        session = 0
    else:
        if str(cs[-1][-1]) == 'SessionID':   #enabling differentiation between sessions (every time the game is opened)
            session = 0
            print("New Session Started:",session)
        else:
            session = int(cs[-1][-1]) + 1
            print("New Session Started:",session)
        csv_file = open('gamestatedata.csv','a', newline = "")
        GSIWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)    
        
    igts = float(server.get_info("provider","timestamp"))
    cts = float(format(time.time(),".0f"))   
    datacount = 0        
    while abs(igts - cts) <= 10:     #loop to continuously add data to the csv, only if there is a change, and there is a weapon of interest active. loop will only start once the player is playing the game.
        activity = server.get_info("player","activity")
        previous = []
        while activity == "playing":
            ts = float(format(time.time(),".2f"))
            toadd = info()
            if toadd != [] and toadd != previous:
                previous = []
                for i in range(len(toadd)):
                    previous.append(toadd[i])
                toadd.append(ts)
                toadd.append(session)
                GSIWriter.writerow(toadd)
                datacount += 1
            time.sleep(0.03)    #fastest weapon fire rate is 1000rpm meaning once every 0.06sec therefore Nvyquist means rate of 0.06/2
            activity = server.get_info("player","activity")
        igts = float(server.get_info("provider","timestamp"))
        cts = float(format(time.time(),".0f"))   
        
    try:
        csv_file.close()
    except:
        print("Collection Failed")
    else:
        if datacount == 0:
            print("Session not completed: 0 datapoints added")
        else:
            print("Session completed:",datacount,"datapoints added")
    
server = GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()
getGSIdata()
time.sleep(1)
server.shutdown()