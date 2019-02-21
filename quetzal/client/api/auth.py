import click

from quetzal.client.cli import BaseGroup, help_options, pass_state, error_wrapper


def login(client):
    """ Login a API client object.

    This function calls the auth/token endpoint in order to obtain an
    authentication bearer token. It changes _in place_ the `client` to update
    its access token configuration.

    Parameters
    ----------
    client: quetzal.client.Client
        Client object that will be used to authenticate. Its configuration
        will be updated according to the results.

    Returns
    -------
    None

    Raises
    ------
    quetzal.client.exceptions.QuetzalAPIException
        When the API returns an error.

    """
    response = client.auth_get_token()
    # Manage success: save the access token
    client.configuration.access_token = response.token


# TODO: continue here creating the api objects?
@auth_group.command()
@error_wrapper
@help_options
@pass_state
def logout(state):
    config = state.api_config
    client = state.api_client
    if not config.access_token:
        if not config.username or not config.password:
            raise click.ClickException('Cannot logout without access_token or credentials')

    client.auth_logout()
    click.secho('Access token revoked: logout successful', fg='green')
