import ast

import humanize

import numpy as np

from dash import html

def to_ratio(a: float, b: float) -> float:
    return np.log(b / a) / np.log(10)

def print_results(results_str: str):
    results = ast.literal_eval(results_str)
    return html.Div([
        html.P(f"Runtime: {to_ratio(float(results['model']['standard']['runtime']), float(results['model']['robust']['runtime'])):.2f}"),
        html.P(f"Memory : {humanize.naturalsize(results['model']['standard']['memory'])} / {humanize.naturalsize(results['model']['robust']['memory'])}"),
        html.Hr()
    ] + [
        html.P(f"{metric}: {float(results['metrics'][metric]['standard']['mean']):.2f} ({float(results['metrics'][metric]['standard']['std']):.2f}) / {float(results['metrics'][metric]['robust']['mean']):.2f} ({float(results['metrics'][metric]['robust']['std']):.2f})")
        for metric in results['metrics']
    ])
