import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

from adapter import Adapter

from utils import print_results

from config import Config

c = Config()

adapter = Adapter(c.data['database'])

dash.register_page(__name__, path_template="/usecase/<usecase_id>")

def layout(usecase_id=0, **kwargs):
    usecase = adapter.get_usecase(usecase_id)
    if usecase:
        with open(f'usecases/{usecase.full_description}', 'r') as f:
            description = dcc.Markdown(f.read(), mathjax=True)

        return html.Div([
            dbc.Row(
                dbc.Col(html.H1(f'{usecase.title}'))
            ),
            dbc.Row(
                dbc.Col(description)
            ),
            dbc.Row(
                dbc.Col(html.H2('Benchmarks'))
            )
        ])
    else:
        return html.Div()
