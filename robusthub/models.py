"""
Facilities for loading models.

A model in RobustHub is simply an instance of :code:`torch.nn.Module`, i.e. a PyTorch model.

RobustHub relies on PyTorch Hub for loading models externally. Consult the `PyTorch Hub documentation page <https://pytorch.org/docs/stable/hub.html>`_ for more information.
"""

import torch

type Model = torch.nn.Module


def load(repo: str, ident: str, **kwargs) -> Model:
    """
    Load a model from a given repository.

    Parameters
    -----------
    repo
        The repository identifier.

    ident
        The model identifier.

    kwargs
        Optional keyword arguments for :code:`torch.hub.load`.
    
    Returns
    --------
    Model
        A :code:`Model` instance. This is an alias of :code:`torch.nn.Module`.
    """
    return torch.hub.load(repo, ident, **kwargs)
