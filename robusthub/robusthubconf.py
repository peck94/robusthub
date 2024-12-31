from robusthub.defenses import Defense, AdversarialTraining, RandomizedSmoothing
from robusthub.attacks import Attack, ProjectedGradientDescent, FastGradientSignMethod

dependencies = []

def adversarial_training(**kwargs) -> Defense:
    return AdversarialTraining(**kwargs)

def randomized_smoothing(**kwargs) -> Defense:
    return RandomizedSmoothing(**kwargs)

def pgd(**kwargs) -> Attack:
    return ProjectedGradientDescent(**kwargs)

def fgsm(**kwargs) -> Attack:
    return FastGradientSignMethod(**kwargs)
