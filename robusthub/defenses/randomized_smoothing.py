"""
Randomized smoothing
=====================

Catalog of randomized smoothing defenses.
"""

from robusthub.models import Model
from robusthub.defenses.defense import Defense

class RandomizedSmoothing(Defense):
    """
    Basic randomized smoothing implementation.
    """

    def __init__(self):
        pass

    def apply(self, model: Model) -> Model:
        return model


class DenoisedSmoothing(RandomizedSmoothing):
    """
    Basic denoised smoothing implementation.
    """

    def __init__(self):
        pass

    def apply(self, model: Model) -> Model:
        return model
