"""
This module offers standardized methods of loading commonly used data sets.

Each data set, when loaded, returns a tuple of :code:`torch.utils.data.DataLoader` objects:

* The training loader, which contains batches of data that can be used for training (e.g. standard or adversarial training).
* The validation loader, which contains batches of data to be used during training procedures to prevent overfitting and perform other optimizations.
* The test loader, which contains batches of test data to be used after training is complete.

These three sets are disjoint and randomly split according to the supplied :code:`seed`.

Note that most machine learning data sets do not have a standardized validation set.
Whenever this is the case, validation data will be obtained by randomly splitting off 20% of the training set.
The test set is never mixed with the other sets in order to maintain compatibility with external evaluations.
"""
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
    
    @abstractmethod
    def load(self, batch_size: int = 32, seed: int = 42) -> Tuple[DataLoader, DataLoader, DataLoader]:
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
        pass
