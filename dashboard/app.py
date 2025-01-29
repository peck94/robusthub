import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

# external JavaScript files
external_scripts = []

# external CSS stylesheets
external_stylesheets = [
    dbc.themes.BOOTSTRAP,
]

app = dash.Dash(
    external_stylesheets=external_stylesheets,
    external_scripts=external_scripts,
    use_pages=True)
app.title = 'RobustHub'

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Home", href="/"),
                dbc.NavLink("Documentation", href="/page-1"),
                dbc.NavLink("GitHub", href="https://github.com/peck94/robusthub"),
            ],
            brand="RobustHub",
            color="primary",
            dark=True,
        ),
        dbc.Container([
            dash.page_container
        ], id="page-content", className="pt-4")
    ]
)

if __name__ == "__main__":
    app.run_server(port=8888, threaded=True)
