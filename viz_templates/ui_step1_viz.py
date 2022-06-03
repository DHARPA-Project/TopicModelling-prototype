from dash import html

def create_viz_step1(input_data,color,height,scale_type,agg):
    
    timestamped_corpus = html.Iframe(srcDoc=f"""
            <!DOCTYPE html>
            <meta charset="utf-8">
            <title>timestamped-corpus</title>
            <link rel="stylesheet" type="text/css" href="../assets/visualizations/timestamped-corpus/inspector.css">
            <head></head>
            <body>
            <script src="https://cdn.jsdelivr.net/npm/d3@6"></script>
            <script type="module">

            import define from "../assets/visualizations/timestamped-corpus/index.js";
            import {{Runtime, Library, Inspector}} from "../assets/visualizations/timestamped-corpus/runtime.js";


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

                if (name === 'dateInfo') {{
                    return {{
                        fulfilled(value) {{ 
                            const divDate = parent.document.getElementById('date-info')
                            
                            if (divDate !== null) {{
                                divDate.value = value
                            }}

                            }},
                    }};
                }}
            }});

            main.redefine("source",{input_data})
            main.redefine("timeSelected","{agg}")
            main.redefine("userColor","{color}")
            main.redefine("scaleType","{scale_type}")
            
            </script>
            """,style={'width':'100%'},height=height)
        
       
        
    return timestamped_corpus