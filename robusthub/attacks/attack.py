"""
Attacks
========

Catalog of adversarial attacks.
"""

from abc import ABC, abstractmethod

from robusthub.base import Array
from robusthub.models import Model

class Attack(ABC):
    """
    Abstract base class for all adversarial attacks.
    """
    def __init__(self, model: Model):
        """
        Initialize the attack.

        Parameters
        -----------
        model
            The model to attack.
        """
        self.model = model

    @abstractmethod
    def apply(self, x_data: Array, y_data: Array | None) -> Array:
        """
        Apply the attack to a batch of samples.

        Parameters
        -----------
        x_data
            Array of input data samples.
        
        y_data
            Array of targets (optional).
        
        Returns
        --------
        Array
            Array of corrupted data samples.
        """
        pass
