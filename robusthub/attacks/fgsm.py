from robusthub.base import Array
from robusthub.attacks.attack import Attack

class FastGradientSignMethod(Attack):
    """
    The fast gradient sign attack.
    """
    def __init__(self, model):
        super().__init__(model)
    
    def apply(self, x_data: Array, y_data: Array | None) -> Array:
        return x_data
