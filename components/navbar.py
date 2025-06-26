from dash import html, dcc, callback, Output, Input

def get_navbar():
    return html.Nav(
        className="navbar navbar-expand-lg navbar-dark px-4 shadow",
        style={
            "background-color": "#023047",
            "color": "#ffffff",
            "position": "sticky",  # Make navbar sticky
            "top": "0",            # Stick to top
            "zIndex": "1000"       # Ensure it stays above other content
        },
        children=[
            dcc.Location(id="url", refresh=False),

            html.Div(className="container-fluid", children=[
                html.A("🏦 Customer Churn Dashboard", className="navbar-brand", href="#"),
                html.Div(id="nav-links", className="d-flex gap-2")
            ])
        ]
    )

# Callback to update active nav button
@callback(
    Output("nav-links", "children"),
    Input("url", "pathname")
)
def update_nav_links(pathname):
    def get_class(target):
        return "btn btn-outline-light active" if pathname == target else "btn btn-outline-light"

    return [
        dcc.Link("Home", href="/", className=get_class("/")),
        dcc.Link("Customer Info", href="/customer", className=get_class("/customer")),
        dcc.Link("Account Info", href="/account", className=get_class("/account")),
    ]
