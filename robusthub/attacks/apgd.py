import torch
import torch.nn.functional as F

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.attacks.attack import Attack, _grad_check

class AutoProjectedGradientDescent(Attack):
    """
    The AutoPGD attack proposed by :cite:`croce2020reliable`.

    Parameters
    -----------
    threat_model
        The threat model to use.
    
    iterations
        Number of iterations of optimization.
    
    alpha
        Weighting factor for exponential moving average updates.
    
    eta
        Per-iteration step size.
    
    device
        Device to use.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 iterations: int = 100,
                 alpha: float = .75,
                 eta: float = .01,
                 device: torch.device = torch.device('cuda')):
        super().__init__(threat_model)

        self.iterations = iterations
        self.alpha = alpha
        self.eta = eta
        self.device = device
    
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        eta = self.eta
        noise = torch.randn(x_data.shape).to(self.device)
        x_tilde = self.threat.project(x_data, x_data + noise)
        prev_samples = x_tilde.clone()
        best_loss = -torch.inf
        x_best = torch.zeros_like(x_data)

        for _ in range(self.iterations):
            samples = x_tilde.clone().detach().requires_grad_()

            y_pred = model(samples)
            loss = F.nll_loss(y_pred, y_data)
            _grad_check(loss)
            loss.backward()

            g = samples.grad
            z = self.threat.project(x_data, samples + eta * g)
            x_tilde = self.threat.project(x_data, samples + self.alpha * (z - samples) + (1 - self.alpha) * (samples - prev_samples))

            y_pred = model(x_tilde)
            loss = F.nll_loss(y_pred, y_data)
            if loss > best_loss:
                best_loss = loss
                x_best = x_tilde.clone()
            
            samples.grad = None
            prev_samples = samples.clone()

        return x_best
