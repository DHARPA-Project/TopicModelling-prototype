import dash 
from dash import html

dash.register_page(__name__)

layout = html.Div(
    [
        html.P("This is a test for page 2")
    ]
)
