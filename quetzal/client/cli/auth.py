import getpass

import click

from quetzal.client.cli import help_options, pass_state
from quetzal.client.api_client import UnauthorizedException


@click.group(options_metavar='[AUTH OPTIONS]')
@help_options
def auth(**kwargs):
    """Authentication operations"""
    pass


@auth.command()
@help_options
@pass_state
def login(state):
    config = state.api_config
    client = state.api_client
    if not config.username:
        raise click.ClickException('Cannot login without username credentials')
    try:
        response = client.auth_api.app_api_auth_get_token()
    except UnauthorizedException:
        raise click.ClickException('Incorrect user or password')

    # Manage success: save the access token
    client.configuration.access_token = response.token
    if config.username:
        click.secho(f'Logged in with user {config.username} successful!', fg='green')
    else:
        click.secho(f'Logged in access token successful!', fg='green')


@auth.command()
@help_options
@pass_state
@click.pass_context
def logout(ctx, state):
    config = state.api_config
    client = state.api_client
    if not config.access_token:
        if not config.username or not config.password:
            raise click.ClickException('Cannot logout without access_token or credentials')
        ctx.invoke(login)

    client.auth_api.app_api_auth_logout()
    click.secho('Access token revoked: logout successful', fg='green')
