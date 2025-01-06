import dash
from dash import html

import pandas as pd

from dash import html, dash_table

import dash_bootstrap_components as dbc

from adapter import Adapter

adapter = Adapter('sqlite:///../robusthub.db')

dash.register_page(__name__, path='/')

def create_catalog(data_dict: dict):
    data_df = pd.DataFrame(data_dict)
    data_catalog = dash_table.DataTable(
        data=data_df.to_dict('records'),
        columns=[{'name': i, 'id': i} for i in data_df.columns],
        style_cell={'textAlign': 'left'},
        style_header={
            'fontWeight': 'bold'
        },
        style_as_list_view=True
    )

    return data_catalog

model_title = html.H2('Model catalog')
models = adapter.load_models()
print(models)
models_dict = {
    'Name': [model.name for model in models],
    'Repository': [model.repo for model in models],
    'Tags': ['none' for model in models]
}
model_catalog = create_catalog(models_dict)

defense_title = html.H2('Defense catalog')
defenses = adapter.load_defenses()
defenses_dict = {
    'Name': [defense.name for defense in defenses],
    'Repository': [defense.repo for defense in defenses],
    'Tags': ['none' for defense in defenses]
}
defense_catalog = create_catalog(defenses_dict)

attacks_title = html.H2('Attack catalog')
attacks = adapter.load_defenses()
attacks_dict = {
    'Name': [attack.name for attack in attacks],
    'Repository': [attack.repo for attack in attacks],
    'Tags': ['none' for attack in attacks]
}
attacks_catalog = create_catalog(attacks_dict)

layout = html.Div(
    [
        dbc.Row(
            dbc.Col(model_title)
        ),
        dbc.Row(
            dbc.Col(model_catalog)
        ),
        dbc.Row(
            dbc.Col(defense_title)
        ),
        dbc.Row(
            dbc.Col(defense_catalog)
        ),
        dbc.Row(
            dbc.Col(attacks_title)
        ),
        dbc.Row(
            dbc.Col(attacks_catalog)
        )
    ]
)
