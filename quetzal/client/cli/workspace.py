import datetime
import csv
import itertools
import json

import backoff
import click
import yaml


from quetzal.client import helpers
from quetzal.client.cli import (
    BaseGroup, error_wrapper, FamilyVersionListType,
    help_options, OneRequiredOption, MutexOption, pass_state,
    rename_kwargs, State, _progress
)
from quetzal.client.exceptions import QuetzalAPIException


def name_option(required=True):
    extra_kwargs = {}
    if required:
        extra_kwargs['cls'] = OneRequiredOption
        extra_kwargs['one_of_with'] = ['id']
    else:
        extra_kwargs['cls'] = MutexOption
        extra_kwargs['not_required_if'] = ['id']

    def decorator(f):
        def callback(ctx, param, value):
            if value and not ctx.resilient_parsing:
                state = ctx.ensure_object(State)
                if not state.api_config.username:
                    raise click.BadOptionUsage(
                        param,
                        'Using --name to refer to a workspace requires a '
                        'the --username options to be set because the workspace '
                        'is uniquely identified by the name and username. '
                        'Alternatively, use the --id option to set the workspace.',
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
    else:
        extra_kwargs['cls'] = MutexOption
        extra_kwargs['not_required_if'] = ['name']

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
def workspace_group():
    """Workspace operations."""
    pass


@workspace_group.command()
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
    """Create a workspace."""
    client = state.api_client
    families = {tup[0]: tup[1] for tup in families}
    progress = _progress.generic_progress('Workspace created and initialized.')
    w_details = helpers.workspace.create(client, name, description, families, wait,
                                         progress=progress)
    _print_details(w_details)


@workspace_group.command(name='list')
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
    """List workspaces."""
    client = state.api_client

    results, total = helpers.workspace.list_(client, name, owner, deleted, limit)
    if not results:
        click.secho('No workspaces found.', fg='yellow')
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
    _print_table(results, columns, total)


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@help_options
@pass_state
def details(state, name, wid):
    """Show workspace details."""
    # TODO: add username option
    client = state.api_client
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    _print_details(w_details)


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will commit the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def commit(state, name, wid, wait):
    """Commit a workspace."""

    client = state.api_client

    # Get the workspace details
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    # Do the commit
    progress = _progress.commit_progress()
    w_details = helpers.workspace.commit(client, w_details.id, wait, progress=progress)

    _print_details(w_details)


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will update the workspace views. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is ready.')
@help_options
@pass_state
def scan(state, name, wid, wait):
    """Scan a workspace."""

    client = state.api_client

    # Get the workspace details
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    # Do the scan
    progress = _progress.scan_progress()
    w_details = helpers.workspace.scan(client, w_details.id, wait, progress=progress)

    _print_details(w_details)


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--limit', type=click.INT, default=10, show_default=True,
              help='Limit the number of results.')
@help_options
@pass_state
def files(state, name, wid, limit):
    """List files on a workspace."""
    client = state.api_client

    # Get the workspace details
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    limit = min(limit, 1000)
    file_list, total = helpers.workspace.files(client, w_details.id, limit=limit)

    if not file_list:
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
    _print_table(file_list, columns, total)


@workspace_group.command()
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
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    file_details = helpers.workspace.upload(client, w_details.id, file)
    click.secho(f'File {file.name} uploaded successfully. Its id is {file_details.id}.',
                fg='green')


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@click.confirmation_option(prompt='This will delete the workspace. Are you sure?')
@click.option('--wait', is_flag=True, help='Wait until the workspace is deleted.')
@help_options
@pass_state
def delete(state, name, wid, wait):
    """Delete a workspace."""

    client = state.api_client

    # Get the workspace details
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

    # Delete it
    progress = _progress.generic_progress('Workspace deleted.')
    helpers.workspace.delete(client, w_details.id, wait=wait, progress=progress)


@workspace_group.command()
@error_wrapper
@workspace_identifier_options()
@click.option('--file-id', required=True,
              help='File identifier whose metadata will be updated.')
@click.option('--metadata-file', type=click.File('r'),
              help='JSON file with metadata.')
@help_options
@pass_state
def update_metadata(state, name, wid, file_id, metadata_file):
    """Update the metadata of a file in a workspace."""

    client = state.api_client

    # Get the workspace details
    w_details = helpers.workspace.details(client, wid, name)
    if w_details is None:
        # Can only happen when the name is used and there are no results. Not
        # with the wid option because it would raise a 404 QuetzalAPIException
        raise click.ClickException(f'Workspace named "{name}" does not exist.')

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
        _csv_dump(table, file)
    else:
        raise ValueError('Invalid output format')


def _csv_dump(table, filename):
    with open(filename.name, 'w') as f:
        if not table:
            return
        writer = csv.DictWriter(f, table[0].keys())
        writer.writeheader()
        writer.writerows(table)


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
