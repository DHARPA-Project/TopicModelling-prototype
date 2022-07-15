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
Input('augmented-data-alias','data'),
Input('augmented-data2-alias','data'),
)
def output_viz(alias,alias2):
    viz_data = timestamped_corpus_data(alias2 if alias2 is not None else alias)
    viz_data['agg'] = 'month'
    viz_data = viz_data.astype(str)
   
    # print(viz_data.info())
    
    color = "blue"
    height= 130 + len(viz_data['publication_name'].unique())*23
    scale = 'color'
    agg = 'month'

    viz_data = viz_data.to_dict('records')
    
    viz = html.Div(children=[
        create_viz_step1(viz_data, color or 'blue',height, scale or 'color',agg or 'month'),
        ])
    
    return viz



# @callback(
# Output("corpus-selection-viz", "children"),
# Output("datatable-advanced-filtering", "data"),
# Output("datatable-advanced-filtering", "columns"),
# Output("viz-data", "data"),
# Output('reset-data','n_clicks'),
# [Input('stored-data','data'),
# Input('select-color', 'value'),
# Input('select-scale', 'value'),
# Input('select-agg', 'value'),
# Input('datatable-advanced-filtering', 'derived_virtual_data'),
# Input('reset-data','n_clicks')
# ])
# def output_text(data,color,scale,agg,table,reset):
#     if data:
#         viz_df = pd.DataFrame.from_dict(data['viz-data'])

#         viz_df = viz_df[viz_df['agg'] == (agg or 'month')]

#         if table is not None:
#             if (len(table) > 0) and (len(table) < len(viz_df)):      
#                 viz_df = pd.DataFrame.from_records(table)
#                 viz_df = viz_df[viz_df['agg'] == (agg or 'month')]


#         viz_data = viz_df.to_dict('records')
        
#         if reset>0:
#             viz_df = pd.DataFrame.from_dict(data['viz-data'])
#             viz_data = viz_df.to_dict('records')

#         height = 130 + len(viz_df['publication_name'].unique())*23
            
#         viz = html.Div(children=[
#                 create_viz_step1(viz_data, color or 'blue',height, scale or 'color',agg or 'month'),
#                 ])

#         table_columns = [{"name":i, "id": i} for i in viz_df.columns]


#         output = viz, viz_data, table_columns, viz_data, 0
        
#         return output

#     else:
#         raise PreventUpdate

# @callback(
#     Output("collapse", "is_open"),
#     [Input("collapse-button", "n_clicks"),
#     Input("subset-button", "n_clicks")],
#     [State("collapse", "is_open")],
# )
# def toggle_collapse(n, n2, is_open):
#     if n or n2:
#         return not is_open
#     return is_open
    

# @callback(  
# Output("viz-data-display", "children"),
# Output('confirm-date','n_clicks'),
# [Input('confirm-date',"n_clicks"),
# Input("viz-date", "data"),
# Input('viz-data','data'),
# Input('select-agg', 'value'),
# ])
# def display_viz_data(clicks,dvalue,data,agg):
#     if clicks > 0:
#         agg_level = agg or 'month'
#         viz_df = pd.DataFrame.from_dict(data)
#         date = dvalue.split(',')
#         print(date)
#         year = date[0]
#         month = date[1] if len(date[1]) > 1 else f"0{date[1]}"
#         day = date[2]
        
#         #if agg_level == 'month':
#         data_tab = viz_df[viz_df['date'].apply(lambda x: x.startswith(f"{year}-{month}-")) ]
#         print(data_tab.head())
        
#         tab = dbc.Table.from_dataframe(data_tab)

        
#         return tab,0
        
        
        

        


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
                                    