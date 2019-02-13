import click

from quetzal.client.cli import (
    BaseGroup, FamilyVersionListType,
    help_options, pass_state, State
)
from quetzal.client.exceptions import QuetzalAPIException



@click.group(options_metavar='[DATA OPTIONS]')
@help_options
def data(*args, **kwargs):
    """Data operations"""
    pass


@data.group(options_metavar='[WORKSPACE OPTIONS]', cls=BaseGroup)
@help_options
def workspace(*args, **kwargs):
    """Workspace operations"""
    pass


@workspace.command()
@click.argument('name')
@click.option('--description', help='Workspace description.', default='', show_default=True)
@click.option('--families', '-f', type=FamilyVersionListType(),
              metavar='name:version,... ',
              default='base:latest',
              show_default=True,
              help='List of family names and version numbers to use in this '
                   'workspace, separated by commas. Version number can be '
                   '"latest", which means the most recent version available.')
@click.option('--wait', is_flag=True, help='Wait until the workspace is initialized.')
@help_options
@pass_state
def create(state, name, description, families, wait):
    """Create a workspace"""
    client = state.api_client
    workspace_create_object = {
        "name": name,
        "description": description,
        "families": {tup[0]:tup[1] for tup in families}
    }
    try:
        response = client.data_api.app_api_data_workspace_create(workspace_create_object)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to create workspace\n{ex}')
    # if not wait:
    #     return response
    print(response)


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
