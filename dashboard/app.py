import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("RobustHub", className="display-3"),
            html.P(
                "Robust machine learning for everyone.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Design, compare and deploy robust machine learning models. "
                "Check out the model catalog, or learn how it works. Contribute defenses."
            ),
            html.P(
                dbc.ButtonGroup([
                    dbc.Button("Model catalog", color="primary", outline=True),
                    dbc.Button("Documentation", color="primary", outline=True),
                    dbc.Button("Contribute", color="primary", outline=True),
                ]),
                className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-body-secondary rounded-3",
)

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
            jumbotron,
            dash.page_container
        ], id="page-content", className="pt-4"),
    ]
)

if __name__ == "__main__":
    app.run_server(port=8888, threaded=True)
