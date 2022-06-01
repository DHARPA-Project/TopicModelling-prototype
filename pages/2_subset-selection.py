import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd
from processing_steps.pr_step1 import dir_list
from processing_steps.pr_step1 import get_df
from viz_templates.ui_step1_viz import create_viz_step1

dash.register_page(__name__)

layout = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        children=[html.H5("Dataset exploration and filtering"
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
                      ],style={"padding-bottom":"1em"}),

                    html.Div(id='radio_container2', children=[
                        dcc.Dropdown(id='select-scale',
                    options= ['color','height'],
                    value='color',
                    placeholder="Select scale type",
                    ),
                      ],style={"padding-bottom":"1em"}),
                    

                    html.Div(id='radio_container3', children=[
                        dcc.Dropdown(id='select-agg',
                    options= ['year','month', 'day'],
                    value='month',
                    placeholder="Aggregate by",
                    ),
                      ],style={"padding-bottom":"1em"}),

                ]), width=2, style={'padding-top':'1em'}),
                dbc.Col(html.Div([
            #html.Div(id='corpus-selection-slider'),
            html.Div(id='corpus-selection-viz'),
                ]), width=10),
            ]
        ),
        dbc.Tabs(
            [
            dbc.Tab(
                html.Div(children=[

                    dash_table.DataTable(
                    columns = [],
                    data=None,
                    id='datatable-advanced-filtering',
                    filter_action="native",
                    page_size= 10,
                    ),
                    html.Div(children=[

                    dbc.Button("Reset Filters", color="light", className="me-1", id="reset-data", n_clicks=0),
                    dbc.Button(
                                    "Save subset",
                                    id="collapse-button",
                                    className="me-1",
                                    color="light",
                                    n_clicks=0,
                                ),
                                dbc.Collapse(
                                    children=[
                                        dbc.Input(id="subset-alias", placeholder="Subset alias..", type="text", style={'margin-top':'.8em', 'margin-bottom':'.5em'}),
                                        dbc.Button("Confirm", color="light", className="me-1", id='subset-button', n_clicks=0)
                                    ],
                                    id="collapse",
                                    is_open=False,
                                ),
                    
                        ],style={'float':'right','padding':'1em'}),
                    
                
                ]),
                
                label="Data selection", label_style={"color": "#2c3e50"}),

                dbc.Tab(html.Div(children=[
                    html.Div(id='viz-data-display'),
                    dcc.Input(id='date-info',value='')

                ]), label="Visualization exploration", label_style={"color": "#2c3e50"})
                ]
            ),
            
        dbc.Row(
               html.Div(
                   children=[
                       html.H5('Subsets'),
                       html.Div(id='subset-list',
                        children=[dbc.ListGroup(
                            children=[]
                        )],
                        style={"margin-top":"1em"})

                   ]
                        
                    )
        )]
    ),
    className="mt-3",),


    ])

@callback(
Output("corpus-selection-viz", "children"),
Output("datatable-advanced-filtering", "data"),
Output("datatable-advanced-filtering", "columns"),
Output('reset-data','n_clicks'),
[Input('stored-data','data'),
Input('select-color', 'value'),
Input('select-scale', 'value'),
Input('select-agg', 'value'),
Input('datatable-advanced-filtering', 'derived_virtual_data'),
Input('reset-data','n_clicks')
])
def output_text(data,color,scale,agg,table,reset):
    if data:
        viz_df = pd.DataFrame.from_dict(data['viz-data'])

        viz_df = viz_df[viz_df['agg'] == (agg or 'month')]

        if table is not None:
            if (len(table) > 0) and (len(table) < len(viz_df)):      
                viz_df = pd.DataFrame.from_records(table)
                viz_df = viz_df[viz_df['agg'] == (agg or 'month')]


        viz_data = viz_df.to_dict('records')
        
        if reset>0:
            viz_df = pd.DataFrame.from_dict(data['viz-data'])
            viz_data = viz_df.to_dict('records')

        height = 130 + len(viz_df['publication_name'].unique())*23
            
        viz = html.Div(children=[
                create_viz_step1(viz_data, color or 'blue',height, scale or 'color',agg or 'month'),
                ])

        table_columns = [{"name":i, "id": i} for i in viz_df.columns]


        output = viz, viz_data, table_columns, 0
        
        return output

    else:
        raise PreventUpdate

@callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks"),
    Input("subset-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, n2, is_open):
    if n or n2:
        return not is_open
    return is_open
    

@callback(  
Output("viz-data-display", "children"),
[Input("date-info", "value")
])
def display_viz_data(dvalue):
    print(dvalue)

@callback(
Output("stored-subset", "data"),
Output("subset-button", "n_clicks"),
[Input("subset-button", "n_clicks"),
Input("subset-alias", "value"),
Input('datatable-advanced-filtering', 'derived_virtual_data'),
Input("stored-subset","data")
])
def display_viz_data(subset_click,alias,data,prev_data):
    if (subset_click >0) and (len(data)>0) and alias is not None :
        if len(prev_data) == 0:
            return [{'alias': alias, 'data': data}], 0
        else:
            subsets = prev_data
            subsets.append({'alias': alias, 'data': data})
            return subsets, 0

        
@callback(
    Output('subset-list','children'),
    Input("stored-subset","data")
)
def display_subsets(data):
    #print(data)
    if len(data) > 0:
        subsets = []
        for datum in data:
            subsets.append(dbc.ListGroupItem(datum['alias']))
        return subsets

    else:
        #print('stored data none')
        #print(data)
        return 'No subset yet'
                                    