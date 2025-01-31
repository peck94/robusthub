import torch
import torch.nn.functional as F

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
    
    restarts
        The number of random restarts.
    
    sigma
        Standard deviation of initial noise.
    
    device
        Device to use.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 iterations: int = 100,
                 alpha: float = .01,
                 restarts: int = 5,
                 sigma: float = .01,
                 device: torch.device = torch.device('cuda')):
        super().__init__(threat_model)

        self.iterations = iterations
        self.alpha = alpha
        self.restarts = restarts
        self.sigma = sigma
        self.device = device
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        # track best set of adversarial examples
        x_best = x_data.detach().clone()
        best_loss = -torch.inf

        # do a number of random restarts
        for _ in range(self.restarts):
            # initialize run with noisy samples
            noise = self.sigma * torch.randn_like(x_data)
            x_adv = self.threat.project(x_data, x_data.detach().clone() + noise)
            x_adv.requires_grad = True

            # iteratively optimize the perturbations
            for _ in range(self.iterations):
                # get loss gradients
                y_pred = model(x_adv)
                loss = F.nll_loss(y_pred, y_data)
                _grad_check(loss)
                loss.backward()

                with torch.no_grad():
                    # update perturbations
                    deltas = self.alpha * torch.sign(x_adv.grad)
                    x_adv = x_adv + deltas
                    x_adv = self.threat.project(x_data, x_adv)

                    # check new best
                    y_pred = model(x_adv)
                    loss = F.nll_loss(y_pred, y_data).item()
                    if loss > best_loss:
                        best_loss = loss
                        x_best = x_adv.detach().clone()
                x_adv.requires_grad = True

        return x_best
