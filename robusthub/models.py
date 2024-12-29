"""
Facilities for loading models.
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
        Optional keyword arguments for `torch.hub.load`.
    
    Returns
    --------
    Model
        A `Model` instance.
    """
    return torch.hub.load(repo, ident, **kwargs)
