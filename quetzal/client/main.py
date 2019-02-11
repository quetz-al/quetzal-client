import click

from quetzal_client import (
    ApiClient, AuthenticationApi, Configuration, DataApi
)
from quetzal_client.rest import ApiException


@click.group()
@click.option('--url', help='URL of Quetzal server')
@click.option('--username', help='Username for the Quetzal API', required=True)
@click.password_option(confirmation_prompt=False, help='Password for the Quetzal API')
@click.option('--debug', is_flag=True, help='Turn on verbose debug logging')
@click.pass_context
def cli(ctx, url, username, password, debug):

    config = Configuration()
    config.username = username
    config.password = password
    config.host = url or config.host
    config.debug = debug

    ctx.ensure_object(dict)
    ctx.obj['configuration'] = config


@cli.group()
def auth():
    """Authentication operations"""
    pass


@auth.command()
@click.pass_context
def login(ctx, *args, **kwargs):
    if 'client' not in ctx.obj:
        client = ApiClient(ctx.obj['configuration'])
        ctx.obj['client'] = client
    api = AuthenticationApi(client)
    try:
        response = api.app_api_auth_get_token()
    except ApiException as ex:
        raise click.ClickException(f'Invalid credentials. Error {ex.status}')

    ctx.obj['configuration'].api_key = response.token
    ctx.obj['configuration'].api_key_prefix = 'Bearer'


@auth.command()
def logout():
    pass


@cli.group()
@click.argument('name')
@click.pass_context
def workspace(ctx, name):
    """Workspace operations"""
    print(f'Getting information of workspace {name}')
    import ipdb; ipdb.set_trace(context=21)
    ctx.forward(login)

    client = ctx.obj['client']
    api = DataApi(client)
    response = api.app_api_data_workspace_fetch(name=name)
    print(response)


@workspace.command(name='list')
def list_():
    pass


@workspace.command()
def details():
    pass


@workspace.command()
@click.confirmation_option()
@click.pass_context
def commit(ctx):
    print('commiting', ctx.obj)


@workspace.command()
def scan():
    pass


@workspace.command()
def upload():
    pass


def main():
    return cli()


if __name__ == '__main__':
    main()
