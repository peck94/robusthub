"""
Facilities for loading models.

RobustHub relies on PyTorch Hub for loading models externally. Consult the `PyTorch Hub documentation page <https://pytorch.org/docs/stable/hub.html>`_ for more information.
"""

import torch

from typing import List, Iterable

from abc import ABC, abstractmethod

class Model(ABC):
    """
    Abstract base class for all models.
    """

    @abstractmethod
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the model.

        Parameters
        -----------
        x
            Input tensor.
        
        Returns
        --------
        torch.Tensor
            Output tensor.
        """
        pass

    @abstractmethod
    def parameters(self) -> Iterable:
        """
        Return the model parameters.

        Returns
        --------
        Iterable
            Iterable of model parameters.
        """
        pass

    def __call__(self, x: torch.Tensor) -> torch.Tensor:
        """
        Forward pass through the model.

        Parameters
        -----------
        x
            Input tensor.
        
        Returns
        --------
        torch.Tensor
            Output tensor.
        """
        return self.forward(x)

class CompositeModel(Model):
    """
    Composition of multiple models.

    Parameters
    -----------
    models
        List of models to compose sequentially (first to last).
    """
    def __init__(self, models: List[Model]):
        super().__init__()
        self.models = models
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y_out = x
        for model in self.models:
            y_out = model(y_out)
        return y_out

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
        A :code:`Model` instance.
    """
    return torch.hub.load(repo, ident, **kwargs)
