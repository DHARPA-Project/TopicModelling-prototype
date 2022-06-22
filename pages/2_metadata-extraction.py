import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table
from kiara_processes import get_table_preview, extract_metadata
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
        html.Div(id='augmented-table', children=[])
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
            html.H5('Data preview'),
            preview,
            html.Br(),
            html.H5('Select the column that contains the file names'),
            dcc.Dropdown(columns, id='col-sel'),
            html.Br(),
            dbc.Button("Confirm", color="light", id='confirm-col', className="me-1", n_clicks=0),
        ]) 
        return ui_el

@callback(
    Output('augmented-table','children'),
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
                html.H5('Augmented table preview'),
                table.create_table(result[0]),
                html.Br(),
                
            ]) 

            return ui_el
        else:
            return html.Div('no table found')
    else:
        raise PreventUpdate
    