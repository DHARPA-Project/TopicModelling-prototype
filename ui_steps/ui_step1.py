from dash import html
import dash_bootstrap_components as dbc

from processing_steps.pr_step1 import dir_list


ui_step1 = dbc.Card(
    dbc.CardBody(
        [
        html.P("Select a corpus to work with"
        , className="card-text"),
        
        dbc.DropdownMenu(
            label="Select corpus",
            children= [dbc.DropdownMenuItem(dir) for dir in dir_list],
        )
        ]
    ),
    className="mt-3",
)