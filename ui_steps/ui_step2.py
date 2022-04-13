from dash import html
import dash_bootstrap_components as dbc

step2 = dbc.Card(
    dbc.CardBody(
        [
            html.P("This will be the content of 2nd step", className="card-text")
        ]
    ),
    className="mt-3",
)