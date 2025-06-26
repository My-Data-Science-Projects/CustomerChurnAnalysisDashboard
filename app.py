import dash
from dash import html

app = dash.Dash(__name__, use_pages=True, suppress_callback_exceptions=True)
server = app.server

# Only dynamic page content shown here
app.layout = html.Div([
    dash.page_container
])

if __name__ == "__main__":
    app.run(debug=True)
