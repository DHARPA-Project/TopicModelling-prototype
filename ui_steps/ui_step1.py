import dash
from dash import html, Input, Output, State, dcc, dash_table
import dash_bootstrap_components as dbc

from processing_steps.pr_step1 import dir_list

ui_step1 = html.Div(children=[
    dbc.Card(
    dbc.CardBody(
        [
        html.P("Prior to running this workflow, a corpus needs to be added in a 'datasets' folder located at the root of the 'TopicModelling-prototype' repository."
        , className="card-text"),

        html.P("Inside the repository, one or more subfolders representing titles/publications need to contain text files named with the following convention: LCCN title information and publication date (yyyy-mm-dd), like for example: '/sn86069873/1900-01-05/'."
        , className="card-text"),
        
        html.P("Select a corpus to work with"
        , className="card-text"),
        
        dcc.Dropdown(
            [dir for dir in dir_list],
            id = 'corpus-selection',
        ),

        html.Div(id='corpus-selection-head'),

        html.Div(id='corpus-selection-tail'),

        html.Div(id='corpus-selection-info'),

        ]
    ),
    className="mt-3",),
    
    html.Iframe(srcDoc=f"""
    <!DOCTYPE html>
    <meta charset="utf-8">
    <title>timestamped-corpus</title>
    <link rel="stylesheet" type="text/css" href="../assets/inspector.css">
    <head></head>
    <body>
    <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
    <script type="module">

    import define from "../assets/index.js";
    import {{Runtime, Library, Inspector}} from "../assets/runtime.js";


    const runtime = new Runtime();
    runtime.module(define, name => {{
        if (name === "style") {{
            //console.log(new Inspector)
            return new Inspector(document.head)
            //return new Inspector(document.body)
            // document.head.appendChild(sc)
        }} 

        if (name === "viewof chart") {{   
            var elem = document.createElement('div')
            elem.setAttribute('id','chart')
            document.body.appendChild(elem)
            return new Inspector(document.querySelector("#chart"));
    }} 
    }});
    </script>
     """,style={'width':'100%'},height=500)
    
    ])


