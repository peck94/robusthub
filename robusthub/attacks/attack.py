"""
Catalog of adversarial attacks.
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
    model
        The model to attack.
    
    threat_model
        The threat model of the attack.
    """
    def __init__(self, model: Model, threat_model: ThreatModel):
        self.model = model
        self.threat = threat_model

    @abstractmethod
    def apply(self, x_data: torch.Tensor, y_data: torch.Tensor | None) -> torch.Tensor:
        """
        Apply the attack to a batch of samples.

        Parameters
        -----------
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
