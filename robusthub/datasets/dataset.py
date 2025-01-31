from torch.utils.data import DataLoader

from abc import ABC, abstractmethod

from typing import Tuple

class Dataset(ABC):
    """
    Abstract base class for data sets.

    Parameters
    -----------
    name
        The name of the data set.
    
    path
        Path to a directory where the data is stored.
    """
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path
    
    """
    Load the data set.

    Parameters
    -----------
    batch_size
        Size of the data batches.

    seed
        Random seed to use for data splitting.
    
    Returns
    --------
    A tuple consisting of the training, validation and test data.
    """
    @abstractmethod
    def load(self, batch_size: int = 32, seed: int = 42) -> Tuple[DataLoader, DataLoader, DataLoader]:
        pass
