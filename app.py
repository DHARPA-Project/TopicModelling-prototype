import dash
from dash import html, Input, Output, State
import dash_bootstrap_components as dbc

from ui_els.ui_data_selection import step1
from ui_els.ui_data_selection import step2
from ui_els.ui_nb import static_nb_view
from ui_els.ui_general import steps


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
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)

