"""
Catalog of adversarial defenses and facilities for loading external defenses.
"""
import torch

import contextlib

import sys

import os

import shutil

import zipfile

from urllib.error import HTTPError
from urllib.request import urlopen

from types import ModuleType

from typing import Callable

from robusthub.models import Model

from abc import ABC, abstractmethod

MODULE_HUBCONF = 'robusthubconf.py'
VAR_DEPENDENCY = 'dependencies'
HUB_DIR = 'hub'

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

def load(repo: str, ident: str, source: str = 'github', force_reload: bool = False, **kwargs) -> Defense:
    """
    Load an adversarial defense from a given repository.

    Parameters
    -----------
    repo
        The repository identifier. If `source` is `local`, this is the path to the local directory where the `robusthubconf.py` file can be found.

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

def _git_archive_link(repo_owner: str, repo_name: str, ref: str) -> str:
    # https://docs.github.com/en/rest/reference/repos#download-a-repository-archive-zip
    return f"https://github.com/{repo_owner}/{repo_name}/zipball/{ref}"

def _parse_repo_info(github: str) -> str:
    if ':' in github:
        repo_info, ref = github.split(':')
    else:
        repo_info, ref = github, None
    repo_owner, repo_name = repo_info.split('/')

    if ref is None:
        try:
            with urlopen(f'https://github.com/{repo_owner}/{repo_name}/tree/main/'):
                ref = 'main'
        except HTTPError as e:
            if e.code == 404:
                ref = 'master'
            else:
                raise
    return repo_owner, repo_name, ref

def _remove_if_exists(path: str):
    if os.path.exists(path):
        if os.path.isfile(path):
            os.remove(path)
        else:
            shutil.rmtree(path)

def _get_github(github: str, force_reload: bool) -> str:
    os.makedirs(HUB_DIR, exist_ok=True)

    repo_owner, repo_name, ref = _parse_repo_info(github)
    normalized_br = ref.replace("/", "_")
    owner_name_branch = "_".join([repo_owner, repo_name, normalized_br])
    repo_dir = os.path.join(HUB_DIR, owner_name_branch)

    cached_file = os.path.join(HUB_DIR, normalized_br + '.zip')
    _remove_if_exists(cached_file)

    try:
        url = _git_archive_link(repo_owner, repo_name, ref)
        sys.stderr.write(f'Downloading: "{url}" to {cached_file}\n')
        torch.hub.download_url_to_file(url, cached_file, progress=False)
    except HTTPError as err:
        if err.code == 300:
            disambiguated_branch_ref = f'refs/heads/{ref}'
            url = _git_archive_link(
                repo_owner, repo_name, ref=disambiguated_branch_ref
            )
            torch.hub.download_url_to_file(url, cached_file, progress=False)
        else:
            raise

    with zipfile.ZipFile(cached_file) as cached_zipfile:
        extraced_repo_name = cached_zipfile.infolist()[0].filename
        extracted_repo = os.path.join(HUB_DIR, extraced_repo_name)
        _remove_if_exists(extracted_repo)
        cached_zipfile.extractall(HUB_DIR)

    _remove_if_exists(cached_file)
    _remove_if_exists(repo_dir)
    shutil.move(extracted_repo, repo_dir)

@contextlib.contextmanager
def _add_to_sys_path(path: str):
    sys.path.insert(0, path)
    try:
        yield
    finally:
        sys.path.remove(path)

def _import_module(name: str, path: str) -> ModuleType:
    import importlib.util
    from importlib.abc import Loader

    spec = importlib.util.spec_from_file_location(name, path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert isinstance(spec.loader, Loader)
    spec.loader.exec_module(module)
    return module

def _load_attr_from_module(module: ModuleType, func_name: str) -> Callable:
    if func_name not in dir(module):
        return None
    return getattr(module, func_name)

def _check_module_exists(name: str) -> bool:
    import importlib.util

    return importlib.util.find_spec(name) is not None

def _check_dependencies(m: ModuleType):
    dependencies = _load_attr_from_module(m, VAR_DEPENDENCY)

    if dependencies is not None:
        missing_deps = [pkg for pkg in dependencies if not _check_module_exists(pkg)]
        if missing_deps:
            raise RuntimeError(f'Missing dependencies: {', '.join(missing_deps)}')

def _load_entry_from_hubconf(m: ModuleType, defense: str):
    _check_dependencies(m)

    func = _load_attr_from_module(m, defense)

    if func is None or not callable(func):
        raise RuntimeError(f'Callable {defense} not found in robusthubconf')

    return func

def _load_local(repo: str, ident: str, **kwargs) -> Defense:
    with _add_to_sys_path(repo):
        hubconf_path = os.path.join(repo, MODULE_HUBCONF)
        hub_module = _import_module(MODULE_HUBCONF, hubconf_path)

        entry = _load_entry_from_hubconf(hub_module, ident)
        defense = entry(**kwargs)
    
    return defense
