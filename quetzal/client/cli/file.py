import pathlib

import click

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
                   'path + filename of the base metadata family',)
@workspace_identifier_options
@pass_state
def download(state, file_id, output, output_dir, name, wid):
    """Download a file in a workspace"""
    client = state.api_client
    # Get the workspace details
    w_details = _get_details(state, name, wid)

    if output is None:
        metadata = client.data_file_details_w(wid=w_details.id, uuid=file_id,
                                              accept='application/json',
                                              _preload_content=True)
        base = metadata['metadata']['base']
        output = pathlib.Path(output_dir or '.') / base['path'] / base['filename']
    else:
        output = pathlib.Path(output)

    response = client.data_file_details_w(wid=w_details.id, uuid=file_id,
                                          accept='application/octet-stream',
                                          _preload_content=False)

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, 'wb') as f:
        f.write(response.data)

    click.secho(f'File {output} downloaded!', fg='green')
