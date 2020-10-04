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

url_base = '/dash/app1/'


def Add_Dash(server):


    german = pd.read_csv("German_Complete.csv")
    features = ['Purpose', 'Status_Account', 'Saving_Account', 'Present', 'Personal_Status',
                'Property', 'Liable_People', 'Installment', 'Other', 'Housing', 'Job', 'Foreign_Worker']


    graphStyles = ['Bar', 'Markers', 'Lines', 'Lines+Markers']

    def graph_reg(hue):
        if hue == 'none':
            trace0 = px.scatter(german, x="Duration", y="Credit_Amount",
                                size='Age',
                                title="Distribution of Credit Amount per Duration")
        else:
            trace0 = px.scatter(german, x="Duration", y="Credit_Amount", color=hue,
                                size='Age',
                                title="Distribution of Credit Amount per Duration")
        layout = go.Layout(title="Regression Linéaire")
        fig = go.Figure(data=trace0, layout=layout)
        return fig

    def graph_box_plot(xAxis, hue):
        if hue == 'none':
            trace0 = px.box(german, x=xAxis, y="Credit_Amount",
                            notched=True,
                            title="Box plot of Credit Amount"
                            )
        else:
            trace0 = px.box(german, x=xAxis, y="Credit_Amount", color=hue,
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
    app = dash.Dash(server=server,external_stylesheets=external_stylesheets,url_base_pathname=url_base)
    app.layout = html.Div([
        html.H1('German Credit Data', style={'marginLeft': '16em'}),
        html.Div([
            html.Div([
                html.Div([
                    html.H3('Main Analysis Axis:'),
                    dcc.Dropdown(
                        id='xaxis',
                        options=[{'label': i.title(), 'value': i} for i in features],
                        value='Purpose'
                    )
                ],
                    style={'width': '20%', 'display': 'inline-block', 'marginLeft': '40em'})
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
                                    options=[{'label': i.title(), 'value': i}
                                             for i in features],
                                    value='',
                                    style={'width': '15em'})
                            ],
                                style={'width': 'auto', 'marginLeft': '15em', 'marginTop': '3em'}
                            )
                        ),

                        dbc.Row(
                            html.Div([dcc.Graph(id='feature-graphic')],
                                     style={'width': 'auto', 'marginLeft': '5em'})
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
                                    options=[{'label': i.title(), 'value': i}
                                             for i in features],
                                    value='none',
                                    style={'width': '15em'})],
                                style={'width': 'auto',
                                       'marginLeft': '15em', 'marginTop': '3em'}
                            )
                        ),

                        dbc.Row(
                            html.Div([dcc.Graph(id='feature_graphic_box')],
                                     style={'width': 'auto'})
                        )
                    ])

                )

            ]),

            ################################################################################################################################
            dbc.Row(
                html.Div(dcc.Graph(id='feature_graphic_reg'), style={
                         'width': '80%', 'marginLeft': '10em', 'marginTop': '3em'})
            )
        ])
    ], style={'padding': 10, 'className': 'dark-table', 'backgroundColor': '#FFDBF8'})


    @app.callback(
        Output('feature-graphic', 'figure'),
        [Input('xaxis', 'value'),
         Input('yaxis', 'value')])
    def update_graph(xaxis_name, yaxis_name):
        if yaxis_name == '':
            return {
                'data': [
                    {'x': german[(german[xaxis_name] == i)][xaxis_name].value_counts().index.values,
                     'y': german[(german[xaxis_name] == i)][xaxis_name].value_counts().values,
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
                    'title': 'Barplot count of {}'.format(xaxis_name)
                }
            }
        else:
            return {
                'data': [
                    {'x': german[(german[xaxis_name] == i)][yaxis_name].value_counts().index.values,
                     'y': german[(german[xaxis_name] == i)][yaxis_name].value_counts().values,
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
                    'title': 'Barplot count of {}'.format(xaxis_name)
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
            return graph_box_plot(xaxis_name, 'none')
        else:
            return graph_box_plot(xaxis_name, yaxis_name)

    return app.server


    # features = german.columns
    # featuresZAxis = german.drop(columns=['Purpose', 'Status_Account',
    #                                     'Saving_Account', 'Present', 'Personal_Status', 'Property']).columns
    # graphStyles = ['Bar', 'Markers', 'Lines', 'Lines+Markers']
    # colors = {
    #     'background': '#111111',
    #     'text': '#7FDBFF'
    # }
    # app = dash.Dash(server=server)
    # app.layout = html.Div([
    #     html.H1('German Credit Data'),
    #     html.Div([
    #         html.H3('X Axis:'),
    #         dcc.Dropdown(
    #             id='xaxis',
    #             options=[{'label': i.title(), 'value': i} for i in features],
    #             value='Duration'
    #         )
    #     ],
    #         style={'width': '20%', 'display': 'inline-block'}),
    #     html.Div([
    #         html.H3('Y Axis:'),
    #         dcc.Dropdown(
    #             id='yaxis',
    #             options=[{'label': i.title(), 'value': i} for i in features],
    #             value=''
    #         )
    #     ], style={'width': '20%', 'display': 'inline-block'}),
    #     html.Div([
    #         html.H3('Z Axis (Color):'),
    #         dcc.Dropdown(
    #             id='zaxis',
    #             options=[{'label': i.title(), 'value': i}
    #                     for i in featuresZAxis],
    #             value='Purpose'
    #         )
    #     ], style={'width': '20%', 'display': 'inline-block'}),
    #     dcc.Graph(id='feature-graphic')
    # ], style={'padding': 10, 'className': 'dark-table'})
    # @app.callback(
    #     Output('feature-graphic', 'figure'),
    #     [Input('xaxis', 'value'),
    #     Input('yaxis', 'value'),
    #     Input('zaxis', 'value')])
    # def update_graph(xaxis_name, yaxis_name, zaxis_name):
    #     if yaxis_name == '':
    #         return {
    #             'data': [
    #                 {'x': german[(german[xaxis_name] == i)][xaxis_name].value_counts().index.values,
    #                 'y': german[(german[xaxis_name] == i)][xaxis_name].value_counts().values,
    #                 'type': 'bar',
    #                 'name': i
    #                 }
    #                 for i in german[xaxis_name].unique()
    #             ],
    #             'layout': {
    #                 'plot_bgcolor': colors['background'],
    #                 'paper_bgcolor': colors['background'],
    #                 'font': {
    #                     'color': colors['text']
    #                 }
    #             }
    #         }
    #     else:
    #         return {
    #             'data': [
    #                 {'x': german[(german[xaxis_name] == i)][yaxis_name].value_counts().index.values,
    #                 'y': german[(german[xaxis_name] == i)][yaxis_name].value_counts().values,
    #                 'type': 'bar',
    #                 'name': i
    #                 }
    #                 for i in german[xaxis_name].unique()
    #             ],
    #             'layout': {
    #                 'plot_bgcolor': colors['background'],
    #                 'paper_bgcolor': colors['background'],
    #                 'font': {
    #                     'color': colors['text']
    #                 }
    #             }
    #         }





    
