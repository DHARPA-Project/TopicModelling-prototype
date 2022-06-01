import dash 
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div(
    [
        html.P("Select a subset to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            id='subset-selection',
            children = []
        ),
    ]
)



@callback(
    Output('subset-selection','children'),
    Input('stored-subset','data')
)
def load_subset(data):
    print('hello')

