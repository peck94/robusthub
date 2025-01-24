import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)
app.title = 'RobustHub'

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Home", href="/"),
                dbc.NavLink("Documentation", href="/page-1"),
                dbc.NavLink("GitHub", href="/page-2"),
            ],
            brand="RobustHub",
            color="primary",
            dark=True,
        ),
        dbc.Container([
            dash.page_container
        ], id="page-content", className="pt-4"),
    ]
)

if __name__ == "__main__":
    app.run_server(port=8888, threaded=True)
