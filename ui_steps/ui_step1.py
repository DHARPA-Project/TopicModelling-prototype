import dash
from dash import html, Input, Output, State, dcc, dash_table
import dash_bootstrap_components as dbc

from processing_steps.pr_step1 import dir_list


ui_step1 = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        [
        html.P("Prior to running this workflow, a corpus needs to be added in a 'datasets' folder located at the root of the 'TopicModelling-prototype' repository."
        , className="card-text"),

        html.P("Inside the repository, one or more subfolders representing titles/publications need to contain text files named with the following convention: LCCN title information and publication date (yyyy-mm-dd), like for example: '/sn86069873/1900-01-05/'."
        , className="card-text"),
        
        html.P("Select a corpus to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            [dir for dir in dir_list],
            id = 'corpus-selection',
        ),

        html.Div(id='corpus-selection-head'),

        html.Div(id='corpus-selection-tail'),

        html.Div(id='corpus-selection-info'),

        html.Div(children=[
            dcc.RadioItems(['blue', 'green','grey', 'orange', 'purple', 'red'], 'blue', inline=True, id="select-color"),
        ],id='radio_container', style={"display":"none"}),
        

        html.Div(id='corpus-selection-viz'),

        ]
    ),
    className="mt-3",),
    
    
    ])


