import torch

from robusthub.models import Model
from robusthub.attacks.attack import Attack
from robusthub.threats import ThreatModel

class Dummy(Attack):
    """
    The dummy attack does nothing and simply returns the unmodified input data.

    Parameters
    -----------
    threat_model
        The threat model to use.
    """
    def __init__(self, threat_model: ThreatModel):
        super().__init__(threat_model)
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        return x_data
