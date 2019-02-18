import pathlib
import sys

import click
import json
import yaml

from quetzal.client.cli import BaseGroup, help_options, pass_state, error_wrapper, MutexOption
from quetzal.client.cli.workspace import workspace_identifier_options, _get_details


@click.group('file', options_metavar='[FILE OPTIONS]', cls=BaseGroup)
def file():
    """File operations."""
    pass


@file.command()
@error_wrapper
@click.argument('file_id')
@click.option('--output', cls=MutexOption, not_required_if=['output_dir'],
              help='Output file. If not set, uses the path + filename from '
                   'the base metadata family.')
@click.option('--output-dir', cls=MutexOption, not_required_if=['output'],
              default='data', show_default=True,
              help='Output directory. When set, it uses this directory + '
                   'path + filename of the base metadata family')
@workspace_identifier_options
@pass_state
def download(state, file_id, output, output_dir, name, wid):
    """Download a file in a workspace"""
    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    if output is None:
        response = client.data_file_details_w(wid=w_details.id, uuid=file_id,
                                              _accept='application/json',
                                              _preload_content=True)
        base = response['metadata']['base']
        output = pathlib.Path(output_dir or '.') / base['path'] / base['filename']
    else:
        output = pathlib.Path(output)

    response = client.data_file_details_w(wid=w_details.id, uuid=file_id,
                                          _accept='application/octet-stream',
                                          _preload_content=False)

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        f.write(response.data)

    click.secho(f'File {output} downloaded!', fg='green')


@file.command()
@error_wrapper
@click.argument('file_id')
@click.option('--output', help='Output file.',
              type=click.File('w'), default=sys.stdout)
@click.option('--format', 'output_format', help='Output file format.',
              type=click.Choice(['json', 'yaml']), default='json')
@workspace_identifier_options
@pass_state
def metadata(state, file_id, output, output_format, name, wid):
    """Download the metadata of a file"""
    if output_format is None:
        if hasattr(output, 'name'):
            output_filename = pathlib.Path(output.name)
            ext = output_filename.suffix[1:]
            if ext not in ('json', 'yaml'):
                raise click.BadParameter(f'No format provided: "{ext}" is not supported. '
                                         f'Set the format with --format')
            output_format = ext

    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    response = client.data_file_details_w(wid=w_details.id, uuid=file_id,
                                          _accept='application/json',
                                          _preload_content=True)
    meta = response['metadata']

    if output_format == 'json':
        json.dump(meta, output, indent=2)
    elif output_format == 'yaml':
        yaml.safe_dump(meta, output, default_flow_style=False)
    else:
        raise ValueError('Invalid output format')
