import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from dash.exceptions import PreventUpdate
import time
import pandas as pd
from processing_steps.pr_step1 import dir_list
from processing_steps.pr_step1 import get_df

dash.register_page(__name__, path="/")

layout = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        children=[html.Div(children=[
            html.P("Prior to running this workflow, a corpus needs to be added in a 'datasets' folder located at the root of the 'TopicModelling-prototype' repository."
        , className="card-text"),

        html.P("Inside the repository, one or more subfolders representing titles/publications need to contain text files named with the following convention: LCCN title information and publication date (yyyy-mm-dd), like for example: '/sn86069873/1900-01-05/'."
        , className="card-text"),
        
        html.P("Select a corpus to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            [dir for dir in dir_list],
            id = 'corpus-selection',
            persistence=True,
            persistence_type='session'
        ),

        html.P(id='selected-corpus'),

        html.Div(id='corpus-result'),

        ])]
    ),
    className="mt-3",),

    ])

tab1 = html.Div(id='corpus-selection-head')
tab2 = html.Div(id='corpus-selection-tail')

corpus_result = html.Div(children=[
        html.Div(id='corpus-selection-info'),
        dbc.Tabs(
        [
        dbc.Tab(tab1, label="Dataset head"),
        dbc.Tab(tab2, label="Dataset tail")
        ]),
        
])

@callback(
    Output('stored-data','data'),
    Input('corpus-selection','value')
)
def store_initial_dataset(value):
    if value:
        result = get_df(value)

        return result

@callback(
Output("corpus-result", "children"),
[Input("corpus-selection", "value"),])
def display_corpus(value):
    if value:
        time.sleep(1)
        return corpus_result

@callback(
Output("corpus-selection-head", "children"),
Output("corpus-selection-tail", "children"),
Output("corpus-selection-info", "children"),
[Input('stored-data','data')])
def context_el(data):
    if data is not None:
        
        df_head = html.Div(children=[
                html.H5("Dataset preview - head"
            , className="card-title", style={'padding-top':'1em'}),
                dbc.Table.from_dataframe(pd.DataFrame.from_dict(data['preview1'])) 
                ])
        df_tail = html.Div(children=[
                html.H5("Dataset preview - tail"
            , className="card-title", style={'padding-top':'1em'}),
                dbc.Table.from_dataframe(pd.DataFrame.from_dict(data['preview2'])) 
                ]) 
            
        corpus_info = html.Div(children=[
                html.H5("Dataset Information"
            , className="card-title", style={'padding-top':'1em'}),
                html.P(f"This corpus contains {data['files-len']} documents from {data['pub-list-len']} titles", className="card-text",style={'padding-bottom':'2em'}) 
                ])  

        return df_head, df_tail, corpus_info
    
    else:

        raise PreventUpdate
