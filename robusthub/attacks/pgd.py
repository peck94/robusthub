import torch

from robusthub.attacks.attack import Attack

class ProjectedGradientDescent(Attack):
    """
    The projected gradient descent attack.
    """
    def __init__(self, model):
        super().__init__(model)
    
    def apply(self, x_data: torch.Tensor, y_data: torch.Tensor | None) -> torch.Tensor:
        return x_data
