import dash
from dash import html, dcc

import dash_bootstrap_components as dbc

from typing import List

from adapter import Adapter

from config import Config

c = Config()
adapter = Adapter(c.data['database'])

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

jumbotron = html.Div(
    dbc.Container(
        [
            html.H1("RobustHub", className="display-3"),
            html.P(
                "Robust machine learning for everyone.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Design, compare and deploy robust machine learning models."
            ),
            html.P(
                dbc.ButtonGroup([
                    dbc.Button("Documentation", color="primary", outline=True),
                    dbc.Button("Contribute", color="primary", outline=True),
                ]),
                className="lead"
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-body-secondary rounded-3",
)

usecase_title = html.H2('Usecases')
usecases = adapter.load_usecases()
usecase_table = html.Div([
    html.Div([
        html.Img(src=usecase.thumbnail, className='card-img-top', height=325),
        html.Div([
            html.Div([
                html.H5(usecase.title)
            ], className='card-title'),
            html.P([
                usecase.short_description
            ], className='card-text'),
            dcc.Link('Read more', href=f'/usecase/{usecase.id}', className='card-link')
        ], className='card-body')
    ], className='card')
    for usecase in usecases
], className='card-group')

model_title = html.H2('Model catalog')
models = adapter.load_models()
model_table = create_catalog(models, 'model')

defense_title = html.H2('Defense catalog')
defenses = adapter.load_defenses()
defense_table = create_catalog(defenses, 'defense')

attacks_title = html.H2('Attack catalog')
attacks = adapter.load_attacks()
attack_table = create_catalog(attacks, 'attack')

datasets_title = html.H2('Dataset catalog')
datasets = adapter.load_datasets()
datasets_table = dbc.Table([
    html.Thead(html.Tr([
        html.Th('Name'), html.Th('URL')
    ]))] + [
        html.Tr([
            html.Td(dcc.Link(dataset.title, href=f'/dataset/{dataset.id}')),
            html.Td(dcc.Link(dataset.url, href=dataset.url))
        ]) for dataset in datasets
    ], bordered=True)

layout = dbc.Container(
    [
        jumbotron,
        dbc.Row(
            dbc.Col(usecase_title)
        ),
        dbc.Row(
            dbc.Col(usecase_table)
        ),
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
        ),
        dbc.Row(
            dbc.Col(datasets_title)
        ),
        dbc.Row(
            dbc.Col(datasets_table)
        )
    ]
)
