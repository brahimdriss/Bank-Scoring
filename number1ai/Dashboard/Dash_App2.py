# -*- coding: utf-8 -*-

from flask import Flask, url_for
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from logging import basicConfig, DEBUG, getLogger, StreamHandler

from dash import Dash
from dash.dependencies import Input, State, Output
from .Dash_fun import apply_layout_with_auth, load_object, save_object
import dash_core_components as dcc
import dash_html_components as html

import dash
import dash_auth
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import plotly.offline as pyo


import dash_bootstrap_components as dbc
import plotly.express as px

import pandas as pd

url_base = '/dash/app2/'



def Add_Dash(server):

    german = pd.read_csv('taiwan.csv')

    features = german.drop(columns=['billSeptember', 'billAugust', 'billJuly', 'billJune', 'billMay', 'billApril',
                                    'prevSeptember', 'prevAugust', 'prevJuly', 'prevJune', 'prevMay', 'prevApril', 'amount']).columns


    features1 = german.drop(columns=['billSeptember', 'billAugust', 'billJuly', 'billJune', 'billMay', 'billApril',
                                 'prevSeptember', 'prevAugust', 'prevJuly', 'prevJune', 'prevMay', 'prevApril', 'payJune', 'payJuly', 'payMay', 'payAugust', 'paySeptember', 'amount', 'age', 'payApril'
                                 ]).columns

    def graph_reg(hue):
        if hue == 'none':
            trace0 = px.scatter(german, x="education", y="amount",
                                size='age',
                                title="Distribution of Credit Amount per Education")
        else:
            trace0 = px.scatter(german, x="education", y="amount", color=hue,
                                size='age',
                                title="Distribution of Credit Amount per Education")
        layout = go.Layout(title="Regression Linéaire")
        fig = go.Figure(data=trace0, layout=layout)
        return fig

    def graph_box_plot(xAxis, hue):
        if hue == 'none':
            trace0 = px.box(german, x=xAxis, y="amount",
                            notched=True,
                            title="Box plot of Credit Amount"
                            )
        else:
            trace0 = px.box(german, x=xAxis, y="amount", color=hue,
                            notched=True,
                            title="Box plot of Credit Amount"
                            )
        layout = go.Layout(title="Regression Linéaire")
        fig = go.Figure(data=trace0, layout=layout)
        return fig

    external_stylesheets = [dbc.themes.BOOTSTRAP]

    colors = {
        'background': '#FFFFFF',
        'text': '#000000'
    }
    app = dash.Dash(server=server, url_base_pathname=url_base,
                    external_stylesheets=external_stylesheets)
    #app = dash.Dash(server=server, , external_stylesheets=external_stylesheets)
    app.layout = html.Div([
         html.H1('Taiwan Bank Data', style = {'marginLeft' : '16em'}),
         html.Div([
             html.Div([
                         html.Div([
                             html.H3('Main Analysis Axis:'),
                             dcc.Dropdown(
                                 id='xaxis',
                                 options=[{'label': i.title(), 'value': i} for i in features],
                                 value='education'
                             )
                         ],
                         style={'width': '20%', 'display': 'inline-block', 'marginLeft' : '40em'})
                     ]),
     ################################################################################################################################            
     ################################################################################################################################            
             dbc.Row([
                         dbc.Col(
                             html.Div([
                                 dbc.Row(
                                                      html.Div([
                                                         html.H3('Secondary Analysis Axis:', style={'marginLeft': '5'}),
                                                         dcc.Dropdown(
                                                             id='yaxis',
                                                             options=[{'label': i.title(), 'value': i} for i in features],
                                                             value='sex',
                                                             style={'width': '15em'})
                                                      ],
                                                              style={'width': 'auto', 'marginLeft': '15em', 'marginTop': '3em'}
                                                      )
                                     ),  
                                 dbc.Row(
                                     html.Div([dcc.Graph(id='feature-graphic')], style={'width': 'auto','marginLeft': '5em'})
                                 )
                             ])
                         ),
     ###############################################################################          
                     dbc.Col(
                                 html.Div([
                                     dbc.Row(
                                                          html.Div([
                                                             html.H3('Secondary Analysis Axis:'),
                                                             dcc.Dropdown(
                                                                 id='yaxis1',
                                                                 options=[{'label': i.title(), 'value': i} for i in features1],
                                                                 value='marriage',
                                                                 style={'width': '15em'})],
                                                                  style={'width': 'auto', 'marginLeft': '15em', 'marginTop': '3em'}
                                                          )
                                         ),  
                                     dbc.Row(
                                         html.Div([dcc.Graph(id='feature_graphic_box')], style={'width': 'auto'})
                                     )
                                 ])
                              )
                     ]),     
     ################################################################################################################################                
             dbc.Row(
                 html.Div(dcc.Graph(id='feature_graphic_reg'), style={'width': '80%', 'marginLeft': '10em', 'marginTop': '3em'})
             )
         ]) 
     ], style={'padding':10, 'className':'dark-table', 'backgroundColor':'#FFDBF8'})
    
    @app.callback(
        Output('feature-graphic', 'figure'), 
        [Input('xaxis', 'value'),
         Input('yaxis', 'value')])
    def update_graph(xaxis_name, yaxis_name):
        if yaxis_name == '':
            return {
                    'data': [
                        {'x' : german[(german[xaxis_name]== i)][xaxis_name].value_counts().index.values,
                         'y' : german[(german[xaxis_name]== i)][xaxis_name].value_counts().values, 
                         'type': 'bar', 
                         'name': i
                        }
                        for i in german[xaxis_name].unique()
                    ],
                    'layout': {
                        'plot_bgcolor': colors['background'],
                        'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        },
                        'title' : 'Barplot count of {}'.format(xaxis_name)
                    }
                }
        else:
            return {
                    'data': [
                        {'x' : german[(german[xaxis_name]== i)][yaxis_name].value_counts().index.values,
                         'y' : german[(german[xaxis_name]== i)][yaxis_name].value_counts().values, 
                         'type': 'bar', 
                         'name': i
                        }
                        for i in german[xaxis_name].unique()
                    ],
                    'layout': {
                        'plot_bgcolor': colors['background'],
    #                     'paper_bgcolor': colors['background'],
                        'font': {
                            'color': colors['text']
                        },
                        'title' : 'Barplot count of {}'.format(xaxis_name)
                    }
                }


    @app.callback(
        Output('feature_graphic_reg', 'figure'), 
        [Input('xaxis', 'value'),
         Input('yaxis', 'value')])
    def update_graph_Reg(xaxis_name, yaxis_name):
        if xaxis_name == '':
            return graph_reg('none')
        else:
            return graph_reg(xaxis_name)

    @app.callback(
        Output('feature_graphic_box', 'figure'), 
        [Input('xaxis', 'value'),
         Input('yaxis1', 'value')])
    def update_graph_Box(xaxis_name, yaxis_name):
        if xaxis_name == '':
            return graph_box_plot(xaxis_name,'none')
        else:
            return graph_box_plot(xaxis_name, yaxis_name)

    return app.server
