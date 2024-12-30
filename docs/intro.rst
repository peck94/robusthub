Getting started
================

RobustHub is designed with two target audiences in mind:

1. **Practitioners** who wish to deploy robust models in a real production setting, but who are not experts in adversarial machine learning.
2. **Researchers** who wish to develop novel adversarial defenses and want an easy way to compare their work to the existing state of the art.

Therefore, the fundamental aim of RobustHub is to facilitate the selection and application of existing defenses to arbitrary models and data sets. To that end, we supply a catalog of defenses as well as benchmarking results of these defenses on a variety of data sets and models. These benchmarks are fully reproducible using only a few lines of code, as demonstrated in the below `examples`_.

We also strongly encourage *diversity* in our benchmarks. The field of adversarial machine learning tends to focus almost exclusively on image classification, particularly the CIFAR-10 and ImageNet data sets. This lack of diversity in tasks and data sets calls into question the generalizability of current defenses. It also hinders the adoption of adversarial defenses in practice, since most applications are not developed for classifying ImageNet. RobustHub therefore includes a diverse set of threat models, adversarial attacks and defenses aimed at a wide variety of domains and modalities.

Installation
-------------

Examples
---------

This section provides concrete examples for common usecases of this package.

Adversarial training
^^^^^^^^^^^^^^^^^^^^^

This example demonstrates how to apply a simple adversarial training defense. We assume the CIFAR-10 data set has been loaded, where :code:`train_loader` provides training data and :code:`val_loader` provides validation data. The adversarial training here is carried out on a ResNet18 model in the :math:`L_\infty` threat model at :math:`\varepsilon = 0.03`.

.. code-block:: python

    from robusthub import models, defenses, threats

    # Load CIFAR-10

    # ... snip ...
    
    # The model can be loaded from PyTorch Hub
    model = models.load('pytorch/vision', 'resnet18')

    # The threat model is Linfty at eps = 0.03 and clipping between (0,1)
    threat_model = threats.Composite([
        threats.Linf(.03),
        threats.Bounds(0, 1)])

    # Initialize the defense
    defense = defenses.AdversarialTraining(train_loader, val_loader, threat_model)

    # Adversarially training the model returns a robust model
    robust_model = defense.apply(model)


Using an external defense
^^^^^^^^^^^^^^^^^^^^^^^^^^

One of the most important features of RobustHub is the ability to easily load external defenses published by third parties. The API is deliberately modeled after PyTorch Hub for this functionality:

.. code-block:: python

    from robusthub import models, defenses, threats

    # Load CIFAR-10

    # ... snip ...
    
    # The model can be loaded from PyTorch Hub
    model = load_model('pytorch/vision', 'resnet18')

    # The threat model is Linfty at eps = 0.03 and clipping between (0,1)
    threat_model = threats.Composite([
        threats.Linf(.03),
        threats.Bounds(0, 1)])

    # Load the defense from GitHub
    defense = defenses.load('peck94/robusthub', # repository
                    'adversarial_training', # entrypoint
                    # keyword arguments for defense constructor
                    training_data=train_loader,
                    validation_data=test_loader,
                    threat_model=threat_model)

    # Adversarially training the model returns a robust model
    robust_model = defense.apply(model)

If you wish to contribute your own defense to RobustHub so it can be easily loaded via this interface, consult our page on :doc:`contributing <publish>`.

.. warning::
    As with external models in PyTorch Hub, loading external defenses in RobustHub executes third-party Python code.
    Specifically, RobustHub downloads and executes the provided :code:`robusthubconf.py` file, which may contain arbitrary code.
    **Never load defenses from untrusted sources.**
