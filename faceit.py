# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 16:53:45 2020

@author: garla
"""
import json
import requests

name = "RobO_"

def datagrab(url):
    headers = {"accept": "application/json", "Authorization" : "Bearer 8e0b7ac3-7d5b-4f15-b3cc-233bf6782f75"}
    r = requests.get(url, headers=headers)
    m = r.text
    entry = json.loads(m)
    #mdecode = m.decode("utf-8")
   # entry = eval(mdecode)
    return entry

def mostrecent(name):
    playerinfourl= "https://open.faceit.com/data/v4/players?nickname="+name+"&game=csgo" #interfacing to get the correct matches
    playerinfo = datagrab(playerinfourl)
    playerid= playerinfo["player_id"]
    matchhistoryurl = "https://open.faceit.com/data/v4/players/"+playerid+"/history?game=csgo&offset=0&limit=16"
    datastore1 = datagrab(matchhistoryurl)
    matches = datastore1["items"]
    matchids = []
    datastore = []
    keyinfo = []
    for i in range(16):
        matchid = matches[i]["match_id"]
        matchids.append(matchid)
    for i in range(16):
        matchdetailsurl = "https://open.faceit.com/data/v4/matches/"+matchids[i]+"/stats"
        matchdetails = datagrab(matchdetailsurl)
        datastore.append(matchdetails)
    for i in range(len(datastore)):
        maps = datastore[i]["rounds"][0]["round_stats"]["Map"]
        winningteamid = datastore[i]["rounds"][0]["round_stats"]["Winner"]
        for j in range(len(datastore[i]["rounds"][0]["teams"][0]["players"])):
            x = datastore[i]["rounds"][0]["teams"][0]["players"][j]["nickname"]
            if x == "RobO_":
                teamid = datastore[i]["rounds"][0]["teams"][0]["team_id"]
                Rkills = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Kills"]
                Rdeaths = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Deaths"]
                Rassists = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Assists"]
                Rheadshots = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Headshot"]
                Rtriple = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Triple Kills"]
                Rquad = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Quadro Kills"]
                Rpent = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["Penta Kills"]
                RMVP = datastore[i]["rounds"][0]["teams"][0]["players"][j]["player_stats"]["MVPs"]
                FS1 = datastore[i]["rounds"][0]["teams"][0]["team_stats"]["Final Score"]
                FS2 = datastore[i]["rounds"][0]["teams"][1]["team_stats"]["Final Score"]
        for j in range(len(datastore[i]["rounds"][0]["teams"][1]["players"])):
            y = datastore[i]["rounds"][0]["teams"][1]["players"][j]["nickname"]
            if y == "RobO_":
                teamid = datastore[i]["rounds"][0]["teams"][1]["team_id"]
                Rkills = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Kills"]
                Rdeaths = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Deaths"]
                Rassists = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Assists"]
                Rheadshots = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Headshot"]
                Rtriple = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Triple Kills"]
                Rquad = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Quadro Kills"]
                Rpent = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["Penta Kills"]
                RMVP = datastore[i]["rounds"][0]["teams"][1]["players"][j]["player_stats"]["MVPs"]
                FS1 = datastore[i]["rounds"][0]["teams"][1]["team_stats"]["Final Score"]
                FS2 = datastore[i]["rounds"][0]["teams"][0]["team_stats"]["Final Score"]
        if teamid == winningteamid:
            result = "W"
        else:
            result = "L"
        
        keyinfo.append([maps, result, "{} - {}".format(FS1,FS2), Rkills, Rassists, Rdeaths, Rheadshots, Rtriple, Rquad, Rpent, RMVP])
    return keyinfo
