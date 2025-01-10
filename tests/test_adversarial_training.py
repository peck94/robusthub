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
    at_model = defense.apply(model)

    # test adversarially trained model
    correct = 0
    total = 0
    for x_batch, y_batch in testloader:
        y_pred = at_model(x_batch)
        correct += (y_batch.cpu().detach().numpy() == y_pred.cpu().detach().numpy()).sum()
        total += x_batch.shape[0]
    print(f'Accuracy: {correct/total:.2%}')
