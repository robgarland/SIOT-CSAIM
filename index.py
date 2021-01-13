# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 16:01:24 2021

@author: garla
"""

import dash
import csv, boto3
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd

from apptest import App, build_graph_and_tables, Breakdown, update_dd_options, build_spray_tables

from dashboard import Homepage
from dataanalysis import data_analyser

s3 = boto3.resource('s3')
gamestateDF = pd.read_csv('gamestatedata2.csv')
acceldataDF = pd.read_csv('acceldata2.csv').sort_values(by='Timestamp').reset_index(drop=True)

# with open('usefuldata.csv','w',newline="") as csv_file:
#     CSVWriter = csv.writer(csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)  
#     useful = data_analyser(gamestateDF, acceldataDF)
#     CSVWriter.writerow(["Type","Weapon Name","InstanceBullets","InstanceKills","Position Data","SessionID","Total Bullets"])
#     for i in range(len(useful)):
#         CSVWriter.writerow(useful[i])

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id = 'url', refresh = False),
    html.Div(id = 'page-content')
])

@app.callback(Output('page-content', 'children'),
            [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/all-data':
        return App()
    elif pathname == '/aim-breakdown':
        return Breakdown()
#    elif pathname == '/insights':
#        pass
    else:
        return Homepage()
    
@app.callback([Output('output1', 'children'),
               Output('output2','children')],
              [Input('session_dropdown', 'value'),
               Input('table_dropdown', 'value')]
)
def update_graph(session,table):
    graph, dfftable, daatable = build_graph_and_tables(session,table)
    if table == 'gsd':
        return graph, dfftable
    else:
        return graph, daatable


@app.callback([Output('spray_dropdown','options'),
               Output('burst_dropdown','options'),
               Output('tap_dropdown','options')],
              [Input('session_dropdown', 'value')]
              )
def update_dropdowns(session):
        sprayoptions, burstoptions, tapoptions = update_dd_options(session)
        return sprayoptions, burstoptions, tapoptions


@app.callback([Output('output3', 'children'),
               Output('output4', 'children'),
               Output('output5', 'children'),
               Output('output6', 'children'),
               Output('output7', 'children'),
               Output('output8', 'children')],
              [Input('session_dropdown', 'value'),
              Input('spray_dropdown','value'),
              Input('burst_dropdown','value'),
              Input('tap_dropdown','value')])
def update_spray_tables(session,spraynumber,burstnumber,tapnumber):
    graph1, text1, graph2, text2, graph3, text3 = build_spray_tables(session,spraynumber,burstnumber,tapnumber)
    return graph1, graph2, graph3, text1, text2, text3
    


# @app.callback(
#     Output('output2','children'),
#     [Input('session_dropdown', 'value'), 
#      ]
#  )
# def update_table(session,table):
#     graph, dfftable, daatable = build_graph_and_tables(session)
#     if table == 'gsd':
#         return dfftable
#     elif table == 'acc':
#         return daatable


if __name__ == '__main__':
    app.run_server(debug=True)
   # s3.Bucket('siotbucket').download_file('acceldata2.csv', 'acceldata2.csv')
   # s3.Bucket('siotbucket').download_file('gamestatedata2.csv', 'gamestatedata2.csv')