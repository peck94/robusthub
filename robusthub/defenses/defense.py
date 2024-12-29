"""
Catalog of adversarial defenses.
"""

import robusthub
from robusthub.models import Model

from abc import ABC, abstractmethod

class Defense(ABC):
    """
    Abstract base class for all adversarial defenses.
    """

    def __init__(self):
        """
        Initialize the defense.
        """
        pass

    @abstractmethod
    def apply(self, model: Model) -> Model:
        """
        Apply the defense to a given model.

        Parameters
        -----------
        model
            The model to which the defense will be applied.
        
        Returns
        --------
        Model
            The supplied model with the defense applied.
        """
        pass
