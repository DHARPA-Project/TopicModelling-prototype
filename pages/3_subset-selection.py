import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, callback, dash_table
from dash.exceptions import PreventUpdate
import time
import pandas as pd
# from processing_steps.pr_step1 import dir_list
# from processing_steps.pr_step1 import get_df
from visualizations.timestamped_corpus import create_viz_step1
from kiara_processes import timestamped_corpus_data


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
        )
                    
                
                ]),
                
                label="Data selection", label_style={"color": "#2c3e50"}),

                dbc.Tab(html.Div(children=[
                    html.Div(children=[
                        html.Div('Click on date on top of corpus explorer to display related data',style={"padding-top":"1em", "padding-bottom":"1em"}),
                        dbc.Input(value="No date selected", id='date-info', readonly=True,size="sm",style={"width": "10%","display":"inline","margin-right":"1em","background-color":"white"}),
                        dbc.Button('View data', color="light", className="me-1", id='confirm-date', n_clicks=0),
                    ]
                    ),
                    
                    html.Div(id='viz-data-display', children=[]),

                ]), label="Visualization exploration", label_style={"color": "#2c3e50"})
                ]
            ),
            
        ]
    ),
    className="mt-3",),


    ])

@callback(
Output("corpus-selection-viz", "children"),
Output("viz-data", "data"),
Output("datatable-advanced-filtering", "data"),
Output("datatable-advanced-filtering", "columns"),
Output('reset-data','n_clicks'),
Input('augmented-data-alias','data'),
Input('augmented-data2-alias','data'),
Input('select-color','value'),
Input('select-scale','value'),
Input('select-agg','value'),
Input('datatable-advanced-filtering', 'derived_virtual_data'),
Input('reset-data','n_clicks')
)
def output_viz(alias,alias2,color,scale,agg,table,reset):
    
    viz_data = timestamped_corpus_data(alias2 if alias2 is not None else alias, 'publication_name' if alias2 is not None else 'publication', agg or 'month')
    
    viz_data['agg'] = agg or 'month'

    if reset > 0:
        table = None

    if table is not None:
        if (len(table) > 0) and (len(table) < len(viz_data)):      
            viz_data = pd.DataFrame.from_records(table)
            viz_data = viz_data[viz_data['agg'] == (agg or 'month')]

    viz_data = viz_data.astype(str)

    table_columns = [{"name":i, "id": i} for i in viz_data.columns]

    height= 130 + len(viz_data['publication_name'].unique())*23

    viz_data = viz_data.to_dict('records')

    # if reset>0:
    #     viz_df = pd.DataFrame.from_dict(viz_data)
    #     viz_data = viz_df.to_dict('records')
    
    viz = html.Div(children=[
        create_viz_step1(viz_data, color or 'blue',height, scale or 'color',agg or 'month'),
        ])
    
    return viz, viz_data, viz_data, table_columns, 0

    

@callback(  
Output("viz-data-display", "children"),
Output('confirm-date','n_clicks'),
[Input('confirm-date',"n_clicks"),
Input("viz-date", "data"),
Input('viz-data','data'),
Input('select-agg', 'value'),
])
def display_viz_data(clicks,dvalue,viz_data,agg):
    
    if clicks > 0:
        viz_df = pd.DataFrame.from_records(viz_data)

        date = dvalue.split(',')
        year = date[0]
        month = date[1] if len(date[1]) > 1 else f"0{date[1]}"
        day = date[2]
        
        if agg == 'month':
            data_tab = viz_df[viz_df['date'].apply(lambda x: x.startswith(f"{year}-{month}-")) ]
        
        if agg == 'year':
            data_tab = viz_df[viz_df['date'].apply(lambda x: x.startswith(f"{year}-")) ]
        
        if agg == 'day':
            data_tab = viz_df[viz_df['date'].apply(lambda x: x.startswith(f"{year}-{month}-{day}")) ]
        
        tab = dbc.Table.from_dataframe(data_tab)

        
        return tab,0
        
        
        

        


# @callback(
# Output("stored-subset", "data"),
# Output("subset-button", "n_clicks"),
# [Input("subset-button", "n_clicks"),
# Input("subset-alias", "value"),
# Input('datatable-advanced-filtering', 'derived_virtual_data'),
# Input("stored-subset","data")
# ])
# def display_viz_data(subset_click,alias,data,prev_data):
#     if (subset_click >0) and (len(data)>0) and alias is not None :
#         if len(prev_data) == 0:
#             return [{'alias': alias, 'data': data}], 0
#         else:
#             subsets = prev_data
#             subsets.append({'alias': alias, 'data': data})
#             return subsets, 0

        
# @callback(
#     Output('subset-list','children'),
#     Input("stored-subset","data")
# )
# def display_subsets(data):
#     #print(data)
#     if len(data) > 0:
#         subsets = []
#         for datum in data:
#             subsets.append(dbc.ListGroupItem(datum['alias']))
#         return subsets

#     else:
#         #print('stored data none')
#         #print(data)
#         return 'No subset yet'
                                    