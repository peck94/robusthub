"""
Facilities for loading models.
"""

import torch

type Model = torch.nn.Module


def load(repo: str, ident: str, weights: str | None = None) -> Model:
    """
    Load a model from a given repository.

    Parameters
    -----------
    repo
        The repository identifier.

    ident
        The model identifier.

    weights
        Pretrained weights identifier (optional).
    
    Returns
    --------
    Model
        A `Model` instance.
    """
    return torch.hub.load(repo, ident, weights=weights)
