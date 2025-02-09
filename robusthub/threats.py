"""
Catalog of threat models.

A *threat model* defines the feasible set of the adversarial attack.
Threat models can be composed, in which case the feasible set is the intersection of all threat models. See :py:class:`robusthub.threats.Composite`.
"""
import torch

import numpy as np

import warnings

from abc import ABC, abstractmethod

from typing import List

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

    def __repr__(self) -> str:
        """
        String represenation of this threat model.
        """
        return "ThreatModel"

class Composite(ThreatModel):
    """
    Sequentially compose multiple threat models.
    """
    def __init__(self, threat_models: List[ThreatModel]):
        super().__init__()
        self.threats = threat_models
    
    def project(self, x_orig: torch.Tensor, x_tilde: torch.Tensor) -> torch.Tensor:
        """
        Apply all given threat models.
        """
        x_proj = x_tilde
        for threat in self.threats:
            x_proj = threat.project(x_orig, x_proj)
        return x_proj
    
    def __repr__(self) -> str:
        return "; ".join([str(t) for t in self.threats])

class Bounds(ThreatModel):
    """
    Simple bounds on the numerical values of the data vectors.

    Parameters
    ----------
    lower_bound
        Lower bound on the values. Specify :code:`None` for no lower bound.
    
    upper_bound
        Upper bound on the values. Specify :code:`None` for no upper bound.
    """
    def __init__(self, lower_bound: float | None, upper_bound: float | None):
        super().__init__()
        self.lower = lower_bound
        self.upper = upper_bound
    
    def project(self, x_orig: torch.Tensor, x_tilde: torch.Tensor) -> torch.Tensor:
        """
        Clip the values of the data to the specified range.
        """
        if x_orig.min() < self.lower or x_orig.max() > self.upper:
            warnings.warn(f'Threat model bounds ({self.lower}, {self.upper}) do not agree with data bounds ({x_orig.min()}, {x_orig.max()})')
        return torch.clamp(x_tilde, self.lower, self.upper)
    
    def __repr__(self) -> str:
        return f"Bounds({self.lower}, {self.upper})"

class Lp(ThreatModel):
    """
    :math:`L_p` threat model.

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
    
    def __repr__(self) -> str:
        if np.isfinite(self.p):
            return f"L{self.p}({self.epsilon:.2f})"
        else:
            return f"Linf({self.epsilon:.2f})"

class Linf(Lp):
    """
    :math:`L_\infty` threat model.
    """
    def __init__(self, epsilon: float):
        super().__init__(np.inf, epsilon)

class L2(Lp):
    """
    :math:`L_2` threat model.
    """
    def __init__(self, epsilon: float):
        super().__init__(2, epsilon)
