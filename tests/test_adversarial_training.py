from robusthub import threats
from robusthub import models
from robusthub import defenses

def test_at(trainloader, testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # define threat model
    threat_model = threats.Composite([
        threats.Linf(.03),
        threats.Bounds(0, 1)])

    # initialize defense
    defense = defenses.AdversarialTraining(trainloader, testloader, threat_model, 2, 2, device)

    # adversarially train
    robust_model = defense.apply(model)
