import dash
from dash import html

import dash_bootstrap_components as dbc

from adapter import Adapter

from utils import print_results

adapter = Adapter('sqlite:///../robusthub.db')

dash.register_page(__name__, path_template="/dataset/<dataset_id>")

def layout(dataset_id=0, **kwargs):
    dataset = adapter.get_dataset(dataset_id)
    if dataset:
        benchmarks = adapter.get_benchmarks(dataset_id=dataset_id)
        benchmark_list = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Model'),
                html.Th('Attack'),
                html.Th('Defense'),
                html.Th('Results')
            ]))
        ] + [html.Tr([
                html.Td(b.model.title),
                html.Td(b.attack.title),
                html.Td(b.defense.title),
                html.Td(print_results(b.results))
            ])
            for b in benchmarks
        ])

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{dataset.title}'))
            ),
            dbc.Row(
                dbc.Col(dbc.Button("Download", color="primary", href=dataset.url))
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            benchmark_list
        ])
    else:
        return html.Div()
