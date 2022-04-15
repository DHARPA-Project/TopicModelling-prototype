import dash
from dash import html, Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import os

from ui_steps.ui_nb import static_nb_view
from ui_steps.ui_general import steps

from processing_steps.pr_step1 import get_df
from ui_steps.ui_step1_viz import create_viz_step1

app = dash.Dash(external_stylesheets=[dbc.themes.FLATLY],include_assets_files=False)

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


@app.callback(
    Output("corpus-selection-head", "children"),
    Output("corpus-selection-tail", "children"),
    Output("corpus-selection-info", "children"),
    Output("radio_container", "style"),
    Output("corpus-selection-viz", "children"),
[Input("corpus-selection", "value"),
Input('select-color', 'value'),])

def output_text(value,color):

    result = get_df(value)

    if result is None:
        raise PreventUpdate

    elif result:

        df_head = html.Div(children=[
            html.H5("Dataset preview - head"
        , className="card-title", style={'padding-top':'1em'}),
            dbc.Table.from_dataframe(result[0]) 
            ])
        
        df_tail = html.Div(children=[
            html.H5("Dataset preview - tail"
        , className="card-title", style={'padding-top':'1em'}),
            dbc.Table.from_dataframe(result[1]) 
            ]) 
        
        corpus_info = html.Div(children=[
            html.H5("Dataset Info"
        , className="card-title", style={'padding-top':'1em'}),
             html.P(f"This corpus contains {result[2]} documents from {result[3]} titles", className="card-text") 
            ]) 

        st = {'display': 'inline'}

        viz = html.Div(children=[
            create_viz_step1(result[4],color),
            ])

        output = df_head, df_tail, corpus_info, st, viz
    
        return output
    
    # prevent error display in debug mode
    else:
        return None,None,None,None,None
    


if __name__ == "__main__":
    app.run_server(debug=True)

