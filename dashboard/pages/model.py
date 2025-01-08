import dash
from dash import html

from utils import print_results

import dash_bootstrap_components as dbc

from adapter import Adapter

from config import Config

c = Config()
adapter = Adapter(c.data['database'])

dash.register_page(__name__, path_template="/model/<model_id>")

def layout(model_id=0, **kwargs):
    model = adapter.get_model(model_id)
    if model:
        benchmarks = adapter.get_benchmarks(model_id=model.id)
        benchmark_list = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Dataset'),
                html.Th('Threat model'),
                html.Th('Defense'),
                html.Th('Attack'),
                html.Th('Results')
            ]))
        ] + [html.Tr([
                html.Td(b.dataset.title),
                html.Td(b.threat_model),
                html.Td(b.defense.title),
                html.Td(b.attack.title),
                html.Td(print_results(b.results))
            ])
            for b in benchmarks
        ])

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{model.title}'))
            ),
            dbc.Row(
                dbc.Col(html.P("Loading the model:"))
            ),
            dbc.Row(
                dbc.Col(html.Pre(html.Code([
                    "from robusthub import models",
                    html.Br(),
                    f"model = models.load('{model.repo}', '{model.name}')"
                ])))
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            benchmark_list
        ])
    else:
        return html.Div()
