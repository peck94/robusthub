Getting started
================

RobustHub is designed with two target audiences in mind:

1. Practitioners who wish to deploy robust models but are not experts in adversarial machine learning.
2. Researchers who wish to develop novel adversarial defenses and want an easy way to compare their work to the existing state of the art.

Therefore, the fundamental aim of RobustHub is to facilitate the selection and application of existing defenses to arbitrary models and data sets. To that end, we supply a catalog of defenses as well as benchmarking results of these defenses on a variety data sets and models. These benchmarks are fully reproducible using only a few lines of code, as demonstrated in the below examples.

Installation
-------------

Example: randomized smoothing
------------------------------

Example: adversarial training
------------------------------

This example demonstrates how to apply a simple adversarial training defense. We assume the CIFAR-10 data set has been loaded, where `train_loader` provides training data and `val_loader` provides validation data. The adversarial training here is carried out on a ResNet18 model in the :math:`L_\infty` threat model at :math:`\varepsilon = 0.03`.

.. code-block:: python

    from robusthub.models import load
    from robusthub.threats import Linf
    from robusthub.defenses import AdversarialTraining

    # Load CIFAR-10

    # ... snip ...
    
    # The model can be loaded from PyTorch Hub
    model = load('pytorch/vision', 'resnet18')

    # The threat model is Linfty at eps = 0.03
    threat_model = Linf(.03)

    # Initialize the defense
    defense = AdversarialTraining(train_loader, val_loader, threat_model)

    # Adversarially training the model returns a robust model
    robust_model = defense.apply(model)

Example: reproducing a benchmark
---------------------------------
