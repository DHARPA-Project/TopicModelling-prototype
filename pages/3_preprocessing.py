import dash 
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(
    [
        html.P("Select a subset to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            ['subset-1917']
        ),
    ]
)
