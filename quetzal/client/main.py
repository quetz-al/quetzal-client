import click

from quetzal.client.autogen import (
    ApiClient, AuthenticationApi, Configuration, DataApi
)
from quetzal.client.autogen.rest import ApiException


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
    client = ctx.obj['client']
    api = AuthenticationApi(client)
    try:
        response = api.app_api_auth_get_token()
    except ApiException as ex:
        raise click.ClickException(f'Invalid credentials. Error {ex.status}')

    ctx.obj['configuration'].access_token = response.token


@auth.command()
def logout():
    pass


@cli.group()
@click.argument('name')
@click.pass_context
def workspace(ctx, name):
    """Workspace operations"""
    print(f'Getting information of workspace {name}')
    ctx.forward(login)

    client = ctx.obj['client']
    api = DataApi(client)
    response = api.app_api_data_workspace_fetch(name=name)
    print(response)


@workspace.command(name='list')
@click.pass_context
def list_(ctx):
    ctx.forward(login)

    client = ctx.obj['client']
    api = DataApi(client)

    print(f'{"id":>6} {"status":>10} {"name":>20} {"families":>20} {"data_url":>32} {"owner":>12}'.upper())
    response = api.app_api_data_workspace_fetch()
    for w in response.data:
        families = ', '.join(f'{k}:{v}' for k, v in sorted(w.families.items()))
        print(f'{w.id:>6} {w.status:>10} {w.name:>20} {families:>20} {w.data_url:>32} {w.owner:>12}')


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
