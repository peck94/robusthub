"""
Catalog of adversarial defenses and facilities for loading external defenses.

A *defense* is an operator on the space of models. That is, it takes a model as input and returns another model as output.
"""
from robusthub.models import Model
from robusthub.utils import _get_github, _load_local

from abc import ABC, abstractmethod

class Defense(ABC):
    """
    Abstract base class for all adversarial defenses.
    """

    def __init__(self):
        pass

    @abstractmethod
    def apply(self, model: Model) -> Model:
        """
        Apply the defense to a given model.

        Parameters
        -----------
        model
            The model to which the defense will be applied.
        
        Returns
        --------
        Model
            The supplied model with the defense applied.
        """
        pass

class Vanilla(Defense):
    """
    The vanilla defense simply returns a model as-is.
    """
    def __init__(self):
        super().__init__()
    
    def apply(self, model: Model) -> Model:
        return model

def load(repo: str, ident: str, source: str = 'github', force_reload: bool = False, **kwargs) -> Defense:
    """
    Load an adversarial defense from a given repository.

    Parameters
    -----------
    repo
        The repository identifier. If `source` is `local`, this is the path to the local directory where the :code:`robusthubconf.py` file can be found.

    ident
        The defense identifier.
    
    source
        Source to load from. Either `local` or `github`.
    
    force_reload
        Force reloading of the module.

    kwargs
        Optional keyword arguments for the defense.
    
    Returns
    --------
    Defense
        A `Defense` instance.
    """
    source = source.lower()

    if source not in ['github', 'local']:
        raise ValueError(f'Unknown source: {repo}. Should be local or github.')
    
    if source == 'github':
        repo = _get_github(repo, force_reload)
    
    defense = _load_local(repo, ident, **kwargs)

    assert isinstance(defense, Defense), 'Not a valid defense'

    return defense
