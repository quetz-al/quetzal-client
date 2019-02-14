import datetime
import itertools
import sys

import backoff
import click

from quetzal.client.cli import (
    BaseGroup, FamilyVersionListType,
    help_options, OneRequiredOption, pass_state
)
from quetzal.client.exceptions import QuetzalAPIException
from quetzal.client.utils import HistoryConsole


def name_option(f):
    return click.option('--name', cls=OneRequiredOption, one_of_with=['id'],
                        help='Workspace name.')(f)


def id_option(f):
    return click.option('--id', cls=OneRequiredOption, one_of_with=['name'],
                        help='Workspace identifier.')(f)


def workspace_identifier_options(f):
    f = id_option(f)
    f = name_option(f)
    return f


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
        w_details = _wait_for_workspace(w_details, client,
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

    kwargs = dict(per_page=min(limit, 100))
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
        'data_url': {'head': 'DATA_URL', 'width': 64, 'align': '>'},
        'families': {'head': 'FAMILIES', 'width': 64, 'align': '>'}
    }

    max_width = {k: len(k) for k in columns}

    for row in results:
        for k in row:
            if k not in columns:
                continue
            if isinstance(row[k], datetime.datetime):
                str_k = row[k].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(row[k], dict):
                str_k = ', '.join(f'{k}:{v}' for k, v in row[k].items())
            else:
                str_k = str(row[k])
            str_k = str_k or 'empty'
            max_k = columns.get(k, {}).get('width', 100)
            row[k] = _trim_string(str_k, max_k)

            max_width[k] = max(max_width[k], len(str_k))

    row_format = '    '.join(
        '{' + ('{name}:{align}{max_width}'.format(name=c, max_width=min(max_width[c], columns[c]['width']), **columns[c])) + '}'
        for c in columns)

    term_width, _ = click.get_terminal_size()
    header = {k: columns[k]['head'] for k in columns}
    head_line = _trim_string(row_format.format(**header), term_width)
    click.secho(head_line, fg='blue')

    for row in results:
        row_line = _trim_string(row_format.format(**row), term_width)
        click.echo(row_line)

    click.secho(f'\nShowing {len(results)} out of {fetch_result.total} workspaces', fg='green')


@workspace.command()
@workspace_identifier_options
@help_options
@pass_state
def details(state, name, id):
    """Show workspace details"""

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
            w_details = client.data_workspace_details(id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to retrieve workspace:\n{ex}')

    _print_details(w_details)


@workspace.command()
@workspace_identifier_options
@click.confirmation_option(prompt='This will commit the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def commit(state, name, id, wait):
    """Commit a workspace"""

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
            w_details = client.data_workspace_details(id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to retrieve workspace:\n{ex}')

    # Do the commit
    try:
        client.data_workspace_commit(w_details.id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to commit workspace:\n{ex}')

    if wait:
        w_details = _wait_for_workspace(w_details, client,
                                        lambda w: w.status == 'COMMITTING')
        click.secho(f'\nWorkspace [{w_details.name}] committed successfully!', fg='green')
        _print_details(w_details)

    else:
        click.secho(f'\nWorkspace [{w_details.name}] was marked for committing.', fg='green')

    return w_details


@workspace.command()
@workspace_identifier_options
@click.confirmation_option(prompt='This will update the workspace views. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def scan(state, name, id, wait):
    """Scan a workspace"""

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

    # Do the scan
    try:
        client.data_workspace_scan(w_details.id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to scan workspace:\n{ex}')

    if wait:
        w_details = _wait_for_workspace(w_details, client,
                                        lambda w: w.status == 'SCANNING')
        click.secho(f'\nWorkspace [{w_details.name}] scanned successfully!', fg='green')
        _print_details(w_details)

    else:
        click.secho(f'\nWorkspace [{w_details.name}] was marked for scanning.', fg='green')

    return w_details


@workspace.command()
@workspace_identifier_options
@click.option('--query', type=click.File('r'), help='Input query file',
              default=sys.stdin)
@click.option('--dialect', default='postgresql', show_default=True,
              help='Dialect of query')
@click.option('--limit', type=click.INT, default=10, show_default=True,
              help='Limit the number of workspaces.')
@click.option('--output', '-o', type=click.File('w'),
              help='File where query results will be saved.')
@help_options
@pass_state
def query(state, name, id, query, dialect, limit, output):
    """Query a workspace"""

    if query.isatty():
        console = HistoryConsole()
        lines_read = []
        line = True
        print('Write your query followed by an empty line: ',
              file=sys.stderr)
        while line:
            line = console.raw_input()
            lines_read.append(line)
        query_contents = '\n'.join(lines_read)
    else:
        query_contents = query.read()

    print('Query:', query_contents)


@workspace.command()
@workspace_identifier_options
@click.confirmation_option(prompt='This will delete the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is deleted.')
@help_options
@pass_state
def delete(state, name, id, wait):
    """Delete a workspace"""

    client = state.api_client
    username = state.api_config.username
    if not username:
        raise click.ClickException('Cannot delete workspace without an username.')

    # Get the workspace details
    try:
        if name:
            response = client.data_workspace_fetch(owner=username, name=name)
            w_details = response.data[0]
        else:
            w_details = client.data_workspace_details(id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to retrieve workspace:\n{ex}')

    # Delete it
    try:
        client.data_workspace_delete(w_details.id)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to delete workspace:\n{ex}')

    if wait:
        w_details = _wait_for_workspace(w_details, client,
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


def _wait_for_workspace(w, client, func):

    roll_map = itertools.cycle(r'\|/-')

    @backoff.on_predicate(backoff.constant, func, interval=1)
    def poll():
        w_details = client.data_workspace_details(w.id)
        print(f'\rWaiting for workspace {w_details.id} {w_details.name} '
              f'[{w_details.status}] ... {next(roll_map)}',
              sep='', end='')
        return w_details

    return poll()
