import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

import numpy as np

import plotly.graph_objects as go
from plotly.graph_objs._figure import Figure
from plotly.subplots import make_subplots

from adapter import Adapter

from models import Benchmark

from utils import print_results, interpret_results

from config import Config

from typing import List

c = Config()

adapter = Adapter(c.data['database'])

dash.register_page(__name__, path_template="/usecase/<usecase_id>")

def get_summaries(benchmarks: List[Benchmark]) -> Figure:
    plots = {}
    for b in benchmarks:
        results = interpret_results(b)
        for metric in results['metrics']:
            values = results['metrics'][metric]
            if metric not in plots:
                plots[metric] = {
                    'standard': [],
                    'standard_err': [],
                    'robust': [],
                    'robust_err': [],
                    'bounds': values['bounds']
                }

            plots[metric]['standard'].append(values['standard']['mean'])
            plots[metric]['standard_err'].append(values['standard']['err'])
            plots[metric]['robust'].append(values['robust']['mean'])
            plots[metric]['robust_err'].append(values['robust']['err'])

    fig = make_subplots(rows=len(plots), cols=1, subplot_titles=sorted(plots.keys()))
    for metric in sorted(plots.keys()):
        data = plots[metric]
        fig.add_trace(
            go.Scatter(
                x=data['standard'],
                y=data['robust'],
                mode='markers',
                hovertemplate='<b>Standard:</b> %{x:.2f}<br><b>Robust:</b> %{y:.2f}',
                showlegend=False
            )
        )
    return fig

def layout(usecase_id=0, **kwargs):
    usecase = adapter.get_usecase(usecase_id)
    if usecase:
        with open(f'usecases/{usecase.full_description}', 'r') as f:
            description = dcc.Markdown(f.read(), mathjax=True)

        summaries = get_summaries(usecase.benchmarks)

        benchmark_list = benchmark_list = dbc.Table([
            html.Thead(html.Tr([
                html.Th('Dataset'),
                html.Th('Model'),
                html.Th('Threat model'),
                html.Th('Defense'),
                html.Th('Attack'),
                html.Th('Results')
            ]))] + [html.Tr([
                html.Td(b.dataset.title),
                html.Td(b.model.title),
                html.Td(b.threat_model),
                html.Td(b.defense.title),
                html.Td(b.attack.title),
                html.Td(print_results(b.results))
            ], className='benchmarks_row')
            for b in usecase.benchmarks
        ])

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{usecase.title}'))
            ),
            dbc.Row(
                dbc.Col(description)
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            dbc.Row(
                dbc.Col(benchmark_list)
            ),
            dbc.Row(
                dbc.Col(html.H2('Summaries'))
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='summaries', figure=summaries)
                )
            )
        ])
    else:
        return html.Div()
