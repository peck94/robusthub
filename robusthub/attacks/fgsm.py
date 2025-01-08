import torch
import torch.nn.functional as F

from robusthub.models import Model
from robusthub.attacks.attack import Attack
from robusthub.threats import ThreatModel

class FastGradientSignMethod(Attack):
    """
    The fast gradient sign attack proposed by :cite:`goodfellow2014explaining`.
    """
    def __init__(self, threat_model: ThreatModel):
        super().__init__(threat_model)
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        samples = x_data.clone().detach().requires_grad_()

        y_pred = model(samples)
        loss = F.nll_loss(y_pred, y_data)
        loss.backward()

        x_tilde = samples + torch.sign(samples.grad)
        return self.threat.project(x_data, x_tilde)
