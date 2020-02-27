import pathlib
import sys

import click
import json
import yaml

from quetzal.client import helpers
from quetzal.client.cli import BaseGroup, help_options, pass_state, error_wrapper, MutexOption
from quetzal.client.cli.workspace import workspace_identifier_options, _get_details


@click.group('file', options_metavar='[FILE OPTIONS]', cls=BaseGroup)
def file_group():
    """File operations."""
    pass


@file_group.command()
@error_wrapper
@click.argument('file_id')
@click.option('--output', cls=MutexOption, not_required_if=['output_dir'],
              help='Output file. If not set, the --output-dir naming approach is used.')
@click.option('--output-dir', cls=MutexOption, not_required_if=['output'],
              default='quetzal-data', show_default=True,
              help=f'Output directory. When set, it uses this directory with '
                   f'the path and filename entries of the base metadata to '
                   f'save the file as '
                   f'{pathlib.Path("output-dir") / "path" / "filename"}.')
@workspace_identifier_options(required=False)
@help_options
@pass_state
def download(state, file_id, output, output_dir, name, wid):
    """Download a file in a workspace"""
    client = state.api_client

    if name is not None or wid is not None:
        w_details = helpers.workspace.details(client, wid, name)
        if w_details is None:
            # Can only happen when the name is used and there are no results. Not
            # with the wid option because it would raise a 404 QuetzalAPIException
            raise click.ClickException(f'Workspace named "{name}" does not exist.')
        wid = w_details.id

    saved_file = helpers.file.download(client, file_id, wid=wid, output=output, output_dir=output_dir)
    click.secho(f'Downloaded file: {saved_file}', fg='green')


@file_group.command()
@error_wrapper
@click.argument('file_id')
@click.option('--output', help='Output file.',
              type=click.File('w'), default=sys.stdout)
@click.option('--format', 'output_format', help='Output file format.',
              type=click.Choice(['json', 'yaml']), default='json')
@workspace_identifier_options(required=False)
@help_options
@pass_state
def metadata(state, file_id, output, output_format, name, wid):
    """Download the metadata of a file"""
    if output_format is None:
        if hasattr(output, 'name'):
            output_filename = pathlib.Path(output.name)
            ext = output_filename.suffix[1:]
            if ext not in ('json', 'yaml', 'yml'):
                raise click.BadParameter(f'No format provided: "{ext}" is not supported. '
                                         f'Set the format with --format')
            output_format = ext

    client = state.api_client

    if name is not None or wid is not None:
        w_details = helpers.workspace.details(client, wid, name)
        if w_details is None:
            # Can only happen when the name is used and there are no results. Not
            # with the wid option because it would raise a 404 QuetzalAPIException
            raise click.ClickException(f'Workspace named "{name}" does not exist.')
        wid = w_details.id

    meta = helpers.file.metadata(client, file_id, wid=wid)

    if output_format == 'json':
        json.dump(meta, output, indent=2)
    elif output_format in ('yaml', 'yml'):
        yaml.safe_dump(meta, output, default_flow_style=False)
    else:
        raise ValueError('Invalid output format')


@file_group.command()
@error_wrapper
@click.argument('file_id')
@workspace_identifier_options(required=True)
@help_options
@pass_state
def delete(state, file_id, name, wid):
    client = state.api_client

    if name is not None or wid is not None:
        w_details = helpers.workspace.details(client, wid, name)
        if w_details is None:
            # Can only happen when the name is used and there are no results. Not
            # with the wid option because it would raise a 404 QuetzalAPIException
            raise click.ClickException(f'Workspace named "{name}" does not exist.')
        wid = w_details.id

    ctx = click.get_current_context()

    meta = helpers.file.metadata(client, file_id, wid=wid)
    base_meta = meta['base']
    state = base_meta['state']
    if state == 'DELETED':
        click.secho(f'File {file_id} is already a deleted file', fg='red')
        ctx.exit(-1)
        return
    if state in 'READY':
        confirm = click.confirm(f'File {file_id} is not temporary, are you sure you want to delete it?')
        if not confirm:
            click.secho('User aborted operation', fg='red')
            ctx.exit(-1)
            return

    click.echo(f'Requesting delete of file {file_id}...')
    helpers.file.delete(client, file_id, wid=wid)
