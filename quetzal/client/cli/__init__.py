from contextlib import contextmanager

import click

from quetzal.client.api_client import Client
from quetzal.client.configuration import Configuration


class State(object):

    def __init__(self):
        self.api_config = Configuration()
        self.api_client = Client(self.api_config)


# Decorator to obtain the state directly. Use with @pass_state
pass_state = click.make_pass_decorator(State, ensure=True)


def _collect_options(cmd, ctx, list_help=True):
    opts = []
    for param in cmd.get_params(ctx):
        if not list_help and param.name in ('help', 'help_all'):
            continue
        rv = param.get_help_record(ctx)
        if rv is not None:
            opts.append(rv)
    return opts


def _format_options(cmd, ctx, formatter, list_help=True):
    """Writes all the options into the formatter if they exist."""
    opts = _collect_options(cmd, ctx, list_help)

    if opts:
        if cmd.options_metavar:
            title = cmd.options_metavar.replace('[', '').replace(']', '')
        else:
            title = 'Options'
        with formatter.section(title):
            formatter.write_dl(opts)


def _format_help(ctx):
    # We are going to need to do some operations on the parent contexts, but
    # traversing this by .parent gives a reversed result
    parent_contexts = []
    current = ctx.parent
    while current is not None:
        parent_contexts.append(current)
        current = current.parent
    parent_contexts = parent_contexts[::-1]

    formatter = ctx.make_formatter()

    # Obtain the correct usage considering the options of parent commands
    pieces = []
    for parent in parent_contexts:
        parent_pieces = parent.command.collect_usage_pieces(parent)
        # Change 'COMMAND [ARGS]...' with the instantiation of the command
        parent_pieces[1] = parent.info_name
        # Remove '[OPTIONS]' if there are none
        has_options = bool(_collect_options(parent.command, parent, list_help=False))
        if not has_options:
            parent_pieces.pop(0)
        pieces.extend(parent_pieces[::-1])
    pieces.append(ctx.info_name)
    pieces.extend(ctx.command.collect_usage_pieces(ctx))
    prog = pieces[0]
    args = pieces[1:]
    formatter.write_usage(prog, ' '.join(args))

    # Add the help_text of the current command
    ctx.command.format_help_text(ctx, formatter)

    # Add the options of parent command but not their sub-commands
    for parent in parent_contexts:
        _format_options(parent.command, parent, formatter, list_help=False)

    # Add the options of this command
    _format_options(ctx.command, ctx, formatter, list_help=True)
    # ...and its available sub-commands if it is a MultiCommand
    if isinstance(ctx.command, click.MultiCommand):
        ctx.command.format_commands(ctx, formatter)

    # Finally, the epilog of this command
    ctx.command.format_epilog(ctx, formatter)

    # Show the message
    help_text = formatter.getvalue().rstrip('\n')
    click.echo(help_text, color=ctx.color)
    ctx.exit()


def all_help_option(f):
    def callback(ctx, param, value):
        if value and not ctx.resilient_parsing:
            _format_help(ctx)

    return click.option('--help-all',
                        help='Show a detailed help message with all options and exit.',
                        is_eager=True, expose_value=False, is_flag=True,
                        callback=callback)(f)


def help_options(f):
    f = click.help_option(help='Show help message for this command and exit.')(f)
    f = all_help_option(f)
    return f
