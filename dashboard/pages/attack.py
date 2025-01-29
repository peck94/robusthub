import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

from adapter import Adapter

from utils import print_results

from config import Config

c = Config()

adapter = Adapter(c.data['database'])

dash.register_page(__name__, path_template="/attack/<attack_id>")

def layout(attack_id=0, **kwargs):
    attack = adapter.get_attack(attack_id)
    if attack:
        benchmarks = adapter.get_benchmarks(attack_id=attack.id)
        benchmark_list = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Model'),
                html.Th('Dataset'),
                html.Th('Threat model'),
                html.Th('Defense'),
                html.Th('Results')
            ]))
        ] + [html.Tr([
                html.Td(b.model.title),
                html.Td(b.dataset.title),
                html.Td(b.threat_model),
                html.Td(b.defense.title),
                html.Td(print_results(b.results))
            ], className='benchmarks_row')
            for b in benchmarks
        ])

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{attack.title}'))
            ),
            dbc.Row(
                dbc.Col(html.P("Loading the attack:"))
            ),
            dbc.Row(
                dbc.Col(dcc.Markdown(f"""```python
from robusthub import attacks

attack = attacks.load('{attack.repo}', '{attack.name}')
"""))
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            benchmark_list
        ])
    else:
        return html.Div()
