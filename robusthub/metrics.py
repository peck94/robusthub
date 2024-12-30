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
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor | None) -> float:
        """
        Compute the metric value for a given model and batch of data samples.

        Parameters
        ----------
        model
            Model to evaluate.
        
        x_data
            Input data samples.
        
        y_data
            Input data targets (optional).
        
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

class Runtime(Metric):
    """
    *Runtime* is the average time per sample needed for model inference.
    """
    def __init__(self):
        super().__init__('Runtime')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA, ProfilerActivity.XPU]) as prof:
            with record_function('model_inference'):
                model(x_data)
        
        ev = prof.key_averages()[0]
        return ev.cpu_time_total + ev.device_time_total

class Memory(Metric):
    """
    *Memory* is the average amount of memory per sample needed for model inference.
    """
    def __init__(self):
        super().__init__('Memory')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        with profile(activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA, ProfilerActivity.XPU], profile_memory=True) as prof:
            model(x_data)
        
        ev = prof.key_averages()[0]
        return ev.cpu_memory_usage + ev.device_memory_usage
