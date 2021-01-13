# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 14:48:37 2021

@author: garla
"""
import pandas as pd
import pickle### Graphing
import plotly.graph_objects as go### Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input
## Navbar
from navbar import Navbar
from dataanalysis import data_analyser

gamestateDF = pd.read_csv('gamestatedata2.csv')
acceldataDF = pd.read_csv('acceldata2.csv').sort_values(by='Timestamp').reset_index(drop=True)
usefuldata = pd.read_csv('usefuldata.csv')
spraydata = pd.DataFrame(usefuldata[usefuldata['Type'] == 'Spray']).reset_index(drop=True)
burstdata = pd.DataFrame(usefuldata[usefuldata['Type'] == 'Burst']).reset_index(drop=True)
tapdata = pd.DataFrame(usefuldata[usefuldata['Type'] == 'Tap']).reset_index(drop=True)

nav = Navbar()

header = html.H3(
    'Select a session number to see a full time series brekdown of that session'
)

header2 = html.H3(
    'Select a session number to see a brekdown of that session'
)

header3 = html.H5(
    'Select Spray Number'
    )

header4 = html.H5(
    'Select Burst Number'
    )

header5 = html.H5(
    'Select Tap Number'
    )


graphoptions = [{'label':i,'value':i} for i in range(int(gamestateDF['SessionID'].max())+1)]
tableoptions = [{'label':'Session Gamestate Data','value':'gsd'},{'label':'Session Accelerometer Raw Data','value':'acc'}]

dropdown = html.Div(dcc.Dropdown(
    id = 'session_dropdown',
    options = graphoptions,
    value = gamestateDF.loc[gamestateDF.last_valid_index(),'SessionID'] #defaults to latest session
))

dropdown2 = html.Div(dcc.Dropdown(
    id = 'table_dropdown',
    options = tableoptions,
    value = 'gsd' #defaults to gamestate
))

dropdown3 = html.Div(dcc.Dropdown(
    id = 'spray_dropdown',
    options = [],
    value = 1 #defaults to first in category
))

dropdown4 = html.Div(dcc.Dropdown(
    id = 'burst_dropdown',
    options = [],
    value = 1 #defaults to gamestate
))

dropdown5 = html.Div(dcc.Dropdown(
    id = 'tap_dropdown',
    options = [],
    value = 1 #defaults to gamestate
))



graphoutput = html.Div(id = 'output1',
                children = [],
                )
tableoutput = html.Div(id = 'output2',
                children = [],
                )

sprayoutput = html.Div(id = 'output3',
                children = [],
                )
burstoutput = html.Div(id = 'output4',
                children = [],
                )
tapoutput = html.Div(id = 'output5',
                children = [],
                )

spraytext = html.Div(id = 'output6',
                children = [],
                )

bursttext = html.Div(id = 'output7',
                children = [],
                )

taptext = html.Div(id = 'output8',
                children = [],
                )

def update_dd_options(session):
    spray = spraydata[spraydata['SessionID'] == session]
    burst = burstdata[burstdata['SessionID'] == session]
    tap = tapdata[tapdata['SessionID'] == session]
    sprayoptions = [{'label':i,'value':i} for i in range(len(spray))]
    burstoptions = [{'label':i,'value':i} for i in range(len(burst))]
    tapoptions = [{'label':i,'value':i} for i in range(len(tap))]
    
    return sprayoptions, burstoptions, tapoptions

def create_tscatter(source, yaxis, linetype):
    goscatter = go.Scatter(
        x = source['Timestamp'],
        y = source[yaxis],
        name = yaxis, mode=linetype)
    return goscatter

def App():
    layout = html.Div([
        nav,dbc.Container([
            header,
            dropdown,
            graphoutput,
            dropdown2,
            tableoutput
            ])
    ])
    return layout

def Breakdown():
    layout = html.Div([
        nav,dbc.Container([
            header2,
            dropdown,
            dbc.Row([
                dbc.Col([header3,dropdown3,sprayoutput,spraytext]),
                dbc.Col([header4,dropdown4,burstoutput,bursttext]),
                dbc.Col([header5,dropdown5,tapoutput,taptext]),
                ])
            ])
    ])
    return layout
    
def table(dataframe):
    x = list(dataframe.columns)
    fig = go.Figure(data=[go.Table(header=dict(values=x),
                  cells=dict(values=[dataframe[x[i]] for i in range(len(x))]))
                      ])
    return fig
        

def build_graph_and_tables(sessionID,tableID):
    dff = pd.DataFrame(gamestateDF[gamestateDF['SessionID'] == sessionID])
    daa = pd.DataFrame(acceldataDF[acceldataDF['Timestamp'].between(dff.loc[dff.first_valid_index(),'Timestamp'],dff.loc[dff.last_valid_index(),'Timestamp'])])
    
    fig = go.Figure(data = [go.Scatter(
                            x = dff['Timestamp'],
                            y = dff["Current Ammo"],
                            name = "Current Ammo", mode="lines+markers",text=dff["Weapon Name"]),
                            create_tscatter(dff,"Current Kills","lines+markers"),
                            create_tscatter(dff,"Health","lines+markers"),
                            create_tscatter(dff,"Player Team Score","lines"),
                            create_tscatter(dff,"Enemy Team Score","lines"),
                            create_tscatter(daa,"X acceleration (m/s^2)","lines"),
                            create_tscatter(daa,"Y acceleration (m/s^2)","lines")], 
        layout = go.Layout(
        title = 'Session {} Raw Data Plot'.format(sessionID),
        xaxis = {'title': 'Time'},
        hovermode = 'x unified'))
    
    graph = dcc.Graph(
           figure = fig
          )
    if tableID == 'gsd':
        dfftable = dcc.Graph(
            figure= table(dff))
        daatable = None
    elif tableID == 'acc':
        dfftable = None
        daatable = dcc.Graph(
            figure= table(daa))
    
    return graph, dfftable, daatable

def build_spray_tables(session,spraynumber,burstnumber,tapnumber):
    spray = pd.DataFrame(spraydata[spraydata['SessionID'] == session]).reset_index(drop=True)
    burst = pd.DataFrame(burstdata[burstdata['SessionID'] == session]).reset_index(drop=True)
    tap = pd.DataFrame(tapdata[tapdata['SessionID'] == session]).reset_index(drop=True)
    spraytokill = 0
    bursttokill = 0
    taptokill = 0
    if len(spray) > 0:
        spraytokill = len(spray[spray['InstanceKills'] > 0])/len(spray)
    if len(burst) > 0:
        bursttokill = len(burst[burst['InstanceKills'] > 0])/len(burst)
    if len(tap) > 0:
        taptokill = len(tap[tap['InstanceKills'] > 0])/len(tap)
    
    otherspray = spraydata[spraydata['SessionID'] != session]
    otherburst = burstdata[burstdata['SessionID'] != session]
    othertap = tapdata[tapdata['SessionID'] != session]
    
    otherstk = len(otherspray[otherspray['InstanceKills'] > 0])/len(otherspray)
    otherbtk = len(otherburst[otherburst['InstanceKills'] > 0])/len(otherburst)
    otherttk = len(othertap[othertap['InstanceKills'] > 0])/len(othertap)
    
    if spraytokill >= otherstk:
        t1 = 'Your spray is looking good!'
    elif spraytokill < otherstk:
        t1 = 'Your spray needs some attention, try spray traing in AimBotz!'
    if bursttokill >= otherbtk:
        t2 = 'Your burst is looking good!'
    elif bursttokill < otherbtk:
        t2 = 'Practise some burst firing in FFA!'
    if taptokill >= otherttk:
        t3 = 'Your tap firing is looking good!'
    elif taptokill < otherttk:
        t3 = 'Your tap fining needs some attention, play some headshot only or pistol FFA!'
    
    fig1 = go.Figure(data = [go.Scatter(
                            x=eval(spray.loc[spraynumber,'Position Data'])[0],
                            y=eval(spray.loc[spraynumber,'Position Data'])[1],
                            name = "Positional Data", mode="lines+markers", text="{}, Kills: {}".format(spray.loc[spraynumber,"Weapon Name"],spray.loc[spraynumber,"InstanceKills"]))
        ],
        layout = go.Layout(
        title = 'Session {}: Spray {}'.format(session,spraynumber),
        xaxis = {'title': 'X Pos (m)'},
        yaxis = {'title': 'Y Pos (m)'},
        hovermode = 'x unified')
        )
        
    fig2 = go.Figure(data = [go.Scatter(
                            x=eval(burst.loc[burstnumber,'Position Data'])[0],
                            y=eval(burst.loc[burstnumber,'Position Data'])[1],
                            name = "Positional Data", mode="lines+markers", text="{}, Kills: {}".format(burst.loc[burstnumber,"Weapon Name"],burst.loc[burstnumber,"InstanceKills"]))
        ],
        layout = go.Layout(
        title = 'Session {}: Burst {}'.format(session,burstnumber),
        xaxis = {'title': 'X Pos (m)'},
        yaxis = {'title': 'Y Pos (m)'},
        hovermode = 'x unified'))
        
    fig3 = go.Figure(data = [go.Scatter(
                            x=eval(tap.loc[tapnumber,'Position Data'])[0],
                            y=eval(tap.loc[tapnumber,'Position Data'])[1],
                            name = "Positional Data", mode="lines+markers", text="{}, Kills: {}".format(tap.loc[tapnumber,"Weapon Name"],tap.loc[tapnumber,"InstanceKills"]))
        ],
        layout = go.Layout(
        title = 'Session {}: Tap {}'.format(session,tapnumber),
        xaxis = {'title': 'X Pos (m)'},
        yaxis = {'title': 'Y Pos (m)'},
        hovermode = 'x unified'))
    
    graph1 = dcc.Graph(
           figure = fig1
          )
    
    graph2 = dcc.Graph(
           figure = fig2
          )
    
    graph3 = dcc.Graph(
           figure = fig3
          )
    
    text1 = html.H3( '{} Session Spray to kill ratio\n{}'.format(spraytokill,t1))
    text2 = html.H3( '{} Session Burst to kill ratio\n{}'.format(bursttokill,t2))
    text3 = html.H3( '{} Session Spray to kill ratio\n{}'.format(taptokill,t3))
    
    return graph1, text1, graph2, text2, graph3, text3
    

