"""
Models
=======

Facilities for loading models.
"""

import torch

from robusthub.base import Array

from abc import ABC, abstractmethod

class Model(ABC):
    """
    Abstract base class for all models.
    """
    def __init__(self):
        """
        Construct the model.
        """
        pass

    @abstractmethod
    def predict(self, x_data: Array) -> Array:
        """
        Query the model on a batch of samples.

        Parameters
        -----------
        x_data
            A batch of input data samples.
        
        Returns
        -------
        Array
            A batch of outputs from the model.
        """
        pass

class PyTorchModel(Model):
    """
    A model derived from a PyTorch module.
    """
    def __init__(self, model: torch.nn.Module):
        """
        Construct the model.

        Parameters
        -----------
        model
            The PyTorch module to use.
        """
        self.model = model
    
    def predict(self, x_data: torch.Tensor) -> torch.Tensor:
        """
        Query the model on a set of samples.

        Parameters
        -----------
        x_data
            A torch tensor containing a batch of samples.
        
        Returns
        --------
        torch.Tensor
            A batch of outputs from the model.
        """
        return self.model(x_data)


def load(repo: str, ident: str, pretrained: bool = False) -> Model:
    """
    Load a model from a given repository.

    Parameters
    -----------
    repo
        The repository identifier.

    ident
        The model identifier.

    pretrained
        Load pretrained weights.
    
    Returns
    --------
    Model
        A `Model` instance.
    """
    model = torch.hub.load(repo, ident, pretrained=pretrained)
    return PyTorchModel(model)
