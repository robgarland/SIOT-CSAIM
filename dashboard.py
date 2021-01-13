# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 15:48:24 2021

@author: garla
"""

import dash
import pandas as pd
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime
import plotly.graph_objects as go### Dash

#import pandas as pd

from navbar import Navbar
from faceit import mostrecent

nav = Navbar()
usefuldata = pd.read_csv('usefuldata.csv')
gamestateDF = pd.read_csv('gamestatedata2.csv')

lastgames = mostrecent("RobO_")

def lastgameanalysis(array):
    length = len(array)
    totalkills = 0
    totaldeaths = 0
    lastkills = 0
    lastdeaths = 0
    wins = 0
    losses = 0
    lastw = 0
    lastl = 0
    rounddiff = 0
    lastdiff = 0
    for i in range(int(float(length/2))):
        totalkills += float(array[i][3])
        totaldeaths += float(array[i][5])
        lastkills += float(array[(int(float(length/2)))+i][3])
        lastdeaths += float(array[(int(float(length/2)))+i][5])
        if array[i][1] == 'W':
            wins += 1
        elif array[i][1] == 'L':
            losses += 1
        if array[(int(float(length/2)))+i][1] == 'W':
            lastw += 1
        elif array[(int(float(length/2)))+i][1] == 'L':
            lastl  += 1
        rounddiff += eval(array[i][2])
        lastdiff += eval(array[(int(float(length/2)))+i][2])
    
    KD = totalkills/totaldeaths
    LKD = lastkills/lastdeaths
    KDC = KD - LKD
    WP = float(wins)/(float(losses)+float(wins))
    LWP = float(lastw)/(float(lastl)+float(lastw))
    WPC = WP-LWP
    RDC = rounddiff - lastdiff
    
    return KD, KDC, WP, WPC, rounddiff, RDC

def simple_analysis(gsd,ufd):
    df = pd.DataFrame(gsd[gsd["SessionID"] == gamestateDF.loc[gamestateDF.last_valid_index(),'SessionID']]).reset_index(drop=True)
    dff = pd.DataFrame(ufd[ufd["SessionID"] == gamestateDF.loc[gamestateDF.last_valid_index(),'SessionID']]).reset_index(drop=True)
    totalrounds = 0
    for i in range(len(df)):
        if i == df.first_valid_index():
            pass
        elif abs(df.loc[i,"Player Team Score"] - df.loc[i-1,"Player Team Score"]) > 0 or abs(df.loc[i,"Enemy Team Score"] - df.loc[i-1,"Enemy Team Score"])>0:
            totalrounds +=1
    sprays = len(dff[dff["Type"] == "Spray"])
    bursts = len(dff[dff["Type"] == "Burst"])
    taps = len(dff[dff["Type"] == "Tap"])
    mins = abs(((datetime.strptime(df.loc[df.first_valid_index(),'Timestamp'], "%Y-%m-%d %H:%M:%S.%f"))-(datetime.strptime(df.loc[df.last_valid_index(),'Timestamp'], "%Y-%m-%d %H:%M:%S.%f"))).total_seconds())/60
    bulletsfired = abs(dff.loc[dff.last_valid_index(),"Total Bullets"] - abs(dff.loc[dff.first_valid_index(),"Total Bullets"]))
    return mins, sprays, bursts, taps, totalrounds, bulletsfired

kd, kdc, wp, wpc, rd, rdc = lastgameanalysis(lastgames)
mins, sprays, bursts, taps, totalrounds, bulletsfired = simple_analysis(gamestateDF,usefuldata)
types = ["Sprays","Bursts","Taps"]

body = dbc.Container([
       dbc.Row([
               dbc.Col([
                     html.H2("Recent Matches"),
                     html.Table([
                         html.Thead(
                             html.Tr([html.Th("Map"), html.Th("Result"), html.Th("Score"), html.Th("K"), html.Th("A"), html.Th("D")])
                                                     ),
                                         html.Tbody([
                                             html.Tr([html.Td(lastgames[i][col]) for col in range(6)]) for i in range(8)])
                                         ]), 
                   dbc.Row([
                       dbc.Col([html.Table([html.Thead(html.Tr([html.Th("Win %"),html.Th("vs. Prev 8")])),html.Tbody([html.Tr([html.Td("{:.2f}%".format(wp*100)),html.Td("{:.2f}%".format(wpc*100))])])])
                             ]),
                         
                     dbc.Col([html.Table([html.Thead(html.Tr([html.Th("Round Diff"),html.Th("vs. Prev 8")])),html.Tbody([html.Tr([html.Td("{:.2f}".format(rd)),html.Td("{:.2f}".format(rdc))])])])
                             ])
                     ]),
                   dbc.Row([
                       dbc.Col([html.Table([html.Thead(html.Tr([html.Th("AverageKD"),html.Th("vs. Prev 8")])),html.Tbody([html.Tr([html.Td("{:.2f}".format(kd)),html.Td("{:.2f}".format(kdc))])])])
                             ])
                   ])#,
                          # dbc.Button("View insights", color="secondary",href="/insights")
               ]),
              dbc.Col(
                 [
                     html.H2("Last Session"),
                     html.Table([
                         html.Thead(
                             html.Tr([html.Th("Minutes"), html.Th("Rounds Played"), html.Th("Bullets Fired")])
                                                     ),
                                         html.Tbody([
                                             html.Tr([html.Td("{:.2f}".format(mins)),html.Td("{:.2f}".format(totalrounds)),html.Td("{:.2f}".format(bulletsfired))])
                                         ]),
                                     ]),
                     dcc.Graph(
                         figure= go.Figure([go.Bar(x=types, y=[sprays, bursts, taps])])
                            ), dbc.Button("View details", color="secondary",href="/aim-breakdown")
                        ]
                     ),
                ]
            )
       ],
className="mt-4",
)
    
def Homepage():
    layout = html.Div([
    nav,
    body
    ])
    
    return layout
