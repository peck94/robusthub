import ast

import humanize

from models import Benchmark

def to_ratio(baseline: float, value: float) -> float:
    return (value - baseline) / baseline

def interpret_results(benchmark: Benchmark) -> dict:
    return ast.literal_eval(benchmark.results)

def print_results(results_str: str) -> dict:
    results = ast.literal_eval(results_str)
    
    baseline_mem = results['model']['standard']['memory']
    defense_mem = results['defense']['memory']
    robust_mem = results['model']['robust']['memory']

    baseline_time = results['model']['standard']['runtime']
    defense_time = to_ratio(baseline_time, results['defense']['runtime'])
    robust_time = to_ratio(baseline_time, results['model']['robust']['runtime'])

    records = {
        'Memory': f'{humanize.naturalsize(baseline_mem)} / {humanize.naturalsize(defense_mem)} / {humanize.naturalsize(robust_mem)}',
        'Runtime': f'{defense_time:.2f} / {robust_time:.2f}'
    }
    for metric in results['metrics']:
        records[metric] = f"{float(results['metrics'][metric]['standard']['mean']):.2f} / {float(results['metrics'][metric]['robust']['mean']):.2f}"
    return records
