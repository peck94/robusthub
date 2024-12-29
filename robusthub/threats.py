"""
Catalog of threat models.
"""
import torch

import numpy as np

from abc import ABC, abstractmethod

class ThreatModel(ABC):
    """
    Abstract base class for threat models.
    """
    def __init__(self):
        pass

    @abstractmethod
    def project(self, x_orig: torch.Tensor, x_tilde: torch.Tensor) -> torch.Tensor:
        """
        Project perturbed samples onto the feasible set of this threat model.

        Parameters
        -----------
        x_orig
            Original samples.
        
        x_tilde
            Perturbed samples.
        
        Returns
        --------
        torch.Tensor
            Perturbed samples projected back onto the feasible set.
        """
        pass

class Lp(ThreatModel):
    """
    Lp threat model.

    Parameters
    -----------
    p
        Norm of this threat model.

    epsilon
        The maximum magnitude of the perturbations.
    """
    def __init__(self, p: float, epsilon: float):
        super().__init__()
        self.epsilon = epsilon
        self.p = p
    
    def project(self, x_orig: torch.Tensor, x_tilde: torch.Tensor) -> torch.Tensor:
        """
        Project the perturbed samples onto the given Lp norm ball.
        """
        deltas = (x_tilde - x_orig).view(x_orig.shape[0], -1)
        norms = torch.linalg.vector_norm(deltas, self.p, dim=1, keepdim=True)

        x_proj = x_orig + torch.where(norms > self.epsilon, self.epsilon * deltas / norms, deltas).view(x_orig.shape)
        return x_proj

class Linf(Lp):
    """
    Linf threat model.
    """
    def __init__(self, epsilon: float):
        super().__init__(np.inf, epsilon)

class L2(Lp):
    """
    L2 threat model.
    """
    def __init__(self, epsilon: float):
        super().__init__(2, epsilon)
