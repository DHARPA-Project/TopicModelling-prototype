import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd
from processing_steps.pr_step1 import dir_list
from processing_steps.pr_step1 import get_df
from viz_templates.ui_step1_viz import create_viz_step1

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

        html.Div(id='slider-output-test')
        ])]
    ),
    className="mt-3",),

    ])

tab1 = html.Div(id='corpus-selection-head')
tab2 = html.Div(id='corpus-selection-tail')

corpus_result = html.Div(children=[
        dbc.Tabs(
        [
        dbc.Tab(tab1, label="Dataset head"),
        dbc.Tab(tab2, label="Dataset tail")
        ]),
        html.Div(id='corpus-selection-info'),
        html.H5("Dataset exploration and filtering"
            , className="card-title", style={'padding-top':'1em'}),
        dbc.Row(
            [
                dbc.Col(html.Div([
                    html.P('Display settings'),
                                     
                    html.Div(id='radio_container', children=[
                        dcc.Dropdown(id='select-color',
                    options= ['blue', 'green','grey', 'orange', 'purple', 'red'],
                    value='blue',
                    placeholder="Select color",
                    ),
            #dcc.RadioItems(id='select-color', options = ['blue', 'green','grey', 'orange', 'purple', 'red'], value='blue', inline=True, labelStyle={"padding":"1em"}),
        ]),
                    
                ]), width=2, style={'padding-top':'1em'}),
                dbc.Col(html.Div([
            html.Div(id='corpus-selection-slider'),
            html.Div(id='corpus-selection-viz'),
                ]), width=10),
            ]
        ),
        
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
Output("corpus-selection-viz", "children"),
#Output("corpus-selection-slider", "children"),
[Input("corpus-selection", "value"),
Input('select-color', 'value')])
def output_text(value,color):
    if value:
        result = get_df(value)

        if result is None:
            raise PreventUpdate

        elif result:

            
            df_head = html.Div(children=[
                html.H5("Dataset preview - head"
            , className="card-title", style={'padding-top':'1em'}),
                dbc.Table.from_dataframe(pd.DataFrame.from_dict(result['preview1'])) 
                ])
            df_tail = html.Div(children=[
                html.H5("Dataset preview - tail"
            , className="card-title", style={'padding-top':'1em'}),
                dbc.Table.from_dataframe(pd.DataFrame.from_dict(result['preview2'])) 
                ]) 
            
            corpus_info = html.Div(children=[
                html.H5("Dataset Info"
            , className="card-title", style={'padding-top':'1em'}),
                html.P(f"This corpus contains {result['files-len']} documents from {result['pub-list-len']} titles", className="card-text") 
                ]) 
            
            
            viz_df = pd.DataFrame.from_dict(result['viz-data'])
            
            
            unique_dates = viz_df[viz_df['agg'] == 'month']['date'].unique()

           
            """
                slider = dcc.RangeSlider(0, len(unique_dates), id='select-range', value=[0, len(unique_dates)-1],  marks={
                    0: {'label': unique_dates[0]},
                    len(unique_dates): {'label': unique_dates[len(unique_dates)-1]},
                    }
            )
            """
            
            viz = html.Div(children=[
                create_viz_step1(result['viz-data'],color or 'blue'),
                ])

           ## table = dash_table.DataTable(
           #     data=df.to_dict('records')

           # )

            output = df_head, df_tail, corpus_info, viz
        
            return output
    
    # prevent error display in debug mode
    else:
        return None,None,None,None

@callback(
    Output('slider-output-test', 'children'),
    Input('select-range', 'value'))
def update_output(value):
    print(value)
