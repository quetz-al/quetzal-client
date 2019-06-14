""" Helper module for easier access to common API methods

This package encapsulates the methods used in :py:mod:`quetzal.client.cli` so
that other libraries using this package do not have to interact with the
Quetzal client through the command line.

"""
from . import auth, file, workspace
from .query import query
from .misc import get_client

__all__ = (
    'auth',
    'file',
    'get_client',
    'query',
    'workspace',
)
