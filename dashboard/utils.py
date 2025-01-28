import ast

import humanize

import numpy as np

from dash import html

from models import Benchmark

def to_ratio(a: float, b: float) -> float:
    return np.log(b / a) / np.log(10)

def interpret_results(benchmark: Benchmark) -> dict:
    return ast.literal_eval(benchmark.results)

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
            html.Td(f"{results['model']['standard']['runtime']:.2f}"),
            html.Td(f"{results['defense']['runtime']:.2f}"),
            html.Td(f"{results['model']['robust']['runtime']:.2f}")
        ]),
        html.Tr([
            html.Td('Memory'),
            html.Td(humanize.naturalsize(results['model']['standard']['memory'])),
            html.Td(humanize.naturalsize(results['defense']['memory'])),
            html.Td(humanize.naturalsize(results['model']['robust']['memory']))
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
