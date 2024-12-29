from robusthub import threats
from robusthub import models
from robusthub import defenses

def test_at(trainloader, testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # initialize defense
    defense = defenses.AdversarialTraining(trainloader, testloader, threats.Linf(.03), 10, 10, device)

    # adversarially train
    robust_model = defense.apply(model)
