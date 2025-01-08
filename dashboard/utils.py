import ast

import humanize

import numpy as np

from dash import html

def to_ratio(a: float, b: float) -> float:
    return np.log(b / a) / np.log(10)

def print_results(results_str: str):
    results = ast.literal_eval(results_str)
    return html.Table([
        html.Tr([
            html.Th('Metric'),
            html.Th('Baseline'),
            html.Th('Defense'),
            html.Th('Robust')
        ]),
        html.Tr([
            html.Td('Runtime'),
            html.Td(results['model']['standard']['runtime']),
            html.Td(results['defense']['runtime']),
            html.Td(results['model']['robust']['runtime'])
        ]),
        html.Tr([
            html.Td('Memory'),
            html.Td(results['model']['standard']['memory']),
            html.Td(results['defense']['memory']),
            html.Td(results['model']['robust']['memory'])
        ]),
        html.Tr([
            html.Th('Metric'),
            html.Th('Standard'),
            html.Th('Robust')
        ])
    ] + [
        html.Tr([
            html.Td(metric),
            html.Td(f'{float(results['metrics'][metric]['standard']['mean']):.2f}'),
            html.Td(f'{float(results['metrics'][metric]['robust']['mean']):.2f}')
        ])
        for metric in results['metrics']
    ])
