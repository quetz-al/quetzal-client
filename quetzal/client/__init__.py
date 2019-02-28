from ._version import get_versions
from .base import Client
from .config import Configuration
from .exceptions import QuetzalAPIException


__version__ = get_versions()['version']
del get_versions

__all__ = (
    '__version__',
    'Client',
    'Configuration',
    'QuetzalAPIException',
)
