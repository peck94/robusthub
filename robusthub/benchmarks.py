"""
Benchmarks evaluate combinations of models and adversarial defenses according to *task-specific metrics*,
which are unique to the particular task the models need to solve, and *task-agnostic metrics*
which are always relevant. All benchmarks always measure the following task-agnostic metrics:

* Runtime of applying the defense.
* Runtime of inference.
* Memory consumption during application of the defense.
* Memory consumption during inference.

Task-specific metrics must be specified by the user and are detailed in our :doc:`Metrics <metrics>` page.
All task-specific metrics are computed on clean as well as adversarially corrupted data.
"""

from typing import List, NamedTuple

import torch

import pyinstrument

import numpy as np

from robusthub import models
from robusthub import defenses
from robusthub import attacks
from robusthub import metrics


class Value(NamedTuple):
    """
    Represents the average value of a metric over a data set.
    """

    #: Mean of the metric values over the data set.
    mean: float

    #: Standard deviation of the values over the data set.
    std: float

    def __repr__(self):
        """
        String representation of this value.
        """
        return f"{{'mean': '{self.mean}', 'std': {self.std}}}"

class Benchmark:
    """
    Base class for all benchmarks.

    Parameters
    -----------
    attack
        Adversarial attack used for robustness assessment.
    
    metrics
        List of task-specific metrics.
    
    device
        Torch device.
    """
    def __init__(self, attack: attacks.Attack, metrics: List[metrics.Metric], device: torch.device):
        self.attack = attack
        self.metrics = metrics
        self.device = device

    def run(self, model: models.Model, defense: defenses.Defense, data_loader: torch.utils.data.DataLoader) -> dict:
        """
        Run the benchmark.

        Parameters
        -----------
        model
            Baseline model to use.
        
        defense
            Adversarial defense to apply.
        
        data_loader
            Data set to use for evaluation.
        
        Returns
        --------
        dict
            A dictionary of benchmark results.
        """
        result = {
            'model': {},
            'defense': {},
            'metrics': {}
        }
        model = model.to(self.device)
        profiler = pyinstrument.Profiler()

        # Profile defense
        print('[*] Profiling defense')
        torch.cuda.reset_peak_memory_stats(self.device)
        with profiler:
            robust_model = defense.apply(model)
        result['defense'] = {
            'memory': torch.cuda.max_memory_allocated(self.device),
            'runtime': profiler.last_session.cpu_time
        }
        profiler.reset()

        # Profile model inference
        print('[*] Profiling standard model')
        torch.cuda.reset_peak_memory_stats(self.device)
        with profiler:
            for x_data, _ in data_loader:
                model(x_data.to(self.device))
        result['model']['standard'] = {
            'memory': torch.cuda.max_memory_allocated(self.device),
            'runtime': profiler.last_session.cpu_time
        }
        profiler.reset()

        print('[*] Profiling robust model')
        torch.cuda.reset_peak_memory_stats(self.device)
        with profiler:
            for x_data, _ in data_loader:
                robust_model(x_data.to(self.device))
        result['model']['robust'] = {
            'memory': torch.cuda.max_memory_allocated(self.device),
            'runtime': profiler.last_session.cpu_time
        }

        # Measure task-specific metrics
        print('[*] Calculating task-specific metrics')
        for metric in self.metrics:
            standard_values = []
            robust_values = []
            for x_data, y_data in data_loader:
                x_data, y_data = x_data.to(self.device), y_data.to(self.device)
                x_tilde = self.attack.apply(robust_model, x_data, y_data)

                standard_value = metric.compute(robust_model, x_data, y_data)
                robust_value = metric.compute(robust_model, x_tilde, y_data)

                standard_values.append(standard_value)
                robust_values.append(robust_value)
            result['metrics'][metric.name] = {
                'standard': Value(mean=np.mean(standard_values), std=np.std(standard_values)),
                'robust': Value(mean=np.mean(robust_values), std=np.std(robust_values))
            }

        return result
