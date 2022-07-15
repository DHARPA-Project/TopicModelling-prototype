import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table, ALL
from kiara_processes import get_table_preview, extract_metadata, get_col_unique_values, map_pub_ids
from dash.exceptions import PreventUpdate
from ui_custom import table

dash.register_page(__name__)

layout = dbc.Card(children=[

    dbc.CardBody(
    [   
        html.Br(),
        dbc.Alert("The metadata extraction feature will work with file names formatted as per LCCN title information and publication date (yyyy-mm-dd) format, like so: '/sn86069873/1900-01-05/'", color="light"),
        html.Br(),
        dbc.Label("Extract metadata from file names?"),
        dbc.RadioItems(
            options=[
                {"label": "yes", "value": True},
                {"label": "no", "value": False},
            ],
            value=False,
            id="extract-metadata",
            inline=True,
        ),
        html.Br(),
        html.Div(id='col-selection', children=[]),
        html.Div(id='augmented-table', children=[]),
        html.Br(),
        html.Div(id='publication_name'),
        html.Br(),
        html.Div(id='pub_mapping'),
        html.Br(),
        html.Div(id='mapping_el', style={"maxWidth":"60%"}),
        html.Br(),
        html.Div(id='augmented-table-2'),

    ]
)

])

@callback(
    Output('col-selection','children'),
    [Input('extract-metadata','value'),
    Input('initial-alias','data')]
    )
def get_metadata(extract,alias):
    if extract:
        table_el = get_table_preview(alias)
        preview = table.create_table(table_el[0][0:2])
        columns = table_el[2]
        
        ui_el = html.Div(children=[
            html.Br(),
            html.P('Data preview'),
            preview,
            html.Br(),
            html.P('Select the column that contains the file names'),
            dcc.Dropdown(columns, id='col-sel'),
            html.Br(),
            dbc.Button("Confirm", color="light", id='confirm-col', className="me-1", n_clicks=0),
        ]) 
        return ui_el

@callback(
    Output('augmented-table','children'),
    Output('augmented-data-alias','data'),
    Output('publication_name','children'),
    [Input('col-sel', 'value'),
    Input('initial-alias','data'),
    Input('confirm-col', 'n_clicks')]
)
def augment_table(col,data,confirm):
    if col and data and confirm>0:
        result = extract_metadata(data,col)
        if result:
        
            ui_el = html.Div(children=[
                html.Br(),
                html.P('Augmented table preview'),
                table.create_table(result[0][0]),
                html.Br(),
                #dbc.Button('Use augmented table for next step', n_clicks=0, color="light", id='confirm-augment', className="me-1",),
                
            ]) 

            pub_name = html.Div(children=[dbc.Label("Map publication references with names?"),
                dbc.RadioItems(
                    options=[
                        {"label": "yes", "value": 1},
                        {"label": "no", "value": 2},
                    ],
                    value=None,
                    id="map_pub",
                    inline=True,
                ),])

            return ui_el, result[1], pub_name
        else:
            return html.Div('no table found'), None
    else:
        raise PreventUpdate


@callback(
    Output('pub_mapping','children'),
    Input('map_pub', 'value'),
    Input('augmented-data-alias','data'),
)
def map_pub_name(map,alias):

    if map == 1:
        columns = get_table_preview(alias)[2]
        pub_mapping = html.Div(children=[
            html.P('Select the column that contains publication references'),
            dcc.Dropdown(columns, id='pub_sel'),
            html.Br(),
            dbc.Button("Confirm", color="light", id='confirm-pub', className="me-1", n_clicks=0)
        ])
        return pub_mapping
    else:
        raise PreventUpdate

@callback(
    Output('mapping_el','children'),
    Input('pub_sel','value'),
    Input('augmented-data-alias','data'),
    Input('confirm-pub','n_clicks'),
)
def get_ref_tomap(col,alias,confirm):
    
    if col and alias and confirm > 0:

        cols =  get_col_unique_values(alias,col)
        input_group = []

        for idx, col in enumerate(cols):
            input = dbc.InputGroup([dbc.InputGroupText(col), dbc.Input(id={"index": idx, "type": "pub_name"},), html.Br()])
            input_group.append(input)
        
        input_group.append(html.Br())
        input_group.append(dbc.Button("Add publication names", color="light", id='confirm-pub-name', className="me-1", n_clicks=0))

        ui_input = html.Div(children = input_group)
       
        return ui_input

    else:
        raise PreventUpdate



@callback(
    Output('augmented-table-2', 'children'),
    Output('augmented-data2-alias','data'),
    Input('confirm-pub-name', 'n_clicks'),
    Input({'type': 'pub_name', 'index': ALL}, "value"),
    Input('pub_sel','value'), # pub indexes
    Input('augmented-data-alias','data'),
    Input('confirm-pub','n_clicks'),
)
def display_augmented_table(confirm, names, col, alias, confirm_pub):
    
    if names and confirm > 0 and confirm_pub > 0:
        # ids to map with names
        pub_ids =  get_col_unique_values(alias,col)
        
        # publication names
        pub_names = names

        augmented_table = map_pub_ids(alias,col,'publication_name',[pub_ids,pub_names])

        df_head = table.create_table(augmented_table[0][0])
        df_alias = augmented_table[1]
        
        return df_head, df_alias
    
    else:
        raise PreventUpdate



    