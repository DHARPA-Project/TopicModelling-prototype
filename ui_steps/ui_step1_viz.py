from dash import html

# main.redefine("source", {input_data})

def create_viz_step1(input_data):

    timestamped_corpus = html.Iframe(srcDoc=f"""
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
        const main = runtime.module(define, name => {{

            if (name === "style") {{
                return new Inspector(document.head)
            }} 

            if (name === "viewof chart") {{   
                var elem = document.createElement('div')
                elem.setAttribute('id','chart')
                document.body.appendChild(elem)
                return new Inspector(document.querySelector("#chart"));
        }} 
        }});

        main.redefine("source",{input_data})

        </script>
        """,style={'width':'100%'},height=500)
    
    return timestamped_corpus