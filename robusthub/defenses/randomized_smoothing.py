"""
Randomized smoothing
=====================

Catalog of randomized smoothing defenses.
"""

import torch
import torch.nn.functional as F

from robusthub.models import Model, CompositeModel
from robusthub.defenses.defense import Defense

class SmoothedModel(Model):
    """
    Model smoothed using randomized smoothing.

    Parameters
    -----------
    model
        The model to smooth.
    
    n_samples
        The number of samples to take.
    
    sigma
        Variance of the noise added to the samples.
    
    n_classes
        Number of classes.
    """
    def __init__(self, model: Model, n_samples: int, sigma: float, n_classes: int):
        super().__init__()
        self.model = model
        self.n_samples = n_samples
        self.sigma = sigma
        self.n_classes = n_classes
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y_outputs = []
        for _ in range(self.n_samples):
            eta = self.sigma * torch.randn_like(x)
            y_outputs.append(self.model(x + eta))
        y_preds = torch.stack([torch.argmax(y_output, dim=1) for y_output in y_outputs], dim=0)
        return F.one_hot(torch.mode(y_preds, dim=0)[0], self.n_classes).float()

class RandomizedSmoothing(Defense):
    """
    Basic randomized smoothing implementation based on :cite:`cohen2019certified`.

    Parameters
    -----------
    n_samples
        The number of samples to take.
    
    sigma
        Variance of the noise added to the samples.
    
    n_classes
        Number of classes.
    """

    def __init__(self, n_samples: int, sigma: float, n_classes: int):
        super().__init__()

        self.n_samples = n_samples
        self.sigma = sigma
        self.n_classes = n_classes

    def apply(self, model: Model) -> Model:
        return SmoothedModel(model, self.n_samples, self.sigma, self.n_classes)


class DenoisedSmoothing(RandomizedSmoothing):
    """
    Basic denoised smoothing implementation proposed by :cite:`salman2020denoised`.

    Parameters
    -----------
    denoiser
        Denoising model.

    n_samples
        The number of samples to take.
    
    sigma
        Variance of the noise added to the samples.
    
    n_classes
        Number of classes.
    """

    def __init__(self, denoiser: Model, n_samples: int, sigma: float, n_classes: int):
        super().__init__(n_samples, sigma, n_classes)

        self.denoiser = denoiser

    def apply(self, model: Model) -> Model:
        return SmoothedModel(CompositeModel([self.denoiser, model]), self.n_samples, self.sigma, self.n_classes)
