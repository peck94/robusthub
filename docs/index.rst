RobustHub documentation
=======================

**TODO:**

Publishing models
------------------

RobustHub relies on `PyTorch Hub <https://pytorch.org/hub/>`_ to load external models. Any model that has been published on PyTorch Hub is compatible with RobustHub. Consult the `PyTorch Hub documentation page <https://pytorch.org/docs/stable/hub.html>`_ for more information.

Publishing defenses
--------------------

RobustHub uses a mechanism similar to PyTorch Hub to load external defenses. External defenses can be loaded in from a local directory or from a remote GitHub repository. The only requirement is that the directory or repository must contain a `robusthubconf.py` file in its root. This file specifies all dependencies as well as one or more entrypoints which instantiate the defense and any of its variants. An example `robusthubconf.py` file can be found in the RobustHub GitHub repository itself.

To provide a user-friendly and unified interface, RobustHub expects all external defenses to subclass :py:class:`robusthub.defenses.defense.Defense`. Attempting to load an external defense that does not match this interface will raise an error.

RobustHub provides several defenses out of the box, which can be used as a basis for developing and publishing new defenses of your own. See our :doc:`Defenses <defenses>` page for more details.

Contents
----------

.. toctree::
   :maxdepth: 1
   
   models
   threats
   defenses
   attacks
