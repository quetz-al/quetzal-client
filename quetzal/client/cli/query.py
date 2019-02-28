import pathlib
import sys

import click

from quetzal.client.cli import error_wrapper, MutexOption, rename_kwargs, \
    help_options, pass_state
from quetzal.client.cli.workspace import workspace_identifier_options, \
    _get_details, _save_results, _print_table
from quetzal.client.utils import HistoryConsole


@click.command('query')
@error_wrapper
@workspace_identifier_options(required=False)
@click.option('--input', 'query_file', type=click.File('r'),
              help='Input query file. If not set, a query will be requested '
                   'on the console.', default=sys.stdin)
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
def query_command(state, name, wid, query_file, dialect, limit, retrieve_all, output, output_format):
    """Query metadata."""

    if name is None and wid is None:
        raise click.ClickException('Query outside a workspace is not implemented yet.')

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

    limit = 100_000 if retrieve_all else min(limit, 100)
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
        click.secho(f'Saved {len(results)} out of {query_details.total} results '
                    f'in {output.name}.')
