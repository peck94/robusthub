"""
Catalog of metrics.

A metric is a real-valued summary statistic computed from a model and a batch of data.
"""

import torch

from torch.profiler import profile, record_function, ProfilerActivity

from abc import ABC, abstractmethod

from robusthub.models import Model

class Metric(ABC):
    """
    Abstract base class for all metrics.

    Parameters
    -----------
    name
        Name of the metric.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        """
        Compute the metric value.

        Returns
        --------
        float
            Metric value.
        """
        pass

class Accuracy(Metric):
    """
    *Accuracy* is the proportion of model predictions that match the given ground truth.
    """
    def __init__(self):
        super().__init__('Accuracy')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        return torch.mean((y_pred.argmax(dim=1) == y_data).float()).item()
