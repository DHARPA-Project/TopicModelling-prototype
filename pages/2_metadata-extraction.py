import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback, dash_table

dash.register_page(__name__)

layout = dbc.Card(children=[

    dbc.CardBody(
    [   
        html.Br(),
        dbc.Label("Extract metadata from file name?"),
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
        html.Div(id='augmented-table', children=[])
    ]
)

])

@callback(
    Output('augmented-table','children'),
    [Input('extract-metadata','value')]
)
def extract_metadata(extract):
    if extract:
        return 'yes'