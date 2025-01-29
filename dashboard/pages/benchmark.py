import dash
from dash import html, dcc

from utils import print_results

import dash_bootstrap_components as dbc

from adapter import Adapter

from config import Config

c = Config()
adapter = Adapter(c.data['database'])

dash.register_page(__name__, path_template="/benchmark/<benchmark_id>")

def layout(benchmark_id=0, **kwargs):
    benchmark = adapter.get_benchmark(benchmark_id)
    if benchmark:
        usecase_list = 'This benchmark has no associated usecases.'
        if benchmark.usecases:
            usecase_list = html.Div([
                html.Div([
                    dcc.Link(
                        html.Img(src=usecase.thumbnail, className='card-img-top', height=325),
                        href=f'/usecase/{usecase.id}'),
                    html.Div([
                        html.Div([
                            html.H5(usecase.title)
                        ], className='card-title'),
                        html.P([
                            usecase.short_description
                        ], className='card-text'),
                    ], className='card-body')
                ], className='card bg-light mb-3')
                for usecase in benchmark.usecases
            ], className='card-group')

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'Benchmark'))
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        html.Tbody([
                            html.Tr([
                                html.Th('Data set'),
                                html.Td(
                                    dcc.Link(benchmark.dataset.title, href=f'/dataset/{benchmark.dataset.id}')
                                )
                            ]),
                            html.Tr([
                                html.Th('Model'),
                                html.Td(
                                    dcc.Link(benchmark.model.title, href=f'/model/{benchmark.model.id}')
                                )
                            ]),
                            html.Tr([
                                html.Th('Defense'),
                                html.Td(
                                    dcc.Link(benchmark.defense.title, href=f'/defense/{benchmark.defense.id}')
                                )
                            ]),
                            html.Tr([
                                html.Th('Attack'),
                                html.Td(
                                    dcc.Link(benchmark.attack.title, href=f'/attack/{benchmark.attack.id}')
                                )
                            ]),
                            html.Tr([
                                html.Th('Threat model'),
                                html.Td(benchmark.threat_model)
                            ]),
                        ])
                    )
                )
            ),
            dbc.Row(
                dbc.Col(html.H5('Running the benchmark:'))
            ),
            dbc.Row(
                dbc.Col(dcc.Markdown(f"""```python
from robusthub import models, attacks, defenses, benchmarks

model = models.load('{benchmark.model.repo}', '{benchmark.model.name}')
defense = defenses.load('{benchmark.defense.repo}', '{benchmark.defense.name}')
attack = attacks.load('{benchmark.attack.repo}', '{benchmark.attack.name}')
benchmark = benchmarks.Benchmark(attack(threat_model), [metrics.Accuracy()])
result = benchmark.run(model, defense, testloader)"""))
            ),
            dbc.Row(
                dbc.Col(html.H5('Results:'))
            ),
            dbc.Row(
                print_results(benchmark.results)
            ),
            dbc.Row(
                dbc.Col(html.H5('Associated usecases:'))
            ),
            dbc.Row(
                dbc.Col(usecase_list)
            )
        ])
    else:
        return html.Div()
