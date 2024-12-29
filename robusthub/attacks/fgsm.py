import torch
import torch.nn.functional as F

from robusthub.models import Model
from robusthub.attacks.attack import Attack

class FastGradientSignMethod(Attack):
    """
    The fast gradient sign attack.
    """
    def __init__(self, model: Model, epsilon: float = .03):
        super().__init__(model)

        self.epsilon = epsilon
    
    def apply(self, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        samples = x_data.clone().detach().requires_grad_()
        samples.retain_grad()

        y_pred = self.model(samples)
        loss = F.nll_loss(y_pred, y_data)
        loss.backward()

        return samples + self.epsilon * torch.sign(samples.grad)
