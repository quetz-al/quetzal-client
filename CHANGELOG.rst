=========
Changelog
=========

This document list all important changes to quetzal-client.

Quetzal-client version numbers follow `semantic versioning <http://semver.org>`_.

0.1.1 (2019-03-08)
------------------

* ``quetzal.client.api`` has been renamed to ``quetzal.client.helpers``.
* File download, with verification of known files, added to helpers.
* File download falls back to user data directory if output not set.
* Config default to environment variable values when created.
* Initial structure of Sphinx documentation.


0.1.0 (2019-03-05)
------------------

* First iteration of the Quetzal Python client.
* Delegates the *automatic* code to `quetzal-openapi-client <https://github.com/quetz-al/quetzal-openapi-client>`_.
* Command-line interface implemented with `Click <https://palletsprojects.com/p/click/>`_
  for most operations available on the Quetzal API.
* Incomplete implementation of a helper module `quetzal.client.api` that
  encapsulates the usage of the auto-generated client.
