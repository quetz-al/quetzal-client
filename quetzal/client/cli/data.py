import click

from quetzal.client.cli import BaseGroup, help_options
from quetzal.client.cli.workspace import workspace
from quetzal.client.cli.file import file


@click.group('data', options_metavar='[DATA OPTIONS]', cls=BaseGroup)
@help_options
def data_group():
    """Data API operations"""
    pass


data_group.add_command(workspace)
data_group.add_command(file)
