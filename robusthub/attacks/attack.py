"""
Catalog of adversarial attacks.

An *adversarial attack* takes a model and a batch of data samples and returns a new set of data samples called *adversarial examples*.
These adversarial examples are optimized so that the model achieves the worst possible score on one or more task-specific metrics,
subject to the constraints defined by a given threat model.
"""
import torch

from abc import ABC, abstractmethod

from robusthub.models import Model
from robusthub.threats import ThreatModel
from robusthub.utils import _get_github, _load_local

class Attack(ABC):
    """
    Abstract base class for all adversarial attacks.

    Parameters
    -----------
    threat_model
        The threat model of the attack.
    """
    def __init__(self, threat_model: ThreatModel):
        self.threat = threat_model

    @abstractmethod
    def apply(self, model: Model, x_data: torch.Tensor, y_data: torch.Tensor | None) -> torch.Tensor:
        """
        Apply the attack to a batch of samples.

        Parameters
        -----------
        model
            Model to attack.

        x_data
            Tensor of input data samples.
        
        y_data
            Tensor of targets (optional).
        
        Returns
        --------
        torch.Tensor
            Tensor of corrupted data samples.
        """
        pass

def load(repo: str, ident: str, source: str = 'github', force_reload: bool = False, **kwargs) -> Attack:
    """
    Load an adversarial attack from a given repository.

    Parameters
    -----------
    repo
        The repository identifier. If `source` is `local`, this is the path to the local directory where the :code:`robusthubconf.py` file can be found.

    ident
        The attack identifier.
    
    source
        Source to load from. Either `local` or `github`.
    
    force_reload
        Force reloading of the module.

    kwargs
        Optional keyword arguments for the attack.
    
    Returns
    --------
    Attack
        An `Attack` instance.
    """
    source = source.lower()

    if source not in ['github', 'local']:
        raise ValueError(f'Unknown source: {repo}. Should be local or github.')
    
    if source == 'github':
        repo = _get_github(repo, force_reload)
    
    attack = _load_local(repo, ident, **kwargs)

    assert isinstance(attack, Attack), 'Not a valid attack'

    return attack
