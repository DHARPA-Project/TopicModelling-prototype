import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, dcc


app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=[dbc.themes.FLATLY], include_assets_files=False, suppress_callback_exceptions=True
    )

nb_view = html.Div(
    [
        dbc.Button("Open notebook view", id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            html.P(
                "This may contain static notebook view mock-up at later stage."
            ),
            id="offcanvas",
            title="Title",
            placement="end",
            is_open=False,
            
        ),
    ],
    style={'display':'block','float':'right', 'padding':'1em'}
)

navbar = dbc.NavbarSimple(children=[
    
    dbc.DropdownMenu(
        [
            dbc.DropdownMenuItem(page["name"], href=page["path"])
            for page in dash.page_registry.values()
            if page["module"] != "pages.not_found_404"
        ],
        nav=True,
        label="Workflow steps",
        style={"padding":"1em"}
        
    ),
    nb_view,

    ],brand='LUMY PROTOTYPING / Topic Modelling')


app.layout = dbc.Container(
    [navbar,dcc.Store(id="stored-data", data=None), dl.plugins.page_container],

)

@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


if __name__ == "__main__":
    app.run_server(debug=True)