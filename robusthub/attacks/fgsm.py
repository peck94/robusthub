from robusthub.attacks.attack import Attack

class FastGradientSignMethod(Attack):
    """
    The fast gradient sign attack.
    """
    def __init__(self, model):
        super().__init__(model)
