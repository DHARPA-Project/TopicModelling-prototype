import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
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
                      ]),
                    
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
                    columns = [], #[{"name":i, "id": i} for i in viz_df.columns],
                    data=None,#viz_df[viz_df['agg'] == 'month'].to_dict('records'),
                    id='datatable-advanced-filtering',
                    filter_action="native",
                    # sort_action="native",
                    # sort_mode="multi",
                    # column_selectable="single",
                    # row_selectable="multi",
                    # row_deletable=True,
                    # selected_columns=[],
                    # selected_rows=[],
                    # page_action="native",
                    # page_current= 0,
                    page_size= 10,
                    ),
                    html.Div(children=[

                    dbc.Button("Reset", color="light", className="me-1", id="reset-data", n_clicks=0),
                    dbc.Button("Save subset", color="light", className="me-1")
                    
                        ],style={'float':'right','padding':'1em'}),
                ]),
                
                label="Data selection", label_style={"color": "#2c3e50"}),

                dbc.Tab(html.Div(), label="Visualization exploration", label_style={"color": "#2c3e50"})
                ]
            ),]
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
Input('datatable-advanced-filtering', 'derived_virtual_data'),
Input('reset-data','n_clicks')
])
def output_text(data,color,scale,table,reset):
    if data:
        viz_df = pd.DataFrame.from_dict(data['viz-data'])
        #viz_df['date'] = pd.to_datetime(viz_df['date'])

        viz_df = viz_df[viz_df['agg'] == 'month']

        if (table is not None) and (len(table) > 0):       
            viz_df = pd.DataFrame.from_dict(table)


        viz_data = viz_df.to_dict('records')
            #print(filtered.columns)
        
        if reset>0:
            viz_df = pd.DataFrame.from_dict(data['viz-data'])
            viz_data = viz_df.to_dict('records')

        height = 130 + len(viz_df['publication_name'].unique())*23
            
        viz = html.Div(children=[
                create_viz_step1(viz_data, color or 'blue',height, scale or 'color'),
                ])

        table_columns = [{"name":i, "id": i} for i in viz_df.columns]


        output = viz, viz_data, table_columns, 0
        
        return output

    else:
        raise PreventUpdate
    # if data:
    #     result = data

    #     if result is None:
    #         raise PreventUpdate

    #     elif result is not None:
            
            

    #         #print(table)

    #         # if table is not None:
    #         #     #print(len(table))
    #         #     filtered = pd.DataFrame.from_dict(table)
            
    #         #     viz_df = filtered

    #         #print(color)

    #         #print(viz_df)

            

    #         #table_columns = [{"name":i, "id": i} for i in viz_df.columns]
            
    #         #table_data =  viz_df.to_dict('records')

    #         #output = viz, table_data, table_columns
        
    #         return viz
    # # prevent error display in debug mode
    # else:
    #     return None

