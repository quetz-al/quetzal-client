=========
Changelog
=========

This document list all important changes to quetzal-client.

Quetzal-client version numbers follow `semantic versioning <http://semver.org>`_.

0.5.1 (2020-02-27)
------------------

* Fix problem with API key authentication when requesting file details.
* Fix API key management on configuration object.
* Fix lack of default format on CLI for file metadata.
* Add file delete CLI.

0.5.0 (2019-10-17)
------------------

* Update to API version 0.5.0.
* Add API key authentication.

0.3.0 (2019-07-02)
------------------

* Update to API version 0.3.0.
* Add more helper functions (query and client).
* Fix incorrect call to derived configuration object.
* Fix unpickeable exception types.
* Fix bugs on file download checksum verification and file upload parameters.

0.2.0 (2019-03-21)
------------------

* Update dependency *quetzal-openapi-client* to match Quetzal API version 0.2.0.
* Fix ``dependency_links`` to correctly link to *quetzal-openapi-client*.

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
