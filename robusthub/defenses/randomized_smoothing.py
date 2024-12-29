"""
Randomized smoothing
=====================

Catalog of randomized smoothing defenses.
"""

from robusthub.models import Model
from robusthub.defenses.defense import Defense

class RandomizedSmoothing(Defense):
    """
    Basic randomized smoothing implementation based on :cite:`cohen2019certified`.
    """

    def __init__(self):
        pass

    def apply(self, model: Model) -> Model:
        return model


class DenoisedSmoothing(RandomizedSmoothing):
    """
    Basic denoised smoothing implementation proposed by :cite:`salman2020denoised`.
    """

    def __init__(self):
        pass

    def apply(self, model: Model) -> Model:
        return model
