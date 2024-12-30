"""
Benchmarks evaluate combinations of models and adversarial defenses according to *task-specific metrics*,
which are unique to the particular task the models need to solve, and *task-agnostic metrics*
which are always relevant. All benchmarks always measure the following task-agnostic metrics:

* Runtime of training.
* Runtime of inference.
* Memory consumption during training.
* Memory consumption during inference.

Task-specific metrics must be specified by the user and are detailed in our :doc:`Metrics <metrics>` page.
All task-specific metrics are computed on clean as well as adversarially corrupted data.
"""

from typing import List

from collections import namedtuple

import torch

import numpy as np

from torch.profiler import profile, ProfilerActivity

from robusthub import models
from robusthub import defenses
from robusthub import attacks
from robusthub import metrics

Value = namedtuple('Value', ['mean', 'std'])

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
        activities = [ProfilerActivity.CPU, ProfilerActivity.CUDA, ProfilerActivity.XPU]
        result = {}

        # Profile defense
        with profile(activities=activities, profile_memory=True) as prof:
            robust_model = defense.apply(model)

        # Profile model inference
        with profile(activities=activities, profile_memory=True) as prof:
            for x_data, _ in data_loader:
                robust_model(x_data.to(self.device))

        # Measure task-specific metrics
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
            result[metric.name] = {
                'standard': Value(mean=np.mean(standard_values), std=np.std(standard_values)),
                'robust': Value(mean=np.mean(robust_values), std=np.std(robust_values))
            }

        return result
