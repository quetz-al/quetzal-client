import click

from quetzal.client.cli import BaseGroup, help_options, pass_state, error_wrapper


@click.group('auth', options_metavar='[AUTH OPTIONS]', cls=BaseGroup)
@help_options
def auth_group():
    """Authentication operations."""
    pass


@auth_group.command()
@error_wrapper
@help_options
@pass_state
def login(state):
    config = state.api_config
    client = state.api_client
    if not config.username:
        raise click.ClickException('Cannot login without username credentials')

    response = client.auth_get_token()

    # Manage success: save the access token
    client.configuration.access_token = response.token
    if config.username:
        click.secho(f'Logged in with user {config.username} successful!', fg='green')
    else:
        click.secho(f'Logged in access token successful!', fg='green')


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
