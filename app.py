import dash
import dash_labs as dl
import dash_bootstrap_components as dbc
from dash import html, Input, Output, State, dcc

external_stylesheets = [dbc.themes.FLATLY]

app = dash.Dash(
    __name__, plugins=[dl.plugins.pages], external_stylesheets=external_stylesheets, suppress_callback_exceptions=True, assets_ignore='.*.js'
    )

# this won't be necessary at the moment
# nb_view = html.Div(
#     [
#         dbc.Button("Open notebook view", id="open-offcanvas", n_clicks=0),
#         dbc.Offcanvas(
#             html.Div(children=[
#                 dbc.Row(dbc.Button("download .ipynb", color="light", id='export-ipynb', size="sm", style={"float":"right", "margin-bottom":"1em"}),),
#                 html.H5("1. Corpus information"),
#                 dcc.Markdown('''
#                  ```

#                 publications_list =  [file for file in os.listdir(f'./datasets/{folder}/') if file != '.DS_Store'  ]

#                 files_list = []

#                 for pub in publications_list:
#                     files = os.listdir(f"./datasets/{folder}/{pub}/")
#                     files_list.append(files)
                
#                 files_list_flat = [item for sublist in files_list for item in sublist]
                
#                 sources = pd.DataFrame(files_list_flat, columns=['file_name'])")
#                 ''', style={"border":".2px solid grey"}),
        
#                 dbc.Textarea(className="mb-3", placeholder="Notes.."),

#                 html.H5("2. Subset selection"),
#                 dcc.Markdown('''
#                  ```
#                 sources_subset = sources[sources[date] == 1917]")
#                 ''', style={"border":".2px solid grey"}),
        
#                 dbc.Textarea(className="mb-3", placeholder="Notes..")]),
#             id="offcanvas",
#             title="Topic modelling - ChroniclItaly collection",
#             placement="end",
#             is_open=False,
            
#         ),
#     ],
#     style={'display':'block','float':'right', 'padding':'1em'}
# )

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
    #nb_view,

    ],brand='LUMY PROTOTYPING / Topic Modelling')


app.layout = dbc.Container(
    [navbar,dcc.Store(id="stored-data", data=None),dcc.Store(id="initial-alias", data=None),dcc.Store(id="augmented-data-alias", data=None),dcc.Store(id="augmented-data2-alias", data=None),dcc.Store(id="stored-subset", data=[]),dcc.Store(id="viz-data", data=[]),dcc.Store(id="viz-date", data=[]), dl.plugins.page_container]

)

# @app.callback(
#     Output("offcanvas", "is_open"),
#     Input("open-offcanvas", "n_clicks"),
#     [State("offcanvas", "is_open")],)
# def toggle_offcanvas(n1, is_open):
#     if n1:
#         return not is_open
#     return is_open

# temporary solution to handle bidirectionality from viz
app.clientside_callback(
    """
    function(clicks,value) {
        if (clicks>0) {
            date = document.getElementById('date-info').value
            return date

        }
    }
    """,
    Output("viz-date", "data"),
    [Input('confirm-date',"n_clicks"),
    Input("date-info", "value")],
)


if __name__ == "__main__":
    app.run_server(debug=True)