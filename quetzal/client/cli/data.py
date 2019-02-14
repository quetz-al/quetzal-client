import itertools

import backoff
import click

from quetzal.client.cli import (
    BaseGroup, FamilyVersionListType,
    help_options, pass_state
)
from quetzal.client.exceptions import QuetzalAPIException


def wait_for_workspace(w, client, func):

    roll_map = itertools.cycle(r'\|/-')

    @backoff.on_predicate(backoff.constant, func, interval=1)
    def poll():
        w_details = client.data_workspace_details(w.id)
        print(f'\rWaiting for workspace {w_details.id} {w_details.name} '
              f'[{w_details.status}] ... {next(roll_map)}',
              sep='', end='')
        return w_details

    return poll()


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
        w_details = client.data_workspace_create(workspace_create_object)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to create workspace\n{ex}')

    if wait:
        w_details = wait_for_workspace(w_details, client,
                                       lambda w: w.status == 'INITIALIZING')

    click.secho('\nWorkspace created successfully!', fg='green')
    _print_details(w_details)

    return w_details


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


@workspace.command()
@click.argument('name')
@click.confirmation_option(prompt='This will delete the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is initialized.')
@help_options
@pass_state
def delete(state, name, wait):
    """Delete a workspace"""
    client = state.api_client
    username = state.api_config.username
    if not username:
        raise click.ClickException('Cannot delete workspace without an username')

    # Get the workspace details
    try:
        response = client.data_workspace_fetch(owner=username, name=name)
        w_details = response.data[0]
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to retrieve workspace:\n{ex}')


    # Delete it
    try:
        client.data_workspace_delete(w_details.id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to delete workspace:\n{ex}')

    if wait:
        w_details = wait_for_workspace(w_details, client,
                                       lambda w: w.status == 'DELETING')

    click.secho('\nWorkspace deleted successfully!', fg='green')
    _print_details(w_details)

    return w_details


def _print_details(w):
    click.secho('Workspace details:', fg='blue')
    for field in ('id', 'name', 'status', 'description', 'temporary', 'owner'):
        click.secho(f'  {field}: ', fg='blue', nl=False)
        click.secho(str(w.to_dict()[field]))
    click.secho('  families:', fg='blue')
    click.secho('\n'.join(f'    {k}: {v}' for k, v in w.families.items()))
