import torch
import torch.nn.functional as F

from robusthub.models import Model
from robusthub.attacks.attack import Attack, _grad_check
from robusthub.threats import ThreatModel

class FastGradientSignMethod(Attack):
    """
    The fast gradient sign attack proposed by :cite:`goodfellow2014explaining`.

    Parameters
    -----------
    threat_model
        The threat model to use.
    
    eps
        Multiplier for the gradient sign vector.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 eps: float = 1):
        super().__init__(threat_model)
        self.eps = eps
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        x_adv = x_data.clone().detach()
        x_adv.requires_grad = True

        y_pred = model(x_adv)
        loss = F.nll_loss(y_pred, y_data)
        _grad_check(loss)
        loss.backward()

        with torch.no_grad():
            deltas = self.eps * torch.sign(x_adv.grad)
            x_adv = x_adv + deltas
            x_adv = self.threat.project(x_data, x_adv)

        x_adv.grad = None
        loss.grad = None
        model.zero_grad()

        return x_adv.detach()
