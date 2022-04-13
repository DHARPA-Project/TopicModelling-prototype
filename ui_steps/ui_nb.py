from dash import html
import dash_bootstrap_components as dbc

static_nb_view = html.Div(
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