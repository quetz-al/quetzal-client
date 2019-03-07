""" Common API methods

This package encapsulates the methods used in :py:mod:`quetzal.client.cli` so
that other libraries using this package do not have to interact with the
Quetzal client through the command line.

"""
from . import auth, file, query, workspace

__all__ = (
    'auth',
    'file',
    'query',
    'workspace',
)
