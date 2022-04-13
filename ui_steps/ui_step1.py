from dash import html
import dash_bootstrap_components as dbc


step1 = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is the data selection space", className="card-text")
        ]
    ),
    className="mt-3",
)