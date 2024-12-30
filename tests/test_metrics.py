import numpy as np

from robusthub import models
from robusthub import metrics

def test_at(testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # measure things
    accuracy = metrics.Accuracy()

    accs = []
    for x_data, y_data in testloader:
        accs.append(accuracy.compute(model, x_data.to(device), y_data.to(device)))
    print(f'Accuracy: {np.sum(accs) / len(testloader):.2%}')
