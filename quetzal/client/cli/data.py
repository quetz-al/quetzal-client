import click

from quetzal.client.cli import help_options, State
from quetzal.client.cli.auth import login, logout


@click.group(options_metavar='[DATA OPTIONS]')
@help_options
def data(*args, **kwargs):
    """Data operations"""
    pass


@data.group(options_metavar='[WORKSPACE OPTIONS]')
@help_options
def workspace(*args, **kwargs):
    """Workspace operations"""
    pass

#workspace = click.Group(name='workspace', help='Workspace operations.')

# @click.argument('name')
# @click.pass_context
# def workspace(ctx, name):
#     """Workspace operations"""
#     print(forkspace {name}')
    # ctx.forward(login)
    #
    # client = ctx.obj['client']
    # user = ctx.obj['user']
    # api = DataApi(client)
    # response = api.app_api_data_workspace_fetch(name=name, owner=user)
    # if not response.data:
    #     raise click.ClickException(f'Workspace "{name}" not found')
    # ctx.obj['workspace'] = response.data[0]


@workspace.command(name='list')
@help_options
@click.pass_context
def fetch(ctx):
    # ctx.forward(logout)
    # client = ctx.obj['client']
    # api = DataApi(client)
    # import ipdb; ipdb.set_trace(context=21)
    #
    # print(f'{"id":>6} {"status":>10} {"name":>20} {"families":>20} {"data_url":>32} {"owner":>12}'.upper())
    # try:
    #     response = api.app_api_data_workspace_fetch()
    #     for w in response.data:
    #         families = ', '.join(f'{k}:{v}' for k, v in sorted(w.families.items()))
    #         print(f'{w.id:>6} {w.status:>10} {w.name:>20} {families:>20} {w.data_url:>32} {w.owner:>12}')
    #
    # except ApiException as ex:
    #     print(ex)
    pass


@workspace.command()
@help_options
def details():
    pass


@workspace.command()
@click.confirmation_option()
@help_options
@click.pass_context
def commit(ctx):
    print('committing', ctx.obj)


@workspace.command()
@click.confirmation_option()
@help_options
def scan():
    pass


@workspace.command()
@help_options
def upload():
    pass
