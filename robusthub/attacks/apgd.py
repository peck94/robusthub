import torch
import torch.nn.functional as F

import numpy as np

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.attacks.attack import Attack, _grad_check

class AutoProjectedGradientDescent(Attack):
    """
    The AutoPGD attack proposed by :cite:`croce2020reliable`.

    The default values are the ones used in the paper. It is not recommended to modify them.

    Parameters
    -----------
    threat_model
        The threat model to use.
    
    iterations
        Number of iterations of optimization.
    
    alpha
        Weighting factor for exponential moving average updates.
    
    eta
        Initial per-iteration step size.
    
    rho
        Fraction of update steps that must lead to improvement before step size is halved.
    
    restarts
        Number of random restarts.
    
    sigma
        Standard deviation of initial noise.
    
    device
        Device to use.
    """
    def __init__(self,
                 threat_model: ThreatModel,
                 iterations: int = 100,
                 alpha: float = .75,
                 eta: float = .01,
                 rho: float = .75,
                 restarts: int = 5,
                 sigma: float = .01,
                 device: torch.device = torch.device('cuda')):
        super().__init__(threat_model)

        self.iterations = iterations
        self.alpha = alpha
        self.eta = eta
        self.rho = rho
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
            x_prev = x_data.detach().clone()

            # initialize checkpoints
            checkpoint = 0
            p_prev = 0
            p_next = .22
            improvement_counter = 0
            eta = self.eta
            eta_prev = self.eta
            best_loss_prev = best_loss

            # iteratively optimize the perturbations
            for i in range(self.iterations):
                # get loss gradients
                y_pred = model(x_adv)
                loss = F.nll_loss(y_pred, y_data)
                _grad_check(loss)
                loss.backward()

                with torch.no_grad():
                    # update perturbations
                    z = self.threat.project(x_data, x_adv + eta * torch.sign(x_adv.grad))
                    x_next = self.threat.project(x_data,
                                                 x_adv
                                                + self.alpha * (z - x_adv)
                                                + (1 - self.alpha) * (x_adv - x_prev))
                    x_prev = x_adv.detach().clone()
                    x_adv = x_next.detach().clone()

                    # check new best
                    y_pred = model(x_adv)
                    loss = F.nll_loss(y_pred, y_data).item()
                    if loss > best_loss:
                        # record improvement
                        best_loss_prev = best_loss
                        best_loss = loss
                        x_best = x_adv.detach().clone()
                        improvement_counter += 1
                    
                    # checkpoint
                    if i >= checkpoint:
                        # check conditions C1 and C2
                        period = (p_next - p_prev) * self.iterations
                        c1 = (improvement_counter / period < self.rho)
                        c2 = (np.isclose(eta, eta_prev) and np.isclose(best_loss, best_loss_prev))
                        if c1 or c2:
                            # halve step size and reset
                            eta_prev = eta
                            eta /= 2
                            x_adv = x_best.detach().clone()

                        # reset counters
                        improvement_counter = 0

                        # set next checkpoint
                        checkpoint = int(np.ceil(p_next * self.iterations))
                        p_next = p_next + max(p_next - p_prev - .03, .06)
                x_adv.requires_grad = True

        return x_best
