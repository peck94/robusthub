from robusthub.defenses import load
from robusthub.threats import Linf

def test_local_hubconf(trainloader, testloader):
    threat = Linf(.03)
    defense = load('robusthub', 'adversarial_training', 'local',
                   training_data=trainloader,
                   validation_data=testloader,
                   threat_model=threat)
    assert defense

def test_github_hubconf(trainloader, testloader):
    threat = Linf(.03)
    defense = load('peck94/robusthub', 'adversarial_training', 'github',
                   training_data=trainloader,
                   validation_data=testloader,
                   threat_model=threat)
    assert defense
