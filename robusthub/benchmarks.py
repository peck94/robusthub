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

from typing import List, NamedTuple, Union

from enum import Flag, auto

import torch

import numpy as np

from robusthub import models
from robusthub import defenses
from robusthub import attacks
from robusthub import metrics
from robusthub.profiler import Profiler


class Value(NamedTuple):
    """
    Represents the average value of a metric over a data set.
    """

    #: Mean of the metric values over the data set.
    mean: float

    #: Standard error of the mean of values over the data set.
    err: float

    def __repr__(self):
        """
        String representation of this value.
        """
        return f"{{'mean': '{self.mean}', 'err': {self.err}}}"

class ResultFlags(Flag):
    """
    Flags that identify a specific type of measurement result.
    """

    #: A task-agnostic metric.
    AGNOSTIC = auto()

    #: A task-specific metric.
    SPECIFIC = auto()

    #: This value applies to the model.
    MODEL = auto()

    #: This value applies to the defense.
    DEFENSE = auto()

    #: This value was measured in the standard (non-adversarial) setting.
    STANDARD = auto()

    #: This value was measured in the adversarial setting.
    ROBUST = auto()

class Result:
    """
    Represents the results of a benchmark.
    """
    def __init__(self):
        self.record = []

    def store(self, metric: Union[metrics.Metric, str], t: ResultFlags, value: Value):
        """
        Store a result.

        Parameters
        -----------
        metric
            The metric that was measured.
        
        t
            Flags describing the type of measurement.
        
        value
            The measured value.
        
        bounds
            Lower and upper bounds of the metric, if any.
        """
        if isinstance(metric, metrics.Metric):
            record = {
                'metric': metric.name,
                'flags': t,
                'value': value
            }
        else:
            record = {
                'metric': metric,
                'flags': t,
                'value': value
            }
        self.record.append(record)
    
    def __repr__(self):
        return f'[{", ".join(self.record)}]'

class Benchmark:
    """
    Base class for all benchmarks.

    Parameters
    -----------
    attack
        Adversarial attack used for robustness assessment.
    
    metrics_list
        List of task-specific metrics.
    
    device
        Torch device.
    """
    def __init__(self, attack: attacks.Attack, metrics_list: List[metrics.Metric], device: torch.device = torch.device('cuda')):
        self.attack = attack
        self.metrics = metrics_list
        self.device = device

    def run(self, model: models.Model, defense: defenses.Defense, data_loader: torch.utils.data.DataLoader) -> Result:
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
        Result
            An object describing the benchmark results.
        """
        result = Result()
        model = model.to(self.device)
        profiler = Profiler(self.device)

        # Profile defense
        print('[*] Profiling defense')
        with profiler:
            robust_model = defense.apply(model)
        result.store('Memory',
                     ResultFlags.AGNOSTIC | ResultFlags.DEFENSE,
                     Value(mean=profiler.memory, err=0))
        result.store('Runtime',
                     ResultFlags.AGNOSTIC | ResultFlags.DEFENSE,
                     Value(mean=profiler.runtime, err=0))

        # Profile standard model inference
        print('[*] Profiling standard model')
        with profiler:
            for x_data, _ in data_loader:
                model(x_data.to(self.device))
        result.store('Memory',
                     ResultFlags.AGNOSTIC | ResultFlags.MODEL | ResultFlags.STANDARD,
                     Value(mean=profiler.memory, err=0))
        result.store('Runtime',
                     ResultFlags.AGNOSTIC | ResultFlags.MODEL | ResultFlags.STANDARD,
                     Value(mean=profiler.runtime, err=0))

        # Profile robust model inference
        print('[*] Profiling robust model')
        with profiler:
            for x_data, _ in data_loader:
                robust_model(x_data.to(self.device))
        result.store('Memory',
                     ResultFlags.AGNOSTIC | ResultFlags.MODEL | ResultFlags.ROBUST,
                     Value(mean=profiler.memory, err=0))
        result.store('Runtime',
                     ResultFlags.AGNOSTIC | ResultFlags.MODEL | ResultFlags.ROBUST,
                     Value(mean=profiler.runtime, err=0))

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
            result.store(metric,
                         ResultFlags.SPECIFIC | ResultFlags.STANDARD,
                         Value(mean=np.mean(standard_values), err=1.96*np.std(standard_values)/np.sqrt(len(standard_values))))
            result.store(metric,
                         ResultFlags.SPECIFIC | ResultFlags.ROBUST,
                         Value(mean=np.mean(robust_values), err=1.96*np.std(robust_values)/np.sqrt(len(robust_values))))

        return result
