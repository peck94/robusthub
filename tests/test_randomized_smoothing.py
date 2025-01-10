from robusthub import models
from robusthub import defenses

def test_rs(trainloader, testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # initialize defense
    defense = defenses.RandomizedSmoothing(10, .01)

    # smooth model
    rs_model = defense.apply(model)

    # test smoothed model
    correct = 0
    total = 0
    for x_batch, y_batch in testloader:
        y_pred = rs_model(x_batch)
        correct += (y_batch.cpu().detach().numpy() == y_pred.cpu().detach().numpy()).sum()
        total += x_batch.shape[0]
    print(f'Accuracy: {correct/total:.2%}')
