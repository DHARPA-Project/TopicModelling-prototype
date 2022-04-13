from dash import html
import dash_bootstrap_components as dbc

from ui_steps.ui_step1 import step1
from ui_steps.ui_step2 import step2

steps = html.Div(
    [
    dbc.Tabs(
    [
        dbc.Tab(step1, label="Data selection", active_label_style={'border-bottom': '2px solid var(--bs-body-color)'}, label_style={'color':'var(--bs-body-color)'}),
        dbc.Tab(step2, label="Pre-processing", active_label_style={'border-bottom': '2px solid var(--bs-body-color)'}, label_style={'color':'var(--bs-body-color)'}),
    ]
    )
    ],style={'clear':'both'}
)

