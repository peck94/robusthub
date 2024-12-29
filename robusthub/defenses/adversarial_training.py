"""
Adversarial training
=====================

Catalog of adversarial training defenses.
"""

from robusthub.models import Model
from robusthub.defenses import Defense

class AdversarialTraining(Defense):
    """
    Basic adversarial training defense.
    """

    def __init__(self):
        pass

    def apply(self, model: Model) -> Model:
        return model
