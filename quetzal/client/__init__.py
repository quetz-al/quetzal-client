from ._version import get_versions
from .base import Client
from .config import Configuration
from .exceptions import QuetzalAPIException
from quetzal._auto_client import __openapi_generator_cli_version__


__version__ = get_versions()['version']
del get_versions

__all__ = (
    '__version__',
    '__openapi_generator_cli_version__',
    'Client',
    'Configuration',
)
