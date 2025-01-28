from robusthub import defenses
from robusthub.defenses import Defense

from robusthub import attacks
from robusthub.attacks import Attack

dependencies = []

def vanilla_defense(**kwargs) -> Defense:
    return defenses.Vanilla(**kwargs)

def adversarial_training(**kwargs) -> Defense:
    return defenses.AdversarialTraining(**kwargs)

def randomized_smoothing(**kwargs) -> Defense:
    return defenses.RandomizedSmoothing(**kwargs)

def apgd(**kwargs) -> Attack:
    return attacks.AutoProjectedGradientDescent(**kwargs)

def pgd(**kwargs) -> Attack:
    return attacks.ProjectedGradientDescent(**kwargs)

def fgsm(**kwargs) -> Attack:
    return attacks.FastGradientSignMethod(**kwargs)

def simba(**kwargs) -> Attack:
    return attacks.Simba(**kwargs)
