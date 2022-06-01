import dash 
from dash import html, dcc, callback, Input, Output

dash.register_page(__name__)

layout = html.Div(
    [
        html.P("Select a subset to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            id='subset-selection',
            options = []
        ),
    ]
)



@callback(
    Output('subset-selection','options'),
    Input('stored-subset','data')
)
def load_subset(data):
    if len(data) > 0:
        subsets = [datum['alias'] for datum in data]
        return subsets
    else:
        return 'No subset created'

