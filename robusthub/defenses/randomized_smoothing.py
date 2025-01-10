"""
Randomized smoothing
=====================

Catalog of randomized smoothing defenses.
"""

import torch

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
    """
    def __init__(self, model: Model, n_samples: int, sigma: float):
        super().__init__()
        self.model = model
        self.n_samples = n_samples
        self.sigma = sigma
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y_outputs = []
        for _ in range(self.n_samples):
            eta = self.sigma * torch.randn_like(x)
            y_outputs.append(self.model(x + eta))
        y_preds = torch.stack([torch.argmax(y_output, dim=1) for y_output in y_outputs], dim=0)
        return torch.mode(y_preds, dim=0)[0]

class RandomizedSmoothing(Defense):
    """
    Basic randomized smoothing implementation based on :cite:`cohen2019certified`.

    Parameters
    -----------
    n_samples
        The number of samples to take.
    
    sigma
        Variance of the noise added to the samples.
    """

    def __init__(self, n_samples: int, sigma: float):
        super().__init__()

        self.n_samples = n_samples
        self.sigma = sigma

    def apply(self, model: Model) -> Model:
        return SmoothedModel(model, self.n_samples, self.sigma)


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
    """

    def __init__(self, denoiser: Model, n_samples: int, sigma: float):
        super().__init__(n_samples, sigma)

        self.denoiser = denoiser

    def apply(self, model: Model) -> Model:
        return SmoothedModel(CompositeModel([self.denoiser, model]), self.n_samples, self.sigma)
