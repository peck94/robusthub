import torch
import torch.nn.functional as F

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.attacks.attack import Attack

class ProjectedGradientDescent(Attack):
    """
    The projected gradient descent attack popularized by :cite:`madry2017attack`.
    """
    def __init__(self,
                 model: Model,
                 threat_model: ThreatModel,
                 iterations: int = 100,
                 device: torch.device = torch.device('cuda')):
        super().__init__(model, threat_model)

        self.iterations = iterations
        self.device = device
    
    def apply(self, x_data: torch.Tensor, y_data: torch.Tensor) -> torch.Tensor:
        noise = torch.randn(x_data.shape).to(self.device)
        x_tilde = self.threat.project(x_data, x_data + noise)

        for _ in range(self.iterations):
            samples = x_tilde.clone().detach().requires_grad_()
            samples.retain_grad()

            y_pred = self.model(samples)
            loss = F.nll_loss(y_pred, y_data)
            loss.backward()

            deltas = torch.sign(samples.grad)
            x_tilde = self.threat.project(x_data, x_tilde + deltas)
            samples.grad.zero_()
        return x_tilde
