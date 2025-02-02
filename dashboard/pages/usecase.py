import dash
from dash import html, dcc, dash_table

import dash_bootstrap_components as dbc

import numpy as np

import plotly.graph_objects as go
import plotly.express as px
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

def get_scatterplots(benchmarks: List[Benchmark]) -> Figure:
    if benchmarks:
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
                        'bounds': values['bounds'],
                        'models': [],
                        'defenses': [],
                        'datasets': []
                    }

                plots[metric]['standard'].append(float(values['standard']['mean']))
                plots[metric]['standard_err'].append(float(values['standard']['err']))
                plots[metric]['robust'].append(float(values['robust']['mean']))
                plots[metric]['robust_err'].append(float(values['robust']['err']))
                plots[metric]['models'].append(b.model.title)
                plots[metric]['defenses'].append(b.defense.title)
                plots[metric]['datasets'].append(b.dataset)

        fig = make_subplots(rows=len(plots), cols=1, subplot_titles=sorted(plots.keys()))
        for i, metric in enumerate(sorted(plots.keys())):
            data = plots[metric]
            fig.add_trace(
                go.Scatter(
                    x=data['standard'],
                    y=data['robust'],
                    customdata=np.stack((data['models'], data['defenses'], [d.title for d in data['datasets']]), axis=-1),
                    error_x=dict(
                        type='data',
                        array=data['standard_err'],
                        visible=True
                    ),
                    error_y=dict(
                        type='data',
                        array=data['robust_err'],
                        visible=True
                    ),
                    mode='markers',
                    marker_color=[px.colors.qualitative.Plotly[d.id] for d in data['datasets']],
                    hovertemplate='<b>%{customdata[2]}</b><br><b>Standard:</b> %{x:.2f}<br><b>Robust:</b> %{y:.2f}<br><b>Model:</b> %{customdata[0]}<br><b>Defense:</b> %{customdata[1]}',
                    showlegend=False,
                    name=metric
                )
            )

            lower, upper = data['bounds']
            if np.isfinite(lower) and np.isfinite(upper):
                zs = np.linspace(lower, upper)
                fig.add_trace(
                    go.Scatter(
                        x=zs,
                        y=zs,
                        line=dict(
                            dash='dot',
                            color='gray',
                            width=1
                        ),
                        showlegend=False
                    )
                )
            fig.update_xaxes(range=data['bounds'], title='Standard', row=i+1, col=1)
            fig.update_yaxes(range=data['bounds'], title='Robust', row=i+1, col=1)
        return fig
    else:
        return None

def layout(usecase_id=0, **kwargs):
    usecase = adapter.get_usecase(usecase_id)
    if usecase:
        with open(f'usecases/{usecase.full_description}', 'r') as f:
            description = dcc.Markdown(f.read(), mathjax=True)

        scatterplots = get_scatterplots(usecase.benchmarks)

        records = [
            {
                'Data set': benchmark.dataset.title,
                'Model': benchmark.model.title,
                'Threat model': benchmark.threat_model,
                'Defense': benchmark.defense.title,
                'Attack': benchmark.attack.title,
                **print_results(benchmark.results)
            }
            for benchmark in usecase.benchmarks
        ]
        benchmark_table = dash_table.DataTable(
            records,
            #filter_action="native",
            sort_action="native",
            sort_mode='multi',
            selected_rows=[],
            page_action='native',
            page_size=20,
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto'
            }
        )

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{usecase.title}'))
            ),
            dbc.Row([
                dbc.Col(
                    html.Img(src=usecase.thumbnail, width='100%'),
                    width=3
                ),
                dbc.Col(description)
            ]),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            ),
            dbc.Row(
                dbc.Col(
                    dcc.Graph(id='scatterplots', figure=scatterplots)
                )
            ),
            dbc.Row(
                dbc.Col(benchmark_table)
            ),
        ])
    else:
        return html.Div()
