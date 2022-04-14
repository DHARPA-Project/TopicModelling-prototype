import dash
from dash import html, Input, Output, State, dcc, dash_table
import dash_bootstrap_components as dbc

from processing_steps.pr_step1 import dir_list


ui_step1 = dbc.Card(
    dbc.CardBody(
        [
        html.P("Select a corpus to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            # pythlabel="Select corpus",
            [dir for dir in dir_list],
            id = 'corpus-selection',
            #dcc.Dropdown(['NYC', 'MTL', 'SF'], 'NYC', id='demo-dropdown'),
            # children= [dbc.DropdownMenuItem(dir) for dir in dir_list],
        ),

        html.Div(id='dd-output-container'),

        #dbc.Table.from_dataframe(id='dd-output-container')
        #dash_table.DataTable(id='dd-output-container')

        ]
    ),
    className="mt-3",
)



