import dash

import dash_bootstrap_components as dbc

import pandas as pd

from dash import Input, Output, dcc, html, dash_table

from adapter import Adapter

adapter = Adapter('sqlite:///../robusthub.db')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Documentation", href="/page-1", active="exact"),
                dbc.NavLink("GitHub", href="/page-2", active="exact"),
            ],
            brand="RobustHub",
            color="primary",
            dark=True,
        ),
        dbc.Container(id="page-content", className="pt-4"),
    ]
)

def create_catalog(data_dict: dict):
    data_df = pd.DataFrame(data_dict)
    data_catalog = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in data_df.columns],
        style_cell={'textAlign': 'left'},
        style_header={
            'fontWeight': 'bold'
        },
        style_as_list_view=True
    )

    return data_catalog

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
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

        model_title = html.H2('Model catalog')
        models = adapter.load_models()
        models_dict = {
            'Name': [model.name for model in models],
            'Repository': [model.repo for model in models],
            'Tags': ['none' for model in models]
        }
        model_catalog = create_catalog(models_dict)

        defense_title = html.H2('Defense catalog')
        defenses = adapter.load_defenses()
        defenses_dict = {
            'Name': [defense.name for defense in defenses],
            'Repository': [defense.repo for defense in defenses],
            'Tags': ['none' for defense in defenses]
        }
        defense_catalog = create_catalog(defenses_dict)

        attacks_title = html.H2('Attack catalog')
        attacks = adapter.load_defenses()
        attacks_dict = {
            'Name': [attack.name for attack in attacks],
            'Repository': [attack.repo for attack in attacks],
            'Tags': ['none' for attack in attacks]
        }
        attacks_catalog = create_catalog(attacks_dict)

        main_content = html.Div(
            [
                dbc.Row(
                    dbc.Col(jumbotron)
                ),
                dbc.Row(
                    dbc.Col(model_title)
                ),
                dbc.Row(
                    dbc.Col(model_catalog)
                ),
                dbc.Row(
                    dbc.Col(defense_title)
                ),
                dbc.Row(
                    dbc.Col(defense_catalog)
                ),
                dbc.Row(
                    dbc.Col(attacks_title)
                ),
                dbc.Row(
                    dbc.Col(attacks_catalog)
                )
            ]
        )

        return main_content
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("Oh cool, this is page 2!")
    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


if __name__ == "__main__":
    app.run_server(port=8888, threaded=True)
