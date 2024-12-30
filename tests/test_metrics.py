import numpy as np

from robusthub import models
from robusthub import metrics

def test_at(testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # measure things
    accuracy = metrics.Accuracy()
    time = metrics.Runtime()
    memory = metrics.Memory()

    accs = []
    times = []
    mems = []
    for batch in testloader:
        x_data, y_data = batch
        x_data, y_data = x_data.to(device), y_data.to(device)

        accs.append(accuracy.compute(model, x_data, y_data))
        times.append(time.compute(model, x_data, y_data))
        mems.append(memory.compute(model, x_data, y_data))
    
    print(f'Accuracy: {np.sum(accs) / len(testloader):.2%}')
    print(f'Runtime : {np.mean(times)}')
    print(f'Memory  : {np.mean(mems)}')
