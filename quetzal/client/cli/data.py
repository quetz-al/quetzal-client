import datetime
import itertools

import backoff
import click

from quetzal.client.cli import (
    BaseGroup, FamilyVersionListType,
    help_options, MutexOption, pass_state
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
@click.option('--name', help='Filter workspaces with this name only.')
@click.option('--owner', default=None, help='Filter only workspace owned by this user.')
@click.option('--include-deleted', 'deleted', is_flag=True, show_default=True,
              help='Include deleted workspaces.')
@click.option('--limit', type=click.INT, default=10, show_default=True,
              help='Limit the number of workspaces.')
@help_options
@pass_state
def fetch(state, name, owner, deleted, limit):
    """List workspaces"""
    client = state.api_client

    kwargs = dict(per_page=10)
    if name:
        kwargs['name'] = name
    if owner:
        kwargs['owner'] = owner
    if deleted:
        kwargs['deleted'] = True

    fetch_result = client.data_workspace_fetch(**kwargs)
    results = [w.to_dict() for w in fetch_result.data]
    while len(results) < limit and len(results) < fetch_result.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        fetch_result = client.data_workspace_fetch(**kwargs)
        results.extend([w.to_dict() for w in fetch_result.data])

    columns = {
        'id': {'head': 'ID', 'width': 19, 'align': '^'},
        'name': {'head': 'NAME', 'width': 64, 'align': '^'},
        'status': {'head': 'STATUS', 'width': 11, 'align': '^'},
        'owner': {'head': 'OWNER', 'width': 64, 'align': '^'},
        'description': {'head': 'DESCRIPTION', 'width': 32, 'align': '>'},
        'creation_date': {'head': 'CREATED AT', 'width': 19, 'align': '^'},
        'data_url': {'head': 'DATA_URL', 'width': 64, 'align': '>'}
    }

    max_width = dict()

    for row in results:
        for k in row:
            if isinstance(row[k], datetime.datetime):
                str_k = row[k].strftime('%Y-%m-%d %H:%M:%S')
            else:
                str_k = str(row[k])
            max_k = columns.get(k, {}).get('width', 100)
            row[k] = _trim_string(str_k, max_k)
            max_width[k] = max(max_width.get(k, 0), len(str_k))

    row_format = '    '.join(
        '{' + ('{name}:{align}{max_width}'.format(name=c, max_width=min(max_width[c], columns[c]['width']), **columns[c])) + '}'
        for c in columns)

    term_width, _ = click.get_terminal_size()
    header = {k:columns[k]['head'] for k in columns}
    head_line = _trim_string(row_format.format(**header), term_width)
    click.secho(head_line, fg='blue')

    for row in results:
        row_line = _trim_string(row_format.format(**row), term_width)
        click.echo(row_line)

    click.secho(f'\nShowed {len(results)} out of {fetch_result.total} workspaces', fg='green')


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
@click.option('--name', cls=MutexOption, not_required_if=['wid'])
@click.option('--id', 'wid',type=click.INT, cls=MutexOption, not_required_if=['name'],
              help='Identifier of the workspace to delete')
@click.confirmation_option(prompt='This will delete the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is initialized.')
@help_options
@pass_state
def delete(state, name, wid, wait):
    """Delete a workspace"""
    client = state.api_client
    username = state.api_config.username
    if not username:
        raise click.ClickException('Cannot delete workspace without an username')

    # Get the workspace details
    try:
        if name:
            response = client.data_workspace_fetch(owner=username, name=name)
            w_details = response.data[0]
        else:
            w_details = client.data_workspace_details(wid)
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
        click.secho(f'\nWorkspace [{w_details.name}] deleted successfully!', fg='green')
        _print_details(w_details)

    else:
        click.secho(f'\nWorkspace [{w_details.name}] was marked for deletion.', fg='green')

    return w_details


def _print_details(w):
    click.secho('Workspace details:', fg='blue')
    for field in ('id', 'name', 'status', 'description', 'temporary', 'owner'):
        click.secho(f'  {field}: ', fg='blue', nl=False)
        click.secho(str(w.to_dict()[field]))
    click.secho('  families:', fg='blue')
    click.secho('\n'.join(f'    {k}: {v}' for k, v in w.families.items()))


def _trim_string(string, width):
    if len(string) > width:
        return string[:width-3] + '...'
    return string
