import dash
from dash import html, dcc
from components.navbar import get_navbar

dash.register_page(__name__, path="/", name="Home")

layout = html.Div([
    get_navbar(),

    html.Div(
        className="text-white text-center",
        style={
            "backgroundImage": "url('/assets/images/bg1.png')",
            "backgroundSize": "contain",
            "backgroundRepeat": "no-repeat",
            "backgroundPosition": "center",
            "paddingTop": "100px",
            "paddingBottom": "100px",
            "height": "auto",
            "minHeight": "450px",     
        },
    ),

    html.Div(className="text-center my-4", children=[
        dcc.Link("📊 Customer Info", href="/customer", className="btn custom-link btn-lg mx-2", style={
        "backgroundColor": "white",
        "color": "#023047",
        "border": "2px solid #240046"
    }),
        dcc.Link("📂 Account Info", href="/account", className="btn custom-link btn-lg mx-2", style={
        "backgroundColor": "white",
        "color": "#023047",
        "border": "2px solid #240046"
    }),
    ])
])
