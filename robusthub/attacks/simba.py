import torch

import numpy as np

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.attacks.attack import Attack

class Simba(Attack):
    """
    The simple black-box attack proposed by :cite:`guo2019simple`.

    Parameters
    -----------
    threat_model
        The threat model to use.
    
    iterations
        Maximum number of iterations.
    
    eps
        Budget of the attack.
    
    basis
        Basis to use. Options are :code:`standard` for the standard Cartesian basis or :code:`dct` for the DCT basis.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 iterations: int = 1000,
                 eps: float = 1,
                 basis: str = 'standard'):
        super().__init__(threat_model)

        self.iterations = iterations
        self.eps = eps
        self.basis = basis
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        deltas = torch.zeros_like(x_data)
        bs = x_data.shape[0]
        for _ in range(self.iterations):
            qs = 2 * self.eps * torch.rand_like(deltas) - self.eps
            if self.basis == 'dct':
                qs = torch.fft.ifft2(qs).real
            
            x_old = self.threat.project(x_data, x_data + deltas)
            x_tilde = self.threat.project(x_data, x_data + deltas + qs)

            y_pred_old = model(x_old)
            y_pred_new = model(x_tilde)
            for i in range(bs):
                if y_pred_old[i, y_data[i]] > y_pred_new[i, y_data[i]]:
                    deltas[i, ...] = deltas[i, ...] + qs[i, ...]

        return self.threat.project(x_data, x_data + deltas)
