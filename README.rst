.. Note that this file is included on Sphinx as well.

Quetzal Python client
=====================

Python client for the Quetzal API.

If you are not familiar with the Quetzal API, read its
`documentation <https://quetzal-api.readthedocs.org>`_ first. This Python
package provides a command-line and helper functions to interact with the
Quetzal API.

Note that this package depends on an auto-generated package
`quetzal.openapi_client <https://github.com/quetz-al/quetzal-openapi-client>`_,
which is also a client to this API. You can use the latter as a pure Python
client, but *quetzal.client* provides some helpers and small fixes.

Installation
------------

You can install *quetzal-client*, with ``pip``:

.. code-block:: console

    pip install quetzal-client

Alternatively, add this line to your ``requirements.txt``:

.. code-block:: none

    quetzal-client

and then do ``pip install -r requirements.txt``.

If you are using conda, add the following structure to your ``environment.yaml``:

.. code-block:: yaml

    ...
    dependencies:
      - pip
      - pip:
        - quetzal-client

and create or update your environment with
``conda env create -f environment.yaml`` or
``conda env update -f environment.yaml``, respectively.


Getting started
---------------

In order to use *quetzal.client*, you need to know the URL of the API server,
your username and password. You can set these on the command-line interface,
through a configuration object, or using environment variables:

.. list-table:: Environment variables considered by `quetzal-client`.
   :header-rows: 1

   * - Variable
     - Description
     - Default if not set
   * - ``QUETZAL_URL``
     - Complete URL of the Quetzal server + API version.
     - ``'https://api.quetz.al/api/v1'``
   * - ``QUETZAL_USER``
     - Quetzal username.
     - ``''``
   * - ``QUETZAL_PASSWORD``
     - Quetzal password.
     - ``''``


Basic usage
-----------

There are two ways this package helps you: with a command-line interface or by
providing some helper modules that you can use in Python.

Command-line interface
^^^^^^^^^^^^^^^^^^^^^^

The command-line interface is available through the ``quetzal-client`` command.
Use the ``--help`` or ``--help-all`` options to get a detailed description of
each command.

.. code-block:: console

    $ quetzal-client --help

    Usage: quetzal-client [GLOBAL OPTIONS] COMMAND [ARGS]...

      Command-line utility for the Quetzal API client.

    Options:
      --url TEXT       Quetzal URL. If not set, uses environment variable
                       QUETZAL_URL if this variable is defined.  [default:
                       https://staging.quetz.al/api/v1]
      --insecure       Do not verify HTTPS certificates.
      --username TEXT  Quetzal username. If not set, uses environment variable
                       QUETZAL_USER. Option is mutually exclusive with token.
      --password TEXT  Quetzal password. If not set, uses environment variable
                       QUETZAL_PASSWORD. Option is mutually exclusive with token.
      --token TEXT     Quetzal access token. If not set, uses environment variable
                       QUETZAL_TOKEN. Option is mutually exclusive with username,
                       password.
      -v, --verbose    Verbosity level. Use -v for verbose, -vv for even more
                       verbosity
      --help-all       Show a detailed help message with all options and exit.
      --help           Show help message for this command and exit.
      --version        Show the version and exit.

    Commands:
      auth       Authentication operations.
      file       File operations.
      query      Query metadata.
      workspace  Workspace operations.


Python
^^^^^^

To start using *quetzal.client* on Python code, use the following template:

.. code-block:: python

    from quetzal.client import Client, Configuration, QuetzalAPIException
    from quetzal.client import helpers

    config = Configuration()
    # ... change config as needed or fallback to the environment variables ...
    # config.verify_ssl = False  # Use this for servers without certificates (dev servers)
    client = Client(config)

    # A simple test using the helpers to verify that we can login to Quetzal
    try:
        helpers.auth.login(client)
        print('Logged in successfully!')
    except QuetzalAPIException as ex:
        print(f'Operation failed. {ex.title} - {ex.detail}')


Documentation
-------------

There are more details on *quetzal.client* on its official documentation at
`readthedocs <https://quetzal-client.readthedocs.io/en/latest/>`_.



Contribute
----------

- Issue Tracker: https://github.com/quetz-al/quetzal-client/issues
- Source Code: https://github.com/quetz-al/quetzal-client


License
-------

The project is under the BSD 3-clause license.
