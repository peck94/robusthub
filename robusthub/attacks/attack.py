"""
Catalog of adversarial attacks.

An *adversarial attack* takes a model and a batch of data samples and returns a new set of data samples called *adversarial examples*.
These adversarial examples are optimized so that the model achieves the worst possible score on one or more task-specific metrics,
subject to the constraints defined by a given threat model.
"""
import torch

from abc import ABC, abstractmethod

from robusthub.models import Model
from robusthub.threats import ThreatModel

class Attack(ABC):
    """
    Abstract base class for all adversarial attacks.

    Parameters
    -----------
    threat_model
        The threat model of the attack.
    """
    def __init__(self, threat_model: ThreatModel):
        self.threat = threat_model

    @abstractmethod
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor | None) -> torch.Tensor:
        """
        Apply the attack to a batch of samples.

        Parameters
        -----------
        model
            Model to attack.

        x_data
            Tensor of input data samples.
        
        y_data
            Tensor of targets (optional).
        
        Returns
        --------
        torch.Tensor
            Tensor of corrupted data samples.
        """
        pass
