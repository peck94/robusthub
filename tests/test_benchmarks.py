from robusthub import threats
from robusthub import models
from robusthub import defenses
from robusthub import benchmarks
from robusthub import attacks
from robusthub import metrics

def test_benchmark(trainloader, testloader, device):
    # load model
    model = models.load('pytorch/vision', 'resnet18').to(device)

    # define threat model
    threat_model = threats.Composite([
        threats.Linf(.03),
        threats.Bounds(0, 1)])

    # initialize defense
    defense = defenses.AdversarialTraining(trainloader, testloader, threat_model, 2, 2, device)

    # initialize benchmark
    attack = attacks.FastGradientSignMethod(threat_model)
    metric_list = [metrics.Accuracy()]
    benchmark = benchmarks.Benchmark(attack, metric_list, device)
    result = benchmark.run(model, defense, testloader)

    print(result)
