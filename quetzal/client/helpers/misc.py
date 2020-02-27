import urllib3

from quetzal.client import Client, Configuration


def get_client(url=None, username=None, password=None, insecure=False, api_key=None):
    """ Get a Quetzal client instance.

    Prepares a :py:ref:`quetzal.client.Client` instance with the provided
    credentials.

    Parameters
    ----------
    url: str
        URL of the Quetzal API.
    username: str
        Quetzal API username. Do not use with api_key.
    password: str
        Quetzal API password. Do not use with api_key.
    insecure: bool, optional
        When ``False``, disables SSL verification of the HTTPS certificate.
    api_key: str, optional
        Quetzal API key. Do not use with username or password.

    Returns
    -------
    quetzal.client.Client
        A Quetzal API client instance.

    """
    config = Configuration()
    config.host = url or config.host
    config.username = username or config.username
    config.password = password or config.password
    if api_key is not None:
        config.api_key['X-API-KEY'] = api_key
    if insecure:
        config.verify_ssl = False
        # Mute urllib3 warnings
        urllib3.disable_warnings()
    client = Client(config)
    return client
