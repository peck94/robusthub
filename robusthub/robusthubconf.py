from robusthub.defenses import Defense, AdversarialTraining, RandomizedSmoothing

dependencies = []

def adversarial_training(**kwargs) -> Defense:
    return AdversarialTraining(**kwargs)

def randomized_smoothing(**kwargs) -> Defense:
    return RandomizedSmoothing(**kwargs)
