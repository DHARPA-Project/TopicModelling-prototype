import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd
from processing_steps.pr_step1 import dir_list
from processing_steps.onboarding import onboard_df

dash.register_page(__name__, path="/")

layout = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        children=[html.Div(children=[
            html.P("Prior to running this workflow, a corpus needs to be added in a 'datasets' folder located at the root of the 'TopicModelling-prototype' repository."
        , className="card-text"),

        html.P("Inside the repository, one or more subfolders representing titles/publications need to contain text files named with the following convention: LCCN title information and publication date (yyyy-mm-dd), like for example: '/sn86069873/1900-01-05/'."
        , className="card-text"),
        
        html.P("Onboard corpus into Kiara"
        , className="card-text"),

        html.Div(children=[
            dcc.Dropdown(
            [dir for dir in dir_list],
            id = 'corpus-selection',
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

corpus_result = html.Div(children=[
        html.Div(id='corpus-selection-info'),
        dbc.Tabs(
        [
        dbc.Tab(tab1, label="Dataset head", label_style={"color": "#2c3e50"}),
        dbc.Tab(tab2, label="Dataset tail", label_style={"color": "#2c3e50"})
        ]),       
])


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

            df_head = html.Div(children=[
                html.H5("Dataset preview - head"
            , className="card-title", style={'padding-top':'1em'}),
                dash_table.DataTable(

                        preview[0].to_dict('records'),

                        [{"name": i, "id": i} for i in preview[0].columns],

                        id='tbl',

                        css=[{
                            'selector': '.dash-spreadsheet td div',
                            'rule': '''
                                line-height: 15px;
                                max-height: 50px; min-height: 50px; height: 50px;
                                display: block;
                                overflow-y: scroll;
                            '''
                        }],

                    #     tooltip_data=[
                    #         {
                    #         column: {'value': str(value), 'type': 'markdown'}
                    #         for column, value in row.items()
                    #         } for row in preview[1].to_dict('records')
                    #     ],

                    # tooltip_duration=None,

                    style_cell={'font_family': 'var(--bs-body-font-family)','textAlign': 'left', 'fontSize':'var(--bs-body-font-size)', 'fontWeight':'var(--bs-body-font-weight)','lineHeight':'var(--bs-body-line-height)', 'padding':'.6em'},

                    style_data={'font_family': 'var(--bs-body-font-family)','textAlign': 'left', 'fontSize':'var(--bs-body-font-size)', 'fontWeight':'var(--bs-body-font-weight)','lineHeight':'var(--bs-body-line-height)','whiteSpace': 'normal','height': 'auto'},

                    )
                   
                ])
            df_tail = html.Div(children=[
                    html.H5("Dataset preview - tail"
                , className="card-title", style={'padding-top':'1em'}),
                    
                    dash_table.DataTable(

                        preview[1].to_dict('records'),

                        [{"name": i, "id": i} for i in preview[1].columns],

                        id='tbl',

                        css=[{
                            'selector': '.dash-spreadsheet td div',
                            'rule': '''
                                line-height: 15px;
                                max-height: 50px; min-height: 50px; height: 50px;
                                display: block;
                                overflow-y: scroll;
                            '''
                        }],

                    #     tooltip_data=[
                    #         {
                    #         column: {'value': str(value), 'type': 'markdown'}
                    #         for column, value in row.items()
                    #         } for row in preview[1].to_dict('records')
                    #     ],

                    # tooltip_duration=None,

                    style_cell={'font_family': 'var(--bs-body-font-family)','textAlign': 'left', 'fontSize':'var(--bs-body-font-size)', 'fontWeight':'var(--bs-body-font-weight)','lineHeight':'var(--bs-body-line-height)', 'padding':'.6em'},

                    style_data={'font_family': 'var(--bs-body-font-family)','textAlign': 'left', 'fontSize':'var(--bs-body-font-size)', 'fontWeight':'var(--bs-body-font-weight)','lineHeight':'var(--bs-body-line-height)','whiteSpace': 'normal','height': 'auto'},

                    )
                                
                    #dbc.Table.from_dataframe(preview[1]) 
                    ]) 
            return df_head, df_tail, 0

    else:
        raise PreventUpdate


# @callback(
#     Output('corpus-selection-head','children'),
#     Output('corpus-selection-tail','children'),
#     Output('confirm-selection','n_clicks'),
#     #Input('corpus-selection','value'),
#     #Input('corpus-alias','value'),
#     Input('confirm-selection', 'n_clicks')
# )
# def preview_data(confirm):
#     print(confirm)
#     if confirm>0:
#         print('hello')
#         return ' ', ' ',0
        # if corpus and alias:
            
        #     preview = onboard_df(corpus,alias)

        #     df_head = html.Div(children=[
        #         html.H5("Dataset preview - head"
        #     , className="card-title", style={'padding-top':'1em'}),
        #         dbc.Table.from_dataframe(preview[0]) 
        #         ])
        #     df_tail = html.Div(children=[
        #             html.H5("Dataset preview - tail"
        #         , className="card-title", style={'padding-top':'1em'}),
        #             dbc.Table.from_dataframe(preview[1]) 
        #             ]) 
        #     return df_head, df_tail, 0

