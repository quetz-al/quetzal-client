import datetime
import itertools
import json
import pathlib
import sys

import backoff
import click
import yaml


from quetzal.client.cli import (
    BaseGroup, error_wrapper, FamilyVersionListType,
    help_options, MutexOption, OneRequiredOption, pass_state,
    rename_kwargs, State
)
from quetzal.client.exceptions import QuetzalAPIException
from quetzal.client.utils import HistoryConsole


def name_option(required=True):
    extra_kwargs = {}
    if required:
        extra_kwargs['cls'] = OneRequiredOption
        extra_kwargs['one_of_with'] = ['id']

    def decorator(f):
        def callback(ctx, param, value):
            if value and not ctx.resilient_parsing:
                state = ctx.ensure_object(State)
                if not state.api_config.username:
                    raise click.BadOptionUsage(
                        param,
                        'Using --name to refer to a workspace requires a '
                        'the --username options to be set because the workspace '
                        'is uniquely identified by the name and username.',
                        ctx=ctx)
                return value

        return click.option('--name', callback=callback, help='Workspace name.',
                            **extra_kwargs)(f)

    return decorator


def id_option(required=True):
    extra_kwargs = {}
    if required:
        extra_kwargs['cls'] = OneRequiredOption
        extra_kwargs['one_of_with'] = ['name']

    def decorator(f):
        return click.option('--id', help='Workspace identifier.',
                            **extra_kwargs)(f)

    return decorator


def workspace_identifier_options(required=True):

    def decorator(f):
        f = id_option(required)(f)
        f = name_option(required)(f)
        f = rename_kwargs(wid='id')(f)
        return f

    return decorator


@click.group('workspace', options_metavar='[WORKSPACE OPTIONS]', cls=BaseGroup)
@help_options
def workspace():
    """Workspace operations"""
    pass


@workspace.command()
@error_wrapper
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
    w_details = client.workspace_create(workspace_create_object)

    if wait:
        w_details = _wait_for_workspace(w_details, client,
                                        lambda w: w.status == 'INITIALIZING')

    click.secho('\nWorkspace created successfully!', fg='green')
    _print_details(w_details)

    return w_details


@workspace.command(name='list')
@error_wrapper
@click.option('--name', help='Filter workspaces with this name only.')
@click.option('--owner', default=None, help='Filter only workspace owned by this user.')
@click.option('--include-deleted', 'deleted', is_flag=True, show_default=True,
              help='Include deleted workspaces.')
@click.option('--limit', type=click.INT, default=10, show_default=True,
              help='Limit the number of workspaces.')
@help_options
@pass_state
def list_(state, name, owner, deleted, limit):
    """List workspaces"""
    client = state.api_client

    kwargs = dict(per_page=min(limit, 100))
    if name:
        kwargs['name'] = name
    if owner:
        kwargs['owner'] = owner
    if deleted:
        kwargs['deleted'] = True

    fetch_result = client.workspace_fetch(**kwargs)
    results = [w.to_dict() for w in fetch_result.results]
    while len(results) < limit and len(results) < fetch_result.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        fetch_result = client.workspace_fetch(**kwargs)
        results.extend([w.to_dict() for w in fetch_result.results])

    if not results:
        click.secho('No workspaces found.', fg='green')
        return

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
    _print_table(results, columns, fetch_result.total)


@workspace.command()
@workspace_identifier_options()
@help_options
@pass_state
def details(state, name, wid):
    """Show workspace details"""
    w_details = _get_details(state, name, wid)

    _print_details(w_details)


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will commit the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def commit(state, name, wid, wait):
    """Commit a workspace"""

    client = state.api_client

    # Get the workspace details
    w_details = _get_details(state, name, wid)

    # Do the commit
    try:
        client.workspace_commit(w_details.id)
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
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will update the workspace views. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def scan(state, name, wid, wait):
    """Scan a workspace"""

    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    # Do the scan
    client.workspace_scan(w_details.id)

    if wait:
        w_details = _wait_for_workspace(w_details, client,
                                        lambda w: w.status == 'SCANNING')
        click.secho(f'\nWorkspace [{w_details.name}] scanned successfully!', fg='green')
        _print_details(w_details)

    else:
        click.secho(f'\nWorkspace [{w_details.name}] was marked for scanning.', fg='green')

    return w_details


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--query', 'query_file', type=click.File('r'),
              help='Input query file', default=sys.stdin)
@click.option('--dialect', default='postgresql', show_default=True,
              help='Dialect of query')
@click.option('--limit', type=click.INT, default=10, show_default=True,
              cls=MutexOption, not_required_if=['all'],
              help='Limit the number of results.')
@click.option('--all', is_flag=True, cls=MutexOption, not_required_if=['limit'],
              help='Get all results.')
@click.option('--output', '-o', type=click.File('w'),
              help='File where query results will be saved.')
@click.option('--format', 'output_format',
              type=click.Choice(['csv', 'json', 'yaml']),
              help='Output file format, if not set, it is guessed from the extension.')
@rename_kwargs(retrieve_all='all')
@help_options
@pass_state
def query(state, name, wid, query_file, dialect, limit, retrieve_all, output, output_format):
    """Query a workspace"""

    if output_format is None:
        if hasattr(output, 'name'):
            output_filename = pathlib.Path(output.name)
            ext = output_filename.suffix[1:]
            if ext not in ('csv', 'json', 'yaml'):
                raise click.BadParameter(f'No format provided: "{ext}" is not supported. '
                                         f'Set the format with --format')
            output_format = ext

    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    if query_file.isatty():
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
        query_contents = query_file.read()

    limit = sys.maxsize if retrieve_all else min(limit, 100)
    kwargs = dict(per_page=limit)

    query_obj = {
        'dialect': dialect,
        'query': query_contents,
    }

    query_details = client.workspace_query_create(w_details.id, query_obj, **kwargs)
    results = query_details.results
    if not results:
        _save_results([], output, output_format)
        click.secho('No results.', fg='green')
        return

    # The query POST action redirects to the GET details but does not have
    # a per_page, so we might get more that we needed
    if len(results) > limit:
        results = results[:limit]

    while len(results) < limit and len(results) < query_details.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        query_details = client.workspace_query_details(w_details.id, query_details.id, **kwargs)
        results.extend(query_details.results)

    total_width, _ = click.get_terminal_size()
    num_cols = len(results[0])
    columns = {
        col: {'head': col, 'width': total_width // num_cols - 1, 'align': '>'}
        for col in results[0].keys()
    }

    if output is None:
        _print_table(results, columns, query_details.total)
    else:
        _save_results(results, output, output_format)
        click.secho(f'Saved {len(results)} out of {query_details.results.total} results '
                    f'in {output.name}.')


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--limit', type=click.INT, default=10, show_default=True,
              help='Limit the number of results.')
@help_options
@pass_state
def files(state, name, wid, limit):
    """List files on a workspace"""
    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    kwargs = dict(per_page=min(limit, 100))

    fetch_result = client.workspace_file_fetch(w_details.id, **kwargs)
    results = [r.to_dict() for r in fetch_result.results]
    while len(results) < limit and len(results) < fetch_result.total:
        kwargs['page'] = kwargs.get('page', 1) + 1
        fetch_result = client.workspace_file_fetch(w_details.id, **kwargs)
        results.extend([r.to_dict() for r in fetch_result.results])

    if not results:
        click.secho('No files have been added on this workspace '
                    '(no metadata modifications either).',
                    fg='green')
        return

    columns = {
        'id': {'head': 'ID', 'width': 36, 'align': '^'},
        'path': {'head': 'PATH', 'width': 32, 'align': '>'},
        'filename': {'head': 'FILENAME', 'width': 32, 'align': '>'},
        'size': {'head': 'SIZE', 'width': 50, 'align': '>'},
    }
    _print_table(results, columns, fetch_result.total)


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--file', '-f', type=click.File(mode='rb'), required=True,
              help='File to upload.')
@help_options
@pass_state
def upload(state, name, wid, file):
    """Upload a file to a workspace."""
    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    file_details = client.workspace_file_create(w_details.id, file_content=file.name)
    click.secho(f'File {file.name} uploaded successfully. Its id is {file_details.id}.',
                fg='green')


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will delete the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is deleted.')
@help_options
@pass_state
def delete(state, name, wid, wait):
    """Delete a workspace"""

    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    # Delete it
    client.workspace_delete(w_details.id)

    if wait:
        w_details = _wait_for_workspace(w_details, client,
                                        lambda w: w.status == 'DELETING')
        click.secho(f'\nWorkspace [{w_details.name}] deleted successfully!', fg='green')
        _print_details(w_details)

    else:
        click.secho(f'\nWorkspace [{w_details.name}] was marked for deletion.', fg='green')

    return w_details


@workspace.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--file-id', required=True,
              help='File identifier whose metadata will be updated.')
@click.option('--metadata-file', type=click.File('r'),
              help='JSON file with metadata.')
@help_options
@pass_state
def update_metadata(state, name, wid, file_id, metadata_file):
    """Update the metadata of a file in a workspace"""

    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    metadata_contents = json.load(metadata_file)
    response = client.workspace_file_update_metadata(wid=w_details.id, uuid=file_id,
                                                     body=metadata_contents)
    click.secho(f'Metadata for file {file_id} successfully changed.', fg='green')
    click.secho('Updated metadata:')
    click.secho(json.dumps(response, indent=2), fg='blue')


def _wait_for_workspace(w, client, func):

    roll_map = itertools.cycle(r'\|/-')

    @backoff.on_predicate(backoff.constant, func, interval=1)
    def poll():
        w_details = client.workspace_details(w.id)
        print(f'\rWaiting for workspace {w_details.id} {w_details.name} '
              f'[{w_details.status}] ... {next(roll_map)}',
              sep='', end='')
        return w_details

    return poll()


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


def _print_table(results, schema, total):
    max_width = {k: len(k) for k in schema}

    for row in results:
        for k in row:
            if k not in schema:
                continue
            if isinstance(row[k], datetime.datetime):
                str_k = row[k].strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(row[k], dict):
                str_k = ', '.join(f'{k}:{v}' for k, v in row[k].items())
            else:
                str_k = str(row[k])
            #str_k = str_k or 'empty'
            max_k = schema.get(k, {}).get('width', 100)
            row[k] = _trim_string(str_k, max_k)

            max_width[k] = max(max_width[k], len(str_k))

    row_format = '    '.join(
        '{' + ('{name}:{align}{max_width}'.format(name=c, max_width=min(max_width[c], schema[c]['width']), **schema[c])) + '}'
        for c in schema)

    term_width, _ = click.get_terminal_size()
    header = {k: schema[k]['head'] for k in schema}
    head_line = _trim_string(row_format.format(**header), term_width)
    click.secho(head_line, fg='blue')

    for row in results:
        row_line = _trim_string(row_format.format(**row), term_width)
        click.echo(row_line)

    click.secho(f'\nShowing {len(results)} out of {total} results.', fg='green')


def _save_results(table, file, fmt):
    if file is None:
        return

    if fmt == 'json':
        json.dump(table, file, indent=2)
    elif fmt == 'yaml':
        yaml.safe_dump(table, file, default_flow_style=False)
    elif fmt == 'csv':
        raise NotImplementedError
    else:
        raise ValueError('Invalid output format')


def _get_details(state, name, wid):
    client = state.api_client
    try:
        if name:
            username = state.api_config.username
            response = client.workspace_fetch(owner=username, name=name)
            if not response.results:
                raise click.ClickException('Workspace not found.')
            w_details = response.results[0]
        else:
            w_details = client.workspace_details(wid)
    except QuetzalAPIException as ex:
        raise click.ClickException(f'Failed to retrieve workspace:\n{ex}')
    return w_details
