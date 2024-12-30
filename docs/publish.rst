Contributing
=============

Publishing models
------------------

RobustHub relies on `PyTorch Hub <https://pytorch.org/hub/>`_ to load external models. Any model that has been published on PyTorch Hub is compatible with RobustHub. Consult the `PyTorch Hub documentation page <https://pytorch.org/docs/stable/hub.html>`_ for more information.

Publishing defenses
--------------------

RobustHub uses a mechanism similar to PyTorch Hub to load external defenses. External defenses can be loaded in from a local directory or from a remote GitHub repository. The only requirement is that the directory or repository must contain a :code:`robusthubconf.py` file in its root. This file specifies all dependencies as well as one or more entrypoints which instantiate the defense and any of its variants. An example :code:`robusthubconf.py` file can be found in the RobustHub GitHub repository itself. A basic script looks like this:

.. code:: python

    from robusthub.defenses import Defense, AdversarialTraining, RandomizedSmoothing

    dependencies = []

    def adversarial_training(**kwargs) -> Defense:
        return AdversarialTraining(**kwargs)

This script simply returns the built-in :py:class:`robusthub.defenses.AdversarialTraining` defense and is hence quite useless in practice. However, it should make the basic structure of the script clear. The file begins with a set of imports necessary for the script to function. Then, we declare a :code:`dependencies` list which consists of the names of modules on which the defense depends. It is not necessary to specifiy :code:`robusthub`, obviously. It is also not necessary to specifiy :code:`torch` or :code:`torchvision`, since RobustHub already depends on these. The script then defines one or more functions which take keyword arguments and return an object of type :py:class:`robusthub.defenses.defense.Defense`. The location of the :code:`robusthubconf.py` file as well as the name of the function which constructs the defense are supplied to the :py:meth:`robusthub.defenses.defense.load` method.

.. note::
    To provide a user-friendly and unified interface, RobustHub expects all external defenses to subclass :py:class:`robusthub.defenses.defense.Defense`. Attempting to load an external defense that does not match this interface will raise an error.

RobustHub provides several defenses out of the box, which can be used as a basis for developing and publishing new defenses of your own. See our :doc:`Defenses <defenses>` page for more details.
