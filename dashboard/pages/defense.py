import dash
from dash import html

import dash_bootstrap_components as dbc

from adapter import Adapter

adapter = Adapter('sqlite:///../robusthub.db')

dash.register_page(__name__, path_template="/defense/<defense_id>")

def layout(defense_id=0, **kwargs):
    defense = adapter.get_defense(defense_id)
    if defense:
        benchmarks = adapter.get_benchmarks(defense=defense.id)
        benchmark_list = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Model'),
                html.Th('Attack'),
                html.Th('Results')
            ]))
        ] + [html.Tr([
                html.Td('model'),
                html.Td('attack'),
                html.Td('result')
            ])
            for b in benchmarks
        ])

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{defense.title}'))
            ),
            dbc.Row(
                dbc.Col(html.P("Loading the defense:"))
            ),
            dbc.Row(
                dbc.Col(html.Pre(html.Code([
                    "from robusthub import defenses",
                    html.Br(),
                    f"defense = defenses.load('{defense.repo}', '{defense.name}')"
                ])))
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            benchmark_list
        ])
    else:
        return html.Div()
