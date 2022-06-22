import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd
import os
from pyparsing import White
from kiara_processes import onboard_df
from ui_custom import table

dash.register_page(__name__, path="/")


layout = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        children=[html.Div(children=[
        html.P("Please prepare a folder with one or more subfolders representing titles/publications for your corpus, and copy/paste the path to this folder below."
        , className="card-text"),
        
        html.P("Onboard corpus into Kiara"
        , className="card-text"),

        html.Div(children=[
        
        dbc.Input(
            id = 'corpus-selection',
            placeholder='Paste path to folder containing corpus',
            persistence=True,
            persistence_type='session',
        ),

        html.Br(),

        dbc.Input(id="corpus-alias", placeholder="Corpus alias", type="text", persistence=True,
            persistence_type='session'),

        html.Br(),
        
        dbc.Button("Confirm", color="light", id='confirm-selection', className="me-1", n_clicks=0),

        ], style={"width":"40%"}),

        html.Br(),

        # html.P(id='selected-corpus'),

        html.Div(id='corpus-result'),

        ])]
    ),
    className="mt-3",),

    ])

tab1 = html.Div(id='corpus-selection-head')
tab2 = html.Div(id='corpus-selection-tail')

corpus_result = dcc.Loading(children=[
        html.Div(id='corpus-selection-info'),
        dbc.Tabs(
        [
        dbc.Tab(tab1, label="Dataset head", label_style={"color": "#2c3e50"}),
        dbc.Tab(tab2, label="Dataset tail", label_style={"color": "#2c3e50"})
        ]),       
],
        type="default",
        color='grey')


@callback(
Output("corpus-result", "children"),
    [Input('corpus-selection','value'),
    Input('corpus-alias','value'),
    Input('confirm-selection', 'n_clicks')])
def display_corpus(corpus,alias,confirm):
    if confirm>0:   
        if corpus and alias:
            time.sleep(1)
            return corpus_result

@callback(
    Output('initial-alias','data'),
    Output('corpus-selection-head','children'),
    Output('corpus-selection-tail','children'),
    Output('confirm-selection','n_clicks'),
    [Input('corpus-selection','value'),
    Input('corpus-alias','value'),
    Input('confirm-selection', 'n_clicks')]
)
def preview_data(corpus,alias,confirm):
    if confirm>0:
        if corpus and alias:
            preview = onboard_df(corpus,alias)
            df_head = table.create_table(preview[0])
            df_tail = table.create_table(preview[1])
            
            return alias, df_head, df_tail, 0

    else:
        raise PreventUpdate