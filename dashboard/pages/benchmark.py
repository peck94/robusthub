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
        
        threat_model = [
            f'threats.{ident}'
            for ident in benchmark.threat_model.split('; ')
        ]
        if len(threat_model) > 1:
            threat_model = f'threats.Composite(\n\t{",\n\t".join(threat_model)})'
        else:
            threat_model = threat_model[0]
        
        metric_names = [f'metrics.{m}' if '(' in m else f'metrics.{m}()' for m in benchmark.metrics.split("; ")]
        metrics = f'[{", ".join(metric_names)}]'

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
from robusthub import models, attacks, defenses, benchmarks, threats, datasets, metrics

# load data set
train_loader, val_loader, test_loader = datasets.CIFAR10().load()

# set threat model
threat_model = {threat_model}

# set metrics
metrics_list = {metrics}

# load model
model = models.load('{benchmark.model.repo}', '{benchmark.model.name}')

# load defense
defense = defenses.load('{benchmark.defense.repo}', '{benchmark.defense.name}')

# load attack
attack = attacks.load(
    '{benchmark.attack.repo}', '{benchmark.attack.name}',
    threat_model=threat_model)

# initialize benchmark
benchmark = benchmarks.Benchmark(attack, metrics_list)

# run benchmark
result = benchmark.run(model, defense, test_loader)"""))
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
