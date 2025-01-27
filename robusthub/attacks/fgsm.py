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
        samples = x_data.clone().detach().requires_grad_()

        y_pred = model(samples)
        loss = F.nll_loss(y_pred, y_data)
        _grad_check(loss)
        loss.backward()

        x_tilde = samples + self.eps * torch.sign(samples.grad)
        return self.threat.project(x_data, x_tilde)
