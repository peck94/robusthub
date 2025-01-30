import torch
import torch.nn.functional as F

import gc

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.attacks.attack import Attack, _grad_check

class ProjectedGradientDescent(Attack):
    """
    The projected gradient descent attack popularized by :cite:`madry2017attack`.

    Parameters
    -----------
    threat_model
        The threat model to use.
    
    iterations
        Number of iterations of optimization.
    
    alpha
        Per-iteration step size.
    
    device
        Device to use.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 iterations: int = 100,
                 alpha: float = .01,
                 device: torch.device = torch.device('cuda')):
        super().__init__(threat_model)

        self.iterations = iterations
        self.alpha = alpha
        self.device = device
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        x_adv = x_data.clone().detach()
        x_adv.requires_grad = True

        x_best = torch.zeros_like(x_data)
        best_loss = -torch.inf
        for _ in range(self.iterations):
            y_pred = model(x_adv)
            loss = F.nll_loss(y_pred, y_data)
            loss.backward()

            with torch.no_grad():
                deltas = self.alpha * torch.sign(x_adv.grad)
                x_adv = x_adv + deltas
                x_adv = self.threat.project(x_data, x_adv)

                y_pred = model(x_adv)
                loss = F.nll_loss(y_pred, y_data).item()
                if loss > best_loss:
                    best_loss = loss
                    x_best = x_adv.detach().clone()
            x_adv.requires_grad = True

        return x_best
