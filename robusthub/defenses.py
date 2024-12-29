"""
defenses
=========

Catalog of adversarial defenses.
"""

import robusthub

class Defense:
    """
    Abstract base class for all adversarial defenses.
    """

    def __init__(self):
        """
        Initialize the defense.
        """
        pass

    def apply(self, model: robusthub.models.Model) -> robusthub.models.Model:
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
