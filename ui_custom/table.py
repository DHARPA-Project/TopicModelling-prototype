import dash 
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table


def create_table(data):

    table = dash_table.DataTable(
            data.to_dict('records'),
            [{"name": i, "id": i} for i in data.columns],

            css=[{
                'selector': '.dash-spreadsheet td div',
                'rule': '''
                    line-height: 15px;
                    max-height: 50px; min-height: 50px; height: 50px;
                    display: block;
                    overflow-y: scroll;
                '''
            }],

        #style_cell={'textAlign': 'left','lineHeight':'var(--bs-body-line-height)', 'padding':'.6em'},

        style_data={'textAlign': 'left', 'whiteSpace': 'normal'},
        style_data_conditional=[                
                {
                    "if": {"state": "selected"},              
                    "backgroundColor": '#FFF',
                    "border": '1px solid rgba(0,0,0.5)',
                },]
        )

    return table



