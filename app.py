import dash
from dash import html, Input, Output, State
import dash_bootstrap_components as dbc
import os

from ui_steps.ui_nb import static_nb_view
from ui_steps.ui_general import steps

from processing_steps.pr_step1 import get_df


app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY])

app_title = html.Div(children=[
    html.H2(['Topic Modelling'], 
            style={'padding':'.2em'})
])

app.layout = html.Div(children=[
    app_title,
    static_nb_view,
    steps
])

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(Output("dd-output-container", "children"), [Input("corpus-selection", "value")])
def output_text(value):

    df = dbc.Table.from_dataframe(get_df(value)) if value != None else None

    # id='dd-output-container')

    return df


if __name__ == "__main__":
    app.run_server(debug=True)

