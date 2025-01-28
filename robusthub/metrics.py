"""
Catalog of task-specific metrics.

A metric is a real-valued summary statistic computed from a model and a batch of data.

We refer to these metrics as *task-specific* because their relevance depends on the particular task that the target model needs to solve.
For instance, :py:class:`robusthub.metrics.Accuracy` is only applicable to classification tasks,
whereas :py:class:`robusthub.metrics.MSE` is only applicable to regression problems.

Metrics that are not task-specific are called *task-agnostic*. These include, for example, inference speed and memory consumption.
Task-agnostic metrics are built into all benchmarks. Consult our :doc:`Benchmarks <benchmarks>` page for more information.
"""

import torch

import numpy as np

from abc import ABC, abstractmethod

from robusthub.models import Model

from skimage.metrics import structural_similarity, peak_signal_noise_ratio

from sklearn.metrics import f1_score, roc_auc_score, roc_curve

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
    The proportion of model predictions that match the given ground truth.
    """
    def __init__(self):
        super().__init__('Accuracy')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        return torch.mean((y_pred.argmax(dim=1) == y_data).float()).item()

class MSE(Metric):
    """
    The mean squared error between the model predictions and the ground truth.
    """
    def __init__(self):
        super().__init__('MSE')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        return torch.mean(torch.square(y_pred - y_data)).item()

class NMSE(Metric):
    """
    The normalized mean squared error between the model predictions and the ground truth.
    """
    def __init__(self):
        super().__init__('NMSE')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        mse = torch.mean(torch.square(y_pred - y_data))
        return mse / torch.mean(torch.square(y_data))

class MAE(Metric):
    """
    The mean absolute error between the model predictions and the ground truth.
    """
    def __init__(self):
        super().__init__('MAE')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        return torch.mean(torch.square(y_pred - y_data)).item()

class SSIM(Metric):
    """
    The structural similarity index measure.
    """
    def __init__(self):
        super().__init__('SSIM')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        r = x_data.max() - x_data.min()

        im1 = y_data.cpu().detach().numpy()
        im2 = y_pred.cpu().detach().numpy()
        return structural_similarity(im1, im2, data_range=r.item(), win_size=3)

class PSNR(Metric):
    """
    The peak signal-to-noise ratio.
    """
    def __init__(self):
        super().__init__('PSNR')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        r = x_data.max() - x_data.min()
        return peak_signal_noise_ratio(y_data.cpu().detach().numpy(),
                                       y_pred.cpu().detach().numpy(),
                                       data_range=r.item())

class F1(Metric):
    """
    The F1 score.
    """
    def __init__(self):
        super().__init__('F1')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        labels = y_pred.argmax(dim=1).cpu().detach().numpy()
        return f1_score(y_data.cpu().detach().numpy(), labels)

class AUC(Metric):
    """
    The AUC score.
    """
    def __init__(self):
        super().__init__('F1')
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        return roc_auc_score(y_data.cpu().detach().numpy(), y_pred.cpu().detach().numpy())

class TPR(Metric):
    """
    The true positive rate at a given false positive rate threshold.

    Parameters
    -----------
    fpr
        The maximum false positive rate.
    """
    def __init__(self, fpr=.1):
        super().__init__(f'TPR@FPR={fpr:.2%}')
        self.fpr = fpr

        assert 0 <= fpr <= 1, 'FPR must be between 0 and 1'
    
    def compute(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> float:
        y_pred = model(x_data)
        fpr, tpr, _ = roc_curve(y_data.cpu().detach().numpy(), y_pred.cpu().detach().numpy())

        idx = max(0, np.searchsorted(fpr, self.fpr, side='right') - 1)
        return tpr[idx]
