import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

from typing import List

from adapter import Adapter

adapter = Adapter('sqlite:///../robusthub.db')

dash.register_page(__name__, path='/')

def create_catalog(models: List, slug: str):
    model_head = html.Thead(html.Tr([
        html.Th('Name'), html.Th('Identifier'), html.Th('Repository'), html.Th('Tags')
    ]))
    model_list = [
        html.Tr([
            html.Td(dcc.Link(model.title, href=f'/{slug}/{model.id}')),
            html.Td(model.name),
            html.Td(dcc.Link(model.repo, href=f'https://github.com/{model.repo}')),
            html.Td('none')
        ]) for model in models
    ]
    model_table = dbc.Table([model_head] + model_list, bordered=True)

    return model_table

model_title = html.H2('Model catalog')
models = adapter.load_models()
model_table = create_catalog(models, 'model')

defense_title = html.H2('Defense catalog')
defenses = adapter.load_defenses()
defense_table = create_catalog(defenses, 'defense')

attacks_title = html.H2('Attack catalog')
attacks = adapter.load_attacks()
attack_table = create_catalog(attacks, 'attack')

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(model_title)
        ),
        dbc.Row(
            dbc.Col(model_table)
        ),
        dbc.Row(
            dbc.Col(defense_title)
        ),
        dbc.Row(
            dbc.Col(defense_table)
        ),
        dbc.Row(
            dbc.Col(attacks_title)
        ),
        dbc.Row(
            dbc.Col(attack_table)
        )
    ]
)
